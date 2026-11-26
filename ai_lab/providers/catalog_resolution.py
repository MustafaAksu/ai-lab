"""Historical catalog-resolution codecs and the Step 3A refusal boundary.

DECISION-20261126-0001 replaces the old single-source positive entry point.
``resolve_identity`` never projects ``resolved=True``: a complete explicit r2
query/context may be assessed, but the legacy return shape cannot represent
its source/identity/qualification distinctions. No-context calls refuse.

IdentityResolution v1 remains a historical, non-authoritative annotation format.
Its reason vocabulary is preserved; r2 refusal/assessment results must never be
coerced into it. Neither a historical annotation nor its graph seed establishes
current executor identity, independence, qualification or authorization.
"""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from typing import Any, Mapping, Sequence

from ai_lab.providers.catalog import (
    CatalogRecordError,
    DEFAULT_FRESHNESS_WINDOW_DAYS,
    CHANNEL_STATUSES,
    CONTENT_EVIDENCE_STATUSES,
    canonical_catalog_json,
    parse_timestamp,
    validate_catalog_record,
)


RESOLUTION_SCHEMA_VERSION = "v1"
RESOLUTION_DIR = "docs/catalog/resolutions"

REASON_NO_APPLICABLE_ASSERTION = "no_applicable_assertion"
REASON_SNAPSHOT_AFTER_INVOCATION = "snapshot_after_invocation"
REASON_AMBIGUOUS_ASSERTIONS = "ambiguous_assertions"
REASON_EXPIRED_FRESHNESS_WINDOW = "expired_freshness_window"
REASON_CONTRADICTED_EVIDENCE = "contradicted_evidence"

NON_RESOLUTION_REASONS = (
    REASON_NO_APPLICABLE_ASSERTION,
    REASON_SNAPSHOT_AFTER_INVOCATION,
    REASON_AMBIGUOUS_ASSERTIONS,
    REASON_EXPIRED_FRESHNESS_WINDOW,
    REASON_CONTRADICTED_EVIDENCE,
)

# Slice B predicates (ABS-0004 v5 Section 5). No predicate outside this
# list may be emitted by this slice (warrant condition 7).
SLICE_B_PREDICATES = ("resolved_to", "asserted_by", "concerns", "captured")


class ResolutionError(ValueError):
    """Raised when a resolution record violates the Slice B schema."""


QUALIFICATION_SCHEMA_VERSION = "ai_lab.qualification.r2/1"
LEGACY_CONTEXT_REQUIRED = "LEGACY_CONTEXT_REQUIRED"
LEGACY_POSITIVE_DISABLED = "LEGACY_POSITIVE_DISABLED"


def _legacy_assessment(
    *, query: Mapping[str, Any], anchor: Any,
    bindings: Sequence[tuple[Mapping[str, Any], Sequence[str]]],
) -> tuple[dict[str, Any] | None, tuple[str, ...]]:
    """Assess an explicitly supplied query after exact legacy-subject binding.

    The anchor is obtained outside Query by the consumer. Every supplied legacy
    invocation must equal the complete parsed, digest-checked invocation bytes
    of its named query side. Failure never calls the retired resolver.
    """
    try:
        from ai_lab.providers.qualification_records import (
            canonical_bytes, record_ref, strict_loads, validate_shape,
        )
        from ai_lab.providers.qualification import (
            evaluate_production_r2, evaluate_synthetic_r2,
        )

        validate_shape(dict(query), "Query")
        domain = anchor.domain
        if domain not in {"synthetic", "production"} or query.get("domain") != domain:
            return None, ("DOMAIN_MISMATCH",)
        for invocation, sides in bindings:
            actual = canonical_bytes(dict(invocation))
            candidates = [
                canonical_bytes(strict_loads(anchor.read(query[side]["invocation_ref"])))
                for side in sides
            ]
            if actual not in candidates:
                return None, ("CONTEXT_ANCHOR_MISMATCH",)
        if domain == "synthetic":
            result = evaluate_synthetic_r2(query, anchor=anchor)
        else:
            result = evaluate_production_r2(query, anchor=anchor)
        if (not isinstance(result, dict)
                or result.get("schema_version") != QUALIFICATION_SCHEMA_VERSION
                or result.get("record_kind") != "assessment_result"
                or result.get("domain") != domain):
            return None, ("NOT_EVALUATED",)
        validate_shape(result, "AssessmentResult")
        expected_query = record_ref(query["query_id"], canonical_bytes(dict(query)))
        if (result.get("query_ref") != expected_query
                or result.get("evidence_context_ref") != query["evidence_context_ref"]):
            return None, ("CONTEXT_ANCHOR_MISMATCH",)
        return result, ()
    except Exception:
        # A disabled/unavailable evaluator, malformed input or failed read is a
        # non-permitting boundary. Do not recover the old positive code path.
        return None, ("NOT_EVALUATED",)


