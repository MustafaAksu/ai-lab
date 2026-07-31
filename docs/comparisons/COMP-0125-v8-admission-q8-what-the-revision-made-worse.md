# COMP-0125: Provider Comparison — v8 admission Q8 what-the-revision-made-worse

## Metadata

- comparison_id: `COMP-0125`
- title: `v8 admission Q8 what-the-revision-made-worse`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-2033c066a496888e.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0125", "target_id": "INV-2033c066a496888e"}, {"authoritative": false, "evidence": "docs/invocations/INV-912a36f118ceb244.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0125", "target_id": "INV-912a36f118ceb244"}]`
- created_at: `2026-07-31T13:49:01.065746+00:00`
- command: `scripts/compare_providers.py --title v8 admission Q8 what-the-revision-made-worse You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q8 ===
Both documents were revised in response to a review. Revisions introduce defects of their own.

Name anything in v8's Section 3 or in the plan text below that is worse than what it replaced, or that is new and unsound. Consider in particular: text added to disclose a limitation that now reads as a rule; a correction that overshot; a sentence whose only function is to record that a previous sentence was wrong; and any place where the document now argues with itself in the reader's presence rather than simply saying what holds. If nothing is worse, say so and name the change you were most suspicious of.

=== EVIDENCE ABS-0004:v8:S3 (all blocks) ===
The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

Declared subordinate execution classes carry the same
breadth legibility as `authority_scope`. A broad declaration is permitted and
must be legible as broad; it may not be described, in a record or a summary,
as narrow because the field was populated. v7 imposed this on
`authority_scope` alone. The asymmetry was a drafting omission, not a
decision: nothing distinguishes the two cases, and a parent authorization
declaring very broad subordinate classes was subject to no visibility
obligation at all.

A disclosure violation under 4.7 is a classification,
not a detection. Nothing in this ontology detects that a subordinate
execution went undeclared. A violation is recorded when someone establishes
it by other means. No statement in this document or in any summary of it may
describe undeclared execution as surfaced, caught, or prevented by these
constraints.

P7. Root authority is extra-systemic. An authorization chain
terminates at a standing authority that the system records and does not
establish. Who is accountable for AI-Lab is a fact about the world, about
who controls the repository and answers for it, and no arrangement of
records inside the repository can make that fact true or verify it. Any
design that appears to derive root authority from internal evidence has
merely moved the regress and disguised it.

Authorization-chain termination. A chain terminates at an
AccountablePrincipal's standing authority within a declared
`authority_scope`. Authorizations the principal issues inside that scope
are self-standing. Every other authorization must chain, through one or
more steps, to such a standing authority. An authorization that chains to
nothing is not thereby permitted: it is unauthorized.

A standing-authority claim is recorded, never
verified. AI-Lab does not validate that a declared principal is entitled to
the authority it claims. No arrangement of records inside this repository can
establish that entitlement, and presenting a record as though it had would be
the overclaim P6 forbids.

That is a statement about repository records. It is not a claim that no means
of any kind exists: whether some external process could establish entitlement
is a separate question this ontology neither answers nor forecloses. v7 said
AI-Lab "has no means to do so", which asserted more than P7 supports.

What the record provides is visibility of the declared: the claim, its
declared scope, and those authorizations that are declared and correctly
chained are legible and attributable. It does not provide visibility of
authorizations that were never declared. Undeclared subordinate execution is
possible under this ontology — the inheritance rule above says so, and
classifies it as a 4.7 disclosure violation rather than detecting it. v7
claimed that "every authorization resting on it" is legible, which its own
Section 3 contradicted two paragraphs earlier.

Visibility of the declared is the whole of what this constraint is for, and it
is not prevention. Whether it is achieved is a further question this constraint
does not settle. No chain-link representation, completeness condition,
traversal rule, or attribution rule is specified anywhere in this ontology, so
nothing here establishes that the authorizations resting on a claim can in fact
be enumerated or followed. v7 asserted that visibility "is the whole of what
this constraint achieves"; achievement was never demonstrated, and the earlier
draft of v8 narrowed the scope of that assertion without withdrawing it. The
constraint states an intended and bounded function. Delivering it depends on
recording being complete and usable, which no rule in this document requires.

Scope breadth is visible, and breadth is not the
defect. A declared `authority_scope` may be arbitrarily wide, including
universal. A wide scope is permitted and must be legible as wide; it may not
be described, in a record or in a summary, as bounded merely because a scope
field was populated. A boundary that no one can fail to satisfy is not a
boundary, and calling it one is a defect P6 forbids.

The legibility requirement is unenforced, and saying so
is part of stating it. Nothing in this ontology supplies a scope grammar, an
interpretation rule, a validation step, a rendering requirement, or a rule
governing what a summary may say about a scope field. The requirement above
therefore binds whoever writes a record or a summary, and a violation is a
defect discoverable by reading rather than one caught by a check. This
constraint is included because the earlier draft of v8 corrected exactly this
overclaim in the standing-authority constraint and reproduced it here two
paragraphs later, which is the defect class P6 names and the third occurrence
of it inside this document.

What makes a scope declaration something other than self-assertion.
COMP-0037 defeated v6's scope rule from two directions, not one. One reviewer
declared a scope wide enough to cover the intended invocation; the other
declared one narrowly tailored to authorize exactly itself, observing that a
declaration so tailored "should not be an acceptable root merely because it
has a stated scope". A maximum-breadth rule stops the first construction and
not the second. Breadth is therefore not the property at fault. What both
constructions share is that the declarant fixed its own scope, and that is
the open question this ontology does not answer.

The decision not to bound breadth is recorded as an
override, not as an absence. COMP-0037 recommended that AI-Lab "reject scopes
that are universal, unparseable, or circular", and this ontology does not
adopt that. The reason is that the recommendation addresses one of the two
constructions its own round produced, so adopting it would report progress
against a defect it does not close. v7 declined the same recommendation
without recording that it was declining anything, and described COMP-0037
only as "the same self-authorization path", which under-reported what that
round found. An override that is not recorded is indistinguishable from an
oversight.

Self-issued authorization is marked, never silently
accepted. Where the issuing principal and the authorized executor are the
same party, or where a principal issues an authorization covering an
invocation it also performs, the authorization records `self_issued: true`.

A self-issued authorization is not refused. At the root of a chain the
accountable party may authorize work it also performs, and commonly will.
v7 said it "necessarily" does; that is false. This ontology separates the
AccountablePrincipal role from the executor role and permits one party to
hold both without requiring it, so a root authorization need not be
self-issued.

The disqualification is conditional, is currently
inert, and must be described as such. A self-issued authorization does not
count as independent authorization wherever independence is required. Nothing
in this ontology establishes when independence is required: that belongs to
AuthorizationPolicy, which Section 4.16 defines and defers. The issuing
principal populates its own authorization's independence requirements, so
until an external policy fixes them, a self-issued authorization may be
recorded with no independence requirement against it, and nothing is
disqualified. Until AuthorizationPolicy exists the marking is a label, and it
may not be presented, in a record or a summary or an implementation plan, as
a control.

Standing authority is not a capability of executors. A model, tool,
or human acting as an executor never holds standing authority by virtue of
executing; it holds it only as an AccountablePrincipal within a declared
scope, which is a separate role under Section 4.13. One party may hold both
roles; the ontology separates the roles, not the parties, and the
`self_issued` marking is how the coincidence is recorded rather than
denied.

Whether standing authority requires periodic re-declaration or
review. COMP-0037 established what v6 got wrong: two reviewers independently
defeated v6's claim to prevent convenient closure of the regress, by
different constructions, and both recommended mechanical scope bounding.
This ontology declines that recommendation for the reason recorded above,
and records the declining.

v8 does not assert that no internal control could close the regress. v7 did,
and drew a universal claim from a single defeated rule. What is established is
narrower: the one control v6 attempted was defeated, and no internal control
is known that survives either COMP-0037 construction. Whether some other
control could is unresolved. P7 gives a reason to expect not, since
entitlement is a fact about the world — but P7 is a stated position about what
records can establish, not a demonstrated result about what controls are
possible, and COMP-0037 does not demonstrate it.

What would move this question is a specification of the external evidence a
scope declaration carries: the external source or accountable process against
which a declaration is assessed, who may assess it, what counts as
sufficient, what follows when that evidence is absent, contested, expired, or
narrower than the declaration, and which outputs the answer affects:
visibility only, invocation authorization, evidence admission, or all three. A
specification that names the evidence without naming what changes when the
evidence fails states a requirement with no operative consequence, which is
the defect this round found in four separate constraints. None of that exists,
and naming its absence is not progress toward it.

=== EVIDENCE PLAN-20260723-0002#scope[12] ===
The one-hop bound is recorded on the outcome: the self-adjudication result carries a check_depth field marking the check as direct-only. The field discloses the scope of the check that ran. It does not prevent a consumer from misreading a permitted result, and it carries no information about whether a deeper collision exists for the artifact in question: a two-hop-clean and a two-hop-colliding artifact both return permitted with the identical value. A permitted result establishes no general independence finding and does not exclude equivalent-executor conflicts further back in the evidence ancestry. Nothing in this slice prevents that misuse; only Slice D's ancestry traversal could establish or rule out such a conflict. The earlier wording claimed a consumer cannot misread the result, which asserted a control a field cannot provide and contradicted ABS-0004 P6, under which a label implying confirmation where none exists is a defect regardless of the correctness of its contents.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q8 ===
Both documents were revised in response to a review. Revisions introduce defects of their own.

Name anything in v8's Section 3 or in the plan text below that is worse than what it replaced, or that is new and unsound. Consider in particular: text added to disclose a limitation that now reads as a rule; a correction that overshot; a sentence whose only function is to record that a previous sentence was wrong; and any place where the document now argues with itself in the reader's presence rather than simply saying what holds. If nothing is worse, say so and name the change you were most suspicious of.

=== EVIDENCE ABS-0004:v8:S3 (all blocks) ===
The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

Declared subordinate execution classes carry the same
breadth legibility as `authority_scope`. A broad declaration is permitted and
must be legible as broad; it may not be described, in a record or a summary,
as narrow because the field was populated. v7 imposed this on
`authority_scope` alone. The asymmetry was a drafting omission, not a
decision: nothing distinguishes the two cases, and a parent authorization
declaring very broad subordinate classes was subject to no visibility
obligation at all.

A disclosure violation under 4.7 is a classification,
not a detection. Nothing in this ontology detects that a subordinate
execution went undeclared. A violation is recorded when someone establishes
it by other means. No statement in this document or in any summary of it may
describe undeclared execution as surfaced, caught, or prevented by these
constraints.

P7. Root authority is extra-systemic. An authorization chain
terminates at a standing authority that the system records and does not
establish. Who is accountable for AI-Lab is a fact about the world, about
who controls the repository and answers for it, and no arrangement of
records inside the repository can make that fact true or verify it. Any
design that appears to derive root authority from internal evidence has
merely moved the regress and disguised it.

Authorization-chain termination. A chain terminates at an
AccountablePrincipal's standing authority within a declared
`authority_scope`. Authorizations the principal issues inside that scope
are self-standing. Every other authorization must chain, through one or
more steps, to such a standing authority. An authorization that chains to
nothing is not thereby permitted: it is unauthorized.

A standing-authority claim is recorded, never
verified. AI-Lab does not validate that a declared principal is entitled to
the authority it claims. No arrangement of records inside this repository can
establish that entitlement, and presenting a record as though it had would be
the overclaim P6 forbids.

That is a statement about repository records. It is not a claim that no means
of any kind exists: whether some external process could establish entitlement
is a separate question this ontology neither answers nor forecloses. v7 said
AI-Lab "has no means to do so", which asserted more than P7 supports.

What the record provides is visibility of the declared: the claim, its
declared scope, and those authorizations that are declared and correctly
chained are legible and attributable. It does not provide visibility of
authorizations that were never declared. Undeclared subordinate execution is
possible under this ontology — the inheritance rule above says so, and
classifies it as a 4.7 disclosure violation rather than detecting it. v7
claimed that "every authorization resting on it" is legible, which its own
Section 3 contradicted two paragraphs earlier.

Visibility of the declared is the whole of what this constraint is for, and it
is not prevention. Whether it is achieved is a further question this constraint
does not settle. No chain-link representation, completeness condition,
traversal rule, or attribution rule is specified anywhere in this ontology, so
nothing here establishes that the authorizations resting on a claim can in fact
be enumerated or followed. v7 asserted that visibility "is the whole of what
this constraint achieves"; achievement was never demonstrated, and the earlier
draft of v8 narrowed the scope of that assertion without withdrawing it. The
constraint states an intended and bounded function. Delivering it depends on
recording being complete and usable, which no rule in this document requires.

Scope breadth is visible, and breadth is not the
defect. A declared `authority_scope` may be arbitrarily wide, including
universal. A wide scope is permitted and must be legible as wide; it may not
be described, in a record or in a summary, as bounded merely because a scope
field was populated. A boundary that no one can fail to satisfy is not a
boundary, and calling it one is a defect P6 forbids.

The legibility requirement is unenforced, and saying so
is part of stating it. Nothing in this ontology supplies a scope grammar, an
interpretation rule, a validation step, a rendering requirement, or a rule
governing what a summary may say about a scope field. The requirement above
therefore binds whoever writes a record or a summary, and a violation is a
defect discoverable by reading rather than one caught by a check. This
constraint is included because the earlier draft of v8 corrected exactly this
overclaim in the standing-authority constraint and reproduced it here two
paragraphs later, which is the defect class P6 names and the third occurrence
of it inside this document.

What makes a scope declaration something other than self-assertion.
COMP-0037 defeated v6's scope rule from two directions, not one. One reviewer
declared a scope wide enough to cover the intended invocation; the other
declared one narrowly tailored to authorize exactly itself, observing that a
declaration so tailored "should not be an acceptable root merely because it
has a stated scope". A maximum-breadth rule stops the first construction and
not the second. Breadth is therefore not the property at fault. What both
constructions share is that the declarant fixed its own scope, and that is
the open question this ontology does not answer.

The decision not to bound breadth is recorded as an
override, not as an absence. COMP-0037 recommended that AI-Lab "reject scopes
that are universal, unparseable, or circular", and this ontology does not
adopt that. The reason is that the recommendation addresses one of the two
constructions its own round produced, so adopting it would report progress
against a defect it does not close. v7 declined the same recommendation
without recording that it was declining anything, and described COMP-0037
only as "the same self-authorization path", which under-reported what that
round found. An override that is not recorded is indistinguishable from an
oversight.

Self-issued authorization is marked, never silently
accepted. Where the issuing principal and the authorized executor are the
same party, or where a principal issues an authorization covering an
invocation it also performs, the authorization records `self_issued: true`.

A self-issued authorization is not refused. At the root of a chain the
accountable party may authorize work it also performs, and commonly will.
v7 said it "necessarily" does; that is false. This ontology separates the
AccountablePrincipal role from the executor role and permits one party to
hold both without requiring it, so a root authorization need not be
self-issued.

The disqualification is conditional, is currently
inert, and must be described as such. A self-issued authorization does not
count as independent authorization wherever independence is required. Nothing
in this ontology establishes when independence is required: that belongs to
AuthorizationPolicy, which Section 4.16 defines and defers. The issuing
principal populates its own authorization's independence requirements, so
until an external policy fixes them, a self-issued authorization may be
recorded with no independence requirement against it, and nothing is
disqualified. Until AuthorizationPolicy exists the marking is a label, and it
may not be presented, in a record or a summary or an implementation plan, as
a control.

Standing authority is not a capability of executors. A model, tool,
or human acting as an executor never holds standing authority by virtue of
executing; it holds it only as an AccountablePrincipal within a declared
scope, which is a separate role under Section 4.13. One party may hold both
roles; the ontology separates the roles, not the parties, and the
`self_issued` marking is how the coincidence is recorded rather than
denied.

Whether standing authority requires periodic re-declaration or
review. COMP-0037 established what v6 got wrong: two reviewers independently
defeated v6's claim to prevent convenient closure of the regress, by
different constructions, and both recommended mechanical scope bounding.
This ontology declines that recommendation for the reason recorded above,
and records the declining.

v8 does not assert that no internal control could close the regress. v7 did,
and drew a universal claim from a single defeated rule. What is established is
narrower: the one control v6 attempted was defeated, and no internal control
is known that survives either COMP-0037 construction. Whether some other
control could is unresolved. P7 gives a reason to expect not, since
entitlement is a fact about the world — but P7 is a stated position about what
records can establish, not a demonstrated result about what controls are
possible, and COMP-0037 does not demonstrate it.

What would move this question is a specification of the external evidence a
scope declaration carries: the external source or accountable process against
which a declaration is assessed, who may assess it, what counts as
sufficient, what follows when that evidence is absent, contested, expired, or
narrower than the declaration, and which outputs the answer affects:
visibility only, invocation authorization, evidence admission, or all three. A
specification that names the evidence without naming what changes when the
evidence fails states a requirement with no operative consequence, which is
the defect this round found in four separate constraints. None of that exists,
and naming its absence is not progress toward it.

=== EVIDENCE PLAN-20260723-0002#scope[12] ===
The one-hop bound is recorded on the outcome: the self-adjudication result carries a check_depth field marking the check as direct-only. The field discloses the scope of the check that ran. It does not prevent a consumer from misreading a permitted result, and it carries no information about whether a deeper collision exists for the artifact in question: a two-hop-clean and a two-hop-colliding artifact both return permitted with the identical value. A permitted result establishes no general independence finding and does not exclude equivalent-executor conflicts further back in the evidence ancestry. Nothing in this slice prevents that misuse; only Slice D's ancestry traversal could establish or rule out such a conflict. The earlier wording claimed a consumer cannot misread the result, which asserted a control a field cannot provide and contradicted ABS-0004 P6, under which a label implying confirmation where none exists is a defect regardless of the correctness of its contents.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
The revisions introduce several new or worsened defects.

1. **Section 3 turns unimplemented disclosure aspirations into operative-looking rules.**  
   For declared subordinate classes and `authority_scope`, it says breadth “must be legible as broad” and “may not be described … as narrow/bounded.” It then concedes that there is no “scope grammar, an interpretation rule, a validation step, a rendering requirement, or a rule governing what a summary may say.”  
   
   That is worse than a simple limitation disclosure: the text imposes a rule on record and summary writers while supplying no determinate way to apply it. In particular, “broad,” “narrow,” “bounded,” and legibility are left without operative criteria. Saying a violation is discoverable “by reading” does not resolve whose reading controls or what makes a description defective.

2. **The section asserts visibility and then withdraws the basis for asserting it.**  
   It says: “What the record provides is visibility of the declared,” including declared and correctly chained authorizations being “legible and attributable.” But it later says no chain-link representation, completeness condition, traversal rule, or attribution rule is specified, and therefore “nothing here establishes that the authorizations resting on a claim can in fact be enumerated or followed.” Likewise, it says “Scope breadth is visible” immediately before conceding that the legibility requirement is unenforced and lacks rendering and interpretation rules.  
   
   The latter qualifications are important, but they do not repair the earlier present-tense claims. The text should say only what the constraint requires or intends, not that the visibility and attribution are provided or achieved.

3. **“Self-standing” authorization appears to give operative status to an unverified assertion.**  
   “A chain terminates at an AccountablePrincipal's standing authority within a declared `authority_scope`” and authorizations issued within that scope “are self-standing.” Yet the section also says a standing-authority claim is “recorded, never verified,” and that the repository cannot establish entitlement.  
   
   If “self-standing” means authorized for ontology purposes merely because a principal declared standing authority and scope, the correction overshoots: it converts an admitted unverified claim into a chain-terminating authorization rule. If it instead means only that the *recorded chain representation* stops there, the text needs to say that. As written, it blurs declared chain status with actual authorization.

4. **The new self-issued rule is presented as a meaningful disqualification while admitted to be inert.**  
   The text first states that self-issued authorization “does not count as independent authorization wherever independence is required,” then says nothing establishes when independence is required; the issuer populates its own independence requirements; and until external policy exists, “nothing is disqualified.”  
   
   The conditional statement may be true, but its placement and categorical wording make the marking read as a control before the text reveals that it currently has no operative consequence. The conclusion—“the marking is a label” and may not be presented as a control—is the more accurate rule. The preceding apparent disqualification should be narrowed to a future-policy condition.

5. **Several passages are revision-history argument rather than ontology content, and make the document argue with itself in the reader’s presence.**  
   Examples include the claims that an asymmetry “was a drafting omission,” that an earlier v8 draft “reproduced” a defect “two paragraphs later,” that this is “the third occurrence” in the document, and repeated accounts of what v6 and v7 said or what COMP-0037 established. These may be useful review notes, but they do not define the ontology’s current semantics. They also repeatedly state a proposition, attack an earlier version of that proposition, and then qualify it.  
   
   The sentence saying the earlier draft of v8 corrected an overclaim and “reproduced it here two paragraphs later” is especially problematic: its principal function is to record that prior text was wrong, not to state what presently holds.

6. **The text overstates what COMP-0037 established.**  
   It says COMP-0037 “established what v6 got wrong” and later that two reviewers “independently defeated v6’s claim.” The evidence supplied here contains no COMP-0037 text, no reviewed v6 scope rule, and no adjudication. More importantly, the section itself later correctly limits the conclusion: the attempted v6 control was defeated, while whether another internal control could work remains unresolved. The stronger “established” and “defeated” formulations should be confined to the particular constructions and claims actually tested.

7. **The plan’s one-hop disclosure still claims properties of the field and Slice D that the supplied plan text does not establish.**  
   The plan says `check_depth` “discloses the scope of the check that ran,” and that “only Slice D’s ancestry traversal could establish or rule out” a deeper equivalent-executor conflict. The surrounding limitations are sounder than the prior claim that consumers cannot misread the result. But the new assertions remain unsupported in this evidence:
   * no schema, production rule, or integrity condition establishes that `check_depth` accurately represents the check actually run;
   * no definition establishes what “direct-only,” “two-hop-clean,” “two-hop-colliding,” or an “equivalent-executor conflict” mean;
   * no Slice D text is supplied to support the exclusivity claim that only it could establish or rule out the conflict.

   Without those materials, the plan can safely say that this slice does not perform deeper traversal or establish general independence. It cannot, on this evidence, claim that the field successfully discloses the check scope or that Slice D is the only possible means of resolving the issue.

To assess the historical comparisons more definitively, I would need the actual cited v6, v7, earlier-v8, COMP-0037, and COMP-0039..0046 text—not merely Section 3’s characterizations of them. To assess the plan’s claims about `check_depth` and Slice D, I would need the field schema and production/validation rules, the definitions of the collision terms, and the referenced Slice D traversal specification.
```

