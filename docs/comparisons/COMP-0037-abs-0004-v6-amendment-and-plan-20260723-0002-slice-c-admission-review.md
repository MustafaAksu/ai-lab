# COMP-0037: Provider Comparison — ABS-0004 v6 amendment and PLAN-20260723-0002 slice C admission review

## Metadata

- comparison_id: `COMP-0037`
- title: `ABS-0004 v6 amendment and PLAN-20260723-0002 slice C admission review`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-c88990a85196d35d.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0037", "target_id": "INV-c88990a85196d35d"}, {"authoritative": false, "evidence": "docs/invocations/INV-c9fecfbf0964c1d2.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0037", "target_id": "INV-c9fecfbf0964c1d2"}]`
- created_at: `2026-07-23T20:28:14.567114+00:00`
- command: `scripts/compare_providers.py --title ABS-0004 v6 amendment and PLAN-20260723-0002 slice C admission review Review the plan below for admission, together with the ontology amendment it depends on. Full texts are included; do not rely on repository access, and quote only text that appears below. If something you need is not present, say so rather than inferring it.

=== ABS-0004 v6 SECTION 3 (three decisions, authorization-chain termination) ===
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

`[DEF]` Authorization-chain termination. An authorization chain terminates at
an AccountablePrincipal's standing authority. A principal holds standing
authority within a declared `authority_scope`; authorizations the principal
issues inside that scope are self-standing and require no prior
authorization. Every other authorization must chain, through one or more
steps, to a standing authority. An authorization that chains to nothing is
not thereby permitted: it is unauthorized.

`[ADOPTED_CONSTRAINT]` Standing authority is declared, bounded, and
recorded. A principal may not assert standing authority implicitly, by
practice, or for a scope wider than its declared `authority_scope`; an
authorization issued outside that scope does not terminate a chain and is
unauthorized. This is what prevents the regress from being closed by
convenience: the terminating step is a recorded human or organizational
commitment with stated bounds, not an executor exempting itself.

`[DEF]` Standing authority is not a capability of executors. A model, tool,
or human acting as an executor never holds standing authority by virtue of
executing; it holds it only as an AccountablePrincipal within a declared
scope, which is a separate role under Section 4.13.

`[OPEN]` Whether standing authority requires periodic re-declaration or
review, and what evidence a scope declaration must carry beyond its own
statement.


=== ABS-0004 v6 SECTION 4.6-4.7 (qualification, executors) ===
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


=== ABS-0004 v6 SECTION 4.9 (RoleDefinition) ===
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


=== ABS-0004 v6 SECTION 4.13 (DecisionRecord, AccountablePrincipal) ===
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


=== ABS-0004 v6 SECTION 8 (consequence classes) ===
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


=== PLAN-20260723-0002 ===
{
  "constraints": [
    "Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan.",
    "Field names and semantics follow ABS-0004 v6 exactly; deviations require an ABS revision first.",
    "All relations use the GraphRelation shape; no predicate outside the registered Slice A, B, and C lists.",
    "authorize() is pure over stored records: no I/O, no clock, no network; the decision timestamp is supplied by the caller.",
    "Slice A capture and Slice B resolution behavior are unchanged: no field, path, or default of either is altered.",
    "Standing authority may not be asserted implicitly. A principal record must declare its authority_scope, and an authorization outside that scope is refused rather than downgraded."
  ],
  "created_at": "2026-07-23T00:00:00+00:00",
  "created_from": {
    "repo_commit": "96209e95a722c5e1f6d18061e746ff75b33b3fca",
    "source_gap_id": "GAP-0005"
  },
  "depends_on_capability_ids": [
    "CAP-0015",
    "CAP-0016"
  ],
  "evidence_ids": [
    "docs/self_model/gaps/GAP-0005.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
    "docs/self_model/decisions/DECISION-20260723-0001.json",
    "docs/self_model/verifications/VERIFY-20260723-0002.json",
    "docs/self_model/capabilities/CAP-0015.json",
    "docs/self_model/capabilities/CAP-0016.json"
  ],
  "expected_outputs": [
    "ai_lab/governance/roles.py (role, qualification, and principal schemas with validators).",
    "ai_lab/governance/authorization.py (authorization records, pure authorize(), consequence classification, governed/experimental classifier, one-hop self-adjudication check).",
    "docs/self_model/PREDICATE_REGISTRY.md extended with the Slice C predicates.",
    "docs/self_model/AUTHORIZATION_RECORDS.md documenting the record family, the standing-authority termination rule, and stated limitations including the one-hop bound.",
    "tests/test_roles.py and tests/test_authorization.py with schema, rejection, refusal-reason, and integration fixtures.",
    "Seed records: the operator's AccountablePrincipal record and the role definitions AI-Lab already uses in practice (drafting actuator, comparison advisor, adjudicating principal, deterministic verifier)."
  ],
  "mitigation": "Both limits are stated in the documentation and in the capability record rather than left to inference: governed means an authorization covers the invocation, and the self-adjudication check is one hop. Refusal reasons are enumerated so that a permitted outcome is never a silent default. The role vocabulary is copied from ABS-0004 v6 verbatim rather than invented, and the seed roles describe practice already visible in the record.",
  "next_action": "Run the admission comparison round with this plan, the ABS-0004 v6 amendment, GAP-0005, and the relevant ontology sections attached as text; on operator adjudication, admit the v6 amendment and issue the plan's admission warrant.",
  "non_goals": [
    "Refusing or blocking any execution. Authorization classifies; it does not gate. Execution refusal requires a separately admitted plan.",
    "Routing, escalation, or model selection (RoutingDecision remains deferred).",
    "Multi-hop lineage traversal, independence assessment, or evidence admission (Slice D).",
    "Retroactive authorization of invocations captured before this slice; they remain experimental, and the pre-provenance boundary applies.",
    "Any claim that the one-hop check implements C3. It implements C3's most direct case only, and the documentation must say so.",
    "Automatic consequence assignment from artifact content; consequence is declared per authorization with the default derived from target type.",
    "Cryptographic attestation of principals; ABS-0004 records it as a later implementation mechanism, not an ontology requirement."
  ],
  "objective": "Make the authority separation AI-Lab has practised in conversation structural: who may perform what, under which role, at what consequence, on whose standing authority, recorded as evidence rather than as testimony. The immediate motivation is concrete: on 2026-07-23 a model-default change would have set the reviewer slot to the drafting executor's own identity, collapsing reviewer and author under C3. Nothing in the system would have noticed; it was caught because a human happened to be told. Slice C makes the most direct case of that collision detectable by machine.",
  "plan_id": "PLAN-20260723-0002",
  "proposed_change": "After a separate admission checkpoint, and after ABS-0004 v6 is admitted: add ai_lab/governance/roles.py (RoleDefinition, RoleQualification, AccountablePrincipal schemas and validators), ai_lab/governance/authorization.py (InvocationAuthorization records, the pure authorize() function, consequence classification, the experimental-versus-governed classifier, and the one-hop self-adjudication check), predicate-registry entries, documentation, and tests. No change to provider-call behavior, no change to Slice A capture or Slice B resolution, and no refusal of any execution.",
  "rationale": [
    "ABS-0004's enforcement matrix records C6 authority separation as 'adopted, not currently evidenced': no artifact names the check. Slice C is what lets that row cite something.",
    "The near-miss of 2026-07-23 is the exhibit: identity collision between reviewer and author was invisible to every test, and was avoided by chance rather than by control.",
    "Slice A supplies produced_by and executed_by, so a one-hop identity collision is detectable now without the ancestry traversal that belongs to Slice D. The cheap case is available; the expensive case stays deferred.",
    "ABS-0004 v6 closes the authorization-bootstrap open question by terminating chains at a principal's declared standing authority, so the regress is resolved in the ontology before any code depends on it."
  ],
  "repo_commit": "96209e95a722c5e1f6d18061e746ff75b33b3fca",
  "risk": "An authorization system that classifies but never refuses can create a false sense of control: readers may assume governed means checked when it means covered by a record. The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision. Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate.",
  "schema_version": "v1",
  "scope": [
    "A roles module defining schema v1 for RoleDefinition (task_function, epistemic_authority, action_authority, and the constraint fields ABS-0004 4.9 enumerates), with a validator, canonical serialization, and deterministic identity and path rules under docs/roles/.",
    "RoleQualification records, execution-scoped as ABS-0004 4.6 requires: qualified executor, role, service endpoint scope, permitted ExecutionProfile constraints, session-state constraints, policy version, and the evaluation evidence relied on. A qualification never transfers implicitly to another endpoint or a materially different profile, and the validator rejects a qualification lacking an execution scope.",
    "AccountablePrincipal records with principal_id, principal_kind, authority_scope, and delegation_reference, carrying no personal identifying data.",
    "InvocationAuthorization as a DecisionRecord kind: invocation request, authorized executor, assigned role, consequence class, applicable policy, qualifications relied on, independence requirements, conditions, issuing principal, and the standing-authority or chained-authorization reference that terminates its chain.",
    "A pure authorize() function over stored records returning an authorization outcome or one of the enumerated refusal reasons: no qualification for this executor and role, qualification out of execution scope, consequence above the role ceiling, unterminated authorization chain, standing authority claimed outside its declared scope, and self-adjudication conflict.",
    "The one-hop self-adjudication check: for an adjudicator-authority role over a target artifact, if the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization, refuse. Scoped explicitly to one hop; multi-hop ancestry is Slice D.",
    "Consequence classification per ABS-0004 Section 8: default by target type, effective consequence as the maximum of the default and applicable modifier levels, modifiers only raising, and downward adjustment only as a governed exception carrying reason, principal, scope, evidence, and review condition.",
    "The experimental-versus-governed boundary: a classify function marking an invocation governed only when a valid authorization covers it, experimental otherwise. Classification only; no invocation is refused execution by this slice.",
    "Predicate-registry entries for the Slice C predicates: assigned_role, authorized_by, authorizes, qualifies_executor, qualifies_for, issued_under, based_on, approved_by.",
    "Validator fixtures covering valid records, each rejection class, and each refusal reason, plus an integration fixture authorizing an invocation against stored role, qualification, and principal records offline."
  ],
  "source_capability_ids": [
    "CAP-0015",
    "CAP-0016"
  ],
  "source_gap_id": "GAP-0005",
  "status": "proposed",
  "success_criteria": [
    "A stored invocation is classified governed when a valid authorization covers it and experimental otherwise, demonstrated by fixtures for both outcomes.",
    "Each enumerated refusal reason is exercised by a fixture and yields an explicit reason; authorization never fails silently and never defaults to permitted.",
    "An authorization whose chain terminates nowhere is refused, and an authorization issued outside a principal's declared authority_scope is refused, each with its own reason.",
    "The one-hop self-adjudication check refuses an adjudicator authorization over an artifact produced by the same executor identity, demonstrated against a real captured InvocationRecord, and permits it when the identities differ.",
    "Consequence is monotonic: modifiers only raise the class, a downward adjustment without a recorded governed exception is refused, and a test asserts the maximum rule over an ordinal scale rather than arithmetic.",
    "A qualification lacking an execution scope is rejected, and a qualification is not honoured for an endpoint or execution profile outside its scope.",
    "All new behavior covered by tests; the full suite passes offline; the repository audit remains ok true verified_current; cross-environment reproduction succeeds byte-identically."
  ],
  "summary": "Implement ABS-0004 v6 Slice C: RoleDefinition records on the three admitted axes, execution-scoped RoleQualification, InvocationAuthorization as a DecisionRecord kind, consequence classification, and the experimental-versus-governed boundary. An authorization is issued by an AccountablePrincipal holding standing authority within a declared scope, or chains to one; an authorization that chains to nothing is unauthorized rather than permitted. Authorization has one consequence in this slice and no others: an invocation is classified governed only when an authorization covers it, and experimental otherwise. Nothing is refused execution. The authorization function additionally performs a one-hop self-adjudication check using Slice A provenance: if the artifact under adjudication carries an InvocationRecord whose executor identity equals the executor being authorized, authorization is refused with an enumerated reason.",
  "title": "Roles, qualification, and invocation authorization (ABS-0004 Slice C)"
}

=== QUESTIONS ===
1. The v6 amendment terminates authorization chains at a principal's declared standing authority. Construct a way to abuse that termination: a path by which an executor or an unbounded scope declaration effectively authorizes itself while satisfying the text as written.
2. Slice C classifies invocations as governed or experimental but refuses no execution. Is 'governed' then a meaningful status, or does it manufacture assurance? Argue from the plan text.
3. The one-hop self-adjudication check catches only direct collisions. Construct a two-hop case it misses that a reader would reasonably expect it to catch, and say whether the plan's disclosure is sufficient.
4. Does the scope stay inside Slice C, and does anything belong to Slice D or to routing?
5. Are the six enumerated refusal reasons complete? Name a case that should refuse and has no reason.
6. Which decisions here constrain Slice D's evidence admission, and how?
7. Are the success criteria mechanically checkable? Name any that is not, and any missing check.
8. Recommendation: admit as written, admit with named conditions (state them), or revise first.

Do not certify or praise. No provider product recommendations.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

Review the plan below for admission, together with the ontology amendment it depends on. Full texts are included; do not rely on repository access, and quote only text that appears below. If something you need is not present, say so rather than inferring it.

=== ABS-0004 v6 SECTION 3 (three decisions, authorization-chain termination) ===
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

`[DEF]` Authorization-chain termination. An authorization chain terminates at
an AccountablePrincipal's standing authority. A principal holds standing
authority within a declared `authority_scope`; authorizations the principal
issues inside that scope are self-standing and require no prior
authorization. Every other authorization must chain, through one or more
steps, to a standing authority. An authorization that chains to nothing is
not thereby permitted: it is unauthorized.

`[ADOPTED_CONSTRAINT]` Standing authority is declared, bounded, and
recorded. A principal may not assert standing authority implicitly, by
practice, or for a scope wider than its declared `authority_scope`; an
authorization issued outside that scope does not terminate a chain and is
unauthorized. This is what prevents the regress from being closed by
convenience: the terminating step is a recorded human or organizational
commitment with stated bounds, not an executor exempting itself.

`[DEF]` Standing authority is not a capability of executors. A model, tool,
or human acting as an executor never holds standing authority by virtue of
executing; it holds it only as an AccountablePrincipal within a declared
scope, which is a separate role under Section 4.13.

`[OPEN]` Whether standing authority requires periodic re-declaration or
review, and what evidence a scope declaration must carry beyond its own
statement.


=== ABS-0004 v6 SECTION 4.6-4.7 (qualification, executors) ===
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


=== ABS-0004 v6 SECTION 4.9 (RoleDefinition) ===
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


=== ABS-0004 v6 SECTION 4.13 (DecisionRecord, AccountablePrincipal) ===
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


=== ABS-0004 v6 SECTION 8 (consequence classes) ===
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


=== PLAN-20260723-0002 ===
{
  "constraints": [
    "Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan.",
    "Field names and semantics follow ABS-0004 v6 exactly; deviations require an ABS revision first.",
    "All relations use the GraphRelation shape; no predicate outside the registered Slice A, B, and C lists.",
    "authorize() is pure over stored records: no I/O, no clock, no network; the decision timestamp is supplied by the caller.",
    "Slice A capture and Slice B resolution behavior are unchanged: no field, path, or default of either is altered.",
    "Standing authority may not be asserted implicitly. A principal record must declare its authority_scope, and an authorization outside that scope is refused rather than downgraded."
  ],
  "created_at": "2026-07-23T00:00:00+00:00",
  "created_from": {
    "repo_commit": "96209e95a722c5e1f6d18061e746ff75b33b3fca",
    "source_gap_id": "GAP-0005"
  },
  "depends_on_capability_ids": [
    "CAP-0015",
    "CAP-0016"
  ],
  "evidence_ids": [
    "docs/self_model/gaps/GAP-0005.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
    "docs/self_model/decisions/DECISION-20260723-0001.json",
    "docs/self_model/verifications/VERIFY-20260723-0002.json",
    "docs/self_model/capabilities/CAP-0015.json",
    "docs/self_model/capabilities/CAP-0016.json"
  ],
  "expected_outputs": [
    "ai_lab/governance/roles.py (role, qualification, and principal schemas with validators).",
    "ai_lab/governance/authorization.py (authorization records, pure authorize(), consequence classification, governed/experimental classifier, one-hop self-adjudication check).",
    "docs/self_model/PREDICATE_REGISTRY.md extended with the Slice C predicates.",
    "docs/self_model/AUTHORIZATION_RECORDS.md documenting the record family, the standing-authority termination rule, and stated limitations including the one-hop bound.",
    "tests/test_roles.py and tests/test_authorization.py with schema, rejection, refusal-reason, and integration fixtures.",
    "Seed records: the operator's AccountablePrincipal record and the role definitions AI-Lab already uses in practice (drafting actuator, comparison advisor, adjudicating principal, deterministic verifier)."
  ],
  "mitigation": "Both limits are stated in the documentation and in the capability record rather than left to inference: governed means an authorization covers the invocation, and the self-adjudication check is one hop. Refusal reasons are enumerated so that a permitted outcome is never a silent default. The role vocabulary is copied from ABS-0004 v6 verbatim rather than invented, and the seed roles describe practice already visible in the record.",
  "next_action": "Run the admission comparison round with this plan, the ABS-0004 v6 amendment, GAP-0005, and the relevant ontology sections attached as text; on operator adjudication, admit the v6 amendment and issue the plan's admission warrant.",
  "non_goals": [
    "Refusing or blocking any execution. Authorization classifies; it does not gate. Execution refusal requires a separately admitted plan.",
    "Routing, escalation, or model selection (RoutingDecision remains deferred).",
    "Multi-hop lineage traversal, independence assessment, or evidence admission (Slice D).",
    "Retroactive authorization of invocations captured before this slice; they remain experimental, and the pre-provenance boundary applies.",
    "Any claim that the one-hop check implements C3. It implements C3's most direct case only, and the documentation must say so.",
    "Automatic consequence assignment from artifact content; consequence is declared per authorization with the default derived from target type.",
    "Cryptographic attestation of principals; ABS-0004 records it as a later implementation mechanism, not an ontology requirement."
  ],
  "objective": "Make the authority separation AI-Lab has practised in conversation structural: who may perform what, under which role, at what consequence, on whose standing authority, recorded as evidence rather than as testimony. The immediate motivation is concrete: on 2026-07-23 a model-default change would have set the reviewer slot to the drafting executor's own identity, collapsing reviewer and author under C3. Nothing in the system would have noticed; it was caught because a human happened to be told. Slice C makes the most direct case of that collision detectable by machine.",
  "plan_id": "PLAN-20260723-0002",
  "proposed_change": "After a separate admission checkpoint, and after ABS-0004 v6 is admitted: add ai_lab/governance/roles.py (RoleDefinition, RoleQualification, AccountablePrincipal schemas and validators), ai_lab/governance/authorization.py (InvocationAuthorization records, the pure authorize() function, consequence classification, the experimental-versus-governed classifier, and the one-hop self-adjudication check), predicate-registry entries, documentation, and tests. No change to provider-call behavior, no change to Slice A capture or Slice B resolution, and no refusal of any execution.",
  "rationale": [
    "ABS-0004's enforcement matrix records C6 authority separation as 'adopted, not currently evidenced': no artifact names the check. Slice C is what lets that row cite something.",
    "The near-miss of 2026-07-23 is the exhibit: identity collision between reviewer and author was invisible to every test, and was avoided by chance rather than by control.",
    "Slice A supplies produced_by and executed_by, so a one-hop identity collision is detectable now without the ancestry traversal that belongs to Slice D. The cheap case is available; the expensive case stays deferred.",
    "ABS-0004 v6 closes the authorization-bootstrap open question by terminating chains at a principal's declared standing authority, so the regress is resolved in the ontology before any code depends on it."
  ],
  "repo_commit": "96209e95a722c5e1f6d18061e746ff75b33b3fca",
  "risk": "An authorization system that classifies but never refuses can create a false sense of control: readers may assume governed means checked when it means covered by a record. The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision. Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate.",
  "schema_version": "v1",
  "scope": [
    "A roles module defining schema v1 for RoleDefinition (task_function, epistemic_authority, action_authority, and the constraint fields ABS-0004 4.9 enumerates), with a validator, canonical serialization, and deterministic identity and path rules under docs/roles/.",
    "RoleQualification records, execution-scoped as ABS-0004 4.6 requires: qualified executor, role, service endpoint scope, permitted ExecutionProfile constraints, session-state constraints, policy version, and the evaluation evidence relied on. A qualification never transfers implicitly to another endpoint or a materially different profile, and the validator rejects a qualification lacking an execution scope.",
    "AccountablePrincipal records with principal_id, principal_kind, authority_scope, and delegation_reference, carrying no personal identifying data.",
    "InvocationAuthorization as a DecisionRecord kind: invocation request, authorized executor, assigned role, consequence class, applicable policy, qualifications relied on, independence requirements, conditions, issuing principal, and the standing-authority or chained-authorization reference that terminates its chain.",
    "A pure authorize() function over stored records returning an authorization outcome or one of the enumerated refusal reasons: no qualification for this executor and role, qualification out of execution scope, consequence above the role ceiling, unterminated authorization chain, standing authority claimed outside its declared scope, and self-adjudication conflict.",
    "The one-hop self-adjudication check: for an adjudicator-authority role over a target artifact, if the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization, refuse. Scoped explicitly to one hop; multi-hop ancestry is Slice D.",
    "Consequence classification per ABS-0004 Section 8: default by target type, effective consequence as the maximum of the default and applicable modifier levels, modifiers only raising, and downward adjustment only as a governed exception carrying reason, principal, scope, evidence, and review condition.",
    "The experimental-versus-governed boundary: a classify function marking an invocation governed only when a valid authorization covers it, experimental otherwise. Classification only; no invocation is refused execution by this slice.",
    "Predicate-registry entries for the Slice C predicates: assigned_role, authorized_by, authorizes, qualifies_executor, qualifies_for, issued_under, based_on, approved_by.",
    "Validator fixtures covering valid records, each rejection class, and each refusal reason, plus an integration fixture authorizing an invocation against stored role, qualification, and principal records offline."
  ],
  "source_capability_ids": [
    "CAP-0015",
    "CAP-0016"
  ],
  "source_gap_id": "GAP-0005",
  "status": "proposed",
  "success_criteria": [
    "A stored invocation is classified governed when a valid authorization covers it and experimental otherwise, demonstrated by fixtures for both outcomes.",
    "Each enumerated refusal reason is exercised by a fixture and yields an explicit reason; authorization never fails silently and never defaults to permitted.",
    "An authorization whose chain terminates nowhere is refused, and an authorization issued outside a principal's declared authority_scope is refused, each with its own reason.",
    "The one-hop self-adjudication check refuses an adjudicator authorization over an artifact produced by the same executor identity, demonstrated against a real captured InvocationRecord, and permits it when the identities differ.",
    "Consequence is monotonic: modifiers only raise the class, a downward adjustment without a recorded governed exception is refused, and a test asserts the maximum rule over an ordinal scale rather than arithmetic.",
    "A qualification lacking an execution scope is rejected, and a qualification is not honoured for an endpoint or execution profile outside its scope.",
    "All new behavior covered by tests; the full suite passes offline; the repository audit remains ok true verified_current; cross-environment reproduction succeeds byte-identically."
  ],
  "summary": "Implement ABS-0004 v6 Slice C: RoleDefinition records on the three admitted axes, execution-scoped RoleQualification, InvocationAuthorization as a DecisionRecord kind, consequence classification, and the experimental-versus-governed boundary. An authorization is issued by an AccountablePrincipal holding standing authority within a declared scope, or chains to one; an authorization that chains to nothing is unauthorized rather than permitted. Authorization has one consequence in this slice and no others: an invocation is classified governed only when an authorization covers it, and experimental otherwise. Nothing is refused execution. The authorization function additionally performs a one-hop self-adjudication check using Slice A provenance: if the artifact under adjudication carries an InvocationRecord whose executor identity equals the executor being authorized, authorization is refused with an enumerated reason.",
  "title": "Roles, qualification, and invocation authorization (ABS-0004 Slice C)"
}

=== QUESTIONS ===
1. The v6 amendment terminates authorization chains at a principal's declared standing authority. Construct a way to abuse that termination: a path by which an executor or an unbounded scope declaration effectively authorizes itself while satisfying the text as written.
2. Slice C classifies invocations as governed or experimental but refuses no execution. Is 'governed' then a meaningful status, or does it manufacture assurance? Argue from the plan text.
3. The one-hop self-adjudication check catches only direct collisions. Construct a two-hop case it misses that a reader would reasonably expect it to catch, and say whether the plan's disclosure is sufficient.
4. Does the scope stay inside Slice C, and does anything belong to Slice D or to routing?
5. Are the six enumerated refusal reasons complete? Name a case that should refuse and has no reason.
6. Which decisions here constrain Slice D's evidence admission, and how?
7. Are the success criteria mechanically checkable? Name any that is not, and any missing check.
8. Recommendation: admit as written, admit with named conditions (state them), or revise first.

Do not certify or praise. No provider product recommendations.

## OpenAI Response

- model: `gpt-5.6-terra`

```
1. **Standing-authority termination can be self-bootstrapped**

