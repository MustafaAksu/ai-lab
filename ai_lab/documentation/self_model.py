from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections.abc import Callable, Iterable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
class SelfModelError(ValueError):
    """Raised when a self-model record is structurally invalid."""


CAPABILITY_STATUSES = {"implemented", "partial", "experimental", "planned", "deprecated"}
GAP_STATUSES = {"open", "accepted", "closed", "deferred"}
GAP_PRIORITIES = {"low", "medium", "high"}
DECISION_STATUSES = {"recorded"}
ADMITTING_DECISIONS = {"admit", "admit_with_warning"}

CAPABILITY_ID_RE = re.compile(r"^CAP-\d{4}$")
GAP_ID_RE = re.compile(r"^GAP-\d{4}$")
VERIFY_ID_RE = re.compile(r"^VERIFY-\d{8}-\d{4}$")
AUDIT_ID_RE = re.compile(r"^AUDIT-\d{8}-\d{4}$")
PLAN_ID_RE = re.compile(r"^PLAN-\d{8}-\d{4}$")
DECISION_ID_RE = re.compile(r"^DECISION-\d{8}-\d{4}$")
FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def _require_mapping(value: object, path: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise SelfModelError(f"{path} must be an object")
    return value


def _require_list(value: object, path: str) -> list[object]:
    if not isinstance(value, list):
        raise SelfModelError(f"{path} must be a list")
    return value


def _require_non_empty_string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value:
        raise SelfModelError(f"{path} must be a non-empty string")
    return value


def _optional_string_or_null(value: object, path: str) -> None:
    if value is not None and (not isinstance(value, str) or not value):
        raise SelfModelError(f"{path} must be null or a non-empty string")


def _require_full_commit(value: object, path: str) -> str:
    commit = _require_non_empty_string(value, path)
    if not FULL_COMMIT_RE.match(commit):
        raise SelfModelError(f"{path} must be a full 40-character lowercase git hash")
    return commit


def _require_id(value: object, path: str, pattern: re.Pattern[str], label: str) -> str:
    identifier = _require_non_empty_string(value, path)
    if not pattern.match(identifier):
        raise SelfModelError(f"{path} must match {label}")
    return identifier


def read_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SelfModelError(f"{path} must contain a JSON object")
    return data


def file_sha256(path: Path) -> str:
    """Return the lowercase SHA-256 hash of a file's bytes."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _validate_recorded_by(recorded_by: object) -> None:
    data = _require_mapping(recorded_by, "$.recorded_by")
    _require_non_empty_string(data.get("peer_id"), "$.recorded_by.peer_id")
    _require_non_empty_string(data.get("substrate"), "$.recorded_by.substrate")
    _require_non_empty_string(data.get("role"), "$.recorded_by.role")


def validate_verification_record(record: dict[str, object]) -> None:
    """Validate a VERIFY-* execution-evidence record."""

    if record.get("schema_version") != "v1":
        raise SelfModelError("$.schema_version must be v1")

    _require_id(record.get("verification_id"), "$.verification_id", VERIFY_ID_RE, "VERIFY-YYYYMMDD-NNNN")
    _require_full_commit(record.get("repo_commit"), "$.repo_commit")
    _validate_recorded_by(record.get("recorded_by"))
    _require_non_empty_string(record.get("created_at"), "$.created_at")

    commands = _require_list(record.get("commands"), "$.commands")
    if not commands:
        raise SelfModelError("$.commands must not be empty")

    for index, item in enumerate(commands):
        command = _require_mapping(item, f"$.commands[{index}]")
        _require_non_empty_string(command.get("command"), f"$.commands[{index}].command")
        if not isinstance(command.get("exit_code"), int):
            raise SelfModelError(f"$.commands[{index}].exit_code must be an int")
        _require_non_empty_string(command.get("summary"), f"$.commands[{index}].summary")


def _validate_commit_evidence(items: object) -> None:
    commits = _require_list(items, "$.evidence.commits")
    if not commits:
        raise SelfModelError("$.evidence.commits must not be empty")

    for index, item in enumerate(commits):
        entry = _require_mapping(item, f"$.evidence.commits[{index}]")
        _require_full_commit(entry.get("commit"), f"$.evidence.commits[{index}].commit")
        _require_non_empty_string(entry.get("role"), f"$.evidence.commits[{index}].role")


def _validate_file_evidence(items: object) -> None:
    files = _require_list(items, "$.evidence.files")
    if not files:
        raise SelfModelError("$.evidence.files must not be empty")

    for index, item in enumerate(files):
        entry = _require_mapping(item, f"$.evidence.files[{index}]")
        _require_non_empty_string(entry.get("path"), f"$.evidence.files[{index}].path")
        _require_non_empty_string(entry.get("role"), f"$.evidence.files[{index}].role")
        if "content_hash" not in entry:
            raise SelfModelError(f"$.evidence.files[{index}].content_hash is required")
        _optional_string_or_null(entry.get("content_hash"), f"$.evidence.files[{index}].content_hash")


def _validate_id_path_role(items: object, field_name: str) -> None:
    records = _require_list(items, f"$.evidence.{field_name}")

    for index, item in enumerate(records):
        entry = _require_mapping(item, f"$.evidence.{field_name}[{index}]")
        _require_non_empty_string(entry.get("id"), f"$.evidence.{field_name}[{index}].id")
        _require_non_empty_string(entry.get("path"), f"$.evidence.{field_name}[{index}].path")
        _require_non_empty_string(entry.get("role"), f"$.evidence.{field_name}[{index}].role")


def validate_capability_record(record: dict[str, object]) -> None:
    """Validate a CAP-* self-model capability record."""

    if record.get("schema_version") != "v1":
        raise SelfModelError("$.schema_version must be v1")

    _require_id(record.get("capability_id"), "$.capability_id", CAPABILITY_ID_RE, "CAP-NNNN")
    _require_non_empty_string(record.get("name"), "$.name")

    status = _require_non_empty_string(record.get("status"), "$.status")
    if status not in CAPABILITY_STATUSES:
        raise SelfModelError("$.status is not a valid capability status")

    _require_non_empty_string(record.get("category"), "$.category")
    _require_non_empty_string(record.get("summary"), "$.summary")

    interfaces = _require_list(record.get("interfaces"), "$.interfaces")
    for index, item in enumerate(interfaces):
        _require_non_empty_string(item, f"$.interfaces[{index}]")

    evidence = _require_mapping(record.get("evidence"), "$.evidence")
    _validate_commit_evidence(evidence.get("commits"))
    _validate_file_evidence(evidence.get("files"))
    _validate_id_path_role(evidence.get("memory_records"), "memory_records")
    _validate_id_path_role(evidence.get("admissions"), "admissions")

    for field_name in ("limits", "risks", "recommended_next_actions"):
        values = _require_list(record.get(field_name), f"$.{field_name}")
        for index, item in enumerate(values):
            _require_non_empty_string(item, f"$.{field_name}[{index}]")

    last_verified = _require_mapping(record.get("last_verified"), "$.last_verified")
    _require_full_commit(last_verified.get("repo_commit"), "$.last_verified.repo_commit")
    _require_non_empty_string(last_verified.get("verification_artifact"), "$.last_verified.verification_artifact")
    _require_non_empty_string(last_verified.get("verified_at"), "$.last_verified.verified_at")


def validate_gap_record(record: dict[str, object]) -> None:
    """Validate a GAP-* missing-capability record."""

    if record.get("schema_version") != "v1":
        raise SelfModelError("$.schema_version must be v1")

    _require_id(record.get("gap_id"), "$.gap_id", GAP_ID_RE, "GAP-NNNN")
    _require_non_empty_string(record.get("name"), "$.name")

    status = _require_non_empty_string(record.get("status"), "$.status")
    if status not in GAP_STATUSES:
        raise SelfModelError("$.status is not a valid gap status")

    priority = _require_non_empty_string(record.get("priority"), "$.priority")
    if priority not in GAP_PRIORITIES:
        raise SelfModelError("$.priority is not a valid gap priority")

    _require_non_empty_string(record.get("category"), "$.category")
    _require_non_empty_string(record.get("summary"), "$.summary")

    related = _require_list(record.get("related_capabilities"), "$.related_capabilities")
    for index, item in enumerate(related):
        _require_id(item, f"$.related_capabilities[{index}]", CAPABILITY_ID_RE, "CAP-NNNN")

    evidence = _require_mapping(record.get("evidence"), "$.evidence")
    _require_non_empty_string(evidence.get("reason"), "$.evidence.reason")
    files_checked = _require_list(evidence.get("files_checked"), "$.evidence.files_checked")
    for index, item in enumerate(files_checked):
        _require_non_empty_string(item, f"$.evidence.files_checked[{index}]")

    _require_non_empty_string(record.get("risk"), "$.risk")
    _require_non_empty_string(record.get("recommended_first_slice"), "$.recommended_first_slice")

    blocked_by = _require_list(record.get("blocked_by"), "$.blocked_by")
    for index, item in enumerate(blocked_by):
        _require_non_empty_string(item, f"$.blocked_by[{index}]")


def _git_success(args: list[str], repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def _git_output(args: list[str], repo_root: Path) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _commit_distance(commit: str, repo_root: Path) -> int | None:
    output = _git_output(["rev-list", "--count", f"{commit}..HEAD"], repo_root)
    if output is None:
        return None
    try:
        return int(output)
    except ValueError:
        return None


def _finding(severity: str, code: str, target: str, message: str) -> dict[str, str]:
    return {
        "severity": severity,
        "code": code,
        "target": target,
        "message": message,
    }


def _admission_target(record: dict[str, object]) -> str | None:
    direct = record.get("target_item_id")
    if isinstance(direct, str) and direct:
        return direct

    target = record.get("target")
    if isinstance(target, dict):
        item_id = target.get("item_id") or target.get("id")
        if isinstance(item_id, str) and item_id:
            return item_id

    return None


def _latest_admission_for_target(repo_root: Path, target_item_id: str) -> tuple[dict[str, object] | None, bool]:
    admissions_dir = repo_root / "docs" / "memory" / "admissions"
    if not admissions_dir.is_dir():
        return None, False

    matches: list[tuple[str, Path, dict[str, object]]] = []
    used_fallback = False

    for path in admissions_dir.glob("*.json"):
        try:
            record = read_json(path)
        except Exception:
            continue

        if _admission_target(record) != target_item_id:
            continue

        created_at = record.get("created_at")
        if not isinstance(created_at, str) or not created_at:
            used_fallback = True
            created_at = path.name

        matches.append((created_at, path, record))

    if not matches:
        return None, used_fallback

    matches.sort(key=lambda item: (item[0], item[1].name))
    return matches[-1][2], used_fallback


def audit_self_model_registry(
    repo_root: Path = Path("."),
) -> dict[str, object]:
    """Audit canonical registry discovery and references."""

    repo_root = repo_root.resolve()
    findings: list[dict[str, str]] = []
    registry_root = repo_root / "docs" / "self_model"

    try:
        registry = SelfModelRegistry(repo_root)
    except Exception as error:
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_REGISTRY_INVALID",
                str(registry_root),
                str(error),
            )
        )
        return {
            "schema_version": "v1",
            "ok": False,
            "findings": findings,
        }

    for issue in registry.unresolved_references():
        reference = issue.reference
        source_entry = registry.require(
            reference.source_record_id
        )
        target = (
            f"{source_entry.source_path}"
            f"#{reference.field_name}"
        )

        if issue.code == "missing_target":
            findings.append(
                _finding(
                    "error",
                    "SELF_MODEL_REFERENCE_TARGET_MISSING",
                    target,
                    (
                        f"{reference.source_record_id} "
                        f"{reference.field_name} references "
                        f"missing {reference.expected_target_type} "
                        f"record {reference.target_id}."
                    ),
                )
            )
            continue

        if issue.code == "wrong_target_type":
            findings.append(
                _finding(
                    "error",
                    (
                        "SELF_MODEL_REFERENCE_"
                        "TARGET_TYPE_MISMATCH"
                    ),
                    target,
                    (
                        f"{reference.source_record_id} "
                        f"{reference.field_name} references "
                        f"{reference.target_id} as "
                        f"{reference.expected_target_type}, "
                        f"but the target is "
                        f"{issue.actual_target_type}."
                    ),
                )
            )
            continue

        findings.append(
            _finding(
                "error",
                "SELF_MODEL_REFERENCE_INVALID",
                target,
                (
                    "Unsupported registry reference issue: "
                    f"{issue.code}"
                ),
            )
        )

    ok = not any(
        finding["severity"] == "error"
        for finding in findings
    )

    return {
        "schema_version": "v1",
        "ok": ok,
        "findings": findings,
    }


def audit_self_model(
    repo_root: Path = Path("."),
    stale_commit_threshold: int = 10,
) -> dict[str, object]:
    """Run deterministic v1 self-model checks."""

    findings: list[dict[str, str]] = []
    capabilities_dir = repo_root / "docs" / "self_model" / "capabilities"

    if not capabilities_dir.is_dir():
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_CAPABILITIES_DIR_MISSING",
                str(capabilities_dir),
                "Capabilities directory is missing.",
            )
        )
        return {"schema_version": "v1", "ok": False, "findings": findings}

    for cap_path in sorted(capabilities_dir.glob("CAP-*.json")):
        target = cap_path.stem

        try:
            record = read_json(cap_path)
            validate_capability_record(record)
        except Exception as error:
            findings.append(
                _finding(
                    "error",
                    "SELF_MODEL_CAPABILITY_INVALID",
                    target,
                    str(error),
                )
            )
            continue

        findings.append(
            _finding(
                "info",
                "SELF_MODEL_CAPABILITY_SCHEMA_VALID",
                target,
                "Capability record schema is valid.",
            )
        )

        evidence = record["evidence"]
        assert isinstance(evidence, dict)

        for item in evidence.get("commits", []):
            if not isinstance(item, dict):
                continue
            commit = item.get("commit")
            if isinstance(commit, str) and not _git_success(["cat-file", "-e", f"{commit}^{{commit}}"], repo_root):
                findings.append(
                    _finding(
                        "error",
                        "SELF_MODEL_COMMIT_MISSING",
                        target,
                        f"Referenced commit is missing: {commit}",
                    )
                )

        for item in evidence.get("files", []):
            if not isinstance(item, dict):
                continue

            item_path = item.get("path")
            if isinstance(item_path, str) and not (repo_root / item_path).exists():
                findings.append(
                    _finding(
                        "error",
                        "SELF_MODEL_EVIDENCE_PATH_MISSING",
                        target,
                        f"Referenced evidence path is missing: {item_path}",
                    )
                )

            content_hash = item.get("content_hash")
            if content_hash is None:
                findings.append(
                    _finding(
                        "warn",
                        "SELF_MODEL_CONTENT_HASH_MISSING",
                        target,
                        f"Evidence path has no content_hash yet: {item_path}",
                    )
                )
            elif isinstance(item_path, str) and (repo_root / item_path).exists():
                actual_hash = file_sha256(repo_root / item_path)
                if actual_hash != content_hash:
                    findings.append(
                        _finding(
                            "warn",
                            "SELF_MODEL_CONTENT_HASH_MISMATCH",
                            target,
                            f"Evidence path content_hash mismatch: {item_path}",
                        )
                    )
                else:
                    findings.append(
                        _finding(
                            "info",
                            "SELF_MODEL_CONTENT_HASH_MATCH",
                            target,
                            f"Evidence path content_hash matches: {item_path}",
                        )
                    )

        for field_name in ("memory_records", "admissions"):
            for item in evidence.get(field_name, []):
                if not isinstance(item, dict):
                    continue

                item_path = item.get("path")
                if isinstance(item_path, str) and not (repo_root / item_path).exists():
                    findings.append(
                        _finding(
                            "error",
                            "SELF_MODEL_EVIDENCE_RECORD_MISSING",
                            target,
                            f"Referenced {field_name} record is missing: {item_path}",
                        )
                    )

        last_verified = record["last_verified"]
        assert isinstance(last_verified, dict)

        verification_artifact = last_verified.get("verification_artifact")
        if isinstance(verification_artifact, str):
            verification_path = repo_root / verification_artifact
            if not verification_path.exists():
                findings.append(
                    _finding(
                        "error",
                        "SELF_MODEL_VERIFICATION_MISSING",
                        target,
                        f"Verification artifact is missing: {verification_artifact}",
                    )
                )
            else:
                try:
                    validate_verification_record(read_json(verification_path))
                    findings.append(
                        _finding(
                            "info",
                            "SELF_MODEL_VERIFICATION_EXISTS",
                            target,
                            f"Verification artifact exists: {verification_artifact}",
                        )
                    )
                except Exception as error:
                    findings.append(
                        _finding(
                            "error",
                            "SELF_MODEL_VERIFICATION_INVALID",
                            target,
                            str(error),
                        )
                    )

        verified_commit = last_verified.get("repo_commit")
        if isinstance(verified_commit, str):
            if not _git_success(["cat-file", "-e", f"{verified_commit}^{{commit}}"], repo_root):
                findings.append(
                    _finding(
                        "error",
                        "SELF_MODEL_VERIFICATION_COMMIT_MISSING",
                        target,
                        f"Verification commit is missing: {verified_commit}",
                    )
                )
            else:
                distance = _commit_distance(verified_commit, repo_root)
                if distance is not None and distance > stale_commit_threshold:
                    findings.append(
                        _finding(
                            "warn",
                            "SELF_MODEL_STALE_VERIFICATION",
                            target,
                            (
                                "Capability verification is older than "
                                f"{stale_commit_threshold} commits."
                            ),
                        )
                    )

        for item in evidence.get("admissions", []):
            if not isinstance(item, dict) or item.get("role") != "warrant":
                continue

            item_path = item.get("path")
            if not isinstance(item_path, str):
                continue

            try:
                warrant_record = read_json(repo_root / item_path)
            except Exception as error:
                findings.append(
                    _finding(
                        "error",
                        "SELF_MODEL_WARRANT_INVALID",
                        target,
                        f"Referenced warrant is unreadable or invalid JSON: {error}",
                    )
                )
                continue

            target_item_id = _admission_target(warrant_record)
            if target_item_id is None:
                findings.append(
                    _finding(
                        "error",
                        "SELF_MODEL_WARRANT_TARGET_MISSING",
                        target,
                        "Referenced warrant has no target item id.",
                    )
                )
                continue

            latest_record, used_fallback = _latest_admission_for_target(
                repo_root=repo_root,
                target_item_id=target_item_id,
            )

            if latest_record is None:
                findings.append(
                    _finding(
                        "error",
                        "SELF_MODEL_WARRANT_STATE_MISSING",
                        target,
                        f"No current admission state found for target: {target_item_id}",
                    )
                )
                continue

            if used_fallback:
                findings.append(
                    _finding(
                        "warn",
                        "SELF_MODEL_WARRANT_FALLBACK_ORDER",
                        target,
                        "Admission created_at missing; lexical fallback used.",
                    )
                )

            decision = latest_record.get("decision")
            if decision not in ADMITTING_DECISIONS:
                findings.append(
                    _finding(
                        "warn",
                        "SELF_MODEL_WARRANT_NOT_ADMITTING",
                        target,
                        (
                            f"Latest warrant state for {target_item_id} "
                            f"is not admitting: {decision}"
                        ),
                    )
                )
            else:
                findings.append(
                    _finding(
                        "info",
                        "SELF_MODEL_WARRANT_ADMITTING",
                        target,
                        f"Latest warrant state for {target_item_id} is admitting.",
                    )
                )

    registry_audit = audit_self_model_registry(
        repo_root
    )
    registry_findings = registry_audit.get("findings")

    if isinstance(registry_findings, list):
        findings.extend(
            finding
            for finding in registry_findings
            if isinstance(finding, dict)
        )

    ok = not any(
        finding["severity"] == "error"
        for finding in findings
    )
    return {
        "schema_version": "v1",
        "ok": ok,
        "findings": findings,
    }



PLAN_STATUSES = {"proposed", "admitted", "rejected", "completed", "superseded"}


def _plan_require_string(record: dict[str, object], key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        raise SelfModelError(f"$.{key} must be a non-empty string.")
    return value


def _plan_require_string_list(record: dict[str, object], key: str) -> list[str]:
    value = record.get(key)
    if not isinstance(value, list) or not value:
        raise SelfModelError(f"$.{key} must be a non-empty list of strings.")

    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            raise SelfModelError(f"$.{key}[{index}] must be a non-empty string.")
        result.append(item)

    return result



def validate_decision_record(record: dict[str, object]) -> None:
    """Validate an existing DECISION-* self-model record."""

    if not isinstance(record, dict):
        raise SelfModelError("Decision record must be a JSON object.")

    if record.get("schema_version") != "v1":
        raise SelfModelError("$.schema_version must be v1.")

    _require_id(
        record.get("decision_id"),
        "$.decision_id",
        DECISION_ID_RE,
        "DECISION-YYYYMMDD-NNNN",
    )

    status = _require_non_empty_string(
        record.get("status"),
        "$.status",
    )
    if status not in DECISION_STATUSES:
        raise SelfModelError(
            "$.status is not a valid decision status"
        )

    for field_name in (
        "title",
        "created_at",
        "decision",
        "selection_effect",
        "summary",
    ):
        _require_non_empty_string(
            record.get(field_name),
            f"$.{field_name}",
        )

    _require_full_commit(
        record.get("repo_commit"),
        "$.repo_commit",
    )

    _require_id(
        record.get("source_gap_id"),
        "$.source_gap_id",
        GAP_ID_RE,
        "GAP-NNNN",
    )
    _require_id(
        record.get("source_plan_id"),
        "$.source_plan_id",
        PLAN_ID_RE,
        "PLAN-YYYYMMDD-NNNN",
    )

    source_capability_ids = _require_list(
        record.get("source_capability_ids"),
        "$.source_capability_ids",
    )
    for index, item in enumerate(source_capability_ids):
        _require_id(
            item,
            f"$.source_capability_ids[{index}]",
            CAPABILITY_ID_RE,
            "CAP-NNNN",
        )

    for field_name in (
        "evidence_refs",
        "rationale",
        "authorized_effects",
        "blocked_effects",
        "required_next_governance",
    ):
        values = _require_list(
            record.get(field_name),
            f"$.{field_name}",
        )
        for index, item in enumerate(values):
            _require_non_empty_string(
                item,
                f"$.{field_name}[{index}]",
            )


def validate_plan_record(record: dict[str, object]) -> None:
    if not isinstance(record, dict):
        raise SelfModelError("Plan record must be a JSON object.")

    if record.get("schema_version") != "v1":
        raise SelfModelError("$.schema_version must be v1.")

    plan_id = _plan_require_string(record, "plan_id")
    if not PLAN_ID_RE.match(plan_id):
        raise SelfModelError("$.plan_id must match PLAN-YYYYMMDD-NNNN.")

    source_gap_id = _plan_require_string(record, "source_gap_id")
    if not GAP_ID_RE.match(source_gap_id):
        raise SelfModelError("$.source_gap_id must match GAP-NNNN.")

    status = _plan_require_string(record, "status")
    if status not in PLAN_STATUSES:
        raise SelfModelError(
            "$.status must be one of: " + ", ".join(sorted(PLAN_STATUSES))
        )

    for key in (
        "title",
        "created_at",
        "objective",
        "proposed_change",
        "risk",
        "next_action",
    ):
        _plan_require_string(record, key)

    for key in ("rationale", "constraints", "success_criteria"):
        _plan_require_string_list(record, key)


WARRANT_TARGET_TYPES = {"capability", "gap", "plan", "verification", "self_model_index"}
WARRANT_STATES = {"supported", "disputed", "rejected", "superseded", "unreviewed"}
WARRANT_DECISIONS = {"admit", "admit_with_warning", "reject", "defer"}
WARRANT_ID_RE = re.compile(r"^WARR-\d{8}-\d{4}$")


def _warrant_require_string(record: dict[str, object], key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        raise SelfModelError(f"$.{key} must be a non-empty string.")
    return value


def _warrant_require_string_list(record: dict[str, object], key: str) -> list[str]:
    value = record.get(key)
    if not isinstance(value, list) or not value:
        raise SelfModelError(f"$.{key} must be a non-empty list of strings.")

    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            raise SelfModelError(f"$.{key}[{index}] must be a non-empty string.")
        result.append(item)

    return result


def validate_warrant_record(record: dict[str, object]) -> None:
    if not isinstance(record, dict):
        raise SelfModelError("Warrant record must be a JSON object.")

    if record.get("schema_version") != "v1":
        raise SelfModelError("$.schema_version must be v1.")

    warrant_id = _warrant_require_string(record, "warrant_id")
    if not WARRANT_ID_RE.match(warrant_id):
        raise SelfModelError("$.warrant_id must match WARR-YYYYMMDD-NNNN.")

    target_item_id = _warrant_require_string(record, "target_item_id")
    if not target_item_id:
        raise SelfModelError("$.target_item_id must be non-empty.")

    target_item_type = _warrant_require_string(record, "target_item_type")
    if target_item_type not in WARRANT_TARGET_TYPES:
        raise SelfModelError(
            "$.target_item_type must be one of: "
            + ", ".join(sorted(WARRANT_TARGET_TYPES))
        )

    decision = _warrant_require_string(record, "decision")
    if decision not in WARRANT_DECISIONS:
        raise SelfModelError(
            "$.decision must be one of: " + ", ".join(sorted(WARRANT_DECISIONS))
        )

    warrant_state = _warrant_require_string(record, "warrant_state")
    if warrant_state not in WARRANT_STATES:
        raise SelfModelError(
            "$.warrant_state must be one of: " + ", ".join(sorted(WARRANT_STATES))
        )

    for key in ("created_at", "author", "substrate", "reason", "scope"):
        _warrant_require_string(record, key)

    _warrant_require_string_list(record, "evidence_ids")

def _repo_head(repo_root: Path) -> str | None:
    return _git_output(["rev-parse", "HEAD"], repo_root)


def _load_valid_records(
    directory: Path,
    pattern: str,
    validator,
) -> list[tuple[Path, dict[str, object]]]:
    records: list[tuple[Path, dict[str, object]]] = []

    if not directory.is_dir():
        return records

    for path in sorted(directory.glob(pattern)):
        record = read_json(path)
        validator(record)
        records.append((path, record))

    return records


def _count_by_field(
    records: list[tuple[Path, dict[str, object]]],
    field: str,
) -> dict[str, int]:
    counts: dict[str, int] = {}

    for _, record in records:
        value = record.get(field)
        if isinstance(value, str):
            counts[value] = counts.get(value, 0) + 1

    return dict(sorted(counts.items()))


def _count_by_status(records: list[tuple[Path, dict[str, object]]]) -> dict[str, int]:
    counts: dict[str, int] = {}

    for _, record in records:
        status = record.get("status")
        if isinstance(status, str):
            counts[status] = counts.get(status, 0) + 1

    return dict(sorted(counts.items()))


def _audit_severity_counts(audit: dict[str, object]) -> dict[str, int]:
    counts = {"error": 0, "warn": 0, "info": 0}

    findings = audit.get("findings")
    if isinstance(findings, list):
        for finding in findings:
            if not isinstance(finding, dict):
                continue

            severity = finding.get("severity")
            if isinstance(severity, str):
                counts[severity] = counts.get(severity, 0) + 1

    return dict(sorted(counts.items()))


def _relative_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()



RecordValidator = Callable[[dict[str, object]], None]


def _freeze_json(value: object) -> object:
    """Recursively freeze JSON-compatible data."""

    if isinstance(value, dict):
        return MappingProxyType({
            str(key): _freeze_json(item)
            for key, item in value.items()
        })

    if isinstance(value, list):
        return tuple(
            _freeze_json(item)
            for item in value
        )

    return value


def _thaw_json(value: object) -> object:
    """Return mutable JSON-compatible data from frozen data."""

    if isinstance(value, Mapping):
        return {
            str(key): _thaw_json(item)
            for key, item in value.items()
        }

    if isinstance(value, tuple):
        return [
            _thaw_json(item)
            for item in value
        ]

    return deepcopy(value)


def _mapping_value_at_path(
    record: Mapping[str, object],
    field_path: tuple[str, ...],
) -> object | None:
    """Return a nested mapping value or None when the path is absent."""

    value: object = record

    for part in field_path:
        if not isinstance(value, Mapping):
            return None
        if part not in value:
            return None
        value = value[part]

    return value


@dataclass(frozen=True)
class ReferenceSpec:
    """Static location and expected type for a canonical ID reference."""

    field_path: tuple[str, ...]
    target_type: str | None = None
    target_type_path: tuple[str, ...] | None = None
    many: bool = False

    def __post_init__(self) -> None:
        if not self.field_path:
            raise ValueError("reference field_path must not be empty")

        if (self.target_type is None) == (
            self.target_type_path is None
        ):
            raise ValueError(
                "reference must define exactly one of target_type "
                "or target_type_path"
            )


@dataclass(frozen=True)
class RecordTypeSpec:
    """Static ontology information for one canonical record family."""

    record_type: str
    directory_name: str
    filename_glob: str
    id_field: str
    id_pattern: re.Pattern[str]
    id_prefix: str
    date_scoped: bool
    validator: RecordValidator
    status_field: str | None = "status"
    allowed_statuses: frozenset[str] = frozenset()
    open_statuses: frozenset[str] = frozenset()
    references: tuple[ReferenceSpec, ...] = ()


@dataclass(frozen=True)
class RegistryReference:
    """One explicit canonical ID reference discovered in a record."""

    source_record_id: str
    source_record_type: str
    field_path: tuple[str, ...]
    target_id: str
    expected_target_type: str

    @property
    def field_name(self) -> str:
        return ".".join(self.field_path)

    @property
    def predicate(self) -> str:
        """Return the normalized namespaced relation predicate."""

        return f"self_model.{self.field_name}"


@dataclass(frozen=True)
class RegistryReferenceIssue:
    """A missing or wrong-type canonical registry reference."""

    code: str
    reference: RegistryReference
    actual_target_type: str | None


@dataclass(frozen=True)
class RegistryRelation:
    """A graph-compatible relation derived from registry references."""

    source_id: str
    predicate: str
    target_id: str
    relation_source: str
    authoritative: bool
    scope: str | None = None
    evidence: str | None = None


@dataclass(frozen=True)
class RegistryEntry:
    """One validated, recursively immutable self-model record."""

    record_type: str
    record_id: str
    source_path: Path
    record: Mapping[str, object]
    status: str | None

    def mutable_record(self) -> dict[str, object]:
        """Return an independent mutable JSON-compatible record."""

        thawed = _thaw_json(self.record)
        if not isinstance(thawed, dict):
            raise SelfModelError(
                f"{self.record_id} did not thaw to an object"
            )
        return thawed


SELF_MODEL_RECORD_SPECS: tuple[RecordTypeSpec, ...] = (
    RecordTypeSpec(
        record_type="capability",
        directory_name="capabilities",
        filename_glob="CAP-*.json",
        id_field="capability_id",
        id_pattern=CAPABILITY_ID_RE,
        id_prefix="CAP",
        date_scoped=False,
        validator=validate_capability_record,
        allowed_statuses=frozenset(CAPABILITY_STATUSES),
    ),
    RecordTypeSpec(
        record_type="gap",
        directory_name="gaps",
        filename_glob="GAP-*.json",
        id_field="gap_id",
        id_pattern=GAP_ID_RE,
        id_prefix="GAP",
        date_scoped=False,
        validator=validate_gap_record,
        allowed_statuses=frozenset(GAP_STATUSES),
        open_statuses=frozenset({"open"}),
        references=(
            ReferenceSpec(
                field_path=("related_capabilities",),
                target_type="capability",
                many=True,
            ),
            ReferenceSpec(
                field_path=("closure_warrant_id",),
                target_type="warrant",
            ),
        ),
    ),
    RecordTypeSpec(
        record_type="verification",
        directory_name="verifications",
        filename_glob="VERIFY-*.json",
        id_field="verification_id",
        id_pattern=VERIFY_ID_RE,
        id_prefix="VERIFY",
        date_scoped=True,
        validator=validate_verification_record,
        status_field=None,
        references=(
            ReferenceSpec(
                field_path=("target_item_id",),
                target_type_path=("target_item_type",),
            ),
        ),
    ),
    RecordTypeSpec(
        record_type="plan",
        directory_name="plans",
        filename_glob="PLAN-*.json",
        id_field="plan_id",
        id_pattern=PLAN_ID_RE,
        id_prefix="PLAN",
        date_scoped=True,
        validator=validate_plan_record,
        allowed_statuses=frozenset(PLAN_STATUSES),
        open_statuses=frozenset({"proposed", "admitted"}),
        references=(
            ReferenceSpec(
                field_path=("source_gap_id",),
                target_type="gap",
            ),
            ReferenceSpec(
                field_path=("admission_warrant_id",),
                target_type="warrant",
            ),
            ReferenceSpec(
                field_path=("completion_verification_id",),
                target_type="verification",
            ),
            ReferenceSpec(
                field_path=("completion_warrant_id",),
                target_type="warrant",
            ),
            ReferenceSpec(
                field_path=("source_capability_id",),
                target_type="capability",
            ),
            ReferenceSpec(
                field_path=("source_capability_ids",),
                target_type="capability",
                many=True,
            ),
            ReferenceSpec(
                field_path=("depends_on_capability_ids",),
                target_type="capability",
                many=True,
            ),
            ReferenceSpec(
                field_path=(
                    "created_from",
                    "source_capability_id",
                ),
                target_type="capability",
            ),
            ReferenceSpec(
                field_path=(
                    "created_from",
                    "source_plan_id",
                ),
                target_type="plan",
            ),
        ),
    ),
    RecordTypeSpec(
        record_type="warrant",
        directory_name="warrants",
        filename_glob="WARR-*.json",
        id_field="warrant_id",
        id_pattern=WARRANT_ID_RE,
        id_prefix="WARR",
        date_scoped=True,
        validator=validate_warrant_record,
        status_field="warrant_state",
        allowed_statuses=frozenset(WARRANT_STATES),
        references=(
            ReferenceSpec(
                field_path=("target_item_id",),
                target_type_path=("target_item_type",),
            ),
        ),
    ),
    RecordTypeSpec(
        record_type="decision",
        directory_name="decisions",
        filename_glob="DECISION-*.json",
        id_field="decision_id",
        id_pattern=DECISION_ID_RE,
        id_prefix="DECISION",
        date_scoped=True,
        validator=validate_decision_record,
        allowed_statuses=frozenset(DECISION_STATUSES),
        references=(
            ReferenceSpec(
                field_path=("source_gap_id",),
                target_type="gap",
            ),
            ReferenceSpec(
                field_path=("source_plan_id",),
                target_type="plan",
            ),
            ReferenceSpec(
                field_path=("source_capability_ids",),
                target_type="capability",
                many=True,
            ),
        ),
    ),
)


class SelfModelRegistry:
    """Read-only discovery and lookup over canonical self-model records."""

    def __init__(
        self,
        repo_root: Path = Path("."),
        specs: Iterable[RecordTypeSpec] = SELF_MODEL_RECORD_SPECS,
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.specs = tuple(specs)

        spec_by_type: dict[str, RecordTypeSpec] = {}
        for spec in self.specs:
            if spec.record_type in spec_by_type:
                raise SelfModelError(
                    "duplicate record-type specification: "
                    f"{spec.record_type}"
                )

            if not spec.open_statuses.issubset(
                spec.allowed_statuses
            ):
                raise SelfModelError(
                    "open statuses must be a subset of allowed "
                    f"statuses for {spec.record_type}"
                )

            spec_by_type[spec.record_type] = spec

        self._spec_by_type = MappingProxyType(spec_by_type)

        entries: list[RegistryEntry] = []
        entries_by_id: dict[str, RegistryEntry] = {}

        for spec in self.specs:
            directory = (
                self.repo_root
                / "docs"
                / "self_model"
                / spec.directory_name
            )

            if not directory.is_dir():
                continue

            for path in sorted(directory.glob(spec.filename_glob)):
                try:
                    record = read_json(path)
                    spec.validator(record)
                except (OSError, json.JSONDecodeError, SelfModelError) as exc:
                    relative = path.relative_to(self.repo_root)
                    raise SelfModelError(
                        f"{relative}: {exc}"
                    ) from exc

                identifier = record.get(spec.id_field)
                if (
                    not isinstance(identifier, str)
                    or not spec.id_pattern.fullmatch(identifier)
                ):
                    relative = path.relative_to(self.repo_root)
                    raise SelfModelError(
                        f"{relative}: $.{spec.id_field} does not "
                        "match its record-type specification"
                    )

                expected_name = f"{identifier}.json"
                if path.name != expected_name:
                    relative = path.relative_to(self.repo_root)
                    raise SelfModelError(
                        f"{relative}: filename must be "
                        f"{expected_name}"
                    )

                if identifier in entries_by_id:
                    previous = entries_by_id[identifier]
                    raise SelfModelError(
                        f"duplicate self-model ID {identifier}: "
                        f"{previous.source_path} and "
                        f"{path.relative_to(self.repo_root)}"
                    )

                status: str | None = None
                if spec.status_field is not None:
                    value = record.get(spec.status_field)

                    if value is not None and not isinstance(value, str):
                        relative = path.relative_to(self.repo_root)
                        raise SelfModelError(
                            f"{relative}: $.{spec.status_field} "
                            "must be a string"
                        )

                    if isinstance(value, str):
                        status = value

                    if (
                        status is not None
                        and spec.allowed_statuses
                        and status not in spec.allowed_statuses
                    ):
                        relative = path.relative_to(self.repo_root)
                        raise SelfModelError(
                            f"{relative}: unsupported "
                            f"{spec.status_field} value {status}"
                        )

                frozen_record = _freeze_json(record)
                if not isinstance(frozen_record, Mapping):
                    raise SelfModelError(
                        f"{identifier} did not freeze to an object"
                    )

                entry = RegistryEntry(
                    record_type=spec.record_type,
                    record_id=identifier,
                    source_path=path.relative_to(self.repo_root),
                    record=frozen_record,
                    status=status,
                )
                entries.append(entry)
                entries_by_id[identifier] = entry

        self._entries = tuple(entries)
        self._entries_by_id = MappingProxyType(entries_by_id)
        self._references = self._collect_references()

    @property
    def record_types(self) -> tuple[str, ...]:
        return tuple(spec.record_type for spec in self.specs)

    def entries(
        self,
        record_type: str | None = None,
    ) -> tuple[RegistryEntry, ...]:
        if record_type is None:
            return self._entries

        if record_type not in self._spec_by_type:
            raise SelfModelError(
                f"unknown self-model record type: {record_type}"
            )

        return tuple(
            entry
            for entry in self._entries
            if entry.record_type == record_type
        )

    def get(self, record_id: str) -> RegistryEntry | None:
        return self._entries_by_id.get(record_id)

    def require(self, record_id: str) -> RegistryEntry:
        entry = self.get(record_id)
        if entry is None:
            raise SelfModelError(
                f"unknown self-model record ID: {record_id}"
            )
        return entry

    def count(self, record_type: str | None = None) -> int:
        return len(self.entries(record_type))

    def count_by_status(
        self,
        record_type: str,
    ) -> dict[str, int]:
        counts: dict[str, int] = {}

        for entry in self.entries(record_type):
            if entry.status is not None:
                counts[entry.status] = (
                    counts.get(entry.status, 0) + 1
                )

        return dict(sorted(counts.items()))

    def is_open(self, record_id: str) -> bool:
        entry = self.require(record_id)
        spec = self._spec_by_type[entry.record_type]
        return (
            entry.status is not None
            and entry.status in spec.open_statuses
        )

    def open_entries(
        self,
        record_type: str,
    ) -> tuple[RegistryEntry, ...]:
        return tuple(
            entry
            for entry in self.entries(record_type)
            if self.is_open(entry.record_id)
        )

    def _collect_references(
        self,
    ) -> tuple[RegistryReference, ...]:
        references: list[RegistryReference] = []

        for entry in self._entries:
            spec = self._spec_by_type[entry.record_type]

            for reference_spec in spec.references:
                raw_value = _mapping_value_at_path(
                    entry.record,
                    reference_spec.field_path,
                )

                if raw_value is None:
                    continue

                if reference_spec.target_type is not None:
                    expected_type = reference_spec.target_type
                else:
                    expected_value = _mapping_value_at_path(
                        entry.record,
                        reference_spec.target_type_path or (),
                    )
                    if not isinstance(expected_value, str):
                        raise SelfModelError(
                            f"{entry.record_id} "
                            f"{'.'.join(reference_spec.field_path)} "
                            "requires a string target type"
                        )
                    expected_type = expected_value

                if expected_type not in self._spec_by_type:
                    raise SelfModelError(
                        f"{entry.record_id} references unknown "
                        f"record type {expected_type}"
                    )

                if reference_spec.many:
                    if not isinstance(raw_value, tuple):
                        raise SelfModelError(
                            f"{entry.record_id} "
                            f"{'.'.join(reference_spec.field_path)} "
                            "must be a list"
                        )
                    target_values = raw_value
                else:
                    target_values = (raw_value,)

                for target_value in target_values:
                    if not isinstance(target_value, str):
                        raise SelfModelError(
                            f"{entry.record_id} "
                            f"{'.'.join(reference_spec.field_path)} "
                            "must contain string IDs"
                        )

                    references.append(
                        RegistryReference(
                            source_record_id=entry.record_id,
                            source_record_type=entry.record_type,
                            field_path=reference_spec.field_path,
                            target_id=target_value,
                            expected_target_type=expected_type,
                        )
                    )

        return tuple(references)

    def references(
        self,
        record_type: str | None = None,
    ) -> tuple[RegistryReference, ...]:
        if record_type is None:
            return self._references

        if record_type not in self._spec_by_type:
            raise SelfModelError(
                f"unknown self-model record type: {record_type}"
            )

        return tuple(
            reference
            for reference in self._references
            if reference.source_record_type == record_type
        )

    def resolve_reference(
        self,
        reference: RegistryReference,
    ) -> RegistryEntry | None:
        target = self.get(reference.target_id)

        if target is None:
            return None

        if target.record_type != reference.expected_target_type:
            return None

        return target

    def unresolved_references(
        self,
    ) -> tuple[RegistryReferenceIssue, ...]:
        issues: list[RegistryReferenceIssue] = []

        for reference in self._references:
            target = self.get(reference.target_id)

            if target is None:
                issues.append(
                    RegistryReferenceIssue(
                        code="missing_target",
                        reference=reference,
                        actual_target_type=None,
                    )
                )
                continue

            if target.record_type != reference.expected_target_type:
                issues.append(
                    RegistryReferenceIssue(
                        code="wrong_target_type",
                        reference=reference,
                        actual_target_type=target.record_type,
                    )
                )

        return tuple(issues)

    def relations(self) -> tuple[RegistryRelation, ...]:
        """Return graph-compatible relations for resolved registry IDs."""

        relations: list[RegistryRelation] = []

        for reference in self._references:
            target = self.resolve_reference(reference)
            if target is None:
                continue

            source_entry = self.require(
                reference.source_record_id
            )

            relations.append(
                RegistryRelation(
                    source_id=reference.source_record_id,
                    predicate=reference.predicate,
                    target_id=target.record_id,
                    relation_source="self_model_registry",
                    authoritative=True,
                    scope="self_model",
                    evidence=(
                        f"{source_entry.source_path}"
                        f"#{reference.field_name}"
                    ),
                )
            )

        return tuple(relations)

def record_type_spec(
    record_type: str,
) -> RecordTypeSpec:
    """Return the canonical specification for one record type."""

    for spec in SELF_MODEL_RECORD_SPECS:
        if spec.record_type == record_type:
            return spec

    raise SelfModelError(
        f"unknown self-model record type: {record_type}"
    )


def _record_date_token(
    value: str | None,
) -> str:
    """Return a validated YYYYMMDD token."""

    if value is None:
        return datetime.now(timezone.utc).strftime("%Y%m%d")

    token = value.replace("-", "")

    if not re.fullmatch(r"\d{8}", token):
        raise SelfModelError(
            "record date must use YYYY-MM-DD or YYYYMMDD"
        )

    try:
        datetime.strptime(token, "%Y%m%d")
    except ValueError as error:
        raise SelfModelError(
            f"invalid record date: {value}"
        ) from error

    return token


def suggest_next_record_id(
    record_type: str,
    *,
    repo_root: Path = Path("."),
    record_date: str | None = None,
) -> str:
    """
    Suggest the next locally available max-suffix record ID.

    This is intentionally non-transactional and provides no protection
    against IDs created concurrently in another branch or worktree.
    """

    spec = record_type_spec(record_type)
    registry = SelfModelRegistry(repo_root)

    if spec.date_scoped:
        date_token = _record_date_token(record_date)
        stem = f"{spec.id_prefix}-{date_token}-"
    else:
        stem = f"{spec.id_prefix}-"

    suffixes: list[int] = []

    for entry in registry.entries(record_type):
        if not entry.record_id.startswith(stem):
            continue

        suffix = entry.record_id.rsplit("-", 1)[-1]

        if suffix.isdigit():
            suffixes.append(int(suffix))

    next_suffix = max(suffixes, default=0) + 1

    return f"{stem}{next_suffix:04d}"


def default_record_path(
    repo_root: Path,
    record_type: str,
    record_id: str,
) -> Path:
    """Return the canonical JSON path for a self-model record."""

    spec = record_type_spec(record_type)

    if not spec.id_pattern.fullmatch(record_id):
        raise SelfModelError(
            f"{record_id} does not match the "
            f"{record_type} ID specification"
        )

    return (
        repo_root.resolve()
        / "docs"
        / "self_model"
        / spec.directory_name
        / f"{record_id}.json"
    )


def write_new_self_model_record(
    repo_root: Path,
    record_type: str,
    record: Mapping[str, object],
) -> Path:
    """
    Validate and exclusively create one canonical self-model record.

    Existing records and current-worktree path collisions are never
    overwritten.
    """

    repo_root = repo_root.resolve()
    spec = record_type_spec(record_type)
    candidate = deepcopy(dict(record))

    spec.validator(candidate)

    identifier = candidate.get(spec.id_field)

    if not isinstance(identifier, str):
        raise SelfModelError(
            f"$.{spec.id_field} must be a string"
        )

    registry = SelfModelRegistry(repo_root)
    existing = registry.get(identifier)

    if existing is not None:
        raise SelfModelError(
            f"self-model record ID already exists: "
            f"{identifier} at {existing.source_path}"
        )

    output = default_record_path(
        repo_root,
        record_type,
        identifier,
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        with output.open(
            "x",
            encoding="utf-8",
        ) as handle:
            handle.write(
                json.dumps(
                    candidate,
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )
    except FileExistsError as error:
        raise SelfModelError(
            f"refusing to overwrite existing path: "
            f"{output.relative_to(repo_root)}"
        ) from error

    return output


def build_self_model_index(
    repo_root: Path = Path("."),
    generated_at: str | None = None,
) -> dict[str, object]:
    repo_root = repo_root.resolve()

    registry = SelfModelRegistry(repo_root)

    capabilities = [
        (
            repo_root / entry.source_path,
            entry.mutable_record(),
        )
        for entry in registry.entries("capability")
    ]
    gaps = [
        (
            repo_root / entry.source_path,
            entry.mutable_record(),
        )
        for entry in registry.entries("gap")
    ]
    verifications = [
        (
            repo_root / entry.source_path,
            entry.mutable_record(),
        )
        for entry in registry.entries("verification")
    ]
    plans = [
        (
            repo_root / entry.source_path,
            entry.mutable_record(),
        )
        for entry in registry.entries("plan")
    ]
    warrants = [
        (
            repo_root / entry.source_path,
            entry.mutable_record(),
        )
        for entry in registry.entries("warrant")
    ]

    audit = audit_self_model(repo_root)

    capability_records = [
        {
            "capability_id": str(record["capability_id"]),
            "name": str(record["name"]),
            "status": str(record["status"]),
            "category": str(record["category"]),
            "source_path": _relative_path(path, repo_root),
        }
        for path, record in capabilities
    ]

    gap_records = [
        {
            "gap_id": str(record["gap_id"]),
            "name": str(record["name"]),
            "status": str(record["status"]),
            "category": str(record["category"]),
            "priority": str(record["priority"]),
            "source_path": _relative_path(path, repo_root),
        }
        for path, record in gaps
    ]

    verification_records = [
        {
            "verification_id": str(record["verification_id"]),
            "repo_commit": str(record["repo_commit"]),
            "source_path": _relative_path(path, repo_root),
        }
        for path, record in verifications
    ]

    plan_records = [
        {
            "plan_id": str(record["plan_id"]),
            "title": str(record["title"]),
            "status": str(record["status"]),
            "source_gap_id": str(record["source_gap_id"]),
            "source_path": _relative_path(path, repo_root),
        }
        for path, record in plans
    ]

    warrant_records = [
        {
            "warrant_id": str(record["warrant_id"]),
            "target_item_id": str(record["target_item_id"]),
            "target_item_type": str(record["target_item_type"]),
            "decision": str(record["decision"]),
            "warrant_state": str(record["warrant_state"]),
            "source_path": _relative_path(path, repo_root),
        }
        for path, record in warrants
    ]

    admitted_plans = [
        str(record["target_item_id"])
        for _, record in warrants
        if record.get("target_item_type") == "plan"
        and record.get("decision") in {"admit", "admit_with_warning"}
        and record.get("warrant_state") == "supported"
    ]

    known_risks: list[dict[str, str]] = []
    for _, record in capabilities:
        capability_id = str(record["capability_id"])
        risks = record.get("risks")
        if isinstance(risks, list):
            for index, risk in enumerate(risks):
                if isinstance(risk, str) and risk:
                    known_risks.append(
                        {
                            "risk": risk,
                            "source_record": capability_id,
                            "source_field": f"risks[{index}]",
                        }
                    )

    for _, record in gaps:
        risk = record.get("risk")
        if isinstance(risk, str) and risk:
            known_risks.append(
                {
                    "risk": risk,
                    "source_record": str(record["gap_id"]),
                    "source_field": "risk",
                }
            )

    for _, record in plans:
        risk = record.get("risk")
        if isinstance(risk, str) and risk:
            known_risks.append(
                {
                    "risk": risk,
                    "source_record": str(record["plan_id"]),
                    "source_field": "risk",
                }
            )

    recommended_next_targets: list[dict[str, str]] = []
    for _, record in gaps:
        if record.get("status") != "open":
            continue

        first_slice = record.get("recommended_first_slice")
        if isinstance(first_slice, str) and first_slice:
            recommended_next_targets.append(
                {
                    "target": first_slice,
                    "source_record": str(record["gap_id"]),
                    "source_field": "recommended_first_slice",
                }
            )

    return {
        "schema_version": "v1",
        "generated_at": generated_at
        or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_head": _repo_head(repo_root),
        "system_label": "AI-Lab",
        "model_type": "self_model",
        "generation_rule": "aggregation_only",
        "capability_counts": _count_by_status(capabilities),
        "gap_counts": _count_by_status(gaps),
        "plan_counts": _count_by_status(plans),
        "warrant_counts": _count_by_field(warrants, "warrant_state"),
        "active_capabilities": [
            str(record["capability_id"])
            for _, record in capabilities
            if record.get("status") == "implemented"
        ],
        "open_gaps": [
            str(record["gap_id"])
            for _, record in gaps
            if record.get("status") == "open"
        ],
        "open_plans": [
            str(record["plan_id"])
            for _, record in plans
            if record.get("status") in {"proposed", "admitted"}
        ],
        "admitted_plans": sorted(set(admitted_plans)),
        "capabilities": capability_records,
        "gaps": gap_records,
        "verifications": verification_records,
        "plans": plan_records,
        "warrants": warrant_records,
        "known_risks": known_risks,
        "recommended_next_targets": recommended_next_targets,
        "audit_summary": {
            "ok": bool(audit.get("ok")),
            "severity_counts": _audit_severity_counts(audit),
        },
    }


SELF_MODEL_INDEX_SOURCE_PATHS = (
    "docs/self_model/capabilities",
    "docs/self_model/gaps",
    "docs/self_model/verifications",
    "docs/self_model/plans",
    "docs/self_model/warrants",
)


def _normalized_self_model_index(index: dict[str, object]) -> dict[str, object]:
    normalized = dict(index)
    normalized.pop("generated_at", None)
    normalized.pop("repo_head", None)
    return normalized


def _git_path_changed_since(repo_root: Path, commit: str, path: str) -> bool | None:
    result = subprocess.run(
        ["git", "diff", "--quiet", f"{commit}..HEAD", "--", path],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True
    return None


def audit_self_model_index(
    repo_root: Path = Path("."),
    index_path: Path | None = None,
) -> dict[str, object]:
    repo_root = repo_root.resolve()
    resolved_index_path = index_path or repo_root / "docs" / "self_model" / "SELF_MODEL.json"

    findings: list[dict[str, str]] = []

    if not resolved_index_path.exists():
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_MISSING",
                str(resolved_index_path),
                "SELF_MODEL.json is missing.",
            )
        )
        return {"schema_version": "v1", "ok": False, "findings": findings}

    try:
        index = read_json(resolved_index_path)
    except Exception as error:
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_INVALID_JSON",
                str(resolved_index_path),
                str(error),
            )
        )
        return {"schema_version": "v1", "ok": False, "findings": findings}

    if index.get("schema_version") != "v1":
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_SCHEMA_INVALID",
                str(resolved_index_path),
                "$.schema_version must be v1.",
            )
        )

    if index.get("generation_rule") != "aggregation_only":
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_GENERATION_RULE_INVALID",
                str(resolved_index_path),
                "$.generation_rule must be aggregation_only.",
            )
        )

    stored_repo_head = index.get("repo_head")
    current_head = _repo_head(repo_root)

    if not isinstance(stored_repo_head, str) or not FULL_COMMIT_RE.match(stored_repo_head):
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_REPO_HEAD_INVALID",
                str(resolved_index_path),
                "$.repo_head must be a full 40-character lowercase git hash.",
            )
        )
    elif not _git_success(["cat-file", "-e", f"{stored_repo_head}^{{commit}}"], repo_root):
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_REPO_HEAD_MISSING",
                str(resolved_index_path),
                f"Stored repo_head is missing from git history: {stored_repo_head}",
            )
        )
    elif stored_repo_head == current_head:
        findings.append(
            _finding(
                "info",
                "SELF_MODEL_INDEX_REPO_HEAD_CURRENT",
                str(resolved_index_path),
                "Stored repo_head matches current HEAD.",
            )
        )
    else:
        changed_paths: list[str] = []
        unknown_paths: list[str] = []

        for source_path in SELF_MODEL_INDEX_SOURCE_PATHS:
            changed = _git_path_changed_since(repo_root, stored_repo_head, source_path)
            if changed is True:
                changed_paths.append(source_path)
            elif changed is None:
                unknown_paths.append(source_path)

        if changed_paths:
            findings.append(
                _finding(
                    "warn",
                    "SELF_MODEL_INDEX_SOURCE_RECORDS_CHANGED",
                    str(resolved_index_path),
                    "Self-model source records changed since stored repo_head: "
                    + ", ".join(changed_paths),
                )
            )
        elif unknown_paths:
            findings.append(
                _finding(
                    "warn",
                    "SELF_MODEL_INDEX_SOURCE_DRIFT_UNKNOWN",
                    str(resolved_index_path),
                    "Could not determine source-record drift for: "
                    + ", ".join(unknown_paths),
                )
            )
        else:
            findings.append(
                _finding(
                    "info",
                    "SELF_MODEL_INDEX_REPO_HEAD_DIFFERS_SOURCE_UNCHANGED",
                    str(resolved_index_path),
                    "Stored repo_head differs from current HEAD, but source records are unchanged.",
                )
            )

    try:
        rebuilt = build_self_model_index(
            repo_root=repo_root,
            generated_at=(
                index.get("generated_at")
                if isinstance(index.get("generated_at"), str)
                else None
            ),
        )
    except Exception as error:
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_REBUILD_FAILED",
                str(resolved_index_path),
                str(error),
            )
        )
    else:
        if _normalized_self_model_index(index) != _normalized_self_model_index(rebuilt):
            findings.append(
                _finding(
                    "warn",
                    "SELF_MODEL_INDEX_CONTENT_STALE",
                    str(resolved_index_path),
                    "Stored SELF_MODEL.json differs from a normalized rebuild.",
                )
            )
        else:
            findings.append(
                _finding(
                    "info",
                    "SELF_MODEL_INDEX_CONTENT_CURRENT",
                    str(resolved_index_path),
                    "Stored SELF_MODEL.json matches a normalized rebuild.",
                )
            )

    ok = not any(finding["severity"] == "error" for finding in findings)
    return {"schema_version": "v1", "ok": ok, "findings": findings}


def audit_self_model_index(
    repo_root: Path = Path("."),
    index_path: Path | None = None,
) -> dict[str, object]:
    repo_root = repo_root.resolve()
    resolved_index_path = index_path or repo_root / "docs" / "self_model" / "SELF_MODEL.json"

    findings: list[dict[str, str]] = []

    if not resolved_index_path.exists():
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_MISSING",
                str(resolved_index_path),
                "SELF_MODEL.json is missing.",
            )
        )
        return {"schema_version": "v1", "ok": False, "findings": findings}

    try:
        index = read_json(resolved_index_path)
    except Exception as error:
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_INVALID_JSON",
                str(resolved_index_path),
                str(error),
            )
        )
        return {"schema_version": "v1", "ok": False, "findings": findings}

    if index.get("schema_version") != "v1":
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_SCHEMA_INVALID",
                str(resolved_index_path),
                "$.schema_version must be v1.",
            )
        )

    if index.get("generation_rule") != "aggregation_only":
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_GENERATION_RULE_INVALID",
                str(resolved_index_path),
                "$.generation_rule must be aggregation_only.",
            )
        )

    stored_repo_head = index.get("repo_head")
    current_head = _repo_head(repo_root)
    changed_paths: list[str] = []
    unknown_paths: list[str] = []

    if not isinstance(stored_repo_head, str) or not FULL_COMMIT_RE.match(stored_repo_head):
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_REPO_HEAD_INVALID",
                str(resolved_index_path),
                "$.repo_head must be a full 40-character lowercase git hash.",
            )
        )
    elif not _git_success(["cat-file", "-e", f"{stored_repo_head}^{{commit}}"], repo_root):
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_REPO_HEAD_MISSING",
                str(resolved_index_path),
                f"Stored repo_head is missing from git history: {stored_repo_head}",
            )
        )
    elif stored_repo_head == current_head:
        findings.append(
            _finding(
                "info",
                "SELF_MODEL_INDEX_REPO_HEAD_CURRENT",
                str(resolved_index_path),
                "Stored repo_head matches current HEAD.",
            )
        )
    else:
        for source_path in SELF_MODEL_INDEX_SOURCE_PATHS:
            changed = _git_path_changed_since(repo_root, stored_repo_head, source_path)
            if changed is True:
                changed_paths.append(source_path)
            elif changed is None:
                unknown_paths.append(source_path)

    try:
        rebuilt = build_self_model_index(
            repo_root=repo_root,
            generated_at=(
                index.get("generated_at")
                if isinstance(index.get("generated_at"), str)
                else None
            ),
        )
    except Exception as error:
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_REBUILD_FAILED",
                str(resolved_index_path),
                str(error),
            )
        )
        content_current = False
    else:
        content_current = (
            _normalized_self_model_index(index)
            == _normalized_self_model_index(rebuilt)
        )

    if isinstance(stored_repo_head, str) and FULL_COMMIT_RE.match(stored_repo_head):
        if stored_repo_head != current_head:
            if changed_paths and content_current:
                findings.append(
                    _finding(
                        "info",
                        "SELF_MODEL_INDEX_SOURCE_RECORDS_CHANGED_CONTENT_CURRENT",
                        str(resolved_index_path),
                        "Source records changed since stored repo_head, but stored SELF_MODEL.json matches a normalized rebuild: "
                        + ", ".join(changed_paths),
                    )
                )
            elif changed_paths:
                findings.append(
                    _finding(
                        "warn",
                        "SELF_MODEL_INDEX_SOURCE_RECORDS_CHANGED",
                        str(resolved_index_path),
                        "Self-model source records changed since stored repo_head: "
                        + ", ".join(changed_paths),
                    )
                )
            elif unknown_paths:
                findings.append(
                    _finding(
                        "warn",
                        "SELF_MODEL_INDEX_SOURCE_DRIFT_UNKNOWN",
                        str(resolved_index_path),
                        "Could not determine source-record drift for: "
                        + ", ".join(unknown_paths),
                    )
                )
            else:
                findings.append(
                    _finding(
                        "info",
                        "SELF_MODEL_INDEX_REPO_HEAD_DIFFERS_SOURCE_UNCHANGED",
                        str(resolved_index_path),
                        "Stored repo_head differs from current HEAD, but source records are unchanged.",
                    )
                )

    if content_current:
        findings.append(
            _finding(
                "info",
                "SELF_MODEL_INDEX_CONTENT_CURRENT",
                str(resolved_index_path),
                "Stored SELF_MODEL.json matches a normalized rebuild.",
            )
        )
    else:
        findings.append(
            _finding(
                "error",
                "SELF_MODEL_INDEX_CONTENT_STALE",
                str(resolved_index_path),
                "Stored SELF_MODEL.json differs from a normalized rebuild.",
            )
        )

    ok = not any(finding["severity"] == "error" for finding in findings)
    return {"schema_version": "v1", "ok": ok, "findings": findings}
