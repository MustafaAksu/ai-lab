#!/usr/bin/env python3
"""VERIFY v2 writer: run a declared profile against one exact commit and write a receipt.

PLAN-20261124-0001 S2, admitted under WARR-20261124-0001.

The writer executes the profile's commands itself, in a detached git worktree of
the subject commit, and records what it observed. No argument accepts an exit
code, output, summary or result: every result in the receipt is produced by the
run it describes.

The receipt is a producer's claim of observation ("observed_by_writer"). It does
not establish that the writer is independent of the code it checks, that a
command tests its declared property, or, when produced in CI, that the claimed
runner produced it. verifier_lineage_status is always "self_authored_unreviewed".

Standard library only, and nothing is imported from ai_lab, so that the
verifier's identity is this one file.

Exit codes: 0 result all_commands_exit_zero; 1 one_or_more_commands_failed;
3 either a valid incomplete receipt or a failure to finish a receipt; 2 refused
before running (no receipt is written). A failure to finish publishes no receipt
and attempts a separate, bounded failure diagnostic outside the blob store.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from importlib import metadata
from pathlib import Path, PurePosixPath

RECEIPT_SCHEMA = "ai-lab/verify-v2-receipt/1"
PROFILE_SCHEMA = "ai-lab/verify-v2-profile/1"
FAILURE_SCHEMA = "ai-lab/verify-v2-failure/1"
FAILURE_DIAGNOSTIC_LIMIT_BYTES = 2048
WRITER_PATH = "scripts/verify_v2.py"
RETENTION_LIMIT_BYTES = 8 * 1024 * 1024
LINEAGE = "self_authored_unreviewed"
BASE_ENVIRONMENT_NAMES = ("PATH", "HOME", "LANG", "TZ")
TREE_OBSERVATION_METHOD = (
    "git rev-parse HEAD and git status --porcelain=v1 --untracked-files=all --ignored -z"
)
TREE_OBSERVATION_SCOPE = (
    "command_boundaries_only: Git-status-reported paths only, not byte-level tree equality; "
    "status-hidden changes (including assume-unchanged) and a path changed and restored "
    "within one command are not detected"
)
FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
ENV_NAME_RE = re.compile(r"^[A-Z_][A-Z0-9_]*$")
SECRET_NAME_RE = re.compile(r"(KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|AUTH)", re.IGNORECASE)
RESULTS = ("all_commands_exit_zero", "one_or_more_commands_failed", "incomplete")
TERMINATIONS = ("exited", "timeout", "signal", "failed_to_start")


class Refusal(Exception):
    """Raised when the writer refuses to run; no receipt is written."""


FAILURE_STAGES = frozenset({
    "preflight", "prepare_worktree", "check_writer", "load_profile", "capture_environment",
    "capture_runner", "observe_initial", "run_command", "assemble_receipt", "cleanup",
    "serialize_receipt", "store_receipt", "publish_receipt", "unknown",
})


def _safe_error_type(error: Exception) -> str:
    """Classify without serializing exception messages, reprs, or payloads."""
    for kind in (FileExistsError, PermissionError, FileNotFoundError, OSError,
                 subprocess.CalledProcessError, subprocess.TimeoutExpired,
                 UnicodeError, json.JSONDecodeError, ValueError, TypeError, RuntimeError):
        if isinstance(error, kind):
            return kind.__name__
    return "Exception"


class WriterFailure(Exception):
    """A sanitized failure to complete a receipt; never a verification record."""

    def __init__(self, stage: str, error: Exception) -> None:
        self.stage = stage if stage in FAILURE_STAGES else "unknown"
        self.error_type = _safe_error_type(error)
        super().__init__(f"{self.stage}: {self.error_type}")


# ---------------------------------------------------------------- pure functions
# ai_lab/documentation/verification_v2.py carries an independent copy of these
# two functions for validation; tests/test_verify_v2.py checks they agree.


def compute_result(profile_command_count: int, commands: list[dict], initial_boundary: dict) -> str:
    """Return the receipt result with precedence incomplete, then failed, then success."""

    complete = (
        profile_command_count > 0
        and len(commands) == profile_command_count
        and all(c.get("termination") == "exited" and isinstance(c.get("exit_code"), int)
                and not isinstance(c.get("exit_code"), bool) for c in commands)
    )
    boundaries = [initial_boundary] + [c.get("boundary_after") or {} for c in commands]
    disallowed_change = any(
        not (b.get("head_matches_subject") is True and b.get("status_clean") is True) for b in boundaries
    )
    if not complete or disallowed_change:
        return "incomplete"
    if any(c["exit_code"] != 0 for c in commands):
        return "one_or_more_commands_failed"
    return "all_commands_exit_zero"


def compute_output_retention(commands: list[dict]) -> str:
    for command in commands:
        for stream in ("stdout", "stderr"):
            if (command.get(stream) or {}).get("capture_complete") is not True:
                return "partial"
    return "complete"


def store_relative_path(digest: str) -> str:
    return f"sha256/{digest[:2]}/{digest}"


# ---------------------------------------------------------------- helpers


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="microseconds")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=check,
    )


def _git_text(repo: Path, *args: str) -> str:
    return _git(repo, *args).stdout.decode("utf-8").strip()


def _atomic_write_exclusive(path: Path, data: bytes) -> None:
    """Publish complete bytes atomically without replacing any existing name.

    The temporary file is on the destination filesystem. Linking is atomic and
    refuses an existing destination, unlike a replacing rename. No final path
    becomes visible until writing and fsync have succeeded.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".verify-v2-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass  # A staging-file cleanup failure cannot invalidate published bytes.