A conforming-looking abuse path is available because the amendment requires a declared scope, but does not state who is authorized to create, approve, activate, or constrain the declaration of that scope.

Example:

1. An executor uses, or is associated with, an `AccountablePrincipal` record.
2. That principal record declares a narrowly worded `authority_scope`, such as authority over authorizing a specified role, target class, or even a specified invocation request.
3. The same principal issues an `InvocationAuthorization` for the executor.
4. Because the authorization is inside the declared scope, it is “self-standing and require[s] no prior authorization.”

This need not use a visibly unlimited scope. A scope limited to “authorization of invocation I” is formally narrow while still allowing the declaration to manufacture authority exactly where wanted.

The text says standing authority is “declared, bounded, and recorded,” and rejects authority asserted “implicitly, by practice,” but it does not define:

- a machine-checkable grammar or maximum breadth for `authority_scope`;
- who may create or approve an `AccountablePrincipal` record;
- whether a principal may declare its own standing authority;
- whether the declaration itself needs an independent governance record;
- how `delegation_reference` is validated, if present;
- whether scope declarations have activation, expiry, supersession, or review requirements.

The `[OPEN]` question expressly leaves open “what evidence a scope declaration must carry beyond its own statement.” That leaves the declaration itself able to serve as the only root evidence.

The separate-role rule does not close this fully. It says an executor does not acquire standing authority merely by executing, but it does not prohibit an executor from being represented as an `AccountablePrincipal` or require an independent actor to establish that principal’s standing authority. A human may legitimately be both an executor and an accountable principal; the missing constraint is not identity separation alone, but independent establishment of the principal’s authority.

