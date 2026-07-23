# COMP-0036: Provider Comparison — PLAN-20260723-0001 slice B admission review

## Metadata

- comparison_id: `COMP-0036`
- title: `PLAN-20260723-0001 slice B admission review`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-0ae13a18453a458f.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0036", "target_id": "INV-0ae13a18453a458f"}, {"authoritative": false, "evidence": "docs/invocations/INV-08687f806100ba12.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0036", "target_id": "INV-08687f806100ba12"}]`
- created_at: `2026-07-23T15:56:45.672207+00:00`
- command: `scripts/compare_providers.py --title PLAN-20260723-0001 slice B admission review Review the plan below for admission. Full texts of the plan, its source gap, the relevant ontology sections, and the prior round that shaped it are included. Do not rely on repository access; quote only text that appears below. If something you need is not present, say so rather than inferring it.

=== PLAN-20260723-0001 ===
{
  "constraints": [
    "Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan.",
    "Field names and semantics follow ABS-0004 v5 exactly; deviations require an ABS revision first.",
    "All relations use the GraphRelation shape; no parallel edge vocabulary; no predicate outside the registered Slice A and Slice B lists.",
    "The two CatalogCapture status fields may never be merged, defaulted from one another, or derived from one another.",
    "Live network access is opt-in, disabled by default, and no test may require it.",
    "Slice A behavior is unchanged: no field, path, or default of invocation capture is altered by this slice."
  ],
  "created_at": "2026-07-23T00:00:00+00:00",
  "created_from": {
    "repo_commit": "6d7dfeefb58cbf0a58ea2cd50a8c90795d3f41bf",
    "source_gap_id": "GAP-0005"
  },
  "depends_on_capability_ids": [
    "CAP-0015"
  ],
  "evidence_ids": [
    "docs/self_model/gaps/GAP-0005.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
    "docs/comparisons/COMP-0035-slice-b-scoping-catalog-identity-resolution.md",
    "docs/self_model/capabilities/CAP-0015.json",
    "docs/self_model/warrants/WARR-20260722-0002.json"
  ],
  "expected_outputs": [
    "ai_lab/providers/catalog.py (identity, assertion, snapshot, and capture schemas with validators).",
    "ai_lab/providers/catalog_resolution.py (pure resolution, freshness, and annotation records).",
    "Opt-in live capture path with recorded fixtures under tests/fixtures/catalog/.",
    "docs/self_model/PREDICATE_REGISTRY.md extended with the Slice B predicates.",
    "docs/self_model/CATALOG_RECORDS.md documenting the record family, the evidence-class separation, and stated limitations.",
    "tests/test_catalog.py and tests/test_catalog_resolution.py with schema, rejection, non-resolution, and integration fixtures."
  ],
  "mitigation": "Non-resolution is explicit and enumerated rather than defaulted; the temporal rule requires the snapshot to precede the invocation, so a later snapshot can never retroactively verify an earlier call; ambiguity blocks resolution rather than picking a winner; fixtures record their capture date and the freshness validator reports currency against it rather than assuming it.",
  "next_action": "Run the admission comparison round with this plan, GAP-0005, and ABS-0004 v5 Sections 4.2 to 4.4 attached as text; on operator adjudication, issue the admission warrant and flip status to admitted.",
  "non_goals": [
    "Mutating captured InvocationRecords; resolution is append-only annotation.",
    "Any claim of independent verification of catalog content while the only source is provider self-report.",
    "RoleDefinition, RoleQualification, InvocationAuthorization, or consequence classes (Slice C).",
    "Lineage traversal, independence assessment, or evidence-admission enforcement (Slice D).",
    "Routing, escalation, model selection, or provider recommendation of any kind.",
    "Any consumer that gates a decision on resolution results; C2 catalog admission activation is a later decision.",
    "Capture on any path other than the admitted Slice A path; Slice B adds catalog capture, not invocation capture.",
    "Automatic re-resolution of previously annotated invocations when catalogs change; supersession is recorded, not retroactively applied."
  ],
  "objective": "Make provider identity claims representable and datable so that the unresolved status Slice A records everywhere can be discharged honestly, and so that ADVISOR-0000-class catalog claims can be dated, superseded, and contradicted instead of merely believed or disbelieved.",
  "plan_id": "PLAN-20260723-0001",
  "proposed_change": "After a separate admission checkpoint: add ai_lab/providers/catalog.py (schema, validators, canonical serialization, identity and path rules), ai_lab/providers/catalog_resolution.py (pure resolution and freshness functions, annotation records), an opt-in live capture path, predicate-registry entries, recorded fixtures, tests, and documentation. No change to Slice A capture, no change to provider-call behavior, and no consumer that gates any decision on resolution results.",
  "rationale": [
    "GAP-0005 records that model identity is a settings string with no identity, endpoint, or catalog object behind it, so every catalog claim is unverifiable by construction; Slice B is the admitted ontology's second proposed boundary.",
    "Slice A now emits identity_verification_status unresolved on every record with no mechanism to discharge it; the status is honest but permanently stuck without this slice.",
    "COMP-0035 supplied the design constraints both witnesses converged on: temporal bounding, unambiguous resolution, append-only annotation for stale assertions, and separation of what the channel proves from what the content claims.",
    "ABS-0004 v5 renamed CatalogVerification to CatalogCapture and added P6 precisely because this slice would otherwise build a record whose name overstates its evidence; the amendment is upstream of the implementation, as intended."
  ],
  "repo_commit": "6d7dfeefb58cbf0a58ea2cd50a8c90795d3f41bf",
  "risk": "Resolution semantics decided here determine what identity independence can mean in Slice D: if resolution is loose, C3's per-kind equivalence check inherits the looseness. A permissive freshness window would let stale assertions discharge unresolved statuses that should remain open. Recorded fixtures of provider catalogs age, and an aged fixture can encode a mapping the provider has since changed.",
  "schema_version": "v1",
  "scope": [
    "A catalog module defining schema v1 for ModelIdentity, ServiceEndpointIdentity, CatalogAssertion, CatalogSnapshot, and CatalogCapture as ABS-0004 v5 Sections 4.2, 4.3, and 4.4 specify, with validate_catalog_record entrypoints, canonical serialization reusing the invocation-record precedent, and deterministic identity and path rules under docs/catalog/.",
    "Atomic assertions only: one claim per assertion with assertion_subject, assertion_predicate, assertion_value_or_target, unit, scope, valid_from, valid_until or superseded, and source; heterogeneous multi-claim records are rejected by the validator.",
    "CatalogCapture with the two independently scoped status fields; the validator rejects any capture whose source_type is provider_self_report and whose content_evidence_status is stronger than self_asserted (ABS-0004 v5 adopted constraint).",
    "A resolution function, pure over stored snapshots, mapping (service_endpoint, requested_model_name, occurred_at) to a ModelIdentity or to an explicit non-resolution reason: no applicable assertion, snapshot observed after the invocation, ambiguous multiple applicable assertions, or expired freshness window.",
    "An append-only IdentityResolution annotation record referencing an InvocationRecord by id and carrying the resolved identity, the snapshot and assertion relied on, the resolution timestamp, and the evidence class inherited from the capture; captured invocation records are never mutated.",
    "A freshness validator reporting per-assertion currency using the shared verification-outcome vocabulary for channel authentication and freshness only, never for content evidence.",
    "Predicate-registry entries for the Slice B predicates: resolved_to, asserted_by, concerns, and captured.",
    "A live catalog fetch path behind an explicit opt-in (environment flag), disabled by default, writing CatalogCaptures with source_type provider_self_report; recorded fixtures of real catalog payloads for offline tests.",
    "Validator fixtures covering valid records, each rejection class, each non-resolution reason, and an integration fixture resolving a stored Slice A invocation record offline."
  ],
  "source_capability_ids": [
    "CAP-0015"
  ],
  "source_gap_id": "GAP-0005",
  "status": "proposed",
  "success_criteria": [
    "A stored Slice A InvocationRecord resolves to a ModelIdentity through the pure resolution function using a stored snapshot, producing an append-only IdentityResolution annotation; the InvocationRecord file is byte-identical before and after.",
    "Each non-resolution reason is exercised by a fixture: no applicable assertion, snapshot observed after the invocation, ambiguous applicable assertions, and expired freshness window; each yields an explicit reason, never a silent default to resolved.",
    "The validator rejects a CatalogCapture whose source_type is provider_self_report and whose content_evidence_status is independently_corroborated, and accepts the same capture with self_asserted.",
    "Assertions are atomic: a record carrying two claims is rejected.",
    "Freshness reporting uses the shared verification-outcome vocabulary for channel authentication and freshness; a test asserts that content_evidence_status never takes a verification-outcome value.",
    "The full suite passes offline with no network access; the live capture path is disabled by default and its absence does not fail any test.",
    "The repository audit remains ok true verified_current, and cross-environment reproduction from the public repository succeeds byte-identically."
  ],
  "summary": "Implement ABS-0004 v5 Slice B: catalog identity resolution for the invocation records Slice A already captures. Adds ModelIdentity and ServiceEndpointIdentity records; atomic CatalogAssertions grouped into CatalogSnapshots; CatalogCapture records carrying capture_method, source_type, captured_at, capture_success, capturing_executor, content_digest, and the two independently scoped status fields channel_authentication_status and content_evidence_status; requested-name to resolved-identity linkage; and a freshness and resolution validator. An already-captured InvocationRecord may move from identity_verification_status unresolved to resolved only when an applicable assertion binds its endpoint and requested name at its occurrence time, unambiguously and from a snapshot observed no later than the invocation. Resolution is recorded as an append-only annotation referencing the invocation, never by mutating the captured record. Live catalog fetching is a separate opt-in path; the resolution and freshness logic is a pure function over stored snapshots and is tested offline against recorded fixtures.",
  "title": "Catalog identity resolution with honest evidence classing (ABS-0004 Slice B)"
}

=== GAP-0005 ===
{
  "blocked_by": [],
  "category": "provider_infrastructure",
  "evidence": {
    "files_checked": [
      "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
      "docs/comparisons/COMP-0032-abs-0004-invocation-authorization-ontology-challenge-round.md",
      "docs/abstractions/evidence/ADVISOR-MANIFEST.md",
      "docs/abstractions/evidence/ADVISOR-0000-sol-model-stack-proposal.md",
      "ai_lab/providers/settings.py",
      "ai_lab/providers/claude_provider.py",
      "scripts/ask_provider.py",
      "scripts/compare_providers.py"
    ],
    "reason": "ABS-0004 v4 was admitted at commit 56f18a2 with enforcement-matrix rows C1, C2, C4, C5, and C8 marked proposed with representability none: the admitted ontology itself records that its subject matter cannot yet be represented. ai_lab/providers/settings.py holds model identity as environment-overridable strings and AI_LAB_CLAUDE_MAX_TOKENS with default 4096; no identity, endpoint, catalog, invocation, or manifest object exists anywhere in ai_lab/. COMP-0032's Claude response was truncated by that 4096 cap and the saved artifact could not explain the truncation from its own contents; the incident chain recorded in the artifact's addendum is cited in ABS-0004 Slice A as motivation for ExecutionProfile capture. ADVISOR-0000 consists largely of catalog assertions with verification_outcome unverifiable at capture, and no mechanism exists to verify, date, or supersede such claims. C3, C6, C7, C9, C10, and C11 are adopted-manual; their current enforcement evidence is attestations and disclosure statements in warrants, not structural checks."
  },
  "gap_id": "GAP-0005",
  "last_reviewed_at": "2026-07-20T00:00:00+00:00",
  "name": "Provider invocations lack ontology-mandated representation and governance",
  "notes": [
    "Expressed against admitted ABS-0004 v4 per the agreed sequence (ontology first, challenge round, then the gap). Candidate remediation path is Slices A-D of ABS-0004 Section 10, each a separately governed plan; this gap does not pre-admit any of them.",
    "The deferred provider comparison (third-provider decision per the C5 witness-path framing, per-provider escalation ladders, live catalog verification) is intentionally sequenced after Slice B, because its subject matter is catalog assertions and identities that only Slice B makes representable.",
    "The parked CLAUDE_MAX_TOKENS default change should ride with Slice A as a governed settings change, so the new ExecutionProfile capture records the corrected limit from its first use."
  ],
  "priority": "high",
  "recommended_first_slice": "ABS-0004 Section 10 Slice A exactly as admitted: invocation provenance capture on the scripts/compare_providers.py path only. Atomic InvocationRecord; executor reference with identity-verification status; requested API model name; endpoint surface; session identity; minimal EffectiveInputManifest (rendered prompt digest, instruction digests, ContextManifest reference, tool-schema digest, prior tool-result references, session-state mode, completeness_attestation); ExecutionProfile reference including output-token limits; spawned edges; experimental-versus-governed marker; produced_by relation; status; validator and integration fixture. No routing, no catalog enforcement. Relations in GraphRelation shape with predicate-registry entries for the seven Slice A predicates.",
  "related_capabilities": [],
  "risk": "Without invocation provenance, every governed decision that relies on provider outputs rests on undisclosed execution conditions: truncations, configuration differences, session contamination, and model substitutions are invisible after the fact, as COMP-0032's truncation incident showed. Without catalog verification, unverifiable provider claims (ADVISOR-0000 class) can only be excluded by operator vigilance. Without structural authority separation, the C3/C6/C7 disciplines depend entirely on session practice and degrade silently if practice slips. Deferring representation while building routing or escalation would recreate the retrofit debt GAP-0004 was opened to prevent.",
  "schema_version": "v1",
  "status": "open",
  "summary": "The admitted invocation authorization ontology ABS-0004 v4 (commit 56f18a2) defines the objects, relations, and constraints under which AI-Lab authorizes invocations for roles, but none of it is representable or enforceable in the running system. Concretely: provider calls made through ask_provider.py and compare_providers.py leave no InvocationRecord, no executor identity, no ExecutionProfile, no EffectiveInputManifest, and no session identity; model identity is a settings string with no ModelIdentity, ServiceEndpointIdentity, CatalogSnapshot, or CatalogVerification behind it, so every catalog claim (including the entire ADVISOR-0000 model stack) is unverifiable by construction; roles, qualifications, and InvocationAuthorization have no record forms, so the epistemic-authority separation practiced in sessions is testimonial rather than structural; and lineage, independence assessment, and evidence admission (C3-C5, C9-C11) are enforced only by manual discipline with no ancestry capture. The COMP-0032 round demonstrated the operational cost concretely: a response truncation shaped the evidence record and nothing in the record could explain it, because the output-token limit that caused it was captured nowhere. The deficiency blocks the deferred provider comparison (third-provider decision, escalation ladders, live catalog verification), the sidecar generation slice under GAP-0002 (which needs structured generator provenance), and any future routing or escalation policy."
}

=== ABS-0004 v5 SECTIONS 4.2-4.4 (identity, endpoint, catalog) ===
### 4.2 ServiceEndpointIdentity

`[DEF]` The concrete API surface through which execution is requested:
stable endpoint identifier and operating organization (which may differ from
the model's originator). Mutable endpoint properties (region, processing
jurisdiction, retention behavior, data handling) are represented as
time-bounded endpoint assertions under the catalog model, not identity
fields; this applies to endpoints the same identity/assertion discipline
applied to models. The same ModelIdentity served through different endpoints
may differ in identity resolution, jurisdiction, and catalog properties;
endpoint diversity never implies model independence.

### 4.3 ModelIdentity

`[DEF]` The stable identity of a model release used for provenance:
`model_id`, `originator_id` (developing organization), canonical name,
release/version identity where verifiable, identity verification status.
Deprecation is mutable and endpoint-specific; it lives in catalog
assertions. `[ADOPTED_CONSTRAINT]` An invocation records the most precise
ModelIdentity establishable at execution time; unresolved requested names are
recorded as unresolved, never silently substituted.

### 4.4 CatalogSnapshot, CatalogAssertion, and CatalogCapture

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic and records ONLY
the claim: `assertion_subject`, `assertion_predicate`,
`assertion_value_or_target`, unit, scope, `valid_from`,
`valid_until`/superseded, source. An assertion may concern an API alias, an
endpoint, a price, a region, or a model identity. Example atomic
assertions: (api-name-X, resolves_to, model-identity-Y);
(api-name-X, context_limit, 400000, tokens).

`[DEF]` CatalogCapture: the record of how and when an assertion was
obtained. Fields: `capture_method`, `source_type`, `captured_at`,
`capture_success`, `capturing_executor`, `content_digest` of the retrieved
payload, and two independently scoped status fields that must never be
merged:

- `channel_authentication_status`: what was independently established about
  the channel the claim arrived through (for example endpoint identity via
  a certificate chain or key digest). This is genuine evidence: it is not
  controlled by the content of the provider's catalog claim.
- `content_evidence_status`: what was established about the truth of the
  claim itself. When the only source is the provider describing its own
  catalog, this is `self_asserted` and nothing stronger, regardless of how
  well the channel authenticated.

`[ADOPTED_CONSTRAINT]` A capture whose `source_type` is
`provider_self_report` may never record a content-evidence status implying
independent confirmation. Authenticating the channel establishes who said
it, not whether it is true.

`[DEF]` The shared three-valued vocabulary of
`ai_lab/documentation/verification_outcome.py` applies to
`channel_authentication_status` and to freshness assessment. It does not
apply to `content_evidence_status`, whose values describe evidence class
(`self_asserted`, `independently_corroborated`, `contradicted`,
`unassessed`), not verification currency.

`[DEF]` Catalog assertions record what a provider claims; they never record
suitability for an AI-Lab role.

`[PRINCIPLE]` P6. Naming may not exceed evidence. A record whose name or
status field implies independent confirmation, where none exists, is a
defect regardless of the correctness of its contents: consumers read the
label, not the caveat. v4 named this record CatalogVerification; both
COMP-0035 witnesses independently identified that name as circular
self-attestation, a provider's own assertion relabelled as its own
verification. The rename to CatalogCapture is the remedy, and the
principle generalizes: prefer a blunt name that cannot be misread over a
precise one that will be.


=== ABS-0004 v5 SECTION 10 (proposed slice sequence) ===
## 10. Proposed Implementation Sequence

`[PROPOSAL]` Candidate slices, each subject to GAP definition, plan
admission, and review; not commitments:

- Slice A, invocation provenance capture on exactly one path
  (`scripts/compare_providers.py`): atomic InvocationRecord; executor
  reference with identity-verification status; requested API model name;
  endpoint surface; session identity (not mode alone; shared
  provider-managed state is undetectable from a mode flag); minimal
  EffectiveInputManifest containing rendered prompt digest,
  system/developer instruction digests, ContextManifest reference, exposed
  tool-schema digest, prior tool-result references, session-state mode,
  and completeness_attestation (only fields applicable to this path
  populated); ExecutionProfile reference including output-token limits
  (motivated by the COMP-0032 truncation incident, which the record could
  not explain from its own contents); `spawned` edges for subordinate
  executions; experimental-versus-governed marker; `produced_by`; status;
  validator and integration fixture. No routing, no catalog enforcement.
- Slice B, catalog identity resolution: ModelIdentity,
  ServiceEndpointIdentity, atomic assertions in snapshots, requested-name
  to resolved-identity linkage, freshness/verification validator.
- Slice C, role and authorization: RoleDefinition, execution-scoped
  qualification, InvocationAuthorization, consequence class,
  experimental/governed boundary.
- Slice D, lineage and evidence admission: effective-input ancestry,
  pre-provenance inheritance, EvidenceAdmissionDecision, conservative
  independence statuses.


=== QUESTIONS ===
1. Does the scope stay inside the Slice B boundary, and does anything in it belong to Slice C or D?
2. The plan resolves invocations by append-only annotation and never mutates captured records. Construct a case where this is insufficient: a situation where an annotation-only design leaves a consumer with a materially misleading picture.
3. The temporal rule requires the snapshot to be observed no later than the invocation. Name a legitimate case this rule wrongly excludes, if one exists, and say whether excluding it is the right trade.
4. The validator forbids a provider_self_report capture from carrying content evidence stronger than self_asserted. Construct a way to satisfy that rule while still conveying false confidence to a downstream reader.
5. Which decisions in this slice constrain Slice D's independence assessment, and how?
6. Are the success criteria mechanically checkable? Name any that is not, and any missing check.
7. Recommendation: admit as written, admit with named conditions (state them), or revise first.

Do not certify or praise. No provider product recommendations.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Review the plan below for admission. Full texts of the plan, its source gap, the relevant ontology sections, and the prior round that shaped it are included. Do not rely on repository access; quote only text that appears below. If something you need is not present, say so rather than inferring it.

=== PLAN-20260723-0001 ===
{
  "constraints": [
    "Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan.",
    "Field names and semantics follow ABS-0004 v5 exactly; deviations require an ABS revision first.",
    "All relations use the GraphRelation shape; no parallel edge vocabulary; no predicate outside the registered Slice A and Slice B lists.",
    "The two CatalogCapture status fields may never be merged, defaulted from one another, or derived from one another.",
    "Live network access is opt-in, disabled by default, and no test may require it.",
    "Slice A behavior is unchanged: no field, path, or default of invocation capture is altered by this slice."
  ],
  "created_at": "2026-07-23T00:00:00+00:00",
  "created_from": {
    "repo_commit": "6d7dfeefb58cbf0a58ea2cd50a8c90795d3f41bf",
    "source_gap_id": "GAP-0005"
  },
  "depends_on_capability_ids": [
    "CAP-0015"
  ],
  "evidence_ids": [
    "docs/self_model/gaps/GAP-0005.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
    "docs/comparisons/COMP-0035-slice-b-scoping-catalog-identity-resolution.md",
    "docs/self_model/capabilities/CAP-0015.json",
    "docs/self_model/warrants/WARR-20260722-0002.json"
  ],
  "expected_outputs": [
    "ai_lab/providers/catalog.py (identity, assertion, snapshot, and capture schemas with validators).",
    "ai_lab/providers/catalog_resolution.py (pure resolution, freshness, and annotation records).",
    "Opt-in live capture path with recorded fixtures under tests/fixtures/catalog/.",
    "docs/self_model/PREDICATE_REGISTRY.md extended with the Slice B predicates.",
    "docs/self_model/CATALOG_RECORDS.md documenting the record family, the evidence-class separation, and stated limitations.",
    "tests/test_catalog.py and tests/test_catalog_resolution.py with schema, rejection, non-resolution, and integration fixtures."
  ],
  "mitigation": "Non-resolution is explicit and enumerated rather than defaulted; the temporal rule requires the snapshot to precede the invocation, so a later snapshot can never retroactively verify an earlier call; ambiguity blocks resolution rather than picking a winner; fixtures record their capture date and the freshness validator reports currency against it rather than assuming it.",
  "next_action": "Run the admission comparison round with this plan, GAP-0005, and ABS-0004 v5 Sections 4.2 to 4.4 attached as text; on operator adjudication, issue the admission warrant and flip status to admitted.",
  "non_goals": [
    "Mutating captured InvocationRecords; resolution is append-only annotation.",
    "Any claim of independent verification of catalog content while the only source is provider self-report.",
    "RoleDefinition, RoleQualification, InvocationAuthorization, or consequence classes (Slice C).",
    "Lineage traversal, independence assessment, or evidence-admission enforcement (Slice D).",
    "Routing, escalation, model selection, or provider recommendation of any kind.",
    "Any consumer that gates a decision on resolution results; C2 catalog admission activation is a later decision.",
    "Capture on any path other than the admitted Slice A path; Slice B adds catalog capture, not invocation capture.",
    "Automatic re-resolution of previously annotated invocations when catalogs change; supersession is recorded, not retroactively applied."
  ],
  "objective": "Make provider identity claims representable and datable so that the unresolved status Slice A records everywhere can be discharged honestly, and so that ADVISOR-0000-class catalog claims can be dated, superseded, and contradicted instead of merely believed or disbelieved.",
  "plan_id": "PLAN-20260723-0001",
  "proposed_change": "After a separate admission checkpoint: add ai_lab/providers/catalog.py (schema, validators, canonical serialization, identity and path rules), ai_lab/providers/catalog_resolution.py (pure resolution and freshness functions, annotation records), an opt-in live capture path, predicate-registry entries, recorded fixtures, tests, and documentation. No change to Slice A capture, no change to provider-call behavior, and no consumer that gates any decision on resolution results.",
  "rationale": [
    "GAP-0005 records that model identity is a settings string with no identity, endpoint, or catalog object behind it, so every catalog claim is unverifiable by construction; Slice B is the admitted ontology's second proposed boundary.",
    "Slice A now emits identity_verification_status unresolved on every record with no mechanism to discharge it; the status is honest but permanently stuck without this slice.",
    "COMP-0035 supplied the design constraints both witnesses converged on: temporal bounding, unambiguous resolution, append-only annotation for stale assertions, and separation of what the channel proves from what the content claims.",
    "ABS-0004 v5 renamed CatalogVerification to CatalogCapture and added P6 precisely because this slice would otherwise build a record whose name overstates its evidence; the amendment is upstream of the implementation, as intended."
  ],
  "repo_commit": "6d7dfeefb58cbf0a58ea2cd50a8c90795d3f41bf",
  "risk": "Resolution semantics decided here determine what identity independence can mean in Slice D: if resolution is loose, C3's per-kind equivalence check inherits the looseness. A permissive freshness window would let stale assertions discharge unresolved statuses that should remain open. Recorded fixtures of provider catalogs age, and an aged fixture can encode a mapping the provider has since changed.",
  "schema_version": "v1",
  "scope": [
    "A catalog module defining schema v1 for ModelIdentity, ServiceEndpointIdentity, CatalogAssertion, CatalogSnapshot, and CatalogCapture as ABS-0004 v5 Sections 4.2, 4.3, and 4.4 specify, with validate_catalog_record entrypoints, canonical serialization reusing the invocation-record precedent, and deterministic identity and path rules under docs/catalog/.",
    "Atomic assertions only: one claim per assertion with assertion_subject, assertion_predicate, assertion_value_or_target, unit, scope, valid_from, valid_until or superseded, and source; heterogeneous multi-claim records are rejected by the validator.",
    "CatalogCapture with the two independently scoped status fields; the validator rejects any capture whose source_type is provider_self_report and whose content_evidence_status is stronger than self_asserted (ABS-0004 v5 adopted constraint).",
    "A resolution function, pure over stored snapshots, mapping (service_endpoint, requested_model_name, occurred_at) to a ModelIdentity or to an explicit non-resolution reason: no applicable assertion, snapshot observed after the invocation, ambiguous multiple applicable assertions, or expired freshness window.",
    "An append-only IdentityResolution annotation record referencing an InvocationRecord by id and carrying the resolved identity, the snapshot and assertion relied on, the resolution timestamp, and the evidence class inherited from the capture; captured invocation records are never mutated.",
    "A freshness validator reporting per-assertion currency using the shared verification-outcome vocabulary for channel authentication and freshness only, never for content evidence.",
    "Predicate-registry entries for the Slice B predicates: resolved_to, asserted_by, concerns, and captured.",
    "A live catalog fetch path behind an explicit opt-in (environment flag), disabled by default, writing CatalogCaptures with source_type provider_self_report; recorded fixtures of real catalog payloads for offline tests.",
    "Validator fixtures covering valid records, each rejection class, each non-resolution reason, and an integration fixture resolving a stored Slice A invocation record offline."
  ],
  "source_capability_ids": [
    "CAP-0015"
  ],
  "source_gap_id": "GAP-0005",
  "status": "proposed",
  "success_criteria": [
    "A stored Slice A InvocationRecord resolves to a ModelIdentity through the pure resolution function using a stored snapshot, producing an append-only IdentityResolution annotation; the InvocationRecord file is byte-identical before and after.",
    "Each non-resolution reason is exercised by a fixture: no applicable assertion, snapshot observed after the invocation, ambiguous applicable assertions, and expired freshness window; each yields an explicit reason, never a silent default to resolved.",
    "The validator rejects a CatalogCapture whose source_type is provider_self_report and whose content_evidence_status is independently_corroborated, and accepts the same capture with self_asserted.",
    "Assertions are atomic: a record carrying two claims is rejected.",
    "Freshness reporting uses the shared verification-outcome vocabulary for channel authentication and freshness; a test asserts that content_evidence_status never takes a verification-outcome value.",
    "The full suite passes offline with no network access; the live capture path is disabled by default and its absence does not fail any test.",
    "The repository audit remains ok true verified_current, and cross-environment reproduction from the public repository succeeds byte-identically."
  ],
  "summary": "Implement ABS-0004 v5 Slice B: catalog identity resolution for the invocation records Slice A already captures. Adds ModelIdentity and ServiceEndpointIdentity records; atomic CatalogAssertions grouped into CatalogSnapshots; CatalogCapture records carrying capture_method, source_type, captured_at, capture_success, capturing_executor, content_digest, and the two independently scoped status fields channel_authentication_status and content_evidence_status; requested-name to resolved-identity linkage; and a freshness and resolution validator. An already-captured InvocationRecord may move from identity_verification_status unresolved to resolved only when an applicable assertion binds its endpoint and requested name at its occurrence time, unambiguously and from a snapshot observed no later than the invocation. Resolution is recorded as an append-only annotation referencing the invocation, never by mutating the captured record. Live catalog fetching is a separate opt-in path; the resolution and freshness logic is a pure function over stored snapshots and is tested offline against recorded fixtures.",
  "title": "Catalog identity resolution with honest evidence classing (ABS-0004 Slice B)"
}

=== GAP-0005 ===
{
  "blocked_by": [],
  "category": "provider_infrastructure",
  "evidence": {
    "files_checked": [
      "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
      "docs/comparisons/COMP-0032-abs-0004-invocation-authorization-ontology-challenge-round.md",
      "docs/abstractions/evidence/ADVISOR-MANIFEST.md",
      "docs/abstractions/evidence/ADVISOR-0000-sol-model-stack-proposal.md",
      "ai_lab/providers/settings.py",
      "ai_lab/providers/claude_provider.py",
      "scripts/ask_provider.py",
      "scripts/compare_providers.py"
    ],
    "reason": "ABS-0004 v4 was admitted at commit 56f18a2 with enforcement-matrix rows C1, C2, C4, C5, and C8 marked proposed with representability none: the admitted ontology itself records that its subject matter cannot yet be represented. ai_lab/providers/settings.py holds model identity as environment-overridable strings and AI_LAB_CLAUDE_MAX_TOKENS with default 4096; no identity, endpoint, catalog, invocation, or manifest object exists anywhere in ai_lab/. COMP-0032's Claude response was truncated by that 4096 cap and the saved artifact could not explain the truncation from its own contents; the incident chain recorded in the artifact's addendum is cited in ABS-0004 Slice A as motivation for ExecutionProfile capture. ADVISOR-0000 consists largely of catalog assertions with verification_outcome unverifiable at capture, and no mechanism exists to verify, date, or supersede such claims. C3, C6, C7, C9, C10, and C11 are adopted-manual; their current enforcement evidence is attestations and disclosure statements in warrants, not structural checks."
  },
  "gap_id": "GAP-0005",
  "last_reviewed_at": "2026-07-20T00:00:00+00:00",
  "name": "Provider invocations lack ontology-mandated representation and governance",
  "notes": [
    "Expressed against admitted ABS-0004 v4 per the agreed sequence (ontology first, challenge round, then the gap). Candidate remediation path is Slices A-D of ABS-0004 Section 10, each a separately governed plan; this gap does not pre-admit any of them.",
    "The deferred provider comparison (third-provider decision per the C5 witness-path framing, per-provider escalation ladders, live catalog verification) is intentionally sequenced after Slice B, because its subject matter is catalog assertions and identities that only Slice B makes representable.",
    "The parked CLAUDE_MAX_TOKENS default change should ride with Slice A as a governed settings change, so the new ExecutionProfile capture records the corrected limit from its first use."
  ],
  "priority": "high",
  "recommended_first_slice": "ABS-0004 Section 10 Slice A exactly as admitted: invocation provenance capture on the scripts/compare_providers.py path only. Atomic InvocationRecord; executor reference with identity-verification status; requested API model name; endpoint surface; session identity; minimal EffectiveInputManifest (rendered prompt digest, instruction digests, ContextManifest reference, tool-schema digest, prior tool-result references, session-state mode, completeness_attestation); ExecutionProfile reference including output-token limits; spawned edges; experimental-versus-governed marker; produced_by relation; status; validator and integration fixture. No routing, no catalog enforcement. Relations in GraphRelation shape with predicate-registry entries for the seven Slice A predicates.",
  "related_capabilities": [],
  "risk": "Without invocation provenance, every governed decision that relies on provider outputs rests on undisclosed execution conditions: truncations, configuration differences, session contamination, and model substitutions are invisible after the fact, as COMP-0032's truncation incident showed. Without catalog verification, unverifiable provider claims (ADVISOR-0000 class) can only be excluded by operator vigilance. Without structural authority separation, the C3/C6/C7 disciplines depend entirely on session practice and degrade silently if practice slips. Deferring representation while building routing or escalation would recreate the retrofit debt GAP-0004 was opened to prevent.",
  "schema_version": "v1",
  "status": "open",
  "summary": "The admitted invocation authorization ontology ABS-0004 v4 (commit 56f18a2) defines the objects, relations, and constraints under which AI-Lab authorizes invocations for roles, but none of it is representable or enforceable in the running system. Concretely: provider calls made through ask_provider.py and compare_providers.py leave no InvocationRecord, no executor identity, no ExecutionProfile, no EffectiveInputManifest, and no session identity; model identity is a settings string with no ModelIdentity, ServiceEndpointIdentity, CatalogSnapshot, or CatalogVerification behind it, so every catalog claim (including the entire ADVISOR-0000 model stack) is unverifiable by construction; roles, qualifications, and InvocationAuthorization have no record forms, so the epistemic-authority separation practiced in sessions is testimonial rather than structural; and lineage, independence assessment, and evidence admission (C3-C5, C9-C11) are enforced only by manual discipline with no ancestry capture. The COMP-0032 round demonstrated the operational cost concretely: a response truncation shaped the evidence record and nothing in the record could explain it, because the output-token limit that caused it was captured nowhere. The deficiency blocks the deferred provider comparison (third-provider decision, escalation ladders, live catalog verification), the sidecar generation slice under GAP-0002 (which needs structured generator provenance), and any future routing or escalation policy."
}

=== ABS-0004 v5 SECTIONS 4.2-4.4 (identity, endpoint, catalog) ===
### 4.2 ServiceEndpointIdentity

`[DEF]` The concrete API surface through which execution is requested:
stable endpoint identifier and operating organization (which may differ from
the model's originator). Mutable endpoint properties (region, processing
jurisdiction, retention behavior, data handling) are represented as
time-bounded endpoint assertions under the catalog model, not identity
fields; this applies to endpoints the same identity/assertion discipline
applied to models. The same ModelIdentity served through different endpoints
may differ in identity resolution, jurisdiction, and catalog properties;
endpoint diversity never implies model independence.

### 4.3 ModelIdentity

`[DEF]` The stable identity of a model release used for provenance:
`model_id`, `originator_id` (developing organization), canonical name,
release/version identity where verifiable, identity verification status.
Deprecation is mutable and endpoint-specific; it lives in catalog
assertions. `[ADOPTED_CONSTRAINT]` An invocation records the most precise
ModelIdentity establishable at execution time; unresolved requested names are
recorded as unresolved, never silently substituted.

### 4.4 CatalogSnapshot, CatalogAssertion, and CatalogCapture

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic and records ONLY
the claim: `assertion_subject`, `assertion_predicate`,
`assertion_value_or_target`, unit, scope, `valid_from`,
`valid_until`/superseded, source. An assertion may concern an API alias, an
endpoint, a price, a region, or a model identity. Example atomic
assertions: (api-name-X, resolves_to, model-identity-Y);
(api-name-X, context_limit, 400000, tokens).

`[DEF]` CatalogCapture: the record of how and when an assertion was
obtained. Fields: `capture_method`, `source_type`, `captured_at`,
`capture_success`, `capturing_executor`, `content_digest` of the retrieved
payload, and two independently scoped status fields that must never be
merged:

- `channel_authentication_status`: what was independently established about
  the channel the claim arrived through (for example endpoint identity via
  a certificate chain or key digest). This is genuine evidence: it is not
  controlled by the content of the provider's catalog claim.
- `content_evidence_status`: what was established about the truth of the
  claim itself. When the only source is the provider describing its own
  catalog, this is `self_asserted` and nothing stronger, regardless of how
  well the channel authenticated.

`[ADOPTED_CONSTRAINT]` A capture whose `source_type` is
`provider_self_report` may never record a content-evidence status implying
independent confirmation. Authenticating the channel establishes who said
it, not whether it is true.

`[DEF]` The shared three-valued vocabulary of
`ai_lab/documentation/verification_outcome.py` applies to
`channel_authentication_status` and to freshness assessment. It does not
apply to `content_evidence_status`, whose values describe evidence class
(`self_asserted`, `independently_corroborated`, `contradicted`,
`unassessed`), not verification currency.

`[DEF]` Catalog assertions record what a provider claims; they never record
suitability for an AI-Lab role.

`[PRINCIPLE]` P6. Naming may not exceed evidence. A record whose name or
status field implies independent confirmation, where none exists, is a
defect regardless of the correctness of its contents: consumers read the
label, not the caveat. v4 named this record CatalogVerification; both
COMP-0035 witnesses independently identified that name as circular
self-attestation, a provider's own assertion relabelled as its own
verification. The rename to CatalogCapture is the remedy, and the
principle generalizes: prefer a blunt name that cannot be misread over a
precise one that will be.


=== ABS-0004 v5 SECTION 10 (proposed slice sequence) ===
## 10. Proposed Implementation Sequence

`[PROPOSAL]` Candidate slices, each subject to GAP definition, plan
admission, and review; not commitments:

- Slice A, invocation provenance capture on exactly one path
  (`scripts/compare_providers.py`): atomic InvocationRecord; executor
  reference with identity-verification status; requested API model name;
  endpoint surface; session identity (not mode alone; shared
  provider-managed state is undetectable from a mode flag); minimal
  EffectiveInputManifest containing rendered prompt digest,
  system/developer instruction digests, ContextManifest reference, exposed
  tool-schema digest, prior tool-result references, session-state mode,
  and completeness_attestation (only fields applicable to this path
  populated); ExecutionProfile reference including output-token limits
  (motivated by the COMP-0032 truncation incident, which the record could
  not explain from its own contents); `spawned` edges for subordinate
  executions; experimental-versus-governed marker; `produced_by`; status;
  validator and integration fixture. No routing, no catalog enforcement.
- Slice B, catalog identity resolution: ModelIdentity,
  ServiceEndpointIdentity, atomic assertions in snapshots, requested-name
  to resolved-identity linkage, freshness/verification validator.
- Slice C, role and authorization: RoleDefinition, execution-scoped
  qualification, InvocationAuthorization, consequence class,
  experimental/governed boundary.
- Slice D, lineage and evidence admission: effective-input ancestry,
  pre-provenance inheritance, EvidenceAdmissionDecision, conservative
  independence statuses.


=== QUESTIONS ===
1. Does the scope stay inside the Slice B boundary, and does anything in it belong to Slice C or D?
2. The plan resolves invocations by append-only annotation and never mutates captured records. Construct a case where this is insufficient: a situation where an annotation-only design leaves a consumer with a materially misleading picture.
3. The temporal rule requires the snapshot to be observed no later than the invocation. Name a legitimate case this rule wrongly excludes, if one exists, and say whether excluding it is the right trade.
4. The validator forbids a provider_self_report capture from carrying content evidence stronger than self_asserted. Construct a way to satisfy that rule while still conveying false confidence to a downstream reader.
5. Which decisions in this slice constrain Slice D's independence assessment, and how?
6. Are the success criteria mechanically checkable? Name any that is not, and any missing check.
7. Recommendation: admit as written, admit with named conditions (state them), or revise first.

Do not certify or praise. No provider product recommendations.

## OpenAI Response

- model: `gpt-5`

```
Here are answers, grounded only in the texts you provided.

