# Catalog Records (ABS-0004 v5 Slice B)

Admitted by WARR-20260723-0001 under GAP-0005 (PLAN-20260723-0001).

Representation only. Nothing gates a decision on a resolution result: C2
catalog admission is not activated, no role qualification consults these
records, and no independence assessment reads them. This slice makes
provider identity claims representable and datable, nothing more.

## The record family

- **ModelIdentity** (`MID-`): stable identity of a model release —
  `originator_id`, `canonical_name`, `release_identity`.
- **ServiceEndpointIdentity** (`EID-`): the API surface — operating
  organization and endpoint identifier. Mutable endpoint properties
  (region, jurisdiction, retention) belong in assertions, not here.
- **CatalogAssertion**: exactly one atomic claim. A record carrying two
  claims, or a compound value, is rejected by the validator.
- **CatalogSnapshot** (`SNAP-`): a set of assertions observed together at
  `observed_at`, from a digested source set.
- **CatalogCapture** (`CAP-`): how and when a snapshot was obtained.
- **IdentityResolution** (`RES-`): an append-only annotation binding one
  invocation to one resolved identity, or recording why it did not
  resolve.

Records live under `docs/catalog/<kind>/` and `docs/catalog/resolutions/`,
at paths derived from their identities.

## Evidence classing, and its limits

A capture carries two status fields that are independent by construction:

| field | vocabulary | what it means |
| --- | --- | --- |
| `content_evidence_status` | `self_asserted`, `independently_corroborated`, `contradicted`, `unassessed` | what was established about the truth of the claim |
| `channel_authentication_status` | `verified_current`, `stale`, `unverifiable` | what was independently established about the channel the claim arrived through |

The two vocabularies are disjoint sets, checked at import. A value from one
can never be silently accepted in the other, so neither field can be
defaulted from or derived from the other.

A capture whose `source_type` is `provider_self_report` may never carry
`independently_corroborated`, no matter how well the channel authenticated.
Authenticating the channel establishes **who said it**, not **whether it is
true**. In practice this means: every catalog claim AI-Lab can currently
obtain is `self_asserted`, and every identity resolved from one inherits
that class.

### The adjacency mitigation, stated honestly

Canonical serialization places `content_evidence_status` immediately before
`channel_authentication_status`, always, so that a strong channel status
cannot be displayed without the weak content status directly above it.

**This is a mitigation, not a control.** Both COMP-0036 reviewers
independently constructed the same attack: a dashboard or summary that
shows `channel_authentication_status: verified_current` next to a resolved
identity, while omitting or burying the content status, conveys false
confidence while every record involved is perfectly valid. Field ordering
does not stop a renderer from reordering, filtering, or relabelling. A
rendering rule is deferred until consumers exist; until then, the defense
is this paragraph and the reviewer who reads it.

## Resolution

`resolve_identity` is pure: it reads only its arguments, performs no I/O,
and consults no clock. The resolution timestamp is supplied by the caller.

An invocation resolves only when an assertion binds its endpoint and
requested name at its occurrence instant, unambiguously, from a snapshot
observed no later than the invocation and no older than the freshness
window. Otherwise the outcome is one of five enumerated reasons, never a
silent default:

- `no_applicable_assertion`
- `snapshot_after_invocation`
- `ambiguous_assertions` — more than one target; ambiguity blocks rather
  than picking a winner
- `expired_freshness_window`
- `contradicted_evidence` — the backing capture is `contradicted`. The
  resolver declines to act rather than proceeding mechanically. Declining
  is not an admissibility judgment; admissibility belongs to Slice D.

### Non-resolution is not invalidity

`no_applicable_assertion` means the requested name is **not in the listing**.
It does not mean the name is invalid, unsupported, or wrong.

This is not a theoretical caveat. The first live capture (2026-07-23)
established it directly: AI-Lab's own configured default at the time,
`claude-sonnet-4-5`, does not appear in the provider's models listing, which
carries `claude-sonnet-4-5-20250929` instead. Every AI-Lab call using the
bare alias had been succeeding. So the endpoint accepts names the listing
does not enumerate, and a listing is therefore a partial account of an
endpoint's accepted names, not a complete one.