2. **“Governed” has a narrow meaning, but can manufacture assurance**

The plan gives “governed” a precise narrow meaning: an invocation is governed “only when a valid authorization covers it,” otherwise it is experimental. That is meaningful as a record-classification and audit-query status. It can distinguish an invocation with a stored authorization record from one without one.

But it is not an execution-control status. The plan states:

- “Authorization classifies; it does not gate.”
- “Nothing is refused execution.”
- “Classification only; no invocation is refused execution by this slice.”

The plan itself identifies the assurance problem:

> “An authorization system that classifies but never refuses can create a false sense of control: readers may assume governed means checked when it means covered by a record.”

That risk is material because “valid authorization” may be read as operational permission or as an assurance that conditions were enforced. The plan instead describes a classification system over stored records. An invocation can still run without authorization, be classified experimental afterward, and potentially already have produced effects.

The status should therefore be documented and named as record coverage, not as execution enforcement, evidence admission, correctness, safety, or independent review. It also must not be treated as a substitute for the separate `EvidenceAdmissionDecision` required for governed evidence.

3. **A two-hop self-adjudication case the check misses**

A direct two-hop construction is:

1. Executor A performs Invocation A1 and produces source artifact S.
2. Executor B performs Invocation B1, using S, and produces artifact T.
3. Executor A is authorized in an adjudicator role over T.

