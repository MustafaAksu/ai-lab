# Compact Artifact Sidecar Contract

Admitted by WARR-20260717-0001 under GAP-0002 (PLAN-20260717-0001).
Implemented in `ai_lab/documentation/artifact_sidecar.py`. Contract only:
no generation, no bulk processing, no context-selection integration.

## Principles

Canonical human-readable artifacts remain the sole authoritative source.
Sidecars are explicitly derived, versioned, provenance-bearing, and
regenerable. No sidecar may claim semantic completeness without fidelity
evidence.

## Identity, path, serialization

- Identity: `<source_artifact_id>::<profile>`.
- Path: `docs/sidecars/<source_artifact_id>.<profile>.json`.
- Serialization: canonical JSON with sorted keys, two-space indent,
  UTF-8, trailing newline. Regenerating an unchanged sidecar must be
  byte-identical.

## Profiles

- `rich_immediate` (token hypothesis 250-500): all thirteen semantic
  fields required; `omitted_fields` must be empty.
- `concise_second_level` (token hypothesis 80-200): semantic fields may
  be omitted, but every omitted field must be listed in
  `omitted_fields`. A field is never both present and omitted, and never
  silently absent.

Token ranges are validation hypotheses (WARR-20260717-0001), estimated
with `whitespace_word_count_v1`. Non-compliance is a reported finding
(`SIDECAR_OVER_TOKEN_HYPOTHESIS` warn, `SIDECAR_UNDER_TOKEN_HYPOTHESIS`
info), never a schema failure.

## Fields

Provenance (required in both profiles): `sidecar_id`, `schema_version`,
`profile`, `source_artifact_id`, `source_path`, `source_content_hash`
(sha256 of the source bytes), `source_repo_commit` (full hash),
`generator` (structured: `provider`, `identity`, `version`),
`generated_at`, `omitted_fields`, optional `superseded_by`, optional
`fidelity_category`.

Semantic (thirteen): `purpose`, `status`, `key_claims`, `decisions`,
`results`, `constraints`, `risks`, `dependencies`, `evidence_refs`,
`uncertainty`, `unresolved`, `next_actions`, `lineage`.

The structured `generator` field records who or what produced the
sidecar (for example `deterministic/fixture-writer/v1` or a future
`model/<model-id>/<prompt-version>`), making generation provenance
queryable before any model-generation slice exists.

## Validation categories

1. Schema validity and provenance validity: `validate_sidecar_record`
   raises `SidecarError`.
2. Profile compliance: `assess_profile_compliance` returns findings.
3. Staleness: `assess_staleness` returns the shared three-valued
   `verification_outcome` (GAP-0004 vocabulary): source hash match is
   `verified_current`; hash mismatch is `stale` (drift, error); missing
   or unreadable source is `unverifiable` (evidence unavailable, warn).
   The `ok` field is boolean and fail-closed.
4. Semantic fidelity: `fidelity_category` takes `faithful`,
   `omissive_but_flagged`, `distorted`, or `unassessed` (default).
   Assessing fidelity is a later governed slice; this contract only
   carries the evidence field.

## Staleness, regeneration, supersession, deletion

A `stale` sidecar must be regenerated from the current source,
superseded (`superseded_by` pointing at the replacement sidecar id), or
deleted. An `unverifiable` sidecar makes no drift claim and must not be
treated as current. Deleting a canonical artifact orphans its sidecars;
orphaned sidecars must be deleted or marked superseded.

## Later separately governed slices

Explicitly out of scope here and requiring their own plans and
admissions: sidecar generation (deterministic or model-produced), bulk
or corpus-wide generation, fidelity evaluation, graph-packing and
context-selection integration, provider exposure, persistence or index
integration.
