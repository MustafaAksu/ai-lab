# COMP-0038: Provider Comparison — ABS-0004 v7 amendment and revised PLAN-20260723-0002 slice C admission review

## Metadata

- comparison_id: `COMP-0038`
- title: `ABS-0004 v7 amendment and revised PLAN-20260723-0002 slice C admission review`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-83db700fbe901487.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0038", "target_id": "INV-83db700fbe901487"}, {"authoritative": false, "evidence": "docs/invocations/INV-b59b93ec9cd8dbe6.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0038", "target_id": "INV-b59b93ec9cd8dbe6"}]`
- created_at: `2026-07-25T16:14:06.114988+00:00`
- command: `scripts/compare_providers.py --title ABS-0004 v7 amendment and revised PLAN-20260723-0002 slice C admission review Review the plan below for admission, together with the ontology amendment it depends on. Full texts are included; do not rely on repository access, and quote only text that appears below. If something you need is not present, say so rather than inferring it.

Status of what you are reading: the ABS-0004 v7 amendment is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force yet, and this round is the admission checkpoint for both.

One disclosure, because the plan text refers to it and withholding it would be dishonest rather than isolating: v7 replaces a v6 rule that claimed to prevent the authorization regress from being closed by convenience, after two reviewers in a prior round independently defeated it. The plan's rationale characterises that break. Do not accept the plan's characterisation, and do not treat the prior break as the only one available. Where a question asks you to construct an abuse, construct it from the text below. If you judge that this disclosure has shaped your answer, say where.

=== ABS-0004 v7 SECTION 3 (three decisions, P7, authorization-chain termination) ===
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

`[PRINCIPLE]` P7. Root authority is extra-systemic. An authorization chain
terminates at a standing authority that the system records and does not
establish. Who is accountable for AI-Lab is a fact about the world, about
who controls the repository and answers for it, and no arrangement of
records inside the repository can make that fact true or verify it. Any
design that appears to derive root authority from internal evidence has
merely moved the regress and disguised it.

`[DEF]` Authorization-chain termination. A chain terminates at an
AccountablePrincipal's standing authority within a declared
`authority_scope`. Authorizations the principal issues inside that scope
are self-standing. Every other authorization must chain, through one or
more steps, to such a standing authority. An authorization that chains to
nothing is not thereby permitted: it is unauthorized.

`[ADOPTED_CONSTRAINT]` A standing-authority claim is recorded, never
verified. AI-Lab does not validate that a declared principal is entitled to
the authority it claims; it has no means to do so, and pretending otherwise
would be the overclaim P6 forbids. What the record provides is visibility:
the claim, its declared scope, and every authorization resting on it are
legible and attributable. Visibility is the whole of what this constraint
achieves, and it is not prevention.

`[ADOPTED_CONSTRAINT]` Scope breadth is visible, not bounded by fiat. A
declared `authority_scope` may be arbitrarily wide, including universal. A
wide scope is permitted and must be legible as wide; it may not be
described, in a record or in a summary, as bounded merely because a scope
field was populated. A boundary that no one can fail to satisfy is not a
boundary, and calling it one is the defect this constraint exists to
prevent.

`[ADOPTED_CONSTRAINT]` Self-issued authorization is marked, never silently
accepted. Where the issuing principal and the authorized executor are the
same party, or where a principal issues an authorization covering an
invocation it also performs, the authorization records `self_issued: true`.
A self-issued authorization is not refused: at the root of any chain, the
accountable party necessarily authorizes work it is also responsible for.
It is instead disqualified from counting as independent authorization
wherever independence is required, and it is countable as such.

`[DEF]` Standing authority is not a capability of executors. A model, tool,
or human acting as an executor never holds standing authority by virtue of
executing; it holds it only as an AccountablePrincipal within a declared
scope, which is a separate role under Section 4.13. One party may hold both
roles; the ontology separates the roles, not the parties, and the
`self_issued` marking is how the coincidence is recorded rather than
denied.

`[OPEN]` Whether standing authority requires periodic re-declaration or
review. COMP-0037 established what v6 got wrong here: both reviewers
independently constructed the same self-authorization path, and v6's claim
to prevent convenient closure of the regress was false. v7 does not close
the question by asserting a stronger internal control; it records that no
internal control can close it, and asks instead what external evidence a
scope declaration should carry.

=== ABS-0004 v7 SECTION 4.6-4.7 (qualification, executors) ===
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

=== ABS-0004 v7 SECTION 4.9 (RoleDefinition) ===
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

=== ABS-0004 v7 SECTION 4.13 (DecisionRecord, AccountablePrincipal) ===
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

=== ABS-0004 v7 SECTION 8 (consequence classes) ===
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

=== ABS-0004 v7 SECTION 9 (enforcement matrix) ===
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

=== ABS-0004 v7 CONSTRAINTS C3 AND C6 (from Section 6) ===
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

=== PLAN-20260723-0002 ===
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

=== QUESTIONS ===
1. The central question of this round. v6 claimed to prevent convenient closure of the authorization regress; v7 withdraws that claim and asserts only visibility: a standing-authority claim is recorded and never verified, a declared authority_scope may be arbitrarily wide including universal, and a self-issued authorization is marked and disqualified from independence rather than refused. Two readings are available. (a) This is the honest terminus: no arrangement of internal records can establish extra-systemic authority, so any mechanical scope bound would be theatre, and saying so plainly is the most the system can truthfully do. (b) This is capitulation: the constraint existed to bound the root, and permitting a universal scope while requiring only that it be legible as wide converts a control into a label. Argue for one reading. State what construction or evidence would distinguish them, so the disagreement is decidable rather than a matter of taste.

2. v7 was written to retract an overclaim. Does it contain a new one? Read its adopted constraints as written and name any sentence that claims more than the record can support - including any place where the retraction itself is overstated, or where visibility is asserted as achieved when the mechanism described would not achieve it.

3. Attack v7 independently. Construct a path by which an executor or principal obtains effective authority, or by which the record misrepresents who authorized what, while satisfying every sentence of Section 3 as written. If the self_issued marking together with the disqualification-from-independence rule blocks your construction, report that plainly rather than forcing an attack.

4. The plan enumerates ten refusal reasons. Are they complete for the meaning of "valid authorization" the plan adopts? Note that the plan does not state whether Section 4.7's disclosure constraints - undisclosed material subordinate execution, undeclared execution-path-changing tool configuration, undeclared material external interaction - are checked here, excluded from the meaning of valid authorization, or deferred. Name the disposition the plan should state, and any further case that should refuse and has no enumerated reason.

5. The plan makes the one-hop bound machine-visible through a check_depth field on the authorization outcome. Does a field on the result prevent a consumer from reading a permitted one-hop result as an independence finding, or does it only give the system somewhere to point afterwards? Construct a two-hop case the check misses and say whether check_depth is sufficient disclosure for that case.

6. Slice C classifies invocations as governed or experimental and refuses no execution. The enforcement matrix records C6 authority separation as "adopted, not currently evidenced" with current evidence "none (no current record names the check)". Would this slice let that row cite something real, or would it only let the matrix cite a record that names a check without performing one? Argue from the text below.

7. Which of the ten success criteria are mechanically checkable as written, and which are not? Address specifically: the audit criterion, which supplies no procedure, command, or semantics for verified_current; the cross-environment reproduction criterion, which names no environments, build inputs, or normalization rules; the coverage criterion; and criterion 4's "demonstrated against a real captured InvocationRecord", which names no record and gives no acceptance rule for "real". Name any missing check.

8. Which decisions in this slice constrain later evidence admission and lineage work, and which of them would be expensive to reverse once records exist?

9. Recommendation: admit as written, admit with named conditions (state them), or revise first. If you recommend admission while judging reading (b) of question 1 correct, state explicitly what the admission concedes.

Do not certify or praise. No provider product recommendations.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

Review the plan below for admission, together with the ontology amendment it depends on. Full texts are included; do not rely on repository access, and quote only text that appears below. If something you need is not present, say so rather than inferring it.

Status of what you are reading: the ABS-0004 v7 amendment is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force yet, and this round is the admission checkpoint for both.

One disclosure, because the plan text refers to it and withholding it would be dishonest rather than isolating: v7 replaces a v6 rule that claimed to prevent the authorization regress from being closed by convenience, after two reviewers in a prior round independently defeated it. The plan's rationale characterises that break. Do not accept the plan's characterisation, and do not treat the prior break as the only one available. Where a question asks you to construct an abuse, construct it from the text below. If you judge that this disclosure has shaped your answer, say where.

=== ABS-0004 v7 SECTION 3 (three decisions, P7, authorization-chain termination) ===
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

`[PRINCIPLE]` P7. Root authority is extra-systemic. An authorization chain
terminates at a standing authority that the system records and does not
establish. Who is accountable for AI-Lab is a fact about the world, about
who controls the repository and answers for it, and no arrangement of
records inside the repository can make that fact true or verify it. Any
design that appears to derive root authority from internal evidence has
merely moved the regress and disguised it.

`[DEF]` Authorization-chain termination. A chain terminates at an
AccountablePrincipal's standing authority within a declared
`authority_scope`. Authorizations the principal issues inside that scope
are self-standing. Every other authorization must chain, through one or
more steps, to such a standing authority. An authorization that chains to
nothing is not thereby permitted: it is unauthorized.

`[ADOPTED_CONSTRAINT]` A standing-authority claim is recorded, never
verified. AI-Lab does not validate that a declared principal is entitled to
the authority it claims; it has no means to do so, and pretending otherwise
would be the overclaim P6 forbids. What the record provides is visibility:
the claim, its declared scope, and every authorization resting on it are
legible and attributable. Visibility is the whole of what this constraint
achieves, and it is not prevention.

`[ADOPTED_CONSTRAINT]` Scope breadth is visible, not bounded by fiat. A
declared `authority_scope` may be arbitrarily wide, including universal. A
wide scope is permitted and must be legible as wide; it may not be
described, in a record or in a summary, as bounded merely because a scope
field was populated. A boundary that no one can fail to satisfy is not a
boundary, and calling it one is the defect this constraint exists to
prevent.

`[ADOPTED_CONSTRAINT]` Self-issued authorization is marked, never silently
accepted. Where the issuing principal and the authorized executor are the
same party, or where a principal issues an authorization covering an
invocation it also performs, the authorization records `self_issued: true`.
A self-issued authorization is not refused: at the root of any chain, the
accountable party necessarily authorizes work it is also responsible for.
It is instead disqualified from counting as independent authorization
wherever independence is required, and it is countable as such.

`[DEF]` Standing authority is not a capability of executors. A model, tool,
or human acting as an executor never holds standing authority by virtue of
executing; it holds it only as an AccountablePrincipal within a declared
scope, which is a separate role under Section 4.13. One party may hold both
roles; the ontology separates the roles, not the parties, and the
`self_issued` marking is how the coincidence is recorded rather than
denied.

`[OPEN]` Whether standing authority requires periodic re-declaration or
review. COMP-0037 established what v6 got wrong here: both reviewers
independently constructed the same self-authorization path, and v6's claim
to prevent convenient closure of the regress was false. v7 does not close
the question by asserting a stronger internal control; it records that no
internal control can close it, and asks instead what external evidence a
scope declaration should carry.

=== ABS-0004 v7 SECTION 4.6-4.7 (qualification, executors) ===
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

=== ABS-0004 v7 SECTION 4.9 (RoleDefinition) ===
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

=== ABS-0004 v7 SECTION 4.13 (DecisionRecord, AccountablePrincipal) ===
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

=== ABS-0004 v7 SECTION 8 (consequence classes) ===
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

=== ABS-0004 v7 SECTION 9 (enforcement matrix) ===
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

=== ABS-0004 v7 CONSTRAINTS C3 AND C6 (from Section 6) ===
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

=== PLAN-20260723-0002 ===
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

=== QUESTIONS ===
1. The central question of this round. v6 claimed to prevent convenient closure of the authorization regress; v7 withdraws that claim and asserts only visibility: a standing-authority claim is recorded and never verified, a declared authority_scope may be arbitrarily wide including universal, and a self-issued authorization is marked and disqualified from independence rather than refused. Two readings are available. (a) This is the honest terminus: no arrangement of internal records can establish extra-systemic authority, so any mechanical scope bound would be theatre, and saying so plainly is the most the system can truthfully do. (b) This is capitulation: the constraint existed to bound the root, and permitting a universal scope while requiring only that it be legible as wide converts a control into a label. Argue for one reading. State what construction or evidence would distinguish them, so the disagreement is decidable rather than a matter of taste.

2. v7 was written to retract an overclaim. Does it contain a new one? Read its adopted constraints as written and name any sentence that claims more than the record can support - including any place where the retraction itself is overstated, or where visibility is asserted as achieved when the mechanism described would not achieve it.

3. Attack v7 independently. Construct a path by which an executor or principal obtains effective authority, or by which the record misrepresents who authorized what, while satisfying every sentence of Section 3 as written. If the self_issued marking together with the disqualification-from-independence rule blocks your construction, report that plainly rather than forcing an attack.

4. The plan enumerates ten refusal reasons. Are they complete for the meaning of "valid authorization" the plan adopts? Note that the plan does not state whether Section 4.7's disclosure constraints - undisclosed material subordinate execution, undeclared execution-path-changing tool configuration, undeclared material external interaction - are checked here, excluded from the meaning of valid authorization, or deferred. Name the disposition the plan should state, and any further case that should refuse and has no enumerated reason.

5. The plan makes the one-hop bound machine-visible through a check_depth field on the authorization outcome. Does a field on the result prevent a consumer from reading a permitted one-hop result as an independence finding, or does it only give the system somewhere to point afterwards? Construct a two-hop case the check misses and say whether check_depth is sufficient disclosure for that case.

6. Slice C classifies invocations as governed or experimental and refuses no execution. The enforcement matrix records C6 authority separation as "adopted, not currently evidenced" with current evidence "none (no current record names the check)". Would this slice let that row cite something real, or would it only let the matrix cite a record that names a check without performing one? Argue from the text below.

7. Which of the ten success criteria are mechanically checkable as written, and which are not? Address specifically: the audit criterion, which supplies no procedure, command, or semantics for verified_current; the cross-environment reproduction criterion, which names no environments, build inputs, or normalization rules; the coverage criterion; and criterion 4's "demonstrated against a real captured InvocationRecord", which names no record and gives no acceptance rule for "real". Name any missing check.

8. Which decisions in this slice constrain later evidence admission and lineage work, and which of them would be expensive to reverse once records exist?

9. Recommendation: admit as written, admit with named conditions (state them), or revise first. If you recommend admission while judging reading (b) of question 1 correct, state explicitly what the admission concedes.

Do not certify or praise. No provider product recommendations.

## OpenAI Response

- model: `gpt-5.6-terra`

```
## 1. Reading of v7’s authorization terminus

