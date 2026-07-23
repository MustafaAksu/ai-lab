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

## Known limitations

- Every obtainable catalog claim is currently `self_asserted`. AI-Lab has
  no independent source against which to corroborate a provider's account
  of its own catalog.
- A provider that silently substitutes a model without updating its
  catalog is undetectable from catalog evidence alone. Resolution records
  what the catalog said, not what the provider did.
- Channel authentication is representable but not yet performed: the live
  capture path is opt-in and disabled by default, and no TLS chain or key
  digest is currently recorded.
- No consumer reads these records. Resolution results gate nothing.
