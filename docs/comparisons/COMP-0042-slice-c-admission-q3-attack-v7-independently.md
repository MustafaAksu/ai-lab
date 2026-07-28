# COMP-0042: Provider Comparison — Slice C admission Q3 attack-v7-independently

## Metadata

- comparison_id: `COMP-0042`
- title: `Slice C admission Q3 attack-v7-independently`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-eaa6bda0606982af.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0042", "target_id": "INV-eaa6bda0606982af"}, {"authoritative": false, "evidence": "docs/invocations/INV-00966c9ed3510c6d.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0042", "target_id": "INV-00966c9ed3510c6d"}]`
- created_at: `2026-07-28T18:48:40.305026+00:00`
- command: `scripts/compare_providers.py --title Slice C admission Q3 attack-v7-independently You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: the ABS-0004 v7 amendment is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force yet.

One disclosure, because the plan text refers to it and withholding it would be dishonest rather than isolating: v7 replaces a v6 rule that claimed to prevent the authorization regress from being closed by convenience, after two reviewers in a prior round independently defeated it. Do not accept the plan's characterisation of that break, and do not treat it as the only one available.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q3 ===
Construct a path by which an executor or principal obtains effective authority, or by which the record misrepresents who authorized what, while satisfying every sentence of Section 3 as written.

Build it from the attached text. If the self_issued marking together with the disqualification-from-independence rule blocks your construction, report that plainly rather than forcing an attack.

=== EVIDENCE ABS-0004:v7:S3 :: ABS-0004 v7 Section 3 (three decisions, P7, chain termination) ===
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

=== QUESTION Q3 ===
Construct a path by which an executor or principal obtains effective authority, or by which the record misrepresents who authorized what, while satisfying every sentence of Section 3 as written.

Build it from the attached text. If the self_issued marking together with the disqualification-from-independence rule blocks your construction, report that plainly rather than forcing an attack.

=== EVIDENCE ABS-0004:v7:S3 :: ABS-0004 v7 Section 3 (three decisions, P7, chain termination) ===
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

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
A path exists within the record system; it does not establish real-world root authority.

1. Party X creates an `AccountablePrincipal` record declaring X’s `authority_scope` as universal (or broad enough to cover the intended invocation).
2. X records a standing-authority claim for that principal. The claim is recorded rather than verified, and scope breadth may be arbitrarily wide.
3. X, acting as principal, issues an `InvocationAuthorization` for invocation I to X, acting as executor, within that declared scope.
4. The authorization is marked `self_issued: true`, because the issuing principal also performs the invocation.
5. The record identifies the decision as an invocation authorization and supplies the authorized executor, role, consequence class, policy, qualifications, independence requirements, and conditions.
6. X performs I.

On the ontology’s chain rule, that authorization terminates at X’s recorded standing authority and is therefore self-standing within the declared scope. The system does not validate whether X is actually entitled to that standing authority. Thus, a false or opportunistic standing-authority claim can yield effective authorization *in the repository’s authorization records* while leaving the real-world authority claim unverified.

The self-issued marking does not block this construction. It requires disclosure and disqualifies the authorization from counting as independent where independence is required. Section 3 does not impose an independence requirement on every invocation authorization. The path therefore works where no applicable authorization condition requires independent authorization. If such a condition does apply, the self-issued record cannot satisfy that independent-authorization condition.

This can also misrepresent who authorized what in the practically important sense that the record attributes the authorization to X’s standing authority even when X lacks that authority in the world. The record remains legible and attributable, but the stated constraint expressly makes visibility rather than prevention its effect.

Missing evidence: the applicable policy and any invocation-specific conditions or independence requirements are not provided. They would be needed to determine whether the particular planned invocation requires independent authorization and therefore defeats the self-issued path.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Constructed path

**Step 1 — Establish a self-declared, universal root.**
A single party declares itself an `AccountablePrincipal` with `authority_scope` set to universal. Section 3 explicitly permits this: *"A declared `authority_scope` may be arbitrarily wide, including universal. A wide scope is permitted and must be legible as wide."* The record shows the scope as universal, not disguised as bounded — satisfying that sentence exactly.

**Step 2 — Self-issue the InvocationAuthorization.**
The same party, acting as executor, is authorized by itself to perform the invocation. Section 3 requires this be marked: *"Where the issuing principal and the authorized executor are the same party... the authorization records `self_issued: true`."* The record does so. Section 3 also says this is expected, not forbidden: *"A self-issued authorization is not refused: at the root of any chain, the accountable party necessarily authorizes work it is also responsible for."*

**Step 3 — Never trigger the one operative check.**
The disqualification clause reads: *"It is instead disqualified from counting as independent authorization wherever independence is required."* This is conditional. `InvocationAuthorization` carries an `independence requirements` field (4.13), but nothing in Section 3 specifies who sets that field's content or which consequence classes must carry a nonzero independence requirement. Since the issuing principal is also the one populating its own authorization record, it can declare — truthfully, on the record — that no independence requirement applies to this consequence class. The disqualification clause then has nothing to bite: it disqualifies self-issuance *from independence*, but does not itself impose independence. Where none is declared required, the self-issued authorization is fully countable, standing authority under the chain-termination rule: *"Authorizations the principal issues inside that scope are self-standing."*

**Step 4 — Chain termination and P7 are satisfied, not violated.**
The record never claims to verify or establish the principal's standing authority — it only asserts it, per *"A standing-authority claim is recorded, never verified... Visibility is the whole of what this constraint achieves, and it is not prevention."* P7 is likewise satisfied rather than defeated: the record does not attempt to derive root authority from internal evidence; it simply records an extra-systemic claim, exactly as P7 contemplates.

**Result.** Every sentence of Section 3 is individually satisfiable while the same party (a) declares itself universally scoped, (b) authorizes its own execution, (c) is marked self-issued as required, and (d) faces no independence check because none was ever declared applicable — yielding unchecked effective authority over an arbitrarily wide domain, built entirely from compliant, honestly-marked records.

## Does the self_issued + disqualification rule block this?

**No — not as written.** The rule's force is entirely conditional on independence being "required," and Section 3 contains no provision establishing *when* independence is required for a given role or consequence class. That determination is pushed to "applicable policy" (named as a field in `InvocationAuthorization`, 4.13) and possibly to Section 4.7 (referenced but not included), neither of which is in evidence. The rule as given is a labeling requirement plus a conditional disqualifier; it is not itself a substantive independence mandate. So the construction is not forced through a defeat of the self_issued rule — it goes around it, using exactly the gap the rule leaves open.

## A second, weaker path (flagged as less certain)

The subordinate-authorization-inheritance `[DEF]` requires a parent authorization's conditions to "declare the permitted subordinate execution classes," but — unlike `authority_scope` — there is no sentence in Section 3 requiring that breadth to be "legible as wide" or barred from being described as narrow when it is not. A parent authorization could declare very broad subordinate execution classes inside ordinary "conditions" text without triggering any visibility obligation analogous to the scope-breadth constraint. This could let later subordinate invocations be recorded as authorized-by-inheritance in a way the original accountable approver did not meaningfully contemplate — a misrepresentation of who authorized what, though softer than the primary path since it depends on drafting, not a clean structural gap.

## What's missing from the evidence set

1. **The content of "applicable policy" / "independence requirements"** — whatever document specifies which consequence classes or roles mandate independent authorization. Without it, I cannot tell whether the primary path is available for *all* consequence classes or only some; I would use it to check whether high-consequence invocations are structurally forced to declare an independence requirement (which would close Step 3 for those cases while leaving it open elsewhere).
2. **Section 4.7** (disclosure violations), referenced by the subordinate-inheritance `[DEF]` — needed to know whether undeclared or overbroad subordinate class declarations carry any consequence, which bears on the second path.
3. **Any visibility/breadth constraint on subordinate execution classes** analogous to the `authority_scope` breadth constraint — its absence here is what makes the second path possible, but I cannot confirm it is truly absent from the full ontology rather than merely absent from this excerpt.
```