class Store:
    """Content-addressed blob store: <root>/sha256/<first two hex>/<digest>."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.created: set[Path] = set()

    def put(self, data: bytes) -> tuple[str, str]:
        digest = _sha256(data)
        relative = store_relative_path(digest)
        path = self.root / relative
        try:
            _atomic_write_exclusive(path, data)
        except FileExistsError:
            if path.read_bytes() != data:
                raise RuntimeError(f"store collision with different bytes at {relative}")
        else:
            self.created.add(path)
        return digest, relative


def _stream_record(store: Store, data: bytes) -> dict:
    retained = data[:RETENTION_LIMIT_BYTES]
    digest, relative = store.put(retained)
    return {
        "observed_bytes": len(data),
        "retained_bytes": len(retained),
        "sha256": digest,
        "store_path": relative,
        "capture_complete": len(retained) == len(data),
    }


def _load_profile(worktree: Path, profile_arg: str) -> tuple[bytes, dict]:
    posix = PurePosixPath(profile_arg)
    if posix.is_absolute() or Path(profile_arg).is_absolute():
        raise Refusal("profile path must be relative to the subject tree")
    if ".." in posix.parts:
        raise Refusal("profile path must not escape the subject tree")
    path = (worktree / profile_arg).resolve()
    if worktree.resolve() not in path.parents:
        raise Refusal("profile path resolves outside the subject tree")
    if not path.is_file():
        raise Refusal(f"profile is absent at the subject commit: {profile_arg}")
    data = path.read_bytes()
    try:
        profile = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"profile is not valid JSON: {error}") from error
    _check_profile(profile)
    return data, profile


def _check_profile(profile: object) -> None:
    if not isinstance(profile, dict) or profile.get("profile_schema") != PROFILE_SCHEMA:
        raise Refusal(f"profile_schema must be {PROFILE_SCHEMA}")
    if not isinstance(profile.get("profile_id"), str) or not profile["profile_id"] or "\0" in profile["profile_id"]:
        raise Refusal("profile_id must be a non-empty NUL-free string")
    if profile.get("permitted_tree_changes") != []:
        raise Refusal("this writer supports only profiles that permit no tree change")
    environment = profile.get("environment")
    if not isinstance(environment, dict):
        raise Refusal("profile environment must be an object of literal values")
    for name, value in environment.items():
        if not isinstance(name, str) or not ENV_NAME_RE.fullmatch(name) or name in BASE_ENVIRONMENT_NAMES:
            raise Refusal("profile environment name not allowed")
        if SECRET_NAME_RE.search(name):
            raise Refusal("profile environment name looks like a secret")
        if not isinstance(value, str) or "$" in value or "\0" in value:
            raise Refusal("profile environment values must be literal NUL-free strings")
    commands = profile.get("commands")
    if not isinstance(commands, list) or not commands:
        raise Refusal("profile must declare at least one command")
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            raise Refusal(f"profile command {index} must be an object")
        argv = command.get("argv")
        if (not isinstance(argv, list) or not argv
                or not all(isinstance(a, str) and a and "\0" not in a for a in argv)):
            raise Refusal(f"profile command {index} argv must be a non-empty list of NUL-free strings")
        timeout = command.get("timeout_seconds")
        if (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)
                or (isinstance(timeout, float) and not math.isfinite(timeout))
                or not (0 < timeout < 86400)):
            raise Refusal(f"profile command {index} timeout_seconds must be positive and finite")
        if (not isinstance(command.get("declared_property"), str) or not command["declared_property"]
                or "\0" in command["declared_property"]):
            raise Refusal(f"profile command {index} declared_property must be a non-empty NUL-free string")


def _boundary(worktree: Path, subject: str) -> dict:
    head = _git(worktree, "rev-parse", "HEAD", check=False)
    head_text = head.stdout.decode("utf-8").strip() if head.returncode == 0 else None
    status = _git(
        worktree, "status", "--porcelain=v1", "--untracked-files=all", "--ignored", "-z", check=False
    )
    entries = [e for e in status.stdout.decode("utf-8", "replace").split("\0") if e] if status.returncode == 0 else None
    return {
        "head": head_text,
        "head_matches_subject": head_text == subject,
        "status_clean": entries == [],
        "changed_paths": entries if entries is not None else ["<git status failed>"],
    }


def _resolve_argv(template: list[str], scratch: Path) -> list[str]:
    resolved = []
    for token in template:
        if token == "{python}":
            resolved.append(sys.executable)
        else:
            resolved.append(token.replace("{scratch}", str(scratch)))
    return resolved


def _command_environment(profile: dict, home: Path) -> dict:
    git_path = shutil.which("git")
    path_entries = []
    if git_path:
        path_entries.append(str(Path(git_path).parent))
    for entry in ("/usr/bin", "/bin"):
        if entry not in path_entries:
            path_entries.append(entry)
    environment = {
        "PATH": ":".join(path_entries),
        "HOME": str(home),
        "LANG": "C.UTF-8",
        "TZ": "UTC",
    }
    environment.update(profile["environment"])
    return environment


def _run_command(index: int, spec: dict, worktree: Path, scratch: Path, env: dict, store: Store, subject: str) -> dict:
    argv = _resolve_argv(spec["argv"], scratch)
    started = _now()
    termination = "exited"
    exit_code = None
    signal_number = None
    stdout = b""
    stderr = b""
    try:
        completed = subprocess.run(
            argv,
            cwd=worktree,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=spec["timeout_seconds"],
        )
        stdout, stderr = completed.stdout, completed.stderr
        if completed.returncode < 0:
            termination = "signal"
            signal_number = -completed.returncode
        else:
            exit_code = completed.returncode
    except subprocess.TimeoutExpired as error:
        termination = "timeout"
        stdout = error.stdout or b""
        stderr = error.stderr or b""
    except OSError as error:
        termination = "failed_to_start"
        stderr = f"{_safe_error_type(error)}: command could not start".encode("utf-8")
    finished = _now()
    record = {
        "index": index,
        "argv_template": list(spec["argv"]),
        "argv": argv,
        "cwd": ".",
        "timeout_seconds": spec["timeout_seconds"],
        "declared_property": spec["declared_property"],
        "termination": termination,
        "exit_code": exit_code,
        "started_at": started,
        "finished_at": finished,
        "stdout": _stream_record(store, stdout),
        "stderr": _stream_record(store, stderr),
        "boundary_after": _boundary(worktree, subject),
    }
    if signal_number is not None:
        record["signal"] = signal_number
    return record


def _installed_distributions() -> bytes:
    names = sorted(
        {f"{(d.metadata['Name'] or '').lower()}=={d.version}" for d in metadata.distributions() if d.metadata["Name"]}
    )
    return ("\n".join(names) + "\n").encode("utf-8")


def _runner(kind: str, worktree: Path) -> tuple[dict, dict]:
    runner = {"kind": kind}
    subject_extra: dict = {}
    if kind == "github_actions":
        for key, name in (
            ("run_id", "GITHUB_RUN_ID"),
            ("run_attempt", "GITHUB_RUN_ATTEMPT"),
            ("workflow_ref", "GITHUB_WORKFLOW_REF"),
            ("event_name", "GITHUB_EVENT_NAME"),
            ("runner_os", "RUNNER_OS"),
            ("image_os", "ImageOS"),
            ("image_version", "ImageVersion"),
        ):
            runner[key] = os.environ.get(name)
        for key in ("run_id", "run_attempt"):
            value = runner[key]
            if value is not None and not re.fullmatch(r"[1-9][0-9]*", value):
                raise RuntimeError("runner numeric metadata is malformed")
        for key in ("workflow_ref", "event_name", "runner_os", "image_os", "image_version"):
            value = runner[key]
            if value is not None and (not value or "\0" in value):
                raise RuntimeError("runner text metadata is malformed")
        workflow = worktree / ".github" / "workflows" / "verify-v2.yml"
        runner["workflow_file_sha256"] = _sha256(workflow.read_bytes()) if workflow.is_file() else None
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        if event_path and Path(event_path).is_file():
            event = json.loads(Path(event_path).read_text(encoding="utf-8"))
            pull = event.get("pull_request") if isinstance(event, dict) else None
            if isinstance(pull, dict):
                subject_extra = {
                    "pull_request": pull.get("number"),
                    "head_sha": (pull.get("head") or {}).get("sha"),
                    "base_sha": (pull.get("base") or {}).get("sha"),
                }
        runner["reported_by"] = "runner environment variables, unverified"
        if runner["event_name"] in ("pull_request", "pull_request_target") or subject_extra:
            number = subject_extra.get("pull_request")
            if (not isinstance(number, int) or isinstance(number, bool) or number <= 0
                    or not all(isinstance(subject_extra.get(key), str)
                               and FULL_COMMIT_RE.fullmatch(subject_extra[key])
                               for key in ("head_sha", "base_sha"))):
                raise RuntimeError("pull_request runner metadata is incomplete")
    return runner, subject_extra


def _history(repo: Path, worktree: Path, subject: str) -> dict:
    shallow = _git_text(repo, "rev-parse", "--is-shallow-repository") == "true"
    stored = None
    reachable = None
    index = worktree / "docs" / "self_model" / "SELF_MODEL.json"
    if index.is_file():
        try:
            payload = json.loads(index.read_text(encoding="utf-8"))
            stored = payload.get("repo_head") if isinstance(payload, dict) else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            stored = None
    if isinstance(stored, str) and FULL_COMMIT_RE.fullmatch(stored):
        reachable = _git(repo, "merge-base", "--is-ancestor", stored, subject, check=False).returncode == 0
    else:
        stored = None
    return {"shallow": shallow, "stored_repo_head": stored, "stored_repo_head_reachable": reachable}


def _tree_ids(repo: Path, subject: str) -> dict:
    trees = {"root": _git_text(repo, "rev-parse", f"{subject}^{{tree}}")}
    for name in ("tests", "scripts", "ai_lab"):
        result = _git(repo, "rev-parse", f"{subject}:{name}", check=False)
        trees[name] = result.stdout.decode("utf-8").strip() if result.returncode == 0 else None
    return trees


# ---------------------------------------------------------------- main run


def _write_receipt(
    repo: Path,
    commit: str,
    profile_arg: str,
    store_root: Path,
    receipt_out: Path,
    foreign_verifier: bool = False,
    runner_kind: str = "local",
    *,
    progress: dict,
) -> tuple[str, dict]:
    if not isinstance(commit, str) or not FULL_COMMIT_RE.fullmatch(commit):
        raise Refusal("--commit must be a full 40-hex commit id")
    if _git(repo, "cat-file", "-e", f"{commit}^{{commit}}", check=False).returncode != 0:
        raise Refusal(f"commit not found in repository: {commit}")
    if receipt_out.exists() or receipt_out.is_symlink():
        raise Refusal(f"refusing to overwrite existing receipt: {receipt_out}")

    running_bytes = Path(__file__).resolve().read_bytes()
    store = Store(store_root)
    progress["stage"] = "prepare_worktree"
    temp = Path(tempfile.mkdtemp(prefix="verify-v2-")).resolve()
    worktree = temp / "worktree"
    scratch = temp / "scratch"
    home = temp / "home"
    started = _now()
    try:
        scratch.mkdir()
        home.mkdir()
        _git(repo, "worktree", "add", "--detach", str(worktree), commit)

        progress["stage"] = "check_writer"
        subject_writer = worktree / WRITER_PATH
        if subject_writer.is_file():
            subject_writer_bytes = subject_writer.read_bytes()
            matches: object = subject_writer_bytes == running_bytes
            subject_blob = _git_text(repo, "rev-parse", f"{commit}:{WRITER_PATH}")
        else:
            matches = "absent_at_subject"
            subject_blob = None
        if matches is not True and not foreign_verifier:
            raise Refusal(
                "running writer differs from scripts/verify_v2.py at the subject commit "
                f"(verifier_matches_subject={matches}); use --foreign-verifier to run and record it"
            )

        progress["stage"] = "load_profile"
        profile_bytes, profile = _load_profile(worktree, profile_arg)
        profile_digest, profile_store_path = store.put(profile_bytes)
        progress["stage"] = "capture_environment"
        distributions = _installed_distributions()
        dist_digest, dist_store_path = store.put(distributions)
        requirements = worktree / "requirements.txt"
        progress["stage"] = "capture_runner"
        runner, subject_extra = _runner(runner_kind, worktree)
        env = _command_environment(profile, home)

        progress["stage"] = "observe_initial"
        initial = _boundary(worktree, commit)
        commands = []
        progress["stage"] = "run_command"
        for index, spec in enumerate(profile["commands"]):
            commands.append(_run_command(index, spec, worktree, scratch, env, store, commit))

        progress["stage"] = "assemble_receipt"
        subject = {"candidate_commit": commit, "tree_id": _git_text(repo, "rev-parse", f"{commit}^{{tree}}")}
        subject.update({k: v for k, v in subject_extra.items() if v is not None})
        receipt = {
            "receipt_schema": RECEIPT_SCHEMA,
            "observation_basis": "observed_by_writer",
            "subject": subject,
            "history": _history(repo, worktree, commit),
            "verifier": {
                "tool": WRITER_PATH,
                "running_sha256": _sha256(running_bytes),
                "subject_blob_sha": subject_blob,
                "verifier_matches_subject": matches,
                "interpreter": {"path": sys.executable, "version": platform.python_version()},
            },
            "inputs": {
                "trees": _tree_ids(repo, commit),
                "profile": {
                    "path": profile_arg,
                    "profile_id": profile["profile_id"],
                    "sha256": profile_digest,
                    "store_path": profile_store_path,
                },
            },
            "environment": {
                "environment_capture": "partial",
                "python": {
                    "implementation": platform.python_implementation(),
                    "version": platform.python_version(),
                },
                "platform": platform.platform(),
                "requirements_sha256": _sha256(requirements.read_bytes()) if requirements.is_file() else None,
                "installed_distributions": {
                    "sha256": dist_digest,
                    "store_path": dist_store_path,
                    "count": distributions.count(b"\n"),
                },
                "command_environment": env,
                "runner": runner,
            },
            "tree_observation": {
                "method": TREE_OBSERVATION_METHOD,
                "scope": TREE_OBSERVATION_SCOPE,
                "permitted_tree_changes": [],
                "initial": initial,
            },
            "retention_limit_bytes": RETENTION_LIMIT_BYTES,
            "started_at": started,
            "finished_at": _now(),
            "commands": commands,
            "verifier_lineage_status": LINEAGE,
        }
        receipt["result"] = compute_result(len(profile["commands"]), commands, initial)
        receipt["output_retention"] = compute_output_retention(commands)
    finally:
        prior_stage = progress["stage"]
        progress["stage"] = "cleanup"
        try:
            _git(repo, "worktree", "remove", "--force", str(worktree), check=False)
            _git(repo, "worktree", "prune", check=False)
            shutil.rmtree(temp, ignore_errors=True)
        except Exception:
            raise
        else:
            progress["stage"] = prior_stage

    progress["stage"] = "serialize_receipt"
    data = (json.dumps(receipt, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    progress["stage"] = "store_receipt"
    digest, relative = store.put(data)
    progress["stage"] = "publish_receipt"
    try:
        _atomic_write_exclusive(receipt_out, data)
    except Exception:
        # Keep pre-existing evidence. Remove only this run's newly published
        # receipt blob if the requested receipt name could not be published.
        stored_receipt = store_root / relative
        if stored_receipt in store.created:
            try:
                stored_receipt.unlink(missing_ok=True)
            except OSError:
                pass
        raise
    return digest, receipt


def write_receipt(
    repo: Path,
    commit: str,
    profile_arg: str,
    store_root: Path,
    receipt_out: Path,
    foreign_verifier: bool = False,
    runner_kind: str = "local",
) -> tuple[str, dict]:
    """Run once; a failure cannot expose a partially written receipt path."""
    progress = {"stage": "preflight"}
    try:
        return _write_receipt(repo, commit, profile_arg, store_root, receipt_out,
                              foreign_verifier, runner_kind, progress=progress)
    except Refusal:
        raise
    except Exception as error:
        raise WriterFailure(progress["stage"], error) from None


def _write_failure_diagnostic(receipt_out: Path, store_root: Path, failure: WriterFailure) -> Path | None:
    """Best-effort bounded diagnostic, outside CAS and not an importable receipt.

    Fields are fixed or sanitized type/stage labels. No exception message,
    traceback, command, environment, or captured output is included.
    """
    try:
        store = store_root.resolve()
        directory = receipt_out.parent.resolve()
        if directory == store or store in directory.parents:
            directory = store.parent
        if directory == store or store in directory.parents:
            return None
        payload = {
            "failure_schema": FAILURE_SCHEMA,
            "receipt_written": False,
            "exit_code": 3,
            "stage": failure.stage,
            "error_type": failure.error_type,
        }
        data = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
        if len(data) > FAILURE_DIAGNOSTIC_LIMIT_BYTES:
            return None
        path = directory / f"verify-v2-failure-{uuid.uuid4().hex}.json"
        _atomic_write_exclusive(path, data)
        return path
    except Exception:
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a VERIFY v2 profile against one exact commit.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="repository whose commit is checked out")
    parser.add_argument("--commit", required=True, help="full 40-hex subject commit")
    parser.add_argument("--profile", required=True, help="profile path relative to the subject tree")
    parser.add_argument("--store-root", required=True, type=Path, help="content-addressed store root")
    parser.add_argument("--receipt-out", required=True, type=Path, help="path for the receipt; never overwritten")
    parser.add_argument("--foreign-verifier", action="store_true", help="run even if this writer differs from the subject's")
    parser.add_argument("--runner-kind", choices=("local", "github_actions"), default="local")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        digest, receipt = write_receipt(
            repo=args.repo.resolve(),
            commit=args.commit,
            profile_arg=args.profile,
            store_root=args.store_root.resolve(),
            receipt_out=args.receipt_out.absolute(),
            foreign_verifier=args.foreign_verifier,
            runner_kind=args.runner_kind,
        )
    except Refusal as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    except Exception as error:  # the run could not be completed: no receipt, never success
        failure = error if isinstance(error, WriterFailure) else WriterFailure("unknown", error)
        diagnostic = _write_failure_diagnostic(args.receipt_out, args.store_root, failure)
        print(json.dumps({"receipt_written": False, "stage": failure.stage,
                          "error_type": failure.error_type,
                          "failure_diagnostic": str(diagnostic) if diagnostic is not None else None},
                         sort_keys=True), file=sys.stderr)
        return 3
    print(json.dumps({"receipt_sha256": digest, "result": receipt["result"],
                      "output_retention": receipt["output_retention"]}, sort_keys=True))
    return {"all_commands_exit_zero": 0, "one_or_more_commands_failed": 1}.get(receipt["result"], 3)


if __name__ == "__main__":
    sys.exit(main())
