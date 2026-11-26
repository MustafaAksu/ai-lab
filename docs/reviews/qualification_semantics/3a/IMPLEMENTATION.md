# Step 3A implementation contract

[ALG] This document describes the implementation admitted by
[WARR-20261126-0001](../../../self_model/warrants/WARR-20261126-0001.json),
subject to [A1–A4](ADMISSION-AND-CONDITIONS.md). It is implementation
documentation, not a completion decision or execution report.

The governing inputs are the retained [r2 contract](../EQUIVALENCE-EVIDENCE-CONTRACT-DRAFT.md),
[schema](../r2/ASSESSMENT-SCHEMA.json), [deterministic rules](../r2/DETERMINISTIC-RULES.md)
and [consumer matrix](../r2/CONSUMER-COMPATIBILITY.md). A1–A4 restrict that
whole-program proposal to 3A: model/source evaluation, synthetic model witnesses
and immediate legacy refusal. The r2 files retain their historical proposal
wording. Their tool/human and C3 shapes do not imply implementation admission.

## 1. Components and entry points

| Component | Implemented responsibility |
| --- | --- |
| [qualification_records.py](../../../../ai_lab/providers/qualification_records.py) | Strict JSON/schema/reference checks, real Git inventory loading, immutable synthetic anchor and separate assessment persistence |
| [qualification.py](../../../../ai_lab/providers/qualification.py) | Model applicability, complete source aggregation, exact synthetic witness conditions and deterministic result construction |
| [catalog_resolution.py](../../../../ai_lab/providers/catalog_resolution.py) | Non-positive legacy resolution adapter; historical v1 codecs, graph and storage boundary |
| [executor_equivalence.py](../../../../ai_lab/providers/executor_equivalence.py) | Checked diagnostic relation projection; unconditional `blocks_adjudication=True` |
| [qualification_fixtures.py](../../../../tests/qualification_fixtures.py) | Fictional evidence with actual temporary Git commits, trees, blobs and retained bytes |

```python
anchor = load_synthetic_anchor(
    fixture_repo, context_ref=reviewed_context_ref, artifacts=retained_bytes
)
result = evaluate_synthetic_r2(query_bytes, anchor=anchor)
```

The harness chooses `reviewed_context_ref` and `retained_bytes` outside Query.
Query must name that exact context and its retained subjects. It cannot select
another commit, policy, cutoff, source subset, fixture or trust domain. The
factory establishes fixture integrity; it is not a security boundary against
arbitrary Python code or authority to configure a live consumer.

`evaluate_production_r2(query, anchor=None)` returns a typed refusal: no
production anchor is installed. Supplying a synthetic anchor to that entry
point fails domain separation. Production acceptance profiles for endpoint
binding, model witnesses, availability, tool binding, human binding and ancestry
remain empty; Query cannot register one.

## 2. Retained bytes and the source universe

[ALG] The anchor loader verifies the full commit identity and root tree using
Git, enumerates tracked paths, reads regular-file blobs and verifies their Git
hashes. Inventory entries must equal the independently enumerated complete set
under these roots:

- `docs/catalog/eid/`
- `docs/catalog/mid/`
- `docs/catalog/snap/`
- `docs/catalog/cap/`
- `docs/catalog/payloads/`

Catalog symlinks/submodules, missing entries, false tree pins and untracked
catalog substitutions refuse. Auxiliary context/fixture evidence may be supplied
outside Git, but cannot replace pinned path bytes or shadow nonregular tracked
paths. A non-null `git_blob_sha1` requires both the correct blob hash and its
path membership in the pinned commit. All regular-file and auxiliary bytes are
frozen before evaluation; the model evaluator performs no clock or filesystem
lookup.

`RecordRef` binds an actual declared identity and full retained-byte SHA-256.
`ArtifactRef` additionally binds its path and optional Git blob. Exact duplicate
bytes are idempotent; equal IDs with different bytes refuse. Catalog and
invocation v1 identities are recomputed using their existing identity rules;
those subset-field identities do not replace the full-byte digest.

The engine derives sources from every pinned capture, including failed and
contradicted captures. Each source's snapshot, endpoint, payload and decoded
model targets are checked against its supplied row. `model_sources` and
`selected_source_ids` cannot omit an unfavorable capture or target. A retained
snapshot without a capture linkage refuses instead of disappearing.