I favor reading **(a), but narrowly**: v7 is correct that internal records cannot establish the real-world fact of who has root authority. P7 says that root authority is “extra-systemic,” and that no internal arrangement can “make that fact true or verify it.” A repository record can represent a claim, its scope, and the authorizations said to rest on it; it cannot transform an unauthorized claimant into an accountable authority.

That does **not** mean v7 supplies a preventive root-authority control. It expressly says that visibility “is not prevention,” permits an arbitrarily wide scope “including universal,” and permits self-issued authorization. Thus v7 is an honest terminus only if its claimed result is limited to attributable recording, not bounded or independently established authority.

Reading (b) becomes correct if “the constraint” is evaluated as a control intended to prevent an arbitrary party from obtaining system-recognized authority. On that measure, a universal unverified declaration is not a bound. It is a label attached to an unbounded claim.

This can be made decidable by separating two proposed success claims:

* **Traceability claim:** From stored records, an auditor can identify the claimed principal, declared scope, every authorization in the chain, whether the scope is universal, and whether an authorization is self-issued.
* **Authority-control claim:** An unauthorized real-world party cannot obtain system-recognized authority merely by creating records.

The first can be tested by constructing complete and incomplete authorization chains and checking whether the records expose their root claim, scope, and self-issue status. The second is falsified by a false or unaccountable claimant recording a universal standing authority and then issuing an authorization that the system accepts. The supplied text says AI-Lab cannot verify the claimant’s real entitlement, so v7 cannot establish the second claim.