The proposed check examines whether T has a `produced_by` relation to an `InvocationRecord` whose `executed_by` equals A. T was directly produced by B1, so the direct identities differ and the authorization is permitted.

But a reader could reasonably regard this as self-adjudication if B1’s output is materially derived from A1’s work, especially where B1 is a tool, transformation step, or subordinate invocation carrying A’s substantive judgment forward. The relevant ancestry is:

`T --produced_by--> B1 --uses/derives from--> S --produced_by--> A1`

A second version uses the plan’s own subordinate-execution terminology:

1. A executes parent Invocation A1.
2. A1 `spawned` subordinate Invocation B1, executed by a different executor identity.
3. B1 produces T.
4. A is authorized to adjudicate T.

The direct check sees B, not A. An ancestry-aware check could identify that A caused or materially controlled the production chain.

The disclosure is sufficient only for the limited claim actually made. The plan repeatedly says the check is “one hop,” that “multi-hop ancestry traversal” is out of scope, and that it “implements C3’s most direct case only.” It is not sufficient if “self-adjudication conflict” is presented without that qualification, or if a downstream user treats a permitted result as a finding of independence.

4. **Scope boundaries**

Most of the stated implementation fits the plan’s stated Slice C boundary:

- `RoleDefinition`;
- execution-scoped `RoleQualification`;
- `AccountablePrincipal`;
- `InvocationAuthorization`;
- standing-authority-chain evaluation;
- consequence classification;
- governed-versus-experimental classification;
- a direct provenance-based self-adjudication check.

