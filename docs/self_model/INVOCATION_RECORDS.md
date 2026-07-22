# Invocation Provenance Records (ABS-0004 Slice A)

Admitted by WARR-20260722-0001 under GAP-0005 (PLAN-20260722-0001).

Capture only. Nothing reads these records: no routing, no catalog
resolution, no roles or authorization, no lineage or admission enforcement.
Activation of the ABS-0004 C1 `provenance_v1` profile is a later decision.

## What is captured, and where

One `InvocationRecord` per provider call on `scripts/compare_providers.py`,
written to `docs/invocations/<invocation_id>.json` in canonical JSON
(sorted keys, two-space indent, trailing newline), matching the sidecar
contract's serialization precedent.

`scripts/ask_provider.py` emits nothing. The restriction is enforced twice:
the script does not import the capture module, and `capture_path` is a
validated field whose only admitted value is `scripts/compare_providers.py`,
so a record claiming another origin is rejected by the validator.

## Record shape (schema v1)

Top level: `schema_version`, `invocation_id`, `capture_path`, `executor`
(`kind`, `reference`, `identity_verification_status`),
`requested_model_name`, `service_endpoint`, `session_id`, `occurred_at`,
`status`, `governance_marker`, `spawned`, `effective_input_manifest`,
`execution_profile`.

`effective_input_manifest`: `rendered_prompt_digest`,
`system_instruction_digest`, `developer_instruction_digest`,
`context_manifest_reference`, `tool_schema_digest`,
`prior_tool_result_references`, `session_state_mode`,
`completeness_attestation`.

`execution_profile`: `service_endpoint`, `requested_model_name`,
`output_token_limit`, `sampling_parameters`, `reasoning_parameters`,
`provider_request_flags`, `runtime_version`.

Field names and semantics follow ABS-0004 v4 exactly; deviations require an
ABS revision first.

## Identity and schema versioning

Identity is a digest over an explicitly enumerated subset,
`IDENTITY_FIELDS_V1`: schema version, capture path, executor kind and
reference, requested model name, service endpoint, session identity,
rendered-prompt digest, and timestamp. Everything else is outside the
subset.

Consequence for later slices: fields added by Slice B (resolved model
identity, catalog references), Slice C (roles, authorization), or Slice D
(lineage, admission status) do not change the identity of any record
already emitted, because they are not enumerated. A future slice needing an
identity-bearing field must introduce a new schema version with its own
enumerated subset. Schema version participates in the digest, so identical
content under two versions yields two distinct identities and identities
never migrate silently.

## Honest limitations

- `completeness_attestation` is `partial_declared_channels_only` on this
  path. The manifest is not declared exhaustive for all effective-input
  channels, so no record captured here qualifies as blind-witness evidence.
  Slice A makes no eligibility decision; it records the attestation.
- `identity_verification_status` is `unresolved` for every model executor.
  Slice A performs no resolution; the requested name is recorded as
  requested and never silently substituted for a resolved identity.
- `governance_marker` defaults to `experimental` and stays there until an
  admission consumer exists.
- Relations are emitted with `authoritative: false` and
  `relation_source: future_edge_seed`. They are diagnostic seeds, not
  authoritative graph edges.
- Session state mode is observed for this path (`stateless`, or
  `explicit_replayed_context` when a context pack is attached), not assumed.
  Per-provider session-mode cataloging remains deferred.
- Records are prospective only. Invocations made before this capability
  shipped have no records and fall under the ABS-0004 Section 7
  pre-provenance boundary.

## Deferred fields

Fields defined in ABS-0004 but not captured here, with their slice:
resolved model identity, catalog snapshot and assertion references, and
endpoint assertions (Slice B); assigned role, qualification reference,
consequence class, and authorization reference (Slice C); claim-level
ancestry, independence assessment, and admission status (Slice D). Run and
ProtocolRound objects remain deferred entirely; session identity is a field
on the record, not a structured object.

## Capture failure

Capture never breaks a provider call. A failure to build or write a record
is reported to standard error and the call returns its result. Silent
swallowing is prohibited, and so is aborting the call.