## Claude Response

- model: `claude-sonnet-5`

```
# Q8 — Defects Introduced by the Revisions

## The single worst item: the "third occurrence" passage

The clearest case of a document arguing with itself, rather than stating what holds, is this sequence in the scope-breadth constraint:

> "This constraint is included because the earlier draft of v8 corrected exactly this overclaim in the standing-authority constraint and reproduced it here two paragraphs later, which is the defect class P6 names and the third occurrence of it inside this document."

This sentence does not state a rule. It reports on v8's own drafting history — that an earlier internal draft fixed an overclaim in one place and then repeated it in another — and does so without clarifying whether the text now in front of the reader still contains the repeated overclaim or has been cleaned of it. Read against the immediately preceding sentence —

> "v7 asserted that visibility 'is the whole of what this constraint achieves'; achievement was never demonstrated, and the earlier draft of v8 narrowed the scope of that assertion without withdrawing it."

— the passage leaves it unclear whether "the third occurrence" is a defect that has been corrected in the version under review or one the drafter is merely confessing to. Either way, this is worse than what it replaced: v7 had the overclaim once; v8, by its own admission, produced it (or something the same defect class covers) two further times before catching itself in a footnote-like aside. A correction that has to narrate its own recursion rather than simply state the corrected rule has overshot the genre of an ontology section.

## Limitation dressed as a rule: "never silently accepted"

> "Self-issued authorization is marked, never silently accepted."

Read alone this is a rule-shaped guarantee — it sounds like self-issuance triggers scrutiny. The text several sentences later withdraws the implication without withdrawing the sentence:

> "The disqualification is conditional, is currently inert, and must be described as such... a self-issued authorization may be recorded with no independence requirement against it, and nothing is disqualified."

So "never silently accepted" turns out to mean only "always labeled," not "never permitted to pass unexamined." The heading states more than the mechanism delivers, and the reader has to sit through several paragraphs of qualification to learn that the marking is presently inert. This is the "disclosed limitation that now reads as a rule" pattern named in the question.

## The recurring "v7 said X; that is false" sentences

Several sentences in Section 3 have no function beyond recording that a prior sentence was wrong, without adding operative content of their own:

> "v7 said it 'necessarily' does; that is false."

> "v7 claimed that 'every authorization resting on it' is legible, which its own Section 3 contradicted two paragraphs earlier."

> "v7 declined the same recommendation without recording that it was declining anything, and described COMP-0037 only as 'the same self-authorization path', which under-reported what that round found."

Each of these is individually defensible as a correction. Taken together, though, they make Section 3 partly a changelog rather than a statement of what the ontology now holds — the same genre problem as the "third occurrence" sentence above, repeated enough times that it looks like a structural habit of this revision rather than an occasional necessary correction.

## The plan text imports the same defect

> "The earlier wording claimed a consumer cannot misread the result, which asserted a control a field cannot provide and contradicted ABS-0004 P6, under which a label implying confirmation where none exists is a defect regardless of the correctness of its contents."

This sentence does two things worth flagging. First, it is structurally identical to the v8 "v7 said X, that was wrong" sentences — its only function is to record that earlier plan wording overclaimed, not to state the operative constraint (which the preceding sentences already state adequately: "It does not prevent a consumer from misreading a permitted result... A permitted result establishes no general independence finding"). Second, it leans on "ABS-0004 P6" as settled authority for what counts as a defect, while ABS-0004 v8 — including P6 — is proposed and not admitted. A plan citing an unadmitted provision as the standard by which its own prior wording is condemned is treating draft ontology text as if it already had governance force, which the disclosures preceding this question specifically warn against.

## What I could not check

- **Full text of P6.** Both the "third occurrence" sentence and the plan's "contradicted ABS-0004 P6" sentence depend on what P6 actually says. Only fragments are quoted ("a label implying confirmation where none exists is a defect regardless of the correctness of its contents"). I would need the full provision to confirm whether the plan's citation is accurate or itself overshoots.
- **Section 4.7, 4.13, 4.16, and AuthorizationPolicy.** Section 3 repeatedly defers substantive content to these ("belongs to AuthorizationPolicy, which Section 4.16 defines and defers"; "DecisionRecord kinds (Section 4.13)"; "a disclosure violation under 4.7"). Without them I cannot assess whether the deferred mechanisms actually close any of the gaps Section 3 flags as open, or whether they themselves contain the same disclosed-limitation-as-rule pattern.
- **Slice D of the plan** ("only Slice D's ancestry traversal could establish or rule out such a conflict"). I would need this to know whether the plan's disclosed limitation is bounded by an actual mechanism elsewhere or is, like several v8 constraints, a named absence with no operative consequence attached.

If nothing else were suspicious, I would still flag the "never silently accepted" heading as the item most likely to mislead a reader who stops before reaching its qualification three paragraphs later.
```