The following are explicitly deferred to Slice D or are otherwise outside this slice:

- “Multi-hop lineage traversal”;
- “independence assessment”;
- “evidence admission”;
- general verification of the claim or artifact;
- whether required verified properties are actually established for admission.

Routing is also explicitly deferred. `RoutingDecision` requires candidates considered, rejection reasons, selected candidate, policy version, and catalog snapshot. The plan says “Routing, escalation, or model selection” is a non-goal, so it should not implement or imply routing policy.

There is a boundary risk in using the term “self-adjudication conflict.” The proposed check is an authorization-time direct-identity check, not a full independence finding. Full lineage and independence findings are specifically attributes of `EvidenceAdmissionDecision` and belong to the deferred work.

There is also an unresolved implementation boundary concerning the Section 4.7 disclosure constraints. The provided plan does not state checks for material subordinate executions, tool configuration, or material external interactions, even though those constraints bear on whether an invocation’s authority surface is disclosed. If Slice C does not enforce them, it should not imply that a “valid authorization” establishes full disclosure compliance.

5. **The six refusal reasons are not complete**

The listed reasons are:

1. no qualification for this executor and role;
2. qualification out of execution scope;
3. consequence above the role ceiling;
4. unterminated authorization chain;
5. standing authority claimed outside its declared scope;
6. self-adjudication conflict.

