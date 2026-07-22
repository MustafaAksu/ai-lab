# ABS-0004: Abstraction — Invocation Authorization Ontology

## Metadata

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v5` (v1, v2 superseded during drafting and never entered the
  record; v3 entered the record at commit 6802cf7 and underwent the
  COMP-0032 challenge round; v4 applied the twelve adjudicated findings and
  was admitted at 56f18a2; v5 is a narrow amendment replacing
  CatalogVerification with CatalogCapture on the COMP-0035 finding, adopted
  by the operator as accountable principal)
- abstraction_level: `2`
- status: `admitted`
- admitted_at: `2026-07-20`
- admission basis: survived the COMP-0032 challenge round; all twelve
  adjudicated findings applied in this revision; admitted by the operator
  as accountable principal in session (recorded in conversation; structural
  DecisionRecord representation awaits Slice C)
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
- COMP-0032 (challenge round on v3; isolated inputs; both witnesses
  independently ranked the claim-level lineage gap and undeclared external
  authority as the two most severe defects; one witness reported honest
  failure to construct a derivation-based laundering path, sharpening the
  surviving attack class to selection- and copying-based paths outside the
  recorded graph; incident chain of response truncation and one
  confabulated continuation recorded in the artifact itself).
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

`[DEF]` Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

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
requirements. `[OPEN]` Whether an `ExecutorIdentity` superclass is needed.
A proposal to close this by fiat was rejected as conflating identity with
runtime instance; COMP-0032 reopened the question with a stronger argument:
a superclass with identity-equivalence semantics defined per subtype would
make constraints such as C3 properly polymorphic across executor kinds.
The question stands, now with that argument on record.

`[ADOPTED_CONSTRAINT]` Composite-executor disclosure: an invocation may not
acquire authority by encapsulating an undisclosed subordinate executor.
Every epistemically or operationally material subordinate execution (model,
tool, or human) capable of influencing the output or external effect must be
represented as an Invocation linked to its parent (`spawned`). A
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

`[ADOPTED_CONSTRAINT]` External-interaction disclosure: an invocation's
action-authority surface includes its interactions with external systems
that are not executors — network calls, external writes, and systems that
render, fetch, or execute its outputs with privileges (ambient consumers).
For executors producing governed evidence or holding above-read_only action
authority, material external interactions must be declared; undeclared
external interaction defeats deterministic standing and constitutes
undisclosed `external_actuator` authority, violating P4 regardless of
whether the returned output bytes were affected. Hardcoded interaction
targets are interactions, not exemptions. COMP-0032 produced three distinct
constructions defeating the previous two disclosure constraints alone
(configuration hijack, ambient output-triggered actuation, hardcoded
exfiltration); this constraint closes the class. Enforcement object:
OutboundInteractionLog (Section 11).

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
requires_external_verification, `required_verified_properties` (the
properties that must be established by admissible verification before this
role's outputs enter governed evidence; schema conformance is not claim
accuracy).

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
limitations, and an enumeration of verified properties against the
receiving role's `required_verified_properties`; admission may not treat a
property as established that no named verification record covers.

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
inheritance this gap requires, and C11 imposes the interim
high-consequence disclosure this gap requires.

### 4.16 RoutingPolicy and AuthorizationPolicy (defined, deferred)

`[DEF]` RoutingPolicy: a versioned durable rule specifying eligible roles,
qualification requirements, escalation triggers, independence requirements,
cost and latency boundaries, fallback behavior, consequence classes,
catalog freshness requirements.

`[DEF]` AuthorizationPolicy: a versioned durable rule governing invocation
authorization: role eligibility conditions, consequence ceilings,
subordinate-execution classes permitted for inheritance (Section 3),
required qualifications and independence, exception procedures. All policy
references in DecisionRecords (`applicable policy`, `issued_under`,
`policy authority`) are typed references to a versioned policy object,
never untyped strings.

### 4.17 VerificationRun (defined, deferred)

`[DEF]` The typed record C10 requires: verifier executor reference,
verifier version, rule/test version, inputs (content-addressed),
execution environment, result, and `verifier_lineage_status`
(`independent` | `self_authored_with_review` | `self_authored_unreviewed`).
Self-authored-unreviewed verification cannot satisfy admission for
high-consequence outputs; the named independent review artifact converts
the status to `self_authored_with_review`.

### 4.18 IndependenceAssessment (defined, deferred)

`[DEF]` The typed record C5 requires: one field per dimension (information
path, source, executor identity, provider/organization correlation, prompt
common cause, session-state confidence, claim-lineage completeness), each
with an enumerated outcome (`disqualified` | `degraded` | `independent` |
`unresolved`) and a reason reference. Derivation rule: any dimension
`disqualified` yields overall status `dependent`; any dimension
`unresolved` without a named compensating control yields overall
`unresolved`; otherwise `qualified_independent` with degradations listed.

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
    catalog_capture captured catalog_assertion

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

`[ADOPTED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
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

`[ADOPTED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another. Assignment independence
is not exercise license: adjudicator-level epistemic authority and
above-read_only action authority may not both be exercised within a single
invocation against the same target unless the adjudication is covered by
an independent verification edge; an invocation that mutates state it also
adjudicates collapses the separation C6 exists to preserve. COMP-0032
produced two constructions satisfying the axis definitions while defeating
separation; this sentence closes both.

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

`[ADOPTED_CONSTRAINT]` C11 Interim independence disclosure: until
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