Accordingly, v7 may be admitted only as an ontology of visible claims and authorization-chain attribution, not as a mechanism that bounds root authority or prevents false root claims.

## 2. New or retained overclaims in v7

Several sentences claim more than the described mechanism establishes.

1. **“What the record provides is visibility: the claim, its declared scope, and every authorization resting on it are legible and attributable.”**

   The text requires that a standing-authority claim be recorded, but it does not, in the supplied sections, specify a complete chain-discovery mechanism, a required index, an integrity mechanism, a traversal rule, or a requirement that every authorization actually be recorded and linked. Without those, “every authorization resting on it” being legible is not established.

2. **“Visibility is the whole of what this constraint achieves.”**

   This is too categorical. The stated constraints may achieve some schema-level requirements—such as requiring a scope declaration and, in specified cases, `self_issued: true`—but whether they achieve visibility depends on implementation, record completeness, identity resolution, and usable linkage. The amendment does not establish those conditions.

3. **“A wide scope is permitted and must be legible as wide.”**

   The ontology says a scope is declared, but supplies no scope grammar, canonical rendering rule, or validation rule that would make “universal” or an equivalently broad expression mechanically legible. A scope field can be populated while still being ambiguous, malformed, or operationally uninterpretable.

4. **“Where the issuing principal and the authorized executor are the same party … the authorization records `self_issued: true`.”**

   This is a normative requirement, but its reliable achievement depends on determining “the same party.” The amendment later recognizes that one party may hold both roles, but the supplied ontology does not provide party-resolution semantics across `AccountablePrincipal` and executor identities. Without such semantics, the record cannot reliably know when the marking is required.