1) Slice boundary check

- Stays in Slice B:
  - The scope items are squarely “catalog identity resolution”: ModelIdentity, ServiceEndpointIdentity, atomic CatalogAssertions in CatalogSnapshots, CatalogCapture with two status fields, a pure resolution function with explicit non-resolution reasons, a freshness validator using the shared verification-outcome vocabulary (for channel and freshness only), append-only IdentityResolution annotations, predicate-registry entries, opt-in live capture with recorded fixtures, and tests. These match ABS-0004 v5 Sections 4.2–4.4 and Section 10’s “Slice B, catalog identity resolution: ModelIdentity, ServiceEndpointIdentity, atomic assertions in snapshots, requested-name to resolved-identity linkage, freshness/verification validator.”
- Not Slice C:
  - The plan’s non-goals explicitly exclude “RoleDefinition, RoleQualification, InvocationAuthorization, or consequence classes (Slice C).”
- Not Slice D:
  - The plan’s non-goals explicitly exclude “Lineage traversal, independence assessment, or evidence-admission enforcement (Slice D).”
  - Resolution is “append-only annotation” and “captured invocation records are never mutated,” which fits B’s linkage, not D’s lineage/evidence admission.
- Conclusion: Inside Slice B, with C and D explicitly excluded.

2) Where annotation-only can mislead a consumer

