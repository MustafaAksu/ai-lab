"""Compact artifact sidecar contract.

Static schema, validator, deterministic identity/path/serialization rules,
profile definitions, and staleness/fidelity semantics for derived,
AI-optimized compact sidecars attached to canonical repository artifacts.

Admitted by WARR-20260717-0001 under GAP-0002 (PLAN-20260717-0001).
Contract only: this module performs no sidecar generation, no bulk
processing, and no context-selection integration. Canonical human-readable
artifacts remain the sole authoritative source; sidecars are explicitly
derived and regenerable.

Staleness verification uses the shared three-valued vocabulary from
ai_lab.documentation.verification_outcome (GAP-0004 milestone 2): the
sidecar contract imports the vocabulary; the vocabulary imports nothing
from this module.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

from ai_lab.documentation.verification_outcome import (
    CLASS_DRIFT,
    CLASS_EVIDENCE_UNAVAILABLE,
    CLASS_OTHER,
    EVIDENCE_STATUS_NO_GIT_DIR,
    ok_from_outcome,
    rollup_from_findings,
)


SIDECAR_SCHEMA_VERSION = "v1"
TOKEN_ESTIMATOR_ID = "whitespace_word_count_v1"

PROFILE_RICH = "rich_immediate"
PROFILE_CONCISE = "concise_second_level"
SIDECAR_PROFILES = frozenset({PROFILE_RICH, PROFILE_CONCISE})

# Token ranges are validation hypotheses per WARR-20260717-0001, not
# fixed production limits. Non-compliance is a reported finding, never a
# schema-validity failure.
PROFILE_TOKEN_HYPOTHESES: Mapping[str, tuple[int, int]] = {
    PROFILE_RICH: (250, 500),
    PROFILE_CONCISE: (80, 200),
}

SEMANTIC_FIELDS = (
    "purpose",
    "status",
    "key_claims",
    "decisions",
    "results",
    "constraints",
    "risks",
    "dependencies",
    "evidence_refs",
    "uncertainty",
    "unresolved",
    "next_actions",
    "lineage",
)

_LIST_SEMANTIC_FIELDS = frozenset(
    {
        "key_claims",
        "decisions",
        "results",
        "constraints",
        "risks",
        "dependencies",
        "evidence_refs",
        "unresolved",
        "next_actions",
    }
)

FIDELITY_CATEGORIES = (
    "faithful",
    "omissive_but_flagged",
    "distorted",
    "unassessed",
)

_ARTIFACT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@|+-]{0,255}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


class SidecarError(ValueError):
    """Raised when a sidecar record violates the contract."""


def _require_string(record: Mapping[str, Any], key: str, path: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SidecarError(f"{path} must be a non-empty string")
    return value


def sidecar_id_for(source_artifact_id: str, profile: str) -> str:
    """Deterministic sidecar identity: <source_artifact_id>::<profile>."""

    if profile not in SIDECAR_PROFILES:
        raise SidecarError("unknown sidecar profile: " + str(profile))
    if not _ARTIFACT_ID_RE.match(source_artifact_id):
        raise SidecarError("invalid source artifact id")
    return f"{source_artifact_id}::{profile}"


def sidecar_relative_path(source_artifact_id: str, profile: str) -> str:
    """Deterministic path: docs/sidecars/<source_artifact_id>.<profile>.json."""

    sidecar_id_for(source_artifact_id, profile)
    return f"docs/sidecars/{source_artifact_id}.{profile}.json"


def canonical_sidecar_json(record: Mapping[str, Any]) -> str:
    """Deterministic serialization: sorted keys, two-space indent, LF."""

    return json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def estimate_tokens(text: str) -> int:
    """Whitespace word count, versioned as TOKEN_ESTIMATOR_ID."""

    return len(text.split())


def validate_sidecar_record(record: Mapping[str, Any]) -> None:
    """Schema and provenance validity. Raises SidecarError on violation.

    Profile token compliance and staleness are separate assessment
    categories and never schema failures.
    """

    if record.get("schema_version") != SIDECAR_SCHEMA_VERSION:
        raise SidecarError("$.schema_version must be " + SIDECAR_SCHEMA_VERSION)

    profile = _require_string(record, "profile", "$.profile")
    if profile not in SIDECAR_PROFILES:
        raise SidecarError("$.profile must be one of: " + ", ".join(sorted(SIDECAR_PROFILES)))

    source_artifact_id = _require_string(record, "source_artifact_id", "$.source_artifact_id")
    expected_id = sidecar_id_for(source_artifact_id, profile)
    if record.get("sidecar_id") != expected_id:
        raise SidecarError("$.sidecar_id must equal " + expected_id)

    _require_string(record, "source_path", "$.source_path")

    source_hash = _require_string(record, "source_content_hash", "$.source_content_hash")
    if not _SHA256_RE.match(source_hash):
        raise SidecarError("$.source_content_hash must be a lowercase sha256 hex digest")

    commit = _require_string(record, "source_repo_commit", "$.source_repo_commit")
    if not _FULL_COMMIT_RE.match(commit):
        raise SidecarError("$.source_repo_commit must be a full 40-character git hash")

    generator = record.get("generator")
    if not isinstance(generator, Mapping):
        raise SidecarError("$.generator must be an object")
    for key in ("provider", "identity", "version"):
        if not isinstance(generator.get(key), str) or not generator[key].strip():
            raise SidecarError(f"$.generator.{key} must be a non-empty string")

    _require_string(record, "generated_at", "$.generated_at")

    fidelity = record.get("fidelity_category", "unassessed")
    if fidelity not in FIDELITY_CATEGORIES:
        raise SidecarError(
            "$.fidelity_category must be one of: " + ", ".join(FIDELITY_CATEGORIES)
        )

    superseded_by = record.get("superseded_by")
    if superseded_by is not None and (
        not isinstance(superseded_by, str) or not superseded_by.strip()
    ):
        raise SidecarError("$.superseded_by must be null or a non-empty string")

    omitted = record.get("omitted_fields")
    if not isinstance(omitted, list) or not all(isinstance(x, str) for x in omitted):
        raise SidecarError("$.omitted_fields must be a list of strings")
    omitted_set = set(omitted)
    unknown = omitted_set - set(SEMANTIC_FIELDS)
    if unknown:
        raise SidecarError(
            "$.omitted_fields contains unknown fields: " + ", ".join(sorted(unknown))
        )
    if profile == PROFILE_RICH and omitted_set:
        raise SidecarError("rich_immediate sidecars must not omit semantic fields")

    for field in SEMANTIC_FIELDS:
        present = field in record
        listed = field in omitted_set
        if present and listed:
            raise SidecarError(f"$.{field} is both present and listed in omitted_fields")
        if not present and not listed:
            raise SidecarError(
                f"$.{field} must be present or explicitly listed in omitted_fields"
            )
        if present:
            value = record[field]
            if field in _LIST_SEMANTIC_FIELDS:
                if not isinstance(value, list) or not all(
                    isinstance(x, str) and x.strip() for x in value
                ):
                    raise SidecarError(f"$.{field} must be a list of non-empty strings")
            else:
                if not isinstance(value, str) or not value.strip():
                    raise SidecarError(f"$.{field} must be a non-empty string")


def assess_profile_compliance(record: Mapping[str, Any]) -> list[dict[str, str]]:
    """Report token-hypothesis compliance findings. Never raises for size."""

    validate_sidecar_record(record)
    low, high = PROFILE_TOKEN_HYPOTHESES[str(record["profile"])]
    tokens = estimate_tokens(canonical_sidecar_json(record))
    findings: list[dict[str, str]] = []
    if tokens > high:
        findings.append(
            {
                "severity": "warn",
                "code": "SIDECAR_OVER_TOKEN_HYPOTHESIS",
                "class": CLASS_OTHER,
                "message": (
                    f"{record['sidecar_id']} estimated {tokens} tokens exceeds the "
                    f"{low}-{high} hypothesis range ({TOKEN_ESTIMATOR_ID})."
                ),
            }
        )
    elif tokens < low:
        findings.append(
            {
                "severity": "info",
                "code": "SIDECAR_UNDER_TOKEN_HYPOTHESIS",
                "class": CLASS_OTHER,
                "message": (
                    f"{record['sidecar_id']} estimated {tokens} tokens is below the "
                    f"{low}-{high} hypothesis range ({TOKEN_ESTIMATOR_ID})."
                ),
            }
        )
    return findings


def assess_staleness(
    record: Mapping[str, Any],
    repo_root: Path = Path("."),
) -> dict[str, Any]:
    """Three-valued staleness: verified_current, stale, or unverifiable.

    Compares the recorded source_content_hash with the current content of
    source_path. A missing or unreadable source is evidence unavailability,
    not confirmed drift.
    """

    validate_sidecar_record(record)
    findings: list[dict[str, str]] = []
    source_path = repo_root / str(record["source_path"])

    try:
        content = source_path.read_bytes()
    except OSError:
        findings.append(
            {
                "severity": "warn",
                "code": "SIDECAR_SOURCE_UNREADABLE",
                "class": CLASS_EVIDENCE_UNAVAILABLE,
                "evidence_status": EVIDENCE_STATUS_NO_GIT_DIR
                if not (repo_root / ".git").exists()
                else "other",
                "message": f"Source artifact unreadable: {record['source_path']}",
            }
        )
    else:
        actual = hashlib.sha256(content).hexdigest()
        if actual == record["source_content_hash"]:
            findings.append(
                {
                    "severity": "info",
                    "code": "SIDECAR_SOURCE_HASH_MATCH",
                    "class": CLASS_OTHER,
                    "message": "Source content hash matches the sidecar provenance.",
                }
            )
        else:
            findings.append(
                {
                    "severity": "error",
                    "code": "SIDECAR_SOURCE_HASH_MISMATCH",
                    "class": CLASS_DRIFT,
                    "message": (
                        "Source content changed since sidecar generation; "
                        "the sidecar is stale and must be regenerated, "
                        "superseded, or deleted."
                    ),
                }
            )

    outcome = rollup_from_findings(findings)
    return {
        "schema_version": "v1",
        "ok": ok_from_outcome(outcome),
        "verification_outcome": outcome,
        "findings": findings,
    }