5. **“A self-issued authorization is not refused … It is instead disqualified from counting as independent authorization wherever independence is required.”**

   This is only supportable if every use that requires independence actually invokes a check that recognizes self-issue and rejects it as independent. The amendment states the intended semantic consequence, but it does not itself supply the decision procedure, required record field for every relevant relation, or enforcement point.

6. **“At the root of any chain, the accountable party necessarily authorizes work it is also responsible for.”**

   “Necessarily” is too strong as stated. A root accountable party could delegate issuance to another party, or the records could represent issuance by another principal under a root claim. Responsibility and issuance need not coincide in every root-chain arrangement described by the text.

The central retraction—AI-Lab cannot verify extra-systemic standing authority—is not itself an overclaim. The overreach is in moving from “the system records a claim” to assertions that complete, legible, and attributable visibility has thereby been achieved.

## 3. Independent attack on v7

A construction satisfying Section 3 can give an unaccountable party effective system-recognized authority.

1. Party X creates or causes the creation of an `AccountablePrincipal` record asserting standing authority.
2. The record declares `authority_scope` as universal.
3. X issues an authorization within that declared scope.
4. X, or an executor controlled by X, performs the authorized invocation.
5. If X is also the authorized executor, the authorization records `self_issued: true`.
6. No decision in this path requires independent authorization unless some other rule specifically requires independence.

