from __future__ import annotations

import hashlib
import json
import re
import subprocess
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