At least one clear missing refusal case is **authorization conditions not satisfied**.

An `InvocationAuthorization` carries “conditions,” and Section 3 defines invocation authorization as whether an executor may perform an invocation “under role R, consequence C, and conditions K.” Yet there is no listed refusal reason for conditions that are absent, malformed, unmet, or inapplicable.

Other missing cases apparent from the supplied text include:

- the authorization names a different authorized executor than the executor performing the invocation;
- the requested role is missing, invalid, or inconsistent with the role’s `action_authority` bounds or tool permissions;
- the applicable policy is missing, inactive, superseded, or does not permit the request;
- a required independence requirement is not met;
- an authorization is inactive or superseded;
- a principal declaration is missing a scope, has an unparseable scope, or has a scope too broad to qualify as bounded;
- a subordinate invocation is outside the parent authorization’s declared subordinate execution classes;
- material subordinate execution is undisclosed;
- a governed-evidence-producing tool has undeclared execution-path-changing configuration;
- a governed-evidence-producing or above-`read_only` invocation has undeclared material external interaction.

Not all of those necessarily need to be implemented in this slice, but the plan must either enumerate them as refusal outcomes, classify them as outside the meaning of “valid authorization,” or explicitly defer them without representing the result as full compliance.

6. **Decisions that constrain Slice D evidence admission**

Several decisions and records constrain future evidence admission:

- **RoleDefinition.** The receiving role’s `required_verified_properties` directly controls what evidence admission must establish. Section 4.13 says admission must enumerate verified properties against those requirements and “may not treat a property as established that no named verification record covers.”

- **Epistemic authority.** The role axis distinguishes `witness`, `advisor`, and `adjudicator`. Witness outputs require grounding in an observation source, span, measurement, or deterministic derivation. Unsupported hypotheses are advisor outputs, not witness evidence. This limits what epistemic status Slice D can admit.

- **Role constraints.** `may_assign_epistemic_status`, `requires_external_verification`, required independence, allowed input/output classes, catalog status, and maximum consequence class constrain the conditions under which outputs may enter governed evidence.

- **InvocationAuthorization.** The assigned role, consequence class, qualifications relied on, independence requirements, and conditions provide facts Slice D may need to assess whether the producing invocation was authorized for its stated function. But authorization does not itself admit output as evidence.

- **RoleQualification.** Qualification is execution-scoped to endpoint, profile, session-state constraints, and policy version. Slice D should not treat a qualification as portable to another execution context.

- **Consequence classification.** Section 8 makes plan admission high by default and permits modifiers only to raise consequence. That constrains the ceiling and safeguards expected for high-consequence admission-related work.

- **EvidenceAdmissionDecision itself.** It requires lineage and independence findings, disclosed provenance limitations, and named verification coverage. These are separate from authorization and remain unimplemented here.

- **Accountable approval fields in DecisionRecord.** `recommended_status` and `effective_status` are distinct so that a model recommendation does not appear to assign final status before accountable approval. Slice D must preserve that distinction.

The direct one-hop check may supply a narrow negative finding for one direct identity collision, but it cannot establish lineage independence generally.

7. **Mechanical checkability and missing checks**

Some criteria are mechanically testable if the schemas and fixtures are supplied:

- governed versus experimental classification;
- each listed refusal reason;
- an unterminated chain;
- an authorization outside declared scope;
- direct one-hop identity collision;
- ordinal maximum-rule consequence behavior;
- missing or out-of-scope qualifications.

However, several criteria are not mechanically specified by the supplied text:

- “All new behavior covered by tests.” No coverage threshold or definition of “all new behavior” is given.
- “the full suite passes offline.” This is operationally testable, but no suite definition, command, environment, or offline boundary is supplied.
- “the repository audit remains ok true verified_current.” No audit specification, command, or semantics for `verified_current` are provided.
- “cross-environment reproduction succeeds byte-identically.” No environments, build inputs, normalization rules, or artifact to compare are specified.
- “demonstrated against a real captured InvocationRecord.” No particular captured record or acceptance rule for “real” is included.
- “valid authorization” is used in the governed criterion without a complete definition of all validity checks.

Important missing checks include:

- rejection or explicit handling of a self-created standing-authority declaration;
- rejection of an authority scope that is absent, unbounded, unparsable, or broader than an allowed scope grammar;
- validation of who established, activated, superseded, or revoked an `AccountablePrincipal` record;
- authorization-condition enforcement;
- authorized-executor identity matching;
- activation and supersession behavior for `DecisionRecord`;
- policy applicability and policy-version checks;
- parent authorization checks for subordinate invocation classes;
- a test demonstrating that the one-hop result is not represented as a full lineage or independence finding;
- treatment of the Section 4.7 subordinate-executor, tool-configuration, and external-interaction disclosure constraints, whether enforced or deliberately deferred.