This satisfies the Section 3 statements:

* The standing-authority claim is recorded, not verified.
* Universal scope is permitted.
* The authorization chain terminates at the declared standing authority.
* The self-issued authorization is marked rather than refused.
* The self-issued authorization is disqualified only from counting as independent authorization where independence is required.

The resulting authority is not established as legitimate in the world. But it is effective for the system’s own authorization classification because the system accepts the declared root claim as the termination point and does not verify it.

A second version misrepresents who authorized what without violating the stated Section 3 rules: X uses a pseudonymous operator identity as the `AccountablePrincipal`, declares universal scope, and accurately records that pseudonymous principal as issuer. The record is attributable to that identifier, but not necessarily to the real-world person or organization that actually controls it. Section 3 expressly says no personal identifying data are required elsewhere in the amendment, and P7 says the system cannot verify the extra-systemic fact.

The self-issued marking does not block either construction. It blocks counting that authorization as independent where independence is required; it does not block authorization or governed classification generally.

## 4. Completeness of the ten refusal reasons

The ten reasons are not complete for the plan’s stated meaning of a valid authorization.

Most importantly, the plan leaves Section 4.7’s adopted disclosure constraints unresolved. It does not say whether valid authorization requires checking:

* undisclosed material subordinate execution;
* undeclared execution-path-changing tool configuration; or
* undeclared material external interaction.

The plan should state one of the following dispositions explicitly:

1. **Enforced in Slice C:** missing or nonconforming disclosure makes the authorization invalid and yields a named refusal reason; or
2. **Deferred and excluded from Slice C validity:** Slice C’s “valid authorization” is expressly not a determination of compliance with those Section 4.7 constraints, and a governed classification must not be represented as satisfying them.

The first is more consistent with saying field names and semantics follow v7 “exactly,” but it requires capabilities not described in the plan: material-subordinate discovery, effective-input manifests, and `OutboundInteractionLog` evidence. The plan currently does not specify those checks. If they are deferred, then “governed” in Slice C must be qualified as governed only with respect to the narrower authorization-record checks.

At least these additional refusal cases need a disposition and, where applicable, a named reason:

* **Independence requirement unmet.** `InvocationAuthorization` carries “independence requirements,” and self-issued authorization is disqualified wherever independence is required. The plan tests that self-issued authorization is “reported as not independent,” but it does not enumerate refusal of an authorization whose stated independence requirement is not met.
* **Identity or equivalence unresolved where independence is required.** C3 says that unresolved equivalence “cannot establish identity independence” and produces `independence_unresolved`, not an independent path. The plan’s exact-identifier comparison does not state what occurs where identity equivalence is unresolved.
* **C6 exercise conflict.** C6 prohibits an invocation from exercising adjudicator-level epistemic authority and above-`read_only` action authority against the same target without an independent verification edge. The ten reasons include self-adjudication, but not this authority-separation conflict.
* **Invalid or unsupported authority-chain reference.** “Unterminated authorization chain” is not necessarily the same as a chain whose reference is malformed, points to an authorization that does not authorize the next link, or forms a cycle. “A record it relies on is inactive or superseded” covers one portion, but not all linkage validity.
* **Required DecisionRecord fields absent or inconsistent.** The plan mentions field reconciliation, but its refusal list does not clearly cover inconsistency between issuing principal, issuer invocation, accountable approver, policy authority, and the claimed standing or chained authority.

“Authorization conditions unmet, malformed, or absent” is unusually broad and may conceal several materially distinct failures. It could be retained as a general record-validity reason, but the plan should not use it to hide independence, disclosure, chain-integrity, or C6 failures that have distinct governance meanings.

## 5. One-hop `check_depth`

A result field does not prevent overreading. It gives the system somewhere to point after a consumer has overread the result. Prevention would require consumers to be required to interpret a permitted result as direct-only, or a separate status that prohibits treating it as an independence finding.

A two-hop case:

1. Model executor M produces material content.
2. A tool invocation T incorporates that content into artifact A and is recorded as the artifact’s direct `produced_by` invocation.
3. T’s invocation is linked to M’s invocation through `spawned`, or M otherwise appears in the artifact’s ancestry.
4. M is then proposed as the adjudicator for A.
5. The one-hop check compares M to T, finds unequal executor identities, and permits the authorization.
6. The deeper ancestry contains M, so a full C3 analysis should find the conflict.