Constructed cases consistent with the plan’s constraints and non-goals:

- Under-counting resolution by ignoring annotations:
  - Slice A records keep “identity_verification_status unresolved … with no mechanism to discharge it” until Slice B annotations exist. Because “captured invocation records are never mutated,” a consumer who only reads the InvocationRecord (not the IdentityResolution annotation) will conclude the identity remained unresolved, despite a later, valid annotation resolving it. The plan relies on “append-only annotation … InvocationRecord file is byte-identical before and after,” so a reader that does not join annotations gets a materially misleading picture (believing “unresolved” when it is resolved).
- Believing a superseded resolution:
  - The plan’s non-goals say “supersession is recorded, not retroactively applied.” If an early annotation resolves to M1 from a self-asserted snapshot, and later a contradictory capture arrives (e.g., ambiguity found or a corrected assertion) yielding a different resolution or a non-resolution, a consumer that cached or prefers the first annotation and does not process the later supersession record can keep believing M1. Annotation-only plus “supersession … not retroactively applied” enables this divergence in downstream interpretation.

3) Legitimate case the temporal rule excludes, and is that the right trade?

- The plan states the mitigation and rule: “the temporal rule requires the snapshot to precede the invocation, so a later snapshot can never retroactively verify an earlier call” and resolution “mapping … to … explicit non-resolution reason … snapshot observed after the invocation.”
- Legitimate case excluded:
  - A provider’s alias-to-identity mapping is stable across a window that spans the invocation, but you only captured the snapshot shortly after the invocation. Even though the content accurately describes the invocation-time mapping, it was “observed after the invocation,” so the plan will return a non-resolution reason rather than resolve.
