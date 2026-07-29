# COMP-0096: Provider Comparison — Claim linking LK-EX-Q5-claude-sonnet-5-by-gpt-5-6-terra

## Metadata

- comparison_id: `COMP-0096`
- title: `Claim linking LK-EX-Q5-claude-sonnet-5-by-gpt-5-6-terra`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-11a66375edcf54f9.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0096", "target_id": "INV-11a66375edcf54f9"}, {"authoritative": false, "evidence": "docs/invocations/INV-975ae6d692de2343.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0096", "target_id": "INV-975ae6d692de2343"}]`
- created_at: `2026-07-29T06:30:46.747051+00:00`
- command: `scripts/compare_providers.py --title Claim linking LK-EX-Q5-claude-sonnet-5-by-gpt-5-6-terra You are linking extracted claims to the specific block of source text each claim is about. This is a matching task. Do not evaluate whether any claim is correct.

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

1. claim: A field is data, not a control.
   quote: "A field is data, not a control."
   extractor called it about: check_depth field on the authorization outcome

2. claim: The presence of check_depth does not force a downstream consumer to branch on it.
   quote: "nothing about its presence forces a downstream consumer to branch on it."
   extractor called it about: downstream consumers of check_depth

3. claim: The plan does not implement downstream behavior that treats a non-full-ancestry check_depth as a reason to withhold a broader conclusion.
   quote: "downstream behavior this plan does not implement"
   extractor called it about: plan downstream consumer behavior for check_depth

4. claim: check_depth does not stop a consumer from reading a permitted result as clearance.
   quote: "it does not stop a consumer from reading a permitted, undifferentiated-looking result as clearance."
   extractor called it about: check_depth field on permitted authorization results

5. claim: The plan's statement that a consumer cannot read a permitted result as a general independence finding overstates what a field does.
   quote: "overstates what a field does."
   extractor called it about: plan wording about consumer interpretation of permitted results

6. claim: A field makes a misreading avoidable by an attentive reader, rather than making a misreading impossible.
   quote: "it makes a misreading *avoidable by an attentive reader*, which is a different and weaker claim."
   extractor called it about: check_depth field disclosure effect

7. claim: In the two-hop case, the one-hop check passes and authorization is permitted even though A is in Y's evidence ancestry two hops back.
   quote: "A ≠ B, so the check passes and authorization is permitted — even though A sits in Y's evidence ancestry exactly two hops back"
   extractor called it about: two-hop A-to-X-to-Y self-adjudication case

8. claim: The one-hop check implements only C3's most direct case.
   quote: "the one-hop check implements C3's most direct case only."
   extractor called it about: C3 implementation scope

9. claim: check_depth correctly tells a reader that the check examined a single hop and no further.
   quote: "it correctly tells a reader that the check that produced this outcome examined a single hop and no further."
   extractor called it about: check_depth disclosure of check scope

10. claim: check_depth is not disclosure of whether an actual two-hop collision exists for a particular artifact.
   quote: "It is not disclosure of *this case*:"
   extractor called it about: check_depth disclosure in the two-hop case

11. claim: check_depth carries no information about whether an actual two-hop collision exists for a particular artifact.
   quote: "it carries no information about whether an actual two-hop collision exists for this particular artifact."
   extractor called it about: check_depth value on authorization outcomes

12. claim: check_depth cannot distinguish a two-hop-clean case from the described two-hop-colliding case.
   quote: "It cannot distinguish the two-hop-clean case from the two-hop-colliding case above"
   extractor called it about: check_depth value in two-hop ancestry cases

13. claim: check_depth is necessary but not sufficient to prevent the independence misreading in the actual two-hop case.
   quote: "That is necessary but not sufficient to prevent the independence misreading in the actual two-hop case"
   extractor called it about: check_depth sufficiency for two-hop independence interpretation

14. claim: Actual prevention would require either a consumer that refuses to treat direct-only permitted results as evidence of adjudicator independence or ancestry traversal.
   quote: "the actual prevention would require either (a) a consumer that refuses to treat any `check_depth: direct` permitted-result as evidence for adjudicator independence, or (b) the ancestry traversal itself"
   extractor called it about: prevention of independence misreading for direct-only authorization results

15. claim: The plan wording should replace the claim that a consumer cannot read a permitted result as a general independence finding.
   quote: "Replace "a consumer cannot read a permitted result as a general independence finding""
   extractor called it about: plan wording about consumer interpretation of permitted results

16. claim: The evidence set does not define what values check_depth may take beyond "direct."
   quote: "No definition in the evidence set of what values `check_depth` may take beyond "direct""
   extractor called it about: check_depth permitted values

17. claim: No Slice D specification is present for traversal rules, evidence-ancestry graph resolution, or cycle and join termination conditions.
   quote: "No Slice D specification present (traversal rules, what "evidence ancestry" resolves to as a graph operation, termination conditions for cycles/joins)."
   extractor called it about: Slice D ancestry traversal specification

18. claim: No documentation excerpt from AUTHORIZATION_RECORDS.md is included showing how the one-hop bound's limitations are worded for consumers.
   quote: "No documentation excerpt from `AUTHORIZATION_RECORDS.md`"
   extractor called it about: AUTHORIZATION_RECORDS.md consumer-facing limitation documentation

=== CANDIDATE BLOCKS ===

--- ABS-0004:v7:C3#whole ---
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

1. claim: A field is data, not a control.
   quote: "A field is data, not a control."
   extractor called it about: check_depth field on the authorization outcome

2. claim: The presence of check_depth does not force a downstream consumer to branch on it.
   quote: "nothing about its presence forces a downstream consumer to branch on it."
   extractor called it about: downstream consumers of check_depth

3. claim: The plan does not implement downstream behavior that treats a non-full-ancestry check_depth as a reason to withhold a broader conclusion.
   quote: "downstream behavior this plan does not implement"
   extractor called it about: plan downstream consumer behavior for check_depth

4. claim: check_depth does not stop a consumer from reading a permitted result as clearance.
   quote: "it does not stop a consumer from reading a permitted, undifferentiated-looking result as clearance."
   extractor called it about: check_depth field on permitted authorization results

5. claim: The plan's statement that a consumer cannot read a permitted result as a general independence finding overstates what a field does.
   quote: "overstates what a field does."
   extractor called it about: plan wording about consumer interpretation of permitted results

6. claim: A field makes a misreading avoidable by an attentive reader, rather than making a misreading impossible.
   quote: "it makes a misreading *avoidable by an attentive reader*, which is a different and weaker claim."
   extractor called it about: check_depth field disclosure effect

7. claim: In the two-hop case, the one-hop check passes and authorization is permitted even though A is in Y's evidence ancestry two hops back.
   quote: "A ≠ B, so the check passes and authorization is permitted — even though A sits in Y's evidence ancestry exactly two hops back"
   extractor called it about: two-hop A-to-X-to-Y self-adjudication case

8. claim: The one-hop check implements only C3's most direct case.
   quote: "the one-hop check implements C3's most direct case only."
   extractor called it about: C3 implementation scope

9. claim: check_depth correctly tells a reader that the check examined a single hop and no further.
   quote: "it correctly tells a reader that the check that produced this outcome examined a single hop and no further."
   extractor called it about: check_depth disclosure of check scope

10. claim: check_depth is not disclosure of whether an actual two-hop collision exists for a particular artifact.
   quote: "It is not disclosure of *this case*:"
   extractor called it about: check_depth disclosure in the two-hop case

11. claim: check_depth carries no information about whether an actual two-hop collision exists for a particular artifact.
   quote: "it carries no information about whether an actual two-hop collision exists for this particular artifact."
   extractor called it about: check_depth value on authorization outcomes

12. claim: check_depth cannot distinguish a two-hop-clean case from the described two-hop-colliding case.
   quote: "It cannot distinguish the two-hop-clean case from the two-hop-colliding case above"
   extractor called it about: check_depth value in two-hop ancestry cases

13. claim: check_depth is necessary but not sufficient to prevent the independence misreading in the actual two-hop case.
   quote: "That is necessary but not sufficient to prevent the independence misreading in the actual two-hop case"
   extractor called it about: check_depth sufficiency for two-hop independence interpretation

14. claim: Actual prevention would require either a consumer that refuses to treat direct-only permitted results as evidence of adjudicator independence or ancestry traversal.
   quote: "the actual prevention would require either (a) a consumer that refuses to treat any `check_depth: direct` permitted-result as evidence for adjudicator independence, or (b) the ancestry traversal itself"
   extractor called it about: prevention of independence misreading for direct-only authorization results

15. claim: The plan wording should replace the claim that a consumer cannot read a permitted result as a general independence finding.
   quote: "Replace "a consumer cannot read a permitted result as a general independence finding""
   extractor called it about: plan wording about consumer interpretation of permitted results

16. claim: The evidence set does not define what values check_depth may take beyond "direct."
   quote: "No definition in the evidence set of what values `check_depth` may take beyond "direct""
   extractor called it about: check_depth permitted values

17. claim: No Slice D specification is present for traversal rules, evidence-ancestry graph resolution, or cycle and join termination conditions.
   quote: "No Slice D specification present (traversal rules, what "evidence ancestry" resolves to as a graph operation, termination conditions for cycles/joins)."
   extractor called it about: Slice D ancestry traversal specification

18. claim: No documentation excerpt from AUTHORIZATION_RECORDS.md is included showing how the one-hop bound's limitations are worded for consumers.
   quote: "No documentation excerpt from `AUTHORIZATION_RECORDS.md`"
   extractor called it about: AUTHORIZATION_RECORDS.md consumer-facing limitation documentation

=== CANDIDATE BLOCKS ===

--- ABS-0004:v7:C3#whole ---
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
{"links":[{"claim":1,"block":"PLAN-20260723-0002#scope[12]"},{"claim":2,"block":"PLAN-20260723-0002#scope[12]"},{"claim":3,"block":"PLAN-20260723-0002#scope[12]"},{"claim":4,"block":"PLAN-20260723-0002#scope[12]"},{"claim":5,"block":"PLAN-20260723-0002#scope[12]"},{"claim":6,"block":"PLAN-20260723-0002#scope[12]"},{"claim":7,"block":"PLAN-20260723-0002#scope[5]"},{"claim":8,"block":"PLAN-20260723-0002#non_goals[4]"},{"claim":9,"block":"PLAN-20260723-0002#scope[12]"},{"claim":10,"block":"PLAN-20260723-0002#scope[12]"},{"claim":11,"block":"PLAN-20260723-0002#scope[12]"},{"claim":12,"block":"PLAN-20260723-0002#scope[12]"},{"claim":13,"block":"PLAN-20260723-0002#scope[12]"},{"claim":14,"block":"PLAN-20260723-0002#scope[12]"},{"claim":15,"block":"PLAN-20260723-0002#scope[12]"},{"claim":16,"block":"PLAN-20260723-0002#scope[12]"},{"claim":17,"block":null,"reason_if_null":"It concerns the absence of a Slice D traversal specification, rather than a specific included passage."},{"claim":18,"block":null,"reason_if_null":"It concerns the absence of an AUTHORIZATION_RECORDS.md documentation excerpt."}]}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"links":[
{"claim":1,"block":"PLAN-20260723-0002#scope[12]"},
{"claim":2,"block":"PLAN-20260723-0002#scope[12]"},
{"claim":3,"block":"PLAN-20260723-0002#scope[12]"},
{"claim":4,"block":"PLAN-20260723-0002#scope[12]"},
{"claim":5,"block":"PLAN-20260723-0002#scope[12]"},
{"claim":6,"block":"PLAN-20260723-0002#scope[12]"},
{"claim":7,"block":"PLAN-20260723-0002#scope[5]"},
{"claim":8,"block":"PLAN-20260723-0002#non_goals[4]"},
{"claim":9,"block":"PLAN-20260723-0002#success_criteria[3]"},
{"claim":10,"block":"PLAN-20260723-0002#success_criteria[3]"},
{"claim":11,"block":"PLAN-20260723-0002#success_criteria[3]"},
{"claim":12,"block":"PLAN-20260723-0002#success_criteria[3]"},
{"claim":13,"block":"PLAN-20260723-0002#risk"},
{"claim":14,"block":null,"reason_if_null":"This is the critique's own proposed remedy (consumer refusal rule or ancestry traversal) rather than an assertion about a specific passage in the plan or ABS-0004 text."},
{"claim":15,"block":"PLAN-20260723-0002#scope[12]"},
{"claim":16,"block":"PLAN-20260723-0002#success_criteria[3]"},
{"claim":17,"block":"PLAN-20260723-0002#non_goals[2]"},
{"claim":18,"block":"PLAN-20260723-0002#expected_outputs[3]"}
]}
```
