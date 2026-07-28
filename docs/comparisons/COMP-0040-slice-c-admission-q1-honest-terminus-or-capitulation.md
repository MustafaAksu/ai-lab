# COMP-0040: Provider Comparison — Slice C admission Q1 honest-terminus-or-capitulation

## Metadata

- comparison_id: `COMP-0040`
- title: `Slice C admission Q1 honest-terminus-or-capitulation`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-56d31d5bfca54e6d.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0040", "target_id": "INV-56d31d5bfca54e6d"}, {"authoritative": false, "evidence": "docs/invocations/INV-50bc0e8f14b161d9.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0040", "target_id": "INV-50bc0e8f14b161d9"}]`
- created_at: `2026-07-28T18:45:31.877629+00:00`
- command: `scripts/compare_providers.py --title Slice C admission Q1 honest-terminus-or-capitulation You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: the ABS-0004 v7 amendment is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force yet.

One disclosure, because the plan text refers to it and withholding it would be dishonest rather than isolating: v7 replaces a v6 rule that claimed to prevent the authorization regress from being closed by convenience, after two reviewers in a prior round independently defeated it. Do not accept the plan's characterisation of that break, and do not treat it as the only one available.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q1 ===
v6 claimed to prevent convenient closure of the authorization regress. v7 withdraws that claim and asserts only visibility: a standing-authority claim is recorded and never verified, a declared authority_scope may be arbitrarily wide including universal, and a self-issued authorization is marked and disqualified from independence rather than refused.

Two readings are available.

(a) This is the honest terminus. No arrangement of internal records can establish extra-systemic authority, so any mechanical scope bound would be theatre, and saying so plainly is the most the system can truthfully do.

(b) This is capitulation. The constraint existed to bound the root, and permitting a universal scope while requiring only that it be legible as wide converts a control into a label.

Argue for one reading. Then state what construction or evidence would distinguish them, so the disagreement is decidable rather than a matter of taste.

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

=== QUESTION Q1 ===
v6 claimed to prevent convenient closure of the authorization regress. v7 withdraws that claim and asserts only visibility: a standing-authority claim is recorded and never verified, a declared authority_scope may be arbitrarily wide including universal, and a self-issued authorization is marked and disqualified from independence rather than refused.

Two readings are available.

(a) This is the honest terminus. No arrangement of internal records can establish extra-systemic authority, so any mechanical scope bound would be theatre, and saying so plainly is the most the system can truthfully do.

(b) This is capitulation. The constraint existed to bound the root, and permitting a universal scope while requiring only that it be legible as wide converts a control into a label.

Argue for one reading. Then state what construction or evidence would distinguish them, so the disagreement is decidable rather than a matter of taste.

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
I favor **(a)**, but only for the specific claim v6 purported to make: that an internal authorization structure can prevent convenient closure of the *extra-systemic* authorization regress.

Section 3 states the decisive premise: “Root authority is extra-systemic.” Whether a principal is actually entitled to govern AI-Lab is a fact about “who controls the repository and answers for it,” and the evidence says that no internal record arrangement can make or verify that fact. On that premise, a required non-universal scope, a fixed number of delegations, or a prohibition on self-issuance cannot establish that the root claimant has legitimate authority. It can only constrain the shape of records produced by a claimant.

The same applies to self-authorization. A rule refusing self-issued authorization cannot eliminate the root’s self-standing character; it can require the root to use another identity or another record path. Since a party may occupy both executor and AccountablePrincipal roles, the relevant truthful fact is the coincidence, which v7 records as `self_issued: true`. Where independence is required, v7 says that record is disqualified from counting as independent. That is a substantive limitation on an independence finding, even though it is not a test of root entitlement.

On this reading, permitting a universal `authority_scope` is not itself the terminus. The terminus is the explicit statement that a universal declaration does not become a real boundary merely because it is represented in a scope field. The operative result claimed by v7 is limited: attribution and legibility of the claim, its breadth, and the authorizations resting on it. It does not claim prevention.

That does not make (b) incoherent; it identifies a different objective. A system can mechanically reject universal scopes, reject self-issued records, or require a finite delegation chain. Such rules can bound which records the system accepts. They cannot, on the supplied evidence, establish that the accepted root is entitled to govern. Calling that latter effect prevention of the extra-systemic regress would be the error. Calling it a restriction on record admissibility or operational participation would be a different, potentially testable claim.

The readings can be distinguished by an explicit construction and a stated success condition:

1. **Paired-world construction for the regress claim.**  
   Construct two cases with identical repository records:
   - the same `AccountablePrincipal`,
   - the same `authority_scope`,
   - the same delegation and authorization chain,
   - the same `self_issued` markings, and
   - the same DecisionRecords.
   
   In one case, the recorded principal really is accountable in the world; in the other, it is not. If the internal rule reaches the same result in both cases, it cannot verify or establish the difference in actual root authority. This would support (a) for any claimed internal solution to the regress.

2. **Acceptance-language construction for (b)’s narrower control claim.**  
   Define an enforceable system rule such as: an InvocationAuthorization is ineffective unless its chain terminates in a scope satisfying specified limits, and universal scope is rejected. Then test whether records violating that condition can produce an `effective_status` permitting invocation or admission. If they cannot, the system has implemented a genuine internal acceptance bound. That would support (b) only if the disputed claim is “the system bounds what it will operationally accept,” not “the system establishes the root’s real authority.”

3. **External-evidence test for a non-theatrical scope declaration.**  
   The distinction ultimately turns on whether declared scope is compared to evidence outside the authorization chain. Section 3 itself leaves open “what external evidence a scope declaration should carry.” A decision rule would need to specify:
   - the external source or accountable process against which the declared scope is assessed;
   - who may assess it;
   - what constitutes sufficient evidence of the principal’s authority and scope;
   - what happens when that evidence is absent, contested, expired, or narrower than the declaration; and
   - whether the result affects only visibility, invocation authorization, evidence admission, or all of them.

The evidence set is sufficient to decide the conceptual point that internal records cannot establish the extra-systemic fact described in P7. It is insufficient to decide whether v7’s visibility-only approach is preferable to an operational scope-bound regime, because the following are absent:

- the v6 rule that allegedly prevented convenient closure, including its exact enforcement semantics;
- the two reviewers’ constructions in `COMP-0037`, needed to determine precisely what path defeated v6 and whether other failure modes remain;
- any definition of `authority_scope` semantics, including whether scopes are machine-evaluable;
- the policy rules governing when an InvocationAuthorization becomes effective or when an EvidenceAdmissionDecision may admit output;
- the external evidence model contemplated by the Section 3 open question; and
- a threat model and success criterion distinguishing prevention of false claims, prevention of unauthorized system actions, and mere disclosure of claims.

Without those materials, the defensible conclusion is narrow: v7 is correct not to represent its internal records as establishing root authority. Whether it has abandoned a useful operational control cannot be decided from the supplied text.
```

