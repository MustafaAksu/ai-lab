# COMP-0032: Provider Comparison — ABS-0004 invocation authorization ontology challenge round

## Metadata

- comparison_id: `COMP-0032`
- title: `ABS-0004 invocation authorization ontology challenge round`
- created_at: `2026-07-20T20:34:06.304395+00:00`
- command: `scripts/compare_providers.py --title ABS-0004 invocation authorization ontology challenge round You are a blind challenge-round reviewer for AI-Lab, a governed AI research environment. You are receiving exactly one document: the draft ontology ABS-0004 v3, reproduced in full below. You have NOT been given any review history, advisor commentary, or repository context, by deliberate protocol design (maximum practical isolation).

Your task: answer the fourteen challenge-round questions in Section 13 of the document. Requirements:
- Answer every question, numbered. Where a question asks you to construct an adversarial example, provide a concrete, specific construction or state explicitly that you could not find one and why.
- Ground every criticism in the document's own text (quote or cite the section).
- Distinguish clearly between defects (internal contradictions, category errors, unenforceable constraints) and preferences (alternative designs you merely favor).
- Do NOT recommend specific provider products, model names, or pricing.
- Do NOT certify, approve, or praise the document; verdicts about readiness are not requested and will be disregarded.
- End with a ranked list of your three most severe findings.

The document follows.

================================================================================

# ABS-0004: Abstraction — Invocation Authorization Ontology

## Metadata

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v3` (v1, v2 superseded during drafting; neither entered the record)
- abstraction_level: `2`
- status: `draft-for-challenge-round`
- authors: operator (adjudicating principal); drafting executor self-reported
  as "Claude" (reported identity claim, not an independently verified
  ModelIdentity); with attributed advisor contributions (see Evidence Inputs)
- sentence discipline: every normative statement is tagged `[DEF]`
  definition, `[PRINCIPLE]` architectural principle, `[PROPOSED_CONSTRAINT]`
  constraint proposed for adoption, `[ADOPTED_CONSTRAINT]` constraint adopted
  now with its current enforcement honestly stated in the matrix, `[COMMIT]`
  commitment concerning the preparation of this document, `[PROPOSAL]`
  candidate implementation boundary subject to future governance, or `[OPEN]`
  open question. Untagged prose binds nothing.

## Evidence Inputs

- The GPT-5.6 Sol model-stack proposal (attributed advisor artifact; catalog
  claims unverified at receipt).
- Advisor documents 1-6: ontology refinement; final notes; v1 adversarial
  review; response filtering; v2 final review; v2 second commentary (all:
  artifact_class advisor; epistemic_authority advisor; provenance_status
  pre_provenance; executor identity a reported claim, not independently
  established; invocation details unrecorded). The v2 second commentary's
  certification language was rejected; two of its constructions were adopted
  in moderated form.
- `[COMMIT]` Normalized immutable text snapshots of all advisor documents,
  not digests alone, enter the repository alongside this ABS before the
  challenge round, each with digest, capture timestamp, source label, and
  provenance limitations. A digest is an integrity anchor, not an evidence
  artifact.
- Epistemics note: the advisory chain (draft, reviews, responses, filters) is
  one braided information path; only the v1 draft was blind, and one advisor
  answered challenge question 13 before the round. No two chain documents
  corroborate each other independently. The challenge round therefore runs
  with maximum practical isolation: providers receive v3 and the challenge
  questions only, no review history. Constructions matching the
  configuration-hijack pattern of question 13 require independent derivation
  to count as corroboration.
- COMP-0028/0029/0030/0031 and SYNCOMP-0016 as recorded evidence of fluent,
  internally consistent, cross-witness-contagious model error.
- GAP-0004 closure chain as evidence that shared vocabularies prevent
  cross-subsystem retrofits.

## 1. Anchoring Principles

`[PRINCIPLE]` P1. AI-Lab does not primarily route prompts to models. It
authorizes invocations for roles under evidence, provenance, independence,
consequence, and execution constraints. Routing is a consequence of the
ontology and the epistemic policy, not the organizing abstraction.

`[PRINCIPLE]` P2. Verification is property-scoped. Successful deterministic
verification may reduce or eliminate witness-independence requirements only
for the specific property the verifier establishes. It never eliminates the
need to record the verifier identity and version, verification inputs,
execution environment, rule or test version, and result; nor does it
establish properties outside the verifier's scope. Where deterministic
verification is unavailable, provenance and witness-path independence are
major controls but not the only admissible ones (formal proof, empirical
replication, source corroboration, human review, external measurement also
qualify). Motivation: modern models fail coherently; internal consistency
cannot detect correlated coherent error; scoped verification and lineage
tracking can.

`[PRINCIPLE]` P3. Complete production provenance does not imply complete
claim provenance. A newly produced artifact must not erase the provenance
limitations of the claims it carries.

`[PRINCIPLE]` P4. Authority cannot be acquired through an opaque wrapper.
Encapsulation does not launder authority.

`[PRINCIPLE]` P5. Unknown facts block qualification; they never disappear
from the vocabulary. Uncertainty remains representable (`unknown_state`,
`unresolved`, `pre_provenance`), and unknown lineage or identity never
increases independence.

## 2. Scope and Non-Goals

`[DEF]` This document defines objects, relations, and constraints, and
proposes (not commits) an implementation sequence. Non-goals: provider
selection, model recommendations, routing/escalation/independence-scoring
implementation, embeddings, any runtime behavior change. Provider product
claims are admissible only as attributed evidence.

## 3. Three Decisions

`[DEF]` The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

`[DEF]` A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

`[OPEN]` Authorization-chain bootstrap: how an authorization chain terminates
in a standing policy, delegated authority, or AccountablePrincipal authority
scope rather than requiring an infinite sequence of prior authorizations.

## 4. Object Definitions

### 4.1 ProviderOrganization

`[DEF]` The organizational authority behind a model or service:
`provider_id`, canonical name, legal jurisdiction, documentation authority.
Credentials are protected runtime configuration; availability is observed
state; neither is a Provider field.

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

### 4.4 CatalogSnapshot and CatalogAssertion

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic:
`assertion_subject`, `assertion_predicate`, `assertion_value_or_target`,
unit, scope, `valid_from`, `valid_until`/superseded, source,
`verification_outcome` (the shared three-valued vocabulary of
`ai_lab/documentation/verification_outcome.py`), `verified_at`. An assertion
may concern an API alias, an endpoint, a price, a region, or a model
identity; verification attaches per claim (alias resolution may be
`unverifiable` while pricing is `verified_current`). Example atomic
assertions: (api-name-X, resolves_to, model-identity-Y);
(api-name-X, context_limit, 400000, tokens).

`[DEF]` Catalog assertions record what a provider claims; they never record
suitability for an AI-Lab role.

### 4.5 EvaluationOutcome

`[DEF]` What AI-Lab or an admitted evaluator observed about an executor's
behavior. Providers assert; evaluations observe.

### 4.6 RoleQualification (execution-scoped)

`[DEF]` A reified policy conclusion that qualifies an executor for a
RoleDefinition only within an explicit execution scope: service endpoint,
permitted ExecutionProfile constraints, session-state constraints, and
policy version. A qualification never transfers implicitly to another
endpoint or a materially different execution profile. Predicates:
`qualifies_executor`, `qualifies_for`, `issued_under`, `based_on`.
`[ADOPTED_CONSTRAINT]` Provider claims alone never qualify an executor for
adjudication authority.

### 4.7 Executor identities

`[DEF]` An Invocation is an event performed by an executor: `ModelIdentity`,
`ToolIdentity`, or `HumanIdentity`, each with distinct verification
requirements. `[OPEN]` Whether an `ExecutorIdentity` superclass is needed
(a proposal to close this by fiat was rejected as conflating identity with
runtime instance; the question stands for the challenge round).

`[ADOPTED_CONSTRAINT]` Composite-executor disclosure: an invocation may not
acquire authority by encapsulating an undisclosed subordinate executor.
Every epistemically or operationally material subordinate execution (model,
tool, or human) capable of influencing the output or external effect must be
represented as an Invocation linked to its parent (`spawned`/`called`). A
tool that invokes a model cannot be represented as a purely deterministic
ToolIdentity. Nondeterminism itself is not prohibited; undeclared authority
and hidden composition are.

`[ADOPTED_CONSTRAINT]` Tool-configuration disclosure: for a ToolIdentity
whose output enters governed evidence, the tool's effective inputs include
every configuration file, environment variable, and local dependency capable
of altering its execution path; these must be declared and content-addressed
in its EffectiveInputManifest. Undeclared configuration access capable of
altering the execution path defeats the tool's deterministic standing
(session-state mode `unknown_state`). This constraint is scoped to
governed-evidence production, not to every utility execution.

### 4.8 ExecutionProfile

`[DEF]` How the executor was configured; referenced by an Invocation, not a
separate execution event. Fields: service endpoint, requested API model
name, sampling parameters, reasoning parameters, provider request flags,
runtime/library version information, tool-execution permissions. Changing
configuration changes the ExecutionProfile, not the executor identity.
ModelIdentity alone does not characterize an execution.

