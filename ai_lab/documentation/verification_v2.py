"""VERIFY v2 validation: canonical records and the receipts they are derived from.

PLAN-20261124-0001 S1(b)-(c), admitted under WARR-20261124-0001.

A receipt is the writer's raw output (scripts/verify_v2.py). A canonical VERIFY v2
record is derived from a receipt by scripts/import_verification_v2.py. Nothing
here establishes that a run took place where its receipt says: these checks
establish internal consistency and byte integrity only. CI origin stays
"unverified" and verifier lineage stays "self_authored_unreviewed".

compute_result and compute_output_retention are an independent copy of the
writer's functions (the writer imports nothing from ai_lab);
tests/test_verify_v2.py checks that the two copies agree.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path, PurePosixPath

RECEIPT_SCHEMA = "ai-lab/verify-v2-receipt/1"
PROFILE_SCHEMA = "ai-lab/verify-v2-profile/1"
RETENTION_LIMIT_BYTES = 8 * 1024 * 1024
LINEAGE = "self_authored_unreviewed"
ORIGIN_VERIFICATION = "unverified"
BASE_ENVIRONMENT_NAMES = frozenset({"PATH", "HOME", "LANG", "TZ"})
STORE_RELATIVE_ROOT = Path("docs") / "self_model" / "verification_outputs"
RESULTS = frozenset({"all_commands_exit_zero", "one_or_more_commands_failed", "incomplete"})
TERMINATIONS = frozenset({"exited", "timeout", "signal", "failed_to_start"})
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
VERIFICATION_ID_RE = re.compile(r"^VERIFY-[0-9]{8}-[0-9]{4}$")
ENV_NAME_RE = re.compile(r"^[A-Z_][A-Z0-9_]*$")
SECRET_NAME_RE = re.compile(r"(KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|AUTH)", re.IGNORECASE)
TIMESTAMP_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})$")
TREE_OBSERVATION_METHOD = "git rev-parse HEAD and git status --porcelain=v1 --untracked-files=all --ignored -z"
LEGACY_TREE_OBSERVATION_SCOPE = "command_boundaries_only: a path changed and restored within one command is not detected"
TREE_OBSERVATION_SCOPE = (
    "command_boundaries_only: Git-status-reported paths only, not byte-level tree equality; "
    "status-hidden changes (including assume-unchanged) and a path changed and restored within one command are not detected"
)


class VerificationV2Error(ValueError):
    """A VERIFY v2 record or receipt violates the contract."""


# ---------------------------------------------------------------- semantics (copy)


def compute_result(profile_command_count: int, commands: list[dict], initial_boundary: dict) -> str:
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


def summary_from_receipt(receipt: dict) -> dict:
    return {
        "result": receipt["result"],
        "output_retention": receipt["output_retention"],
        "commands": [
            {
                "declared_property": c["declared_property"],
                "termination": c["termination"],
                "exit_code": c["exit_code"],
            }
            for c in receipt["commands"]
        ],
    }


# ---------------------------------------------------------------- small checks


def _fail(message: str) -> None:
    raise VerificationV2Error(message)


def _mapping(value: object, where: str) -> dict:
    if not isinstance(value, dict):
        _fail(f"{where} must be an object")
    return value


def _required(value: object, fields: tuple[str, ...], where: str) -> dict:
    data = _mapping(value, where)
    missing = [name for name in fields if name not in data]
    if missing:
        _fail(f"{where} is missing required fields: {', '.join(missing)}")
    return data


def _string(value: object, where: str) -> str:
    if not isinstance(value, str) or not value or "\0" in value:
        _fail(f"{where} must be a non-empty string without NUL")
    return value


def _integer(value: object, where: str, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        _fail(f"{where} must be an integer >= {minimum}")
    return value


def _boolean(value: object, where: str) -> bool:
    if not isinstance(value, bool):
        _fail(f"{where} must be a boolean")
    return value


def _commit(value: object, where: str, *, nullable: bool = False) -> str | None:
    if nullable and value is None:
        return None
    if not isinstance(value, str) or not FULL_COMMIT_RE.fullmatch(value):
        _fail(f"{where} must be a full 40-hex git object id")
    return value


def _timestamp(value: object, where: str) -> datetime:
    if not isinstance(value, str) or not TIMESTAMP_RE.fullmatch(value):
        _fail(f"{where} must be an ISO-8601 timestamp with timezone")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise VerificationV2Error(f"{where} is not a valid timestamp") from error


def _absolute_path(value: object, where: str) -> PurePosixPath:
    text = _string(value, where)
    path = PurePosixPath(text)
    if not path.is_absolute() or ".." in path.parts or str(path) != text:
        _fail(f"{where} must be a normalized absolute path")
    return path


def _argv(value: object, where: str) -> list[str]:
    if not isinstance(value, list) or not value:
        _fail(f"{where} must be a non-empty list of strings")
    for index, token in enumerate(value):
        _string(token, f"{where}[{index}]")
    return value


def _timeout(value: object, where: str) -> None:
    if (not isinstance(value, (int, float)) or isinstance(value, bool)
            or not (0 < value < 86400)
            or (isinstance(value, float) and not math.isfinite(value))):
        _fail(f"{where} must be positive and finite, below 86400 seconds")


def _sha(value: object, where: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        _fail(f"{where} must be a 64-hex SHA-256")
    return value


def _check_store_path(value: object, digest: str, where: str) -> str:
    if value != store_relative_path(digest):
        _fail(f"{where} must equal the path derived from its digest ({store_relative_path(digest)})")
    return value  # type: ignore[return-value]


def _read_blob(store_root: Path, relative: str, digest: str, where: str) -> bytes:
    path = (store_root / relative).resolve()
    if store_root.resolve() not in path.parents:
        _fail(f"{where} resolves outside the store root")
    if not path.is_file():
        _fail(f"{where} is missing from the store: {relative}")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        _fail(f"{where} bytes do not match the recorded SHA-256")
    return data


def _check_runner(value: object, where: str) -> dict:
    runner = _required(value, ("kind",), where)
    kind = _string(runner.get("kind"), f"{where}.kind")
    if kind not in ("local", "github_actions"):
        _fail(f"{where}.kind must be local or github_actions")
    if kind == "github_actions":
        # Missing runner metadata is represented by an explicit null, never by
        # omitting its field. These are unverified reports, not origin proofs.
        fields = ("run_id", "run_attempt", "workflow_ref", "event_name", "runner_os",
                  "image_os", "image_version", "workflow_file_sha256", "reported_by")
        _required(runner, fields, where)
        for name in fields[:-2]:
            value = runner.get(name)
            if value is not None:
                _string(value, f"{where}.{name}")
        for name in ("run_id", "run_attempt"):
            value = runner.get(name)
            if value is not None and not re.fullmatch(r"[1-9][0-9]*", value):
                _fail(f"{where}.{name} must be a positive decimal string or null")
        workflow_sha = runner.get("workflow_file_sha256")
        if workflow_sha is not None:
            _sha(workflow_sha, f"{where}.workflow_file_sha256")
        if runner.get("reported_by") != "runner environment variables, unverified":
            _fail(f"{where}.reported_by must identify the unverified runner report")
    return runner


def _check_termination(data: dict, where: str, *, has_signal: bool = True) -> None:
    termination = _string(data.get("termination"), f"{where}.termination")
    if termination not in TERMINATIONS:
        _fail(f"{where}.termination is not a defined termination")
    exit_code = data.get("exit_code")
    if termination == "exited":
        _integer(exit_code, f"{where}.exit_code")
    elif exit_code is not None:
        _fail(f"{where}.exit_code must be null unless termination is 'exited'")
    if has_signal:
        if termination == "signal":
            _integer(data.get("signal"), f"{where}.signal", 1)
        elif data.get("signal") is not None:
            _fail(f"{where}.signal is allowed only when termination is 'signal'")


# ---------------------------------------------------------------- canonical record


def validate_canonical_structure(record: dict) -> None:
    """Structure of a canonical VERIFY v2 record; needs no repository access."""

    _required(record, ("schema_version", "verification_id", "repo_commit", "recorded_by",
                      "created_at", "observed_at", "receipt", "summary", "origin", "import",
                      "verifier_lineage_status"), "$")
    if record.get("schema_version") != "v2":
        _fail("$.schema_version must be v2")
    identifier = _string(record.get("verification_id"), "$.verification_id")
    if not VERIFICATION_ID_RE.fullmatch(identifier):
        _fail("$.verification_id must be VERIFY-YYYYMMDD-NNNN")
    recorded_by = _required(record.get("recorded_by"), ("peer_id", "substrate", "role"), "$.recorded_by")
    for name in ("peer_id", "substrate", "role"):
        _string(recorded_by.get(name), f"$.recorded_by.{name}")
    commit = record.get("repo_commit")
    if not isinstance(commit, str) or not FULL_COMMIT_RE.fullmatch(commit):
        _fail("$.repo_commit must be a full 40-hex commit")
    _timestamp(record.get("created_at"), "$.created_at")
    _timestamp(record.get("observed_at"), "$.observed_at")
    receipt = _mapping(record.get("receipt"), "$.receipt")
    digest = _sha(receipt.get("sha256"), "$.receipt.sha256")
    _check_store_path(receipt.get("store_path"), digest, "$.receipt.store_path")
    summary = _mapping(record.get("summary"), "$.summary")
    _string(summary.get("result"), "$.summary.result")
    if summary.get("result") not in RESULTS:
        _fail("$.summary.result is not a defined result")
    if summary.get("output_retention") not in ("complete", "partial"):
        _fail("$.summary.output_retention must be complete or partial")
    if not isinstance(summary.get("commands"), list) or not summary["commands"]:
        _fail("$.summary.commands must be a non-empty list")
    for index, command in enumerate(summary["commands"]):
        where = f"$.summary.commands[{index}]"
        data = _required(command, ("declared_property", "termination", "exit_code"), where)
        _string(data.get("declared_property"), f"{where}.declared_property")
        _check_termination(data, where, has_signal=False)
    origin = _mapping(record.get("origin"), "$.origin")
    if origin.get("origin_verification") != ORIGIN_VERIFICATION:
        _fail("$.origin.origin_verification must be 'unverified'")
    _check_runner(origin.get("claimed_runner"), "$.origin.claimed_runner")
    imported = _mapping(record.get("import"), "$.import")
    _sha(imported.get("importer_sha256"), "$.import.importer_sha256")
    _timestamp(imported.get("imported_at"), "$.import.imported_at")
    if imported.get("imported_at") != record.get("created_at"):
        _fail("$.import.imported_at must equal $.created_at")
    if record.get("verifier_lineage_status") != LINEAGE:
        _fail("$.verifier_lineage_status must be 'self_authored_unreviewed'")


# ---------------------------------------------------------------- receipt


def _check_stream(stream: object, store_root: Path, where: str) -> None:
    data = _required(stream, ("observed_bytes", "retained_bytes", "sha256", "store_path", "capture_complete"), where)
    observed = _integer(data.get("observed_bytes"), f"{where}.observed_bytes")
    retained = _integer(data.get("retained_bytes"), f"{where}.retained_bytes")
    if retained != min(observed, RETENTION_LIMIT_BYTES):
        _fail(f"{where}.retained_bytes must equal min(observed_bytes, retention limit)")
    if data.get("capture_complete") is not (retained == observed):
        _fail(f"{where}.capture_complete is inconsistent with the byte counts")
    digest = _sha(data.get("sha256"), f"{where}.sha256")
    relative = _check_store_path(data.get("store_path"), digest, f"{where}.store_path")
    blob = _read_blob(store_root, relative, digest, where)
    if len(blob) != retained:
        _fail(f"{where} stored length differs from retained_bytes")


def _check_boundary(boundary: object, subject: str, where: str) -> None:
    data = _required(boundary, ("head", "head_matches_subject", "status_clean", "changed_paths"), where)
    _commit(data.get("head"), f"{where}.head", nullable=True)
    _boolean(data.get("head_matches_subject"), f"{where}.head_matches_subject")
    _boolean(data.get("status_clean"), f"{where}.status_clean")
    if data.get("head_matches_subject") is not (data.get("head") == subject):
        _fail(f"{where}.head_matches_subject is inconsistent with head")
    paths = data.get("changed_paths")
    if not isinstance(paths, list):
        _fail(f"{where}.changed_paths must be a list")
    for index, path in enumerate(paths):
        _string(path, f"{where}.changed_paths[{index}]")
    if data.get("status_clean") is not (paths == []):
        _fail(f"{where}.status_clean is inconsistent with changed_paths")


def load_profile(profile_bytes: bytes) -> dict:
    try:
        profile = json.loads(profile_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationV2Error(f"stored profile is not valid JSON: {error}") from error
    _check_profile(profile)
    return profile


def _check_profile(profile: object) -> None:
    """Independent copy of the standalone writer's supported profile rules."""

    data = _required(profile, ("profile_schema", "profile_id", "permitted_tree_changes", "environment", "commands"), "stored profile")
    if data.get("profile_schema") != PROFILE_SCHEMA:
        _fail("stored profile has an unknown profile_schema")
    _string(data.get("profile_id"), "stored profile.profile_id")
    if data.get("permitted_tree_changes") != []:
        _fail("stored profile must permit no tree change")
    environment = _mapping(data.get("environment"), "stored profile.environment")
    for name, value in environment.items():
        if not isinstance(name, str) or not ENV_NAME_RE.fullmatch(name) or name in BASE_ENVIRONMENT_NAMES:
            _fail(f"stored profile environment name not allowed: {name!r}")
        if SECRET_NAME_RE.search(name):
            _fail(f"stored profile environment name looks like a secret: {name}")
        if not isinstance(value, str) or "$" in value or "\0" in value:
            _fail(f"stored profile environment value for {name} must be a literal string without NUL")
    commands = data.get("commands")
    if not isinstance(commands, list) or not commands:
        _fail("stored profile must declare at least one command")
    for index, command in enumerate(commands):
        where = f"stored profile.commands[{index}]"
        spec = _required(command, ("argv", "timeout_seconds", "declared_property"), where)
        _argv(spec.get("argv"), f"{where}.argv")
        _timeout(spec.get("timeout_seconds"), f"{where}.timeout_seconds")
        _string(spec.get("declared_property"), f"{where}.declared_property")


