"""Catalog identity resolution (ABS-0004 v5 Slice B).

Pure functions over stored snapshots, plus the append-only
IdentityResolution annotation. Admitted by WARR-20260723-0001.

Resolution never mutates a captured InvocationRecord. An invocation's
``identity_verification_status`` stays as captured forever; resolution is
recorded beside it as a separate annotation referencing the invocation by
id. Consumers must join the two (see docs/self_model/CATALOG_RECORDS.md).

Non-resolution is always an enumerated reason, never a silent default:

- ``no_applicable_assertion``: no assertion binds this endpoint and
  requested name.
- ``snapshot_after_invocation``: the snapshot was observed after the
  invocation occurred, so it cannot witness what was offered before.
- ``ambiguous_assertions``: more than one applicable assertion resolves to
  different targets; ambiguity blocks resolution rather than picking a
  winner.
- ``expired_freshness_window``: the snapshot predates the invocation by
  more than the configured window.
- ``contradicted_evidence``: the capture backing the snapshot carries
  ``content_evidence_status: contradicted`` (warrant condition 1). The
  resolver blocks rather than proceeding mechanically over contradicted
  evidence, and blocking is not an admissibility judgment: admissibility
  is Slice D's, and this rule only declines to act.

Purity: resolve_identity reads only its arguments. It performs no I/O,
consults no clock, and returns the same output for the same inputs. The
resolution timestamp is supplied by the caller for exactly this reason.
"""

from __future__ import annotations

import hashlib
import json
from datetime import timedelta
from typing import Any, Mapping, Sequence

from ai_lab.providers.catalog import (
    CatalogRecordError,
    DEFAULT_FRESHNESS_WINDOW_DAYS,
    EVIDENCE_CONTRADICTED,
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


def resolve_identity(
    *,
    invocation: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    capture: Mapping[str, Any],
    freshness_window_days: int = DEFAULT_FRESHNESS_WINDOW_DAYS,
) -> dict[str, Any]:
    """Resolve one invocation against one snapshot. Pure.

    Returns a dict with ``resolved`` true and ``resolved_identity``, or
    ``resolved`` false and an enumerated ``reason``. Never raises for a
    non-resolution; raises only on malformed input.
    """

    validate_catalog_record(snapshot)
    validate_catalog_record(capture)

    if capture.get("snapshot_id") != snapshot.get("record_id"):
        raise ResolutionError("capture does not describe this snapshot")

    requested = invocation.get("requested_model_name")
    endpoint = invocation.get("service_endpoint")
    if not requested or not endpoint:
        raise ResolutionError("invocation lacks requested_model_name or service_endpoint")

    occurred_at = parse_timestamp(invocation["occurred_at"], "$.occurred_at")
    observed_at = parse_timestamp(snapshot["observed_at"], "$.observed_at")

    def outcome(reason: str, **extra: Any) -> dict[str, Any]:
        return {"resolved": False, "reason": reason, **extra}

    # Contradiction blocks before anything else: the resolver declines to
    # act on contradicted evidence rather than deciding its admissibility.
    if capture.get("content_evidence_status") == EVIDENCE_CONTRADICTED:
        return outcome(REASON_CONTRADICTED_EVIDENCE, capture_id=capture["record_id"])

    # Temporal precedence, inclusive at the boundary: an observation at
    # instant T did witness the state at instant T.
    if observed_at > occurred_at:
        return outcome(
            REASON_SNAPSHOT_AFTER_INVOCATION,
            observed_at=snapshot["observed_at"],
            occurred_at=invocation["occurred_at"],
        )

    if occurred_at - observed_at > timedelta(days=freshness_window_days):
        return outcome(
            REASON_EXPIRED_FRESHNESS_WINDOW,
            window_days=freshness_window_days,
            age_days=(occurred_at - observed_at).days,
        )

    applicable = [
        assertion
        for assertion in snapshot["assertions"]
        if assertion["assertion_predicate"] == "resolves_to"
        and assertion["assertion_subject"] == requested
        and _assertion_covers(assertion, invocation["occurred_at"])
    ]

    if not applicable:
        return outcome(REASON_NO_APPLICABLE_ASSERTION, requested_model_name=requested)

    targets = {assertion["assertion_value_or_target"] for assertion in applicable}
    if len(targets) > 1:
        return outcome(REASON_AMBIGUOUS_ASSERTIONS, candidates=sorted(targets))

    return {
        "resolved": True,
        "resolved_identity": applicable[0]["assertion_value_or_target"],
        "assertion_subject": requested,
        "snapshot_id": snapshot["record_id"],
        "capture_id": capture["record_id"],
        # Inherited, never recomputed: the annotation may not claim a
        # stronger evidence class than the capture it rests on.
        "content_evidence_status": capture["content_evidence_status"],
        "channel_authentication_status": capture["channel_authentication_status"],
    }


def _assertion_covers(assertion: Mapping[str, Any], occurred_at: str) -> bool:
    moment = parse_timestamp(occurred_at, "$.occurred_at")
    valid_from = parse_timestamp(assertion["valid_from"], "$.valid_from")
    if moment < valid_from:
        return False
    if assertion["valid_until"] is not None:
        valid_until = parse_timestamp(assertion["valid_until"], "$.valid_until")
        if moment > valid_until:
            return False
    return True


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
    """Assemble an append-only IdentityResolution annotation.

    The annotation references the invocation by id and is written beside
    it; the InvocationRecord itself is never touched.
    """

    record: dict[str, Any] = {
        "schema_version": RESOLUTION_SCHEMA_VERSION,
        "record_kind": "identity_resolution",
        "invocation_id": invocation["invocation_id"],
        "requested_model_name": invocation["requested_model_name"],
        "service_endpoint": invocation["service_endpoint"],
        "resolved_at": resolved_at,
        "freshness_window_days": freshness_window_days,
        "resolved": bool(outcome.get("resolved")),
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
    from pathlib import Path

    validate_resolution_record(record)
    target = Path(repo_root) / resolution_relative_path(record["record_id"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(canonical_resolution_json(record), encoding="utf-8")
    return target