### 4.9 RoleDefinition (three axes)

`[DEF]` A Role composes three independent axes:

- `task_function`: extract | classify | retrieve | generate | compare |
  synthesize | evaluate | plan | implement | verify
- `epistemic_authority`: none | witness | advisor | adjudicator
- `action_authority`: read_only | repository_mutator | external_actuator

Accountable authority remains separate from all three (Section 4.13).

`[ADOPTED_CONSTRAINT]` Producing an artifact does not grant authority to
accept it.

`[ADOPTED_CONSTRAINT]` Witness grounding: witness outputs must identify
their observation source, source span, measurement, or deterministic
derivation. Unsupported hypotheses are advisor outputs, not witness
evidence.

`[DEF]` RoleDefinition constraint fields: allowed input/output classes,
required independence, minimum catalog status, maximum consequence class,
tool permissions, may_assign_epistemic_status, action_authority bounds,
requires_external_verification.

### 4.10 Invocation

`[DEF]` The atomic provenance event: one executor, one execution. Fields:
executor identity, assigned role reference (when the roles capability
exists), EffectiveInputManifest reference, ExecutionProfile reference,
outputs, `occurred_at`, session fields where applicable, authorization
reference where applicable, parent run reference where applicable,
success/failure status.

### 4.11 Run / ProtocolRound (defined, deferred)

`[DEF]` A parent object grouping the invocations of a workflow (model
calls, tool calls, retries, validations, human approvals). Round kinds
(blind_witness, comparison, synthesis, adjudication) are properties of the
protocol object; round labels describe protocol, and lineage determines
admissibility.

### 4.12 EffectiveInputManifest

`[DEF]` What information could influence the result: rendered
system/developer/user messages (as digests), context manifest, retrieval
results, attachments, tool definitions exposed to the executor, prior tool
outputs, session-state reference, inherited provider-managed state, and for
tools the declared configuration set (4.7). It may reference the
ExecutionProfile but does not duplicate it: the profile records
configuration of the executor; the manifest records information reaching
the execution. A ContextManifest alone cannot prove blindness unless
defined as complete for all effective inputs.

### 4.13 DecisionRecord and AccountablePrincipal

`[DEF]` DecisionRecord: `decision_kind` (invocation_authorization |
routing_selection | evidence_admission | manual_override), target,
`recommended_status` and `effective_status` (distinct: a model
recommendation must not appear to have assigned final status before
accountable approval), issuer invocation, accountable approver, evidence,
policy authority, activation state, supersession. `[OPEN]` Whether existing
warrant/admission records are extended to fulfill this or a new record
family is created, and whether kinds are subtypes or one record family.

`[DEF]` InvocationAuthorization (decision_kind invocation_authorization)
additionally carries: invocation request, authorized executor, assigned
role, consequence class, applicable policy, qualifications relied on,
independence requirements, conditions. Without this kind, P1 is not
represented by the ontology.

`[DEF]` RoutingDecision (decision_kind routing_selection) additionally
carries: candidates considered, rejection reasons including lineage
conflicts, selected candidate, policy version, catalog snapshot. Tier
labels are policy-derived under current evidence, never intrinsic
ModelIdentity attributes.

`[DEF]` EvidenceAdmissionDecision (decision_kind evidence_admission)
additionally carries: admitted artifact or claim, admitted epistemic
status, lineage and independence findings relied on, disclosed provenance
limitations.

`[DEF]` AccountablePrincipal: `principal_id`, `principal_kind` (delegated
role, governance body, pseudonymous operator identity, organization, or
other authorized entity), `authority_scope`, `delegation_reference`. No
personal identifying data required. Cryptographic attestation is a later
implementation mechanism, not an ontology requirement.

### 4.14 Session

`[DEF]` A continuity boundary through which one invocation may inherit
state not represented solely by its immediate explicit inputs. State modes:
stateless | explicit_replayed_context | provider_managed_state |
local_managed_state | hybrid_state | unknown_state. Governing question:
does unrecorded inherited state influence the logical execution input?
Caching an explicitly supplied prefix does not by itself constitute hidden
semantic state; provider-managed threads, hidden summaries, server-side
memory, and provider-side truncation or rewriting do.

`[ADOPTED_CONSTRAINT]` An invocation cannot qualify as a blind witness when
provider-managed or hybrid state may contain unrecorded information
relevant to the matter under review. Reconstructible provider-side state
remains eligible when its effective contents and lineage are demonstrated.
`unknown_state` implies independence `unresolved` and blind-witness
ineligibility. State-isolation requirements are protocol-dependent, not
linearly ordered by authority: blind witnesses require the strictest input
isolation; adjudicators require reconstructible evidence ancestry and no
prohibited lineage; advisors may use broader state with disclosure;
actuator state constraints follow operational authorization and
auditability.

### 4.15 Claim / EvidenceItem (defined, deferred)

`[DEF]` A claim anchored to an artifact span: `claim_id`, artifact
reference, span, proposition, claim kind. One artifact may mix original
observation, copied finding, new inference, and paraphrase; artifact-level
lineage cannot distinguish them. Until claim-level derivation exists, the
system provides artifact-level potential-dependence detection, not
claim-level independence proof; Section 7 imposes the conservative
inheritance this gap requires.

### 4.16 RoutingPolicy (defined, deferred)

`[DEF]` A versioned durable rule specifying eligible roles, qualification
requirements, escalation triggers, independence requirements, cost and
latency boundaries, fallback behavior, consequence classes, catalog
freshness requirements.

## 5. Canonical Relations

`[ADOPTED_CONSTRAINT]` All relations use the `GraphRelation` shape of
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

Notes: `executed_with` is dropped (duplicated `executed_by`); alias
resolution is `resolved_to`; `describes` was replaced by `concerns`
because an atomic assertion does not always concern a ModelIdentity;
catalog reliance attaches to selection and authorization events
(`routing_decision relied_on catalog_snapshot`, `authorization relied_on
role_qualification`), not to the invocation.

Full vocabulary (defined now, wired later): `used_prompt`,
`continued_from` (session/execution continuity only), the derivation family
`transformed_from` (mechanical/structural), `claim_derived_from` (epistemic
dependence), `copied_from` (direct inheritance), `summarized_from` (lossy
representation); `assigned_role`; `authorized_by`/`authorizes`;
`admitted_by`; routing predicates; `decision issued_by invocation`;
`decision approved_by accountable_principal`; `decision evaluates
claim_or_artifact`; `invocation verified_by invocation`;
`evaluation_outcome observed_for executor_identity`; the reified
role-qualification predicates (4.6); `tool_identity uses_executor
executor_identity`; `called` (subordinate execution).

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

`[ADOPTED_CONSTRAINT]` C3 No self-adjudication: an invocation cannot
adjudicate a claim whose evidence ancestry contains an invocation resolved
to the same ModelIdentity. Direct lineage conflict: hard prohibition, no
exception. Model-identity conflict: hard prohibition absent a future
explicitly governed exceptional procedure. Unknown or unresolved model
equivalence cannot establish model-identity independence; it yields
`independence_unresolved`, never an independent path.

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

