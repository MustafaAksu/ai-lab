# COMP-0041: Provider Comparison — Slice C admission Q2 new-overclaim-in-v7

## Metadata

- comparison_id: `COMP-0041`
- title: `Slice C admission Q2 new-overclaim-in-v7`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-f8d5120327f1d564.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0041", "target_id": "INV-f8d5120327f1d564"}, {"authoritative": false, "evidence": "docs/invocations/INV-35815ed716886f1c.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0041", "target_id": "INV-35815ed716886f1c"}]`
- created_at: `2026-07-28T18:47:04.452127+00:00`
- command: `scripts/compare_providers.py --title Slice C admission Q2 new-overclaim-in-v7 You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: the ABS-0004 v7 amendment is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force yet.

One disclosure, because the plan text refers to it and withholding it would be dishonest rather than isolating: v7 replaces a v6 rule that claimed to prevent the authorization regress from being closed by convenience, after two reviewers in a prior round independently defeated it. Do not accept the plan's characterisation of that break, and do not treat it as the only one available.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q2 ===
v7 was written to retract an overclaim. Does it contain a new one?

Read its adopted constraints as written and name any sentence that claims more than the mechanism described can support. Include any place where the retraction itself is overstated, and any place where visibility is asserted as achieved when the mechanism described would not achieve it.

Quote the sentence you are objecting to, and say what the honest version would be.

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

=== QUESTION Q2 ===
v7 was written to retract an overclaim. Does it contain a new one?

Read its adopted constraints as written and name any sentence that claims more than the mechanism described can support. Include any place where the retraction itself is overstated, and any place where visibility is asserted as achieved when the mechanism described would not achieve it.

Quote the sentence you are objecting to, and say what the honest version would be.

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
The following sentences claim outcomes that the described record fields and rules do not, on the supplied text, establish.

1. **Visibility of the whole authorization dependency set**

> “What the record provides is visibility: the claim, its declared scope, and every authorization resting on it are legible and attributable.”

Section 4.13 supplies `authority_scope`, `delegation_reference`, and DecisionRecord fields, but it does not specify a required chain-link representation, completeness condition, traversal rule, or attribution rule that would ensure that **every** downstream authorization is recorded, discoverable, legible, and attributable. A record can expose what it contains; it cannot by itself establish completeness of what rests on a claim.

Honest version:

> “The record can make a declared claim and scope visible, and can make authorizations visible and attributable to the extent that they are recorded and linked. This text does not establish completeness of that visibility.”

The immediately following sentence therefore also overstates the achieved result:

> “Visibility is the whole of what this constraint achieves, and it is not prevention.”

The constraint as shown may prescribe recording and non-validation, but it does not demonstrate that visibility has been achieved. It should say that visibility is the intended and limited function, subject to complete and usable recording.

2. **Legibility of breadth and control of descriptions outside the field**

> “A wide scope is permitted and must be legible as wide; it may not be described, in a record or in a summary, as bounded merely because a scope field was populated.”

An `authority_scope` field can record a declaration, but the supplied text gives no scope language, interpretation rules, validation, rendering requirement, summary-generation rule, or review process that would make an arbitrarily wide declaration legible as wide. Nor is there a shown mechanism governing what a record or summary may say about that field.

Honest version:

> “A scope declaration should be recorded in a form that permits its breadth to be assessed; this section does not by itself ensure that records or summaries present an arbitrarily wide scope as wide.”

3. **The asserted effect of a `self_issued` mark**

> “It is instead disqualified from counting as independent authorization wherever independence is required, and it is countable as such.”

The shown mechanism records `self_issued: true`. Section 4.13 says that InvocationAuthorization carries “independence requirements,” but it does not state a validation, decision, or admission rule requiring a consumer of the record to reject a self-issued authorization when independence is required. A mark supports disclosure; it does not itself produce disqualification. Also, “countable as such” is ambiguous after “disqualified from counting as independent authorization”: it should specify whether it remains countable as an authorization while not countable as independent authorization.

Honest version:

> “A self-issued authorization must be marked. Where a receiving rule requires independent authorization, that rule should not count a marked self-issued authorization as independent; the authorization may still be recorded and counted as self-issued authorization.”

This sentence also gives an unsupported rationale:

> “A self-issued authorization is not refused: at the root of any chain, the accountable party necessarily authorizes work it is also responsible for.”

The definitions distinguish the AccountablePrincipal role from the executor role and expressly allow, but do not require, one party to hold both. An accountable principal can authorize an invocation performed by another executor. Responsibility for work is not the same thing as performing or self-authorizing it.

Honest version:

> “A root authorization may be self-issued when the accountable principal also performs the invocation, but root authorization need not be self-issued.”

4. **The absolute claim about AI-Lab’s means**

> “AI-Lab does not validate that a declared principal is entitled to the authority it claims; it has no means to do so, and pretending otherwise would be the overclaim P6 forbids.”

P7 supports the narrower proposition that repository arrangements cannot make the extra-systemic fact of root authority true or verify it. It does not, on the text supplied, establish that AI-Lab has **no means** at all—for example, no external investigation, institutional process, or evidence outside repository records. The reference to what “P6 forbids” cannot be assessed because P6 is not included.

Honest version:

> “AI-Lab does not validate entitlement to standing authority through the repository records described here. Those records cannot establish or verify the extra-systemic fact of root authority.”

To determine whether the P6 reference is accurate, **P6** is needed.

5. **The overstatement in the retraction**

> “v7 does not close the question by asserting a stronger internal control; it records that no internal control can close it, and asks instead what external evidence a scope declaration should carry.”

The first clause is a description of v7’s posture. The second converts the demonstrated failure of v6’s particular anti-regress rule into a universal impossibility claim: “no internal control can close it.” The supplied evidence shows that internal records cannot establish or verify the real-world fact of root authority, but it does not establish that no internal control can close every relevant authorization question, impose internal consequences, or require external evidence before a record receives a given status. Nor does the supplied text establish that the prior self-authorization path is the only possible failure mode.

Honest version:

> “v7 does not claim that its internal records establish root authority. The prior v6 control did not prevent the identified self-authorization path; whether, and for what limited purpose, internal controls combined with external evidence can constrain authorization remains open.”

The factual assertion in the same paragraph—

> “COMP-0037 established what v6 got wrong here: both reviewers independently constructed the same self-authorization path, and v6’s claim to prevent convenient closure of the regress was false.”

—cannot be independently assessed from the supplied evidence. **COMP-0037** and the relevant **v6 rule** are needed to assess what the reviewers constructed, what v6 actually claimed, and whether the description of that break is complete rather than selective.

Finally, this claim depends on an absent section:

> “Undeclared subordinate execution is a disclosure violation under 4.7, not an implicitly authorized act.”

The preceding sentence defines when subordinate authorization coverage applies, but the claimed classification as a “disclosure violation under 4.7” requires **Section 4.7**. It would be needed to determine whether that section actually imposes the stated violation, on whom, and with what consequence.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Overclaims in v7's adopted text

**1. The visibility claim in the standing-authority constraint overclaims completeness.**

> `[ADOPTED_CONSTRAINT]` "What the record provides is visibility: the claim, its declared scope, and every authorization resting on it are legible and attributable. Visibility is the whole of what this constraint achieves, and it is not prevention."

The mechanism actually described is: a claim is *recorded*, and a scope is *declared*. Nothing in this section (or in what's provided from Section 4.13) establishes a mechanism that guarantees "every authorization resting on it" is in fact legible and attributable. The chain-termination rule requires that non-root authorizations "must chain... to such a standing authority," but a requirement is not an enforcement mechanism, and the subordinate-inheritance rule concedes the gap directly: undeclared subordinate execution is merely "a disclosure violation under 4.7," not something the mechanism prevents or automatically surfaces. A violation that must be caught and disclosed by some other process is not the same as an authorization that "is legible and attributable" by virtue of this constraint. So "every authorization resting on it" is stated as an achieved property when the described mechanism only supports a weaker claim: authorizations that are correctly declared and not defeated by omission are legible.

Honest version: *"What the record provides is visibility for authorizations that are declared and correctly chained: the claim, its declared scope, and the authorizations that comply with disclosure requirements are legible and attributable. Undeclared or non-conforming authorizations are not made visible by this constraint; they depend on separate detection under 4.7."*

I'd want Section 4.7 (disclosure-violation handling) in evidence to check whether it actually closes this gap — if it does, the overclaim is smaller than I'm treating it; if it doesn't (e.g., if 4.7 is itself only a classification, not a detection mechanism), the overclaim stands as written.

**2. The retraction itself overclaims a general impossibility from a single defeated instance.**

> `[OPEN]` "v7 does not close the question by asserting a stronger internal control; it records that no internal control can close it, and asks instead what external evidence a scope declaration should carry."

The evidence given for this is COMP-0037: "both reviewers independently constructed the same self-authorization path, and v6's claim to prevent convenient closure of the regress was false." That shows one specific rule was defeated by one specific maneuver. It does not show — and nothing in the evidence set demonstrates — that *no possible internal control* could close the regress. The sentence converts a demonstrated failure of one rule into a flat universal claim ("no internal control can close it"), stated as something v7 "records," i.e., as settled, rather than as a hypothesis consistent with P7 but not established by the cited case. This is the same move the disclosure instructs me not to accept when the plan makes it; v7's own text makes it too.

Honest version: *"v7 does not assert a stronger internal control; the one control tried (v6) was defeated by two independent reviewers using the same path, and v7 does not know of an internal control that would survive that path. Whether some other internal control could close the regress is unresolved; P7 treats this as expected in principle, but that is a stated position, not something demonstrated by COMP-0037 alone."*

**Missing evidence I'd want:**
- **P6's actual text.** The standing-authority constraint says "pretending otherwise would be the overclaim P6 forbids" — I can't check whether this characterization of P6 is itself accurate without P6.
- **Section 4.7** (disclosure violations) — needed to know whether undeclared subordinate execution is actually detected/surfaced, which bears directly on whether the visibility claim in item 1 is closer to true than I've assessed.
- **COMP-0037 itself** (not just the summary sentence) — to check whether "two reviewers independently defeated it" supports only "this rule failed" or something closer to the broader claim v7 draws from it.
```
