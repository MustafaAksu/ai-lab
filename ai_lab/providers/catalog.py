"""Catalog record family (ABS-0004 v5 Slice B).

Schema v1 for ModelIdentity, ServiceEndpointIdentity, CatalogAssertion,
CatalogSnapshot, and CatalogCapture, with validators, canonical
serialization, and deterministic identity and path rules.

Admitted by WARR-20260723-0001 under GAP-0005 (PLAN-20260723-0001),
subject to nine binding conditions recorded in that warrant.

Evidence classing
-----------------
A CatalogCapture carries two status fields that are independent by
construction and may never be merged, defaulted from one another, or
derived from one another (warrant condition 3):

- ``channel_authentication_status`` uses the shared three-valued
  verification-outcome vocabulary. It records what was independently
  established about the channel a claim arrived through. This is genuine
  evidence: it is not controlled by the content of the claim.
- ``content_evidence_status`` uses a disjoint evidence-class vocabulary
  (self_asserted, independently_corroborated, contradicted, unassessed).
  It records what was established about the truth of the claim. A capture
  whose source is the provider describing its own catalog may never carry
  anything stronger than self_asserted, however well the channel
  authenticated (ABS-0004 v5 adopted constraint).

The two vocabularies are disjoint sets, checked by ``VOCABULARY_DISJOINT``,
so a value from one can never be silently accepted in the other.

Canonical serialization places ``content_evidence_status`` immediately
before ``channel_authentication_status`` (warrant condition 2). This is a
mitigation, not a control: a downstream renderer can still display channel
strength alone and mislead a reader. See docs/self_model/CATALOG_RECORDS.md.

Timestamps
----------
All record timestamps are ISO 8601 with explicit UTC offset and are
compared at whole-microsecond precision after normalization to UTC
(warrant condition 9). The temporal precedence check is inclusive: a
snapshot observed at exactly the invocation's occurrence instant is
admissible, on the reasoning that an observation at instant T did witness
the state at instant T. Ties therefore resolve in favour of resolution;
anything later does not.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from ai_lab.documentation.verification_outcome import (
    STALE,
    UNVERIFIABLE,
    VERIFIED_CURRENT,
)


CATALOG_SCHEMA_VERSION = "v1"
CATALOG_DIR = "docs/catalog"

# Freshness window (warrant condition 4): declared, not deferred.
DEFAULT_FRESHNESS_WINDOW_DAYS = 30

RECORD_KIND_MODEL_IDENTITY = "model_identity"
RECORD_KIND_ENDPOINT_IDENTITY = "service_endpoint_identity"
RECORD_KIND_SNAPSHOT = "catalog_snapshot"
RECORD_KIND_CAPTURE = "catalog_capture"
RECORD_KINDS = frozenset(
    {
        RECORD_KIND_MODEL_IDENTITY,
        RECORD_KIND_ENDPOINT_IDENTITY,
        RECORD_KIND_SNAPSHOT,
        RECORD_KIND_CAPTURE,
    }
)

ID_PREFIXES = {
    RECORD_KIND_MODEL_IDENTITY: "MID",
    RECORD_KIND_ENDPOINT_IDENTITY: "EID",
    RECORD_KIND_SNAPSHOT: "SNAP",
    RECORD_KIND_CAPTURE: "CAP",
}

# Channel authentication reuses the shared three-valued vocabulary.
CHANNEL_STATUSES = frozenset({VERIFIED_CURRENT, STALE, UNVERIFIABLE})

# Content evidence uses a disjoint evidence-class vocabulary.
EVIDENCE_SELF_ASSERTED = "self_asserted"
EVIDENCE_INDEPENDENTLY_CORROBORATED = "independently_corroborated"
EVIDENCE_CONTRADICTED = "contradicted"
EVIDENCE_UNASSESSED = "unassessed"
CONTENT_EVIDENCE_STATUSES = frozenset(
    {
        EVIDENCE_SELF_ASSERTED,
        EVIDENCE_INDEPENDENTLY_CORROBORATED,
        EVIDENCE_CONTRADICTED,
        EVIDENCE_UNASSESSED,
    }
)

# The two vocabularies must never overlap; a shared value would let one
# field be silently defaulted from the other.
VOCABULARY_DISJOINT = not (CHANNEL_STATUSES & CONTENT_EVIDENCE_STATUSES)

SOURCE_PROVIDER_SELF_REPORT = "provider_self_report"
SOURCE_OPERATOR_ENTERED = "operator_entered"
SOURCE_THIRD_PARTY = "third_party_record"
SOURCE_TYPES = frozenset(
    {SOURCE_PROVIDER_SELF_REPORT, SOURCE_OPERATOR_ENTERED, SOURCE_THIRD_PARTY}
)

# Evidence classes a provider's self-report may never claim.
FORBIDDEN_FOR_SELF_REPORT = frozenset({EVIDENCE_INDEPENDENTLY_CORROBORATED})

ASSERTION_PREDICATES = frozenset(
    {
        "resolves_to",
        "context_limit",
        "price_input_per_mtok",
        "price_output_per_mtok",
        "deprecated",
        "region",
        "modality",
    }
)

_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ID_RE = re.compile(r"^(MID|EID|SNAP|CAP)-[0-9a-f]{16}$")


class CatalogRecordError(ValueError):
    """Raised when a catalog record violates the Slice B schema."""


def parse_timestamp(value: str, path: str) -> datetime:
    """Parse an ISO 8601 timestamp, requiring an explicit offset."""

    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise CatalogRecordError(f"{path} must be an ISO 8601 timestamp") from error
    if parsed.tzinfo is None:
        raise CatalogRecordError(f"{path} must carry an explicit UTC offset")
    return parsed.astimezone(timezone.utc)


def digest_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_catalog_json(record: Mapping[str, Any]) -> str:
    """Deterministic serialization with the mandated status-field order.

    Keys are sorted, except that within a capture record
    ``content_evidence_status`` is emitted immediately before
    ``channel_authentication_status`` (warrant condition 2).
    """

    ordered = _order_for_serialization(record)
    return json.dumps(ordered, indent=2, ensure_ascii=False) + "\n"


def _order_for_serialization(node: Any) -> Any:
    if isinstance(node, Mapping):
        keys = sorted(node)
        if "content_evidence_status" in keys and "channel_authentication_status" in keys:
            keys.remove("content_evidence_status")
            keys.remove("channel_authentication_status")
            anchor = keys.index("capture_success") + 1 if "capture_success" in keys else 0
            keys[anchor:anchor] = [
                "content_evidence_status",
                "channel_authentication_status",
            ]
        return {key: _order_for_serialization(node[key]) for key in keys}
    if isinstance(node, list):
        return [_order_for_serialization(item) for item in node]
    return node


def catalog_id_for(record: Mapping[str, Any]) -> str:
    """Deterministic identity over the record's enumerated identity fields."""

    kind = record.get("record_kind")
    if kind not in RECORD_KINDS:
        raise CatalogRecordError(f"unknown record_kind: {kind!r}")

    if kind == RECORD_KIND_MODEL_IDENTITY:
        fields = ("record_kind", "originator_id", "canonical_name", "release_identity")
    elif kind == RECORD_KIND_ENDPOINT_IDENTITY:
        fields = ("record_kind", "operating_organization", "endpoint_identifier")
    elif kind == RECORD_KIND_SNAPSHOT:
        fields = ("record_kind", "service_endpoint_id", "observed_at", "source_set_digest")
    else:
        fields = ("record_kind", "snapshot_id", "captured_at", "content_digest")

    parts = []
    for name in fields:
        if name not in record:
            raise CatalogRecordError(f"identity field {name} is missing")
        parts.append(f"{name}={record[name]!s}")
    payload = "\u001f".join(parts)
    return f"{ID_PREFIXES[kind]}-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def catalog_relative_path(record_id: str) -> str:
    if not _ID_RE.match(record_id):
        raise CatalogRecordError(f"malformed catalog id: {record_id!r}")
    prefix = record_id.split("-", 1)[0].lower()
    return f"{CATALOG_DIR}/{prefix}/{record_id}.json"