This can be fully disclosed rather than hidden: the subordinate model invocation can be represented and linked as Section 4.7 requires. The failure is not hidden composition; it is the declared but untraversed second hop.

`check_depth: direct` is useful disclosure only for a consumer that actually reads and honors it. It is not sufficient to support the plan’s stronger phrasing that a consumer “cannot read a permitted result as a general independence finding.” A consumer can do exactly that unless the output schema, admission rules, or downstream validators make such an interpretation invalid.

The result should instead carry a status such as direct-conflict-checked only, together with an explicit nonfinding: no lineage-independence determination was made. Later evidence-admission rules should be forbidden from treating the result as C3 compliance or as an independence finding.

## 6. Whether Slice C evidences C6

As written, Slice C would create records relevant to C6, but it would not establish that C6 is being checked or enforced.

C6 has two material components:

1. epistemic, action, and accountable authority are assigned independently; and
2. adjudicator-level epistemic authority and above-`read_only` action authority may not both be exercised within one invocation against the same target unless covered by an independent verification edge.

The plan creates role definitions with three axes and creates authorization records. That can document how authority was assigned. It can therefore give the matrix artifacts to cite for assignments.

But the plan’s listed authorization behavior does not include a C6 validator. The refusal reasons do not include exercising both adjudication and above-`read_only` action authority against the same target without an independent verification edge. Its one-hop check addresses a direct C3 self-adjudication case, not the broader C6 exercise rule. Further, the plan refuses no execution, and does not describe capturing the action-authority exercise needed to determine whether C6 was violated in an invocation.

Therefore, the plan could at most change the evidence from “none” to records that name roles and authorizations. It would not justify claiming that C6 is evidenced as a performed check. The matrix’s intended target is an “artifact validator”; this plan does not specify that validator for C6.

## 7. Mechanical checkability of success criteria

### Mechanically checkable, subject to defined test fixtures

1. **Governed versus experimental fixture classification.**  
   This is mechanically testable for the supplied fixtures, assuming “valid authorization” is made determinate.

2. **Each enumerated refusal reason is exercised by a fixture.**  
   This is mechanically testable for the ten named fixtures. The statement that “no fixture path returns a permitted outcome without a matching authorization record” is also testable for the fixture set, not as a universal code property.

3. **Unterminated chain and out-of-scope standing authority each refuse.**  
   Mechanically testable with fixtures, assuming chain and scope semantics are defined.

6. **Qualification execution-scope rejection and nontransfer.**  
   Mechanically testable if endpoint and ExecutionProfile matching semantics are defined.

8. **Byte-identical Slice A and Slice B fixture outputs before and after importability.**  
   Mechanically testable for the named stored records and the chosen execution environment. It does not establish that every Slice A or Slice B behavior is unchanged.

### Only partly mechanically checkable, or not checkable as written

4. **One-hop self-adjudication criterion.**  
   The same-identity, different-identity, and `check_depth` portions are mechanically testable with specified records. But “demonstrated against a real captured InvocationRecord” is not checkable as written: no InvocationRecord is named, and no rule says what makes a record “real” rather than a test fixture.

5. **Consequence classification criterion.**  
   The fixture idea is mechanically testable only after missing semantics are supplied. Section 8 names classes and modifiers, but its “Detailed classification function” is open. The text does not provide the modifier levels or a complete target-type-to-default mapping. Therefore a fixture cannot presently determine the expected maximum in every named case. The downward-adjustment test also needs a defined representation of a governed exception and its review condition.

7. **Self-issued authorization criterion.**  
   Acceptance and `self_issued: true` can be tested if party sameness is defined. “Reported as not independent by any check that asks for independent authorization” is not fully checkable because “any check” is not an enumerated interface or finite set.

9. **Every public entrypoint and every enumerated outcome are covered; full suite passes offline.**  
   “Full suite passes offline” is mechanically checkable in a specified environment. “Every public entrypoint” and “covered” are not, because the plan supplies no definition of public entrypoint, coverage tool, coverage threshold, or exclusion policy.

10. **Audit and cross-environment reproduction.**  
   This is not mechanically checkable as written.

   * “The repository audit reports `ok true verified_current`” supplies no audit procedure, command, record format, or semantics for `verified_current`.
   * “Cross-environment reproduction” names no environments, build inputs, dependency-resolution rules, operating-system constraints, timestamps, locale rules, path normalization, serialization normalization, or checksum algorithm.
   * “Public repository” is referenced, but no acceptance procedure is supplied in the text.

### Missing checks

The success criteria also omit tests for:

* the declared disposition of all Section 4.7 disclosure constraints;
* C6’s same-target adjudication-plus-action prohibition;
* `independence_unresolved` behavior where independence is required;
* scope-language parsing and universal-scope representation;
* authorization-chain cycles and invalid intermediate delegation;
* pure-function behavior: “no I/O, no clock, no network” is a constraint but no test method is given;
* the requirement that every relation use `GraphRelation` and no predicate fall outside the registered lists, because neither the relation shape nor the lists are supplied here;
* DecisionRecord inherited-field reconciliation beyond documentation;
* the assertion that self-issued marking is correctly detected across the relevant identity kinds.

## 8. Decisions that constrain later admission and lineage work

The following Slice C decisions are load-bearing for later evidence admission and lineage work:

* **Role vocabulary and three-axis model.**  
  `task_function`, `epistemic_authority`, and `action_authority` determine how later admission rules distinguish witness, advisor, adjudicator, read-only, repository-mutating, and external-actuator work.

* **RoleDefinition constraint fields.**  
  In particular, `required independence`, `required_verified_properties`, `may_assign_epistemic_status`, `requires_external_verification`, and consequence ceilings will constrain what later evidence admission can accept.

* **Execution-scoped qualification.**  
  Endpoint, ExecutionProfile, session-state, policy-version, and evidence semantics determine whether a later verifier or adjudicator was qualified in the relevant execution context.

* **AccountablePrincipal and authority-chain model.**  
  Principal identifiers, principal kinds, scopes, delegation references, chain termination, and self-issued semantics become the basis for attribution of later admission decisions.

* **DecisionRecord field reconciliation.**  
  The relation among issuer invocation, issuing principal, accountable approver, policy authority, activation state, and supersession will govern later claims about who recommended, approved, or activated an evidence-admission decision.

* **Consequence classification.**  
  The ordinal classes, target-type defaults, modifier semantics, and downward-exception records will influence the level of verification later required for plan admission and evidence admission.

* **Definition of governed versus experimental.**  
  If “governed” is attached to an invocation merely because a narrow authorization record covers it, later consumers may mistake it for a broader provenance, disclosure, C3, C6, or evidence-admission finding.

* **Identity and direct-lineage handling.**  
  The selected use of `produced_by`, `executed_by`, exact equality, and direct-only checking will affect later lineage traversal and independence determinations.

* **Predicate choices.**  
  `assigned_role`, `authorized_by`, `authorizes`, `qualifies_executor`, `qualifies_for`, `issued_under`, `based_on`, and `approved_by` become persistent graph vocabulary.

The most expensive decisions to reverse after records exist are identity semantics, principal identifiers, scope semantics, chain-link semantics, DecisionRecord field meanings, role identifiers and vocabularies, consequence classes, and predicate meanings. Those choices affect canonical serialization, record identity, paths, existing qualifications, existing authorization chains, and future lineage traversal. A later change may require migration rather than merely changing validation code.

## 9. Recommendation: revise first

I recommend **revise first** for both the amendment and the plan.

The amendment should be revised to remove or qualify claims that visibility has been achieved merely because claims and fields are recorded. It should say that visibility is a design objective contingent on complete, linked, interpretable records and that the ontology does not establish completeness, identity resolution, or real-world authority.

The plan should be revised to include at least these named conditions before admission:

1. State whether Section 4.7 disclosure constraints are enforced in Slice C or deferred and excluded from Slice C validity; if deferred, prohibit “governed” from implying compliance with them.
2. Add named handling for unmet independence requirements and unresolved identity equivalence where independence is required.
3. Add C6 checking or explicitly state that Slice C does not evidence C6 compliance and cannot change the matrix’s “Current enforcement evidence” from none to a performed control.
4. Define scope matching, universal-scope representation, delegation-chain validity, and cycle handling.
5. Define how issuer invocation, issuing principal, accountable approver, and self-issued party sameness are reconciled and validated.
6. Replace the claim that `check_depth` prevents overreading with a direct-only nonfinding status and downstream prohibition on treating it as lineage independence.
7. Supply acceptance procedures for “real captured InvocationRecord,” `verified_current`, repository audit, public-repository reproduction, environments, build inputs, normalization, checksums, public entrypoints, and coverage.
8. Supply the missing consequence-classification mappings and governed-exception representation needed to test criterion 5.
9. Add tests or a stated deferral for purity, relation-shape compliance, registered-predicate compliance, Section 4.7 disclosure, C6, identity-unresolved cases, chain cycles, and invalid chain links.

If admission were nevertheless granted while accepting reading (b), it would concede that the admitted amendment does **not** bound root authority: it would authorize a system that records and labels an unverified, potentially universal root claim, while providing no prevention against that claim being made by a party without the real-world authority it asserts.

The disclosure affected my answer only in the historical framing of questions 1 and 9: I treated the supplied description of v6 as a reason to scrutinize whether v7 reintroduced overclaim through “visibility,” rather than accepting the plan’s characterization of the prior break. The attack in question 3 is constructed from the supplied v7 text, not from an assumed prior-v6 path.
```

## Claude Response

- model: `claude-sonnet-5`

```