- Is excluding it the right trade?
  - Given P6 (“Naming may not exceed evidence … a later snapshot can never retroactively verify an earlier call”) and the plan’s mitigation goal “ambiguity blocks resolution rather than picking a winner,” this is the conservative, honest trade the plan intends. If admitting certain retroactive proofs (e.g., future ABS extensions) is ever desired, “deviations require an ABS revision first,” so changing this would need an ABS change, not a plan-side relaxation.

4) How to satisfy the provider_self_report rule yet still convey false confidence

- The adopted constraint says: “A capture whose source_type is provider_self_report may never record a content-evidence status implying independent confirmation.” The plan enforces this in validation: “the validator rejects a CatalogCapture whose source_type is provider_self_report and whose content_evidence_status is independently_corroborated, and accepts the same capture with self_asserted.”
- Still, a downstream reader can be misled if:
  - You present only the “channel_authentication_status” (from the shared verification-outcome vocabulary) as a green ‘verified’ badge, while keeping “content_evidence_status self_asserted.” This obeys “may never be merged” and the validator rule, yet a UI or report that highlights verified_current channel status next to a “resolved_to” line can give the impression that the content was independently verified.
  - You publish summaries or dashboards that omit the content_evidence_status column entirely, showing only “resolved_to Mx” and “channel_authentication_status verified_current.” This satisfies the field-level rules but can still convey false confidence because consumers “read the label, not the caveat,” per P6.