There is also a schema ambiguity. Section 4.13 defines inherited `DecisionRecord` fields including “issuer invocation,” “accountable approver,” evidence, policy authority, activation state, and supersession. The plan’s scope description for `InvocationAuthorization` instead names an “issuing principal” and a standing-authority or chained-authorization reference. The supplied text does not say how those fields relate. The plan’s requirement that field names and semantics follow the amendment “exactly” needs an explicit reconciliation.

8. **Recommendation: revise first**

Revise before admission. The necessary revisions are:

1. **Close the standing-authority bootstrap path.** Define how an `AccountablePrincipal` and its initial `authority_scope` become valid, including an independent approving or constituting authority, activation, supersession, and any delegation validation. A principal’s own declaration should not alone establish the standing authority that makes its own authorization self-standing.

2. **Define bounded scope mechanically.** Specify the dimensions of `authority_scope` and reject scopes that are universal, unparseable, or circular. A declaration narrowly tailored to authorize itself should not be an acceptable root merely because it has a stated scope.

3. **Reconcile the schemas.** Explicitly include the inherited `DecisionRecord` requirements and state the relationship among issuer invocation, issuing principal, accountable approver, policy authority, activation state, supersession, and authorization-chain references.

4. **Complete the refusal model.** At minimum add explicit outcomes for unsatisfied authorization conditions, authorized-executor mismatch, inactive or superseded records, invalid or missing policy applicability, and invalid standing-authority declarations. State whether Section 4.7 disclosure violations are checked here or excluded from the meaning of valid authorization.

5. **Constrain the meaning of “governed.”** Specify that it means record-covered authorization classification only, not execution prevention, evidence admission, correctness, independent review, full disclosure compliance, or a positive independence finding.

6. **Make the one-hop limitation machine-visible as well as documented.** The output should identify the check as direct-only, rather than emitting an unqualified result that could be consumed as a general self-adjudication or independence determination.

7. **Make success criteria executable.** Name the audit procedure, offline test procedure, reproducibility environments and artifact, coverage standard, and the fixtures or record properties required for the “real captured InvocationRecord” criterion.

The plan correctly states several of its intended limits, but the authority-root mechanism is still underdefined in a way that permits the very self-authorization problem the amendment is intended to prevent.
```

## Claude Response

- model: `claude-sonnet-5`

```
## 1. Abusing chain termination at "standing authority"

The termination rule reads: "A principal holds standing authority within a declared `authority_scope`; authorizations the principal issues inside that scope are self-standing and require no prior authorization." The only stated guard is: "Standing authority is declared, bounded, and recorded. A principal may not assert standing authority implicitly, by practice, or for a scope wider than its declared `authority_scope`."

Nothing in this text constrains the *content* or *breadth* of what may be declared as `authority_scope` — "bounded" means the declaration has a stated boundary, not that the boundary is narrow, justified, or reviewed by anyone other than the declarant. This gap is acknowledged directly: "`[OPEN]` Whether standing authority requires periodic re-declaration or review, and what evidence a scope declaration must carry beyond its own statement."

Abuse path: an entity registers as an `AccountablePrincipal` (e.g. `principal_kind`: "pseudonymous operator identity" per 4.13) and declares an `authority_scope` broad enough to cover whatever it wants to authorize — e.g. "all invocations of drafting and adjudication roles." Every authorization it issues inside that self-declared scope is, by the text, "self-standing and require[s] no prior authorization." Separately, nothing in Section 3 or 4.13 prohibits the same human/organization from also being the executor of the invocation it authorizes as principal — the text only insists these are logically distinct roles ("Standing authority is not a capability of executors... it holds it only as an AccountablePrincipal within a declared scope, which is a separate role"), not that one entity cannot hold both roles simultaneously. So a single actor declares a scope, issues an authorization to itself-as-executor inside that scope, and the chain terminates immediately — satisfying every quoted requirement while functioning as self-authorization. Slice C's one-hop check does not close this: it fires only on adjudicator-role collisions over produced artifacts, not on principal-issuer/executor identity generally.

## 2. Is "governed" meaningful, or manufactured assurance?

The plan states outright: "an invocation is classified governed only when a valid authorization covers it, experimental otherwise... Nothing is refused execution," and "Authorization classifies; it does not gate. Execution refusal requires a separately admitted plan." The risk section itself names the hazard: "An authorization system that classifies but never refuses can create a false sense of control: readers may assume governed means checked when it means covered by a record."

Argued from the text: "governed" is meaningful only as a bookkeeping fact — a `DecisionRecord` of kind `invocation_authorization` exists and covers the invocation. It carries no causal effect on what happens (experimental and governed invocations execute identically), and — per Q1 — the authorization behind "governed" can itself terminate at an unreviewed, self-declared scope. The plan's own risk section concedes the assurance gap rather than closing it structurally, relying instead on documentation ("Both limits are stated in the documentation... rather than left to inference"). So the status is real as a record-existence claim and not real as a safety or correctness claim; the plan discloses this distinction but does not eliminate the risk that readers collapse the two, which is the exact hazard it names.

## 3. Two-hop case the one-hop check misses

The check: "if the artifact carries a `produced_by` relation to an InvocationRecord whose `executed_by` equals the executor under authorization, refuse. Scoped explicitly to one hop."

Construction: executor A drafts artifact X. A distinct invocation by executor B (e.g. a "cleanup," reformatting, or summarization pass — itself possibly `spawned` per the 4.7 composite-executor disclosure constraint) consumes X and produces derived artifact Y; Y's `produced_by` points to B's InvocationRecord. Executor A is then authorized as adjudicator over Y. The check inspects only Y's immediate `produced_by` (executor B, not A) and passes — no collision is flagged — even though A is reviewing its own drafted content laundered through one intermediate step.

