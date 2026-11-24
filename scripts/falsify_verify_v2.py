"""Falsification before reliance for tests/test_verify_v2.py (PLAN-20261124-0001).

Each mutation runs in a private copy of one frozen working-tree snapshot. The
selected tests must first pass without the mutation, then collect and execute
the same exact nodeids with an ordinary call-phase assertion/test failure.
Collection, setup/teardown, internal, usage, environment and timeout errors are
not evidence that a mutation was caught. The source working tree is never edited.

    python3 -I scripts/falsify_verify_v2.py . --report /tmp/falsification.json

The report retains every selected nodeid, test report and complete process output
for both runs. Without --report the full JSON report is written to stdout. These
are local observations, not independent verification or a governance decision.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

W = "scripts/verify_v2.py"
V = "ai_lab/documentation/verification_v2.py"
I = "scripts/import_verification_v2.py"
C = "scripts/check_verification_outputs.py"
Y = ".github/workflows/verify-v2.yml"
T = "tests/test_verify_v2.py"

MUTATIONS = [
    ("F1 writer accepts an exit code", W,
     '    parser.add_argument("--runner-kind"', '    parser.add_argument("--exit-code")\n    parser.add_argument("--runner-kind"', "test_f1"),
    ("F2 failed mapped to success", W,
     '    if any(c["exit_code"] != 0 for c in commands):\n        return "one_or_more_commands_failed"\n    return "all_commands_exit_zero"\n\n\ndef compute_output_retention',
     '    return "all_commands_exit_zero"\n\n\ndef compute_output_retention', "test_f2 or test_f10_stale"),
    ("F3 abbreviated commit accepted", W,
     'FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")', 'FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")', "test_f3_abbreviated"),
    ("F3 invoking clone's working files leak into run", W,
     '        _git(repo, "worktree", "add", "--detach", str(worktree), commit)\n',
     '        _git(repo, "worktree", "add", "--detach", str(worktree), commit)\n        shutil.copyfile(repo / "tracked.txt", worktree / "tracked.txt") if (repo / "tracked.txt").exists() else None\n        _git(worktree, "update-index", "--assume-unchanged", "tracked.txt", check=False)\n',
     "test_f3_uncommitted"),
    ("F4 checker ignores blob address", C,
     '            if relative != verification_v2.store_relative_path(path.name) or path.name != digest:', '            if False:', "test_f4"),
    ("F5 profile read from invoking clone", W,
     "        profile_bytes, profile = _load_profile(worktree, profile_arg)", "        profile_bytes, profile = _load_profile(repo, profile_arg)", "test_f5_profile_is_read"),
    ("F5 escaping profile accepted", W,
     '    if ".." in posix.parts:\n        raise Refusal("profile path must not escape the subject tree")\n    path = (worktree / profile_arg).resolve()\n    if worktree.resolve() not in path.parents:\n        raise Refusal("profile path resolves outside the subject tree")',
     '    path = (worktree / profile_arg).resolve()', "test_f5_absolute or test_f5_dotdot or test_f5_symlink"),
    ("F6 worktree left behind", W,
     '            _git(repo, "worktree", "remove", "--force", str(worktree), check=False)\n            _git(repo, "worktree", "prune", check=False)\n            shutil.rmtree(temp, ignore_errors=True)', "            pass", "test_f6"),
    ("F7 v2 summary block not required", V,
     '    """Structure of a canonical VERIFY v2 record; needs no repository access."""\n',
     '    """Structure of a canonical VERIFY v2 record; needs no repository access."""\n'
     '    record.setdefault("summary", {"result": "all_commands_exit_zero", "output_retention": "complete", '
     '"commands": [{"declared_property": "unguarded", "termination": "exited", "exit_code": 0}]})\n',
     "test_f7_v2"),
    ("F8 writer claims independent lineage", W,
     'LINEAGE = "self_authored_unreviewed"', 'LINEAGE = "independent"', "test_f8"),
    ("F9 re-import not refused", I,
     "    if receipt_sha in _existing_receipt_shas(repo_root):", "    if False:", "test_f9"),
    ("F10/F14 boundaries ignored by result", W,
     "    if not complete or disallowed_change:\n        return \"incomplete\"\n    if any(c[\"exit_code\"] != 0 for c in commands):\n        return \"one_or_more_commands_failed\"\n    return \"all_commands_exit_zero\"\n\n\ndef compute_output_retention(commands: list[dict]) -> str:\n    for command in commands:",
     "    if not complete:\n        return \"incomplete\"\n    if any(c[\"exit_code\"] != 0 for c in commands):\n        return \"one_or_more_commands_failed\"\n    return \"all_commands_exit_zero\"\n\n\ndef compute_output_retention(commands: list[dict]) -> str:\n    for command in commands:",
     "test_f10_old or test_f14"),
    ("F11 foreign writer not refused", W,
     "        if matches is not True and not foreign_verifier:", "        if False:", "test_f11"),
    ("F12 timeout recorded as exit 0", W,
     '        termination = "timeout"\n', '        exit_code = 0\n', "test_f12"),
    ("F13 no retention limit", W,
     "    retained = data[:RETENTION_LIMIT_BYTES]", "    retained = data", "test_f13"),
    ("F14 ignored paths not observed", W,
     '"--untracked-files=all", "--ignored", "-z", check=False', '"--untracked-files=all", "-z", check=False', "test_f14_any"),
    ("F14 untracked paths not observed", W,
     '"--untracked-files=all", "--ignored", "-z", check=False', '"--untracked-files=no", "-z", check=False', "test_f14_any"),
    ("F14/Cond1 HEAD not checked", W,
     '        "head_matches_subject": head_text == subject,', '        "head_matches_subject": True,', "test_f14_head"),
    ("F15 upload not on always()", Y,
     "        if: always()\n", "", "test_f15"),
    ("F15 credentials persisted", Y,
     "          persist-credentials: false\n", "", "test_f15"),
    ("F16 store resolved from cwd", V,
     "    store_root = Path(repo_root) / STORE_RELATIVE_ROOT", "    store_root = Path.cwd() / STORE_RELATIVE_ROOT", "test_f16"),
    ("F17 result not recomputed", V,
     "    if receipt.get(\"result\") != expected_result:", "    if False:", "test_f17_receipt"),
    ("F17/Cond2 completeness against profile count dropped", V,
     "    expected_result = compute_result(len(profile_commands), commands, observation[\"initial\"])",
     "    expected_result = compute_result(len(commands), commands, observation[\"initial\"])", "test_f17_receipt"),
    ("F17/Cond2 argv template not compared", V,
     "        if data.get(\"argv_template\") != spec.get(\"argv\"):", "        if False:", "test_f17_receipt"),
    ("F17/Cond2 capture_complete not checked", V,
     "    if data.get(\"capture_complete\") is not (retained == observed):", "    if False:", "test_f17_receipt"),
    ("F17 repo_commit invariant dropped", V,
     "    if record[\"repo_commit\"] != receipt[\"subject\"][\"candidate_commit\"]:", "    if False:", "test_f17_record"),
    ("F17 origin not required unverified", V,
     "    if origin.get(\"origin_verification\") != ORIGIN_VERIFICATION:", "    if False:", "test_f17_record"),
    ("F17 store path not derived", V,
     "    if value != store_relative_path(digest):", "    if False:", "test_f17_record or test_f17_non_derived"),
    ("F17 store root containment dropped", V,
     "    if store_root.resolve() not in path.parents:\n        _fail(f\"{where} resolves outside the store root\")", "    pass", "test_f17_store"),
    ("F18/Cond3 parent environment passed", W,
     "    environment.update(profile[\"environment\"])\n    return environment", "    environment.update(profile[\"environment\"])\n    environment.update(os.environ)\n    return environment", "test_f18_environment"),
    ("F18/Cond3 secret-like profile names allowed", W,
     "        if SECRET_NAME_RE.search(name):", "        if False:", "test_f18_profile"),
    ("F18/Cond3 env allowlist not checked by validator", V,
     "    if set(command_env) != allowed:", "    if False:", "test_f17_receipt"),
    ("agreement: validator copy diverges", V,
     "        and len(commands) == profile_command_count\n", "", "test_result_and_retention_copies_agree"),
]

HISTORICAL_MUTATION_NAMES = frozenset(mutation[0] for mutation in MUTATIONS)

CONTRACT_TESTS = "tests/test_verification_v2_contract.py"
WRITER_REVIEW_TESTS = "tests/test_verify_v2_writer_review.py"
REVIEW_MUTATIONS = [
    ("R9 nullable field presence not required", V,
     "    if missing:\n", "    if False:\n",
     "test_r9_explicit_absence_is_valid_but_missing_fields_are_not", CONTRACT_TESTS),
    ("R9 bool accepted as integer index", V,
     "    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:",
     "    if not isinstance(value, int) or value < minimum:",
     "test_r9_receipt_rejects_invalid_scalar_types and index", CONTRACT_TESTS),
    ("R10 resolved argv not compared", V,
     '        if data.get("argv") != expected_argv:', '        if False:',
     "test_r10_resolved_command_cannot_contradict_template and executable", CONTRACT_TESTS),
    ("R10 cwd not constrained", V,
     '        if data.get("cwd") != ".":', '        if False:',
     "test_r10_resolved_command_cannot_contradict_template and cwd", CONTRACT_TESTS),
    ("R11 stored profile policy not checked", V,
     "    _check_profile(profile)\n    return profile", "    return profile",
     "test_r11_valid_cas_digest_does_not_admit_invalid_stored_profile and secret_environment", CONTRACT_TESTS),
    ("Section 7 receipt path published before fsync", W,
     '    descriptor, temporary_name = tempfile.mkstemp(prefix=".verify-v2-", dir=path.parent)',
     '    path.write_bytes(b"partial")\n'
     '    descriptor, temporary_name = tempfile.mkstemp(prefix=".verify-v2-", dir=path.parent)',
     "test_atomic_write_failure_does_not_publish_partial_bytes", WRITER_REVIEW_TESTS),
]
MUTATIONS += REVIEW_MUTATIONS


REPORT_SCHEMA = "verify-v2-falsification-v2"

# This plugin lives outside every tested copy. It records reports from pytest,
# rather than inferring test outcomes from process exit codes or terminal text.
PYTEST_PLUGIN = r'''
import json
import os
from pathlib import Path
import pytest

report_path = None
data = {"schema": "pytest-falsification-v1", "selected_nodeids": [], "reports": [], "collection_errors": [],
        "internal_errors": [], "interrupted": False, "session_finished": False}

def save():
    temporary = report_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=True), encoding="utf-8")
    os.replace(temporary, report_path)

def pytest_sessionstart(session):
    save()

def pytest_collection_finish(session):
    data["selected_nodeids"] = [item.nodeid for item in session.items]
    save()

def pytest_collectreport(report):
    if report.failed or report.skipped:
        data["collection_errors"].append({"nodeid": report.nodeid,
            "outcome": report.outcome, "longrepr": str(report.longrepr)})
        save()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.falsification_failure_kind = None
    report.falsification_exception = None
    if call.excinfo is not None:
        kind = call.excinfo.type
        report.falsification_exception = kind.__module__ + "." + kind.__qualname__
        if call.excinfo.errisinstance(AssertionError):
            report.falsification_failure_kind = "assertion"
        elif call.excinfo.errisinstance(pytest.fail.Exception):
            report.falsification_failure_kind = "pytest_fail"
        else:
            report.falsification_failure_kind = "exception"

def pytest_runtest_logreport(report):
    data["reports"].append({"nodeid": report.nodeid, "when": report.when,
        "outcome": report.outcome, "duration": report.duration,
        "failure_kind": getattr(report, "falsification_failure_kind", None),
        "exception": getattr(report, "falsification_exception", None),
        "wasxfail": getattr(report, "wasxfail", None),
        "longrepr": report.longreprtext,
        "sections": [list(section) for section in report.sections]})
    save()

def pytest_internalerror(excrepr, excinfo):
    data["internal_errors"].append(str(excrepr))
    save()

def pytest_keyboard_interrupt(excinfo):
    data["interrupted"] = True
    save()

def pytest_sessionfinish(session, exitstatus):
    data["exitstatus"] = int(exitstatus)
    data["session_finished"] = True
    save()
'''

PYTEST_BOOTSTRAP = r'''
import importlib.util
import sys
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location("falsification_report_plugin", sys.argv[1])
plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin)
plugin.report_path = Path(sys.argv[2])
sys.path.insert(0, str(Path.cwd()))
raise SystemExit(pytest.main(sys.argv[3:], plugins=[plugin]))
'''


class HarnessError(ValueError):
    """A falsification observation cannot safely be made."""


def _environment() -> dict[str, str]:
    # A caller's pytest flags/plugins or Git worktree overrides must not change
    # selection, stop after one failure, or redirect fixture Git writes.
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("PYTEST", "PYTHON", "GIT_"))}
    env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONDONTWRITEBYTECODE="1")
    return env


def _git(repo: Path, *args: str) -> bytes:
    try:
        proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                              timeout=30, env=_environment())
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise HarnessError(f"git observation failed: {exc}") from exc
    if proc.returncode:
        raise HarnessError(f"git observation failed: {proc.stderr.decode('utf-8', 'replace')}")
    return proc.stdout


def _source_files(repo: Path) -> list[str]:
    paths = _git(repo, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    return sorted({p.decode("utf-8") for p in paths.split(b"\0") if p})


def _file_state(repo: Path, names: list[str], destination: Path | None = None) -> list[dict]:
    entries = []
    for name in names:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or ".git" in relative.parts:
            raise HarnessError(f"unsafe snapshot path: {name}")
        path = repo / relative
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != repo):
            raise HarnessError(f"snapshot does not follow symlinks: {name}")
        if not path.exists():
            entries.append({"path": name, "missing": True})
            continue
        if not path.is_file():
            raise HarnessError(f"snapshot requires ordinary files: {name}")
        content = path.read_bytes()
        mode = path.stat().st_mode & 0o777
        entries.append({"path": name, "sha256": hashlib.sha256(content).hexdigest(), "mode": mode})
        if destination is not None:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            target.chmod(mode)
    return entries


def _snapshot(repo: Path, destination: Path) -> dict:
    top = Path(os.fsdecode(_git(repo, "rev-parse", "--show-toplevel")).strip()).resolve()
    if top != repo:
        raise HarnessError("repo must be the repository root")
    head = _git(repo, "rev-parse", "HEAD").decode().strip()
    status = _git(repo, "status", "--porcelain=v1", "--untracked-files=all").decode("utf-8", "replace")
    names = _source_files(repo)
    destination.mkdir()
    files = _file_state(repo, names, destination)
    if (names != _source_files(repo) or files != _file_state(repo, names)
            or head != _git(repo, "rev-parse", "HEAD").decode().strip()):
        raise HarnessError("source changed during snapshot; retry after concurrent edits finish")
    digest = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    # Never copy a linked worktree's .git pointer: all test Git operations must
    # address private metadata. No source hook, remote, or credential is copied.
    _git(destination, "init", "-q")
    _git(destination, "-c", "core.hooksPath=/dev/null", "add", "-f", "-A")
    _git(destination, "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
         "-c", "user.name=Falsification fixture", "-c", "user.email=fixture@ai-lab.invalid",
         "commit", "-q", "--allow-empty", "-m", "isolated falsification snapshot")
    return {"repo": str(repo), "source_head": head, "source_status": status,
            "snapshot_sha256": digest, "files": files}


def _stream(data: bytes) -> dict:
    """Retain exact bytes, using readable text when it is lossless."""
    try:
        value, encoding = data.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        value, encoding = base64.b64encode(data).decode("ascii"), "base64"
    return {"encoding": encoding, "data": value, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def _run_pytest(repo: Path, evidence: Path, test_path: str, selector: str,
                timeout: float, python: str) -> dict:
    evidence.mkdir()
    scratch = evidence / "tmp"
    scratch.mkdir()
    environment = _environment()
    # Cleanup-defeating mutants must not leave their worktrees or command scratch
    # outside this case. pytest fixtures and ordinary tempfile users are isolated.
    environment.update(TMPDIR=str(scratch), TEMP=str(scratch), TMP=str(scratch))
    plugin = evidence / "report_plugin.py"
    plugin.write_text(PYTEST_PLUGIN, encoding="utf-8")
    report_path = evidence / "pytest.json"
    config = evidence / "pytest.ini"
    config.write_text("[pytest]\n", encoding="utf-8")
    argv = [python, "-I", "-B", "-c", PYTEST_BOOTSTRAP, str(plugin), str(report_path),
            "-q", "-p", "no:cacheprovider", "-c", str(config), "--rootdir", str(repo),
            "--basetemp", str(evidence / "fixtures"), test_path, "-k", selector]
    observation = {"argv": argv, "timeout_seconds": timeout, "timed_out": False,
                   "returncode": None, "start_error": None, "report_error": None,
                   "pytest": None}
    stdout = stderr = b""
    try:
        proc = subprocess.Popen(argv, cwd=repo, env=environment, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, start_new_session=os.name == "posix")
    except OSError as exc:
        observation["start_error"] = f"{type(exc).__name__}: {exc}"
    else:
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            observation["timed_out"] = True
            if os.name == "posix":
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                proc.kill()
            stdout, stderr = proc.communicate()
        observation["returncode"] = proc.returncode
    observation.update(stdout=_stream(stdout), stderr=_stream(stderr))
    try:
        observation["pytest"] = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        observation["report_error"] = f"{type(exc).__name__}: {exc}"
    return observation


def _run_problem(run: dict, expected_nodeids: list[str] | None = None) -> str | None:
    """Require a complete, internally consistent pytest test execution."""
    if run.get("timed_out"):
        return "pytest timed out"
    if run.get("start_error"):
        return "pytest failed to start"
    if run.get("returncode") not in (0, 1):
        return f"pytest infrastructure/collection/usage exit {run.get('returncode')}"
    data = run.get("pytest")
    if not isinstance(data, dict) or run.get("report_error"):
        return "pytest report missing or unreadable"
    if (data.get("schema") != "pytest-falsification-v1"
            or not isinstance(data.get("collection_errors"), list)
            or not isinstance(data.get("internal_errors"), list)
            or type(data.get("interrupted")) is not bool):
        return "pytest report protocol fields missing or malformed"
    if data.get("session_finished") is not True or data.get("exitstatus") != run["returncode"]:
        return "pytest session incomplete or exit status inconsistent"
    if data.get("collection_errors") or data.get("internal_errors") or data.get("interrupted"):
        return "pytest collection/internal/interruption error"
    ids = data.get("selected_nodeids")
    if not isinstance(ids, list) or not ids or any(not isinstance(n, str) or not n for n in ids):
        return "no selected test nodeids"
    if len(ids) != len(set(ids)):
        return "duplicate selected nodeids"
    if expected_nodeids is not None and ids != expected_nodeids:
        return "mutation changed the exact selected nodeids"
    by_node = {nodeid: {} for nodeid in ids}
    reports = data.get("reports")
    if not isinstance(reports, list):
        return "test reports missing"
    failed = []
    for report in reports:
        if not isinstance(report, dict):
            return "malformed test report"
        nodeid, when = report.get("nodeid"), report.get("when")
        if nodeid not in by_node or when not in ("setup", "call", "teardown"):
            return "unexpected test nodeid or phase"
        if when in by_node[nodeid]:
            return "repeated test phase"
        by_node[nodeid][when] = report
        if report.get("wasxfail") is not None or report.get("outcome") not in ("passed", "failed"):
            return "skipped/xfail/non-test outcome"
        if report["outcome"] == "failed":
            if when != "call":
                return "setup/teardown failure"
            if report.get("failure_kind") not in ("assertion", "pytest_fail"):
                return f"non-assertion test exception: {report.get('exception')}"
            if not report.get("longrepr"):
                return "test failure output missing"
            failed.append(nodeid)
    if any(set(phases) != {"setup", "call", "teardown"} for phases in by_node.values()):
        return "selected tests did not all execute setup, call and teardown"
    if bool(failed) != (run["returncode"] == 1):
        return "test failures and process exit disagree"
    return None


def _mutation_spec(mutation: tuple) -> dict:
    if len(mutation) not in (5, 6):
        raise HarnessError("mutation needs name, path, old, new, selector, and optional test path")
    name, path, old, new, selector = mutation[:5]
    test_path = mutation[5] if len(mutation) == 6 else T
    if any(not isinstance(v, str) or not v for v in (name, path, old, selector, test_path)):
        raise HarnessError("mutation identity, anchor, selector and test path must be non-empty strings")
    if not isinstance(new, str) or new == old:
        raise HarnessError("mutation replacement must change the anchor")
    for value in (path, test_path):
        if Path(value).is_absolute() or ".." in Path(value).parts:
            raise HarnessError("mutation and test paths must stay inside the snapshot")
    return dict(name=name, path=path, old=old, new=new, selector=selector, test_path=test_path)


def run_mutations(repo: Path, mutations=None, *, timeout: float = 900,
                  python: str = sys.executable) -> dict:
    repo = Path(repo).resolve()
    if not isinstance(timeout, (int, float)) or not 0 < timeout < float("inf"):
        raise HarnessError("timeout must be finite and positive")
    specs = [_mutation_spec(m) for m in (MUTATIONS if mutations is None else mutations)]
    if not specs:
        raise HarnessError("at least one mutation is required")
    report = {"schema": REPORT_SCHEMA, "lineage": "self_authored_unreviewed",
              "results": [], "baselines": {}}
    with tempfile.TemporaryDirectory(prefix="verify-v2-falsification-") as temporary:
        root = Path(temporary)
        snapshot = root / "snapshot"
        report["source"] = _snapshot(repo, snapshot)
        baseline_keys = {}
        for index, spec in enumerate(specs):
            group = "historical_33" if spec["name"] in HISTORICAL_MUTATION_NAMES else "review_additions"
            result = dict(spec, group=group, status="ERROR", reason="", baseline_id=None,
                          mutation_run=None, failed_nodeids=[])
            report["results"].append(result)
            path = snapshot / spec["path"]
            if not path.is_file():
                result.update(status="NOT_APPLICABLE", reason="mutation file missing")
                continue
            original = path.read_bytes()
            old, new = spec["old"].encode(), spec["new"].encode()
            if original.count(old) != 1:
                result.update(status="NOT_APPLICABLE", reason="anchor does not occur exactly once")
                continue
            key = (spec["test_path"], spec["selector"])
            if key not in baseline_keys:
                baseline_id = f"baseline-{len(baseline_keys) + 1:03d}"
                baseline_keys[key] = baseline_id
                with tempfile.TemporaryDirectory(prefix=baseline_id + "-", dir=root) as work:
                    work = Path(work)
                    clone = work / "repo"
                    shutil.copytree(snapshot, clone)
                    report["baselines"][baseline_id] = _run_pytest(
                        clone, work / "evidence", *key, timeout, python)
            baseline_id = baseline_keys[key]
            result["baseline_id"] = baseline_id
            baseline = report["baselines"][baseline_id]
            problem = _run_problem(baseline)
            if problem or baseline["returncode"] != 0:
                result["reason"] = f"baseline did not pass: {problem or 'selected test failure'}"
                continue
            expected = baseline["pytest"]["selected_nodeids"]
            result["expected_nodeids"] = expected
            with tempfile.TemporaryDirectory(prefix=f"mutation-{index + 1:03d}-", dir=root) as work:
                work = Path(work)
                clone = work / "repo"
                shutil.copytree(snapshot, clone)
                (clone / spec["path"]).write_bytes(original.replace(old, new))
                result["mutation_run"] = _run_pytest(clone, work / "evidence", *key, timeout, python)
            mutated = result["mutation_run"]
            problem = _run_problem(mutated, expected)
            if problem:
                result["reason"] = problem
            elif mutated["returncode"] == 0:
                result.update(status="NOT_CAUGHT", reason="all selected tests passed under mutation")
            else:
                result.update(status="CAUGHT", reason="baseline passed; exact selected tests ran; call assertion failed",
                              failed_nodeids=[r["nodeid"] for r in mutated["pytest"]["reports"]
                                              if r["when"] == "call" and r["outcome"] == "failed"])
    caught = sum(r["status"] == "CAUGHT" for r in report["results"])
    report["summary"] = {"mutations": len(specs), "caught": caught,
                         "not_caught": len(specs) - caught,
                         "errors": sum(r["status"] == "ERROR" for r in report["results"])}
    report["summary"]["groups"] = {
        group: {"mutations": sum(r["group"] == group for r in report["results"]),
                "caught": sum(r["group"] == group and r["status"] == "CAUGHT" for r in report["results"])}
        for group in ("historical_33", "review_additions")}
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--timeout", type=float, default=900, help="timeout per selected pytest run")
    parser.add_argument("--report", type=Path, help="retain complete JSON evidence outside the source repository")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    destination = args.report.resolve() if args.report is not None else None
    if destination is not None and destination.is_relative_to(repo):
        parser.error("--report must be outside the source repository")
    try:
        report = run_mutations(repo, timeout=args.timeout)
    except (HarnessError, OSError, ValueError) as exc:
        report = {"schema": REPORT_SCHEMA, "error": f"{type(exc).__name__}: {exc}"}
        code = 2
    else:
        for result in report["results"]:
            print(f"{result['name']} | {result['status']} | {result['reason']}", file=sys.stderr)
        print(json.dumps(report["summary"]), file=sys.stderr)
        code = 0 if report["summary"]["not_caught"] == 0 else 1
    content = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
    if destination is None:
        print(content, end="")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent,
                                         prefix=destination.name + ".", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        try:
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
        print(f"Evidence: {destination}", file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