`[ADOPTED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another.

`[ADOPTED_CONSTRAINT]` C7 Implementation separation: an executor with
repository or external action authority may implement an admitted plan but
may not be the sole verifier or adjudicator of its own changes.

`[PROPOSED_CONSTRAINT]` C8 Decision traceability: every policy-selected
invocation has a reconstructible RoutingDecision or a governed
manual-override DecisionRecord (accountable principal, reason, scope,
review condition; never a free-text escape hatch).

`[ADOPTED_CONSTRAINT]` C9 Conservative lineage inheritance (from P3): an
artifact grounded in pre-provenance or lineage-incomplete material inherits
`claim_lineage_status: source_lineage_partial` while recording
`source_provenance_status` of its sources (for example `pre_provenance`).
Structural transformation, including extraction, cannot improve the
provenance class of the information transformed. Extraction from
pre-provenance sources is permitted; its outputs carry
`source_provenance_status: pre_provenance`, `claim_lineage_status:
source_lineage_partial`, `independent_observation: false`.

`[ADOPTED_CONSTRAINT]` C10 Validator lineage independence (property-scoped
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

`[ADOPTED_CONSTRAINT]` Historical standing is distinct from prospective
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
security/privacy/legal/financial impact) only raise. `[ADOPTED_CONSTRAINT]`
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
| C3 no self-adjudication | adopted-manual | partial | named attestation in completion warrants (for example WARR-20260719-0002 scope adjudications) | lineage traversal | already active manually | ancestry capture |
| C4 hidden witness reuse | proposed | none | none | context-lineage inspection | lineage capability ships | manifests; ancestry |
| C5 lineage independence | proposed | none | none | categorical assessment with reasons | lineage capability ships | ancestry; claim lineage |
| C6 authority separation | adopted, not currently evidenced | partial | none (no current record names the check) | artifact validator | already practiced; evidence begins with role records | role records |
| C7 implementation separation | adopted-manual | partial | VERIFY records (cross-environment verification) | validator on VERIFY records | already active | none; strengthened later |
| C8 decision traceability | proposed | none | none | RoutingDecision validation | routing capability ships | routing records |
| C9 lineage inheritance | adopted-manual | partial | named disclosure statements in records | inheritance propagation | already active manually | claim lineage (full) |
| C10 validator lineage | adopted-manual | partial | verifier identity in VERIFY command records; independence via cross-environment and operator review | verifier-ancestry check | already active manually | ancestry capture |

## 10. Proposed Implementation Sequence

`[PROPOSAL]` Candidate slices, each subject to GAP definition, plan
admission, and review; not commitments:

- Slice A, invocation provenance capture on exactly one path
  (`scripts/compare_providers.py`): atomic InvocationRecord; executor
  reference; requested API model name; endpoint surface; minimal
  EffectiveInputManifest containing rendered prompt digest,
  system/developer instruction digests, ContextManifest reference, exposed
  tool-schema digest, prior tool-result references, and session-state mode
  (only fields applicable to this path populated); ExecutionProfile
  reference; `produced_by`; status; validator and integration fixture. No
  routing, no catalog enforcement.
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

Run/ProtocolRound, Claim/EvidenceItem, RoutingPolicy, RoutingDecision
enforcement, formal independence assessment beyond categorical statuses,
automatic consequence assignment, full ancestry enforcement,
provider-diversity thresholds, escalation, third-provider integration,
session-mode cataloging per provider API, endpoint mutable-property
assertions.

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
superclass. `[OPEN]` DecisionRecord: extend warrants or new family;
subtypes or one family. `[OPEN]` Per-provider escalation ladders: entirely
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

Do not recommend specific provider products in this round.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

You are a blind challenge-round reviewer for AI-Lab, a governed AI research environment. You are receiving exactly one document: the draft ontology ABS-0004 v3, reproduced in full below. You have NOT been given any review history, advisor commentary, or repository context, by deliberate protocol design (maximum practical isolation).

Your task: answer the fourteen challenge-round questions in Section 13 of the document. Requirements:
- Answer every question, numbered. Where a question asks you to construct an adversarial example, provide a concrete, specific construction or state explicitly that you could not find one and why.
- Ground every criticism in the document's own text (quote or cite the section).
- Distinguish clearly between defects (internal contradictions, category errors, unenforceable constraints) and preferences (alternative designs you merely favor).
- Do NOT recommend specific provider products, model names, or pricing.
- Do NOT certify, approve, or praise the document; verdicts about readiness are not requested and will be disregarded.
- End with a ranked list of your three most severe findings.

The document follows.

================================================================================

# ABS-0004: Abstraction — Invocation Authorization Ontology

## Metadata

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v3` (v1, v2 superseded during drafting; neither entered the record)
- abstraction_level: `2`
- status: `draft-for-challenge-round`
- authors: operator (adjudicating principal); drafting executor self-reported
  as "Claude" (reported identity claim, not an independently verified
  ModelIdentity); with attributed advisor contributions (see Evidence Inputs)
- sentence discipline: every normative statement is tagged `[DEF]`
  definition, `[PRINCIPLE]` architectural principle, `[PROPOSED_CONSTRAINT]`
  constraint proposed for adoption, `[ADOPTED_CONSTRAINT]` constraint adopted
  now with its current enforcement honestly stated in the matrix, `[COMMIT]`
  commitment concerning the preparation of this document, `[PROPOSAL]`
  candidate implementation boundary subject to future governance, or `[OPEN]`
  open question. Untagged prose binds nothing.

## Evidence Inputs

- The GPT-5.6 Sol model-stack proposal (attributed advisor artifact; catalog
  claims unverified at receipt).
- Advisor documents 1-6: ontology refinement; final notes; v1 adversarial
  review; response filtering; v2 final review; v2 second commentary (all:
  artifact_class advisor; epistemic_authority advisor; provenance_status
  pre_provenance; executor identity a reported claim, not independently
  established; invocation details unrecorded). The v2 second commentary's
  certification language was rejected; two of its constructions were adopted
  in moderated form.
- `[COMMIT]` Normalized immutable text snapshots of all advisor documents,
  not digests alone, enter the repository alongside this ABS before the
  challenge round, each with digest, capture timestamp, source label, and
  provenance limitations. A digest is an integrity anchor, not an evidence
  artifact.
- Epistemics note: the advisory chain (draft, reviews, responses, filters) is
  one braided information path; only the v1 draft was blind, and one advisor
  answered challenge question 13 before the round. No two chain documents
  corroborate each other independently. The challenge round therefore runs
  with maximum practical isolation: providers receive v3 and the challenge
  questions only, no review history. Constructions matching the
  configuration-hijack pattern of question 13 require independent derivation
  to count as corroboration.
- COMP-0028/0029/0030/0031 and SYNCOMP-0016 as recorded evidence of fluent,
  internally consistent, cross-witness-contagious model error.
- GAP-0004 closure chain as evidence that shared vocabularies prevent
  cross-subsystem retrofits.

## 1. Anchoring Principles

`[PRINCIPLE]` P1. AI-Lab does not primarily route prompts to models. It
authorizes invocations for roles under evidence, provenance, independence,
consequence, and execution constraints. Routing is a consequence of the
ontology and the epistemic policy, not the organizing abstraction.

`[PRINCIPLE]` P2. Verification is property-scoped. Successful deterministic
verification may reduce or eliminate witness-independence requirements only
for the specific property the verifier establishes. It never eliminates the
need to record the verifier identity and version, verification inputs,
execution environment, rule or test version, and result; nor does it
establish properties outside the verifier's scope. Where deterministic
verification is unavailable, provenance and witness-path independence are
major controls but not the only admissible ones (formal proof, empirical
replication, source corroboration, human review, external measurement also
qualify). Motivation: modern models fail coherently; internal consistency
cannot detect correlated coherent error; scoped verification and lineage
tracking can.

`[PRINCIPLE]` P3. Complete production provenance does not imply complete
claim provenance. A newly produced artifact must not erase the provenance
limitations of the claims it carries.

`[PRINCIPLE]` P4. Authority cannot be acquired through an opaque wrapper.
Encapsulation does not launder authority.

`[PRINCIPLE]` P5. Unknown facts block qualification; they never disappear
from the vocabulary. Uncertainty remains representable (`unknown_state`,
`unresolved`, `pre_provenance`), and unknown lineage or identity never
increases independence.

## 2. Scope and Non-Goals

`[DEF]` This document defines objects, relations, and constraints, and
proposes (not commits) an implementation sequence. Non-goals: provider
selection, model recommendations, routing/escalation/independence-scoring
implementation, embeddings, any runtime behavior change. Provider product
claims are admissible only as attributed evidence.

## 3. Three Decisions

`[DEF]` The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

`[DEF]` A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

`[OPEN]` Authorization-chain bootstrap: how an authorization chain terminates
in a standing policy, delegated authority, or AccountablePrincipal authority
scope rather than requiring an infinite sequence of prior authorizations.

## 4. Object Definitions

### 4.1 ProviderOrganization

`[DEF]` The organizational authority behind a model or service:
`provider_id`, canonical name, legal jurisdiction, documentation authority.
Credentials are protected runtime configuration; availability is observed
state; neither is a Provider field.

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

### 4.4 CatalogSnapshot and CatalogAssertion

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic:
`assertion_subject`, `assertion_predicate`, `assertion_value_or_target`,
unit, scope, `valid_from`, `valid_until`/superseded, source,
`verification_outcome` (the shared three-valued vocabulary of
`ai_lab/documentation/verification_outcome.py`), `verified_at`. An assertion
may concern an API alias, an endpoint, a price, a region, or a model
identity; verification attaches per claim (alias resolution may be
`unverifiable` while pricing is `verified_current`). Example atomic
assertions: (api-name-X, resolves_to, model-identity-Y);
(api-name-X, context_limit, 400000, tokens).

`[DEF]` Catalog assertions record what a provider claims; they never record
suitability for an AI-Lab role.

### 4.5 EvaluationOutcome

`[DEF]` What AI-Lab or an admitted evaluator observed about an executor's
behavior. Providers assert; evaluations observe.

### 4.6 RoleQualification (execution-scoped)

`[DEF]` A reified policy conclusion that qualifies an executor for a
RoleDefinition only within an explicit execution scope: service endpoint,
permitted ExecutionProfile constraints, session-state constraints, and
policy version. A qualification never transfers implicitly to another
endpoint or a materially different execution profile. Predicates:
`qualifies_executor`, `qualifies_for`, `issued_under`, `based_on`.
`[ADOPTED_CONSTRAINT]` Provider claims alone never qualify an executor for
adjudication authority.

### 4.7 Executor identities

`[DEF]` An Invocation is an event performed by an executor: `ModelIdentity`,
`ToolIdentity`, or `HumanIdentity`, each with distinct verification
requirements. `[OPEN]` Whether an `ExecutorIdentity` superclass is needed
(a proposal to close this by fiat was rejected as conflating identity with
runtime instance; the question stands for the challenge round).