def _require_string(node: Mapping[str, Any], key: str, path: str) -> str:
    value = node.get(key)
    if not isinstance(value, str) or not value.strip():
        raise CatalogRecordError(f"{path} must be a non-empty string")
    return value


def _require_choice(node: Mapping[str, Any], key: str, allowed, path: str) -> str:
    value = _require_string(node, key, path)
    if value not in allowed:
        raise CatalogRecordError(
            f"{path} must be one of {sorted(allowed)}; got {value!r}"
        )
    return value


def validate_assertion(assertion: Mapping[str, Any], path: str) -> None:
    """One claim per assertion; heterogeneous records are rejected."""

    required = (
        "assertion_subject",
        "assertion_predicate",
        "assertion_value_or_target",
        "unit",
        "scope",
        "valid_from",
        "valid_until",
        "superseded_by",
        "source",
    )
    for field in required:
        if field not in assertion:
            raise CatalogRecordError(f"{path}.{field} is required (may be null)")

    unexpected = set(assertion) - set(required)
    if unexpected:
        raise CatalogRecordError(
            f"{path} has unknown fields: {sorted(unexpected)}; an assertion carries "
            "exactly one atomic claim"
        )

    _require_string(assertion, "assertion_subject", f"{path}.assertion_subject")
    _require_choice(
        assertion, "assertion_predicate", ASSERTION_PREDICATES, f"{path}.assertion_predicate"
    )
    if assertion["assertion_value_or_target"] is None:
        raise CatalogRecordError(f"{path}.assertion_value_or_target must not be null")
    if isinstance(assertion["assertion_value_or_target"], (list, dict)):
        raise CatalogRecordError(
            f"{path}.assertion_value_or_target must be a scalar; an assertion "
            "carries exactly one atomic claim"
        )

    parse_timestamp(assertion["valid_from"], f"{path}.valid_from")
    if assertion["valid_until"] is not None:
        parse_timestamp(assertion["valid_until"], f"{path}.valid_until")
    _require_string(assertion, "source", f"{path}.source")