Inventory declarations also participate. Their retained bodies must equal the
inline declaration excluding its own reference; context declaration references
must equal the pinned inventory's references. `known_at` is compared with the
fixed knowledge cutoff. Missing scope does not prove irrelevance. A known
external source without a supported applicability rule leaves coverage
undetermined.

`pinned_inventory_exhausted` describes this declared universe only. Every valid
assessment retains `OUTSIDE_SCOPE_UNASSESSED`; it is not a claim that no unknown
external source exists.

## 3. Model and time semantics

[ALG] Model subjects require one exact matching catalog endpoint. No match,
multiple exact definitions or an unsupported spelling remains unresolved;
there is no normalization or admitted alias rule. A snapshot bound to a
different valid endpoint cannot resolve the subject's requested model name.

Structural and linkage checks precede use of source claims. They include real
catalog kinds/IDs, successful capture for positive evidence, matching payload
digest, valid ModelIdentity targets, actual timestamp/interval values, capture
after observation and internally consistent availability chronology. Scalars
cannot enter model-target sets through Boolean/integer coercion. A failed
capture cannot prove that the requested name was absent.

Applicability then checks the endpoint, exact requested name, observation time,
freshness, assertion interval and availability. Intervals and freshness limits
are inclusive. Explicit timezone offsets are required; invalid offset minutes
are rejected before Python can normalize them. The fixed availability bound is:

| Mode | Bound |
| --- | --- |
| `event_time` | `min(subject.occurred_at, knowledge_cutoff)` |
| `retrospective` | `knowledge_cutoff`, which must not precede either subject event |

Retrospective evaluation still requires an event-applicable observation; it
does not back-project a later catalog observation. Late availability is an
exclusion, while impossible chronology is invalid. Unknown non-null assertion
scope or uninterpreted `superseded_by` cannot act as a wildcard or newest-source
override. Proven endpoint/name/time exclusions do not become global vetoes.

All applicable sources are aggregated. A relevant contradicted capture,
within-snapshot ambiguity or cross-source disagreement survives favorable
evidence. There is no first-success, majority, newest-source or evidence-label
ranking rule.

| Result axis | Implemented meaning |
| --- | --- |
| `supplied_relation` | Bounded catalog-declared observation; may relax coverage/availability proof only, preserving endpoint, capture, target, time and conflict checks |
| `R_identity` | Catalog-record relation after complete pinned coverage and applicable-source checks; identity basis remains `catalog_declared` |
| `Q_identity` | `conditions_satisfied` only for clean non-equivalent model records with both exact synthetic witnesses and exhausted bounded inventory; otherwise `withheld` |
| `C3`, `C10`, `Q_C3_C10` | Always `unresolved`, with `NOT_EVALUATED`: 3C is not admitted |

An `unknown` release may preserve a catalog-record relation, but cannot satisfy
the synthetic identity condition. Equal MID records, especially unknown-release
records, do not establish affirmative real-executor equivalence or a C3
violation.

## 4. A1: the exact synthetic corroboration premise

[ALG] A `SYN-MODEL-WITNESS-1` witness must match the complete pinned witness row
and the exact same-side endpoint, requested name, MID, event and property
`model_reference_resolves_to_identity`. Its evidence must include one applicable
same-side **capture → snapshot → payload → MID** chain. That capture itself must
carry the corroborated class; another source's label cannot be borrowed.

All evidence, verifier-executor, verifier-version, rule-version, verification
and assessment-scope references are dereferenced to retained bytes. The decoded
verification artifact must equal exactly:

```python
{
    "profile_id": "SYN-MODEL-WITNESS-1",
    "subject": witness["subject"],
    "evidence_refs": witness["evidence_refs"],
}
```

The witness interval must include the event; revocation applies at
`event >= revoked_at`. `assessed_at <= bound` is necessary but insufficient.
An exact pinned availability row must bind both the witness bytes and its
verification artifact, with `assessed_at <= available_at <= bound`. Source
availability separately binds the capture, snapshot and payload, with
`captured_at <= available_at <= bound`.

[OPEN] These are stipulated fictional proof premises. A matching payload digest
establishes byte identity, not semantic derivation of every snapshot assertion
from that payload. A matching verification JSON body does not independently
execute or authenticate a verifier. Neither synthetic success nor a catalog
corroboration label establishes a live binding, epistemic independence or
authorization.

## 5. A2: missing evidence without invented references

