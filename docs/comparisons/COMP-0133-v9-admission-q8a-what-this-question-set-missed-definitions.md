# COMP-0133: Provider Comparison — v9 admission Q8a what-this-question-set-missed-definitions

## Metadata

- comparison_id: `COMP-0133`
- title: `v9 admission Q8a what-this-question-set-missed-definitions`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-0411dbd630ff8c3c.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0133", "target_id": "INV-0411dbd630ff8c3c"}, {"authoritative": false, "evidence": "docs/invocations/INV-d72509ba562103c9.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0133", "target_id": "INV-d72509ba562103c9"}]`
- created_at: `2026-08-10T10:36:10.727900+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q8a what-this-question-set-missed-definitions You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

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

=== QUESTION Q8a ===
The eight questions in this round were written by the executor that drafted v5, v6, v7 and v8, every one of which was withdrawn or superseded. It drafted none of v9.

Someone who has failed four times at a document tends to probe the places they failed.

YOU ARE SEEING PART OF THE DOCUMENT. Below are the metadata, evidence inputs, and Sections 1 through 4: anchoring principles, scope, the three decisions, and the object definitions. Sections 5 through 13 are being reviewed by the same question in a separate call. The whole document did not fit in one call: at 17,533 input tokens it exhausted the entire output budget on reasoning and returned no text, which is the same failure that produced the empty response in COMP-0038. Say so if the split prevents you from answering.

Read what you can see as though no review round had happened. Find what is weakest in it. Then report anything significant that this question set does not ask about, and anything that is unsound rather than merely incomplete.

=== EVIDENCE ABS-0004 v9, metadata and Sections 1 to 4 (of 13) ===
# ABS-0004: Abstraction — Invocation Authorization Ontology

## Metadata

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v9`
- abstraction_level: `2`
- status: `proposed`
- reconstruction baseline: admitted v4 at commit
  `56f18a2ab7b66b1855b631a32d540f654c62b2c2`. Assembly does not admit v9;
  v9 requires its own admission review.
- version admission table:

  | version | state | basis |
  | --- | --- | --- |
  | v1, v2 | superseded during drafting | never entered the record |
  | v3 | superseded | entered the record at 6802cf7; underwent the COMP-0032 challenge round |
  | v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only |
  | v5 | amended, not separately admitted | replaced CatalogVerification with CatalogCapture on the COMP-0035 finding, at 6d7dfee |
  | v6 | amended, not separately admitted; superseded | proposed an authorization-chain termination that both COMP-0037 reviewers broke independently, at 8a1399f |
  | v7 | amended, not separately admitted | replaced v6's termination rule, at 00335d6; reviewed by COMP-0039..0046 |
  | v8 | **withdrawn_after_admission_review** | reviewed by COMP-0118..0125 and withdrawn under DECISION-20260727-0002; retained as evidence, not rejected, and not an implementation authority |
  | v9 | **proposed** | reconstructed from admitted v4 using the literal task 2, task 3, and identity-status text accepted under DECISION-20260727-0004, DECISION-20260727-0005, and DECISION-20260805-0001; assembled under DECISION-20260805-0002; pending its own admission review |

- reconstruction inputs:
  `ABS-0004-v9-task2-required-changes.patch`,
  `ABS-0004-v9-task3-limitations.patch`,
  `ABS-0004-v9-identity-status.patch`, and
  `ASSEMBLY_RULE_CORRECTION.md`, retained under
  `docs/self_model/v9_reconstruction/`.
- authors: operator (adjudicating principal); inherited v4 text drafted by an
  executor self-reported as "Claude"; v9 reconstruction text and assembly by
  the reviewing executor self-reported as `gpt-5.6-thinking`; both executor
  identities are unverified testimony; with attributed advisor contributions
  described in Evidence Inputs.
- sentence discipline: every normative statement is tagged `[DEF]`
  definition; `[PRINCIPLE]` architectural principle;
  `[PROPOSED_CONSTRAINT]` constraint proposed for adoption;
  `[INHERITED_CONSTRAINT]` constraint text carried forward unchanged from the
  admitted v4 baseline. Its current governance force derives from v4's
  admission, not from the proposed v9 document. A substantive change becomes
  `[PROPOSED_CONSTRAINT]` until separately admitted; `[COMMIT]` commitment
  concerning the preparation of this document; `[PROPOSAL]` candidate
  implementation boundary subject to future governance; `[OPEN]` open
  question; or `[LIMITATION]` descriptive boundary on what the ontology, its
  records, or current enforcement establish. A limitation imposes no
  constraint and claims no adoption. Untagged prose binds nothing.

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