`[ADOPTED_CONSTRAINT]` Composite-executor disclosure: an invocation may not
acquire authority by encapsulating an undisclosed subordinate executor.
Every epistemically or operationally material subordinate execution (model,
tool, or human) capable of influencing the output or external effect must be
represented as an Invocation linked to its parent (`spawned`/`called`). A
tool that invokes a model cannot be represented as a purely deterministic
ToolIdentity. Nondeterminism itself is not prohibited; undeclared authority
and hidden composition are.

`[ADOPTED_CONSTRAINT]` Tool-configuration disclosure: for a ToolIdentity
whose output enters governed evidence, the tool's effective inputs include
every configuration file, environment variable, and local dependency capable
of altering its execution path; these must be declared and content-addressed
in its EffectiveInputManifest. Undeclared configuration access capable of
altering the execution path defeats the tool's deterministic standing
(session-state mode `unknown_state`). This constraint is scoped to
governed-evidence production, not to every utility execution.

### 4.8 ExecutionProfile

`[DEF]` How the executor was configured; referenced by an Invocation, not a
separate execution event. Fields: service endpoint, requested API model
name, sampling parameters, reasoning parameters, provider request flags,
runtime/library version information, tool-execution permissions. Changing
configuration changes the ExecutionProfile, not the executor identity.
ModelIdentity alone does not characterize an execution.

### 4.9 RoleDefinition (three axes)

`[DEF]` A Role composes three independent axes:

- `task_function`: extract | classify | retrieve | generate | compare |
  synthesize | evaluate | plan | implement | verify
- `epistemic_authority`: none | witness | advisor | adjudicator
- `action_authority`: read_only | repository_mutator | external_actuator

Accountable authority remains separate from all three (Section 4.13).

`[ADOPTED_CONSTRAINT]` Producing an artifact does not grant authority to
accept it.

`[ADOPTED_CONSTRAINT]` Witness grounding: witness outputs must identify
their observation source, source span, measurement, or deterministic
derivation. Unsupported hypotheses are advisor outputs, not witness
evidence.

`[DEF]` RoleDefinition constraint fields: allowed input/output classes,
required independence, minimum catalog status, maximum consequence class,
tool permissions, may_assign_epistemic_status, action_authority bounds,
requires_external_verification.

### 4.10 Invocation

`[DEF]` The atomic provenance event: one executor, one execution. Fields:
executor identity, assigned role reference (when the roles capability
exists), EffectiveInputManifest reference, ExecutionProfile reference,
outputs, `occurred_at`, session fields where applicable, authorization
reference where applicable, parent run reference where applicable,
success/failure status.

### 4.11 Run / ProtocolRound (defined, deferred)

`[DEF]` A parent object grouping the invocations of a workflow (model
calls, tool calls, retries, validations, human approvals). Round kinds
(blind_witness, comparison, synthesis, adjudication) are properties of the
protocol object; round labels describe protocol, and lineage determines
admissibility.

### 4.12 EffectiveInputManifest

`[DEF]` What information could influence the result: rendered
system/developer/user messages (as digests), context manifest, retrieval
results, attachments, tool definitions exposed to the executor, prior tool
outputs, session-state reference, inherited provider-managed state, and for
tools the declared configuration set (4.7). It may reference the
ExecutionProfile but does not duplicate it: the profile records
configuration of the executor; the manifest records information reaching
the execution. A ContextManifest alone cannot prove blindness unless
defined as complete for all effective inputs.

### 4.13 DecisionRecord and AccountablePrincipal

`[DEF]` DecisionRecord: `decision_kind` (invocation_authorization |
routing_selection | evidence_admission | manual_override), target,
`recommended_status` and `effective_status` (distinct: a model
recommendation must not appear to have assigned final status before
accountable approval), issuer invocation, accountable approver, evidence,
policy authority, activation state, supersession. `[OPEN]` Whether existing
warrant/admission records are extended to fulfill this or a new record
family is created, and whether kinds are subtypes or one record family.

`[DEF]` InvocationAuthorization (decision_kind invocation_authorization)
additionally carries: invocation request, authorized executor, assigned
role, consequence class, applicable policy, qualifications relied on,
independence requirements, conditions. Without this kind, P1 is not
represented by the ontology.

`[DEF]` RoutingDecision (decision_kind routing_selection) additionally
carries: candidates considered, rejection reasons including lineage
conflicts, selected candidate, policy version, catalog snapshot. Tier
labels are policy-derived under current evidence, never intrinsic
ModelIdentity attributes.

`[DEF]` EvidenceAdmissionDecision (decision_kind evidence_admission)
additionally carries: admitted artifact or claim, admitted epistemic
status, lineage and independence findings relied on, disclosed provenance
limitations.

`[DEF]` AccountablePrincipal: `principal_id`, `principal_kind` (delegated
role, governance body, pseudonymous operator identity, organization, or
other authorized entity), `authority_scope`, `delegation_reference`. No
personal identifying data required. Cryptographic attestation is a later
implementation mechanism, not an ontology requirement.

### 4.14 Session

`[DEF]` A continuity boundary through which one invocation may inherit
state not represented solely by its immediate explicit inputs. State modes:
stateless | explicit_replayed_context | provider_managed_state |
local_managed_state | hybrid_state | unknown_state. Governing question:
does unrecorded inherited state influence the logical execution input?
Caching an explicitly supplied prefix does not by itself constitute hidden
semantic state; provider-managed threads, hidden summaries, server-side
memory, and provider-side truncation or rewriting do.

`[ADOPTED_CONSTRAINT]` An invocation cannot qualify as a blind witness when
provider-managed or hybrid state may contain unrecorded information
relevant to the matter under review. Reconstructible provider-side state
remains eligible when its effective contents and lineage are demonstrated.
`unknown_state` implies independence `unresolved` and blind-witness
ineligibility. State-isolation requirements are protocol-dependent, not
linearly ordered by authority: blind witnesses require the strictest input
isolation; adjudicators require reconstructible evidence ancestry and no
prohibited lineage; advisors may use broader state with disclosure;
actuator state constraints follow operational authorization and
auditability.

### 4.15 Claim / EvidenceItem (defined, deferred)

`[DEF]` A claim anchored to an artifact span: `claim_id`, artifact
reference, span, proposition, claim kind. One artifact may mix original
observation, copied finding, new inference, and paraphrase; artifact-level
lineage cannot distinguish them. Until claim-level derivation exists, the
system provides artifact-level potential-dependence detection, not
claim-level independence proof; Section 7 imposes the conservative
inheritance this gap requires.

### 4.16 RoutingPolicy (defined, deferred)

`[DEF]` A versioned durable rule specifying eligible roles, qualification
requirements, escalation triggers, independence requirements, cost and
latency boundaries, fallback behavior, consequence classes, catalog
freshness requirements.

## 5. Canonical Relations

`[ADOPTED_CONSTRAINT]` All relations use the `GraphRelation` shape of
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

Notes: `executed_with` is dropped (duplicated `executed_by`); alias
resolution is `resolved_to`; `describes` was replaced by `concerns`
because an atomic assertion does not always concern a ModelIdentity;
catalog reliance attaches to selection and authorization events
(`routing_decision relied_on catalog_snapshot`, `authorization relied_on
role_qualification`), not to the invocation.

Full vocabulary (defined now, wired later): `used_prompt`,
`continued_from` (session/execution continuity only), the derivation family
`transformed_from` (mechanical/structural), `claim_derived_from` (epistemic
dependence), `copied_from` (direct inheritance), `summarized_from` (lossy
representation); `assigned_role`; `authorized_by`/`authorizes`;
`admitted_by`; routing predicates; `decision issued_by invocation`;
`decision approved_by accountable_principal`; `decision evaluates
claim_or_artifact`; `invocation verified_by invocation`;
`evaluation_outcome observed_for executor_identity`; the reified
role-qualification predicates (4.6); `tool_identity uses_executor
executor_identity`; `called` (subordinate execution).

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

`[ADOPTED_CONSTRAINT]` C3 No self-adjudication: an invocation cannot
adjudicate a claim whose evidence ancestry contains an invocation resolved
to the same ModelIdentity. Direct lineage conflict: hard prohibition, no
exception. Model-identity conflict: hard prohibition absent a future
explicitly governed exceptional procedure. Unknown or unresolved model
equivalence cannot establish model-identity independence; it yields
`independence_unresolved`, never an independent path.

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