5) Decisions here that constrain Slice D’s independence assessment

- From plan risk: “Resolution semantics decided here determine what identity independence can mean in Slice D: if resolution is loose, C3’s per-kind equivalence check inherits the looseness. A permissive freshness window would let stale assertions discharge unresolved statuses that should remain open.” Thus:
  - Strict temporal bound (snapshot must be “observed no later than the invocation”) forces D to only treat identities as established when contemporaneously evidenced; no retroactive upgrades.
  - Ambiguity handling (“ambiguity blocks resolution rather than picking a winner”) means D cannot assume equivalence; it must treat ambiguous mappings as non-equivalent/not independently established.
  - Evidence-class separation and the adopted constraint on provider_self_report mean D must not treat self-asserted captures as independent confirmation.
  - Append-only annotation and “no automatic re-resolution … supersession is recorded, not retroactively applied” mean D must reason over possibly multiple annotations and explicit supersessions, not a single mutable ‘truth.’
- From ABS-0004 v5 Section 4.2: “The same ModelIdentity served through different endpoints may differ … endpoint diversity never implies model independence.” D must not infer independence from endpoint differences.
- From ABS-0004 v5 Section 4.3: “An invocation records the most precise ModelIdentity establishable at execution time; unresolved requested names are recorded as unresolved, never silently substituted.” D inherits that unresolved requested names are not quietly upgraded; independence checks cannot rest on silent substitutions.
- From scope: “Atomic assertions only.” D can rely on per-claim granularity; independence logic should not assume cross-claim packaging.