Sufficiency of disclosure: the plan states this limitation repeatedly and explicitly — as a non-goal ("Multi-hop lineage traversal, independence assessment, or evidence admission (Slice D)"), in the risk section ("the one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision"), and as a required documentation constraint ("Any claim that the one-hop check implements C3. It implements C3's most direct case only, and the documentation must say so"). As textual disclosure this is explicit and repeated across three independent sections, which is sufficient as *disclosure*. Whether it is sufficient as *risk mitigation* is a separate question this text does not resolve: the motivating incident quoted in the objective is itself a one-hop case, so the check addresses the exhibited incident, but a reader encountering only the success-criteria language ("refuses an adjudicator authorization over an artifact produced by the same executor identity") without reading non-goals/risk could reasonably believe more is covered.

## 4. Scope containment

Checking the `scope` list against the plan's own `non_goals`:

- `RoutingDecision` fields (candidates, rejection reasons, catalog snapshot — 4.13) are absent from scope, consistent with the non-goal "Routing, escalation, or model selection (RoutingDecision remains deferred)." No leak.
- `EvidenceAdmissionDecision` fields (admitted status, verified-properties enumeration — 4.13) are absent from scope, consistent with the non-goal listing "evidence admission (Slice D)." No leak.
- `InvocationAuthorization`'s "independence requirements" field is included only as a stored field ("carrying... independence requirements... as ABS-0004 4.13 enumerates"), not as computed independence assessment, which is separately excluded ("independence assessment... (Slice D)"). Consistent.
- `RoleDefinition`'s `required_verified_properties` field (4.9) is in scope as schema only; *using* it to admit evidence is 4.13's EvidenceAdmissionDecision territory, which is out of scope. This is an interface point worth flagging — Slice C fixes the field's shape, which Slice D must then consume unchanged — but it is not itself a scope violation as written.

No item in the `scope` list appears to perform routing selection or evidence admission logic. The boundary as stated holds; the load-bearing risk is not scope creep but that decisions made here (role taxonomy, consequence scheme) will constrain Slice D later (see Q6), which the risk section itself flags rather than conceals.

## 5. Completeness of the six refusal reasons

Listed: "no qualification for this executor and role, qualification out of execution scope, consequence above the role ceiling, unterminated authorization chain, standing authority claimed outside its declared scope, and self-adjudication conflict."

Missing case: Section 3's subordinate-inheritance rule — "A subordinate execution outside the declared classes requires its own authorization. Undeclared subordinate execution is a disclosure violation under 4.7, not an implicitly authorized act." If `authorize()` is invoked for a subordinate invocation whose parent authorization's conditions do not declare the permitted subordinate execution classes, this must not be treated as authorized — but none of the six reasons names this case. "No qualification for this executor and role" does not fit, since the subordinate executor may hold a perfectly valid qualification for its role in isolation; the defect is that the *parent authorization* does not declare coverage for it. This is a refusal case with no enumerated reason.

## 6. Decisions here that constrain Slice D's evidence admission

- Role taxonomy and constraint fields (`task_function`/`epistemic_authority`/`action_authority`, `required_verified_properties`, `may_assign_epistemic_status`, etc., per 4.9): the risk section states directly, "Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate." `EvidenceAdmissionDecision` explicitly checks "against the receiving role's `required_verified_properties`" (4.13), so however Slice C schemas that field, Slice D inherits it as-is.
- Consequence classification (Section 8, scope item 7): consequence class is a shared `DecisionRecord` concept (4.13) across all three decision kinds; the monotonic max-rule and governed-exception mechanism built in Slice C is the only such mechanism defined and would be reused rather than redefined.
- `AccountablePrincipal` schema (4.13): `DecisionRecord`'s shared field "accountable approver" applies to `EvidenceAdmissionDecision` as much as to `InvocationAuthorization`; the principal schema built here fixes that field's shape for Slice D.
- `RoleQualification`'s execution-scope model (4.6): whatever the executor was qualified for at authorization time is part of the evidentiary chain Slice D's "lineage and independence findings" would need to reference.

## 7. Mechanical checkability of success criteria

Checkable as stated: criteria 1 (governed/experimental fixtures), 3 (chain-termination and out-of-scope refusals), 4 (one-hop check against a real record), 6 (qualification execution-scope rejection).

Not mechanically checkable as stated:
- "authorization never fails silently and never defaults to permitted" (criterion 2) — this is a universal negative over all code paths; fixtures can demonstrate enumerated cases do not fail silently, but cannot mechanically prove the *absence* of an unhandled silent-permit path.
- "Consequence is monotonic... a test asserts the maximum rule over an ordinal scale rather than arithmetic" (criterion 5) — monotonicity is stated as a general property, but the check described is example-based (specific fixture assertions), not an exhaustive or property-based proof over the modifier combination space.
- "All new behavior covered by tests" (criterion 7) — no coverage metric or threshold is stated anywhere in this text, so "covered" has no mechanical definition here.

Missing check: the plan's own constraint states "Slice A capture and Slice B resolution behavior are unchanged: no field, path, or default of either is altered," but no success criterion verifies this by regression fixture or diff against prior behavior. Given it is stated as a hard constraint, its absence from `success_criteria` is a gap.

## 8. Recommendation

**Admit with named conditions**, not as written and not requiring full revision. The plan is largely self-disclosing about its own limits (one-hop bound, non-implementation of C3, no-refusal boundary), and the gaps found are additive rather than structural. Conditions:

1. Add an enumerated refusal reason (or explicit named exclusion, if deferred) for undeclared subordinate execution under Section 3 / 4.7's composite-executor disclosure constraint, so `authorize()` does not encounter this case silently.
2. Add a success criterion verifying, by regression fixture, that Slice A capture and Slice B resolution outputs are byte-identical before and after this change — matching the plan's own stated constraint, which currently has no corresponding check.
3. Require `AUTHORIZATION_RECORDS.md` to state explicitly that `authority_scope` breadth is self-declared with no adopted requirement of independent review (per the still-open Section 3 question), and that this slice does not prevent a principal from issuing authorization to an executor identity coinciding with itself.
4. Restate success criteria 2 and 5 to match what is actually demonstrated — enumerated-fixture coverage of named cases — rather than the universal claims ("never," "is monotonic") currently used, or add property-based tests if the universal claim is intended to hold.
```