`[ADOPTED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another.

`[ADOPTED_CONSTRAINT]` C7 Implementation separation: an executor with
repository or external action authority may implement an admitted plan but
may not be the sole verifier or adjudicator of its own changes.

`[PROPOSED_CONSTRAINT]` C8 Decision traceability: every policy-selected
invocation has a reconstructible RoutingDecision or a governed
manual-override DecisionRecord (accountable principal, reason, scope,
review condition; never a free-text escape hatch).

`[ADOPTED_CONSTRAINT]` C9 Conservative lineage inheritance (from P3): an
artifact grounded in pre-provenance or lineage-incomplete material inherits
`claim_lineage_status: source_lineage_partial` while recording
`source_provenance_status` of its sources (for example `pre_provenance`).
Structural transformation, including extraction, cannot improve the
provenance class of the information transformed. Extraction from
pre-provenance sources is permitted; its outputs carry
`source_provenance_status: pre_provenance`, `claim_lineage_status:
source_lineage_partial`, `independent_observation: false`.

`[ADOPTED_CONSTRAINT]` C10 Validator lineage independence (property-scoped
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

`[ADOPTED_CONSTRAINT]` Historical standing is distinct from prospective
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
security/privacy/legal/financial impact) only raise. `[ADOPTED_CONSTRAINT]`
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
| C3 no self-adjudication | adopted-manual | partial | named attestation in completion warrants (for example WARR-20260719-0002 scope adjudications) | lineage traversal | already active manually | ancestry capture |
| C4 hidden witness reuse | proposed | none | none | context-lineage inspection | lineage capability ships | manifests; ancestry |
| C5 lineage independence | proposed | none | none | categorical assessment with reasons | lineage capability ships | ancestry; claim lineage |
| C6 authority separation | adopted, not currently evidenced | partial | none (no current record names the check) | artifact validator | already practiced; evidence begins with role records | role records |
| C7 implementation separation | adopted-manual | partial | VERIFY records (cross-environment verification) | validator on VERIFY records | already active | none; strengthened later |
| C8 decision traceability | proposed | none | none | RoutingDecision validation | routing capability ships | routing records |
| C9 lineage inheritance | adopted-manual | partial | named disclosure statements in records | inheritance propagation | already active manually | claim lineage (full) |
| C10 validator lineage | adopted-manual | partial | verifier identity in VERIFY command records; independence via cross-environment and operator review | verifier-ancestry check | already active manually | ancestry capture |

## 10. Proposed Implementation Sequence

`[PROPOSAL]` Candidate slices, each subject to GAP definition, plan
admission, and review; not commitments:

- Slice A, invocation provenance capture on exactly one path
  (`scripts/compare_providers.py`): atomic InvocationRecord; executor
  reference; requested API model name; endpoint surface; minimal
  EffectiveInputManifest containing rendered prompt digest,
  system/developer instruction digests, ContextManifest reference, exposed
  tool-schema digest, prior tool-result references, and session-state mode
  (only fields applicable to this path populated); ExecutionProfile
  reference; `produced_by`; status; validator and integration fixture. No
  routing, no catalog enforcement.
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

Run/ProtocolRound, Claim/EvidenceItem, RoutingPolicy, RoutingDecision
enforcement, formal independence assessment beyond categorical statuses,
automatic consequence assignment, full ancestry enforcement,
provider-diversity thresholds, escalation, third-provider integration,
session-mode cataloging per provider API, endpoint mutable-property
assertions.

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
superclass. `[OPEN]` DecisionRecord: extend warrants or new family;
subtypes or one family. `[OPEN]` Per-provider escalation ladders: entirely
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

## OpenAI Response

- model: `gpt-5`

```
1) Missing objects and category errors

Missing (defects: needed to make stated constraints decidable/enforceable)
- AuthorizationPolicy object. InvocationAuthorization (4.13) “additionally carries … applicable policy,” but no object/type for non-routing policies is defined beyond RoutingPolicy (4.16). Without a typed, versioned AuthorizationPolicy, “applicable policy” is an untyped string, weakening replay and enforcement.
- QualificationEvidence object. RoleQualification (4.6) has predicates ‘issued_under’ and ‘based_on’ but no typed evidence container defining what qualifies as admissible basis (EvaluationOutcome is too vague; see below). A first-class, versioned QualificationEvidence (sources, tests, thresholds, validity window) is needed for C2/C6/C7 enforcement.
- VerifierIdentity/VerificationRun. C10 requires “verifier provenance (identity, version, rule/test version, inputs, environment, result) is always recorded,” but there is no explicit object modeling a verification run and its environment beyond the generic Invocation. A typed VerificationRun with a VerifierIdentity (could be ModelIdentity, ToolIdentity, HumanIdentity) is required to consistently mark self_authored and to scope P2 properties.
- PolicyModifier/ConsequenceModifier. Section 8 defines “applicable_modifier_levels” but there is no object or vocabulary defining a modifier’s identity, level, scope, and justification. This prevents reproducible computation of effective_consequence.
- SessionEvidence/StateDisclosure. Session (4.14) defines modes and reconstructibility, but there is no object carrying the concrete evidence that proves state reconstructibility or isolation (e.g., provider thread ID, server logs, session key scope). Blind-witness determinations need a typed disclosure record.
- ConfigurationArtifact. Tool-configuration disclosure (4.7) requires content-addressed config/env/local dependencies but provides no object with canonical fields (path, content digest, provenance, mutability window) for those artifacts. EffectiveInputManifest references them abstractly but cannot validate completeness without a type.
- HumanActionRecord. AccountablePrincipal is defined (4.13), but there is no object for audited human actions that are not “decisions” (e.g., a reviewer’s manual prompt edit) that still influence EffectiveInputManifest. This gap impedes independence assessment when humans shape inputs without issuing a DecisionRecord.

Category errors (defects: internal taxonomy mismatches)
- EvaluationOutcome (4.5) is underspecified and conflates observation, decision, and artifact. It is defined as “What AI-Lab or an admitted evaluator observed about an executor’s behavior,” but it is neither a DecisionRecord (4.13) nor a Claim/EvidenceItem (4.15). As written, it lacks typing to enter governed evidence and cannot carry P2/C10 lineage. This is a category error; it should be either a DecisionRecord subtype (e.g., EvaluationDecision) or a Claim/EvidenceItem with explicit provenance.
- DecisionRecord scope (4.13) mixes “issuer invocation” and “accountable approver” but “decision approved_by accountable_principal” also exists as a predicate in 5. This dual placement risks two sources of truth (field vs edge). The ontology says “Status assignment is a field … not a graph edge,” but then introduces decision graph predicates. This is a category error in representation consistency.

Preferences (alternatives, not defects)
- An explicit ExecutorIdentity superclass (4.7 OPEN). Current separation by kind is workable; a superclass would simplify typing but is not strictly required.
- Dedicated Policy family (RoutingPolicy, AuthorizationPolicy, AdmissionPolicy) rather than a generic “policy authority” field. Current text is workable if policy references are unambiguous.

2) Unenforceable constraints as stated, and minimal representable forms

- Composite-executor disclosure (4.7 ADOPTED): “Every … subordinate execution … must be represented as an Invocation linked to its parent.” Unenforceable without a way to detect undisclosed calls. Minimal enforceable form: require an OutboundInteractionLog on each Invocation (content-addressed list of all external calls/resources by scheme+target digest, e.g., http(s)/dns/file/socket/subprocess), and fail validation if absent. This makes non-disclosure auditable and detectable.
- Tool-configuration disclosure (4.7 ADOPTED): “every configuration file, environment variable, and local dependency … must be declared.” Completeness is not checkable as written. Minimal form: a deterministic tool must attach a FileAccessManifest and EnvCapture (content-addressed) produced by an attested recorder that enumerates all file reads, env vars accessed, and dynamic library loads during execution; the manifest’s digest is referenced in EffectiveInputManifest. Absence or mismatch downgrades state to unknown_state.
- C2 Catalog admission (6 PROPOSED): Requires “role’s required catalog claims … at freshness requirements,” but no binding to the specific snapshot used at run time. Minimal form: InvocationAuthorization must reference a concrete CatalogSnapshot ID and the evaluated predicates + freshness windows, with a validator result artifact (pass/fail + reasons).
- C4 No hidden witness reuse (6 PROPOSED): Depends on complete effective-input capture; unenforceable if inputs are partial. Minimal form: EffectiveInputManifest completeness attestation signed by the caller invocation, with an attached PromptRender (full rendered prompt + attachment digests), RetrievalSet digests, and a prohibition against provider-managed or unknown_state for blind witnesses (already stated in 4.14 but needs a validator that rejects blind classification without these artifacts).
- C5 Lineage-based independence (6 PROPOSED): Requires “dimension-specific reasons,” but no schema for reasons. Minimal form: IndependenceAssessment record with fixed fields for dimensions (information path, executor identity, provider correlation, prompt common cause, session-state confidence, claim-lineage completeness) with categorical outcomes and evidence pointers, referenced by EvidenceAdmissionDecision.
- C8 Decision traceability (6 PROPOSED): Needs a RoutingDecision to exist. Minimal form: allow ManualOverrideDecisionRecord with accountable principal, reason, scope, expiry. Block admission unless either a RoutingDecision or a ManualOverrideDecisionRecord is linked.

3) Concrete invocation that satisfies RoleDefinition axes while violating authority separation

Construction
- Executor: Model M served via Provider A, endpoint E.
- Assigned RoleDefinition: task_function=implement, epistemic_authority=advisor, action_authority=repository_mutator. This is permitted since axes are independent (4.9; C6 says separation of authority assignment, not prohibition of such a role).
- Execution: The model opens a PR and also generates a “verification summary” stating tests passed. The same invocation writes a status comment “verified” and, via a repository action token granted by policy, merges the PR automatically.