6) Mechanical checkability of success criteria; gaps

Mechanically checkable:
- Resolution round-trip with byte-identical InvocationRecord afterward.
- Explicit fixtures for each non-resolution reason, including “snapshot observed after the invocation” and “expired freshness window.”
- Validator rejects/accepts provider_self_report depending on content_evidence_status.
- Atomic assertion rejection.
- “content_evidence_status never takes a verification-outcome value.”
- “full suite passes offline” and live path disabled by default.

Not fully mechanically checkable as written:
- “The repository audit remains ok true verified_current, and cross-environment reproduction from the public repository succeeds byte-identically.” This depends on an external audit tool and cross-environment reproducibility beyond unit tests.

Missing or under-specified checks to add:
- Enforce relation shape and predicate registry:
  - A test that “All relations use the GraphRelation shape; no predicate outside the registered Slice A and Slice B lists,” verifying only the four new predicates (“resolved_to, asserted_by, concerns, captured”) appear, and no parallel edge vocabulary is used.
- Independence of the two status fields:
  - A test that changes in channel_authentication_status do not alter or default content_evidence_status, and vice versa, satisfying “may never be merged, defaulted … or derived from one another.”
- Evidence-class inheritance in annotations:
  - A test that IdentityResolution annotations “carry … the evidence class inherited from the capture,” as specified in scope.
