# COMP-0046: Provider Comparison — Slice C admission Q8 slice-d-constraints

## Metadata

- comparison_id: `COMP-0046`
- title: `Slice C admission Q8 slice-d-constraints`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-e9cc2ca90d7fd906.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0046", "target_id": "INV-e9cc2ca90d7fd906"}, {"authoritative": false, "evidence": "docs/invocations/INV-a7aa0d4b2a67252f.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0046", "target_id": "INV-a7aa0d4b2a67252f"}]`
- created_at: `2026-07-28T18:54:55.463847+00:00`
- command: `scripts/compare_providers.py --title Slice C admission Q8 slice-d-constraints You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: the ABS-0004 v7 amendment is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force yet.

One disclosure, because the plan text refers to it and withholding it would be dishonest rather than isolating: v7 replaces a v6 rule that claimed to prevent the authorization regress from being closed by convenience, after two reviewers in a prior round independently defeated it. Do not accept the plan's characterisation of that break, and do not treat it as the only one available.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q8 ===
Which decisions in this slice constrain later evidence admission and lineage work, and which of them would be expensive to reverse once records exist?

Distinguish decisions that only require changing validation code from decisions that would require migrating existing records, and say which category each falls in.

=== EVIDENCE ABS-0004:v7:S4.13 :: ABS-0004 v7 Section 4.13 (DecisionRecord, AccountablePrincipal) ===
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

=== EVIDENCE ABS-0004:v7:S4.9 :: ABS-0004 v7 Section 4.9 (RoleDefinition, three axes) ===
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

=== EVIDENCE ABS-0004:v7:S4.6-4.7 :: ABS-0004 v7 Sections 4.6-4.7 (qualification, executor identities, disclosure) ===
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

=== EVIDENCE PLAN-20260723-0002 :: PLAN-20260723-0002 (revised, corrected at fee90da) ===
{
  "constraints": [
    "Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan.",
    "Field names and semantics follow ABS-0004 v7 exactly; deviations require an ABS revision first.",
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
  "mitigation": "Both limits are stated in the documentation and in the capability record rather than left to inference: governed means an authorization covers the invocation, and the self-adjudication check is one hop. Refusal reasons are enumerated so that a permitted outcome is never a silent default. The role vocabulary is copied from ABS-0004 v7 verbatim rather than invented, and the seed roles describe practice already visible in the record. The ten refusal reasons replace the original six after COMP-0037 found four missing. Success criteria are restated to claim only enumerated-fixture coverage rather than universal properties, per the same round's finding that 'never fails silently' and 'is monotonic' are not mechanically checkable as written. Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected.",
  "next_action": "Re-run the admission comparison round with the revised plan and the ABS-0004 v7 amendment attached as text; on operator adjudication, admit v7 and issue the plan's admission warrant.",
  "non_goals": [
    "Refusing or blocking any execution. Authorization classifies; it does not gate. Execution refusal requires a separately admitted plan.",
    "Routing, escalation, or model selection (RoutingDecision remains deferred).",
    "Multi-hop lineage traversal, independence assessment, or evidence admission (Slice D).",
    "Retroactive authorization of invocations captured before this slice; they remain experimental, and the pre-provenance boundary applies.",
    "Any claim that the one-hop check implements C3. It implements C3's most direct case only, and the documentation must say so.",
    "Automatic consequence assignment from artifact content; consequence is declared per authorization with the default derived from target type.",
    "Cryptographic attestation of principals; ABS-0004 records it as a later implementation mechanism, not an ontology requirement.",
    "Any claim that AI-Lab validates a standing-authority declaration. Per ABS-0004 v7 P7, root authority is extra-systemic: the system records the claim and cannot verify it, and no record, scope grammar, or internal approval step may be presented as verification.",
    "Refusing a self-issued authorization. Self-issue is marked and disqualified from independence, not blocked: at the root of any chain the accountable party necessarily authorizes work it is responsible for."
  ],
  "objective": "Make the authority separation AI-Lab has practised in conversation structural: who may perform what, under which role, at what consequence, on whose standing authority, recorded as evidence rather than as testimony. The immediate motivation is concrete: on 2026-07-23 a model-default change would have set the reviewer slot to the drafting executor's own identity, collapsing reviewer and author under C3. Nothing in the system would have noticed; it was caught because a human happened to be told. Slice C makes the most direct case of that collision detectable by machine.",
  "plan_id": "PLAN-20260723-0002",
  "proposed_change": "After a separate admission checkpoint, and after ABS-0004 v7 is admitted: add ai_lab/governance/roles.py (RoleDefinition, RoleQualification, AccountablePrincipal schemas and validators), ai_lab/governance/authorization.py (InvocationAuthorization records, the pure authorize() function, consequence classification, the experimental-versus-governed classifier, and the one-hop self-adjudication check), predicate-registry entries, documentation, and tests. No change to provider-call behavior, no change to Slice A capture or Slice B resolution, and no refusal of any execution.",
  "rationale": [
    "ABS-0004's enforcement matrix records C6 authority separation as 'adopted, not currently evidenced': no artifact names the check. Slice C is what lets that row cite something.",
    "The near-miss of 2026-07-23 is the exhibit: identity collision between reviewer and author was invisible to every test, and was avoided by chance rather than by control.",
    "Slice A supplies produced_by and executed_by, so a one-hop identity collision is detectable now without the ancestry traversal that belongs to Slice D. The cheap case is available; the expensive case stays deferred.",
    "ABS-0004 v7 fixes where authorization chains terminate - at an AccountablePrincipal's recorded standing-authority claim within a declared scope - and states plainly that this does not close the bootstrap regress. The open question remains open: v7 records that no internal control can close it and that the constraint supplies visibility, not prevention. What is settled before any code depends on it is the termination rule and an honest account of its limits, not a resolution of the regress.",
    "COMP-0037 split: one reviewer recommended revise-first, the other admit-with-conditions, and both independently constructed the same self-authorization path through v6's chain termination. The revision follows the stronger recommendation. v7 does not answer the break with a tighter internal control, because no internal control can answer it; it records that root authority is extra-systemic and makes the coincidence of issuer and executor visible instead."
  ],
  "repo_commit": "96209e95a722c5e1f6d18061e746ff75b33b3fca",
  "risk": "An authorization system that classifies but never refuses can create a false sense of control: readers may assume governed means checked when it means covered by a record. The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision. Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate. Beyond those: v7 makes the honest limitation explicit rather than closing it, so a reader who wants an assurance AI-Lab cannot give will find the system declining to give it, which is correct and may be mistaken for a defect. The self_issued marking depends on identifying when two records name the same party, which is straightforward for exact identifiers and undecidable in general; the implementation must not claim to detect sameness it cannot establish.",
  "schema_version": "v1",
  "scope": [
    "A roles module defining schema v1 for RoleDefinition (task_function, epistemic_authority, action_authority, and the constraint fields ABS-0004 4.9 enumerates), with a validator, canonical serialization, and deterministic identity and path rules under docs/roles/.",
    "RoleQualification records, execution-scoped as ABS-0004 4.6 requires: qualified executor, role, service endpoint scope, permitted ExecutionProfile constraints, session-state constraints, policy version, and the evaluation evidence relied on. A qualification never transfers implicitly to another endpoint or a materially different profile, and the validator rejects a qualification lacking an execution scope.",
    "AccountablePrincipal records with principal_id, principal_kind, authority_scope, and delegation_reference, carrying no personal identifying data.",
    "InvocationAuthorization as a DecisionRecord kind: invocation request, authorized executor, assigned role, consequence class, applicable policy, qualifications relied on, independence requirements, conditions, issuing principal, and the standing-authority or chained-authorization reference that terminates its chain.",
    "A pure authorize() function over stored records returning an authorization outcome or one of the enumerated refusal reasons: no qualification for this executor and role; qualification out of execution scope; consequence above the role ceiling; unterminated authorization chain; standing authority claimed outside its declared scope; authorization conditions unmet, malformed, or absent; authorized executor does not match the executor performing the invocation; the authorization or a record it relies on is inactive or superseded; subordinate execution outside the classes its parent authorization declares; and self-adjudication conflict. Ten reasons, each with a fixture. COMP-0037 found the sixth, seventh, eighth, and ninth of these missing from the six originally proposed.",
    "The one-hop self-adjudication check: for an adjudicator-authority role over a target artifact, if the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization, refuse. Scoped explicitly to one hop; multi-hop ancestry is Slice D.",
    "Consequence classification per ABS-0004 Section 8: default by target type, effective consequence as the maximum of the default and applicable modifier levels, modifiers only raising, and downward adjustment only as a governed exception carrying reason, principal, scope, evidence, and review condition.",
    "The experimental-versus-governed boundary: a classify function marking an invocation governed only when a valid authorization covers it, experimental otherwise. Classification only; no invocation is refused execution by this slice.",
    "Predicate-registry entries for the Slice C predicates: assigned_role, authorized_by, authorizes, qualifies_executor, qualifies_for, issued_under, based_on, approved_by.",
    "Validator fixtures covering valid records, each rejection class, and each refusal reason, plus an integration fixture authorizing an invocation against stored role, qualification, and principal records offline.",
    "Field reconciliation with ABS-0004 4.13: InvocationAuthorization carries the inherited DecisionRecord fields (target, recommended_status and effective_status, issuer invocation, accountable approver, evidence, policy authority, activation state, supersession) alongside its kind-specific fields, and the documentation states how issuing principal, issuer invocation, and accountable approver relate. COMP-0037 found the plan's field list and the ontology's inherited list unreconciled.",
    "Self-issued marking per ABS-0004 v7: where the issuing principal and the authorized executor are the same party, the authorization records self_issued true. Self-issued authorizations are permitted and are disqualified from counting as independent authorization wherever independence is required.",
    "The one-hop bound is machine-visible, not only documented: the self-adjudication outcome carries an explicit check_depth field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding."
  ],
  "source_capability_ids": [
    "CAP-0015",
    "CAP-0016"
  ],
  "source_gap_id": "GAP-0005",
  "status": "proposed",
  "success_criteria": [
    "A stored invocation is classified governed when a valid authorization covers it and experimental otherwise, demonstrated by fixtures for both outcomes.",
    "Each of the ten enumerated refusal reasons is exercised by a fixture and yields that reason; no fixture path returns a permitted outcome without a matching authorization record.",
    "An authorization whose chain terminates nowhere is refused, and an authorization issued outside a principal's declared authority_scope is refused, each with its own reason.",
    "The one-hop self-adjudication check refuses an adjudicator authorization over an artifact produced by the same executor identity, demonstrated against a real captured InvocationRecord, permits it when the identities differ, and carries a check_depth field marking the result as direct-only in both cases.",
    "Consequence classification is exercised over the enumerated modifier set: for each modifier, a fixture asserts the effective class equals the maximum of the default and the modifier level, and a downward adjustment without a recorded governed exception is refused. This is enumerated-fixture coverage of the named cases, not a proof of monotonicity over all inputs.",
    "A qualification lacking an execution scope is rejected, and a qualification is not honoured for an endpoint or execution profile outside its scope.",
    "A self-issued authorization is accepted, carries self_issued true, and is reported as not independent by any check that asks for independent authorization.",
    "Regression: Slice A capture and Slice B resolution are unchanged, demonstrated by a fixture that runs both against stored records before and after authorization code is importable and asserts byte-identical outputs. COMP-0037 found this constraint had no corresponding check.",
    "The new modules are covered by tests exercising every public entrypoint and every enumerated outcome; the full suite passes offline with no network access.",
    "The repository audit reports ok true verified_current, and commit-level cross-environment reproduction from the public repository yields byte-identical checksums for every delivered file."
  ],
  "summary": "Implement ABS-0004 v7 Slice C: RoleDefinition records on the three admitted axes, execution-scoped RoleQualification, InvocationAuthorization as a DecisionRecord kind, consequence classification, and the experimental-versus-governed boundary. An authorization is issued by an AccountablePrincipal holding standing authority within a declared scope, or chains to one; an authorization that chains to nothing is unauthorized rather than permitted. Authorization has one consequence in this slice and no others: an invocation is classified governed only when an authorization covers it, and experimental otherwise. Nothing is refused execution. The authorization function additionally performs a one-hop self-adjudication check using Slice A provenance: if the artifact under adjudication carries an InvocationRecord whose executor identity equals the executor being authorized, authorization is refused with an enumerated reason.",
  "title": "Roles, qualification, and invocation authorization (ABS-0004 Slice C)"
}

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: the ABS-0004 v7 amendment is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force yet.

One disclosure, because the plan text refers to it and withholding it would be dishonest rather than isolating: v7 replaces a v6 rule that claimed to prevent the authorization regress from being closed by convenience, after two reviewers in a prior round independently defeated it. Do not accept the plan's characterisation of that break, and do not treat it as the only one available.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q8 ===
Which decisions in this slice constrain later evidence admission and lineage work, and which of them would be expensive to reverse once records exist?

Distinguish decisions that only require changing validation code from decisions that would require migrating existing records, and say which category each falls in.

=== EVIDENCE ABS-0004:v7:S4.13 :: ABS-0004 v7 Section 4.13 (DecisionRecord, AccountablePrincipal) ===
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

=== EVIDENCE ABS-0004:v7:S4.9 :: ABS-0004 v7 Section 4.9 (RoleDefinition, three axes) ===
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

=== EVIDENCE ABS-0004:v7:S4.6-4.7 :: ABS-0004 v7 Sections 4.6-4.7 (qualification, executor identities, disclosure) ===
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

=== EVIDENCE PLAN-20260723-0002 :: PLAN-20260723-0002 (revised, corrected at fee90da) ===
{
  "constraints": [
    "Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan.",
    "Field names and semantics follow ABS-0004 v7 exactly; deviations require an ABS revision first.",
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
  "mitigation": "Both limits are stated in the documentation and in the capability record rather than left to inference: governed means an authorization covers the invocation, and the self-adjudication check is one hop. Refusal reasons are enumerated so that a permitted outcome is never a silent default. The role vocabulary is copied from ABS-0004 v7 verbatim rather than invented, and the seed roles describe practice already visible in the record. The ten refusal reasons replace the original six after COMP-0037 found four missing. Success criteria are restated to claim only enumerated-fixture coverage rather than universal properties, per the same round's finding that 'never fails silently' and 'is monotonic' are not mechanically checkable as written. Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected.",
  "next_action": "Re-run the admission comparison round with the revised plan and the ABS-0004 v7 amendment attached as text; on operator adjudication, admit v7 and issue the plan's admission warrant.",
  "non_goals": [
    "Refusing or blocking any execution. Authorization classifies; it does not gate. Execution refusal requires a separately admitted plan.",
    "Routing, escalation, or model selection (RoutingDecision remains deferred).",
    "Multi-hop lineage traversal, independence assessment, or evidence admission (Slice D).",
    "Retroactive authorization of invocations captured before this slice; they remain experimental, and the pre-provenance boundary applies.",
    "Any claim that the one-hop check implements C3. It implements C3's most direct case only, and the documentation must say so.",
    "Automatic consequence assignment from artifact content; consequence is declared per authorization with the default derived from target type.",
    "Cryptographic attestation of principals; ABS-0004 records it as a later implementation mechanism, not an ontology requirement.",
    "Any claim that AI-Lab validates a standing-authority declaration. Per ABS-0004 v7 P7, root authority is extra-systemic: the system records the claim and cannot verify it, and no record, scope grammar, or internal approval step may be presented as verification.",
    "Refusing a self-issued authorization. Self-issue is marked and disqualified from independence, not blocked: at the root of any chain the accountable party necessarily authorizes work it is responsible for."
  ],
  "objective": "Make the authority separation AI-Lab has practised in conversation structural: who may perform what, under which role, at what consequence, on whose standing authority, recorded as evidence rather than as testimony. The immediate motivation is concrete: on 2026-07-23 a model-default change would have set the reviewer slot to the drafting executor's own identity, collapsing reviewer and author under C3. Nothing in the system would have noticed; it was caught because a human happened to be told. Slice C makes the most direct case of that collision detectable by machine.",
  "plan_id": "PLAN-20260723-0002",
  "proposed_change": "After a separate admission checkpoint, and after ABS-0004 v7 is admitted: add ai_lab/governance/roles.py (RoleDefinition, RoleQualification, AccountablePrincipal schemas and validators), ai_lab/governance/authorization.py (InvocationAuthorization records, the pure authorize() function, consequence classification, the experimental-versus-governed classifier, and the one-hop self-adjudication check), predicate-registry entries, documentation, and tests. No change to provider-call behavior, no change to Slice A capture or Slice B resolution, and no refusal of any execution.",
  "rationale": [
    "ABS-0004's enforcement matrix records C6 authority separation as 'adopted, not currently evidenced': no artifact names the check. Slice C is what lets that row cite something.",
    "The near-miss of 2026-07-23 is the exhibit: identity collision between reviewer and author was invisible to every test, and was avoided by chance rather than by control.",
    "Slice A supplies produced_by and executed_by, so a one-hop identity collision is detectable now without the ancestry traversal that belongs to Slice D. The cheap case is available; the expensive case stays deferred.",
    "ABS-0004 v7 fixes where authorization chains terminate - at an AccountablePrincipal's recorded standing-authority claim within a declared scope - and states plainly that this does not close the bootstrap regress. The open question remains open: v7 records that no internal control can close it and that the constraint supplies visibility, not prevention. What is settled before any code depends on it is the termination rule and an honest account of its limits, not a resolution of the regress.",
    "COMP-0037 split: one reviewer recommended revise-first, the other admit-with-conditions, and both independently constructed the same self-authorization path through v6's chain termination. The revision follows the stronger recommendation. v7 does not answer the break with a tighter internal control, because no internal control can answer it; it records that root authority is extra-systemic and makes the coincidence of issuer and executor visible instead."
  ],
  "repo_commit": "96209e95a722c5e1f6d18061e746ff75b33b3fca",
  "risk": "An authorization system that classifies but never refuses can create a false sense of control: readers may assume governed means checked when it means covered by a record. The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision. Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate. Beyond those: v7 makes the honest limitation explicit rather than closing it, so a reader who wants an assurance AI-Lab cannot give will find the system declining to give it, which is correct and may be mistaken for a defect. The self_issued marking depends on identifying when two records name the same party, which is straightforward for exact identifiers and undecidable in general; the implementation must not claim to detect sameness it cannot establish.",
  "schema_version": "v1",
  "scope": [
    "A roles module defining schema v1 for RoleDefinition (task_function, epistemic_authority, action_authority, and the constraint fields ABS-0004 4.9 enumerates), with a validator, canonical serialization, and deterministic identity and path rules under docs/roles/.",
    "RoleQualification records, execution-scoped as ABS-0004 4.6 requires: qualified executor, role, service endpoint scope, permitted ExecutionProfile constraints, session-state constraints, policy version, and the evaluation evidence relied on. A qualification never transfers implicitly to another endpoint or a materially different profile, and the validator rejects a qualification lacking an execution scope.",
    "AccountablePrincipal records with principal_id, principal_kind, authority_scope, and delegation_reference, carrying no personal identifying data.",
    "InvocationAuthorization as a DecisionRecord kind: invocation request, authorized executor, assigned role, consequence class, applicable policy, qualifications relied on, independence requirements, conditions, issuing principal, and the standing-authority or chained-authorization reference that terminates its chain.",
    "A pure authorize() function over stored records returning an authorization outcome or one of the enumerated refusal reasons: no qualification for this executor and role; qualification out of execution scope; consequence above the role ceiling; unterminated authorization chain; standing authority claimed outside its declared scope; authorization conditions unmet, malformed, or absent; authorized executor does not match the executor performing the invocation; the authorization or a record it relies on is inactive or superseded; subordinate execution outside the classes its parent authorization declares; and self-adjudication conflict. Ten reasons, each with a fixture. COMP-0037 found the sixth, seventh, eighth, and ninth of these missing from the six originally proposed.",
    "The one-hop self-adjudication check: for an adjudicator-authority role over a target artifact, if the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization, refuse. Scoped explicitly to one hop; multi-hop ancestry is Slice D.",
    "Consequence classification per ABS-0004 Section 8: default by target type, effective consequence as the maximum of the default and applicable modifier levels, modifiers only raising, and downward adjustment only as a governed exception carrying reason, principal, scope, evidence, and review condition.",
    "The experimental-versus-governed boundary: a classify function marking an invocation governed only when a valid authorization covers it, experimental otherwise. Classification only; no invocation is refused execution by this slice.",
    "Predicate-registry entries for the Slice C predicates: assigned_role, authorized_by, authorizes, qualifies_executor, qualifies_for, issued_under, based_on, approved_by.",
    "Validator fixtures covering valid records, each rejection class, and each refusal reason, plus an integration fixture authorizing an invocation against stored role, qualification, and principal records offline.",
    "Field reconciliation with ABS-0004 4.13: InvocationAuthorization carries the inherited DecisionRecord fields (target, recommended_status and effective_status, issuer invocation, accountable approver, evidence, policy authority, activation state, supersession) alongside its kind-specific fields, and the documentation states how issuing principal, issuer invocation, and accountable approver relate. COMP-0037 found the plan's field list and the ontology's inherited list unreconciled.",
    "Self-issued marking per ABS-0004 v7: where the issuing principal and the authorized executor are the same party, the authorization records self_issued true. Self-issued authorizations are permitted and are disqualified from counting as independent authorization wherever independence is required.",
    "The one-hop bound is machine-visible, not only documented: the self-adjudication outcome carries an explicit check_depth field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding."
  ],
  "source_capability_ids": [
    "CAP-0015",
    "CAP-0016"
  ],
  "source_gap_id": "GAP-0005",
  "status": "proposed",
  "success_criteria": [
    "A stored invocation is classified governed when a valid authorization covers it and experimental otherwise, demonstrated by fixtures for both outcomes.",
    "Each of the ten enumerated refusal reasons is exercised by a fixture and yields that reason; no fixture path returns a permitted outcome without a matching authorization record.",
    "An authorization whose chain terminates nowhere is refused, and an authorization issued outside a principal's declared authority_scope is refused, each with its own reason.",
    "The one-hop self-adjudication check refuses an adjudicator authorization over an artifact produced by the same executor identity, demonstrated against a real captured InvocationRecord, permits it when the identities differ, and carries a check_depth field marking the result as direct-only in both cases.",
    "Consequence classification is exercised over the enumerated modifier set: for each modifier, a fixture asserts the effective class equals the maximum of the default and the modifier level, and a downward adjustment without a recorded governed exception is refused. This is enumerated-fixture coverage of the named cases, not a proof of monotonicity over all inputs.",
    "A qualification lacking an execution scope is rejected, and a qualification is not honoured for an endpoint or execution profile outside its scope.",
    "A self-issued authorization is accepted, carries self_issued true, and is reported as not independent by any check that asks for independent authorization.",
    "Regression: Slice A capture and Slice B resolution are unchanged, demonstrated by a fixture that runs both against stored records before and after authorization code is importable and asserts byte-identical outputs. COMP-0037 found this constraint had no corresponding check.",
    "The new modules are covered by tests exercising every public entrypoint and every enumerated outcome; the full suite passes offline with no network access.",
    "The repository audit reports ok true verified_current, and commit-level cross-environment reproduction from the public repository yields byte-identical checksums for every delivered file."
  ],
  "summary": "Implement ABS-0004 v7 Slice C: RoleDefinition records on the three admitted axes, execution-scoped RoleQualification, InvocationAuthorization as a DecisionRecord kind, consequence classification, and the experimental-versus-governed boundary. An authorization is issued by an AccountablePrincipal holding standing authority within a declared scope, or chains to one; an authorization that chains to nothing is unauthorized rather than permitted. Authorization has one consequence in this slice and no others: an invocation is classified governed only when an authorization covers it, and experimental otherwise. Nothing is refused execution. The authorization function additionally performs a one-hop self-adjudication check using Slice A provenance: if the artifact under adjudication carries an InvocationRecord whose executor identity equals the executor being authorized, authorization is refused with an enumerated reason.",
  "title": "Roles, qualification, and invocation authorization (ABS-0004 Slice C)"
}

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
Neither proposed instrument has governance force. The following are therefore prospective design commitments, not admitted requirements.

| Decision in this slice | Constraint on later evidence admission / lineage work | Reversal category once records exist |
|---|---|---|
| `RoleDefinition` uses the three axes and carries constraint fields, especially `required_verified_properties`, `required_independence`, `requires_external_verification`, and `may_assign_epistemic_status` | `EvidenceAdmissionDecision` must enumerate verified properties against the receiving role’s `required_verified_properties`; it cannot treat an uncovered property as established. Role definitions therefore determine what later admission must prove and which outputs can carry epistemic status. | **Existing-record migration and reassessment.** Changing axes, values, or the meaning of a required property would require updating role records and re-evaluating admission decisions that relied on those roles. Adding a validator for an unchanged role schema is **validation-code only**. |
| The distinction between task, epistemic, action, and accountable authority | Admission cannot infer acceptance authority from artifact production, and later lineage work must retain the distinction between an executor, an approver, and an accountable principal. | **Existing-record migration** if identities or fields have been collapsed in stored records. A new validator enforcing an already-recorded separation is **validation-code only**, though historical records may need reclassification if their prior status depended on the collapse. |
| `DecisionRecord` inherited fields, including distinct `recommended_status` and `effective_status`, issuer invocation, accountable approver, evidence, policy authority, activation state, and supersession | Later admission requires a record that distinguishes a recommendation from accountable final status and can identify the evidence, authority, and supersession state on which admission relied. | **Existing-record migration.** Adding inherited fields or splitting a previously conflated status changes persisted decision meaning and requires backfill or explicit unknown values for old records. |
| `EvidenceAdmissionDecision` has admitted artifact or claim, epistemic status, lineage and independence findings, provenance limitations, and verified-property enumeration | This is the direct future admission schema. It fixes the evidence needed to explain why an artifact or claim entered governed evidence and prevents unsupported property assertions. | **Existing-record migration and re-adjudication.** Records admitted without these fields cannot simply be treated as if they contained lineage, independence, or verification findings. Validators alone can enforce the rule only for new decisions. |
| The open choice whether existing warrant/admission records are extended or a new record family is created, and whether kinds are subtypes or one family | This unresolved choice controls record identity, references, query patterns, supersession, and how authorization and admission records relate. | **Expensive existing-record migration if records are created before resolution.** A later family split, merge, or subtype conversion would require transforming records and their references. This is not merely a validator change. |
| Execution-scoped `RoleQualification`: endpoint, `ExecutionProfile` constraints, session-state constraints, and policy version; no implicit transfer | Admission and lineage work can rely only on qualifications tied to the executor’s actual execution context. A later admission cannot safely treat an executor as qualified merely because it was qualified elsewhere. | **Existing-record migration/revalidation** if the scope fields or transfer rule change, because old qualification records and authorizations relying on them must be rechecked. Rejecting new out-of-scope qualifications under the unchanged representation is **validation-code only**. |
| `AccountablePrincipal` with `authority_scope` and `delegation_reference`; authorization chains terminate at a recorded standing-authority claim within scope | Later admission has a recorded authority path and can distinguish an in-scope authority claim from an unterminated or out-of-scope authorization. The plan also makes root authority extra-systemic rather than internally verified. | **Existing-record migration and re-evaluation** if scope or delegation semantics change, because authorization-chain conclusions depend on them. Adding scope validation for records already containing the needed fields is **validation-code only** for future use, but historical governed classifications would need recomputation if they are retained as conclusions. |
| `self_issued` marking and the rule that self-issued authorization cannot count as independent where independence is required | This directly constrains later independence findings in evidence admission. A self-issued authorization may exist, but cannot supply the independent authorization that a receiving role requires. | **Mixed.** Recording `self_issued` and changing the meaning of independence for existing authorizations requires **migration or derived-result backfill**. Improving detection while retaining the same stored identifiers is **validation-code only** prospectively; prior independence findings need re-evaluation. |
| Exact identifier equality is the plan’s only party-sameness test, with broader sameness explicitly not detected | Later lineage and independence work will miss collisions represented by different identifiers unless identity-equivalence work is added. This bounds the evidentiary meaning of the plan’s self-adjudication and self-issued results. | **Primarily validation/identity-resolution code**, if original identifiers remain intact. But any historical “independent” result or permitted one-hop result based on exact equality would require **re-evaluation and likely migration of derived findings** if broader equivalence is later adopted. |
| One-hop self-adjudication check, explicitly marked `check_depth` as direct-only | It supplies only the direct producer/executor collision check. It does not establish multi-hop lineage independence, which the plan defers to Slice D. Consumers of later admission records must not interpret a permitted result as a general independence finding. | **Mixed.** Extending traversal is initially **validation-code only** if complete lineage edges already exist. However, old direct-only outcomes and any downstream admission findings relying on them require **re-evaluation or migration of derived records**. Missing ancestry links cannot be repaired by code alone. |
| Composite-executor disclosure through `spawned` invocation links | Future lineage must represent material model, tool, and human subexecutions rather than allowing authority or influence to disappear inside a tool or composite executor. This is foundational for later multi-hop lineage analysis. | **Expensive existing-record migration, and potentially irrecoverable historical gaps.** New validation can reject undisclosed composition going forward, but it cannot reconstruct unrecorded subordinate executions in existing lineage. |
| Tool-configuration disclosure through `EffectiveInputManifest`, including content-addressed configuration, environment, and local dependencies | Future evidence admission and deterministic-standing assessments depend on knowing the effective inputs to a governed-evidence-producing tool. | **Expensive migration/backfill; potentially impossible.** A validator can enforce manifests for new records, but historical configuration, environment, or dependency state may not be recoverable. |
| External-interaction disclosure and `OutboundInteractionLog` | Later lineage and evidence admission must account for material external interactions and ambient consumers, not merely returned output bytes. This affects whether an invocation can be considered deterministic and whether undeclared `external_actuator` authority existed. | **Expensive migration/backfill; potentially impossible.** Enforcement can be added in validation or capture code for future invocations, but absent historical interaction logs generally cannot be recreated reliably. |
| Invocation executor kinds remain distinct, while the `ExecutorIdentity` superclass question is open | Later lineage constraints may need polymorphic rules across models, tools, and humans. The open superclass question affects how uniformly constraints such as identity and executor checks can be expressed. | **Potentially expensive schema migration** if records are first stored under one identity model and later require a superclass or subtype-specific equivalence semantics. Implementing polymorphic validation without changing stored identity shapes could be **validation-code only**, but that depends on identity fields and relations not supplied here. |
| Fixed Slice C predicates and the plan’s requirement that relations use `GraphRelation` and registered predicate lists | Admission and lineage records will need stable relation names and shapes for such matters as authorization, qualification, approval, production, execution, and ancestry. | **Existing-record migration** if persisted predicates or relation shapes are renamed, split, merged, or reinterpreted. Registering a new predicate without changing existing ones is generally **schema/validation-code only**. |
| Governed versus experimental classification: governed only when a valid authorization covers the invocation; pre-slice invocations remain experimental | Later admission work inherits a provenance boundary: an invocation without valid authorization is not retroactively made governed by this slice. This limits what future admission can claim about earlier records. | **Reclassification and possibly migration of stored labels/derived decisions** if the boundary changes. Altering the classifier alone is **validation-code only** only if historical classifications are retained as time-versioned results rather than overwritten. |
| Consequence classes, role ceilings, modifiers that only raise, and controlled downward adjustment | These determine which roles and authorization conditions are applicable to later evidence-producing or admitting actions. They are described as load-bearing for Slice D. | **Existing-record migration and re-evaluation** if vocabulary ordering, defaults, modifier semantics, or exception requirements change, because stored authorization and admission conclusions may change. Adding checks for unchanged rules is **validation-code only** prospectively. |
| Authorization is classification only and does not refuse execution | This means later evidence admission cannot equate execution occurrence with a successfully governed authorization check. It also preserves a population of executed but experimental invocations that Slice D may need to handle explicitly. | **Primarily validation/workflow code** to change prospectively. If records or policies have relied on the distinction between executed, governed, and experimental, changing it would require **reclassification of existing records**, but not necessarily rewriting invocation capture. |

The decisions most expensive to reverse are the ones that determine what was captured at execution time: material subordinate invocations, `spawned` lineage links, effective input manifests, and outbound interaction logs. A later validator can reject future omissions, but cannot reliably reconstruct omitted historical provenance. The next most expensive are record-family, role-vocabulary, identity, qualification-scope, and authority-chain choices, because they affect the meaning and references of authorization and future admission records.

The plan’s one-hop check is comparatively cheap to extend in code only if the required lineage has already been captured. It is not cheap to upgrade the evidentiary meaning of existing direct-only results: those results would need re-evaluation, and missing lineage would remain missing.

Several needed materials are absent if a more precise migration assessment is required:

- Section 8, to determine the full consequence-class vocabulary, modifier set, and compatibility/migration consequences.
- Section 11, to determine the required shape, retention, and linkage rules for `OutboundInteractionLog`.
- The definitions of `GraphRelation`, the Slice A/B/C predicate lists, and the `produced_by`, `executed_by`, and `spawned` record shapes, to assess whether future multi-hop traversal can be added without changing stored records.
- The applicable definitions of C3, P1, P4, and P7, to determine the precise scope of independence, authority, disclosure, and root-authority claims.
- Any retention, versioning, supersession, and migration rules for existing records, to determine whether changed validation should preserve historical outcomes under their original policy versions or rewrite/reclassify them.
- The existing warrant/admission record schemas, needed to resolve the expressly open choice between extending them and creating a new `DecisionRecord` family.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Decisions in this slice that constrain later evidence-admission / lineage work

**1. The DecisionRecord record-family shape (ABS-0004 v7 §4.13), instantiated now by InvocationAuthorization.**

Section 4.13 marks the family design as unresolved:

> `[OPEN]` Whether existing warrant/admission records are extended to fulfill this or a new record family is created, and whether kinds are subtypes or one record family.

The plan nonetheless persists `InvocationAuthorization` as a concrete `DecisionRecord` kind now (scope item: *"InvocationAuthorization as a DecisionRecord kind... alongside its kind-specific fields"*), and the plan itself notes the reconciliation gap was still open at review time:

> "COMP-0037 found the plan's field list and the ontology's inherited list unreconciled."

**Category: migration-required.** Once InvocationAuthorization records exist under one field layout, and `EvidenceAdmissionDecision` (Slice D) is later built under whichever family design the `[OPEN]` item resolves to, existing authorization records may need structural migration to conform — this is not a validator change, it is a change to persisted record shape.

**2. RoleDefinition's three axes and `required_verified_properties` (§4.9).**

> "`required_verified_properties` (the properties that must be established by admissible verification before this role's outputs enter governed evidence...)"

This field is the direct hook `EvidenceAdmissionDecision` (§4.13) uses: *"an enumeration of verified properties against the receiving role's `required_verified_properties`."* The plan seeds real role records now (drafting actuator, comparison advisor, adjudicating principal, deterministic verifier) with this field populated, and the plan's own risk section says as much:

> "Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate."

**Category: migration-required.** Seed role records are persisted artifacts (`docs/roles/`). If the vocabulary or `required_verified_properties` semantics needs revision once Slice D's admission logic is built against it, those stored role records — and anything that already cites them as authority for a governed classification — need migration, not just a validator update.

**3. AccountablePrincipal shape (§4.13), seeded now.**

The plan creates a real seed record ("the operator's AccountablePrincipal record"). `EvidenceAdmissionDecision` and future admission work will reference `AccountablePrincipal` as accountable approver. 

**Category: migration-required.** Changing `principal_id`/`principal_kind`/`authority_scope`/`delegation_reference` semantics later means migrating the persisted seed record and anything chaining to it.

**4. `self_issued` computed by exact-identifier party sameness only.**

> "Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected."

This flag is stored per authorization record at issue time, not recomputed on demand. Independence findings for evidence admission (§4.13: *"lineage and independence findings relied on"*) will eventually need a broader sameness notion for lineage work.

**Category: migration-required.** If broader-sameness detection is adopted later, previously persisted `self_issued=false` records that are actually same-party under the broader rule are now wrong and must be recomputed/migrated — this is a record-content problem, not a code-only fix, because the flag was written once and consumed downstream (independence checks) as a fact.

**5. The one-hop `check_depth` bound on the self-adjudication check.**

> "the self-adjudication outcome carries an explicit `check_depth` field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding."

**Category: validation-code-only (with a caveat).** As long as Slice D's multi-hop check is additive — new records/new `check_depth` values sitting alongside existing one-hop results — existing records remain valid instances and need no migration. This only becomes migration-required if the eventual multi-hop design requires reinterpreting or restructuring the existing `check_depth` enum rather than extending it; the evidence set doesn't show that design, so I can't rule it out.

**6. Refusal-reason enumeration and predicate registry entries.**

Both are described as enumerable/extensible ("Ten reasons, each with a fixture," "no predicate outside the registered Slice A, B, and C lists" — extended by later slices). Adding refusal reasons or Slice D predicates is additive to an enum/registry.

**Category: validation-code-only.** Nothing about existing records is invalidated by adding new reasons or predicates; only validators/consumers need updating.

**7. Consequence classification (default by target type, modifiers only raise).**

Effective consequence is computed and stored per authorization at issue time (a decision fact), not derived live.

**Category: migration-required if the default/modifier table changes**, since past records embed the old computation as a governance fact; **validation-code-only if only new modifiers are added going forward** without touching already-issued records' stored effective class.

---

## What would be needed but is not in this evidence set

- **ABS-0004 v7 Section 8** (consequence classification detail) — needed to judge how tightly the stored effective-consequence value is coupled to the classification table, i.e., whether a table change is migration-required or re-derivable.
- **ABS-0004 v7 Section 11** (OutboundInteractionLog) — referenced as the enforcement object for external-interaction disclosure; needed to judge whether Slice D lineage work depends on that log's shape and whether it's already schema-frozen.
- **The full text of the `[OPEN]` DecisionRecord resolution**, and **COMP-0037's record itself** — the plan quotes findings from COMP-0037 but the review artifact isn't in evidence; I'd want it to confirm exactly what field reconciliation was left unresolved before implementation, since that bears directly on migration cost for InvocationAuthorization records.
- **Any schema-versioning/migration policy document for AI-Lab's self_model records** — none is in evidence. Without it I can't confirm whether "migration" here means a one-time backfill script or a harder irreversible-record problem; I've assumed the latter is the relevant risk given the plan's own framing of role/consequence vocabulary as "load-bearing."

---

## On the disclosure

The plan frames the v6→v7 break narrowly, as a self-authorization/chain-termination problem solved by declaring root authority extra-systemic. I'm not treating that as the only break relevant to this slice's lineage exposure: Section 4.7 records a second, separate open construction — the `ExecutorIdentity` superclass question reopened by COMP-0032 ("a superclass with identity-equivalence semantics defined per subtype would make constraints such as C3 properly polymorphic across executor kinds") — which is unresolved and bears directly on lineage/independence comparison across `ModelIdentity`/`ToolIdentity`/`HumanIdentity`. Whether resolving it later is validation-code-only or migration-required depends on whether identity-equivalence semantics can be added as a code-level interface over existing subtype records or requires new persisted fields on them; that determination isn't answerable from the evidence here and is a second, independent risk from the one the plan foregrounds.
```