def validate_catalog_record(record: Mapping[str, Any]) -> None:
    """Schema validity for any Slice B catalog record."""

    if not isinstance(record, Mapping):
        raise CatalogRecordError("$ must be an object")

    version = _require_string(record, "schema_version", "$.schema_version")
    if version != CATALOG_SCHEMA_VERSION:
        raise CatalogRecordError(
            f"$.schema_version must be {CATALOG_SCHEMA_VERSION!r}; got {version!r}"
        )

    kind = _require_choice(record, "record_kind", RECORD_KINDS, "$.record_kind")

    if kind == RECORD_KIND_MODEL_IDENTITY:
        _require_string(record, "originator_id", "$.originator_id")
        _require_string(record, "canonical_name", "$.canonical_name")
        if record.get("release_identity") is None:
            raise CatalogRecordError(
                "$.release_identity is required (may be the string 'unknown')"
            )
    elif kind == RECORD_KIND_ENDPOINT_IDENTITY:
        _require_string(record, "operating_organization", "$.operating_organization")
        _require_string(record, "endpoint_identifier", "$.endpoint_identifier")
    elif kind == RECORD_KIND_SNAPSHOT:
        _require_string(record, "service_endpoint_id", "$.service_endpoint_id")
        parse_timestamp(record.get("observed_at", ""), "$.observed_at")
        _require_string(record, "source_set_digest", "$.source_set_digest")
        assertions = record.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            raise CatalogRecordError("$.assertions must be a non-empty list")
        for index, assertion in enumerate(assertions):
            if not isinstance(assertion, Mapping):
                raise CatalogRecordError(f"$.assertions[{index}] must be an object")
            validate_assertion(assertion, f"$.assertions[{index}]")
    else:
        _validate_capture(record)

    expected = catalog_id_for(record)
    actual = _require_string(record, "record_id", "$.record_id")
    if actual != expected:
        raise CatalogRecordError(
            f"$.record_id {actual!r} does not match the computed identity {expected!r}"
        )