def _assessment_ref(result: Mapping[str, Any] | None) -> dict[str, str] | None:
    if result is None:
        return None
    try:
        from ai_lab.providers.qualification_records import assessment_reference
        return assessment_reference(result)
    except Exception:
        return None


def resolve_identity(
    *,
    invocation: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    capture: Mapping[str, Any],
    freshness_window_days: int = DEFAULT_FRESHNESS_WINDOW_DAYS,
    query: Mapping[str, Any] | None = None,
    anchor: Any = None,
) -> dict[str, Any]:
    """Return a noncanonical, nonpersistable legacy refusal projection.

    Snapshot/capture/window arguments remain for call compatibility only. They
    cannot construct or narrow the governed source context. The explicit query
    and consumer anchor select the complete r2 evaluation, which remains
    available through its assessment reference, never ``resolved=True``.
    """
    result = None
    diagnostics: tuple[str, ...] = ()
    if query is None or anchor is None:
        reason = LEGACY_CONTEXT_REQUIRED
    else:
        reason = LEGACY_POSITIVE_DISABLED
        result, diagnostics = _legacy_assessment(
            query=query, anchor=anchor,
            bindings=((invocation, ("left", "right")),),
        )
    return {
        "schema_version": QUALIFICATION_SCHEMA_VERSION,
        "record_kind": "legacy_resolution_refusal",
        "resolved": False,
        "resolved_identity": None,
        "reason": reason,
        "assessment_ref": _assessment_ref(result),
        "diagnostic_codes": list(diagnostics),
    }


def resolution_id_for(record: Mapping[str, Any]) -> str:
    fields = ("schema_version", "invocation_id", "snapshot_id", "capture_id", "resolved_at")
    parts = []
    for name in fields:
        if name not in record:
            raise ResolutionError(f"identity field {name} is missing")
        parts.append(f"{name}={record[name]!s}")
    payload = "\u001f".join(parts)
    return "RES-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def build_resolution_record(
    *,
    invocation: Mapping[str, Any],
    outcome: Mapping[str, Any],
    resolved_at: str,
    freshness_window_days: int = DEFAULT_FRESHNESS_WINDOW_DAYS,
) -> dict[str, Any]:
    """Serialize an explicit historical v1 outcome without changing its standing.

    This utility does not resolve identity or validate a binding. Its output is
    history/diagnostic-only and cannot be consumed as a current r2 assessment.
    The InvocationRecord is never touched; r2 outcomes are explicitly rejected.
    """

    if not isinstance(outcome, Mapping):
        raise ResolutionError("historical outcome must be an object")
    if (outcome.get("schema_version") == QUALIFICATION_SCHEMA_VERSION
            or outcome.get("record_kind") in ("legacy_resolution_refusal", "assessment_result")
            or any(key in outcome for key in ("R_identity", "Q_identity", "Q_C3_C10", "assessment_ref"))):
        raise ResolutionError("r2 assessment/refusal cannot be a historical v1 annotation")
    if type(outcome.get("resolved")) is not bool:
        raise ResolutionError("historical outcome resolved must be a boolean; coercion is forbidden")
    if type(freshness_window_days) is not int or freshness_window_days < 0:
        raise ResolutionError("historical outcome freshness_window_days must be a nonnegative integer")
    if outcome["resolved"]:
        for key, prefix in (("resolved_identity", "MID"), ("snapshot_id", "SNAP"), ("capture_id", "CAP")):
            value = outcome.get(key)
            if not isinstance(value, str) or re.fullmatch(prefix + r"-[0-9a-f]{16}", value) is None:
                raise ResolutionError(f"historical outcome {key} must be a valid {prefix} reference")
        if (not isinstance(outcome.get("content_evidence_status"), str)
                or outcome["content_evidence_status"] not in CONTENT_EVIDENCE_STATUSES):
            raise ResolutionError("historical outcome content_evidence_status is invalid")
        if (not isinstance(outcome.get("channel_authentication_status"), str)
                or outcome["channel_authentication_status"] not in CHANNEL_STATUSES):
            raise ResolutionError("historical outcome channel_authentication_status is invalid")

    record: dict[str, Any] = {
        "schema_version": RESOLUTION_SCHEMA_VERSION,
        "record_kind": "identity_resolution",
        "invocation_id": invocation["invocation_id"],
        "requested_model_name": invocation["requested_model_name"],
        "service_endpoint": invocation["service_endpoint"],
        "resolved_at": resolved_at,
        "freshness_window_days": freshness_window_days,
        "resolved": outcome["resolved"],
        "snapshot_id": outcome.get("snapshot_id"),
        "capture_id": outcome.get("capture_id"),
        "resolved_identity": outcome.get("resolved_identity"),
        "non_resolution_reason": outcome.get("reason"),
        "non_resolution_detail": {
            k: v
            for k, v in outcome.items()
            if k not in {"resolved", "reason", "resolved_identity", "snapshot_id", "capture_id", "content_evidence_status", "channel_authentication_status", "assertion_subject"}
        },
        "content_evidence_status": outcome.get("content_evidence_status"),
        "channel_authentication_status": outcome.get("channel_authentication_status"),
    }
    record["record_id"] = resolution_id_for(record)
    validate_resolution_record(record)
    return record


