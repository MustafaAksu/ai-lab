# COMP-0105: Provider Comparison — Claim linking LK-EX-Q7-gpt-5-6-terra-by-claude-sonnet-5

## Metadata

- comparison_id: `COMP-0105`
- title: `Claim linking LK-EX-Q7-gpt-5-6-terra-by-claude-sonnet-5`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-9f90c30de25ab7b1.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0105", "target_id": "INV-9f90c30de25ab7b1"}, {"authoritative": false, "evidence": "docs/invocations/INV-f73d0bdf835614a2.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0105", "target_id": "INV-f73d0bdf835614a2"}]`
- created_at: `2026-07-29T06:38:44.345916+00:00`
- command: `scripts/compare_providers.py --title Claim linking LK-EX-Q7-gpt-5-6-terra-by-claude-sonnet-5 You are linking extracted claims to the specific block of source text each claim is about. This is a matching task. Do not evaluate whether any claim is correct.

Below are numbered claims, then a closed list of candidate blocks with their identifiers.

For each claim, give the identifier of the ONE block the claim is about - the specific passage it asserts something concerning.

Rules:

1. Copy the block identifier exactly as written. Do not abbreviate or reformat it.
2. If the claim concerns several blocks, choose the one it is most directly about.
3. If the claim is about something NOT in the candidate list, answer null. This is expected and wanted. Do NOT choose the closest available block. A claim linked to the wrong block is worse than a claim left unlinked, because a wrong link reads as structure and will be trusted. Claims about a missing section, about the answer's own reasoning, or about material outside the list should all be null.
4. When you answer null, give a short reason: what the claim is actually about.
5. Answer for every claim number, once each.

Output STRICT JSON and nothing else. No preamble, no commentary, no markdown fences:

{"links":[{"claim":1,"block":"<identifier or null>","reason_if_null":"..."}]}

=== CLAIMS ===

1. claim: The success criteria are not uniformly mechanically checkable as written; some specify fixture-level assertions that can be automated while others depend on undefined terms, missing procedures, or open ontology material.
   quote: "The criteria are not uniformly mechanically checkable as written. Several specify fixture-level assertions that can be automated; others depend on undefined terms, missing procedures, or ontology material explicitly left open."
   extractor called it about: overall mechanical checkability of the ten success criteria

2. claim: Criterion 1 (governed vs experimental classification) is checkable at the stated fixture level, though the meaning of 'valid authorization' depends on the authorization validator and authorize() rules.
   quote: "It supplies an operational outcome rule—“governed when a valid authorization covers it and experimental otherwise”—and requires fixtures for both outcomes."
   extractor called it about: Criterion 1 governed/experimental classification

3. claim: Criterion 2 (ten refusal reasons, no unauthorised-permitted path) is mostly checkable via fixtures, but it is not a proof that all possible implementation paths behave so, since no path model or exhaustive-input domain is specified.
   quote: "It is not a proof that *all possible* implementation paths behave so, because neither a path model nor exhaustive-input domain is specified."
   extractor called it about: Criterion 2 refusal reasons and unauthorised-permitted path

4. claim: Criterion 3 (unterminated chain / out-of-scope standing authority) is only partly checkable because authority_scope has no supplied grammar or matching semantics, so a machine cannot generally determine that an authorization is outside a declared scope.
   quote: "Without those, a machine cannot generally determine that a particular authorization is “outside” a declared scope; it can only test implementation-selected examples."
   extractor called it about: Criterion 3 authority_scope check

5. claim: Criterion 4's requirement of demonstration against a 'real captured InvocationRecord' is not checkable because no InvocationRecord is named, no capture record is supplied, and no acceptance rule distinguishes 'real captured' from a constructed fixture.
   quote: "The required demonstration “against a real captured InvocationRecord” is not: no InvocationRecord is named, no capture record is supplied, and no acceptance rule distinguishes “real captured” from a constructed fixture."
   extractor called it about: Criterion 4 real captured InvocationRecord requirement

6. claim: Testing criterion 4 fully would require the identified InvocationRecord and a rule or provenance criterion establishing that it is a captured record.
   quote: "The evidence set would need the identified InvocationRecord and a rule or provenance criterion establishing that it is a captured record."
   extractor called it about: Criterion 4 real captured InvocationRecord requirement

7. claim: Criterion 5 (consequence classification) is not fully mechanically checkable against Section 8 because Section 8 labels the 'Detailed classification function' as [OPEN], leaving no definition of how modifiers acquire applicable_modifier_levels or how applicability is determined.
   quote: "Section 8 labels the “Detailed classification function” `[OPEN]`."
   extractor called it about: Criterion 5 consequence classification vs Section 8

8. claim: Criterion 5 fixtures can only test an implementation's chosen fixture mapping, not conformity to a complete Section 8 classification function.
   quote: "Thus this can test an implementation’s chosen fixture mapping, not conformity to a complete Section 8 classification function."
   extractor called it about: Criterion 5 consequence classification testability

9. claim: Criterion 6 (qualification scope) is only partly checkable because matching semantics for 'permitted ExecutionProfile constraints' and what makes a profile 'materially different' are not defined.
   quote: "General enforcement is underspecified because the supplied material does not define matching semantics for “permitted ExecutionProfile constraints” or what makes a profile “materially different.”"
   extractor called it about: Criterion 6 qualification scope

10. claim: Criterion 7 (self-issued marking and independence) is only partly checkable; the 'reported as not independent by any check that asks for independent authorization' clause has no supplied interface, set of checks, or complete semantics of independence, so it is not mechanically bounded as written.
   quote: "It is therefore not mechanically bounded as written."
   extractor called it about: Criterion 7 self-issued marking and independence

11. claim: Criterion 8 (Slice A/B regression) is checkable at the stated fixture level via byte comparison, but does not establish the broader constraint that no field, path, or default of either slice is altered for all inputs.
   quote: "It does not establish the broader constraint that “no field, path, or default of either is altered” for all inputs, but the success criterion itself is mechanically executable."
   extractor called it about: Criterion 8 Slice A/B regression

12. claim: Criterion 9 (test coverage and offline suite) is not fully mechanically checkable as written because 'every public entrypoint' lacks a definition of public API, 'covered by tests' lacks a coverage rule, and the offline suite clause names no test command, runner, dependency-installation conditions, or offline enforcement method.
   quote: "However, “every public entrypoint” lacks a definition of public API, and “covered by tests” lacks a coverage rule."
   extractor called it about: Criterion 9 test coverage and offline suite

13. claim: Criterion 10's audit clause cannot be evaluated because it gives no audit procedure, command, report schema, or semantics for verified_current.
   quote: "The audit clause gives no audit procedure, command, report schema, or semantics for `ok true verified_current`."
   extractor called it about: Criterion 10 audit clause / verified_current

14. claim: Criterion 10's cross-environment reproduction clause names no environments, build inputs, dependency-resolution rules, file-selection rule, checksum algorithm, or normalization rules, making 'byte-identical checksums' incomplete.
   quote: "The reproduction clause names no environments, build inputs, dependency-resolution rules, file-selection rule, checksum algorithm, or normalization rules."
   extractor called it about: Criterion 10 cross-environment reproduction clause

15. claim: To make criterion 5 mechanically checkable, a completed Section 8 classification function would be needed defining modifier levels, applicability conditions, evidence representation/validation rules, ordering/max behavior, and machine-validatable form of the governed downward exception.
   quote: "the level assigned by each modifier;"
   extractor called it about: Criterion 5 / Section 8 classification function

16. claim: The admission-warrant scope and expansion constraint has no success criterion checking an admission warrant or comparing implementation scope against it.
   quote: "The constraint that implementation is authorized only within a future admission warrant, and that expansion needs a separate plan, has no success criterion that checks an admission warrant or compares implementation scope against it."
   extractor called it about: Admission-warrant scope and expansion constraint

17. claim: No criterion performs a general conformance comparison against ABS-0004 v7's exact field names and semantics, and the omission of referenced Sections 4.9 and 4.13 plus Section 8's open status means a complete conformance check could not be constructed from the evidence set.
   quote: "Moreover, the supplied evidence omits the referenced Sections 4.9 and 4.13 and leaves Section 8’s detailed function open, so a complete conformance check could not be constructed from this evidence set."
   extractor called it about: ABS-0004 v7 field-and-semantics conformance constraint

18. claim: No criterion checks that all relations use GraphRelation or that no predicate falls outside the registered Slice A/B/C lists, and the GraphRelation shape and predicate lists are not supplied.
   quote: "No criterion checks that all relations use `GraphRelation` or that no predicate falls outside the registered lists."
   extractor called it about: GraphRelation and registered Slice A/B/C predicate restriction constraint

19. claim: No criterion directly checks the purity of authorize() (no I/O, no clock, no network, caller-supplied timestamp), and criterion 9's offline-suite condition does not establish purity.
   quote: "No criterion directly checks that `authorize()` has “no I/O, no clock, no network,” or that its timestamp is supplied by the caller."
   extractor called it about: Purity constraint on authorize()

20. claim: No success criterion executes an invocation flow to verify that classification or authorization refusal does not block execution, despite the plan stating no provider-call behavior change and no execution refusal.
   quote: "No success criterion executes an invocation flow and verifies that classification or authorization refusal does not block execution."
   extractor called it about: No provider-call behavior change / no execution refusal constraint

21. claim: Because both the amendment and plan remain proposed and not admitted, none of the discussed criteria or constraints presently has governance force.
   quote: "Because both the amendment and plan remain proposed and not admitted, none of these criteria or constraints presently has governance force."
   extractor called it about: governance force of the plan's criteria and constraints

=== CANDIDATE BLOCKS ===

--- ABS-0004:v7:S8#def:ordinal-classes-low-medium-high-no ---
Ordinal classes (low | medium | high), not numbers.
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

--- ABS-0004:v7:S4.6-4.7#def:a-reified-policy-conclusion-that-q ---
A reified policy conclusion that qualifies an executor for a
RoleDefinition only within an explicit execution scope: service endpoint,
permitted ExecutionProfile constraints, session-state constraints, and
policy version. A qualification never transfers implicitly to another
endpoint or a materially different execution profile. Predicates:
`qualifies_executor`, `qualifies_for`, `issued_under`, `based_on`.

--- ABS-0004:v7:S4.6-4.7#adopted_constraint:provider-claims-alone-never-qualif ---
Provider claims alone never qualify an executor for
adjudication authority.

### 4.7 Executor identities

--- ABS-0004:v7:S4.6-4.7#def:an-invocation-is-an-event-performe ---
An Invocation is an event performed by an executor: `ModelIdentity`,
`ToolIdentity`, or `HumanIdentity`, each with distinct verification
requirements. `[OPEN]` Whether an `ExecutorIdentity` superclass is needed.
A proposal to close this by fiat was rejected as conflating identity with
runtime instance; COMP-0032 reopened the question with a stronger argument:
a superclass with identity-equivalence semantics defined per subtype would
make constraints such as C3 properly polymorphic across executor kinds.
The question stands, now with that argument on record.

--- ABS-0004:v7:S4.6-4.7#adopted_constraint:composite-executor-disclosure-an-i ---
Composite-executor disclosure: an invocation may not
acquire authority by encapsulating an undisclosed subordinate executor.
Every epistemically or operationally material subordinate execution (model,
tool, or human) capable of influencing the output or external effect must be
represented as an Invocation linked to its parent (`spawned`). A
tool that invokes a model cannot be represented as a purely deterministic
ToolIdentity. Nondeterminism itself is not prohibited; undeclared authority
and hidden composition are.

--- ABS-0004:v7:S4.6-4.7#adopted_constraint:tool-configuration-disclosure-for ---
Tool-configuration disclosure: for a ToolIdentity
whose output enters governed evidence, the tool's effective inputs include
every configuration file, environment variable, and local dependency capable
of altering its execution path; these must be declared and content-addressed
in its EffectiveInputManifest. Undeclared configuration access capable of
altering the execution path defeats the tool's deterministic standing
(session-state mode `unknown_state`). This constraint is scoped to
governed-evidence production, not to every utility execution.

--- ABS-0004:v7:S4.6-4.7#adopted_constraint:external-interaction-disclosure-an ---
External-interaction disclosure: an invocation's
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

--- PLAN-20260723-0002#constraints[0] ---
Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan.

--- PLAN-20260723-0002#constraints[1] ---
Field names and semantics follow ABS-0004 v7 exactly; deviations require an ABS revision first.

--- PLAN-20260723-0002#constraints[2] ---
All relations use the GraphRelation shape; no predicate outside the registered Slice A, B, and C lists.

--- PLAN-20260723-0002#constraints[3] ---
authorize() is pure over stored records: no I/O, no clock, no network; the decision timestamp is supplied by the caller.

--- PLAN-20260723-0002#constraints[4] ---
Slice A capture and Slice B resolution behavior are unchanged: no field, path, or default of either is altered.

--- PLAN-20260723-0002#constraints[5] ---
Standing authority may not be asserted implicitly. A principal record must declare its authority_scope, and an authorization outside that scope is refused rather than downgraded.

--- PLAN-20260723-0002#created_at ---
2026-07-23T00:00:00+00:00

--- PLAN-20260723-0002#depends_on_capability_ids[0] ---
CAP-0015

--- PLAN-20260723-0002#depends_on_capability_ids[1] ---
CAP-0016

--- PLAN-20260723-0002#evidence_ids[0] ---
docs/self_model/gaps/GAP-0005.json

--- PLAN-20260723-0002#evidence_ids[1] ---
docs/abstractions/ABS-0004-invocation-authorization-ontology.md

--- PLAN-20260723-0002#evidence_ids[2] ---
docs/self_model/decisions/DECISION-20260723-0001.json

--- PLAN-20260723-0002#evidence_ids[3] ---
docs/self_model/verifications/VERIFY-20260723-0002.json

--- PLAN-20260723-0002#evidence_ids[4] ---
docs/self_model/capabilities/CAP-0015.json

--- PLAN-20260723-0002#evidence_ids[5] ---
docs/self_model/capabilities/CAP-0016.json

--- PLAN-20260723-0002#expected_outputs[0] ---
ai_lab/governance/roles.py (role, qualification, and principal schemas with validators).

--- PLAN-20260723-0002#expected_outputs[1] ---
ai_lab/governance/authorization.py (authorization records, pure authorize(), consequence classification, governed/experimental classifier, one-hop self-adjudication check).

--- PLAN-20260723-0002#expected_outputs[2] ---
docs/self_model/PREDICATE_REGISTRY.md extended with the Slice C predicates.

--- PLAN-20260723-0002#expected_outputs[3] ---
docs/self_model/AUTHORIZATION_RECORDS.md documenting the record family, the standing-authority termination rule, and stated limitations including the one-hop bound.

--- PLAN-20260723-0002#expected_outputs[4] ---
tests/test_roles.py and tests/test_authorization.py with schema, rejection, refusal-reason, and integration fixtures.

--- PLAN-20260723-0002#expected_outputs[5] ---
Seed records: the operator's AccountablePrincipal record and the role definitions AI-Lab already uses in practice (drafting actuator, comparison advisor, adjudicating principal, deterministic verifier).

--- PLAN-20260723-0002#mitigation ---
Both limits are stated in the documentation and in the capability record rather than left to inference: governed means an authorization covers the invocation, and the self-adjudication check is one hop. Refusal reasons are enumerated so that a permitted outcome is never a silent default. The role vocabulary is copied from ABS-0004 v7 verbatim rather than invented, and the seed roles describe practice already visible in the record. The ten refusal reasons replace the original six after COMP-0037 found four missing. Success criteria are restated to claim only enumerated-fixture coverage rather than universal properties, per the same round's finding that 'never fails silently' and 'is monotonic' are not mechanically checkable as written. Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected.

--- PLAN-20260723-0002#next_action ---
Re-run the admission comparison round with the revised plan and the ABS-0004 v7 amendment attached as text; on operator adjudication, admit v7 and issue the plan's admission warrant.

--- PLAN-20260723-0002#non_goals[0] ---
Refusing or blocking any execution. Authorization classifies; it does not gate. Execution refusal requires a separately admitted plan.

--- PLAN-20260723-0002#non_goals[1] ---
Routing, escalation, or model selection (RoutingDecision remains deferred).

--- PLAN-20260723-0002#non_goals[2] ---
Multi-hop lineage traversal, independence assessment, or evidence admission (Slice D).

--- PLAN-20260723-0002#non_goals[3] ---
Retroactive authorization of invocations captured before this slice; they remain experimental, and the pre-provenance boundary applies.

--- PLAN-20260723-0002#non_goals[4] ---
Any claim that the one-hop check implements C3. It implements C3's most direct case only, and the documentation must say so.

--- PLAN-20260723-0002#non_goals[5] ---
Automatic consequence assignment from artifact content; consequence is declared per authorization with the default derived from target type.

--- PLAN-20260723-0002#non_goals[6] ---
Cryptographic attestation of principals; ABS-0004 records it as a later implementation mechanism, not an ontology requirement.

--- PLAN-20260723-0002#non_goals[7] ---
Any claim that AI-Lab validates a standing-authority declaration. Per ABS-0004 v7 P7, root authority is extra-systemic: the system records the claim and cannot verify it, and no record, scope grammar, or internal approval step may be presented as verification.

--- PLAN-20260723-0002#non_goals[8] ---
Refusing a self-issued authorization. Self-issue is marked and disqualified from independence, not blocked: at the root of any chain the accountable party necessarily authorizes work it is responsible for.

--- PLAN-20260723-0002#objective ---
Make the authority separation AI-Lab has practised in conversation structural: who may perform what, under which role, at what consequence, on whose standing authority, recorded as evidence rather than as testimony. The immediate motivation is concrete: on 2026-07-23 a model-default change would have set the reviewer slot to the drafting executor's own identity, collapsing reviewer and author under C3. Nothing in the system would have noticed; it was caught because a human happened to be told. Slice C makes the most direct case of that collision detectable by machine.

--- PLAN-20260723-0002#plan_id ---
PLAN-20260723-0002

--- PLAN-20260723-0002#proposed_change ---
After a separate admission checkpoint, and after ABS-0004 v7 is admitted: add ai_lab/governance/roles.py (RoleDefinition, RoleQualification, AccountablePrincipal schemas and validators), ai_lab/governance/authorization.py (InvocationAuthorization records, the pure authorize() function, consequence classification, the experimental-versus-governed classifier, and the one-hop self-adjudication check), predicate-registry entries, documentation, and tests. No change to provider-call behavior, no change to Slice A capture or Slice B resolution, and no refusal of any execution.

--- PLAN-20260723-0002#rationale[0] ---
ABS-0004's enforcement matrix records C6 authority separation as 'adopted, not currently evidenced': no artifact names the check. Slice C is what lets that row cite something.

--- PLAN-20260723-0002#rationale[1] ---
The near-miss of 2026-07-23 is the exhibit: identity collision between reviewer and author was invisible to every test, and was avoided by chance rather than by control.

--- PLAN-20260723-0002#rationale[2] ---
Slice A supplies produced_by and executed_by, so a one-hop identity collision is detectable now without the ancestry traversal that belongs to Slice D. The cheap case is available; the expensive case stays deferred.

--- PLAN-20260723-0002#rationale[3] ---
ABS-0004 v7 fixes where authorization chains terminate - at an AccountablePrincipal's recorded standing-authority claim within a declared scope - and states plainly that this does not close the bootstrap regress. The open question remains open: v7 records that no internal control can close it and that the constraint supplies visibility, not prevention. What is settled before any code depends on it is the termination rule and an honest account of its limits, not a resolution of the regress.

--- PLAN-20260723-0002#rationale[4] ---
COMP-0037 split: one reviewer recommended revise-first, the other admit-with-conditions, and both independently constructed the same self-authorization path through v6's chain termination. The revision follows the stronger recommendation. v7 does not answer the break with a tighter internal control, because no internal control can answer it; it records that root authority is extra-systemic and makes the coincidence of issuer and executor visible instead.

--- PLAN-20260723-0002#repo_commit ---
96209e95a722c5e1f6d18061e746ff75b33b3fca

--- PLAN-20260723-0002#risk ---
An authorization system that classifies but never refuses can create a false sense of control: readers may assume governed means checked when it means covered by a record. The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision. Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate. Beyond those: v7 makes the honest limitation explicit rather than closing it, so a reader who wants an assurance AI-Lab cannot give will find the system declining to give it, which is correct and may be mistaken for a defect. The self_issued marking depends on identifying when two records name the same party, which is straightforward for exact identifiers and undecidable in general; the implementation must not claim to detect sameness it cannot establish.

--- PLAN-20260723-0002#schema_version ---
v1

--- PLAN-20260723-0002#scope[0] ---
A roles module defining schema v1 for RoleDefinition (task_function, epistemic_authority, action_authority, and the constraint fields ABS-0004 4.9 enumerates), with a validator, canonical serialization, and deterministic identity and path rules under docs/roles/.

--- PLAN-20260723-0002#scope[1] ---
RoleQualification records, execution-scoped as ABS-0004 4.6 requires: qualified executor, role, service endpoint scope, permitted ExecutionProfile constraints, session-state constraints, policy version, and the evaluation evidence relied on. A qualification never transfers implicitly to another endpoint or a materially different profile, and the validator rejects a qualification lacking an execution scope.

--- PLAN-20260723-0002#scope[2] ---
AccountablePrincipal records with principal_id, principal_kind, authority_scope, and delegation_reference, carrying no personal identifying data.

--- PLAN-20260723-0002#scope[3] ---
InvocationAuthorization as a DecisionRecord kind: invocation request, authorized executor, assigned role, consequence class, applicable policy, qualifications relied on, independence requirements, conditions, issuing principal, and the standing-authority or chained-authorization reference that terminates its chain.

--- PLAN-20260723-0002#scope[4] ---
A pure authorize() function over stored records returning an authorization outcome or one of the enumerated refusal reasons: no qualification for this executor and role; qualification out of execution scope; consequence above the role ceiling; unterminated authorization chain; standing authority claimed outside its declared scope; authorization conditions unmet, malformed, or absent; authorized executor does not match the executor performing the invocation; the authorization or a record it relies on is inactive or superseded; subordinate execution outside the classes its parent authorization declares; and self-adjudication conflict. Ten reasons, each with a fixture. COMP-0037 found the sixth, seventh, eighth, and ninth of these missing from the six originally proposed.

--- PLAN-20260723-0002#scope[5] ---
The one-hop self-adjudication check: for an adjudicator-authority role over a target artifact, if the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization, refuse. Scoped explicitly to one hop; multi-hop ancestry is Slice D.

--- PLAN-20260723-0002#scope[6] ---
Consequence classification per ABS-0004 Section 8: default by target type, effective consequence as the maximum of the default and applicable modifier levels, modifiers only raising, and downward adjustment only as a governed exception carrying reason, principal, scope, evidence, and review condition.

--- PLAN-20260723-0002#scope[7] ---
The experimental-versus-governed boundary: a classify function marking an invocation governed only when a valid authorization covers it, experimental otherwise. Classification only; no invocation is refused execution by this slice.

--- PLAN-20260723-0002#scope[8] ---
Predicate-registry entries for the Slice C predicates: assigned_role, authorized_by, authorizes, qualifies_executor, qualifies_for, issued_under, based_on, approved_by.

--- PLAN-20260723-0002#scope[9] ---
Validator fixtures covering valid records, each rejection class, and each refusal reason, plus an integration fixture authorizing an invocation against stored role, qualification, and principal records offline.

--- PLAN-20260723-0002#scope[10] ---
Field reconciliation with ABS-0004 4.13: InvocationAuthorization carries the inherited DecisionRecord fields (target, recommended_status and effective_status, issuer invocation, accountable approver, evidence, policy authority, activation state, supersession) alongside its kind-specific fields, and the documentation states how issuing principal, issuer invocation, and accountable approver relate. COMP-0037 found the plan's field list and the ontology's inherited list unreconciled.

--- PLAN-20260723-0002#scope[11] ---
Self-issued marking per ABS-0004 v7: where the issuing principal and the authorized executor are the same party, the authorization records self_issued true. Self-issued authorizations are permitted and are disqualified from counting as independent authorization wherever independence is required.

--- PLAN-20260723-0002#scope[12] ---
The one-hop bound is machine-visible, not only documented: the self-adjudication outcome carries an explicit check_depth field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding.

--- PLAN-20260723-0002#source_capability_ids[0] ---
CAP-0015

--- PLAN-20260723-0002#source_capability_ids[1] ---
CAP-0016

--- PLAN-20260723-0002#source_gap_id ---
GAP-0005

--- PLAN-20260723-0002#status ---
proposed

--- PLAN-20260723-0002#success_criteria[0] ---
A stored invocation is classified governed when a valid authorization covers it and experimental otherwise, demonstrated by fixtures for both outcomes.

--- PLAN-20260723-0002#success_criteria[1] ---
Each of the ten enumerated refusal reasons is exercised by a fixture and yields that reason; no fixture path returns a permitted outcome without a matching authorization record.

--- PLAN-20260723-0002#success_criteria[2] ---
An authorization whose chain terminates nowhere is refused, and an authorization issued outside a principal's declared authority_scope is refused, each with its own reason.

--- PLAN-20260723-0002#success_criteria[3] ---
The one-hop self-adjudication check refuses an adjudicator authorization over an artifact produced by the same executor identity, demonstrated against a real captured InvocationRecord, permits it when the identities differ, and carries a check_depth field marking the result as direct-only in both cases.

--- PLAN-20260723-0002#success_criteria[4] ---
Consequence classification is exercised over the enumerated modifier set: for each modifier, a fixture asserts the effective class equals the maximum of the default and the modifier level, and a downward adjustment without a recorded governed exception is refused. This is enumerated-fixture coverage of the named cases, not a proof of monotonicity over all inputs.

--- PLAN-20260723-0002#success_criteria[5] ---
A qualification lacking an execution scope is rejected, and a qualification is not honoured for an endpoint or execution profile outside its scope.

--- PLAN-20260723-0002#success_criteria[6] ---
A self-issued authorization is accepted, carries self_issued true, and is reported as not independent by any check that asks for independent authorization.

--- PLAN-20260723-0002#success_criteria[7] ---
Regression: Slice A capture and Slice B resolution are unchanged, demonstrated by a fixture that runs both against stored records before and after authorization code is importable and asserts byte-identical outputs. COMP-0037 found this constraint had no corresponding check.

--- PLAN-20260723-0002#success_criteria[8] ---
The new modules are covered by tests exercising every public entrypoint and every enumerated outcome; the full suite passes offline with no network access.

--- PLAN-20260723-0002#success_criteria[9] ---
The repository audit reports ok true verified_current, and commit-level cross-environment reproduction from the public repository yields byte-identical checksums for every delivered file.

--- PLAN-20260723-0002#summary ---
Implement ABS-0004 v7 Slice C: RoleDefinition records on the three admitted axes, execution-scoped RoleQualification, InvocationAuthorization as a DecisionRecord kind, consequence classification, and the experimental-versus-governed boundary. An authorization is issued by an AccountablePrincipal holding standing authority within a declared scope, or chains to one; an authorization that chains to nothing is unauthorized rather than permitted. Authorization has one consequence in this slice and no others: an invocation is classified governed only when an authorization covers it, and experimental otherwise. Nothing is refused execution. The authorization function additionally performs a one-hop self-adjudication check using Slice A provenance: if the artifact under adjudication carries an InvocationRecord whose executor identity equals the executor being authorized, authorization is refused with an enumerated reason.

--- PLAN-20260723-0002#title ---
Roles, qualification, and invocation authorization (ABS-0004 Slice C)

--- END OF CANDIDATES ---

Output the JSON now.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are linking extracted claims to the specific block of source text each claim is about. This is a matching task. Do not evaluate whether any claim is correct.

Below are numbered claims, then a closed list of candidate blocks with their identifiers.

For each claim, give the identifier of the ONE block the claim is about - the specific passage it asserts something concerning.

Rules:

1. Copy the block identifier exactly as written. Do not abbreviate or reformat it.
2. If the claim concerns several blocks, choose the one it is most directly about.
3. If the claim is about something NOT in the candidate list, answer null. This is expected and wanted. Do NOT choose the closest available block. A claim linked to the wrong block is worse than a claim left unlinked, because a wrong link reads as structure and will be trusted. Claims about a missing section, about the answer's own reasoning, or about material outside the list should all be null.
4. When you answer null, give a short reason: what the claim is actually about.
5. Answer for every claim number, once each.

Output STRICT JSON and nothing else. No preamble, no commentary, no markdown fences:

{"links":[{"claim":1,"block":"<identifier or null>","reason_if_null":"..."}]}

=== CLAIMS ===

1. claim: The success criteria are not uniformly mechanically checkable as written; some specify fixture-level assertions that can be automated while others depend on undefined terms, missing procedures, or open ontology material.
   quote: "The criteria are not uniformly mechanically checkable as written. Several specify fixture-level assertions that can be automated; others depend on undefined terms, missing procedures, or ontology material explicitly left open."
   extractor called it about: overall mechanical checkability of the ten success criteria

2. claim: Criterion 1 (governed vs experimental classification) is checkable at the stated fixture level, though the meaning of 'valid authorization' depends on the authorization validator and authorize() rules.
   quote: "It supplies an operational outcome rule—“governed when a valid authorization covers it and experimental otherwise”—and requires fixtures for both outcomes."
   extractor called it about: Criterion 1 governed/experimental classification

3. claim: Criterion 2 (ten refusal reasons, no unauthorised-permitted path) is mostly checkable via fixtures, but it is not a proof that all possible implementation paths behave so, since no path model or exhaustive-input domain is specified.
   quote: "It is not a proof that *all possible* implementation paths behave so, because neither a path model nor exhaustive-input domain is specified."
   extractor called it about: Criterion 2 refusal reasons and unauthorised-permitted path

4. claim: Criterion 3 (unterminated chain / out-of-scope standing authority) is only partly checkable because authority_scope has no supplied grammar or matching semantics, so a machine cannot generally determine that an authorization is outside a declared scope.
   quote: "Without those, a machine cannot generally determine that a particular authorization is “outside” a declared scope; it can only test implementation-selected examples."
   extractor called it about: Criterion 3 authority_scope check

5. claim: Criterion 4's requirement of demonstration against a 'real captured InvocationRecord' is not checkable because no InvocationRecord is named, no capture record is supplied, and no acceptance rule distinguishes 'real captured' from a constructed fixture.
   quote: "The required demonstration “against a real captured InvocationRecord” is not: no InvocationRecord is named, no capture record is supplied, and no acceptance rule distinguishes “real captured” from a constructed fixture."
   extractor called it about: Criterion 4 real captured InvocationRecord requirement

6. claim: Testing criterion 4 fully would require the identified InvocationRecord and a rule or provenance criterion establishing that it is a captured record.
   quote: "The evidence set would need the identified InvocationRecord and a rule or provenance criterion establishing that it is a captured record."
   extractor called it about: Criterion 4 real captured InvocationRecord requirement

7. claim: Criterion 5 (consequence classification) is not fully mechanically checkable against Section 8 because Section 8 labels the 'Detailed classification function' as [OPEN], leaving no definition of how modifiers acquire applicable_modifier_levels or how applicability is determined.
   quote: "Section 8 labels the “Detailed classification function” `[OPEN]`."
   extractor called it about: Criterion 5 consequence classification vs Section 8

8. claim: Criterion 5 fixtures can only test an implementation's chosen fixture mapping, not conformity to a complete Section 8 classification function.
   quote: "Thus this can test an implementation’s chosen fixture mapping, not conformity to a complete Section 8 classification function."
   extractor called it about: Criterion 5 consequence classification testability

9. claim: Criterion 6 (qualification scope) is only partly checkable because matching semantics for 'permitted ExecutionProfile constraints' and what makes a profile 'materially different' are not defined.
   quote: "General enforcement is underspecified because the supplied material does not define matching semantics for “permitted ExecutionProfile constraints” or what makes a profile “materially different.”"
   extractor called it about: Criterion 6 qualification scope

10. claim: Criterion 7 (self-issued marking and independence) is only partly checkable; the 'reported as not independent by any check that asks for independent authorization' clause has no supplied interface, set of checks, or complete semantics of independence, so it is not mechanically bounded as written.
   quote: "It is therefore not mechanically bounded as written."
   extractor called it about: Criterion 7 self-issued marking and independence

11. claim: Criterion 8 (Slice A/B regression) is checkable at the stated fixture level via byte comparison, but does not establish the broader constraint that no field, path, or default of either slice is altered for all inputs.
   quote: "It does not establish the broader constraint that “no field, path, or default of either is altered” for all inputs, but the success criterion itself is mechanically executable."
   extractor called it about: Criterion 8 Slice A/B regression

12. claim: Criterion 9 (test coverage and offline suite) is not fully mechanically checkable as written because 'every public entrypoint' lacks a definition of public API, 'covered by tests' lacks a coverage rule, and the offline suite clause names no test command, runner, dependency-installation conditions, or offline enforcement method.
   quote: "However, “every public entrypoint” lacks a definition of public API, and “covered by tests” lacks a coverage rule."
   extractor called it about: Criterion 9 test coverage and offline suite

13. claim: Criterion 10's audit clause cannot be evaluated because it gives no audit procedure, command, report schema, or semantics for verified_current.
   quote: "The audit clause gives no audit procedure, command, report schema, or semantics for `ok true verified_current`."
   extractor called it about: Criterion 10 audit clause / verified_current

14. claim: Criterion 10's cross-environment reproduction clause names no environments, build inputs, dependency-resolution rules, file-selection rule, checksum algorithm, or normalization rules, making 'byte-identical checksums' incomplete.
   quote: "The reproduction clause names no environments, build inputs, dependency-resolution rules, file-selection rule, checksum algorithm, or normalization rules."
   extractor called it about: Criterion 10 cross-environment reproduction clause

15. claim: To make criterion 5 mechanically checkable, a completed Section 8 classification function would be needed defining modifier levels, applicability conditions, evidence representation/validation rules, ordering/max behavior, and machine-validatable form of the governed downward exception.
   quote: "the level assigned by each modifier;"
   extractor called it about: Criterion 5 / Section 8 classification function

16. claim: The admission-warrant scope and expansion constraint has no success criterion checking an admission warrant or comparing implementation scope against it.
   quote: "The constraint that implementation is authorized only within a future admission warrant, and that expansion needs a separate plan, has no success criterion that checks an admission warrant or compares implementation scope against it."
   extractor called it about: Admission-warrant scope and expansion constraint

17. claim: No criterion performs a general conformance comparison against ABS-0004 v7's exact field names and semantics, and the omission of referenced Sections 4.9 and 4.13 plus Section 8's open status means a complete conformance check could not be constructed from the evidence set.
   quote: "Moreover, the supplied evidence omits the referenced Sections 4.9 and 4.13 and leaves Section 8’s detailed function open, so a complete conformance check could not be constructed from this evidence set."
   extractor called it about: ABS-0004 v7 field-and-semantics conformance constraint

18. claim: No criterion checks that all relations use GraphRelation or that no predicate falls outside the registered Slice A/B/C lists, and the GraphRelation shape and predicate lists are not supplied.
   quote: "No criterion checks that all relations use `GraphRelation` or that no predicate falls outside the registered lists."
   extractor called it about: GraphRelation and registered Slice A/B/C predicate restriction constraint

19. claim: No criterion directly checks the purity of authorize() (no I/O, no clock, no network, caller-supplied timestamp), and criterion 9's offline-suite condition does not establish purity.
   quote: "No criterion directly checks that `authorize()` has “no I/O, no clock, no network,” or that its timestamp is supplied by the caller."
   extractor called it about: Purity constraint on authorize()

20. claim: No success criterion executes an invocation flow to verify that classification or authorization refusal does not block execution, despite the plan stating no provider-call behavior change and no execution refusal.
   quote: "No success criterion executes an invocation flow and verifies that classification or authorization refusal does not block execution."
   extractor called it about: No provider-call behavior change / no execution refusal constraint

21. claim: Because both the amendment and plan remain proposed and not admitted, none of the discussed criteria or constraints presently has governance force.
   quote: "Because both the amendment and plan remain proposed and not admitted, none of these criteria or constraints presently has governance force."
   extractor called it about: governance force of the plan's criteria and constraints

=== CANDIDATE BLOCKS ===

--- ABS-0004:v7:S8#def:ordinal-classes-low-medium-high-no ---
Ordinal classes (low | medium | high), not numbers.
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

--- ABS-0004:v7:S4.6-4.7#def:a-reified-policy-conclusion-that-q ---
A reified policy conclusion that qualifies an executor for a
RoleDefinition only within an explicit execution scope: service endpoint,
permitted ExecutionProfile constraints, session-state constraints, and
policy version. A qualification never transfers implicitly to another
endpoint or a materially different execution profile. Predicates:
`qualifies_executor`, `qualifies_for`, `issued_under`, `based_on`.

--- ABS-0004:v7:S4.6-4.7#adopted_constraint:provider-claims-alone-never-qualif ---
Provider claims alone never qualify an executor for
adjudication authority.

### 4.7 Executor identities

--- ABS-0004:v7:S4.6-4.7#def:an-invocation-is-an-event-performe ---
An Invocation is an event performed by an executor: `ModelIdentity`,
`ToolIdentity`, or `HumanIdentity`, each with distinct verification
requirements. `[OPEN]` Whether an `ExecutorIdentity` superclass is needed.
A proposal to close this by fiat was rejected as conflating identity with
runtime instance; COMP-0032 reopened the question with a stronger argument:
a superclass with identity-equivalence semantics defined per subtype would
make constraints such as C3 properly polymorphic across executor kinds.
The question stands, now with that argument on record.

--- ABS-0004:v7:S4.6-4.7#adopted_constraint:composite-executor-disclosure-an-i ---
Composite-executor disclosure: an invocation may not
acquire authority by encapsulating an undisclosed subordinate executor.
Every epistemically or operationally material subordinate execution (model,
tool, or human) capable of influencing the output or external effect must be
represented as an Invocation linked to its parent (`spawned`). A
tool that invokes a model cannot be represented as a purely deterministic
ToolIdentity. Nondeterminism itself is not prohibited; undeclared authority
and hidden composition are.

--- ABS-0004:v7:S4.6-4.7#adopted_constraint:tool-configuration-disclosure-for ---
Tool-configuration disclosure: for a ToolIdentity
whose output enters governed evidence, the tool's effective inputs include
every configuration file, environment variable, and local dependency capable
of altering its execution path; these must be declared and content-addressed
in its EffectiveInputManifest. Undeclared configuration access capable of
altering the execution path defeats the tool's deterministic standing
(session-state mode `unknown_state`). This constraint is scoped to
governed-evidence production, not to every utility execution.

--- ABS-0004:v7:S4.6-4.7#adopted_constraint:external-interaction-disclosure-an ---
External-interaction disclosure: an invocation's
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

--- PLAN-20260723-0002#constraints[0] ---
Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan.

--- PLAN-20260723-0002#constraints[1] ---
Field names and semantics follow ABS-0004 v7 exactly; deviations require an ABS revision first.

--- PLAN-20260723-0002#constraints[2] ---
All relations use the GraphRelation shape; no predicate outside the registered Slice A, B, and C lists.

--- PLAN-20260723-0002#constraints[3] ---
authorize() is pure over stored records: no I/O, no clock, no network; the decision timestamp is supplied by the caller.

--- PLAN-20260723-0002#constraints[4] ---
Slice A capture and Slice B resolution behavior are unchanged: no field, path, or default of either is altered.

--- PLAN-20260723-0002#constraints[5] ---
Standing authority may not be asserted implicitly. A principal record must declare its authority_scope, and an authorization outside that scope is refused rather than downgraded.

--- PLAN-20260723-0002#created_at ---
2026-07-23T00:00:00+00:00

--- PLAN-20260723-0002#depends_on_capability_ids[0] ---
CAP-0015

--- PLAN-20260723-0002#depends_on_capability_ids[1] ---
CAP-0016

--- PLAN-20260723-0002#evidence_ids[0] ---
docs/self_model/gaps/GAP-0005.json

--- PLAN-20260723-0002#evidence_ids[1] ---
docs/abstractions/ABS-0004-invocation-authorization-ontology.md

--- PLAN-20260723-0002#evidence_ids[2] ---
docs/self_model/decisions/DECISION-20260723-0001.json

--- PLAN-20260723-0002#evidence_ids[3] ---
docs/self_model/verifications/VERIFY-20260723-0002.json

--- PLAN-20260723-0002#evidence_ids[4] ---
docs/self_model/capabilities/CAP-0015.json

--- PLAN-20260723-0002#evidence_ids[5] ---
docs/self_model/capabilities/CAP-0016.json

--- PLAN-20260723-0002#expected_outputs[0] ---
ai_lab/governance/roles.py (role, qualification, and principal schemas with validators).

--- PLAN-20260723-0002#expected_outputs[1] ---
ai_lab/governance/authorization.py (authorization records, pure authorize(), consequence classification, governed/experimental classifier, one-hop self-adjudication check).

--- PLAN-20260723-0002#expected_outputs[2] ---
docs/self_model/PREDICATE_REGISTRY.md extended with the Slice C predicates.

--- PLAN-20260723-0002#expected_outputs[3] ---
docs/self_model/AUTHORIZATION_RECORDS.md documenting the record family, the standing-authority termination rule, and stated limitations including the one-hop bound.

--- PLAN-20260723-0002#expected_outputs[4] ---
tests/test_roles.py and tests/test_authorization.py with schema, rejection, refusal-reason, and integration fixtures.

--- PLAN-20260723-0002#expected_outputs[5] ---
Seed records: the operator's AccountablePrincipal record and the role definitions AI-Lab already uses in practice (drafting actuator, comparison advisor, adjudicating principal, deterministic verifier).

--- PLAN-20260723-0002#mitigation ---
Both limits are stated in the documentation and in the capability record rather than left to inference: governed means an authorization covers the invocation, and the self-adjudication check is one hop. Refusal reasons are enumerated so that a permitted outcome is never a silent default. The role vocabulary is copied from ABS-0004 v7 verbatim rather than invented, and the seed roles describe practice already visible in the record. The ten refusal reasons replace the original six after COMP-0037 found four missing. Success criteria are restated to claim only enumerated-fixture coverage rather than universal properties, per the same round's finding that 'never fails silently' and 'is monotonic' are not mechanically checkable as written. Party sameness is decided on exact identifier equality only, and the documentation states that broader sameness is not detected.

--- PLAN-20260723-0002#next_action ---
Re-run the admission comparison round with the revised plan and the ABS-0004 v7 amendment attached as text; on operator adjudication, admit v7 and issue the plan's admission warrant.

--- PLAN-20260723-0002#non_goals[0] ---
Refusing or blocking any execution. Authorization classifies; it does not gate. Execution refusal requires a separately admitted plan.

--- PLAN-20260723-0002#non_goals[1] ---
Routing, escalation, or model selection (RoutingDecision remains deferred).

--- PLAN-20260723-0002#non_goals[2] ---
Multi-hop lineage traversal, independence assessment, or evidence admission (Slice D).

--- PLAN-20260723-0002#non_goals[3] ---
Retroactive authorization of invocations captured before this slice; they remain experimental, and the pre-provenance boundary applies.

--- PLAN-20260723-0002#non_goals[4] ---
Any claim that the one-hop check implements C3. It implements C3's most direct case only, and the documentation must say so.

--- PLAN-20260723-0002#non_goals[5] ---
Automatic consequence assignment from artifact content; consequence is declared per authorization with the default derived from target type.

--- PLAN-20260723-0002#non_goals[6] ---
Cryptographic attestation of principals; ABS-0004 records it as a later implementation mechanism, not an ontology requirement.

--- PLAN-20260723-0002#non_goals[7] ---
Any claim that AI-Lab validates a standing-authority declaration. Per ABS-0004 v7 P7, root authority is extra-systemic: the system records the claim and cannot verify it, and no record, scope grammar, or internal approval step may be presented as verification.

--- PLAN-20260723-0002#non_goals[8] ---
Refusing a self-issued authorization. Self-issue is marked and disqualified from independence, not blocked: at the root of any chain the accountable party necessarily authorizes work it is responsible for.

--- PLAN-20260723-0002#objective ---
Make the authority separation AI-Lab has practised in conversation structural: who may perform what, under which role, at what consequence, on whose standing authority, recorded as evidence rather than as testimony. The immediate motivation is concrete: on 2026-07-23 a model-default change would have set the reviewer slot to the drafting executor's own identity, collapsing reviewer and author under C3. Nothing in the system would have noticed; it was caught because a human happened to be told. Slice C makes the most direct case of that collision detectable by machine.

--- PLAN-20260723-0002#plan_id ---
PLAN-20260723-0002

--- PLAN-20260723-0002#proposed_change ---
After a separate admission checkpoint, and after ABS-0004 v7 is admitted: add ai_lab/governance/roles.py (RoleDefinition, RoleQualification, AccountablePrincipal schemas and validators), ai_lab/governance/authorization.py (InvocationAuthorization records, the pure authorize() function, consequence classification, the experimental-versus-governed classifier, and the one-hop self-adjudication check), predicate-registry entries, documentation, and tests. No change to provider-call behavior, no change to Slice A capture or Slice B resolution, and no refusal of any execution.

--- PLAN-20260723-0002#rationale[0] ---
ABS-0004's enforcement matrix records C6 authority separation as 'adopted, not currently evidenced': no artifact names the check. Slice C is what lets that row cite something.

--- PLAN-20260723-0002#rationale[1] ---
The near-miss of 2026-07-23 is the exhibit: identity collision between reviewer and author was invisible to every test, and was avoided by chance rather than by control.

--- PLAN-20260723-0002#rationale[2] ---
Slice A supplies produced_by and executed_by, so a one-hop identity collision is detectable now without the ancestry traversal that belongs to Slice D. The cheap case is available; the expensive case stays deferred.

--- PLAN-20260723-0002#rationale[3] ---
ABS-0004 v7 fixes where authorization chains terminate - at an AccountablePrincipal's recorded standing-authority claim within a declared scope - and states plainly that this does not close the bootstrap regress. The open question remains open: v7 records that no internal control can close it and that the constraint supplies visibility, not prevention. What is settled before any code depends on it is the termination rule and an honest account of its limits, not a resolution of the regress.

--- PLAN-20260723-0002#rationale[4] ---
COMP-0037 split: one reviewer recommended revise-first, the other admit-with-conditions, and both independently constructed the same self-authorization path through v6's chain termination. The revision follows the stronger recommendation. v7 does not answer the break with a tighter internal control, because no internal control can answer it; it records that root authority is extra-systemic and makes the coincidence of issuer and executor visible instead.

--- PLAN-20260723-0002#repo_commit ---
96209e95a722c5e1f6d18061e746ff75b33b3fca

--- PLAN-20260723-0002#risk ---
An authorization system that classifies but never refuses can create a false sense of control: readers may assume governed means checked when it means covered by a record. The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision. Role and consequence vocabularies decided here are load-bearing for Slice D's admission rules, and a coarse role taxonomy would propagate. Beyond those: v7 makes the honest limitation explicit rather than closing it, so a reader who wants an assurance AI-Lab cannot give will find the system declining to give it, which is correct and may be mistaken for a defect. The self_issued marking depends on identifying when two records name the same party, which is straightforward for exact identifiers and undecidable in general; the implementation must not claim to detect sameness it cannot establish.

--- PLAN-20260723-0002#schema_version ---
v1

--- PLAN-20260723-0002#scope[0] ---
A roles module defining schema v1 for RoleDefinition (task_function, epistemic_authority, action_authority, and the constraint fields ABS-0004 4.9 enumerates), with a validator, canonical serialization, and deterministic identity and path rules under docs/roles/.

--- PLAN-20260723-0002#scope[1] ---
RoleQualification records, execution-scoped as ABS-0004 4.6 requires: qualified executor, role, service endpoint scope, permitted ExecutionProfile constraints, session-state constraints, policy version, and the evaluation evidence relied on. A qualification never transfers implicitly to another endpoint or a materially different profile, and the validator rejects a qualification lacking an execution scope.

--- PLAN-20260723-0002#scope[2] ---
AccountablePrincipal records with principal_id, principal_kind, authority_scope, and delegation_reference, carrying no personal identifying data.

--- PLAN-20260723-0002#scope[3] ---
InvocationAuthorization as a DecisionRecord kind: invocation request, authorized executor, assigned role, consequence class, applicable policy, qualifications relied on, independence requirements, conditions, issuing principal, and the standing-authority or chained-authorization reference that terminates its chain.

--- PLAN-20260723-0002#scope[4] ---
A pure authorize() function over stored records returning an authorization outcome or one of the enumerated refusal reasons: no qualification for this executor and role; qualification out of execution scope; consequence above the role ceiling; unterminated authorization chain; standing authority claimed outside its declared scope; authorization conditions unmet, malformed, or absent; authorized executor does not match the executor performing the invocation; the authorization or a record it relies on is inactive or superseded; subordinate execution outside the classes its parent authorization declares; and self-adjudication conflict. Ten reasons, each with a fixture. COMP-0037 found the sixth, seventh, eighth, and ninth of these missing from the six originally proposed.

--- PLAN-20260723-0002#scope[5] ---
The one-hop self-adjudication check: for an adjudicator-authority role over a target artifact, if the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization, refuse. Scoped explicitly to one hop; multi-hop ancestry is Slice D.

--- PLAN-20260723-0002#scope[6] ---
Consequence classification per ABS-0004 Section 8: default by target type, effective consequence as the maximum of the default and applicable modifier levels, modifiers only raising, and downward adjustment only as a governed exception carrying reason, principal, scope, evidence, and review condition.

--- PLAN-20260723-0002#scope[7] ---
The experimental-versus-governed boundary: a classify function marking an invocation governed only when a valid authorization covers it, experimental otherwise. Classification only; no invocation is refused execution by this slice.

--- PLAN-20260723-0002#scope[8] ---
Predicate-registry entries for the Slice C predicates: assigned_role, authorized_by, authorizes, qualifies_executor, qualifies_for, issued_under, based_on, approved_by.

--- PLAN-20260723-0002#scope[9] ---
Validator fixtures covering valid records, each rejection class, and each refusal reason, plus an integration fixture authorizing an invocation against stored role, qualification, and principal records offline.

--- PLAN-20260723-0002#scope[10] ---
Field reconciliation with ABS-0004 4.13: InvocationAuthorization carries the inherited DecisionRecord fields (target, recommended_status and effective_status, issuer invocation, accountable approver, evidence, policy authority, activation state, supersession) alongside its kind-specific fields, and the documentation states how issuing principal, issuer invocation, and accountable approver relate. COMP-0037 found the plan's field list and the ontology's inherited list unreconciled.

--- PLAN-20260723-0002#scope[11] ---
Self-issued marking per ABS-0004 v7: where the issuing principal and the authorized executor are the same party, the authorization records self_issued true. Self-issued authorizations are permitted and are disqualified from counting as independent authorization wherever independence is required.

--- PLAN-20260723-0002#scope[12] ---
The one-hop bound is machine-visible, not only documented: the self-adjudication outcome carries an explicit check_depth field naming it a direct check, so a consumer cannot read a permitted result as a general independence finding.

--- PLAN-20260723-0002#source_capability_ids[0] ---
CAP-0015

--- PLAN-20260723-0002#source_capability_ids[1] ---
CAP-0016

--- PLAN-20260723-0002#source_gap_id ---
GAP-0005

--- PLAN-20260723-0002#status ---
proposed

--- PLAN-20260723-0002#success_criteria[0] ---
A stored invocation is classified governed when a valid authorization covers it and experimental otherwise, demonstrated by fixtures for both outcomes.

--- PLAN-20260723-0002#success_criteria[1] ---
Each of the ten enumerated refusal reasons is exercised by a fixture and yields that reason; no fixture path returns a permitted outcome without a matching authorization record.

--- PLAN-20260723-0002#success_criteria[2] ---
An authorization whose chain terminates nowhere is refused, and an authorization issued outside a principal's declared authority_scope is refused, each with its own reason.

--- PLAN-20260723-0002#success_criteria[3] ---
The one-hop self-adjudication check refuses an adjudicator authorization over an artifact produced by the same executor identity, demonstrated against a real captured InvocationRecord, permits it when the identities differ, and carries a check_depth field marking the result as direct-only in both cases.

--- PLAN-20260723-0002#success_criteria[4] ---
Consequence classification is exercised over the enumerated modifier set: for each modifier, a fixture asserts the effective class equals the maximum of the default and the modifier level, and a downward adjustment without a recorded governed exception is refused. This is enumerated-fixture coverage of the named cases, not a proof of monotonicity over all inputs.

--- PLAN-20260723-0002#success_criteria[5] ---
A qualification lacking an execution scope is rejected, and a qualification is not honoured for an endpoint or execution profile outside its scope.

--- PLAN-20260723-0002#success_criteria[6] ---
A self-issued authorization is accepted, carries self_issued true, and is reported as not independent by any check that asks for independent authorization.

--- PLAN-20260723-0002#success_criteria[7] ---
Regression: Slice A capture and Slice B resolution are unchanged, demonstrated by a fixture that runs both against stored records before and after authorization code is importable and asserts byte-identical outputs. COMP-0037 found this constraint had no corresponding check.

--- PLAN-20260723-0002#success_criteria[8] ---
The new modules are covered by tests exercising every public entrypoint and every enumerated outcome; the full suite passes offline with no network access.

--- PLAN-20260723-0002#success_criteria[9] ---
The repository audit reports ok true verified_current, and commit-level cross-environment reproduction from the public repository yields byte-identical checksums for every delivered file.

--- PLAN-20260723-0002#summary ---
Implement ABS-0004 v7 Slice C: RoleDefinition records on the three admitted axes, execution-scoped RoleQualification, InvocationAuthorization as a DecisionRecord kind, consequence classification, and the experimental-versus-governed boundary. An authorization is issued by an AccountablePrincipal holding standing authority within a declared scope, or chains to one; an authorization that chains to nothing is unauthorized rather than permitted. Authorization has one consequence in this slice and no others: an invocation is classified governed only when an authorization covers it, and experimental otherwise. Nothing is refused execution. The authorization function additionally performs a one-hop self-adjudication check using Slice A provenance: if the artifact under adjudication carries an InvocationRecord whose executor identity equals the executor being authorized, authorization is refused with an enumerated reason.

--- PLAN-20260723-0002#title ---
Roles, qualification, and invocation authorization (ABS-0004 Slice C)

--- END OF CANDIDATES ---

Output the JSON now.

## OpenAI Response

- model: `gpt-5.6-terra`

```
{"links":[{"claim":1,"block":null,"reason_if_null":"This is an overall assessment of the mechanical checkability of all ten success criteria, not a claim about one specific candidate block."},{"claim":2,"block":"PLAN-20260723-0002#success_criteria[0]"},{"claim":3,"block":"PLAN-20260723-0002#success_criteria[1]"},{"claim":4,"block":"PLAN-20260723-0002#success_criteria[2]"},{"claim":5,"block":"PLAN-20260723-0002#success_criteria[3]"},{"claim":6,"block":"PLAN-20260723-0002#success_criteria[3]"},{"claim":7,"block":"ABS-0004:v7:S8#def:ordinal-classes-low-medium-high-no"},{"claim":8,"block":"PLAN-20260723-0002#success_criteria[4]"},{"claim":9,"block":"PLAN-20260723-0002#success_criteria[5]"},{"claim":10,"block":"PLAN-20260723-0002#success_criteria[6]"},{"claim":11,"block":"PLAN-20260723-0002#success_criteria[7]"},{"claim":12,"block":"PLAN-20260723-0002#success_criteria[8]"},{"claim":13,"block":"PLAN-20260723-0002#success_criteria[9]"},{"claim":14,"block":"PLAN-20260723-0002#success_criteria[9]"},{"claim":15,"block":"ABS-0004:v7:S8#def:ordinal-classes-low-medium-high-no"},{"claim":16,"block":"PLAN-20260723-0002#constraints[0]"},{"claim":17,"block":"PLAN-20260723-0002#constraints[1]"},{"claim":18,"block":"PLAN-20260723-0002#constraints[2]"},{"claim":19,"block":"PLAN-20260723-0002#constraints[3]"},{"claim":20,"block":"PLAN-20260723-0002#proposed_change"},{"claim":21,"block":"PLAN-20260723-0002#status"}]}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"links":[
{"claim":1,"block":null,"reason_if_null":"General overview statement about all ten criteria collectively, not tied to one specific block"},
{"claim":2,"block":"PLAN-20260723-0002#success_criteria[0]","reason_if_null":""},
{"claim":3,"block":"PLAN-20260723-0002#success_criteria[1]","reason_if_null":""},
{"claim":4,"block":"PLAN-20260723-0002#success_criteria[2]","reason_if_null":""},
{"claim":5,"block":"PLAN-20260723-0002#success_criteria[3]","reason_if_null":""},
{"claim":6,"block":"PLAN-20260723-0002#success_criteria[3]","reason_if_null":""},
{"claim":7,"block":"ABS-0004:v7:S8#def:ordinal-classes-low-medium-high-no","reason_if_null":""},
{"claim":8,"block":"PLAN-20260723-0002#success_criteria[4]","reason_if_null":""},
{"claim":9,"block":"PLAN-20260723-0002#success_criteria[5]","reason_if_null":""},
{"claim":10,"block":"PLAN-20260723-0002#success_criteria[6]","reason_if_null":""},
{"claim":11,"block":"PLAN-20260723-0002#success_criteria[7]","reason_if_null":""},
{"claim":12,"block":"PLAN-20260723-0002#success_criteria[8]","reason_if_null":""},
{"claim":13,"block":"PLAN-20260723-0002#success_criteria[9]","reason_if_null":""},
{"claim":14,"block":"PLAN-20260723-0002#success_criteria[9]","reason_if_null":""},
{"claim":15,"block":"ABS-0004:v7:S8#def:ordinal-classes-low-medium-high-no","reason_if_null":""},
{"claim":16,"block":"PLAN-20260723-0002#constraints[0]","reason_if_null":""},
{"claim":17,"block":"PLAN-20260723-0002#constraints[1]","reason_if_null":""},
{"claim":18,"block":"PLAN-20260723-0002#constraints[2]","reason_if_null":""},
{"claim":19,"block":"PLAN-20260723-0002#constraints[3]","reason_if_null":""},
{"claim":20,"block":"PLAN-20260723-0002#proposed_change","reason_if_null":""},
{"claim":21,"block":"PLAN-20260723-0002#status","reason_if_null":""}
]}
```
