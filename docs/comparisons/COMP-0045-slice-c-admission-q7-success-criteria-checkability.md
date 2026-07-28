# COMP-0045: Provider Comparison — Slice C admission Q7 success-criteria-checkability

## Metadata

- comparison_id: `COMP-0045`
- title: `Slice C admission Q7 success-criteria-checkability`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-f0fc3f53f3eb5ee8.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0045", "target_id": "INV-f0fc3f53f3eb5ee8"}, {"authoritative": false, "evidence": "docs/invocations/INV-dafb3f854d8fcffa.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0045", "target_id": "INV-dafb3f854d8fcffa"}]`
- created_at: `2026-07-28T18:53:02.613644+00:00`
- command: `scripts/compare_providers.py --title Slice C admission Q7 success-criteria-checkability You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: the ABS-0004 v7 amendment is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force yet.

One disclosure, because the plan text refers to it and withholding it would be dishonest rather than isolating: v7 replaces a v6 rule that claimed to prevent the authorization regress from being closed by convenience, after two reviewers in a prior round independently defeated it. Do not accept the plan's characterisation of that break, and do not treat it as the only one available.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q7 ===
Which of the plan's ten success criteria are mechanically checkable as written, and which are not?

Address specifically: the audit criterion, which supplies no procedure, command, or semantics for verified_current; the cross-environment reproduction criterion, which names no environments, build inputs, or normalization rules; the coverage criterion; and criterion 4's "demonstrated against a real captured InvocationRecord", which names no record and gives no acceptance rule for "real".

Consider also whether the consequence-classification criterion can be tested at all given the state of Section 8. Name any constraint in the plan that has no corresponding check.

=== EVIDENCE ABS-0004:v7:S8 :: ABS-0004 v7 Section 8 (consequence classes) ===
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

=== QUESTION Q7 ===
Which of the plan's ten success criteria are mechanically checkable as written, and which are not?

Address specifically: the audit criterion, which supplies no procedure, command, or semantics for verified_current; the cross-environment reproduction criterion, which names no environments, build inputs, or normalization rules; the coverage criterion; and criterion 4's "demonstrated against a real captured InvocationRecord", which names no record and gives no acceptance rule for "real".

Consider also whether the consequence-classification criterion can be tested at all given the state of Section 8. Name any constraint in the plan that has no corresponding check.

=== EVIDENCE ABS-0004:v7:S8 :: ABS-0004 v7 Section 8 (consequence classes) ===
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
The criteria are not uniformly mechanically checkable as written. Several specify fixture-level assertions that can be automated; others depend on undefined terms, missing procedures, or ontology material explicitly left open.

| Criterion | Mechanical status | Reason |
|---|---|---|
| 1. Governed versus experimental classification | **Checkable at the stated fixture level** | It supplies an operational outcome rule—“governed when a valid authorization covers it and experimental otherwise”—and requires fixtures for both outcomes. The meaning of “valid authorization” must be supplied by the authorization validator and `authorize()` rules, but the two requested fixture outcomes are mechanically assertable. |
| 2. Ten refusal reasons and no unauthorised permitted fixture path | **Mostly checkable** | The ten reasons are enumerated in scope, so a fixture can invoke each condition and assert the returned reason. The requirement that no fixture path permits without a matching authorization record can also be checked over the defined fixtures. It is not a proof that *all possible* implementation paths behave so, because neither a path model nor exhaustive-input domain is specified. |
| 3. Unterminated chain and out-of-scope standing authority | **Only partly checkable as a general criterion** | A fixture can create a chain that terminates nowhere and can create a chosen out-of-scope case. But `authority_scope` has no supplied grammar or matching semantics. Without those, a machine cannot generally determine that a particular authorization is “outside” a declared scope; it can only test implementation-selected examples. |
| 4. One-hop self-adjudication, including a “real captured InvocationRecord” | **Partly checkable; not fully checkable as written** | Same-identity refusal, different-identity permission, and `check_depth` equal to a direct-only value are fixture-testable. The required demonstration “against a real captured InvocationRecord” is not: no InvocationRecord is named, no capture record is supplied, and no acceptance rule distinguishes “real captured” from a constructed fixture. The evidence set would need the identified InvocationRecord and a rule or provenance criterion establishing that it is a captured record. |
| 5. Consequence classification | **Not fully mechanically checkable against Section 8 as it stands** | A test can assert selected ordinal results for selected fixture values and can reject a downward adjustment lacking the stated exception data. But Section 8 labels the “Detailed classification function” `[OPEN]`. In particular, the evidence does not define how the listed modifiers acquire `applicable_modifier_levels`, how applicability is determined, or a complete record-level validation procedure for a governed downward exception. The ordinal ordering supports a chosen `max` implementation, but not a complete classifier for the named modifiers. Thus this can test an implementation’s chosen fixture mapping, not conformity to a complete Section 8 classification function. |
| 6. Qualification scope | **Partly checkable** | Rejecting an absent execution scope is direct. Testing a chosen endpoint or ExecutionProfile outside a declared scope is also direct. General enforcement is underspecified because the supplied material does not define matching semantics for “permitted ExecutionProfile constraints” or what makes a profile “materially different.” |
| 7. Self-issued marking and independence | **Partly checkable** | Exact-identifier cases can be automated: the plan states that party sameness uses “exact identifier equality only,” and a fixture can assert `self_issued true`. But “reported as not independent by any check that asks for independent authorization” has no supplied interface, set of such checks, or complete semantics of independence. It is therefore not mechanically bounded as written. |
| 8. Slice A/B regression | **Checkable at the stated fixture level** | A defined fixture can run Slice A and Slice B before and after the authorization code is importable and compare bytes. This checks the stated fixture and byte-identity condition. It does not establish the broader constraint that “no field, path, or default of either is altered” for all inputs, but the success criterion itself is mechanically executable. |
| 9. Test coverage and offline suite | **Not fully mechanically checkable as written** | Tests can enumerate public functions and listed outcomes, and a suite can be run with network access blocked. However, “every public entrypoint” lacks a definition of public API, and “covered by tests” lacks a coverage rule. “The full suite passes offline” also names no test command, runner, dependency-installation conditions, or offline enforcement method. It is an automatable goal only after those are specified. |
| 10. Audit and cross-environment reproduction | **Not mechanically checkable as written** | The audit clause gives no audit procedure, command, report schema, or semantics for `ok true verified_current`. The reproduction clause names no environments, build inputs, dependency-resolution rules, file-selection rule, checksum algorithm, or normalization rules. “Byte-identical checksums” is itself incomplete without those definitions. |

## Specifically on criterion 10

The audit condition cannot be evaluated from the plan because it only says:

> “The repository audit reports ok true verified_current”

There is no identified audit record, command, evaluator, report schema, meaning of `verified_current`, or rule for determining the relevant current state.

The cross-environment condition cannot be reproduced because it only says:

> “commit-level cross-environment reproduction from the public repository yields byte-identical checksums for every delivered file.”

It does not identify the environments, operating-system or architecture variation, interpreter and dependency versions, build command, whether dependencies may be fetched, how generated metadata is normalized, which files count as “delivered,” or the checksum method. Those omissions are material, especially for byte identity.

## Consequence-classification limitation

Criterion 5 invokes “the enumerated modifier set,” and Section 8 names the modifiers, but Section 8 also says:

> `[OPEN]` Detailed classification function.

That leaves no complete machine-testable definition for assigning modifier levels or determining applicability. The criterion can support enumerated fixtures whose expected values are chosen in advance, but the evidence does not support treating those fixtures as a complete test of the Section 8 rule.

To make this criterion mechanically checkable, the missing material would be a completed Section 8 classification function defining, at minimum:

- the level assigned by each modifier;
- when each modifier is applicable;
- the representation and validation rules for modifier evidence;
- the ordering and `max` behavior over absent and multiple modifiers; and
- the machine-validatable form of the governed downward exception, including its “reason, accountable principal, scope, evidence, expiry/review.”

## Plan constraints lacking a corresponding success-criterion check

The following plan constraints have no corresponding direct success-criterion check:

1. **Admission-warrant scope and expansion**  
   The constraint that implementation is authorized only within a future admission warrant, and that expansion needs a separate plan, has no success criterion that checks an admission warrant or compares implementation scope against it.

2. **Exact ABS-0004 v7 field names and semantics**  
   No criterion performs a general conformance comparison against v7. Moreover, the supplied evidence omits the referenced Sections 4.9 and 4.13 and leaves Section 8’s detailed function open, so a complete conformance check could not be constructed from this evidence set.

3. **GraphRelation and registered Slice A/B/C predicate restriction**  
   No criterion checks that all relations use `GraphRelation` or that no predicate falls outside the registered lists. The `GraphRelation` shape and the Slice A, B, and C lists are not supplied; they would be needed to perform that check.

4. **Purity of `authorize()`**  
   No criterion directly checks that `authorize()` has “no I/O, no clock, no network,” or that its timestamp is supplied by the caller. Criterion 9’s offline-suite condition does not establish purity: code can access a clock or attempt I/O without requiring successful network access.

5. **No alteration of Slice A/B fields, paths, or defaults**  
   Criterion 8 checks byte-identical output for one stored-record fixture, but does not directly check the constraint’s stronger prohibition on changing any field, path, or default.

6. **No provider-call behavior change and no execution refusal**  
   The proposed change says there is “No change to provider-call behavior” and the non-goals say authorization “does not gate” and no invocation is refused execution by this slice. No success criterion executes an invocation flow and verifies that classification or authorization refusal does not block execution.

The standing-authority constraint does have a partial corresponding check in criterion 3: declared scope is required and an out-of-scope authorization is meant to be refused. Its general mechanical adequacy remains limited by the missing `authority_scope` grammar and matching semantics.

## Missing evidence needed for the unresolved checks

The evidence set is insufficient for full assessment of the following claimed checks. Needed material is:

- a completed Section 8 detailed classification function, for criterion 5;
- the `authority_scope` grammar and scope-matching rules, for criteria 3 and 6;
- the named captured InvocationRecord and a rule establishing “real captured,” for criterion 4;
- a definition of independence checks and their public interfaces, for criterion 7;
- a public-API definition, test command, runner, and offline execution procedure, for criterion 9;
- the audit procedure, command, report schema, and `verified_current` semantics, for criterion 10;
- named reproduction environments, build inputs, dependency rules, normalization rules, delivered-file set, and checksum procedure, for criterion 10;
- the `GraphRelation` shape and registered Slice A/B/C predicate lists, for the relation constraint;
- the referenced ABS-0004 Sections 4.9 and 4.13, for the claimed exact field-and-semantics conformance check.

Because both the amendment and plan remain proposed and not admitted, none of these criteria or constraints presently has governance force.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Mechanically checkable vs. not, by criterion (in the order given in `success_criteria`)

**1. Governed/experimental classification (fixtures for both outcomes).**
Checkable. The classify function and its two outcomes are fully specified in `scope`, and the criterion asks only for fixture demonstration of a binary condition.

**2. Ten refusal reasons, each exercised by fixture; no permitted outcome without a matching authorization record.**
Checkable. The ten reasons are enumerated in `scope`, `authorize()` is specified as pure, and "yields that reason" / "no fixture path returns permitted without a match" are both binary, fixture-testable conditions.

**3. Chain-terminates-nowhere refusal; authority-scope-violation refusal.**
Checkable. Both conditions are named refusal reasons over stored records, testable by constructing the corresponding fixture.

**4. One-hop self-adjudication check.**
Partially checkable, partially not. The mechanical parts — refuse when executor identities match, permit when they differ, `check_depth` field present and marked direct-only — are testable against any fixture InvocationRecord; nothing about that logic requires a "real" one. But **"demonstrated against a real captured InvocationRecord"** supplies no record identifier, no source, and no acceptance rule distinguishing a "real captured" record from a synthetic fixture. As written there is no check that can fail this clause specifically — a reviewer cannot tell whether a given fixture satisfies "real" or not. This sub-clause is not mechanically checkable; the identity-collision logic around it is.

**5. Consequence classification over the enumerated modifier set.**
Checkable only in the narrow sense the plan itself claims ("enumerated-fixture coverage... not a proof of monotonicity"). Section 8 defines `effective_consequence = max(default_consequence, applicable_modifier_levels)` precisely, so a fixture asserting the max-formula holds for a *given* set of modifier levels is testable, and "downward adjustment without a recorded governed exception is refused" is testable against the `[ADOPTED_CONSTRAINT]` on governed exceptions.
However, Section 8 also marks `[OPEN] Detailed classification function` — there is no adopted rule for *deriving* which modifier levels apply to a given invocation's actual content. So the fixtures can only assert internal consistency of the combination formula for levels the test author assigns by hand; they cannot check that the classification of any real invocation is correct, because the mapping from invocation facts to modifier levels doesn't yet exist as governance text. The criterion is checkable as a formula-consistency test, not as a classification-correctness test, and the plan's own hedge ("not a proof of monotonicity over all inputs") is doing real work here — it is narrower than "consequence classification is exercised," which could be misread as testing the classifier itself.

**6. Qualification execution-scope rejection.**
Checkable. Section 4.6 gives the scope fields explicitly (endpoint, ExecutionProfile constraints, session-state constraints, policy version); "lacking an execution scope" and "outside its scope" are both testable against the validator.

**7. Self-issued authorization: accepted, `self_issued` true, reported not-independent.**
Checkable, given the plan's own stated rule (mitigation: "exact identifier equality only"). That rule supplies the missing semantics that a bare "same party" test would otherwise lack.

**8. Regression: byte-identical Slice A/B outputs before and after.**
Checkable. "Byte-identical" is an unambiguous, mechanically comparable output; the fixture procedure (run before/after import) is stated.

**9. Coverage criterion ("every public entrypoint and every enumerated outcome," full suite passes offline).**
Not fully checkable as written. "The full suite passes offline with no network access" is checkable (pass/fail, no network calls). But "covered by tests exercising every public entrypoint and every enumerated outcome" supplies no completeness procedure: no coverage tool, no threshold, no enumerated list of "public entrypoints" against which fixtures are checked off, no definition of what counts as an "enumerated outcome" beyond the ten refusal reasons already covered by criterion 2. Whether a given test suite satisfies "every" entrypoint is a judgment call, not a mechanical check, absent a named coverage instrument or an explicit checklist artifact.

**10. Audit criterion and cross-environment reproduction.**
Not mechanically checkable as written, on both halves:
- "The repository audit reports `ok true verified_current`" — no procedure, command, tool, or semantics for `verified_current` appears anywhere in the evidence set. There is no audit specification to check this against. **Missing:** an audit-tool specification or schema document (not present in evidence) that would define what `verified_current` asserts and how it's computed — needed to know whether this is even a boolean flag, a timestamp comparison, a hash check, or something else.
- "commit-level cross-environment reproduction... yields byte-identical checksums for every delivered file" — no environments are named, no build inputs are specified, and no normalization rules (line endings, timestamps, path separators, toolchain/interpreter versions) are given. Without at least two named environments and a build procedure, "reproduction" cannot be executed, let alone checked. **Missing:** an environment/build specification (e.g., a CI matrix or reproducibility spec) that is not present in this evidence set.

## Constraints with no corresponding check

Checking the plan's top-level `constraints` list against the ten success criteria:

- **"Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan."** No success criterion tests scope containment against a warrant; there is nothing to check this against until a warrant exists, and none of the ten criteria references warrant scope at all.
- **"Field names and semantics follow ABS-0004 v7 exactly; deviations require an ABS revision first."** No criterion checks field-name/semantic conformance to the ontology text. "Field reconciliation with ABS-0004 4.13" appears in `scope`, not in `success_criteria` — it is a deliverable, not a checked outcome.
- **"All relations use the GraphRelation shape; no predicate outside the registered Slice A, B, and C lists."** No criterion checks predicate-registry conformance or relation shape; the predicate-registry entries appear as an expected output, not as something any success criterion verifies.
- **"authorize() is pure over stored records: no I/O, no clock, no network; the decision timestamp is supplied by the caller."** Only the network half is indirectly covered ("full suite passes offline with no network access" in criterion 9). "No I/O," "no clock," and "timestamp supplied by caller" have no corresponding fixture or check anywhere in the ten criteria.

## What I would have used but don't have

- ABS-0004 v7 Section 4.9 (RoleDefinition constraint fields) and Section 4.13 (DecisionRecord inherited fields) — referenced in `scope` but not in evidence; needed to assess whether criterion 3's "own reason" and the field-reconciliation deliverable are actually checkable against defined field lists.
- Any audit-tool or CI/reproducibility specification — not in evidence — needed to assess criterion 10 at all, beyond noting its absence.
```
