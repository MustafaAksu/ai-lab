"""Invocation provenance capture (ABS-0004 Slice A).

Schema v1 for InvocationRecord, its minimal EffectiveInputManifest, and its
ExecutionProfile, with a validator, deterministic canonical serialization,
deterministic identity and path rules, and GraphRelation-shaped relations.

Admitted by WARR-20260722-0001 under GAP-0005 (PLAN-20260722-0001), subject
to eight binding conditions recorded in that warrant.

Capture only. This module reads nothing, enforces no constraint, and gates
no decision: no routing, no catalog resolution, no roles or authorization,
no lineage or admission. Emission is restricted to the single admitted
capture path; see CAPTURE_PATHS.

Field names and semantics follow ABS-0004 v4 exactly. Deviations require an
ABS revision first (plan constraint 4).

Identity and schema versioning (warrant condition 4)
----------------------------------------------------
Record identity is a version-scoped digest over an explicitly enumerated
subset of fields, IDENTITY_FIELDS_V1, not over the whole record. Later
slices may add fields (catalog resolution, roles, authorization, lineage)
without changing the identity of any record already emitted, because those
fields are not in the enumerated subset. If a future slice needs an
identity-bearing field, it must introduce a new schema version with its own
enumerated subset; identities never migrate silently across versions. The
schema version is part of the digest input, so identical content under two
schema versions yields two distinct identities by construction.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


INVOCATION_SCHEMA_VERSION = "v1"

# The single path admitted for capture by WARR-20260722-0001. Emission from
# any other path is a scope violation, not a configuration choice: condition
# 1 requires that scripts/ask_provider.py invoked directly emits nothing.
CAPTURE_PATH_COMPARE_PROVIDERS = "scripts/compare_providers.py"
CAPTURE_PATHS = frozenset({CAPTURE_PATH_COMPARE_PROVIDERS})

INVOCATION_DIR = "docs/invocations"

EXECUTOR_KIND_MODEL = "model"
EXECUTOR_KIND_TOOL = "tool"
EXECUTOR_KIND_HUMAN = "human"
EXECUTOR_KINDS = frozenset(
    {EXECUTOR_KIND_MODEL, EXECUTOR_KIND_TOOL, EXECUTOR_KIND_HUMAN}
)

# ABS-0004 4.3: an invocation records the most precise identity establishable
# at execution time; unresolved requested names are recorded as unresolved,
# never silently substituted. Slice A performs no resolution (Slice B does),
# so every model executor is recorded unresolved.
IDENTITY_UNRESOLVED = "unresolved"
IDENTITY_VERIFIED = "verified"
IDENTITY_VERIFICATION_STATUSES = frozenset(
    {IDENTITY_UNRESOLVED, IDENTITY_VERIFIED}
)

# ABS-0004 4.14 session state modes.
SESSION_STATELESS = "stateless"
SESSION_EXPLICIT_REPLAYED = "explicit_replayed_context"
SESSION_PROVIDER_MANAGED = "provider_managed_state"
SESSION_LOCAL_MANAGED = "local_managed_state"
SESSION_HYBRID = "hybrid_state"
SESSION_UNKNOWN = "unknown_state"
SESSION_STATE_MODES = frozenset(
    {
        SESSION_STATELESS,
        SESSION_EXPLICIT_REPLAYED,
        SESSION_PROVIDER_MANAGED,
        SESSION_LOCAL_MANAGED,
        SESSION_HYBRID,
        SESSION_UNKNOWN,
    }
)

# ABS-0004 Slice A: the marker defaults to experimental until an admission
# consumer exists. No consumer exists in this slice.
MARKER_EXPERIMENTAL = "experimental"
MARKER_GOVERNED = "governed"
GOVERNANCE_MARKERS = frozenset({MARKER_EXPERIMENTAL, MARKER_GOVERNED})

STATUS_SUCCESS = "success"
STATUS_FAILURE = "failure"
INVOCATION_STATUSES = frozenset({STATUS_SUCCESS, STATUS_FAILURE})

# Completeness attestation (ABS-0004 4.12): whether the manifest is declared
# exhaustive for all effective-input channels. Blind-witness qualification
# requires an affirmative attestation; Slice A captures the field and makes
# no eligibility decision.
ATTESTATION_COMPLETE = "complete_for_all_effective_inputs"
ATTESTATION_PARTIAL = "partial_declared_channels_only"
ATTESTATION_UNKNOWN = "unknown"
COMPLETENESS_ATTESTATIONS = frozenset(
    {ATTESTATION_COMPLETE, ATTESTATION_PARTIAL, ATTESTATION_UNKNOWN}
)

MANIFEST_FIELDS = (
    "rendered_prompt_digest",
    "system_instruction_digest",
    "developer_instruction_digest",
    "context_manifest_reference",
    "tool_schema_digest",
    "prior_tool_result_references",
    "session_state_mode",
    "completeness_attestation",
)

PROFILE_FIELDS = (
    "service_endpoint",
    "requested_model_name",
    "output_token_limit",
    "sampling_parameters",
    "reasoning_parameters",
    "provider_request_flags",
    "runtime_version",
)

# Warrant condition 4: the enumerated identity subset for schema v1.
IDENTITY_FIELDS_V1 = (
    "schema_version",
    "capture_path",
    "executor.kind",
    "executor.reference",
    "requested_model_name",
    "service_endpoint",
    "session_id",
    "effective_input_manifest.rendered_prompt_digest",
    "occurred_at",
)

# ABS-0004 Section 5 Slice A predicates. No predicate outside this list may
# be introduced by this slice (warrant condition 8).
SLICE_A_PREDICATES = (
    "produced_by",
    "executed_by",
    "requested_via",
    "used_execution_profile",
    "used_inputs",
    "member_of",
    "spawned",
)

_ID_RE = re.compile(r"^INV-[0-9a-f]{16}$")
_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class InvocationRecordError(ValueError):
    """Raised when a record violates the Slice A schema."""


def digest_text(text: str) -> str:
    """Content-addressed digest used for prompts and instruction envelopes."""

    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_invocation_json(record: Mapping[str, Any]) -> str:
    """Deterministic serialization: sorted keys, two-space indent, LF.

    Byte-stable for semantically identical records; matches the sidecar
    contract's canonical-JSON precedent (plan mitigation).
    """

    return json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _identity_value(record: Mapping[str, Any], dotted: str) -> str:
    node: Any = record
    for part in dotted.split("."):
        if not isinstance(node, Mapping) or part not in node:
            raise InvocationRecordError(
                f"identity field {dotted} is missing; identity is undefined"
            )
        node = node[part]
    if node is None:
        raise InvocationRecordError(f"identity field {dotted} must not be null")
    return str(node)


def invocation_id_for(record: Mapping[str, Any]) -> str:
    """Deterministic identity over IDENTITY_FIELDS_V1 only.

    Fields outside the enumerated subset, including every field a later
    slice may add, do not participate. See the module docstring for the
    schema-versioning rule (warrant condition 4).
    """

    payload = "\u001f".join(
        f"{name}={_identity_value(record, name)}" for name in IDENTITY_FIELDS_V1
    )
    return "INV-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def invocation_relative_path(invocation_id: str) -> str:
    """Deterministic path for a record."""

    if not _ID_RE.match(invocation_id):
        raise InvocationRecordError(f"malformed invocation id: {invocation_id!r}")
    return f"{INVOCATION_DIR}/{invocation_id}.json"


def _require_string(record: Mapping[str, Any], key: str, path: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise InvocationRecordError(f"{path} must be a non-empty string")
    return value


def _require_choice(
    record: Mapping[str, Any], key: str, allowed: frozenset[str], path: str
) -> str:
    value = _require_string(record, key, path)
    if value not in allowed:
        raise InvocationRecordError(
            f"{path} must be one of {sorted(allowed)}; got {value!r}"
        )
    return value


def _require_mapping(record: Mapping[str, Any], key: str, path: str) -> Mapping[str, Any]:
    value = record.get(key)
    if not isinstance(value, Mapping):
        raise InvocationRecordError(f"{path} must be an object")
    return value


def _validate_manifest(manifest: Mapping[str, Any]) -> None:
    path = "$.effective_input_manifest"

    for field in MANIFEST_FIELDS:
        if field not in manifest:
            raise InvocationRecordError(f"{path}.{field} is required (may be null)")

    unexpected = set(manifest) - set(MANIFEST_FIELDS)
    if unexpected:
        raise InvocationRecordError(
            f"{path} has unknown fields: {sorted(unexpected)}; "
            "Slice A field names follow ABS-0004 v4 exactly"
        )

    rendered = _require_string(manifest, "rendered_prompt_digest", f"{path}.rendered_prompt_digest")
    if not _DIGEST_RE.match(rendered):
        raise InvocationRecordError(
            f"{path}.rendered_prompt_digest must be sha256:<64 hex>"
        )

    for optional_digest in ("system_instruction_digest", "developer_instruction_digest", "tool_schema_digest"):
        value = manifest[optional_digest]
        if value is not None and not (isinstance(value, str) and _DIGEST_RE.match(value)):
            raise InvocationRecordError(
                f"{path}.{optional_digest} must be null or sha256:<64 hex>"
            )

    reference = manifest["context_manifest_reference"]
    if reference is not None and not (isinstance(reference, str) and reference.strip()):
        raise InvocationRecordError(
            f"{path}.context_manifest_reference must be null or a non-empty string"
        )

    prior = manifest["prior_tool_result_references"]
    if not isinstance(prior, list) or any(
        not isinstance(item, str) or not item.strip() for item in prior
    ):
        raise InvocationRecordError(
            f"{path}.prior_tool_result_references must be a list of non-empty strings"
        )

    _require_choice(
        manifest, "session_state_mode", SESSION_STATE_MODES, f"{path}.session_state_mode"
    )
    _require_choice(
        manifest,
        "completeness_attestation",
        COMPLETENESS_ATTESTATIONS,
        f"{path}.completeness_attestation",
    )


def _validate_profile(profile: Mapping[str, Any]) -> None:
    path = "$.execution_profile"

    for field in PROFILE_FIELDS:
        if field not in profile:
            raise InvocationRecordError(f"{path}.{field} is required (may be null)")

    unexpected = set(profile) - set(PROFILE_FIELDS)
    if unexpected:
        raise InvocationRecordError(
            f"{path} has unknown fields: {sorted(unexpected)}; "
            "Slice A field names follow ABS-0004 v4 exactly"
        )

    _require_string(profile, "service_endpoint", f"{path}.service_endpoint")
    _require_string(profile, "requested_model_name", f"{path}.requested_model_name")

    limit = profile["output_token_limit"]
    if limit is not None and not (isinstance(limit, int) and not isinstance(limit, bool) and limit > 0):
        raise InvocationRecordError(
            f"{path}.output_token_limit must be null or a positive integer"
        )

    for mapping_field in ("sampling_parameters", "reasoning_parameters", "provider_request_flags"):
        value = profile[mapping_field]
        if not isinstance(value, Mapping):
            raise InvocationRecordError(f"{path}.{mapping_field} must be an object")

    runtime = profile["runtime_version"]
    if runtime is not None and not (isinstance(runtime, str) and runtime.strip()):
        raise InvocationRecordError(
            f"{path}.runtime_version must be null or a non-empty string"
        )


def validate_invocation_record(record: Mapping[str, Any]) -> None:
    """Schema validity for a Slice A InvocationRecord.

    Raises InvocationRecordError on violation. This is the acceptance gate
    for every emitted record (plan mitigation).
    """

    if not isinstance(record, Mapping):
        raise InvocationRecordError("$ must be an object")

    version = _require_string(record, "schema_version", "$.schema_version")
    if version != INVOCATION_SCHEMA_VERSION:
        raise InvocationRecordError(
            f"$.schema_version must be {INVOCATION_SCHEMA_VERSION!r}; got {version!r}"
        )

    capture_path = _require_string(record, "capture_path", "$.capture_path")
    if capture_path not in CAPTURE_PATHS:
        raise InvocationRecordError(
            f"$.capture_path {capture_path!r} is outside the admitted capture "
            f"paths {sorted(CAPTURE_PATHS)} (WARR-20260722-0001 condition 1)"
        )

    executor = _require_mapping(record, "executor", "$.executor")
    _require_choice(executor, "kind", EXECUTOR_KINDS, "$.executor.kind")
    _require_string(executor, "reference", "$.executor.reference")
    _require_choice(
        executor,
        "identity_verification_status",
        IDENTITY_VERIFICATION_STATUSES,
        "$.executor.identity_verification_status",
    )
    unexpected_executor = set(executor) - {"kind", "reference", "identity_verification_status"}
    if unexpected_executor:
        raise InvocationRecordError(
            f"$.executor has unknown fields: {sorted(unexpected_executor)}"
        )

    _require_string(record, "requested_model_name", "$.requested_model_name")
    _require_string(record, "service_endpoint", "$.service_endpoint")

    # Condition 7: session identity must be present in every record, not
    # mode alone. Mode lives on the manifest; identity lives here.
    _require_string(record, "session_id", "$.session_id")

    _require_string(record, "occurred_at", "$.occurred_at")
    _require_choice(record, "status", INVOCATION_STATUSES, "$.status")
    _require_choice(
        record, "governance_marker", GOVERNANCE_MARKERS, "$.governance_marker"
    )

    spawned = record.get("spawned")
    if not isinstance(spawned, list) or any(
        not isinstance(item, str) or not _ID_RE.match(item) for item in spawned
    ):
        raise InvocationRecordError(
            "$.spawned must be a list of invocation ids (may be empty)"
        )

    _validate_manifest(_require_mapping(record, "effective_input_manifest", "$.effective_input_manifest"))
    _validate_profile(_require_mapping(record, "execution_profile", "$.execution_profile"))

    expected_id = invocation_id_for(record)
    actual_id = _require_string(record, "invocation_id", "$.invocation_id")
    if actual_id != expected_id:
        raise InvocationRecordError(
            f"$.invocation_id {actual_id!r} does not match the identity computed "
            f"from {list(IDENTITY_FIELDS_V1)}: {expected_id!r}"
        )


def build_invocation_record(
    *,
    capture_path: str,
    executor_kind: str,
    executor_reference: str,
    identity_verification_status: str,
    requested_model_name: str,
    service_endpoint: str,
    session_id: str,
    occurred_at: str,
    rendered_prompt: str,
    session_state_mode: str,
    completeness_attestation: str,
    status: str,
    output_token_limit: int | None = None,
    sampling_parameters: Mapping[str, Any] | None = None,
    reasoning_parameters: Mapping[str, Any] | None = None,
    provider_request_flags: Mapping[str, Any] | None = None,
    runtime_version: str | None = None,
    system_instruction: str | None = None,
    developer_instruction: str | None = None,
    tool_schema: str | None = None,
    context_manifest_reference: str | None = None,
    prior_tool_result_references: Sequence[str] | None = None,
    spawned: Sequence[str] | None = None,
    governance_marker: str = MARKER_EXPERIMENTAL,
) -> dict[str, Any]:
    """Assemble and validate a Slice A record. Returns the record."""

    record: dict[str, Any] = {
        "schema_version": INVOCATION_SCHEMA_VERSION,
        "capture_path": capture_path,
        "executor": {
            "kind": executor_kind,
            "reference": executor_reference,
            "identity_verification_status": identity_verification_status,
        },
        "requested_model_name": requested_model_name,
        "service_endpoint": service_endpoint,
        "session_id": session_id,
        "occurred_at": occurred_at,
        "status": status,
        "governance_marker": governance_marker,
        "spawned": list(spawned or []),
        "effective_input_manifest": {
            "rendered_prompt_digest": digest_text(rendered_prompt),
            "system_instruction_digest": (
                digest_text(system_instruction) if system_instruction is not None else None
            ),
            "developer_instruction_digest": (
                digest_text(developer_instruction) if developer_instruction is not None else None
            ),
            "context_manifest_reference": context_manifest_reference,
            "tool_schema_digest": (
                digest_text(tool_schema) if tool_schema is not None else None
            ),
            "prior_tool_result_references": list(prior_tool_result_references or []),
            "session_state_mode": session_state_mode,
            "completeness_attestation": completeness_attestation,
        },
        "execution_profile": {
            "service_endpoint": service_endpoint,
            "requested_model_name": requested_model_name,
            "output_token_limit": output_token_limit,
            "sampling_parameters": dict(sampling_parameters or {}),
            "reasoning_parameters": dict(reasoning_parameters or {}),
            "provider_request_flags": dict(provider_request_flags or {}),
            "runtime_version": runtime_version,
        },
    }

    record["invocation_id"] = invocation_id_for(record)
    validate_invocation_record(record)
    return record


def invocation_relations(record: Mapping[str, Any], produced_artifact_id: str | None = None):
    """Slice A relations in GraphRelation shape.

    Returns GraphRelation instances only; no parallel edge vocabulary
    (plan constraint 2, warrant condition 7).
    """

    from ai_lab.documentation.graph_neighborhood import GraphRelation

    validate_invocation_record(record)
    invocation_id = record["invocation_id"]
    relations: list[GraphRelation] = []

    def relate(source_id: str, predicate: str, target_id: str, evidence: str) -> None:
        if predicate not in SLICE_A_PREDICATES:
            raise InvocationRecordError(
                f"predicate {predicate!r} is outside the Slice A list "
                f"{list(SLICE_A_PREDICATES)} (WARR-20260722-0001 condition 8)"
            )
        relations.append(
            GraphRelation(
                source_id=source_id,
                predicate=predicate,
                target_id=target_id,
                relation_source="future_edge_seed",
                authoritative=False,
                scope="invocation_provenance_slice_a",
                evidence=evidence,
            )
        )

    path = invocation_relative_path(invocation_id)

    if produced_artifact_id:
        relate(produced_artifact_id, "produced_by", invocation_id, path)

    relate(invocation_id, "executed_by", record["executor"]["reference"], path)
    relate(invocation_id, "requested_via", record["service_endpoint"], path)
    relate(invocation_id, "used_execution_profile", f"{invocation_id}::execution_profile", path)
    relate(invocation_id, "used_inputs", f"{invocation_id}::effective_input_manifest", path)
    relate(invocation_id, "member_of", record["session_id"], path)

    for child in record["spawned"]:
        relate(invocation_id, "spawned", child, path)

    return tuple(relations)


def write_invocation_record(record: Mapping[str, Any], repo_root: Path) -> Path:
    """Validate and write a record to its deterministic path.

    Raises InvocationRecordError on schema violation and OSError on write
    failure. Callers on the capture path must report failures without
    aborting the underlying provider call (plan constraint 3, warrant
    condition 3).
    """

    validate_invocation_record(record)
    target = repo_root / invocation_relative_path(record["invocation_id"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(canonical_invocation_json(record), encoding="utf-8")
    return target