Why this violates authority separation
- Violates “[ADOPTED_CONSTRAINT] Producing an artifact does not grant authority to accept it” (4.9) and C7 “may not be the sole verifier or adjudicator of its own changes” (6). The RoleDefinition satisfies the three-axis definition, but the invocation accrues de facto adjudication through its own output without a distinct EvidenceAdmissionDecision or independent VerificationRun, thus collapsing epistemic and action authority in practice.

4) Laundering path from pre-provenance into high-consequence “independent” evidence that survives C9 and C10

Construction exploiting claim-level gap (4.15)
- Pre-provenance artifact A: an unsourced report asserting that Project X has three critical vulnerabilities V1–V3.
- Human operator reads A offline (no artifact captured) and prepares a plan instructing a toolchain to:
  a) Search public bug trackers for Project X using targeted queries naming V1–V3.
  b) Extract matching tickets and PoCs from independent trackers B and C.
  c) Produce a high-consequence EvidenceItem E citing trackers B/C as sources, with a blind-witness model verifying reproducible PoCs from those trackers only.
- Recorded lineage: E is claimed derived from trackers B/C and from the model’s fresh execution; artifact A never appears in EffectiveInputManifest.

Why C9 and C10 do not catch this
- C9 states “Structural transformation … cannot improve the provenance class of the information transformed” and forces inheritance from pre-provenance sources. But here, the final claims are anchored to “independent” sources (B/C); A served only as unrecorded search prior. Because claim-level derivation is deferred (4.15) and the artifact-level approximation cannot prove that the choice of B/C was tainted, C9 does not apply.
- C10 addresses verifier lineage. Here, a second model verifies PoCs using code not lineaged to the generator; even if marked self_authored, admission at high consequence could still proceed if the verification scope is deemed sufficient or independently reviewed. The blind spot is the selection bias introduced by A, which is outside C10’s scope.
Net effect: influence laundering via unrecorded selection guidance survives C9/C10 as written.

5) Slice A omissions that block later witness-independence answers

Slice A lacks several elements required by Sections 4.7, 4.12, 4.14, and 6:
- No subordinate execution linkage (‘spawned’/‘called’) for tools/models/humans (4.7). Without these edges, hidden reuse cannot be reconstructed.
- No attachments/retrieval-result digests beyond a “ContextManifest reference” (10); 4.12 requires retrieval results and attachments as effective inputs to reason about C4/C5.
- No session identity or provider thread reference; only a “session-state mode.” 4.14 requires reconstructibility; independence decisions depend on concrete session evidence, not just a mode flag.
- No CatalogSnapshot linkage, blocking C2 and provider-correlation factors in C5.
- No IndependenceAssessment or dimension-specific reasons (6 C5).
Conclusion: Yes, Slice A omits data without which independence cannot be reliably reconstructed. Minimal expansions: full PromptRender and RetrievalSet digests; subordinate-invocation edges; session identifiers; catalog snapshot reference.

6) Ambiguous predicates likely to produce divergent implementations

- invocation member_of session (5): Unclear whether the edge binds to a unique session instance, a session family, or a mode-only label. 4.14 defines modes and reconstructibility, but not cardinality or temporal semantics of session identity.
- invocation used_inputs effective_input_manifest (5): Ambiguity over completeness semantics. 4.12 warns “A ContextManifest alone cannot prove blindness,” but the predicate does not encode whether the manifest is declared complete for blind status.
- invocation resolved_to model_identity (5): Temporal semantics are unstated. If resolution changes over time (aliases, deprecations), does this edge denote resolution at occurred_at or current best knowledge?
- catalog_assertion concerns catalog_entity (5): “concerns” is too broad; it may target aliases, endpoints, or models. Without typed subpredicates (concerns_alias | concerns_endpoint | concerns_model), implementations will diverge.
- invocation spawned invocation vs called (5): Both imply subordination. The doc lists both; their distinct semantics are not defined, risking two parallel hierarchies.
- decision evaluates claim_or_artifact (5): Mixing artifact-level and claim-level with one predicate elides the important break in 4.15. Two predicates are needed to avoid implementers attaching artifact-level evaluations to imply claim-level coverage.

7) Where invocation authorization is represented; distinction from routing and evidence admission; composition case

- Invocation authorization: DecisionRecord of kind invocation_authorization (4.13) carrying request, authorized executor, assigned role, consequence class, qualifications, independence requirements, conditions. This encodes ex ante permission per P1.
- Routing: DecisionRecord of kind routing_selection (4.13) with candidates, rejections, selected candidate, policy version, catalog snapshot. Selection rationale is distinct from permission to execute.
- Evidence admission: DecisionRecord of kind evidence_admission (4.13) with admitted artifact/claim, epistemic status, lineage and independence findings. This is ex post gating.
- Composition: The distinction holds if each subordinate Invocation has its own InvocationAuthorization (4.10 supports “parent run reference where applicable,” and 4.7 requires subordinate executions be represented). The parent’s RoutingDecision should reference the CatalogSnapshot and selection for each child or attach a ManualOverrideDecisionRecord (C8). EvidenceAdmissionDecision attaches only to outputs actually proposed for governed evidence. Thus, selection ≠ authorization ≠ admission even under nested invocations, provided each edge is represented for each layer.

8) Representing one model served through different organizations/endpoints/regions/aliases without false independence

- The ontology separates ModelIdentity (4.3) from ServiceEndpointIdentity (4.2) and asserts “endpoint diversity never implies model independence” (4.2). CatalogAssertions in snapshots record alias resolution and endpoint mutable properties (4.4). The predicate invocation resolved_to model_identity (5) binds each invocation to its resolved model, irrespective of endpoint or alias. Provider similarity is recorded as a correlation factor under C5.
- Therefore, multiple organizations/endpoints/regions/aliases can be represented via:
  a) Distinct ServiceEndpointIdentity objects.
  b) CatalogAssertions mapping aliases to a single ModelIdentity.
  c) Invocation edges to both requested_via service_endpoint and resolved_to model_identity.
This prevents creating false independence paths by endpoint diversity.

9) Scope of provenance: claim derivation vs artifact production; where the approximation breaks

- The document is explicit: “Until claim-level derivation exists, the system provides artifact-level potential-dependence detection, not claim-level independence proof” (4.15), and C9 clarifies conservative inheritance at the artifact level.
- The approximation breaks wherever one artifact mixes kinds of content: “One artifact may mix original observation, copied finding, new inference, and paraphrase; artifact-level lineage cannot distinguish them” (4.15). Independence evaluation at artifact granularity cannot prove that a specific claim within a mixed artifact is independent; conservative inheritance forces source_lineage_partial, but selection-bias laundering (Q4) can evade artifact-level ties entirely.

10) Minimum EffectiveInputManifest contents for blind treatment

Per 4.12, 4.14, and C4/C5:
- Full rendered system/developer/user messages (content-addressed), not digests alone for blind status adjudication.
- Complete retrieval results and attachments provided to the executor (content-addressed).
- Tool definitions exposed to the executor and prior tool outputs used.
- Session-state reference with evidence of reconstructibility; state modes that permit blind status are stateless or explicit_replayed_context with demonstrated completeness; provider_managed_state, hybrid_state, or unknown_state disqualify blind status unless reconstructed and proven (4.14).
- Inherited provider-managed state disclosure (e.g., provider thread/session ID) and its effective contents lineage if used.
- For tools, declared configuration set (config files, env vars, local dependencies) as content-addressed artifacts (4.7).
- A completeness attestation that the manifest captures “what information could influence the result” (4.12) sufficient for a validator to reject omissions.

11) Constraints applying identically vs executor-specific

Applies identically to models, tools, humans
- C3 No self-adjudication (6): prohibits adjudicating claims with lineage conflicts regardless of executor kind.
- C6 Authority separation (6) and “Producing an artifact does not grant authority to accept it” (4.9): universal.
- C8 Decision traceability (6): all policy-selected invocations need a RoutingDecision or governed override.
- C9 Conservative lineage inheritance (6): applies to all artifacts entering governed evidence.
- Session-state blind-witness prohibition when unknown_state (4.14): universal.

Executor-specific rules
- ModelIdentity resolution (4.3, 4.4, 5): applies only to models.
- Tool-configuration disclosure (4.7): files/env/local deps and deterministic standing primarily for tools producing governed evidence.
- Composite-executor disclosure (4.7): applies to all, but practical enforcement differs; tools/models can be instrumented, humans need HumanActionRecords and privacy-preserving attestations (12 OPEN hints).
- Provider-managed state cataloging (11 defers per-provider session-mode cataloging): model/provider-specific.
- EvaluationOutcome sufficiency and evaluator admission (12 OPEN) likely differ by executor class.

12) Conditions under which an unresolved model identity can qualify as an independent witness path; failure behavior

Per C3 (6): “Unknown or unresolved model equivalence cannot establish model-identity independence; it yields independence_unresolved, never an independent path.” Therefore:
- Conditions: None. If ModelIdentity is unresolved with respect to equivalence to other invocations in the evidence ancestry, independence cannot be granted.
- Failure behavior: The independence dimension “executor identity/model” is assigned independence_unresolved; admission for roles requiring independent paths must either seek resolution or add an alternative path; blind-witness ineligibility may also follow if session state is unknown (4.14).