Consequences that must not be lost:

- A reader may not infer from `no_applicable_assertion` that a model does
  not exist or that a call would fail. The only supported inference is that
  the catalog, as captured, does not carry an assertion binding that name.
- Any future consumer that gates on resolution (C2 catalog admission is the
  obvious candidate, and is deferred) would have blocked AI-Lab's own
  working configuration. A gate keyed on catalog presence must therefore
  treat absence as a prompt for review, never as a refusal, unless and
  until a source that enumerates aliases is admitted.
- The same reasoning applies to third-party catalog claims about aliases.
  ADVISOR-0000 asserted that a `gpt-5.6` alias routes to a specific model;
  that alias is absent from the captured listing, and by the rule above its
  absence is not evidence against the claim. It remains unverifiable.

### Freshness window

Default **thirty days**, configurable per call. A snapshot older than the
window relative to the invocation does not resolve it. The window is a
judgment about how fast provider aliases drift, not a measurement; it is
declared here so that it can be argued with rather than discovered in
code.

### Timestamps

All timestamps are ISO 8601 with an explicit offset, normalized to UTC
before comparison, compared at microsecond precision. The precedence check
is **inclusive**: a snapshot observed at exactly the invocation's instant
resolves it, on the reasoning that an observation at instant T did witness
the state at T. One microsecond later does not.

## Append-only, always

Resolution never mutates a captured InvocationRecord. The invocation's
`identity_verification_status` remains `unresolved` in its own file
forever; the resolution lives beside it as a separate annotation
referencing it by id.

**Consumers must join the two.** A reader who examines only the
InvocationRecord will see `unresolved` and conclude no identity was ever
established, which is materially misleading once an annotation exists —
this failure mode was named by a COMP-0036 reviewer and is recorded here
because the design accepts it deliberately: the alternative, rewriting
captured records, would make provenance mutable, which is worse.

Superseded resolutions are recorded, never retroactively applied. If a
later catalog shows a different mapping, that is a new annotation; the
earlier one stands as what was believed on the evidence available then.

## Capture: opt-in live, fixture replay by default

`ai_lab/providers/catalog_capture.py` provides both paths through one
parsing function, so the offline tests exercise the same code the live
path uses.

- **Fixture replay** is the default and needs no network and no opt-in.
  Recorded payloads live under `tests/fixtures/catalog/`, each carrying a
  `recorded_at` date and a `provenance` statement. A snapshot built from a
  fixture takes its `observed_at` from the recording date, never from the
  current time, so a stale fixture correctly fails the freshness window
  instead of silently passing.
- **Live fetch** requires `AI_LAB_ENABLE_LIVE_CATALOG=1`. Attempting it
  while disabled raises rather than falling back. The transport is
  injected as a callable, so no HTTP client is embedded here.

Every capture from either path is `provider_self_report` /
`self_asserted`, and `channel_authentication_status` is recorded as
`unverifiable`: this slice does not inspect certificate chains or key
digests, so nothing has been independently established about the channel.
Recording a stronger channel status without performing the check would be
the overclaim P6 forbids.

## Known limitations

- Every obtainable catalog claim is currently `self_asserted`. AI-Lab has
  no independent source against which to corroborate a provider's account
  of its own catalog.
- A provider that silently substitutes a model without updating its
  catalog is undetectable from catalog evidence alone. Resolution records
  what the catalog said, not what the provider did.
- Channel authentication is representable but not yet performed: no TLS
  chain or key digest is recorded, so every capture reads `unverifiable`
  on that axis.
- No consumer reads these records. Resolution results gate nothing.
- Recorded fixtures are only as faithful as the recording. The original
  fixtures carried a `context_window` field that no live response returns,
  which made the suite exercise a branch live capture could not reach.
  Corrected on 2026-07-23; the lesson is that a fixture asserts a shape, and
  an unverified shape is a claim like any other.
- Context limits are not captured. Neither provider's models listing carries
  one, so AI-Lab records no claim about context windows rather than a claim
  it cannot obtain. This is a gap in the source, not in the schema.