- Freshness window explicitness:
  - Define the freshness window parameter and add boundary-condition tests (exactly on the cutoff, just inside/outside).
- Canonical serialization determinism:
  - Tests that canonical serialization of catalog records and annotations is stable across runs and environments (datetime formatting, field order), supporting “deterministic identity and path rules” and the “content_digest” stability.
- Guardrail for Slice A invariance:
  - A regression test that a stored Slice A InvocationRecord from before Slice B remains byte-identical when revalidated/loaded under the new code, fulfilling “Slice A behavior is unchanged.”

7) Recommendation

Admit with named conditions:

- Add tests enforcing the GraphRelation shape and that only registered Slice A/B predicates are used.
- Add tests demonstrating the independence of channel_authentication_status and content_evidence_status (no merging/defaulting/derivation).
- Add a test that IdentityResolution annotations include the evidence class inherited from the underlying CatalogCapture.
- Specify the freshness window (value and unit) and add edge-case tests; ensure the “expired freshness window” non-resolution reason is parameterized and documented.
- Add canonical-serialization determinism tests for catalog records and annotations, including stable content_digest computation.
- Add a regression test proving Slice A invocation records are unaffected (byte-identical) by Slice B code paths when no annotations are applied.
- Treat the “repository audit … verified_current, cross-environment reproduction … byte-identically” as a post-admission operational check; do not gate admission on environment-dependent audit results.

With these conditions, the plan remains inside Slice B, preserves the honesty constraints in ABS-0004 v5 (including P6 and the provider_self_report rule), and closes the review’s mechanical gaps.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
## Admission Review: PLAN-20260723-0001

### 1. Slice Boundary Compliance

**Stays inside Slice B:** Yes, with one clarification needed.

The scope adheres to the ABS-0004 v5 Section 10 Slice B definition: "catalog identity resolution: ModelIdentity, ServiceEndpointIdentity, atomic assertions in snapshots, requested-name to resolved-identity linkage, freshness/verification validator."

**Boundary observation:**
- The plan explicitly excludes "RoleDefinition, RoleQualification, InvocationAuthorization, or consequence classes (Slice C)"
- It excludes "Lineage traversal, independence assessment, or evidence-admission enforcement (Slice D)"
- The IdentityResolution annotation record carries "the evidence class inherited from the capture"—this is metadata passthrough, not assessment, staying in Slice B

**Missing clarification:** The scope states the annotation record has "the evidence class inherited from the capture" but does not specify whether the resolution function performs any validation that the evidence class permits the resolution to be used. The constraints require "no consumer that gates a decision on resolution results," which implies the resolver itself does not gate, but the interaction between `content_evidence_status` passthrough and the "explicit non-resolution reason" vocabulary could be clearer. If a snapshot has `content_evidence_status: contradicted`, does resolution proceed mechanically or is contradiction a fifth non-resolution reason?

### 2. Annotation-Only Insufficiency Case

**Construction of materially misleading scenario:**

Time T0: Provider catalog asserts `(api-name-X, resolves_to, model-Y-v1)`  
Time T1: InvocationRecord captures request for `api-name-X`, `identity_verification_status: unresolved`  
Time T2: Catalog snapshot captured, assertion observed, `channel_authentication_status: ok`  
Time T3: Resolution function runs, produces IdentityResolution annotation: `resolved_identity: model-Y-v1`, references snapshot from T2  
Time T4: Provider silently substitutes model-Y-v2 for all `api-name-X` requests; catalog not yet updated  
Time T5: Consumer reads InvocationRecord from T1, sees IdentityResolution annotation pointing to model-Y-v1

**The misleading picture:** The consumer believes the T1 invocation used model-Y-v1 because the resolution annotation says so, but the provider had already switched to v2. The InvocationRecord is byte-identical and immutable. The annotation is append-only. No subsequent catalog capture that records the substitution at T4 retroactively corrects the T3 annotation, per the explicit non-goal: "Automatic re-resolution of previously annotated invocations when catalogs change; supersession is recorded, not retroactively applied."

**Is this insufficient?** Not necessarily. The design is honest to its evidence: at T3, the best available evidence said model-Y-v1. The T4 substitution is not detectable from catalog alone if the provider does not update the catalog. The insufficiency, if any, is not in the annotation-only design but in the evidence source: `provider_self_report` with `content_evidence_status: self_asserted`. The plan's mitigation explicitly accepts this: "no claim of independent verification of catalog content while the only source is provider self-report."

**Judgment:** The scenario exists, but annotation-only is not the cause. Mutation would not fix it either—re-resolving historical invocations with new catalog data would create revisionist history. The plan's append-only design is sufficient to its stated scope: making identity claims *representable and datable*, not making them continuously current.

### 3. Temporal Rule Exclusion

**Rule:** "The temporal rule requires the snapshot to precede the invocation, so a later snapshot can never retroactively verify an earlier call."

**Legitimate case wrongly excluded:**

Time T1: InvocationRecord created, `occurred_at: T1`, `identity_verification_status: unresolved`  
Time T2: Catalog snapshot captured, contains assertion `(api-name-X, resolves_to, model-Y)` with `valid_from: T0`, `valid_until: T3` (T0 < T1 < T2 < T3)  
The assertion was *valid at T1* and the catalog claim states it applied then, but the snapshot was *observed at T2*, after the invocation.

**Is exclusion correct?** Yes. The plan's rationale is explicit: "temporal bounding... separation of what the channel proves from what the content claims" (from COMP-0035 convergence). The snapshot observation date bounds what the resolver can rely on. The assertion's `valid_from: T0` is a provider claim; the snapshot's `observed_at: T2` is the capture fact. Allowing T2 > T1 resolution would reintroduce the circularity P6 forbids: treating the provider's claim about validity windows as if it were independent evidence.

The rule excludes a legitimate *claim* but rightly refuses to treat a later observation as evidence for an earlier state. The alternative—trusting `valid_from` timestamps from `provider_self_report` sources—would let providers retroactively verify past invocations by asserting backdated validity windows, which is exactly the "retroactively verify" hole the rule closes.

**Missing case:** The rule does not address snapshot at T1 with assertion observed at T1 but invocation `occurred_at` has millisecond precision placing it fractionally before the snapshot. The scope requires "deterministic identity and path rules under docs/catalog/" but does not specify the resolution of timestamp precision for the precedence check. This should be documented.

### 4. False Confidence Construction Under Validator Rule

**Rule:** A `source_type: provider_self_report` capture may never have `content_evidence_status` stronger than `self_asserted`.

**Construction:**

```json
{
  "capture_id": "...",
  "source_type": "provider_self_report",
  "channel_authentication_status": "ok_verified_current",
  "content_evidence_status": "self_asserted",
  "captured_at": "2026-07-20T00:00:00Z",
  "capture_success": true
}
```

The validator accepts this. A downstream reader sees:
- `channel_authentication_status: ok_verified_current` (strong)
- `capture_success: true`
- A recent capture timestamp
- `content_evidence_status: self_asserted` (correctly weak, but may be skimmed over)

**False confidence vector:** The reader conflates "we verified the channel" with "the content is verified" because both status fields are present and one is strong. The field names are technical (`channel_authentication_status` vs. `content_evidence_status`), and a skimming reader sees "status: ok verified" adjacent to "capture success: true" and infers content verification.

**Mitigation in plan:** The plan states "the two independently scoped status fields that must never be merged, defaulted from one another, or derived from one another" and requires documentation in `CATALOG_RECORDS.md` of "the evidence-class separation." The freshness validator "uses the shared verification-outcome vocabulary for channel authentication and freshness only, never for content evidence."

**Remaining risk:** Documentation and field naming are defenses, but a programmatic consumer might still log or display "catalog verified" based on `channel_authentication_status` alone. The plan's scope includes "canonical serialization" but does not specify whether that serialization orders the fields, groups them, or includes inline documentation. If the JSON serialization places `channel_authentication_status: ok_verified_current` immediately before `content_evidence_status: self_asserted`, the juxtaposition is self-correcting. If it separates them, the risk increases.