def validate_receipt(receipt: dict, store_root: Path) -> dict:
    """Validate a receipt against its stored blobs and stored profile; return the profile."""

    _required(receipt, ("receipt_schema", "observation_basis", "subject", "history", "verifier", "inputs",
                       "environment", "tree_observation", "retention_limit_bytes", "started_at", "finished_at",
                       "commands", "result", "output_retention", "verifier_lineage_status"), "receipt")
    store_root = Path(store_root)
    if receipt.get("receipt_schema") != RECEIPT_SCHEMA:
        _fail(f"receipt_schema must be {RECEIPT_SCHEMA}")
    if receipt.get("observation_basis") != "observed_by_writer":
        _fail("observation_basis must be 'observed_by_writer'")
    if receipt.get("verifier_lineage_status") != LINEAGE:
        _fail("receipt verifier_lineage_status must be 'self_authored_unreviewed'")
    _integer(receipt.get("retention_limit_bytes"), "retention_limit_bytes", 1)
    if receipt.get("retention_limit_bytes") != RETENTION_LIMIT_BYTES:
        _fail("receipt retention_limit_bytes differs from the contract")
    subject = _required(receipt.get("subject"), ("candidate_commit", "tree_id"), "subject")
    candidate = _commit(subject.get("candidate_commit"), "subject.candidate_commit")
    subject_tree = _commit(subject.get("tree_id"), "subject.tree_id")
    started = _timestamp(receipt.get("started_at"), "started_at")
    finished = _timestamp(receipt.get("finished_at"), "finished_at")
    if finished < started:
        _fail("finished_at precedes started_at")

    history = _required(receipt.get("history"), ("shallow", "stored_repo_head", "stored_repo_head_reachable"), "history")
    _boolean(history.get("shallow"), "history.shallow")
    stored_head = _commit(history.get("stored_repo_head"), "history.stored_repo_head", nullable=True)
    reachable = history.get("stored_repo_head_reachable")
    if stored_head is None:
        if reachable is not None:
            _fail("history.stored_repo_head_reachable must be null when stored_repo_head is null")
    else:
        _boolean(reachable, "history.stored_repo_head_reachable")

    verifier = _required(receipt.get("verifier"), ("tool", "running_sha256", "subject_blob_sha", "verifier_matches_subject", "interpreter"), "verifier")
    if verifier.get("tool") != "scripts/verify_v2.py":
        _fail("verifier.tool must identify scripts/verify_v2.py")
    _sha(verifier.get("running_sha256"), "verifier.running_sha256")
    matches = verifier.get("verifier_matches_subject")
    if not isinstance(matches, bool) and matches != "absent_at_subject":
        _fail("verifier.verifier_matches_subject must be true, false or 'absent_at_subject'")
    if matches == "absent_at_subject":
        if verifier.get("subject_blob_sha") is not None:
            _fail("verifier.subject_blob_sha must be null when absent_at_subject")
    else:
        _commit(verifier.get("subject_blob_sha"), "verifier.subject_blob_sha")
    interpreter = _required(verifier.get("interpreter"), ("path", "version"), "verifier.interpreter")
    _absolute_path(interpreter.get("path"), "verifier.interpreter.path")
    _string(interpreter.get("version"), "verifier.interpreter.version")

    inputs = _required(receipt.get("inputs"), ("trees", "profile"), "inputs")
    trees = _required(inputs.get("trees"), ("root", "tests", "scripts", "ai_lab"), "inputs.trees")
    _commit(trees.get("root"), "inputs.trees.root")
    if trees.get("root") != subject_tree:
        _fail("inputs.trees.root must equal subject.tree_id")
    for name in ("tests", "scripts", "ai_lab"):
        _commit(trees.get(name), f"inputs.trees.{name}", nullable=True)
    profile_ref = _required(inputs.get("profile"), ("path", "profile_id", "sha256", "store_path"), "inputs.profile")
    profile_location = _string(profile_ref.get("path"), "inputs.profile.path")
    profile_posix = PurePosixPath(profile_location)
    if profile_posix.is_absolute() or ".." in profile_posix.parts or str(profile_posix) == ".":
        _fail("inputs.profile.path must be relative and stay within the subject tree")
    profile_digest = _sha(profile_ref.get("sha256"), "inputs.profile.sha256")
    profile_path = _check_store_path(profile_ref.get("store_path"), profile_digest, "inputs.profile.store_path")
    profile = load_profile(_read_blob(store_root, profile_path, profile_digest, "inputs.profile"))
    if profile_ref.get("profile_id") != profile["profile_id"]:
        _fail("inputs.profile.profile_id differs from the stored profile")

    environment = _required(receipt.get("environment"), ("environment_capture", "python", "platform", "requirements_sha256",
                                                        "installed_distributions", "command_environment", "runner"), "environment")
    if environment.get("environment_capture") != "partial":
        _fail("environment.environment_capture must be 'partial'")
    python = _required(environment.get("python"), ("implementation", "version"), "environment.python")
    _string(python.get("implementation"), "environment.python.implementation")
    _string(python.get("version"), "environment.python.version")
    if python.get("version") != interpreter.get("version"):
        _fail("environment.python.version differs from verifier.interpreter.version")
    _string(environment.get("platform"), "environment.platform")
    if environment.get("requirements_sha256") is not None:
        _sha(environment.get("requirements_sha256"), "environment.requirements_sha256")
    dists = _required(environment.get("installed_distributions"), ("sha256", "store_path", "count"), "environment.installed_distributions")
    dist_digest = _sha(dists.get("sha256"), "environment.installed_distributions.sha256")
    dist_bytes = _read_blob(store_root, _check_store_path(dists.get("store_path"), dist_digest,
               "environment.installed_distributions.store_path"), dist_digest, "environment.installed_distributions")
    count = _integer(dists.get("count"), "environment.installed_distributions.count")
    if count != dist_bytes.count(b"\n"):
        _fail("environment.installed_distributions.count differs from the retained list")
    command_env = _mapping(environment.get("command_environment"), "environment.command_environment")
    allowed = BASE_ENVIRONMENT_NAMES | set(profile["environment"])
    if set(command_env) != allowed:
        _fail("environment.command_environment names differ from the allowlist of the stored profile")
    for name, value in command_env.items():
        if not isinstance(value, str) or "\0" in value:
            _fail(f"environment.command_environment.{name} must be a string without NUL")
    for name, value in profile["environment"].items():
        if command_env.get(name) != value:
            _fail(f"environment.command_environment.{name} differs from the stored profile's literal value")
    home = _absolute_path(command_env.get("HOME"), "environment.command_environment.HOME")
    if home.name != "home" or home.parent == PurePosixPath("/"):
        _fail("environment.command_environment.HOME must be <absolute-run-directory>/home")
    scratch = str(home.parent / "scratch")
    path_value = _string(command_env.get("PATH"), "environment.command_environment.PATH")
    for index, entry in enumerate(path_value.split(":")):
        _absolute_path(entry, f"environment.command_environment.PATH[{index}]")
    if command_env.get("LANG") != "C.UTF-8" or command_env.get("TZ") != "UTC":
        _fail("environment.command_environment must retain the writer's LANG and TZ")
    runner = _check_runner(environment.get("runner"), "environment.runner")
    pr_fields = ("pull_request", "head_sha", "base_sha")
    if runner.get("event_name") in ("pull_request", "pull_request_target") or any(name in subject for name in pr_fields):
        _required(subject, pr_fields, "subject")
        _integer(subject.get("pull_request"), "subject.pull_request", 1)
        _commit(subject.get("head_sha"), "subject.head_sha")
        _commit(subject.get("base_sha"), "subject.base_sha")

    observation = _required(receipt.get("tree_observation"), ("method", "scope", "permitted_tree_changes", "initial"), "tree_observation")
    if observation.get("method") != TREE_OBSERVATION_METHOD:
        _fail("tree_observation.method is not the supported observation method")
    if observation.get("scope") not in (LEGACY_TREE_OBSERVATION_SCOPE, TREE_OBSERVATION_SCOPE):
        _fail("tree_observation.scope must state the command-boundary limitation")
    if observation.get("permitted_tree_changes") != []:
        _fail("tree_observation.permitted_tree_changes must be empty for this contract")
    _check_boundary(observation.get("initial"), candidate, "tree_observation.initial")

    commands = receipt.get("commands")
    if not isinstance(commands, list):
        _fail("commands must be a list")
    profile_commands = profile["commands"]
    previous_finish = started
    for index, command in enumerate(commands):
        where = f"commands[{index}]"
        data = _required(command, ("index", "argv_template", "argv", "cwd", "timeout_seconds", "declared_property",
                                   "termination", "exit_code", "started_at", "finished_at", "stdout", "stderr", "boundary_after"), where)
        _integer(data.get("index"), f"{where}.index")
        if data.get("index") != index:
            _fail(f"{where}.index must equal its position")
        if index >= len(profile_commands):
            _fail(f"{where} has no counterpart in the stored profile")
        spec = profile_commands[index]
        _argv(data.get("argv_template"), f"{where}.argv_template")
        if data.get("argv_template") != spec.get("argv"):
            _fail(f"{where}.argv_template differs from the stored profile")
        _argv(data.get("argv"), f"{where}.argv")
        expected_argv = [interpreter["path"] if token == "{python}" else token.replace("{scratch}", scratch)
                         for token in spec["argv"]]
        if data.get("argv") != expected_argv:
            _fail(f"{where}.argv differs from resolution of the stored template")
        if data.get("cwd") != ".":
            _fail(f"{where}.cwd must be '.' (the subject worktree root)")
        _timeout(data.get("timeout_seconds"), f"{where}.timeout_seconds")
        if data.get("timeout_seconds") != spec.get("timeout_seconds"):
            _fail(f"{where}.timeout_seconds differs from the stored profile")
        if data.get("declared_property") != spec.get("declared_property"):
            _fail(f"{where}.declared_property differs from the stored profile")
        _check_termination(data, where)
        command_started = _timestamp(data.get("started_at"), f"{where}.started_at")
        command_finished = _timestamp(data.get("finished_at"), f"{where}.finished_at")
        if not (previous_finish <= command_started <= command_finished <= finished):
            _fail(f"{where} timestamps are inconsistent with the run or command order")
        previous_finish = command_finished
        _check_stream(data.get("stdout"), store_root, f"{where}.stdout")
        _check_stream(data.get("stderr"), store_root, f"{where}.stderr")
        _check_boundary(data.get("boundary_after"), candidate, f"{where}.boundary_after")

    expected_result = compute_result(len(profile_commands), commands, observation["initial"])
    if receipt.get("result") != expected_result:
        _fail(f"result {receipt.get('result')!r} differs from the result recomputed from the commands ({expected_result!r})")
    expected_retention = compute_output_retention(commands)
    if receipt.get("output_retention") != expected_retention:
        _fail("output_retention differs from the value recomputed from the commands")
    return profile


def validate_against_store(record: dict, repo_root: Path) -> dict:
    """Validate a canonical v2 record against its receipt in the store under an explicit repo root."""

    validate_canonical_structure(record)
    store_root = Path(repo_root) / STORE_RELATIVE_ROOT
    receipt_ref = record["receipt"]
    receipt_bytes = _read_blob(store_root, receipt_ref["store_path"], receipt_ref["sha256"], "$.receipt")
    try:
        receipt = json.loads(receipt_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationV2Error(f"stored receipt is not valid JSON: {error}") from error
    validate_receipt(_mapping(receipt, "receipt"), store_root)
    if record["repo_commit"] != receipt["subject"]["candidate_commit"]:
        _fail("$.repo_commit must equal receipt.subject.candidate_commit")
    if record["observed_at"] != receipt["finished_at"]:
        _fail("$.observed_at must equal receipt.finished_at")
    if record["summary"] != summary_from_receipt(receipt):
        _fail("$.summary differs from the summary recomputed from the receipt")
    if record["origin"]["claimed_runner"] != receipt["environment"]["runner"]:
        _fail("$.origin.claimed_runner differs from the receipt's runner")
    return receipt