| Missing or adverse condition | Representation and consequence |
| --- | --- |
| Successful-capture payload absent | `payload_ref=null` plus an explicit timely omission matching the expected digest; relevant source remains unavailable |
| MID absent | No fabricated target reference; explicit timely omission matching the missing MID can retain a valid incomplete assessment |
| Unknown expected ID/digest | Keep null in the unavailable declaration; potentially relevant omission blocks clean relation/identity qualification |
| Required snapshot/capture linkage absent | Closed source shape cannot represent a substitute; typed refusal such as `KNOWN_SOURCE_UNAVAILABLE` |
| Reference names absent bytes without a permissible omission | Typed unavailable/missing-target refusal, never a placeholder ArtifactRef |
| Existing bytes conflict with their digest, kind or manifest | Typed invalid assessment; no omission-based repair of conflicting bytes |

Availability or coverage gaps may leave a bounded `supplied_relation`; they
cannot make a malformed endpoint, failed capture, invalid target or relevant
contradiction acceptable. Invalid envelopes keep typed reasons, unresolved
relations and constraints, and withheld identity qualification. They are not
accepted assessment publications.

## 6. A3: compatibility, ordering and publication

[ALG] [DECISION-20261126-0001](../../../self_model/decisions/DECISION-20261126-0001.json)
authorizes the 3A Boolean change while preserving the historical
[DECISION-20260814-0001](../../../self_model/decisions/DECISION-20260814-0001.json).

Legacy `resolve_identity()` never returns a new positive v1 resolution. Missing
context yields a separate r2 refusal with `LEGACY_CONTEXT_REQUIRED`; checked
context yields `LEGACY_POSITIVE_DISABLED`, optionally naming a checked
assessment. Legacy invocation arguments must equal the complete retained
invocation on the corresponding Query side. `equivalence()` may project a
checked diagnostic relation, but `blocks_adjudication` is always true, including
direct result construction. Disabled or failing evaluators cannot recover the
retired first-success path; rollback must preserve the refusal boundary.

The uppercase legacy reasons are not added to IdentityResolution v1. Historical
readers/graphs remain diagnostic and non-authoritative. The v1 builder rejects
r2 envelopes and Boolean coercion; its writer uses atomic no-replacement
publication, refusing same-ID/different-byte overwrite. General catalog-writer
redesign is outside 3A.

Reasons use the total key `(stage, declared ReasonCode order, side, canonical
normalized subject_refs, canonical complete reason)`. Source findings end with
canonical complete-finding bytes. Exact duplicates are idempotent. Permuted
collections cannot choose a different semantic winner; changed retained
context/query bytes legitimately change references and assessment identity.

`write_assessment(result, anchor=..., query_bytes=..., output_dir=...)` accepts
only schema-valid, semantically valid synthetic envelopes equal to exact-input
recomputation. It stores full-content-addressed bytes and a collision-checked
display-ID entry outside the production checkout. Atomic no-replacement writes
prevent partial JSON or overwrite; identical replay is idempotent. A failed
multi-object publication may leave a complete unindexed CAS object, but returns
no accepted publication. Neither this store nor a v1 annotation is a canonical
VERIFY or live qualification record.

## 7. Remaining scope limits and evidence

[OPEN] Subjects must be existing
[InvocationRecord v1](../../../../ai_lab/providers/invocation_record.py)
records, not arbitrary provider responses or session messages. The existing
validator accepts its permitted partial/unknown manifests and nullable
execution-profile fields. Query matching uses the invocation's top-level
executor/name/endpoint/time; 3A adds no independent execution observation or
general semantic reconciliation of duplicated profile metadata. Complete-byte
binding does not prove effective-input completeness or a true runtime identity.

Tool/human profile shapes and prospective `SYN-C3-CONFLICT-1` fields are retained
in the frozen schema only. No tool/human identity rule, ancestry traversal,
C3 conflict evaluator, C10 reliance evaluator, live profile enrollment or
authority consumer is implemented. Cross-kind relations stay unresolved.
GAP-0008 remains structural; no lineage/origin promotion, gap closure, whole-PLAN
completion, merge or Step 5 activation follows from this implementation.

[ALG] [TEST-MATRIX.md](TEST-MATRIX.md) maps source tests to the admitted parts
of the proposed falsifier families. Historical baseline/schema reports remain
pre-implementation evidence. Execution totals, exact subjects, receipts and
mutation outcomes belong to the separately retained validation report.