**Recommendation:** The scope should require the canonical serialization to place the two status fields adjacently in the fixed order `content_evidence_status` first, `channel_authentication_status` second, so that any display of channel strength is preceded by the content-evidence weakness.

### 5. Slice D Independence Assessment Constraints

**Decisions that constrain Slice D:**

**a) Identity-resolution semantics (scope item 4):**
The resolution function is "pure over stored snapshots, mapping (service_endpoint, requested_model_name, occurred_at) to a ModelIdentity." Slice D's independence assessment must determine whether two invocations used independent models. If Slice B's resolution is loose (e.g., treats `model-X-v1` and `model-X-v1-turbo` as the same `ModelIdentity`), Slice D inherits that granularity. The plan acknowledges this: "if resolution is loose, C3's per-kind equivalence check inherits the looseness."

**b) Assertion atomicity (scope item 2, constraint in plan):**
"Atomic assertions only: one claim per assertion." Slice D's evidence-admission rules must work over atomic assertions. If a later proposal wants to admit compound evidence (e.g., "model X trained on corpus Y in jurisdiction Z"), it must either decompose into atomic assertions at capture time or Slice D must handle heterogeneity, but this slice forecloses heterogeneity.

**c) Evidence-class vocabulary (ABS-0004 v5 Section 4.4):**
The `content_evidence_status` values are `self_asserted`, `independently_corroborated`, `contradicted`, `unassessed`. Slice D's independence assessment must use this vocabulary. If Slice D wants a finer-grained distinction (e.g., `corroborated_by_primary_source` vs. `corroborated_by_third_party`), it requires either a Slice B revision or a separate evidence-quality layer.

**d) Temporal rule (scope item 4, mitigation, risk):**
"The snapshot must precede the invocation." Slice D cannot retroactively promote an invocation's independence status when a later catalog capture provides better evidence. The constraint "supersession is recorded, not retroactively applied" propagates to Slice D: if a later snapshot contradicts an earlier one, Slice D's ancestry traversal sees the contradiction as metadata but cannot revise the earlier invocation's resolution.

**e) Non-resolution reasons (scope item 4):**
The explicit enumeration "no applicable assertion, snapshot observed after the invocation, ambiguous multiple applicable assertions, or expired freshness window" becomes the vocabulary for Slice D's lineage traversal. If an invocation's identity is unresolved due to ambiguity, Slice D must treat that ambiguity as non-independent (cannot prove independence without identity), but the plan does not state this implication. Slice D must define the semantics.

**f) Freshness window (scope item 6, risk):**
"A permissive freshness window would let stale assertions discharge unresolved statuses that should remain open." Slice D's independence assessment over time depends on what "fresh" means here. If the freshness validator accepts a 90-day-old snapshot for today's invocation, Slice D inherits that staleness into its independence conclusions. The plan defers the freshness-window parameter: scope item 6 says "freshness validator reporting... currency" but does not set the window.

### 6. Success Criteria Mechanical Checkability

**Mechanically checkable:**
1. ✓ "InvocationRecord file is byte-identical before and after" — `diff` or hash comparison
2. ✓ "Each non-resolution reason is exercised by a fixture" — test suite confirms four fixtures, each asserting a distinct reason
3. ✓ "Validator rejects... source_type provider_self_report and content_evidence_status independently_corroborated, and accepts... self_asserted" — two assertions in validator test
4. ✓ "Assertions are atomic: a record carrying two claims is rejected" — validator test with multi-claim fixture
5. ✓ "Freshness reporting uses the shared verification-outcome vocabulary... content_evidence_status never takes a verification-outcome value" — test asserts value-set disjointness
6. ✓ "Full suite passes offline with no network access" — CI run with network-disabled environment
7. ✓ "Repository audit remains ok true verified_current, and cross-environment reproduction... byte-identically" — `scripts/audit_repository.py && scripts/reproduce_in_clean_env.sh`

**Not mechanically checkable:**
**Criterion 1:** "resolves to a ModelIdentity through the pure resolution function using a stored snapshot, producing an append-only IdentityResolution annotation."

The "append-only" property is checkable (no mutation), but "pure... using a stored snapshot" requires inspection that the resolution function's inputs are only the snapshot and the invocation record, with no environment reads, no network calls, no current-time dependencies beyond `resolution_timestamp`. The test can invoke the function with mocked time and verify no external calls, but confirming purity across the entire implementation requires either property-based testing (e.g., repeated calls with same inputs yield same output) or code review. The plan's scope states "pure over stored snapshots" but the success criteria do not operationalize it beyond the integration fixture.

**Missing checks:**
- **Scope item 1:** "deterministic identity and path rules under docs/catalog/" — no criterion confirms determinism (same inputs → same ID and path)
- **Scope item 2:** "assertion_subject, assertion_predicate, assertion_value_or_target, unit, scope, valid_from, valid_until or superseded, and source" — no criterion checks all fields are present and validated
- **Scope item 3:** "the two independently scoped status fields; the validator rejects..." — criterion 3 checks the rejection but not the independence (that defaulting from one to the other is impossible)
- **Scope item 7:** "predicate-registry entries for the Slice B predicates: resolved_to, asserted_by, concerns, and captured" — no criterion checks these four entries exist and are valid
- **Scope item 8:** "recorded fixtures of real catalog payloads for offline tests" — no criterion confirms the fixtures are real payloads (as opposed to synthetic ones) or that they include capture metadata

### 7. Recommendation

**Admit with the following named conditions:**

**Condition 1 (Contradiction Handling):** The scope must specify whether a snapshot whose assertions have `content_evidence_status: contradicted` produces a fifth non-resolution reason ("contradicted assertion") or whether contradiction is ignored and resolution proceeds mechanically. The current four reasons do not include contradiction. This must be resolved before implementation to avoid the Slice B resolver making an implicit Slice D decision about evidence admissibility.

**Condition 2 (Canonical Serialization Order):** The scope's "canonical serialization" requirement must specify that `content_evidence_status` and `channel_authentication_status` appear adjacently in the output, with `content_evidence_status` first, to prevent readers from conflating channel authentication with content verification. This directly serves the plan's mitigation commitment to evidence-class separation.

**Condition 3 (Purity Operationalization):** Add a success criterion: "The resolution function is deterministic: repeated calls with the same (snapshot, invocation record) inputs produce byte-identical IdentityResolution outputs (modulo resolution_timestamp), confirmed by property-based test fixture with 100 iterations."

**Condition 4 (Missing Success Criteria):** Add criteria for:
- Deterministic identity and path generation (same inputs → same snapshot_id, assertion_id, capture_id)
- All CatalogAssertion fields validated (validator test rejects records missing each required field)
- Predicate-registry entries present and valid for `resolved_to`, `asserted_by`, `concerns`, `captured`
- Recorded fixtures include at least one real provider payload (not synthetic) with capture metadata

**Condition 5 (Timestamp Precision Documentation):** The "deterministic identity and path rules under docs/catalog/" must document the timestamp precision used for the temporal precedence check (snapshot observed_at ≤ invocation occurred_at) and specify tie-breaking if both timestamps resolve to the same precision boundary.

**Condition 6 (Freshness Window Declaration):** The plan defers the freshness-window parameter, but the risk section notes this decision constrains Slice D. Before admission, the plan must either (a) declare a specific freshness window (e.g., 7 days, 30 days) or (b) make the window a documented configuration parameter with a stated default and require the success criteria to test both acceptance and rejection across the boundary.

**Rationale for conditions rather than revision:** The plan is substantively sound. The slice boundary is respected, the constraints are adopted, the evidence-class separation is principled, and the append-only design is justified. The conditions address operationalization gaps and documentation precision, not design defects. Requiring a full revision would delay Slice B while GAP-0005 remains open, and the plan's "honest evidence classing" objective is already served by the structure. The conditions are individually small, mechanically addressable, and do not alter the scope's intended boundaries.

---

**No certification. No product recommendations. Operator adjudication required.**
````