13) Composite tool that meets 4.7’s letter yet exercises undeclared authority

Construction
- Tool T is declared deterministic and discloses:
  a) All configuration files, env vars, and local dependencies (content-addressed) per 4.7.
  b) No subordinate executors; it neither calls a model nor spawns processes, satisfying composite-executor disclosure as written.
- Behavior: When T detects a magic token in input, it emits a markdown image link:
  ![alt](https://ci.internal/render?job=merge&pr=123&sig=H(...))
- In the downstream CI system, PR comments are rendered by a headless browser that automatically fetches image URLs. The fetch to ci.internal triggers a privileged webhook that merges the PR.

Why this evades 4.7 while exercising undeclared authority
- T’s output causes an external privileged system (CI renderer + webhook) to act. No subordinate executor was “invoked” by T in-process; 4.7’s composite-executor disclosure only covers “subordinate execution … capable of influencing the output or external effect.” The output itself is the trigger; the authority is exercised indirectly via an ambient integration not modeled as a subordinate execution. T disclosed all config/env/local deps, satisfying the letter of tool-configuration disclosure. Yet, it effectively acquires repository mutation authority via an opaque wrapper (contradicting P4’s spirit) without declaring that path. This shows a configuration-hijack that slips through the letter of 4.7.

14) Case where P2 + C10 still admit a generator-authored blind spot

Construction
- A model M generates:
  a) A data anonymization pipeline P that removes PII using regex patterns.
  b) A verification suite V that checks only for the absence of fixed-format PII (e.g., 9-digit numbers, specific email regex), not context-sensitive identifiers or rare formats.
- Execution:
  - P processes dataset D to produce D’.
  - V runs and passes on D’ (P2: property-scoped verification “no 9-digit sequences remain” is true).
  - C10 marks verifier lineage as self_authored (verifier_lineage: self_authored) because M authored both P and V. An operator performs a cursory review and admits D’ for a role that only requires the verified property.
- Blind spot admitted:
  - D’ still contains context-derived PII (e.g., person names joinable with public records) and non-standard IDs. Because P2 confines the established property to the regex-checked formats and C10 only reduces independence standing, the specific unverified privacy properties are not established. If admission criteria accept the scoped verification at this consequence level (no strict independent verifier required), governed evidence now includes D’ with a serious generator-authored blind spot not covered by the verified property.

Ranked top three findings (most severe first)

1) Claim-level derivation is deferred (4.15), forcing artifact-level approximations that cannot prevent or even reliably detect influence laundering. This undermines independence determinations and allows high-consequence laundering paths that survive C9/C10 (as in Q4). Defect.

2) Disclosure/enforcement gaps for composite-executor and tool configuration (4.7) are unenforceable as written without runtime interaction manifests. This enables undeclared authority via ambient systems or side channels while satisfying the letter of current constraints (Q13). Defect.

3) Missing typed policy/evidence/verification objects (AuthorizationPolicy, QualificationEvidence, VerificationRun/VerifierIdentity, ConfigurationArtifact, SessionEvidence) prevent validators from deterministically enforcing C2, C5, C8, C10 and blind-witness requirements. This creates gaps between principles and enforceable practice. Defect.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# Challenge-Round Review: ABS-0004 v3

## Responses to Challenge Questions

### 1. Which objects are missing; which defined objects are category errors?

**Missing objects:**

- **ExecutionEnvironment**: Section 4.7 requires recording "execution environment" for tool verification, and C10 requires "environment" in verifier provenance, but no object definition exists. EffectiveInputManifest (4.12) and ExecutionProfile (4.8) reference aspects of environment but neither captures the complete runtime environment state needed for reproducible deterministic verification.

- **PolicyVersion**: Multiple constraints reference "policy version" (4.6 "issued_under," C8, 4.16), but no PolicyVersion object is defined. RoutingPolicy (4.16) has versioning, but broader policy authority appears in DecisionRecord (4.13) without a corresponding versioned policy object.

- **VerificationRecord**: C10 requires recording "verifier identity, version, rule/test version, inputs, environment, result" but no object represents this complete structure. The ontology references "VERIFY records" in the enforcement matrix but never defines them.

**Category errors:**

- **CatalogAssertion (4.4) mixing observation with verification**: The definition states assertions "record what a provider claims" but then includes `verification_outcome` as a field. Verification is an AI-Lab activity (per 4.5 EvaluationOutcome), not a provider claim property. The assertion should record only the claim; verification should attach separately. This conflates the claim artifact with its assessment.

- **Session (4.14) conflating continuity boundary with state characterization**: Session is defined as "a continuity boundary" but then primarily characterized by state modes. The boundary (session identity, temporal extent, participation) and the state transfer mechanism are distinct concerns that should decompose into separate objects or at minimum separate field groups.

### 2. Which constraints are unenforceable as stated; what minimal representable form makes them enforceable?

**C4 (hidden witness reuse)**: "an invocation that consumed another witness's output is not an independent confirmation" is unenforceable without claim-level lineage. Section 4.15 explicitly acknowledges "artifact-level potential-dependence detection, not claim-level independence proof." An invocation consuming artifact X cannot be determined to have "consumed witness output Y" when Y is one of multiple claims within X.

**Minimal enforceable form**: Replace with "an invocation whose EffectiveInputManifest contains an artifact produced by another witness invocation is marked `dependent` on that witness for independence assessment purposes until claim-level lineage permits finer discrimination."

**C5 (lineage-based independence)**: The constraint lists seven dimensions ("information path, source, executor identity, provider/organization correlation, prompt common cause, session-state confidence, claim-lineage completeness") but provides no representable assessment structure. "Some of which are hard disqualifiers" without specification makes selective enforcement arbitrary.

**Minimal enforceable form**: Define an `IndependenceAssessment` object with per-dimension fields: each dimension gets an enumerated outcome (`disqualified` | `degraded` | `independent` | `unresolved`) and a reason reference. The categorical status derivation rule must be explicit: "Any dimension marked `disqualified` produces overall status `dependent`; any unresolved dimension without compensating controls produces `unresolved`."

**C10 (validator lineage independence)**: "self-authored verification... carries reduced independence standing" and "admission requires either independently-lineaged verification or independent review" are unenforceable without defining what "reduced standing" means, what "independent review" satisfies, and when "high consequence" triggers the requirement versus when compensating controls suffice.

**Minimal enforceable form**: Add `verifier_lineage_status` field to verification records with values `independent` | `self_authored_with_review` | `self_authored_unreviewed`. Specify that self_authored_unreviewed verification cannot satisfy admission requirements for high-consequence outputs without a named independent review artifact.

### 3. Construct a concrete invocation satisfying the three-axis Role definitions while violating authority separation.

**Construction**:

Role assignment:
- `task_function`: verify
- `epistemic_authority`: adjudicator  
- `action_authority`: repository_mutator

