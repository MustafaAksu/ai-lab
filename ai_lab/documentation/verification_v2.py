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
import re
from pathlib import Path

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


def _string(value: object, where: str) -> str:
    if not isinstance(value, str) or not value:
        _fail(f"{where} must be a non-empty string")
    return value


def _sha(value: object, where: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.match(value):
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


# ---------------------------------------------------------------- canonical record


def validate_canonical_structure(record: dict) -> None:
    """Structure of a canonical VERIFY v2 record; needs no repository access."""

    if record.get("schema_version") != "v2":
        _fail("$.schema_version must be v2")
    commit = record.get("repo_commit")
    if not isinstance(commit, str) or not FULL_COMMIT_RE.match(commit):
        _fail("$.repo_commit must be a full 40-hex commit")
    _string(record.get("created_at"), "$.created_at")
    _string(record.get("observed_at"), "$.observed_at")
    receipt = _mapping(record.get("receipt"), "$.receipt")
    digest = _sha(receipt.get("sha256"), "$.receipt.sha256")
    _check_store_path(receipt.get("store_path"), digest, "$.receipt.store_path")
    summary = _mapping(record.get("summary"), "$.summary")
    if summary.get("result") not in RESULTS:
        _fail("$.summary.result is not a defined result")
    if summary.get("output_retention") not in ("complete", "partial"):
        _fail("$.summary.output_retention must be complete or partial")
    if not isinstance(summary.get("commands"), list) or not summary["commands"]:
        _fail("$.summary.commands must be a non-empty list")
    origin = _mapping(record.get("origin"), "$.origin")
    if origin.get("origin_verification") != ORIGIN_VERIFICATION:
        _fail("$.origin.origin_verification must be 'unverified'")
    _mapping(origin.get("claimed_runner"), "$.origin.claimed_runner")
    imported = _mapping(record.get("import"), "$.import")
    _sha(imported.get("importer_sha256"), "$.import.importer_sha256")
    _string(imported.get("imported_at"), "$.import.imported_at")
    if record.get("verifier_lineage_status") != LINEAGE:
        _fail("$.verifier_lineage_status must be 'self_authored_unreviewed'")


# ---------------------------------------------------------------- receipt


def _check_stream(stream: object, store_root: Path, where: str) -> None:
    data = _mapping(stream, where)
    observed = data.get("observed_bytes")
    retained = data.get("retained_bytes")
    if not isinstance(observed, int) or not isinstance(retained, int) or observed < 0 or retained < 0:
        _fail(f"{where} byte counts must be non-negative integers")
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
    data = _mapping(boundary, where)
    if data.get("head_matches_subject") is not (data.get("head") == subject):
        _fail(f"{where}.head_matches_subject is inconsistent with head")
    paths = data.get("changed_paths")
    if not isinstance(paths, list):
        _fail(f"{where}.changed_paths must be a list")
    if data.get("status_clean") is not (paths == []):
        _fail(f"{where}.status_clean is inconsistent with changed_paths")


def load_profile(profile_bytes: bytes) -> dict:
    try:
        profile = json.loads(profile_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationV2Error(f"stored profile is not valid JSON: {error}") from error
    if not isinstance(profile, dict) or profile.get("profile_schema") != PROFILE_SCHEMA:
        _fail("stored profile has an unknown profile_schema")
    if not isinstance(profile.get("commands"), list) or not isinstance(profile.get("environment"), dict):
        _fail("stored profile must carry commands and environment")
    return profile


def validate_receipt(receipt: dict, store_root: Path) -> dict:
    """Validate a receipt against its stored blobs and stored profile; return the profile."""

    if receipt.get("receipt_schema") != RECEIPT_SCHEMA:
        _fail(f"receipt_schema must be {RECEIPT_SCHEMA}")
    if receipt.get("observation_basis") != "observed_by_writer":
        _fail("observation_basis must be 'observed_by_writer'")
    if receipt.get("verifier_lineage_status") != LINEAGE:
        _fail("receipt verifier_lineage_status must be 'self_authored_unreviewed'")
    if receipt.get("retention_limit_bytes") != RETENTION_LIMIT_BYTES:
        _fail("receipt retention_limit_bytes differs from the contract")
    subject = _mapping(receipt.get("subject"), "subject")
    candidate = subject.get("candidate_commit")
    if not isinstance(candidate, str) or not FULL_COMMIT_RE.match(candidate):
        _fail("subject.candidate_commit must be a full 40-hex commit")
    _string(receipt.get("started_at"), "started_at")
    _string(receipt.get("finished_at"), "finished_at")
    verifier = _mapping(receipt.get("verifier"), "verifier")
    _sha(verifier.get("running_sha256"), "verifier.running_sha256")
    if verifier.get("verifier_matches_subject") not in (True, False, "absent_at_subject"):
        _fail("verifier.verifier_matches_subject must be true, false or 'absent_at_subject'")

    inputs = _mapping(receipt.get("inputs"), "inputs")
    profile_ref = _mapping(inputs.get("profile"), "inputs.profile")
    profile_digest = _sha(profile_ref.get("sha256"), "inputs.profile.sha256")
    profile_path = _check_store_path(profile_ref.get("store_path"), profile_digest, "inputs.profile.store_path")
    profile = load_profile(_read_blob(store_root, profile_path, profile_digest, "inputs.profile"))

    environment = _mapping(receipt.get("environment"), "environment")
    if environment.get("environment_capture") != "partial":
        _fail("environment.environment_capture must be 'partial'")
    dists = _mapping(environment.get("installed_distributions"), "environment.installed_distributions")
    dist_digest = _sha(dists.get("sha256"), "environment.installed_distributions.sha256")
    _read_blob(store_root, _check_store_path(dists.get("store_path"), dist_digest,
               "environment.installed_distributions.store_path"), dist_digest, "environment.installed_distributions")
    command_env = _mapping(environment.get("command_environment"), "environment.command_environment")
    allowed = BASE_ENVIRONMENT_NAMES | set(profile["environment"])
    if set(command_env) != allowed:
        _fail("environment.command_environment names differ from the allowlist of the stored profile")
    for name, value in profile["environment"].items():
        if command_env.get(name) != value:
            _fail(f"environment.command_environment.{name} differs from the stored profile's literal value")
    _mapping(environment.get("runner"), "environment.runner")

    observation = _mapping(receipt.get("tree_observation"), "tree_observation")
    if observation.get("permitted_tree_changes") != []:
        _fail("tree_observation.permitted_tree_changes must be empty for this contract")
    _check_boundary(observation.get("initial"), candidate, "tree_observation.initial")

    commands = receipt.get("commands")
    if not isinstance(commands, list):
        _fail("commands must be a list")
    profile_commands = profile["commands"]
    for index, command in enumerate(commands):
        where = f"commands[{index}]"
        data = _mapping(command, where)
        if data.get("index") != index:
            _fail(f"{where}.index must equal its position")
        if index >= len(profile_commands):
            _fail(f"{where} has no counterpart in the stored profile")
        spec = profile_commands[index]
        if data.get("argv_template") != spec.get("argv"):
            _fail(f"{where}.argv_template differs from the stored profile")
        if data.get("timeout_seconds") != spec.get("timeout_seconds"):
            _fail(f"{where}.timeout_seconds differs from the stored profile")
        if data.get("declared_property") != spec.get("declared_property"):
            _fail(f"{where}.declared_property differs from the stored profile")
        termination = data.get("termination")
        if termination not in TERMINATIONS:
            _fail(f"{where}.termination is not a defined termination")
        exit_code = data.get("exit_code")
        if termination == "exited":
            if not isinstance(exit_code, int) or isinstance(exit_code, bool):
                _fail(f"{where}.exit_code must be an integer when termination is 'exited'")
        elif exit_code is not None:
            _fail(f"{where}.exit_code must be null unless termination is 'exited'")
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