## Claude Response

- model: `claude-sonnet-5`

```
**Reading argued: (b), with a boundary on how far it extends**

The evidence does not support a single verdict across all three `[ADOPTED_CONSTRAINT]` clauses; it supports (a) for one of them and (b) for another, and the plan's move is to let the justification for the first cover the second without earning it.

Take the standing-authority claim first. P7 says: "Any design that appears to derive root authority from internal evidence has merely moved the regress and disguised it." Given that, the constraint that "A standing-authority claim is recorded, never verified" is correctly described as a terminus — there is no internal fact that could verify an extra-systemic entitlement, so refusing to pretend otherwise is honest, not weak. Reading (a) is right about *this* clause.

But the scope-breadth constraint is a different claim, and P7 does not entail it. "A declared `authority_scope` may be arbitrarily wide, including universal" is not a statement about what can be *verified* — it is a statement about what the system will *accept and act on*. Verifying that a claimed universal scope is true is indeed impossible; that says nothing about whether the system must accept a universal scope claim as usable. The constraint's own text concedes the target of the worry — "A boundary that no one can fail to satisfy is not a boundary, and calling it one is the defect this constraint exists to prevent" — and then prevents only the *mislabeling*, not the unbounded acceptance: "must be legible as wide" is the entire remedy. That is exactly reading (b)'s complaint: "permitting a universal scope while requiring only that it be legible as wide converts a control into a label."

The self-issued clause shows the alternative was available and was in fact taken elsewhere in the same section. There too, verification is refused ("not refused... instead disqualified from counting as independent authorization wherever independence is required"), but disqualification is a real downstream consequence, not a label — it changes what the record can be used for. Nothing in P7 forced v7 to stop at labeling for scope breadth; it could have attached an analogous consequence (e.g., a universal or unusually wide scope disqualified from serving as sole basis for some class of authorization, mirroring how self-issuance is disqualified from independence). That it didn't is a design choice, not an epistemic necessity, and the section offers no argument for the asymmetry.

The `[OPEN]` paragraph's justification for the retreat compounds this: it grounds the whole shift in COMP-0037, where "both reviewers independently constructed the same self-authorization path" — a fact about self-issuance, not about scope breadth. Generalizing from one defeated mechanism (attempted closure of the self-authorization path) to also abandon bounding of a distinct attribute (declared scope width) is an overreach the text asserts but does not demonstrate. Per the disclosure, this break should not be treated as the only one available or as controlling the plan's characterization; here it is being used to do more work than it can support — covering the scope-breadth retreat with a defeat that was actually about self-issuance.

So: (a) for the standing-authority-verification clause, (b) for the scope-breadth clause, and the plan's error is presenting v7 as a single honest terminus when it is actually two different moves bundled under one justification.

**What would make this decidable rather than a matter of taste**

Construct a candidate mechanical control on `authority_scope` breadth that (i) does not require verifying the extra-systemic entitlement claim (i.e., it operates only on record-internal facts: scope text, count of independent co-declaring principals, consequence class invoked, disqualification consequences), and (ii) actually narrows acceptance or downstream use rather than just requiring a label — e.g., "a universal or organization-wide scope is disqualified from independently satisfying independence requirements at the highest consequence class, in the same way self-issuance is disqualified" or "scope breadth above a threshold requires co-declaration by more than one AccountablePrincipal, recorded and disqualified from independence if it later collapses to one."

- If such a control can be specified without smuggling in a verification requirement, and it would do real work (change what a wide-scope authorization can be used for), then its absence in v7 is unexplained by P7, and (b) is confirmed for the scope-breadth clause.
- If every such candidate, on inspection, secretly reduces to needing to verify something extra-systemic (e.g., "independent co-declaration" is meaningless if the system cannot verify that the co-declaring principals are not the same accountable party under different labels — which is exactly the self-authorization path COMP-0037 found), then no mechanical bound on breadth is available either, and (a) is vindicated across the board.

That test is answerable from the ontology's own resources (does a proposed control require verification, yes/no) and does not depend on adjudicating intent.

**Evidence gaps**

- **COMP-0037 itself** is not in evidence, only the `[OPEN]` paragraph's summary of it. I would use the full record to check whether the two reviewers' self-authorization path also implicated scope breadth, or only self-issuance — this is load-bearing for the argument above and I only have the summary's characterization.
- **v6's actual rule text** is absent. Without it, I can't verify what mechanism v6 used or exactly what "prevent convenient closure" meant mechanically, which limits how precisely I can compare v6's failed control to what v7 could have kept.
- **Section 4.7** (disclosure violation) is referenced ("Undeclared subordinate execution is a disclosure violation under 4.7") but not included; it might bear on whether an undisclosed universal-scope claim would itself trigger a disclosure violation, which would be a form of mechanical consequence I haven't accounted for.
- **P1 and P6**, referenced but not quoted, would clarify the "overclaim P6 forbids" language used to justify non-verification, and P1's content (invoked for why InvocationAuthorization must exist) — needed to fully assess whether P6 forbids *only* claiming verification, or also forbids weaker mechanical bounds of the kind I proposed above.
- A definition of **"wherever independence is required"** is not in evidence; without knowing which decisions require independence, I can't assess how much real work the self-issued disqualification actually does, which weakens my contrast between it and the scope-breadth label.
```