def _validate_capture(record: Mapping[str, Any]) -> None:
    _require_string(record, "snapshot_id", "$.snapshot_id")
    _require_string(record, "capture_method", "$.capture_method")
    source_type = _require_choice(record, "source_type", SOURCE_TYPES, "$.source_type")
    parse_timestamp(record.get("captured_at", ""), "$.captured_at")
    if not isinstance(record.get("capture_success"), bool):
        raise CatalogRecordError("$.capture_success must be a boolean")
    _require_string(record, "capturing_executor", "$.capturing_executor")

    content_digest = _require_string(record, "content_digest", "$.content_digest")
    if not _DIGEST_RE.match(content_digest):
        raise CatalogRecordError("$.content_digest must be sha256:<64 hex>")

    channel = _require_choice(
        record,
        "channel_authentication_status",
        CHANNEL_STATUSES,
        "$.channel_authentication_status",
    )
    content = _require_choice(
        record,
        "content_evidence_status",
        CONTENT_EVIDENCE_STATUSES,
        "$.content_evidence_status",
    )

    # The vocabularies are disjoint, so a value from one can never satisfy
    # the other. Checked explicitly rather than assumed.
    if channel in CONTENT_EVIDENCE_STATUSES or content in CHANNEL_STATUSES:
        raise CatalogRecordError(
            "capture status vocabularies must remain disjoint; "
            "content evidence is not a verification outcome"
        )

    if source_type == SOURCE_PROVIDER_SELF_REPORT and content in FORBIDDEN_FOR_SELF_REPORT:
        raise CatalogRecordError(
            "$.content_evidence_status may not imply independent confirmation for a "
            "provider_self_report capture: authenticating the channel establishes "
            "who said it, not whether it is true (ABS-0004 v5)"
        )


def build_model_identity(
    *, originator_id: str, canonical_name: str, release_identity: str = "unknown"
) -> dict[str, Any]:
    record = {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "record_kind": RECORD_KIND_MODEL_IDENTITY,
        "originator_id": originator_id,
        "canonical_name": canonical_name,
        "release_identity": release_identity,
    }
    record["record_id"] = catalog_id_for(record)
    validate_catalog_record(record)
    return record


def build_endpoint_identity(
    *, operating_organization: str, endpoint_identifier: str
) -> dict[str, Any]:
    record = {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "record_kind": RECORD_KIND_ENDPOINT_IDENTITY,
        "operating_organization": operating_organization,
        "endpoint_identifier": endpoint_identifier,
    }
    record["record_id"] = catalog_id_for(record)
    validate_catalog_record(record)
    return record


def build_assertion(
    *,
    assertion_subject: str,
    assertion_predicate: str,
    assertion_value_or_target: Any,
    valid_from: str,
    source: str,
    unit: str | None = None,
    scope: str | None = None,
    valid_until: str | None = None,
    superseded_by: str | None = None,
) -> dict[str, Any]:
    assertion = {
        "assertion_subject": assertion_subject,
        "assertion_predicate": assertion_predicate,
        "assertion_value_or_target": assertion_value_or_target,
        "unit": unit,
        "scope": scope,
        "valid_from": valid_from,
        "valid_until": valid_until,
        "superseded_by": superseded_by,
        "source": source,
    }
    validate_assertion(assertion, "$.assertion")
    return assertion


def build_snapshot(
    *,
    service_endpoint_id: str,
    observed_at: str,
    assertions: Sequence[Mapping[str, Any]],
    source_set: str,
) -> dict[str, Any]:
    record = {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "record_kind": RECORD_KIND_SNAPSHOT,
        "service_endpoint_id": service_endpoint_id,
        "observed_at": observed_at,
        "source_set_digest": digest_text(source_set),
        "assertions": [dict(a) for a in assertions],
    }
    record["record_id"] = catalog_id_for(record)
    validate_catalog_record(record)
    return record


def build_capture(
    *,
    snapshot_id: str,
    capture_method: str,
    source_type: str,
    captured_at: str,
    capture_success: bool,
    capturing_executor: str,
    payload: str,
    channel_authentication_status: str,
    content_evidence_status: str,
) -> dict[str, Any]:
    """Assemble a capture.

    Both status fields are required arguments with no defaults: neither may
    be derived from the other (warrant condition 3).
    """

    record = {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "record_kind": RECORD_KIND_CAPTURE,
        "snapshot_id": snapshot_id,
        "capture_method": capture_method,
        "source_type": source_type,
        "captured_at": captured_at,
        "capture_success": capture_success,
        "capturing_executor": capturing_executor,
        "content_digest": digest_text(payload),
        "content_evidence_status": content_evidence_status,
        "channel_authentication_status": channel_authentication_status,
    }
    record["record_id"] = catalog_id_for(record)
    validate_catalog_record(record)
    return record