def validate_resolution_record(record: Mapping[str, Any]) -> None:
    if not isinstance(record, Mapping):
        raise ResolutionError("$ must be an object")
    if record.get("schema_version") != RESOLUTION_SCHEMA_VERSION:
        raise ResolutionError(f"$.schema_version must be {RESOLUTION_SCHEMA_VERSION!r}")
    if record.get("record_kind") != "identity_resolution":
        raise ResolutionError("$.record_kind must be identity_resolution")

    for field in ("invocation_id", "requested_model_name", "service_endpoint", "resolved_at"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ResolutionError(f"$.{field} must be a non-empty string")

    parse_timestamp(record["resolved_at"], "$.resolved_at")

    if not isinstance(record.get("resolved"), bool):
        raise ResolutionError("$.resolved must be a boolean")

    if record["resolved"]:
        for field in ("resolved_identity", "snapshot_id", "capture_id", "content_evidence_status"):
            if not record.get(field):
                raise ResolutionError(f"$.{field} is required for a resolved annotation")
        if record.get("non_resolution_reason") is not None:
            raise ResolutionError(
                "$.non_resolution_reason must be null on a resolved annotation"
            )
    else:
        reason = record.get("non_resolution_reason")
        if reason not in NON_RESOLUTION_REASONS:
            raise ResolutionError(
                f"$.non_resolution_reason must be one of {list(NON_RESOLUTION_REASONS)}; "
                f"got {reason!r}. Non-resolution is never a silent default."
            )
        if record.get("resolved_identity") is not None:
            raise ResolutionError(
                "$.resolved_identity must be null on an unresolved annotation"
            )

    expected = resolution_id_for(record)
    if record.get("record_id") != expected:
        raise ResolutionError(
            f"$.record_id {record.get('record_id')!r} does not match {expected!r}"
        )


def canonical_resolution_json(record: Mapping[str, Any]) -> str:
    """Deterministic serialization with the mandated status-field order."""

    return canonical_catalog_json(record)


def resolution_relative_path(record_id: str) -> str:
    if not record_id.startswith("RES-") or len(record_id) != 20:
        raise ResolutionError(f"malformed resolution id: {record_id!r}")
    return f"{RESOLUTION_DIR}/{record_id}.json"


def resolution_relations(record: Mapping[str, Any]):
    """Slice B relations in GraphRelation shape.

    Emits only registered Slice B predicates; any other predicate raises.
    """

    from ai_lab.documentation.graph_neighborhood import GraphRelation

    validate_resolution_record(record)
    relations: list[GraphRelation] = []
    evidence = resolution_relative_path(record["record_id"])

    def relate(source_id: str, predicate: str, target_id: str) -> None:
        if predicate not in SLICE_B_PREDICATES:
            raise ResolutionError(
                f"predicate {predicate!r} is outside the Slice B list "
                f"{list(SLICE_B_PREDICATES)} (WARR-20260723-0001 condition 7)"
            )
        relations.append(
            GraphRelation(
                source_id=source_id,
                predicate=predicate,
                target_id=target_id,
                relation_source="future_edge_seed",
                authoritative=False,
                scope="catalog_identity_resolution_slice_b",
                evidence=evidence,
            )
        )

    if record["resolved"]:
        relate(record["invocation_id"], "resolved_to", record["resolved_identity"])
        relate(record["capture_id"], "captured", record["snapshot_id"])
    return tuple(relations)


def write_resolution_record(record: Mapping[str, Any], repo_root) -> Any:
    """Preserve historical bytes atomically; reject a same-ID overwrite.

    New r2 assessments/refusals belong to their own consumer boundary and cannot
    be written here. Identical historical replay is idempotent.
    """
    from pathlib import Path

    validate_resolution_record(record)
    target = Path(repo_root) / resolution_relative_path(record["record_id"])
    target.parent.mkdir(parents=True, exist_ok=True)
    data = canonical_resolution_json(record).encode("utf-8")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".resolution-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError:
            if target.is_symlink() or target.read_bytes() != data:
                raise ResolutionError("historical resolution ID already names different bytes")
        return target
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