`[LIMITATION]` A verification result supports only the property it names. It
does not by itself justify a broader epistemic status or establish truth,
grounding, calibration, privacy, or any other unverified property.

`[PRINCIPLE]` P3. Complete production provenance does not imply complete
claim provenance. A newly produced artifact must not erase the provenance
limitations of the claims it carries.

`[PRINCIPLE]` P4. Authority cannot be acquired through an opaque wrapper.
Encapsulation does not launder authority.

`[PRINCIPLE]` P5. Unknown facts block qualification; they never disappear
from the vocabulary. Uncertainty remains representable (`unknown_state`,
`unresolved`, `pre_provenance`), and unknown lineage or identity never
increases independence.

`[LIMITATION]` Distinct identifiers, endpoints, or invocation records do not by themselves
establish distinct executor identities. When executor-kind-specific
equivalence cannot be resolved, independence remains unresolved.

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

`[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and
authorization records can state and attribute authority claims. Repository
records do not by themselves establish a principal's extra-systemic
entitlement to govern.

`[LIMITATION]` A recorded authorization-chain terminus identifies where the
represented chain stops. It does not by itself establish that the underlying
invocation is substantively authorized.

`[LIMITATION]` Record and relation requirements expose only what was declared,
recorded, linked, traversable, and correctly attributed. They do not establish
that every material invocation, authorization, input, dependency, or external
interaction is present in the record.

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
release/version identity where establishable. Deprecation is mutable and
endpoint-specific; it lives in catalog assertions.

`[DEF]` An invocation's event-time identity resolution and the current
assessment of that resolution are distinct facts. The event-time resolution is
bound to the evidence available when the invocation occurred. A later
assessment is recorded separately and linked to that historical resolution.

`[DEF]` `identity_verification_status` is the immutable capture-time status of
the executor reference in an InvocationRecord. It is not a later identity
resolution outcome or the current assessment of one. `unresolved` means
the capture path did not establish an executor-kind-specific stable identity.
`verified` means an admitted capture path established a unique identity under a
property-scoped verification rule and durably recorded or referenced the
identity, supporting evidence, verifier, rule or test version, and verification
time.

`[LIMITATION]` InvocationRecord schema v1 accepts `verified`, but no admitted
schema-v1 capture path can presently substantiate it: the current path performs
no identity resolution, and provider catalog self-report, even over an
authenticated channel, does not independently establish a model mapping. It
therefore emits `unresolved`. Later append-only identity resolution records do
not mutate or upgrade this field; validator acceptance of `verified` is
syntactic compatibility, not a licensed status.

`[PROPOSED_CONSTRAINT]` An invocation records the most precise ModelIdentity
resolution establishable from evidence available at execution time; an
unresolved requested name is recorded as unresolved and is never silently
substituted. Later evidence that a relied-on catalog assertion was stale,
contradicted, or wrong does not overwrite the event-time resolution.

### 4.4 CatalogSnapshot and CatalogAssertion

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic and records only
the claim: `assertion_subject`, `assertion_predicate`,
`assertion_value_or_target`, unit, scope, `valid_from`,
`valid_until`/superseded, source. An assertion may concern an API alias, an
endpoint, a price, a region, or a model identity. Example atomic assertions:
(api-name-X, resolves_to, model-identity-Y); (api-name-X, context_limit,
400000, tokens).

`[DEF]` A CatalogAssertion records what its named source asserted at the
snapshot's observed time. A provider-controlled catalog response is an
attributed provider self-report. Authentication of the endpoint and integrity
of the captured payload may establish who supplied which bytes at a time; they
do not independently establish the truth of the asserted model mapping,
capability, price, region, or identity.

`[DEF]` Verification of a property concerning a CatalogAssertion is represented
by a VerificationRun (Section 4.17), separate from the assertion. The
VerificationRun identifies the property assessed, the evidence used, and the
result.

`[PROPOSED_CONSTRAINT]` A provider assertion alone never supports an
unqualified `verified` status. Any verification claim concerning a
CatalogAssertion is limited to the named property its evidence establishes.

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
`[INHERITED_CONSTRAINT]` Provider claims alone never qualify an executor for
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

`[INHERITED_CONSTRAINT]` Composite-executor disclosure: an invocation may not
acquire authority by encapsulating an undisclosed subordinate executor.
Every epistemically or operationally material subordinate execution (model,
tool, or human) capable of influencing the output or external effect must be
represented as an Invocation linked to its parent (`spawned`). A
tool that invokes a model cannot be represented as a purely deterministic
ToolIdentity. Nondeterminism itself is not prohibited; undeclared authority
and hidden composition are.

`[INHERITED_CONSTRAINT]` Tool-configuration disclosure: for a ToolIdentity
whose output enters governed evidence, the tool's effective inputs include
every configuration file, environment variable, and local dependency capable
of altering its execution path; these must be declared and content-addressed
in its EffectiveInputManifest. Undeclared configuration access capable of
altering the execution path defeats the tool's deterministic standing
(session-state mode `unknown_state`). This constraint is scoped to
governed-evidence production, not to every utility execution.

`[INHERITED_CONSTRAINT]` External-interaction disclosure: an invocation's
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

`[INHERITED_CONSTRAINT]` Producing an artifact does not grant authority to
accept it.

`[INHERITED_CONSTRAINT]` Witness grounding: witness outputs must identify
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

`[INHERITED_CONSTRAINT]` An invocation cannot qualify as a blind witness when
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
reference, span, proposition, claim kind.

`[LIMITATION]` One artifact may mix original observation, copied finding, new
inference, and paraphrase; artifact-level lineage cannot distinguish them.
Until claim-level derivation exists, the system provides artifact-level
potential-dependence detection, not claim-level independence proof; Section 7
imposes the conservative inheritance this gap requires, and C11 imposes the
interim high-consequence disclosure this gap requires.

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

`[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does
not establish that a policy was active, applicable, evaluated, or enforced for
a decision. AuthorizationPolicy enforcement remains deferred.

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

=== QUESTION Q8a ===
The eight questions in this round were written by the executor that drafted v5, v6, v7 and v8, every one of which was withdrawn or superseded. It drafted none of v9.

Someone who has failed four times at a document tends to probe the places they failed.

YOU ARE SEEING PART OF THE DOCUMENT. Below are the metadata, evidence inputs, and Sections 1 through 4: anchoring principles, scope, the three decisions, and the object definitions. Sections 5 through 13 are being reviewed by the same question in a separate call. The whole document did not fit in one call: at 17,533 input tokens it exhausted the entire output budget on reasoning and returned no text, which is the same failure that produced the empty response in COMP-0038. Say so if the split prevents you from answering.

Read what you can see as though no review round had happened. Find what is weakest in it. Then report anything significant that this question set does not ask about, and anything that is unsound rather than merely incomplete.

=== EVIDENCE ABS-0004 v9, metadata and Sections 1 to 4 (of 13) ===
# ABS-0004: Abstraction — Invocation Authorization Ontology

## Metadata

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v9`
- abstraction_level: `2`
- status: `proposed`
- reconstruction baseline: admitted v4 at commit
  `56f18a2ab7b66b1855b631a32d540f654c62b2c2`. Assembly does not admit v9;
  v9 requires its own admission review.
- version admission table:

  | version | state | basis |
  | --- | --- | --- |
  | v1, v2 | superseded during drafting | never entered the record |
  | v3 | superseded | entered the record at 6802cf7; underwent the COMP-0032 challenge round |
  | v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only |
  | v5 | amended, not separately admitted | replaced CatalogVerification with CatalogCapture on the COMP-0035 finding, at 6d7dfee |
  | v6 | amended, not separately admitted; superseded | proposed an authorization-chain termination that both COMP-0037 reviewers broke independently, at 8a1399f |
  | v7 | amended, not separately admitted | replaced v6's termination rule, at 00335d6; reviewed by COMP-0039..0046 |
  | v8 | **withdrawn_after_admission_review** | reviewed by COMP-0118..0125 and withdrawn under DECISION-20260727-0002; retained as evidence, not rejected, and not an implementation authority |
  | v9 | **proposed** | reconstructed from admitted v4 using the literal task 2, task 3, and identity-status text accepted under DECISION-20260727-0004, DECISION-20260727-0005, and DECISION-20260805-0001; assembled under DECISION-20260805-0002; pending its own admission review |

- reconstruction inputs:
  `ABS-0004-v9-task2-required-changes.patch`,
  `ABS-0004-v9-task3-limitations.patch`,
  `ABS-0004-v9-identity-status.patch`, and
  `ASSEMBLY_RULE_CORRECTION.md`, retained under
  `docs/self_model/v9_reconstruction/`.
- authors: operator (adjudicating principal); inherited v4 text drafted by an
  executor self-reported as "Claude"; v9 reconstruction text and assembly by
  the reviewing executor self-reported as `gpt-5.6-thinking`; both executor
  identities are unverified testimony; with attributed advisor contributions
  described in Evidence Inputs.
- sentence discipline: every normative statement is tagged `[DEF]`
  definition; `[PRINCIPLE]` architectural principle;
  `[PROPOSED_CONSTRAINT]` constraint proposed for adoption;
  `[INHERITED_CONSTRAINT]` constraint text carried forward unchanged from the
  admitted v4 baseline. Its current governance force derives from v4's
  admission, not from the proposed v9 document. A substantive change becomes
  `[PROPOSED_CONSTRAINT]` until separately admitted; `[COMMIT]` commitment
  concerning the preparation of this document; `[PROPOSAL]` candidate
  implementation boundary subject to future governance; `[OPEN]` open
  question; or `[LIMITATION]` descriptive boundary on what the ontology, its
  records, or current enforcement establish. A limitation imposes no
  constraint and claims no adoption. Untagged prose binds nothing.

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

`[LIMITATION]` A verification result supports only the property it names. It
does not by itself justify a broader epistemic status or establish truth,
grounding, calibration, privacy, or any other unverified property.

`[PRINCIPLE]` P3. Complete production provenance does not imply complete
claim provenance. A newly produced artifact must not erase the provenance
limitations of the claims it carries.

`[PRINCIPLE]` P4. Authority cannot be acquired through an opaque wrapper.
Encapsulation does not launder authority.

`[PRINCIPLE]` P5. Unknown facts block qualification; they never disappear
from the vocabulary. Uncertainty remains representable (`unknown_state`,
`unresolved`, `pre_provenance`), and unknown lineage or identity never
increases independence.

`[LIMITATION]` Distinct identifiers, endpoints, or invocation records do not by themselves
establish distinct executor identities. When executor-kind-specific
equivalence cannot be resolved, independence remains unresolved.

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

`[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and
authorization records can state and attribute authority claims. Repository
records do not by themselves establish a principal's extra-systemic
entitlement to govern.

`[LIMITATION]` A recorded authorization-chain terminus identifies where the
represented chain stops. It does not by itself establish that the underlying
invocation is substantively authorized.

`[LIMITATION]` Record and relation requirements expose only what was declared,
recorded, linked, traversable, and correctly attributed. They do not establish
that every material invocation, authorization, input, dependency, or external
interaction is present in the record.

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
release/version identity where establishable. Deprecation is mutable and
endpoint-specific; it lives in catalog assertions.

`[DEF]` An invocation's event-time identity resolution and the current
assessment of that resolution are distinct facts. The event-time resolution is
bound to the evidence available when the invocation occurred. A later
assessment is recorded separately and linked to that historical resolution.

`[DEF]` `identity_verification_status` is the immutable capture-time status of
the executor reference in an InvocationRecord. It is not a later identity
resolution outcome or the current assessment of one. `unresolved` means
the capture path did not establish an executor-kind-specific stable identity.
`verified` means an admitted capture path established a unique identity under a
property-scoped verification rule and durably recorded or referenced the
identity, supporting evidence, verifier, rule or test version, and verification
time.

`[LIMITATION]` InvocationRecord schema v1 accepts `verified`, but no admitted
schema-v1 capture path can presently substantiate it: the current path performs
no identity resolution, and provider catalog self-report, even over an
authenticated channel, does not independently establish a model mapping. It
therefore emits `unresolved`. Later append-only identity resolution records do
not mutate or upgrade this field; validator acceptance of `verified` is
syntactic compatibility, not a licensed status.

`[PROPOSED_CONSTRAINT]` An invocation records the most precise ModelIdentity
resolution establishable from evidence available at execution time; an
unresolved requested name is recorded as unresolved and is never silently
substituted. Later evidence that a relied-on catalog assertion was stale,
contradicted, or wrong does not overwrite the event-time resolution.

### 4.4 CatalogSnapshot and CatalogAssertion

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic and records only
the claim: `assertion_subject`, `assertion_predicate`,
`assertion_value_or_target`, unit, scope, `valid_from`,
`valid_until`/superseded, source. An assertion may concern an API alias, an
endpoint, a price, a region, or a model identity. Example atomic assertions:
(api-name-X, resolves_to, model-identity-Y); (api-name-X, context_limit,
400000, tokens).

`[DEF]` A CatalogAssertion records what its named source asserted at the
snapshot's observed time. A provider-controlled catalog response is an
attributed provider self-report. Authentication of the endpoint and integrity
of the captured payload may establish who supplied which bytes at a time; they
do not independently establish the truth of the asserted model mapping,
capability, price, region, or identity.

`[DEF]` Verification of a property concerning a CatalogAssertion is represented
by a VerificationRun (Section 4.17), separate from the assertion. The
VerificationRun identifies the property assessed, the evidence used, and the
result.

`[PROPOSED_CONSTRAINT]` A provider assertion alone never supports an
unqualified `verified` status. Any verification claim concerning a
CatalogAssertion is limited to the named property its evidence establishes.

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
`[INHERITED_CONSTRAINT]` Provider claims alone never qualify an executor for
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

`[INHERITED_CONSTRAINT]` Composite-executor disclosure: an invocation may not
acquire authority by encapsulating an undisclosed subordinate executor.
Every epistemically or operationally material subordinate execution (model,
tool, or human) capable of influencing the output or external effect must be
represented as an Invocation linked to its parent (`spawned`). A
tool that invokes a model cannot be represented as a purely deterministic
ToolIdentity. Nondeterminism itself is not prohibited; undeclared authority
and hidden composition are.

`[INHERITED_CONSTRAINT]` Tool-configuration disclosure: for a ToolIdentity
whose output enters governed evidence, the tool's effective inputs include
every configuration file, environment variable, and local dependency capable
of altering its execution path; these must be declared and content-addressed
in its EffectiveInputManifest. Undeclared configuration access capable of
altering the execution path defeats the tool's deterministic standing
(session-state mode `unknown_state`). This constraint is scoped to
governed-evidence production, not to every utility execution.

`[INHERITED_CONSTRAINT]` External-interaction disclosure: an invocation's
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

`[INHERITED_CONSTRAINT]` Producing an artifact does not grant authority to
accept it.

`[INHERITED_CONSTRAINT]` Witness grounding: witness outputs must identify
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

`[INHERITED_CONSTRAINT]` An invocation cannot qualify as a blind witness when
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
reference, span, proposition, claim kind.

`[LIMITATION]` One artifact may mix original observation, copied finding, new
inference, and paraphrase; artifact-level lineage cannot distinguish them.
Until claim-level derivation exists, the system provides artifact-level
potential-dependence detection, not claim-level independence proof; Section 7
imposes the conservative inheritance this gap requires, and C11 imposes the
interim high-consequence disclosure this gap requires.

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

`[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does
not establish that a policy was active, applicable, evaluated, or enforced for
a decision. AuthorizationPolicy enforcement remains deferred.

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

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
The split prevents a whole-document finding. Sections 5–13 are absent, including the referenced C3, C5, C10, C11, Section 7, and “OutboundInteractionLog (Section 11).” I would use them to determine whether the defects below are repaired by operative constraints, schemas, validation rules, and admission consequences. The admitted v4 text, reconstruction patches, assembly rule, and cited decisions are also absent; I would use them to test whether text marked `[INHERITED_CONSTRAINT]` is actually unchanged admitted v4 text and whether its asserted continuing force follows.

## Weakest and unsound: independence can be manufactured from an unresolved fact

Section 4.18 is incompatible with P5 as written.

P5 says:

> “Unknown facts block qualification”

and, specifically:

> “unknown lineage or identity never increases independence.”

But the 4.18 derivation rule says an `unresolved` dimension yields overall `unresolved` only:

> “without a named compensating control”

and otherwise permits:

> “qualified_independent with degradations listed.”

There is no type, scope, evidentiary threshold, independence requirement, or property-specific rule for a “compensating control.” Thus a record can have, for example, unresolved executor identity, source, or claim-lineage completeness, name something as a compensating control, and avoid the rule that would otherwise leave it unresolved. That is a direct route for an unknown fact to improve the overall independence result.

This is unsound, not just incomplete. A compensating control might reduce consequence, prohibit a use, require an additional independent witness, or establish some distinct property. It cannot transform an unresolved identity or lineage relationship into independent identity or lineage without evidence establishing that relationship. The current rule neither distinguishes those cases nor preserves the unresolved dimension as a bar to `qualified_independent`.

## Verification status has a label-conversion rule without a verification basis

Section 4.17 states:

> “Self-authored-unreviewed verification cannot satisfy admission for high-consequence outputs; the named independent review artifact converts the status to `self_authored_with_review`.”

A “named independent review artifact” does not itself establish that the review was independent, that it reviewed the verifier rather than merely its output, that it covered the relevant rule/test version and inputs, or that it found the verification adequate. The word “independent” in an artifact description is not an independence assessment.

This permits a status conversion on the existence of a named record rather than on the properties P2 requires: verifier identity and version, inputs, environment, rule/test version, result, and a property-scoped basis. It also has no stated relationship to the dimensioned `IndependenceAssessment` in 4.18. A self-authored verification could therefore acquire a more acceptable lineage label through a review artifact whose own executor identity or information path is unresolved.

The missing definition of “high-consequence outputs” and the admission constraints in Sections 5–13 are needed to assess the full consequence, but they cannot cure the unsupported conversion stated in 4.17 unless they impose substantive requirements on that artifact.

## Invocation authorization is foundational but not operationally or semantically secured

P1 says AI-Lab:

> “authorizes invocations for roles under evidence, provenance, independence, consequence, and execution constraints.”

Yet Section 4.10 makes the authorization reference applicable only:

> “where applicable”

and Section 4.16 says:

> “AuthorizationPolicy enforcement remains deferred.”

The bootstrap is expressly `[OPEN]`. The ontology therefore has no supplied rule establishing that an invocation requiring authorization cannot occur without an active, applicable, prior authorization; that an authorization is effective before the invocation; that its issuer was authorized to issue it; or that its conditions were evaluated.

The limitation is candid:

> “Defining AuthorizationPolicy and requiring typed references does not establish that a policy was active, applicable, evaluated, or enforced for a decision.”

That candor makes this a known unresolved core gap rather than concealed assurance. But it is still the central missing protection: the document defines authorization records while leaving the claimed organizing function of authorization unestablished. The “Subordinate authorization inheritance” rule is particularly exposed because it defines when a subordinate is “covered” while the parent authorization’s validity and applicability remain unestablished.

## `[INHERITED_CONSTRAINT]` governance force is asserted but cannot be verified from this evidence

The metadata says:

> “Its current governance force derives from v4's admission, not from the proposed v9 document.”

That may be true, but this evidence does not include admitted v4, its constraint text, its admission scope, or the reconstruction artifacts. It therefore cannot establish:

1. that every instance of `[INHERITED_CONSTRAINT]` is textually unchanged from admitted v4;
2. that the definitions on which those constraints depend have not changed materially;
3. that changed section references—for example, “Section 11,” C3, C5, C10, and C11—still resolve to the admitted meanings; or
4. that an admitted v4 constraint continues to apply after being embedded in a reconstructed proposed document with changed surrounding definitions.

This matters especially where an inherited constraint depends on terminology that v9 defines or defers. For example, the external-interaction constraint makes enforcement depend on:

> “OutboundInteractionLog (Section 11).”

Without Section 11 and v4, it cannot be determined whether the inherited rule retains an admitted enforcement object or has been placed over a changed or missing one.

The tag is not a demonstrated source of governance force. It is a claim about source and continuity that needs the missing baseline and change evidence.

## Effective-input provenance is weaker than its definition implies

Section 4.12 defines `EffectiveInputManifest` as:

> “What information could influence the result”

but says rendered messages are recorded:

> “(as digests)”

A digest can establish equality or integrity only if the underlying content remains available and the digest method and content binding are defined. It does not itself make the rendered system, developer, or user message reviewable evidence. The evidence-input commitment itself recognizes the distinction:

> “A digest is an integrity anchor, not an evidence artifact.”

No corresponding requirement is stated here that the manifest retain or durably reference the actual rendered content, preserve access controls and redaction transformations, identify the digest algorithm, or bind the digest to canonical rendering. As written, an input manifest may show that some unknown bytes existed without enabling examination of what influenced an output.

The document appropriately says:

> “A ContextManifest alone cannot prove blindness unless defined as complete for all effective inputs.”

But the same completeness problem applies to the entire `EffectiveInputManifest`. Its definition claims a complete causal-input category, while the supplied constraints do not state how completeness is established, especially for provider-side transformations, retrieval behavior, tool definitions, and inherited state.

## Disclosure constraints need a noncompliance semantics that does not confuse absence of a record with proof of absence

The inherited external-interaction constraint says material interactions:

> “must be declared”

and that undeclared interaction:

> “constitutes undisclosed `external_actuator` authority”

At the same time, Section 3 limits all record requirements:

> “They do not establish that every material invocation, authorization, input, dependency, or external interaction is present in the record.”

Those statements can coexist if missing disclosure produces an `unresolved` or ineligible status rather than a factual finding that an undeclared interaction occurred. The supplied text does not state that distinction. It does not say whether absence of an `OutboundInteractionLog` entry means “no interaction,” “unknown,” “disclosure failure,” or merely “no captured entry.”

This is consequential because the constraint attaches authority and deterministic-standing effects to undisclosed interactions. Section 11 is needed to determine whether it handles negative evidence, capture failures, ambient consumers, hardcoded targets, and incomplete logs without treating a record gap as proof of an external act.

## Significant matters I cannot assess because the question set is not supplied

Only Q8a is present. I cannot determine what Q1–Q7 ask, and therefore cannot reliably identify omissions from the eight-question set. The most significant topics that should not be left unexamined are:

- whether C5 repairs the 4.18 conflict with P5;
- whether C10 supplies substantive, independent-review criteria rather than accepting a named artifact;
- whether C11 supplies a usable claim-level or high-consequence disclosure rule;
- whether Section 7’s “conservative inheritance” actually prevents artifact-level potential dependence from being mistaken for claim-level independence;
- whether Section 11 defines reliable noncompliance and uncertainty handling for `OutboundInteractionLog`;
- whether Sections 5–13 impose activation, supersession, timing, authorization-chain, and accountable-approval requirements that make `DecisionRecord` more than an attributed record; and
- whether the v4 baseline and reconstruction evidence support every assertion of inherited governance force.

The present evidence is sufficient to identify the 4.18/P5 contradiction and the unsupported verification-status conversion. It is insufficient to determine whether the remaining deferred and cross-referenced mechanisms are repaired elsewhere.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Scope limitation (per instructions)

I can only see Sections 1–4 plus metadata; Sections 5–13 are being reviewed under the same question in a separate call. This matters concretely: several load-bearing terms here are undefined in what I can see — the numbered constraints **C3, C5, C10, C11** (referenced in 4.7, 4.17, 4.18), **Section 7**'s "conservative inheritance" (referenced in 4.15), and **Section 11**'s `OutboundInteractionLog` (referenced in 4.7). I cannot check whether the [INHERITED_CONSTRAINT]/[PROPOSED_CONSTRAINT] tagging is applied consistently across the full constraint set, only within this slice. I say this per the instruction that a split may prevent a full answer — it does not block what follows, but it caps its confidence.

## What is weakest here

**1. The tagging discipline the whole v9 fix depends on is porous, and Section 3 shows it.**
Disclosure states Section 3 grew to 1.48× v4's size. But every sentence in the visible Section 3 is tagged `[DEF]`, `[OPEN]`, or `[LIMITATION]` — none is `[PROPOSED_CONSTRAINT]` or `[INHERITED_CONSTRAINT]`. Yet the "Subordinate authorization inheritance" paragraph is not merely definitional: it states when a subordinate invocation *is* covered by a parent authorization, and asserts a consequence for exceeding that ("Undeclared subordinate execution is a disclosure violation under 4.7, not an implicitly authorized act"). That is constraint-shaped content wearing a `[DEF]` label. If new, substantive material can enter under `[DEF]` rather than `[PROPOSED_CONSTRAINT]`, then the entire point of this round — whether the tag scheme correctly separates admitted-from-v4 content from newly-proposed content — is compromised independent of whether `[INHERITED_CONSTRAINT]` itself is misused. This is unsound, not merely incomplete: it is a structural gap in the classification system, visible from the text plus the disclosed growth ratio, not a gap from missing information.

**2. `[INHERITED_CONSTRAINT]` cannot be checked against anything.**
The metadata defines the tag as text "carried forward unchanged from the admitted v4 baseline," with governance force "deriv[ing] from v4's admission, not from the proposed v9 document." That is a strong, specific, falsifiable claim — and nothing in the evidence lets me falsify or confirm it. There is no diff, no quoted v4 text, no per-sentence provenance marker distinguishing "verbatim from v4" from "reworded to fit the reconstruction." Several `[INHERITED_CONSTRAINT]` passages (e.g., the External-interaction disclosure constraint in 4.7, which narrates COMP-0032's three attack constructions by name and declares "this constraint closes the class") read as elaborated, occasion-specific prose rather than plausibly-unchanged v4 boilerplate. Given that v9 was assembled from patches ("task 2 required changes," "task 3 limitations," "identity-status") layered onto a v4 baseline, and given that v8 already demonstrated a 24-constraint mistagging failure of a *different but related* kind, the risk that some `[INHERITED_CONSTRAINT]`-tagged sentences are actually patch-introduced or patch-modified text is live and untestable from what's given. This is the central question disclosure 2 says this round exists to resolve, and Sections 1–4 supply no evidentiary basis to resolve it either way.

**3. The governance anchor itself is informally recorded.**
The version table states v4 was "admitted... by the operator as accountable principal in session, recorded in conversation only." Section 4.13 defines `DecisionRecord`, `EvidenceAdmissionDecision`, `effective_status` vs. `recommended_status`, and `AccountablePrincipal` specifically to formalize decisions like this one. Yet the single admission event that all `[INHERITED_CONSTRAINT]` governance force now depends on predates and does not conform to that schema — it is not itself an `EvidenceAdmissionDecision` instance. The document's own apparatus for taking decisions seriously was not applied to the decision the whole reconstruction leans on. That is an internal inconsistency, not a mere gap.

**4. The evidentiary chain behind v4's admission includes a disclosed confabulation.**
COMP-0032 — whose twelve adjudicated findings were "applied" to produce admitted v4 — is described as containing "incident chain of response truncation and one confabulated continuation recorded in the artifact itself." This doesn't necessarily invalidate the adjudicated findings, but it means the chain of custody behind the very content now claiming inherited governance force includes a recorded reliability failure. Nothing in Sections 1–4 addresses how that confabulation incident was isolated from the twelve findings that were actually adopted.

**5. v7's authorization-chain work appears to have been silently dropped.**
The version table records that v6 proposed a chain-termination rule broken by both COMP-0037 reviewers, and v7 "replaced v6's termination rule," reviewed by COMP-0039..0046 — implying that work passed further review. But Section 3 here shows only `[OPEN] Authorization-chain bootstrap`, with no termination rule at all, i.e., a reversion to (apparently) v4's original open state. Nothing explains whether v7's rule was excluded because it failed later review, because the reconstruction patches simply didn't touch it, or because it was judged out of scope. Given the "literal" reconstruction claim, silently discarding previously-reviewed work without a stated reason is a place where "reconstructed from v4" and "incorporates review history" pull in different directions.

## Named gaps — what I would need and why

- **Admitted v4 text (commit `56f18a2ab7b66b1855b631a32d540f654c62b2c2`), Sections 3–4** — to check every `[INHERITED_CONSTRAINT]` sentence against it directly. Without this I cannot verify point 2 at all.
- **DECISION-20260727-0004, -0005, DECISION-20260805-0001, -0002** — cited as the basis for accepting the task2/task3/identity-status patches and the assembly rule; without their text I can't tell what was actually authorized versus what the assembler chose to include.
- **`ASSEMBLY_RULE_CORRECTION.md`** — its existence implies a prior assembly rule was wrong; I'd use it to check whether the correction affects how `[INHERITED_CONSTRAINT]` boundaries were drawn.
- **Section 5 (or wherever C1–C11 are enumerated)** — needed to confirm the C-numbers referenced in 4.7/4.17/4.18 exist, are unchanged in number and content from whatever v4/v7 versions preceded them, and to check the 24-constraint count from v8 against v9's total.
- **COMP-0037 and COMP-0039..0046 findings** — to determine whether v7's dropped termination rule was validated or rejected, resolving point 5.

## What this question set may not be asking

I have no visibility into the other seven questions in this round, so I can't state definitively what they cover. But given the disclosed pattern — this question set's author drafted v5 (CatalogCapture), v6/v7 (chain termination), and v8 (the mistagging defect) and failed on each — the stated tendency to "probe the places they failed" suggests likely concentration on catalog-identity mechanics, chain termination, and the specific 24-constraint mistagging pattern from v8. That leaves the two defects most native to v9 *itself* — the `[DEF]`-vs-constraint boundary softness in Section 3, and the informally-recorded v4 admission underlying every `[INHERITED_CONSTRAINT]` claim — as plausible blind spots, since neither is a repeat of a v5–v8 failure mode and both require reading v9 fresh rather than checking it against old wounds.
```
