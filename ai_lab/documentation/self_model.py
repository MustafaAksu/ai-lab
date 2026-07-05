from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


class SelfModelError(ValueError):
    """Raised when a self-model record is structurally invalid."""


CAPABILITY_STATUSES = {"implemented", "partial", "experimental", "planned", "deprecated"}
GAP_STATUSES = {"open", "accepted", "closed", "deferred"}
GAP_PRIORITIES = {"low", "medium", "high"}
ADMITTING_DECISIONS = {"admit", "admit_with_warning"}

CAPABILITY_ID_RE = re.compile(r"^CAP-\d{4}$")
GAP_ID_RE = re.compile(r"^GAP-\d{4}$")
VERIFY_ID_RE = re.compile(r"^VERIFY-\d{8}-\d{4}$")
AUDIT_ID_RE = re.compile(r"^AUDIT-\d{8}-\d{4}$")
PLAN_ID_RE = re.compile(r"^PLAN-\d{8}-\d{4}$")
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

    ok = not any(finding["severity"] == "error" for finding in findings)
    return {"schema_version": "v1", "ok": ok, "findings": findings}



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


def build_self_model_index(
    repo_root: Path = Path("."),
    generated_at: str | None = None,
) -> dict[str, object]:
    repo_root = repo_root.resolve()

    capabilities = _load_valid_records(
        repo_root / "docs" / "self_model" / "capabilities",
        "CAP-*.json",
        validate_capability_record,
    )
    gaps = _load_valid_records(
        repo_root / "docs" / "self_model" / "gaps",
        "GAP-*.json",
        validate_gap_record,
    )
    verifications = _load_valid_records(
        repo_root / "docs" / "self_model" / "verifications",
        "VERIFY-*.json",
        validate_verification_record,
    )
    plans = _load_valid_records(
        repo_root / "docs" / "self_model" / "plans",
        "PLAN-*.json",
        validate_plan_record,
    )

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
        "capabilities": capability_records,
        "gaps": gap_records,
        "verifications": verification_records,
        "plans": plan_records,
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
                "warn",
                "SELF_MODEL_INDEX_CONTENT_STALE",
                str(resolved_index_path),
                "Stored SELF_MODEL.json differs from a normalized rebuild.",
            )
        )

    ok = not any(finding["severity"] == "error" for finding in findings)
    return {"schema_version": "v1", "ok": ok, "findings": findings}