```

---

## Addendum: incident record — incomplete round

This addendum is part of the artifact. It exists because the artifact could not
otherwise explain its own contents, which is the same defect COMP-0032 recorded
at a lower token limit.

### Round validity

**This round has one complete witness, not two.** The `claude-sonnet-5` section
above is empty. It is not a review, it is not a finding of no objection, and
nothing in this artifact may be cited as independent corroboration or as a
two-witness result.

- Complete witness: `gpt-5.6-terra`, invocation `INV-83db700fbe901487`,
  recommendation revise-first.
- Empty response: `claude-sonnet-5`, invocation `INV-b59b93ec9cd8dbe6`.

### What happened

The `claude-sonnet-5` call returned successfully over HTTP and produced no text
block. The API consumed the entire output budget generating reasoning tokens and
never emitted a response. Reproduced twice against a prompt whose sha256 matches
`INV-b59b93ec9cd8dbe6.effective_input_manifest.rendered_prompt_digest`
(`74c8dd0e16180d8df7ece2c79c91ee246cddafce0abb9ef6b0e8a737088d1ddf`):

| configuration | stop_reason | output_tokens | content blocks | text |
| --- | --- | --- | --- | --- |
| effort unset (API default high), max_tokens 16000 | `max_tokens` | 16000 (= limit) | one `thinking`, empty | none |
| effort unset, max_tokens 21000 | `max_tokens` | 21000 (= limit) | `thinking` + `text` | 17039 chars, truncated |

The thinking block carried no visible content, so inspecting response content
cannot distinguish this from a genuinely empty completion. The only discriminating
signals are `stop_reason` and `output_tokens`.

Raising the limit does not fix this on the current path. At `max_tokens` 32000 the
SDK refuses before dispatch: *"Streaming is required for operations that may take
longer than 10 minutes."* That is a client-side duration guard, not a token
ceiling, so no value of `max_tokens` resolves it without a streaming adapter.

### What the record asserts, and cannot assert

`INV-b59b93ec9cd8dbe6` records `status: success`. Compared field-for-field
against `INV-c9fecfbf0964c1d2` — the COMP-0037 `claude-sonnet-5` invocation that
produced a complete review — the two records are **identical** on `status`,
`governance_marker`, `execution_profile`, and `spawned`. They differ only in
`invocation_id`, `occurred_at`, `session_id`, and the input digest.

`INVOCATION_STATUSES` admits only `success` and `failure`. The schema has no value
for an invocation that returned without exception and produced nothing, so the
record was obliged to assert something false. No field carries `stop_reason` or
output-token count.

Separately, `execution_profile` records *supplied* configuration rather than
*effective* configuration. `reasoning_parameters` is `{}` — accurate, since no
effort was sent — but the record therefore cannot show that the call ran at the
provider's default effort of high, which is the parameter that explains the
outcome.

### Contributing cause: prompt size

The prompt was 60.5% larger than COMP-0037's (294 → 391 lines; ~7,800 → 12,496
input tokens). COMP-0037's `claude-sonnet-5` call completed under the same
16000-token limit and the same default effort. The additional material — Section
9 and constraints C3/C6 — was substantively used by the surviving reviewer, but
the drafting executor did not check output headroom before the round, in a session
in which the prior truncation incident recorded in `ai_lab/providers/settings.py`
had been read.

### Witness asymmetry, pre-existing

`output_token_limit` was 16000 for `claude-sonnet-5` (`max_tokens_source:
settings_default`) and `null` for `gpt-5.6-terra` (`max_tokens_source:
provider_default_unset`). AI-Lab caps one witness and not the other. Whatever
default the OpenAI endpoint applies is not recorded, so these records cannot
establish that the two witnesses had comparable room to answer. The same asymmetry
is present in COMP-0037's records and is disclosed in neither.

### Uncaptured diagnostic invocations

Diagnosis required provider calls made outside `scripts/compare_providers.py`.
These produced **no InvocationRecord** and are absent from the provenance graph.
Disclosed rather than omitted:

- reproduction probe: tiny prompt, and the full prompt at 16000
- configuration ladder: `max_tokens` 32000 (SDK refusal, no tokens billed), and
  one further rung
- pre-flight of the largest atomic prompt at current defaults

Their outputs were not retained. In particular the 17039-character truncated
response was discarded rather than read as a review: the response was cut off in
question order, and the questions it did not reach include the recommendation.

### Disposition

Superseded by the atomic round recorded under
`docs/comparisons/comp0039/MANIFEST.json`, which asks each question in its own
invocation with its own declared evidence set. The `gpt-5.6-terra` review above is
retained as evidence and its findings remain live, but this artifact carries no
two-witness verdict and no adjudication rests on it.
