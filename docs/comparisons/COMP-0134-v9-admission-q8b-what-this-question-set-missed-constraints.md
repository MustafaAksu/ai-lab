# COMP-0134: Provider Comparison — v9 admission Q8b what-this-question-set-missed-constraints

## Metadata

- comparison_id: `COMP-0134`
- title: `v9 admission Q8b what-this-question-set-missed-constraints`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-508904a7fc9ff0ff.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0134", "target_id": "INV-508904a7fc9ff0ff"}, {"authoritative": false, "evidence": "docs/invocations/INV-80eec14c815c4cf1.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0134", "target_id": "INV-80eec14c815c4cf1"}]`
- created_at: `2026-08-10T10:38:43.265427+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q8b what-this-question-set-missed-constraints You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9 is proposed and not admitted. v4 is the last version with an admission event. v9 has no governance force.

Disclosures, because withholding them would be dishonest rather than isolating:

1. v9 is a RECONSTRUCTION, not an amendment. v5 through v8 were withdrawn. v9 was built from the admitted v4 text plus a ledger of findings from five prior review rounds. Its Section 3 is 1.48 times the size of v4's; v8 had grown it 7.5 times.

2. v8 was withdrawn because it carried 24 constraints tagged with a category the document defines as "constraint adopted now" while itself marked proposed. v9's answer is a new tag, [INHERITED_CONSTRAINT]. Whether that answer works is what this round is for. Do not assume it does because it was adopted in response to a finding.

3. The executor that drafted v9 is not the executor that wrote these questions. The question author drafted v5 through v8, all withdrawn. Its priors about what to probe are shaped by four failed attempts.

4. Both prior question sets were written by the party whose text was under review, and both missed defects a third reader found. This one is not, but see 3.

5. Reviewer independence is unresolved. The executor that drafted v9 self-reports as gpt-5.6-thinking. One of the two reviewer slots in this round is gpt-5.6-terra. The provider's own catalog asserts those are distinct model identities, and that catalog is itself a provider self-report. Nothing establishes that the drafter and this reviewer are different executors, and nothing establishes that they are the same.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: if you need a section, constraint or record that is not present, name it and say what you would have used it for. That report is wanted output.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q8b ===
The eight questions in this round were written by the executor that drafted v5, v6, v7 and v8, every one of which was withdrawn or superseded. It drafted none of v9.

YOU ARE SEEING PART OF THE DOCUMENT. Below are Sections 5 through 13: canonical relations, epistemic constraints, legacy and phase-in, consequence classes, the enforcement matrix, the implementation sequence, deferred definitions, open questions, and the challenge-round questions. The metadata and Sections 1 through 4 are being reviewed by the same question in a separate call. The whole document did not fit in one call. Say so if the split prevents you from answering.

Read what you can see as though no review round had happened. Find what is weakest in it. Then report anything significant that this question set does not ask about, and anything that is unsound rather than merely incomplete.

Pay particular attention to the enforcement matrix: it records for each constraint whether it is evidenced, and it is the one place the document states its own enforcement status in a form a reader can check against the rest.

=== EVIDENCE ABS-0004 v9, Sections 5 to 13 (of 13) ===
## 5. Canonical Relations

`[INHERITED_CONSTRAINT]` All relations use the `GraphRelation` shape of
`ai_lab/documentation/graph_neighborhood.py`. No parallel edge vocabulary.

`[PROPOSED_CONSTRAINT]` A predicate registry is a required artifact of the
first implementation: per predicate, source type, target type, exact
meaning, cardinality, inverse, temporal semantics, transitivity, evidence
requirements, authoritative-default behavior.

Candidate Slice A predicates:

    artifact produced_by invocation
    invocation executed_by executor_identity
    invocation requested_via service_endpoint
    invocation used_execution_profile execution_profile
    invocation used_inputs effective_input_manifest
    invocation member_of session
    invocation spawned invocation

Candidate Slice B predicates:

    invocation resolved_to model_identity
    catalog_assertion asserted_by provider_organization
    catalog_assertion concerns catalog_entity
    catalog_verification verifies catalog_assertion

Notes: `executed_with` is dropped (duplicated `executed_by`); alias
resolution is `resolved_to`; `describes` was replaced by `concerns`
because an atomic assertion does not always concern a ModelIdentity;
catalog reliance attaches to selection and authorization events
(`routing_decision relied_on catalog_snapshot`, `authorization relied_on
role_qualification`), not to the invocation. Predicate clarifications from
COMP-0032: `spawned` is the sole subordinate-execution predicate for all
executor kinds; `called` is dropped as an undefined duplicate.
`resolved_to` is exclusively the invocation-level runtime resolution edge,
valid as of `occurred_at`; catalog alias resolution is data inside an
assertion (`assertion_predicate: resolves_to`), never a graph edge, so the
two resolution concepts cannot be conflated by implementations.
`used_inputs` targets exactly one EffectiveInputManifest (never individual
artifacts directly); the manifest carries a `completeness_attestation`
field stating whether it is declared exhaustive for all effective-input
channels, and blind-witness qualification requires that attestation.
`concerns` target types are constrained per assertion_predicate in the
predicate registry.

Full vocabulary (defined now, wired later): `used_prompt`,
`continued_from` (session/execution continuity only), the derivation family
`transformed_from` (mechanical/structural), `claim_derived_from` (epistemic
dependence), `copied_from` (direct inheritance), `summarized_from` (lossy
representation); `assigned_role`; `authorized_by`/`authorizes`;
`admitted_by`; routing predicates; `decision issued_by invocation`;
`decision approved_by accountable_principal`; `decision evaluates
claim_or_artifact`; `invocation verified_by invocation` (targets a
VerificationRun-bearing invocation); `evaluation_outcome observed_for
executor_identity`; the reified role-qualification predicates (4.6);
`tool_identity uses_executor executor_identity`.

`[DEF]` Status assignment is a field on DecisionRecord
(`recommended_status`, `effective_status`), not a graph edge: a literal
cannot be a `GraphRelation` target. Adjudication is represented through
DecisionRecords, never a direct `adjudicated` edge.

## 6. Epistemic Constraints

`[PROPOSED_CONSTRAINT]` C1 Staged provenance completeness. Provenance
profiles activate in stages; a governed output created after activation of
the applicable profile is admissible only if it satisfies that profile:
provenance_v1 (producing invocation; executor identity;
EffectiveInputManifest; session-state mode; ExecutionProfile; output
record; timestamps; model-specific identity and catalog fields required
only when a model participated as executor or execution resource);
authorization_v1 (role assignment, qualification, consequence class,
invocation authorization); lineage_v1 (input/claim ancestry and
independence assessment).

`[PROPOSED_CONSTRAINT]` C2 Catalog admission: an execution candidate
(executor within a qualification's execution scope, 4.6) may serve a
governed role only when the role's required catalog claims are satisfied at
the role's freshness requirements. Experimental execution is permitted;
experimental outputs cannot silently enter governed evidence.

`[INHERITED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
invocation cannot adjudicate a claim whose evidence ancestry contains an
invocation by an equivalent executor identity, with equivalence defined
per executor kind: ModelIdentity resolution equality for models;
tool identity and version equality for tools; principal equality for
humans. Direct lineage conflict: hard prohibition, no exception.
Equivalent-identity conflict: hard prohibition absent a future explicitly
governed exceptional procedure. Unknown or unresolved executor equivalence
cannot establish identity independence; it yields
`independence_unresolved`, never an independent path. An identity
unresolved at one endpoint and resolved at another is treated as distinct
until equivalence is affirmatively established; distinctness never
increases independence (P5).

`[PROPOSED_CONSTRAINT]` C4 No hidden witness reuse: an invocation that
consumed another witness's output is not an independent confirmation of
that testimony; it may count as synthesis or critique.

`[PROPOSED_CONSTRAINT]` C5 Lineage-based independence. Isolation from other
witness outputs is necessary for counting an invocation as independent
confirmation of those outputs, but not sufficient for witness-path
independence: shared erroneous sources, common leading prompts, shared
hidden state, and shared unsupported assumptions defeat it. Round labels
describe protocol; lineage determines admissibility. Independence is
assessed per dimension (information path, source, executor identity,
provider/organization correlation, prompt common cause, session-state
confidence, claim-lineage completeness), some of which are hard
disqualifiers. First implementations produce categorical statuses
(`qualified_independent` | `dependent` | `unresolved`) with
dimension-specific reasons; no single numeric score, and no claimed weight
function without evaluation evidence. Provider similarity is recorded as a
correlation factor.

`[INHERITED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another. Assignment independence
is not exercise license: adjudicator-level epistemic authority and
above-read_only action authority may not both be exercised within a single
invocation against the same target unless the adjudication is covered by
an independent verification edge; an invocation that mutates state it also
adjudicates collapses the separation C6 exists to preserve. COMP-0032
produced two constructions satisfying the axis definitions while defeating
separation; this sentence closes both.

`[LIMITATION]` Role, qualification, and authorization records are inputs to a
C6 evaluation. Their existence does not establish that the C6 exercise
restriction was evaluated or satisfied for a particular invocation.

`[INHERITED_CONSTRAINT]` C7 Implementation separation: an executor with
repository or external action authority may implement an admitted plan but
may not be the sole verifier or adjudicator of its own changes.

`[PROPOSED_CONSTRAINT]` C8 Decision traceability: every policy-selected
invocation has a reconstructible RoutingDecision or a governed
manual-override DecisionRecord (accountable principal, reason, scope,
review condition; never a free-text escape hatch).

`[INHERITED_CONSTRAINT]` C9 Conservative lineage inheritance (from P3): an
artifact grounded in pre-provenance or lineage-incomplete material inherits
`claim_lineage_status: source_lineage_partial` while recording
`source_provenance_status` of its sources (for example `pre_provenance`).
Structural transformation, including extraction, cannot improve the
provenance class of the information transformed. Extraction from
pre-provenance sources is permitted; its outputs carry
`source_provenance_status: pre_provenance`, `claim_lineage_status:
source_lineage_partial`, `independent_observation: false`.

Selection provenance (COMP-0032 finding): an invocation's effective inputs
include the selection criteria and priors used to choose its sources.
Undisclosed selection priors derived from pre-provenance or
lineage-incomplete material taint the selection even when every selected
source is independently clean; at high consequence, claims whose source
selection lacks disclosed selection provenance carry `claim_lineage_status:
source_lineage_partial`. Honest limitation: offline human reading is
unobservable, so this rule is only partially enforceable ever;
HumanActionRecord (Section 11) narrows but cannot close the gap, and the
ontology states this rather than pretending otherwise.

`[INHERITED_CONSTRAINT]` C11 Interim independence disclosure: until
claim-level lineage exists, witness-path independence counts are
artifact-level approximations, and both COMP-0032 witnesses independently
identified the resulting silent failure mode (N "independent" paths
satisfied by N copies of one unrecorded shared claim). Therefore any
high-consequence decision relying on a minimum number of independent
witness paths must disclose in its DecisionRecord that independence was
assessed at artifact level only, and must name the compensating controls
relied on (operator adjudication, source disclosure, deterministic
verification of the claims where available). Absent that disclosure, the
independence requirement is unmet, not silently satisfied.

`[INHERITED_CONSTRAINT]` C10 Validator lineage independence (property-scoped
P2 hardening): verifier provenance (identity, version, rule/test version,
inputs, environment, result) is always recorded. When the code, schema,
tests, or configuration driving a verification share evidence ancestry
with the ModelIdentity that produced the output under test, the
verification is marked `verifier_lineage: self_authored` and carries
reduced independence standing; the verified property claim stands only as
far as the verifier's scope and lineage permit. At high consequence,
admission requires either independently-lineaged verification or
independent review of the verifier. Self-authored verification is
governed, not prohibited: AI-Lab's existing compensating controls
(cross-environment reproduction, operator adjudication, provider
completion review) are recognized independent paths.

## 7. Legacy and Phase-In

`[DEF]` Provenance statuses: provenance_complete | provenance_partial |
pre_provenance | provenance_conflicted. Claim-lineage statuses include
source_lineage_partial. These describe provenance condition, never truth.

`[INHERITED_CONSTRAINT]` Historical standing is distinct from prospective
evidentiary use. Pre-provenance artifacts (including the GAP-0003/0004
closure chains) retain historical governance status in full. Prospective
reuse requires disclosure of missing provenance and may trigger
corroboration, reduced independence standing, or exclusion by receiving
role and consequence class. Grandfathering into full independent-evidence
standing is prohibited. The known laundering path (legacy claim, cleanly
produced summary, blind witness, apparent fresh corroboration) is defeated
by C9: the summary inherits the lineage limitation and any witness
confirmation of it is `dependent` on a lineage-partial path.

## 8. Consequence Classes

`[DEF]` Ordinal classes (low | medium | high), not numbers.
`default_consequence` derives from target type (gap closure, plan
admission: high; comparison/synthesis: medium; extraction/classification:
low). `effective_consequence = max(default_consequence,
applicable_modifier_levels)`; modifiers (repository mutation, external side
effect, irreversibility, warrant/capability status change,
security/privacy/legal/financial impact) only raise. `[INHERITED_CONSTRAINT]`
Downward adjustment is a separate governed exception (reason, accountable
principal, scope, evidence, expiry/review) and can never override hard
prohibitions such as disqualifying lineage conflicts. `[OPEN]` Detailed
classification function.

## 9. Enforcement Matrix

`[DEF]` Normative state: proposed | adopted-manual | machine-enforced.
Representability: none | partial | full. Manual enforcement counts only
when the check leaves a named artifact; the claim that a check happens is
not evidence. Capability dependencies replace slice numbers until admitted
plans exist.

| Constraint | Normative state | Representability | Current enforcement evidence | Target enforcement | Activation condition | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
| C1 staged provenance | proposed | none | none | validator per profile | profile activation decision after capability ships | invocation records; manifests; profiles |
| C2 catalog admission | proposed | none | none | validator + runtime gate | catalog capability ships | catalog snapshots; identities; qualifications |
| C3 no self-adjudication (executor-generic) | adopted-manual | partial | named attestation in completion warrants (for example WARR-20260719-0002 scope adjudications) | per-kind equivalence check + lineage traversal | already active manually | ancestry capture; executor-equivalence semantics |
| C4 hidden witness reuse | proposed | none | none | context-lineage inspection | lineage capability ships | manifests; ancestry |
| C5 lineage independence | proposed | none | none | categorical assessment with reasons | lineage capability ships | ancestry; claim lineage |
| C6 authority separation | adopted, not currently evidenced | partial | none (no current record names the check) | artifact validator | already practiced; evidence begins with role records | role records |
| C7 implementation separation | adopted-manual | partial | VERIFY records (cross-environment verification) | validator on VERIFY records | already active | none; strengthened later |
| C8 decision traceability | proposed | none | none | RoutingDecision validation | routing capability ships | routing records |
| C9 lineage inheritance | adopted-manual | partial | named disclosure statements in records | inheritance propagation | already active manually | claim lineage (full) |
| C10 validator lineage | adopted-manual | partial | verifier identity in VERIFY command records; independence via cross-environment and operator review | VerificationRun with verifier-ancestry check | already active manually | ancestry capture |
| C11 interim independence disclosure | adopted-manual | partial | disclosure statements in DecisionRecords/warrants | admission validator requiring disclosure + named controls | already active manually | none; retired when claim lineage ships |

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

## 11. Defined but Deferred

Run/ProtocolRound, Claim/EvidenceItem, RoutingPolicy and
AuthorizationPolicy enforcement, RoutingDecision enforcement,
VerificationRun and IndependenceAssessment record implementation,
OutboundInteractionLog (content-addressed declaration of a tool's external
interactions: network targets, external writes, privileged output
consumers; the enforcement object for external-interaction disclosure),
HumanActionRecord (audited human actions that shape effective inputs
without issuing a DecisionRecord; privacy-preserving, principal-referenced;
the partial enforcement object for selection provenance), formal
independence assessment beyond categorical statuses, automatic consequence
assignment, full ancestry enforcement, provider-diversity thresholds,
escalation, third-provider integration, session-mode cataloging per
provider API, endpoint mutable-property assertions.

## 12. Open Questions

`[OPEN]` Authorization-chain bootstrap (Section 3). `[OPEN]` Consequence
classification function and override taxonomy. `[OPEN]` Qualifying
witness-path thresholds per consequence class, including whether any
decision class requires paths constructible only with a third provider
(Gemini, DeepSeek, or similar), weighing integration cost, jurisdiction,
endpoint data governance. `[OPEN]` Session-state reconstructibility per
provider API. `[OPEN]` AccountablePrincipal contents and privacy-preserving
human decision records. `[OPEN]` EvaluationOutcome sufficiency per
authority level; who admits evaluators. `[OPEN]` ExecutorIdentity
superclass (reopened by COMP-0032 with the polymorphic-equivalence
argument). `[OPEN]` EvaluationOutcome typing: DecisionRecord kind, or
Claim/EvidenceItem with provenance; as defined it cannot carry lineage
into governed evidence. `[OPEN]` DecisionRecord: extend warrants or new
family; subtypes or one family. `[OPEN]` Per-provider escalation ladders: entirely
deferred to the post-ontology comparison with live catalog verification.

## 13. Challenge-Round Questions

1. Which objects are missing; which defined objects are category errors?
2. Which constraints are unenforceable as stated; what minimal
   representable form makes them enforceable?
3. Construct a concrete invocation satisfying the three-axis Role
   definitions while violating authority separation.
4. Construct a laundering path from a pre-provenance artifact into
   high-consequence independent evidence that survives C9 and C10.
5. Does candidate Slice A omit anything without which the provenance graph
   cannot later answer the witness-independence question?
6. Identify any predicate ambiguous enough to produce divergent
   implementations.
7. Where is invocation authorization represented; how is it distinguished
   from routing and evidence admission; does the distinction hold under
   composition?
8. Can the ontology represent one model served through different
   organizations, endpoints, regions, or mutable aliases without creating
   false model independence?
9. Does provenance as specified apply to claim derivation or only artifact
   production, and where exactly does the artifact-level approximation
   break?
10. What must an effective-input record contain before an invocation may be
    treated as blind?
11. Which constraints apply identically to models, tools, and humans; which
    require executor-specific rules?
12. Under what conditions, if any, can an unresolved model identity qualify
    as an independent witness path? Identify the failure behavior when
    equivalence cannot be resolved.
13. Construct a composite tool that satisfies the disclosure constraints'
    letter (4.7, both) while still exercising undeclared authority.
14. Construct a case where property-scoped verification (P2) plus validator
    lineage marking (C10) still admits a generator-authored blind spot into
    governed evidence.

Do not recommend specific provider products in this round.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9 is proposed and not admitted. v4 is the last version with an admission event. v9 has no governance force.

Disclosures, because withholding them would be dishonest rather than isolating:

1. v9 is a RECONSTRUCTION, not an amendment. v5 through v8 were withdrawn. v9 was built from the admitted v4 text plus a ledger of findings from five prior review rounds. Its Section 3 is 1.48 times the size of v4's; v8 had grown it 7.5 times.

2. v8 was withdrawn because it carried 24 constraints tagged with a category the document defines as "constraint adopted now" while itself marked proposed. v9's answer is a new tag, [INHERITED_CONSTRAINT]. Whether that answer works is what this round is for. Do not assume it does because it was adopted in response to a finding.

3. The executor that drafted v9 is not the executor that wrote these questions. The question author drafted v5 through v8, all withdrawn. Its priors about what to probe are shaped by four failed attempts.

4. Both prior question sets were written by the party whose text was under review, and both missed defects a third reader found. This one is not, but see 3.

5. Reviewer independence is unresolved. The executor that drafted v9 self-reports as gpt-5.6-thinking. One of the two reviewer slots in this round is gpt-5.6-terra. The provider's own catalog asserts those are distinct model identities, and that catalog is itself a provider self-report. Nothing establishes that the drafter and this reviewer are different executors, and nothing establishes that they are the same.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: if you need a section, constraint or record that is not present, name it and say what you would have used it for. That report is wanted output.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q8b ===
The eight questions in this round were written by the executor that drafted v5, v6, v7 and v8, every one of which was withdrawn or superseded. It drafted none of v9.

YOU ARE SEEING PART OF THE DOCUMENT. Below are Sections 5 through 13: canonical relations, epistemic constraints, legacy and phase-in, consequence classes, the enforcement matrix, the implementation sequence, deferred definitions, open questions, and the challenge-round questions. The metadata and Sections 1 through 4 are being reviewed by the same question in a separate call. The whole document did not fit in one call. Say so if the split prevents you from answering.

Read what you can see as though no review round had happened. Find what is weakest in it. Then report anything significant that this question set does not ask about, and anything that is unsound rather than merely incomplete.

Pay particular attention to the enforcement matrix: it records for each constraint whether it is evidenced, and it is the one place the document states its own enforcement status in a form a reader can check against the rest.

=== EVIDENCE ABS-0004 v9, Sections 5 to 13 (of 13) ===
## 5. Canonical Relations

`[INHERITED_CONSTRAINT]` All relations use the `GraphRelation` shape of
`ai_lab/documentation/graph_neighborhood.py`. No parallel edge vocabulary.

`[PROPOSED_CONSTRAINT]` A predicate registry is a required artifact of the
first implementation: per predicate, source type, target type, exact
meaning, cardinality, inverse, temporal semantics, transitivity, evidence
requirements, authoritative-default behavior.

Candidate Slice A predicates:

    artifact produced_by invocation
    invocation executed_by executor_identity
    invocation requested_via service_endpoint
    invocation used_execution_profile execution_profile
    invocation used_inputs effective_input_manifest
    invocation member_of session
    invocation spawned invocation

Candidate Slice B predicates:

    invocation resolved_to model_identity
    catalog_assertion asserted_by provider_organization
    catalog_assertion concerns catalog_entity
    catalog_verification verifies catalog_assertion

Notes: `executed_with` is dropped (duplicated `executed_by`); alias
resolution is `resolved_to`; `describes` was replaced by `concerns`
because an atomic assertion does not always concern a ModelIdentity;
catalog reliance attaches to selection and authorization events
(`routing_decision relied_on catalog_snapshot`, `authorization relied_on
role_qualification`), not to the invocation. Predicate clarifications from
COMP-0032: `spawned` is the sole subordinate-execution predicate for all
executor kinds; `called` is dropped as an undefined duplicate.
`resolved_to` is exclusively the invocation-level runtime resolution edge,
valid as of `occurred_at`; catalog alias resolution is data inside an
assertion (`assertion_predicate: resolves_to`), never a graph edge, so the
two resolution concepts cannot be conflated by implementations.
`used_inputs` targets exactly one EffectiveInputManifest (never individual
artifacts directly); the manifest carries a `completeness_attestation`
field stating whether it is declared exhaustive for all effective-input
channels, and blind-witness qualification requires that attestation.
`concerns` target types are constrained per assertion_predicate in the
predicate registry.

Full vocabulary (defined now, wired later): `used_prompt`,
`continued_from` (session/execution continuity only), the derivation family
`transformed_from` (mechanical/structural), `claim_derived_from` (epistemic
dependence), `copied_from` (direct inheritance), `summarized_from` (lossy
representation); `assigned_role`; `authorized_by`/`authorizes`;
`admitted_by`; routing predicates; `decision issued_by invocation`;
`decision approved_by accountable_principal`; `decision evaluates
claim_or_artifact`; `invocation verified_by invocation` (targets a
VerificationRun-bearing invocation); `evaluation_outcome observed_for
executor_identity`; the reified role-qualification predicates (4.6);
`tool_identity uses_executor executor_identity`.

`[DEF]` Status assignment is a field on DecisionRecord
(`recommended_status`, `effective_status`), not a graph edge: a literal
cannot be a `GraphRelation` target. Adjudication is represented through
DecisionRecords, never a direct `adjudicated` edge.

## 6. Epistemic Constraints

`[PROPOSED_CONSTRAINT]` C1 Staged provenance completeness. Provenance
profiles activate in stages; a governed output created after activation of
the applicable profile is admissible only if it satisfies that profile:
provenance_v1 (producing invocation; executor identity;
EffectiveInputManifest; session-state mode; ExecutionProfile; output
record; timestamps; model-specific identity and catalog fields required
only when a model participated as executor or execution resource);
authorization_v1 (role assignment, qualification, consequence class,
invocation authorization); lineage_v1 (input/claim ancestry and
independence assessment).

`[PROPOSED_CONSTRAINT]` C2 Catalog admission: an execution candidate
(executor within a qualification's execution scope, 4.6) may serve a
governed role only when the role's required catalog claims are satisfied at
the role's freshness requirements. Experimental execution is permitted;
experimental outputs cannot silently enter governed evidence.

`[INHERITED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
invocation cannot adjudicate a claim whose evidence ancestry contains an
invocation by an equivalent executor identity, with equivalence defined
per executor kind: ModelIdentity resolution equality for models;
tool identity and version equality for tools; principal equality for
humans. Direct lineage conflict: hard prohibition, no exception.
Equivalent-identity conflict: hard prohibition absent a future explicitly
governed exceptional procedure. Unknown or unresolved executor equivalence
cannot establish identity independence; it yields
`independence_unresolved`, never an independent path. An identity
unresolved at one endpoint and resolved at another is treated as distinct
until equivalence is affirmatively established; distinctness never
increases independence (P5).

`[PROPOSED_CONSTRAINT]` C4 No hidden witness reuse: an invocation that
consumed another witness's output is not an independent confirmation of
that testimony; it may count as synthesis or critique.

`[PROPOSED_CONSTRAINT]` C5 Lineage-based independence. Isolation from other
witness outputs is necessary for counting an invocation as independent
confirmation of those outputs, but not sufficient for witness-path
independence: shared erroneous sources, common leading prompts, shared
hidden state, and shared unsupported assumptions defeat it. Round labels
describe protocol; lineage determines admissibility. Independence is
assessed per dimension (information path, source, executor identity,
provider/organization correlation, prompt common cause, session-state
confidence, claim-lineage completeness), some of which are hard
disqualifiers. First implementations produce categorical statuses
(`qualified_independent` | `dependent` | `unresolved`) with
dimension-specific reasons; no single numeric score, and no claimed weight
function without evaluation evidence. Provider similarity is recorded as a
correlation factor.

`[INHERITED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another. Assignment independence
is not exercise license: adjudicator-level epistemic authority and
above-read_only action authority may not both be exercised within a single
invocation against the same target unless the adjudication is covered by
an independent verification edge; an invocation that mutates state it also
adjudicates collapses the separation C6 exists to preserve. COMP-0032
produced two constructions satisfying the axis definitions while defeating
separation; this sentence closes both.

`[LIMITATION]` Role, qualification, and authorization records are inputs to a
C6 evaluation. Their existence does not establish that the C6 exercise
restriction was evaluated or satisfied for a particular invocation.

`[INHERITED_CONSTRAINT]` C7 Implementation separation: an executor with
repository or external action authority may implement an admitted plan but
may not be the sole verifier or adjudicator of its own changes.

`[PROPOSED_CONSTRAINT]` C8 Decision traceability: every policy-selected
invocation has a reconstructible RoutingDecision or a governed
manual-override DecisionRecord (accountable principal, reason, scope,
review condition; never a free-text escape hatch).

`[INHERITED_CONSTRAINT]` C9 Conservative lineage inheritance (from P3): an
artifact grounded in pre-provenance or lineage-incomplete material inherits
`claim_lineage_status: source_lineage_partial` while recording
`source_provenance_status` of its sources (for example `pre_provenance`).
Structural transformation, including extraction, cannot improve the
provenance class of the information transformed. Extraction from
pre-provenance sources is permitted; its outputs carry
`source_provenance_status: pre_provenance`, `claim_lineage_status:
source_lineage_partial`, `independent_observation: false`.

Selection provenance (COMP-0032 finding): an invocation's effective inputs
include the selection criteria and priors used to choose its sources.
Undisclosed selection priors derived from pre-provenance or
lineage-incomplete material taint the selection even when every selected
source is independently clean; at high consequence, claims whose source
selection lacks disclosed selection provenance carry `claim_lineage_status:
source_lineage_partial`. Honest limitation: offline human reading is
unobservable, so this rule is only partially enforceable ever;
HumanActionRecord (Section 11) narrows but cannot close the gap, and the
ontology states this rather than pretending otherwise.

`[INHERITED_CONSTRAINT]` C11 Interim independence disclosure: until
claim-level lineage exists, witness-path independence counts are
artifact-level approximations, and both COMP-0032 witnesses independently
identified the resulting silent failure mode (N "independent" paths
satisfied by N copies of one unrecorded shared claim). Therefore any
high-consequence decision relying on a minimum number of independent
witness paths must disclose in its DecisionRecord that independence was
assessed at artifact level only, and must name the compensating controls
relied on (operator adjudication, source disclosure, deterministic
verification of the claims where available). Absent that disclosure, the
independence requirement is unmet, not silently satisfied.

`[INHERITED_CONSTRAINT]` C10 Validator lineage independence (property-scoped
P2 hardening): verifier provenance (identity, version, rule/test version,
inputs, environment, result) is always recorded. When the code, schema,
tests, or configuration driving a verification share evidence ancestry
with the ModelIdentity that produced the output under test, the
verification is marked `verifier_lineage: self_authored` and carries
reduced independence standing; the verified property claim stands only as
far as the verifier's scope and lineage permit. At high consequence,
admission requires either independently-lineaged verification or
independent review of the verifier. Self-authored verification is
governed, not prohibited: AI-Lab's existing compensating controls
(cross-environment reproduction, operator adjudication, provider
completion review) are recognized independent paths.

## 7. Legacy and Phase-In

`[DEF]` Provenance statuses: provenance_complete | provenance_partial |
pre_provenance | provenance_conflicted. Claim-lineage statuses include
source_lineage_partial. These describe provenance condition, never truth.

`[INHERITED_CONSTRAINT]` Historical standing is distinct from prospective
evidentiary use. Pre-provenance artifacts (including the GAP-0003/0004
closure chains) retain historical governance status in full. Prospective
reuse requires disclosure of missing provenance and may trigger
corroboration, reduced independence standing, or exclusion by receiving
role and consequence class. Grandfathering into full independent-evidence
standing is prohibited. The known laundering path (legacy claim, cleanly
produced summary, blind witness, apparent fresh corroboration) is defeated
by C9: the summary inherits the lineage limitation and any witness
confirmation of it is `dependent` on a lineage-partial path.

## 8. Consequence Classes

`[DEF]` Ordinal classes (low | medium | high), not numbers.
`default_consequence` derives from target type (gap closure, plan
admission: high; comparison/synthesis: medium; extraction/classification:
low). `effective_consequence = max(default_consequence,
applicable_modifier_levels)`; modifiers (repository mutation, external side
effect, irreversibility, warrant/capability status change,
security/privacy/legal/financial impact) only raise. `[INHERITED_CONSTRAINT]`
Downward adjustment is a separate governed exception (reason, accountable
principal, scope, evidence, expiry/review) and can never override hard
prohibitions such as disqualifying lineage conflicts. `[OPEN]` Detailed
classification function.

## 9. Enforcement Matrix

`[DEF]` Normative state: proposed | adopted-manual | machine-enforced.
Representability: none | partial | full. Manual enforcement counts only
when the check leaves a named artifact; the claim that a check happens is
not evidence. Capability dependencies replace slice numbers until admitted
plans exist.

| Constraint | Normative state | Representability | Current enforcement evidence | Target enforcement | Activation condition | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
| C1 staged provenance | proposed | none | none | validator per profile | profile activation decision after capability ships | invocation records; manifests; profiles |
| C2 catalog admission | proposed | none | none | validator + runtime gate | catalog capability ships | catalog snapshots; identities; qualifications |
| C3 no self-adjudication (executor-generic) | adopted-manual | partial | named attestation in completion warrants (for example WARR-20260719-0002 scope adjudications) | per-kind equivalence check + lineage traversal | already active manually | ancestry capture; executor-equivalence semantics |
| C4 hidden witness reuse | proposed | none | none | context-lineage inspection | lineage capability ships | manifests; ancestry |
| C5 lineage independence | proposed | none | none | categorical assessment with reasons | lineage capability ships | ancestry; claim lineage |
| C6 authority separation | adopted, not currently evidenced | partial | none (no current record names the check) | artifact validator | already practiced; evidence begins with role records | role records |
| C7 implementation separation | adopted-manual | partial | VERIFY records (cross-environment verification) | validator on VERIFY records | already active | none; strengthened later |
| C8 decision traceability | proposed | none | none | RoutingDecision validation | routing capability ships | routing records |
| C9 lineage inheritance | adopted-manual | partial | named disclosure statements in records | inheritance propagation | already active manually | claim lineage (full) |
| C10 validator lineage | adopted-manual | partial | verifier identity in VERIFY command records; independence via cross-environment and operator review | VerificationRun with verifier-ancestry check | already active manually | ancestry capture |
| C11 interim independence disclosure | adopted-manual | partial | disclosure statements in DecisionRecords/warrants | admission validator requiring disclosure + named controls | already active manually | none; retired when claim lineage ships |

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

## 11. Defined but Deferred

Run/ProtocolRound, Claim/EvidenceItem, RoutingPolicy and
AuthorizationPolicy enforcement, RoutingDecision enforcement,
VerificationRun and IndependenceAssessment record implementation,
OutboundInteractionLog (content-addressed declaration of a tool's external
interactions: network targets, external writes, privileged output
consumers; the enforcement object for external-interaction disclosure),
HumanActionRecord (audited human actions that shape effective inputs
without issuing a DecisionRecord; privacy-preserving, principal-referenced;
the partial enforcement object for selection provenance), formal
independence assessment beyond categorical statuses, automatic consequence
assignment, full ancestry enforcement, provider-diversity thresholds,
escalation, third-provider integration, session-mode cataloging per
provider API, endpoint mutable-property assertions.

## 12. Open Questions

`[OPEN]` Authorization-chain bootstrap (Section 3). `[OPEN]` Consequence
classification function and override taxonomy. `[OPEN]` Qualifying
witness-path thresholds per consequence class, including whether any
decision class requires paths constructible only with a third provider
(Gemini, DeepSeek, or similar), weighing integration cost, jurisdiction,
endpoint data governance. `[OPEN]` Session-state reconstructibility per
provider API. `[OPEN]` AccountablePrincipal contents and privacy-preserving
human decision records. `[OPEN]` EvaluationOutcome sufficiency per
authority level; who admits evaluators. `[OPEN]` ExecutorIdentity
superclass (reopened by COMP-0032 with the polymorphic-equivalence
argument). `[OPEN]` EvaluationOutcome typing: DecisionRecord kind, or
Claim/EvidenceItem with provenance; as defined it cannot carry lineage
into governed evidence. `[OPEN]` DecisionRecord: extend warrants or new
family; subtypes or one family. `[OPEN]` Per-provider escalation ladders: entirely
deferred to the post-ontology comparison with live catalog verification.

## 13. Challenge-Round Questions

1. Which objects are missing; which defined objects are category errors?
2. Which constraints are unenforceable as stated; what minimal
   representable form makes them enforceable?
3. Construct a concrete invocation satisfying the three-axis Role
   definitions while violating authority separation.
4. Construct a laundering path from a pre-provenance artifact into
   high-consequence independent evidence that survives C9 and C10.
5. Does candidate Slice A omit anything without which the provenance graph
   cannot later answer the witness-independence question?
6. Identify any predicate ambiguous enough to produce divergent
   implementations.
7. Where is invocation authorization represented; how is it distinguished
   from routing and evidence admission; does the distinction hold under
   composition?
8. Can the ontology represent one model served through different
   organizations, endpoints, regions, or mutable aliases without creating
   false model independence?
9. Does provenance as specified apply to claim derivation or only artifact
   production, and where exactly does the artifact-level approximation
   break?
10. What must an effective-input record contain before an invocation may be
    treated as blind?
11. Which constraints apply identically to models, tools, and humans; which
    require executor-specific rules?
12. Under what conditions, if any, can an unresolved model identity qualify
    as an independent witness path? Identify the failure behavior when
    equivalence cannot be resolved.
13. Construct a composite tool that satisfies the disclosure constraints'
    letter (4.7, both) while still exercising undeclared authority.
14. Construct a case where property-scoped verification (P2) plus validator
    lineage marking (C10) still admits a generator-authored blind spot into
    governed evidence.

Do not recommend specific provider products in this round.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
## Split limitation and missing materials

The split prevents a complete determination of several claims made here. In particular, Sections 5–13 rely on, but do not supply:

- Section 3, for the authorization bootstrap referenced in Section 12.
- Sections 4.6 and 4.7, for execution-scoped qualifications, reified role-qualification predicates, and the composite-tool disclosure challenge.
- The admitted v4 text and its admission event, to determine whether anything marked `[INHERITED_CONSTRAINT]` was actually admitted.
- The referenced `WARR-20260719-0002`, the unspecified “VERIFY records,” the purported C9 disclosure records, and the C11 DecisionRecords/warrants. These are needed to check whether the enforcement matrix’s claimed evidence exists and actually records the stated checks.
- `ai_lab/documentation/graph_neighborhood.py`, needed to assess whether the asserted common `GraphRelation` shape supplies the necessary relation semantics.
- Definitions of the named record types and their required fields, especially `DecisionRecord`, `RoutingDecision`, `VerificationRun`, `EvidenceAdmissionDecision`, `InvocationAuthorization`, and `EffectiveInputManifest`.

Those omissions do not prevent identifying serious defects in the visible text, especially the matrix, but they prevent validation of inheritance, current enforcement evidence, and several cross-section claims.

## Weakest part: the enforcement matrix

The matrix is the weakest part because it purports to make enforcement status checkable, while several entries are either internally invalid, unsupported by supplied evidence, or weaker than the corresponding constraint.

### 1. C6 uses a normative state that the matrix itself says does not exist

The matrix defines normative state as:

> “proposed | adopted-manual | machine-enforced.”

But C6 is assigned:

> “adopted, not currently evidenced”

That is not one of the defined states. It conflates at least three different questions:

1. whether the constraint was ever admitted;
2. whether it is presently operative;
3. whether there is evidence that it was checked.

The row then gives:

> “Current enforcement evidence | none”

and

> “Activation condition | already practiced; evidence begins with role records”

This is not an enforcement state that a reader can verify. It explicitly records no evidence, while asserting existing practice. Further, Section 6 says:

> “Role, qualification, and authorization records are inputs to a C6 evaluation. Their existence does not establish that the C6 exercise restriction was evaluated or satisfied for a particular invocation.”

Therefore “evidence begins with role records” is insufficient even on the document’s own terms. Role records cannot demonstrate that the prohibited combination of mutation and adjudication was checked, nor that an “independent verification edge” covered it.

This is unsound, not merely incomplete: the matrix represents C6 as adopted and already practiced without a valid matrix state or evidence capable of establishing compliance.

### 2. Several claimed evidence entries cannot be checked from the supplied record

For C3, the matrix cites:

> “named attestation in completion warrants (for example WARR-20260719-0002 scope adjudications)”

For C7:

> “VERIFY records (cross-environment verification)”

For C9:

> “named disclosure statements in records”

For C10:

> “verifier identity in VERIFY command records; independence via cross-environment and operator review”

For C11:

> “disclosure statements in DecisionRecords/warrants”

None of those referenced warrants, VERIFY records, disclosure statements, command records, or DecisionRecords is included. C9 and C11 do not even name a record in the matrix. The stated rule is:

> “Manual enforcement counts only when the check leaves a named artifact; the claim that a check happens is not evidence.”

On the supplied evidence, the C9 and C11 entries fail that rule outright because no named artifact is given. C3, C7, and C10 cannot be verified because their named artifacts are absent.

An attestation also does not necessarily establish the substance of C3. C3 requires executor-kind-specific identity equivalence, evidence ancestry, and a prohibition on direct lineage conflict. A warrant that merely attests to an adjudication does not show that ancestry traversal and equivalence analysis occurred, unless the warrant’s required fields and contents establish that fact.

### 3. The matrix overstates manual enforcement where dependencies are absent or deferred

C9 is marked:

> “adopted-manual”

with a target of:

> “inheritance propagation”

but its dependency is:

> “claim lineage (full)”

Meanwhile, full ancestry enforcement and claim/evidence implementation are deferred in Section 11, and Slice D is only proposed. Manual disclosure can document a limitation, but it cannot demonstrate that all transformed material inherited the correct status, particularly through multi-step derivations or undisclosed source-selection priors.

C10 similarly claims manual enforcement despite depending on:

> “ancestry capture”

which is not shown as operational. Recording verifier identity is not enough to determine whether “the code, schema, tests, or configuration” share evidence ancestry with the producing model. The asserted evidence is therefore materially weaker than the C10 check.

### 4. The matrix does not distinguish “constraint text exists” from “constraint is operative”

Given the stipulated status that v9 is proposed and has no governance force, the matrix cannot itself make a v9 constraint adopted. The rows headed “adopted-manual” and the C6 “adopted, not currently evidenced” entry require support from the admitted v4 text and admission record. The visible evidence does not establish that support.

The `[INHERITED_CONSTRAINT]` tag is not enough. Its meaning, its admission linkage, and the precise v4 source text are absent. As presented, the matrix risks turning a reconstruction’s internal label into an assertion of operative governance.

## Other unsound provisions

### C3 permits the unresolved-identity gap it says it is avoiding

C3 says:

> “Unknown or unresolved executor equivalence cannot establish identity independence”

but also:

> “An identity unresolved at one endpoint and resolved at another is treated as distinct until equivalence is affirmatively established”

and its hard prohibition is framed around evidence ancestry containing:

> “an invocation by an equivalent executor identity”

If equivalence is unresolved, the hard prohibition does not clearly trigger. The text says this yields `independence_unresolved`, but no visible rule says that an adjudication itself is barred when the possible self-adjudicator’s identity is unresolved. “Not independent” and “may not adjudicate” are different consequences.

Thus a same-executor self-adjudication could be relabeled as unresolved rather than identified as equivalent, avoid the stated direct prohibition, and still proceed unless an omitted role or admission rule rejects unresolved independence. The missing rule needed to close this is an explicit adjudication-admission condition: unresolved equivalence must prohibit, or at least suspend, adjudication whenever C3 independence is required.

### C6’s exception is undefined and can reverse its prohibition

C6 prohibits combining adjudication with above-read-only action against the same target:

> “unless the adjudication is covered by an independent verification edge”

But the visible text does not define:

- what makes a verification edge “independent”;
- whether it must precede, follow, or be contemporaneous with adjudication;
- who or what must be independent of whom;
- whether it must verify the mutation, the adjudication, or both;
- whether a later verification can retroactively cure a prohibited combined exercise.

The only listed edge is:

> “invocation verified_by invocation”

That does not itself encode independence, scope, timing, or outcome. This is more than deferred detail because the undefined exception determines when a stated prohibition does not apply.

### C10 calls non-established paths independent

C10 says:

> “AI-Lab's existing compensating controls (cross-environment reproduction, operator adjudication, provider completion review) are recognized independent paths.”

No visible condition requires those paths to have independent evidence ancestry, executor identity, organization/provider correlation, prompts, assumptions, or verifier implementation lineage. Cross-environment reproduction may run the same self-authored test suite; operator adjudication may rely on the same generated evidence; provider completion review may remain within the same provider or organizational correlation domain.

Calling these paths independent without the C5 dimension-by-dimension analysis is unsound. At most, they are possible compensating controls whose independence must be separately established.

### C11 creates an apparent safeguard with no determinate trigger

C11 applies when a high-consequence decision relies on:

> “a minimum number of independent witness paths”

But Section 12 leaves open:

> “Qualifying witness-path thresholds per consequence class”

Without thresholds, the document does not establish which high-consequence decisions require multiple paths, nor when the disclosure requirement triggers. A decision can evade C11 by characterizing itself as not relying on a minimum count. The disclosure requirement is useful only after the relevant admission criteria and thresholds are defined.

### “Current enforcement evidence” is confused with evidence of a control’s inputs

For C10, verifier identity in a command record is evidence of identity recording, not evidence of a verifier-lineage analysis. For C6, role records are inputs to an evaluation, not evidence that the evaluation happened. This repeats a general category error: records used by a check are presented as evidence that the check was performed and passed.

## Significant incompleteness

These points may be repairable, but they are not presently specified.

- The predicate registry is described as required, yet the visible vocabulary has no supplied source/target types, cardinalities, inverses, temporal rules, transitivity rules, evidence requirements, or authoritative-default behavior. The document names those as registry contents but does not provide the registry.
- “All relations use the `GraphRelation` shape” cannot be assessed without the referenced shape. It is also unclear how the shape handles relation-level evidence, temporal validity, conflict, provenance, and asserted versus observed relation status.
- `effective_consequence = max(default_consequence, applicable_modifier_levels)` is not operational while the classification function and override taxonomy remain open. “Applicable” modifiers and their level assignment are not defined.
- C1 refers to “activation of the applicable profile,” but the visible text does not define profile applicability, profile versioning, activation authority, affected scope, transition treatment, or how an output’s creation time is determined when production is distributed or resumed.
- C2’s distinction between experimental and governed output is not represented by a defined admission transition in the visible material. Slice D is only proposed, while C2 says experimental outputs cannot enter governed evidence silently.
- C8 allows a governed manual override but does not define the admissibility or review consequences when the override itself selects a candidate lacking catalog qualification, authorization, or provenance.
- C9 acknowledges that offline human reading is unobservable and only partially enforceable. That limitation is candid, but no visible consequence rule says when that partial enforceability makes high-consequence use unavailable rather than merely disclosed.
- Section 11 defers `HumanActionRecord`, `OutboundInteractionLog`, `VerificationRun`, and full ancestry enforcement, despite C4, C5, C9, and C10 relying on the information those objects would carry.

## Significant matters the challenge-round questions do not ask

The listed questions probe many important semantic and provenance failures, but they do not expressly ask the following:

1. **Whether the enforcement matrix is valid on its own terms.**  
   No challenge question asks why C6 has an undefined normative state, whether “already practiced” can coexist with “none,” or whether the matrix distinguishes operative status from evidence status.

2. **Whether the asserted current evidence is actually available, named, and sufficient.**  
   The questions do not require production and field-level inspection of `WARR-20260719-0002`, VERIFY records, C9 disclosures, or C11 DecisionRecords/warrants.

3. **Whether a proposed reconstruction may represent constraints as adopted or inherited.**  
   No challenge question asks for a constraint-by-constraint comparison against admitted v4 text, the admission event, and any subsequent valid governance act.

4. **Whether unresolved identity blocks adjudication rather than merely blocks an independence count.**  
   Question 12 addresses unresolved model identity and independent witness paths, but not C3’s distinct self-adjudication failure mode for unresolved identities.

5. **Whether C6’s “independent verification edge” exception is defined tightly enough to avoid becoming a universal bypass.**

6. **Whether C10’s listed “independent paths” meet C5’s own independence dimensions.**  
   Question 14 tests one generator-authored blind spot, but it does not test the unsupported classification of cross-environment reproduction, operator adjudication, and provider completion review as independent.

7. **Whether current enforcement is being inferred from the existence of inputs rather than evidence of the check.**  
   This affects C3, C6, C7, C9, C10, and C11.

8. **Whether phase-in produces a valid admission rule during the period when lineage and authorization objects remain deferred.**  
   The questions ask about omissions and enforceability generally, but not the transition case in which high-consequence use occurs before the controls required to evaluate it exist.

The most immediate defect is therefore not a missing object or an ambiguous predicate. It is that the enforcement matrix makes adoption and enforcement representations that are not supported by the visible evidence, contains an invalid normative state for C6, and in multiple rows mistakes evidence of inputs or asserted practice for evidence that the required control was performed.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Scope limitation

I can see only Sections 5–13. Section 3 (predicate registry detail, referenced repeatedly), Section 4 (role axes and qualification reification, referenced as "4.6" and "4.7"), and whatever defines "P2," "P3," and "P5" (cited in C3, C9, C10) are not in this evidence set. I cannot check whether Section 5's canonical relations or Section 6's constraints are consistent with those sections, and I cannot check whether the `[INHERITED_CONSTRAINT]` tag is applied correctly against v4's actual text of those sections, since v4 itself is not in evidence either. I would need Sections 1–4 of v9 and the admitted v4 text to do that.

## The enforcement matrix (Section 9) — weakest part

1. **The matrix uses a normative-state value that its own definition doesn't contain.** Section 9 defines: "Normative state: proposed | adopted-manual | machine-enforced." The C6 row's normative state is "adopted, not currently evidenced" — a fourth value outside the stated enum. This is not a minor omission; it is the enforcement matrix, "the one place the document states its own enforcement status in a form a reader can check against the rest," failing its own check on its own governing definition, for the constraint (authority separation) the document treats as most safety-critical.

2. **Uneven application of the matrix's own evidentiary rule.** Section 9 states: "Manual enforcement counts only when the check leaves a named artifact; the claim that a check happens is not evidence." Only one row satisfies this with a specific instance: C3 cites "named attestation in completion warrants (for example WARR-20260719-0002 scope adjudications)." Every other "adopted-manual" row names a record *type*, not an instance: C7 "VERIFY records (cross-environment verification)," C9 "named disclosure statements in records," C10 "verifier identity in VERIFY command records," C11 "disclosure statements in DecisionRecords/warrants." Under the matrix's own stated rule, "VERIFY records exist as a category" is exactly the kind of unfalsifiable claim the rule was written to exclude — a reader cannot check any of C7/C9/C10/C11 against the rest of the document the way C3 can be checked.

3. **C6's row is internally split.** "Current enforcement evidence" is "none (no current record names the check)" while "Normative state" is nonetheless "adopted." Section 6 itself concedes this in the `[LIMITATION]` note: "Their existence does not establish that the C6 exercise restriction was evaluated or satisfied for a particular invocation." So the body text and the matrix agree there is no check, but the matrix still asserts adopted status using a value the document never defined. That is unsound, not merely incomplete: the document contradicts its own taxonomy while describing the one constraint most exposed to the "mutate what you adjudicate" failure it names.

## The `[INHERITED_CONSTRAINT]` tag itself

Disclosure 2 says the round exists to test whether `[INHERITED_CONSTRAINT]` solves what sank v8. Reading Sections 5–9 as instructed:

- C6 closes with: "COMP-0032 produced two constructions satisfying the axis definitions while defeating separation; this sentence closes both." That sentence is explicitly new content responding to a specific finding, sitting inside a block tagged `[INHERITED_CONSTRAINT]`.
- C9 carries a paragraph headed "Selection provenance (COMP-0032 finding): ..." inside a block tagged `[INHERITED_CONSTRAINT]`.
- C10 is parenthetically self-described as "(property-scoped P2 hardening)" — i.e., a hardening/change — under the same tag.
- C11 states "both COMP-0032 witnesses independently identified the resulting silent failure mode," again new-finding content under the same tag.

The tag is applied at constraint-block granularity, not clause granularity, so each of these blocks mixes material that may have existed in admitted v4 with material that demonstrably originates from post-v4 review findings, under a single status label. That is the same defect v8 had — a status tag applied to a block containing both adopted and not-yet-admitted content — under a new name. Nothing in Sections 5–9 shows a mechanism (e.g., sentence-level tagging, changelog, or diff against v4) that would let a reader separate what was actually admitted from what was added afterward. This is a candidate finding for "unsound rather than incomplete": the tag doesn't just omit detail, it makes a status claim the visible text partially contradicts.

## Other findings

- **Consequence classification is `[OPEN]` but load-bearing constraints are marked active.** Section 8: "`[OPEN]` Detailed classification function." Yet C9, C10, and C11 — all of which have explicit "at high consequence" branches — are marked "adopted-manual … already active manually" in Section 9. Without the classification function, "high consequence" cannot be determined, so the manually-active provisions of C9/C10/C11 have no defined trigger condition. The matrix doesn't flag this dependency; Section 8's `[OPEN]` tag and Section 9's "already active" status are not reconciled anywhere visible.

- **Predicate registry vs. implementation sequence mismatch.** Section 5 states the predicate registry is "a required artifact of the first implementation." Section 10's Slice A deliverable list (InvocationRecord, executor reference, EffectiveInputManifest, ExecutionProfile reference, `spawned` edges, `produced_by`, status, validator, fixture) does not mention the predicate registry as a deliverable. Either it is assumed subsumed under "validator and integration fixture" (not stated) or it is a first-implementation requirement Slice A does not actually produce.

- **Section 13 is itself a normative anomaly.** A document section titled "Challenge-Round Questions" embedded inside the ontology text (as opposed to being an artifact of this review process) is unusual; nothing in Sections 5–12 explains whether Section 13 is part of what would be admitted, or scaffolding the drafter left in. If admitted, an ontology amendment containing a self-directed question list is a category question ("which defined objects are category errors," per its own Q1) that Section 13 does not ask about itself.

- **C7's dependency field is self-contradictory in miniature**: "none; strengthened later" states there is no dependency and then names an unstated future one in the same cell.

## What isn't asked, as far as I can see from Section 13's own list

Section 13's 14 questions cover unenforceability (Q2), laundering (Q4), predicate ambiguity (Q6), and self-adjudication edge cases (Q3, Q12, Q14), but none of them asks: (a) whether the enforcement matrix's own normative-state values conform to its own definition, or (b) whether the `[INHERITED_CONSTRAINT]` tag can be trusted at block granularity when the blocks it labels contain explicit new-finding text. Given disclosure 2's framing of this round, that second gap is the one most relevant to whether v9's central fix actually works — and it is not covered by the document's own self-challenge list.
```