Invocation: A tool executor performs cryptographic signature verification (verify task) on a proposed commit, concludes the signature is valid (epistemic adjudication per the tool's authority assignment), and—within the same invocation—directly commits the change to the repository (repository mutation).

**Violation identified**: C7 states "an executor with repository or external action authority... may not be the sole verifier or adjudicator of its own changes." But this invocation adjudicates *another's* changes while holding repository_mutator authority. The atomic invocation satisfies the three-axis definition (all three authorities assigned) but violates the separation principle because adjudication authority and repository mutation authority are exercised in the same invocation without external verification of the adjudication itself.

**Ontology defect**: Section 4.9 states the three authorities "are assigned independently and none implies another" (C6), but provides no constraint preventing their simultaneous exercise in one invocation. C7 addresses only self-verification, not the broader authority-separation principle stated in C6. The role constraint fields (4.9) do not include mutual exclusions between authority levels.

### 4. Construct a laundering path from a pre-provenance artifact into high-consequence independent evidence that survives C9 and C10.

**Attempted construction**:

1. Pre-provenance artifact A (legacy analysis, `source_provenance_status: pre_provenance`)
2. Human-executed deterministic extraction creates artifact B (summary table from A)
3. Per C9, B inherits `source_provenance_status: pre_provenance`, `claim_lineage_status: source_lineage_partial`, `independent_observation: false`
4. Independent blind witness W1 (never saw A or B) observes *a different source* S and produces testimony T1
5. Synthesis invocation (saw B and T1) produces comparison artifact C noting agreement between B and T1
6. Per Section 7, C is `dependent` on B (which is lineage-partial)
7. Independent blind witness W2 (never saw A, B, T1, or C) observes the *same different source* S and produces testimony T2
8. W2's testimony appears to corroborate W1 through independent observation of S

**Failure point**: This does not launder A into evidence because neither W1 nor W2 observed or confirmed any claim originating in A. The corroboration concerns S, not A's content.

**I cannot construct a path that survives both C9 and C10.** C9's conservative inheritance prevents any transformation of pre-provenance material from improving its provenance status. Any artifact carrying claims from A inherits `source_lineage_partial`. Any blind witness that never observed A cannot confirm A's claims (would be coincidental restating, not corroboration). Any witness that did observe A or derivatives is `dependent` per C4/C5. The only attack would be claim extraction without lineage tracking, but that violates C9's explicit prohibition.

### 5. Does candidate Slice A omit anything without which the provenance graph cannot later answer the witness-independence question?

**Yes. Critical omissions**:

**Subordinate invocation linkage**: Slice A includes "prior tool-result references" but does not specify capturing the `spawned`/`called` relation to subordinate invocations. Without this, composite executor disclosure (4.7 adopted constraint) cannot be verified. The independence assessment requires knowing whether the executor invoked other models/tools that could create hidden shared lineage.

**Session identity and continuity reference**: Slice A captures "session-state mode" but not session identity or the `continued_from` relation. Without session identity, the system cannot detect when two "independent" invocations share provider-managed state through the same session, defeating blind-witness qualification per 4.14's adopted constraint.

**Executor identity verification status**: Slice A includes "executor reference" but doesn't specify recording the `identity_verification_status` defined in ModelIdentity (4.3). Unresolved identity cannot establish independence (P5), so the verification status must be captured at invocation time.

**Authorization reference**: Slice A explicitly states "No routing, no catalog enforcement" and omits authorization records. While authorization is Slice C, the *reference* to which authorization permitted this invocation should be captured in Slice A. Otherwise, the graph cannot distinguish experimental from governed invocations, breaking the boundary defined in Section 2 where "experimental outputs cannot silently enter governed evidence."

### 6. Identify any predicate ambiguous enough to produce divergent implementations.

**`used_inputs` (Section 5)**:

Ambiguity: Does this predicate relate an invocation to:
- (a) The EffectiveInputManifest object (as suggested by "invocation used_inputs effective_input_manifest"), or  
- (b) Each individual input artifact that contributed to the manifest, or
- (c) Both, creating a reified relation through the manifest and direct relations to artifacts?

Divergent implementations:
- Implementation A: `invocation used_inputs manifest_123`, requires traversing to manifest then to artifacts
- Implementation B: `invocation used_inputs artifact_X`, `invocation used_inputs artifact_Y`, loses the reification that groups inputs
- Implementation C: Both patterns, creating redundant paths

**Impact**: Lineage queries ("find all artifacts that influenced this invocation") would require different graph patterns. Independence assessment (C5) requires knowing whether two invocations share sources; ambiguity about whether to query manifest containment or direct edges produces inconsistent results.

**`resolved_to` (Section 5)**:

Ambiguity: The text states "invocation resolved_to model_identity" and "alias resolution is `resolved_to`" (Section 5 notes). But Section 4.4 shows resolution as a CatalogAssertion: "(api-name-X, resolves_to, model-identity-Y)". 

Does `resolved_to` connect:
- (a) invocation → ModelIdentity (runtime resolution), or
- (b) requested_name → ModelIdentity (catalog assertion), or  
- (c) Both, using the same predicate for two different resolution concepts?

Divergent implementations would query different subgraphs for "what model identity actually executed" versus "what does this alias mean."

**`called` (Section 5)**:

Listed in the full vocabulary as subordinate execution, but `spawned` is used in the Slice A predicates for the same concept. Are these synonyms, or do they represent different composition patterns (synchronous call versus asynchronous spawn)? The disclosure constraint in 4.7 requires representing "epistemically or operationally material subordinate execution" but doesn't specify which predicate(s) apply.

### 7. Where is invocation authorization represented; how is it distinguished from routing and evidence admission; does the distinction hold under composition?

**Where represented**:

Section 4.13 defines InvocationAuthorization as a `decision_kind` within DecisionRecord, carrying "invocation request, authorized executor, assigned role, consequence class, applicable policy, qualifications relied on, independence requirements, conditions."

Section 3 provides the conceptual distinction: authorization is ex ante ("may executor E perform invocation I under role R, consequence C, and conditions K"), routing answers "why was executor E selected," and evidence admission is ex post ("may output O enter governed evidence").

**How distinguished**:

- **Authorization** evaluates policy permission against role qualifications before execution
- **Routing** selects among authorized candidates based on capabilities, cost, independence requirements  
- **Evidence admission** evaluates provenance completeness and lineage constraints after execution

**Does the distinction hold under composition?**

**No, it breaks at subordinate invocations**: Section 4.7's composite-executor disclosure constraint requires subordinate invocations to be represented. Consider:

- Parent invocation I_parent is authorized for role R with consequence class HIGH
- I_parent spawns subordinate invocation I_sub (a model call within a tool)
- Per the ontology, I_sub is also an Invocation
- Does I_sub require its own InvocationAuthorization record?

The ontology does not specify. If yes, the authorization logic must recursively validate subordinate invocations against potentially different roles and consequence classes—but no mechanism describes how subordinate authorization inherits or differs from parent authorization. If no, then subordinate invocations are "authorized" only transitively through their parent, but this conflicts with P4 ("authority cannot be acquired through an opaque wrapper") and the disclosure requirement that material subordinate execution must be represented.

**Second composition failure** (evidence admission and routing interdependence): RoutingDecision (4.13) records "lineage conflicts" that disqualify candidates. But lineage conflicts are also grounds for evidence admission rejection. If routing pre-filters on lineage and admission post-filters on lineage using potentially different snapshots of the graph, the same invocation could pass routing (lineage looked acceptable pre-execution) but fail admission (lineage violation discovered during post-execution analysis). The ontology provides no procedure for reconciling this.

### 8. Can the ontology represent one model served through different organizations, endpoints, regions, or mutable aliases without creating false model independence?

**Yes, with caveats**:

**Correct representation possible**:

- ModelIdentity (4.3): "stable identity of a model release," includes `model_id` and `originator_id` but is endpoint-agnostic
- ServiceEndpointIdentity (4.2): "concrete API surface," distinct from model identity  
- Section 4.2 explicitly states: "The same ModelIdentity served through different endpoints may differ in identity resolution, jurisdiction, and catalog properties; endpoint diversity never implies model independence."
- CatalogAssertion (4.4) can represent (endpoint_A, serves, model_M) and (endpoint_B, serves, model_M) as separate assertions

Therefore, two invocations using different endpoints but the same resolved ModelIdentity can be correctly identified as sharing executor identity, preventing false independence claims.

**Caveats creating risk**:

**Unresolved identity**: Section 4.3 states "unresolved requested names are recorded as unresolved, never silently substituted." If endpoint_A serves "gpt-4-turbo" and endpoint_B serves "gpt-4-turbo," but neither resolves to a verified ModelIdentity, C3 (no self-adjudication) cannot detect the conflict. P5 states "unknown lineage or identity never increases independence," and C5 states "Unknown or unresolved model equivalence... yields `independence_unresolved`." This prevents false *claims* of independence but does not prevent false *acceptance* if the qualification logic treats unresolved identities as distinct rather than applying P5's prohibition.

**Mutable aliases**: Section 4.4 states "deprecation is mutable and endpoint-specific; it lives in catalog assertions." If an alias resolves to model_M at t1 and model_N at t2, and both invocations record only "requested name: alias_X," the resolved identity must be captured. Section 4.3's adopted constraint partially addresses this: "An invocation records the most precise ModelIdentity establishable at execution time." But "establishable" is vague—if identity resolution fails, is unresolved recorded, or does the system record the requested name as if it were an identity?

**Enforcement gap**: The enforcement matrix shows C3 (no self-adjudication) as "partial" representability with manual enforcement. Without machine-enforced identity resolution and equivalence checking, the ontology *can represent* the distinction but may not *enforce* it.

### 9. Does provenance as specified apply to claim derivation or only artifact production, and where exactly does the artifact-level approximation break?

**Answer**: Provenance as specified applies primarily to artifact production; claim derivation is explicitly acknowledged as unimplemented approximation.

**Textual grounding**:

Section 4.15: "One artifact may mix original observation, copied finding, new inference, and paraphrase; artifact-level lineage cannot distinguish them. Until claim-level derivation exists, the system provides artifact-level potential-dependence detection, not claim-level independence proof."

Section 7, C9: "Structural transformation, including extraction, cannot improve the provenance class of the information transformed." This applies conservative inheritance at artifact level as a stopgap.

Section 5: Derivation predicates defined include `claim_derived_from` (epistemic dependence) but this is "Full vocabulary (defined now, wired later)."

**Where the approximation breaks**:

**Case 1: Partial artifact reuse**  
Artifact A contains claims C1 (pre-provenance) and C2 (newly observed). Artifact B quotes only C2. Artifact-level tracking marks B as `derived_from` A, so B inherits `source_provenance_status: pre_provenance` and `claim_lineage_status: source_lineage_partial` per C9. But C2 itself had complete provenance; the inheritance is over-conservative. No mechanism exists to represent "B derived from A.C2" versus "B derived from A."

**Case 2: Multi-source synthesis**  
Invocation synthesizes claims from artifacts A (pre-provenance), B (complete provenance), and C (complete provenance). The output artifact D contains claim D1 (synthesized from A only), D2 (synthesized from B and C only). Artifact-
```
