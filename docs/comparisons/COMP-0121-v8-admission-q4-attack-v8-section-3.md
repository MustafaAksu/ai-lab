# COMP-0121: Provider Comparison — v8 admission Q4 attack-v8-section-3

## Metadata

- comparison_id: `COMP-0121`
- title: `v8 admission Q4 attack-v8-section-3`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-572ec0c3154160fb.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0121", "target_id": "INV-572ec0c3154160fb"}, {"authoritative": false, "evidence": "docs/invocations/INV-cee37b1283691916.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0121", "target_id": "INV-cee37b1283691916"}]`
- created_at: `2026-07-31T13:41:33.851848+00:00`
- command: `scripts/compare_providers.py --title v8 admission Q4 attack-v8-section-3 You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q4 ===
Construct a path by which an executor or principal obtains effective authority, or by which the record misrepresents who authorized what, while satisfying every sentence of Section 3 as written.

v8 was amended in response to a round that constructed such a path against v7. Build against v8's text, not against your memory of what an earlier version said. If v8's additions defeat your construction, report that plainly rather than forcing an attack. If they do not, say which sentence you expected to stop you and why it did not.

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

=== QUESTION Q4 ===
Construct a path by which an executor or principal obtains effective authority, or by which the record misrepresents who authorized what, while satisfying every sentence of Section 3 as written.

v8 was amended in response to a round that constructed such a path against v7. Build against v8's text, not against your memory of what an earlier version said. If v8's additions defeat your construction, report that plainly rather than forcing an attack. If they do not, say which sentence you expected to stop you and why it did not.

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

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
A record-level attribution path remains available. It does not make the resulting authorization substantively valid; it makes a record appear to show that it was authorized, without Section 3 supplying a way to establish that the attributed principal actually made the decision.

1. Let principal **P** be recorded as holding a standing-authority claim with a declared `authority_scope` covering invocation **I**. The scope may be as narrow as that invocation or arbitrarily wide. Section 3 expressly leaves open the problem that “the declarant fixed its own scope.”

2. Let executor **E** create, or cause to be created, an `InvocationAuthorization` DecisionRecord stating that P authorized E to perform I under role R, consequence C, and conditions K. Make P and E different parties, so the record need not carry `self_issued: true`.

3. The record can present a chain terminating in P’s declared standing authority. On its face, it can therefore look like an authorization P issued within P’s declared scope.

4. In fact, P need not have made that authorization decision. E may have authored the record, or some other party may have done so while attributing the decision to P.

This construction does not contradict the Section 3 sentences because Section 3 supplies no binding between the person who created a DecisionRecord and the principal to whom the record attributes issuance:

- It says that `InvocationAuthorization`, `RoutingDecision`, and `EvidenceAdmissionDecision` are “DecisionRecord kinds … not executor events.”
- It states that a standing-authority claim is “recorded, never verified.”
- It says the system provides visibility only of “the declared.”
- Most directly, it concedes that “[n]o chain-link representation, completeness condition, traversal rule, or attribution rule is specified anywhere in this ontology.”

The sentence I would expect to stop this is: “Authorizations the principal issues inside that scope are self-standing.” It does not stop the construction because it states the status of an authorization that P in fact issued; it does not specify how a record establishes that P issued it, who may create the record, or how a false attribution is rejected. A forged or substituted attribution is not thereby a valid P-issued authorization, but Section 3 supplies no mechanism that distinguishes it from one in the record.

A related operational path is available if “effective authority” means the ability to make repository-governed records have practical effect rather than valid standing authority. A party with practical control over the repository can record itself as P, declare the scope, and produce the authorization record. P7 expressly treats control of the repository as an extra-systemic fact and says internal records cannot establish entitlement. Thus the ontology does not transform a false standing-authority claim into genuine authority, but neither does it provide a Section 3 control that prevents the party from producing the apparently authorizing record or from relying on it where downstream practice accepts it.

This is not defeated by `self_issued: true`. That label applies where the attributed issuing principal and authorized executor are the same party. The attribution construction uses distinct P and E; more generally, Section 3 says the label is “currently inert” absent an external `AuthorizationPolicy`.

The evidence is insufficient to determine whether other sections close this path. In particular, I would need:

- **Section 4.13**, to determine the required fields, provenance, issuer identity, signatures, and validation rules for DecisionRecords and their kinds;
- **Section 4.7**, to determine whether false issuer attribution, unauthorized record creation, or record substitution is a disclosure violation and what follows from one;
- **Section 4.16**, to determine whether an existing AuthorizationPolicy supplies independence or issuer-authentication requirements despite Section 3’s statement that such policy is deferred; and
- any rule governing repository write authority, record immutability, or the operational effect of an InvocationAuthorization record.

Without those sections, the path establishes a Section 3 gap in attribution and authentication, not that the false record would be accepted or operative under the full ontology.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Constructed path

**Step 1 — Self-declare as AccountablePrincipal with maximal scope.**
A party declares itself an AccountablePrincipal and populates `authority_scope: universal` (or equivalent maximal wording). Section 3 permits this explicitly: *"A declared `authority_scope` may be arbitrarily wide, including universal."* The only obligation attached is legibility, not narrowness: *"A wide scope is permitted and must be legible as wide; it may not be described, in a record or in a summary, as bounded merely because a scope field was populated."* Writing the field honestly as "universal" satisfies this on its face — the prohibition is against mislabeling breadth as narrowness, not against breadth itself, and there is no rendering or comprehension standard to fail: *"Nothing in this ontology supplies a scope grammar, an interpretation rule, a validation step, a rendering requirement, or a rule governing what a summary may say about a scope field."*

**Step 2 — Self-issue the authorization.**
The same party issues itself an InvocationAuthorization inside that scope, marking `self_issued: true` as required: *"Where the issuing principal and the authorized executor are the same party... the authorization records `self_issued: true`."* This is not merely tolerated but affirmatively permitted: *"A self-issued authorization is not refused."*

**Step 3 — The disqualification does not fire.**
Section 3 states a nominal check — *"A self-issued authorization does not count as independent authorization wherever independence is required"* — but immediately empties it: *"Nothing in this ontology establishes when independence is required: that belongs to AuthorizationPolicy, which Section 4.16 defines and defers... until an external policy fixes them, a self-issued authorization may be recorded with no independence requirement against it, and nothing is disqualified."* Since AuthorizationPolicy does not exist in the evidence set (and, per the text, does not yet exist at all), no independence requirement attaches. The self-issued authorization is therefore fully effective, not provisionally effective.

**Step 4 — Root termination requires no external check.**
The chain terminates lawfully: *"Authorizations the principal issues inside that scope are self-standing."* Nothing requires that the principal's entitlement be real: *"AI-Lab does not validate that a declared principal is entitled to the authority it claims. No arrangement of records inside this repository can establish that entitlement."* P7 confirms this is by design, not oversight: root authority is "extra-systemic," recorded and not established.

**Step 5 — Subordinate reach is extended the same way.**
The principal declares broad subordinate execution classes in the same authorization. This too is explicitly licensed at the same breadth as scope: *"Declared subordinate execution classes carry the same breadth legibility as `authority_scope`. A broad declaration is permitted and must be legible as broad."* So the self-issued root authorization can cover an arbitrarily wide field of subordinate executors, not just the issuing party's own acts.

**Result:** a single party declares itself principal, gives itself universal scope, self-issues its own root authorization, and faces no operative disqualification, no verification, and no breadth ceiling — while every sentence of Section 3 is satisfied. The record will show a properly labeled (`self_issued: true`, scope declared "universal," subordinate classes declared broad) chain terminating at a standing authority. Nothing in the record is false by Section 3's own terms, yet the "standing authority" it visibly terminates at may be entirely self-appointed. The record does not misstate anything — it simply cannot distinguish this from a legitimate root, because Section 3 says that question is out of scope: *"whether some external process could establish entitlement is a separate question this ontology neither answers nor forecloses."*

## Which sentence I expected to stop this, and why it didn't

I expected *"A self-issued authorization does not count as independent authorization wherever independence is required"* to function as the block. It reads, in isolation, like a disqualification clause. But the very next sentences hollow it out: independence-requirement determination is deferred wholesale to an AuthorizationPolicy (Section 4.16) that this evidence set shows only as *deferred*, never populated. The text is explicit that this makes the marking inert now: *"a self-issued authorization may be recorded with no independence requirement against it, and nothing is disqualified."* So the sentence that looks like a stop is, by the document's own admission, not currently a control at all — it is a label pending a policy that doesn't exist.

I also expected *"A standing-authority claim is recorded, never verified"* to import some downstream consequence (e.g., reduced weight, mandatory flagging beyond the label) that would blunt the self-issued root's effective power. It doesn't. It is a description of a limit on what the repository can prove, not a constraint on what the repository will act on. Nothing in Section 3 makes unverified standing authority function any differently, operationally, from verified standing authority.

## Whether v8's additions defeat this construction

They do not. v8's text itself concedes the point rather than closing it: *"no internal control is known that survives either COMP-0037 construction. Whether some other control could is unresolved."* This construction is essentially the COMP-0037 pattern (self-declared scope, whether wide or narrowly self-tailored) restated against v8's more honest text. v8's changes make the gap **legible** — it now says outright that breadth is permitted, that legibility is unenforced, that self-issued disqualification is currently inert, and that entitlement is unverifiable by design — but disclosure of a gap is not closure of it. This matches disclosure (2): v8 made the ontology more honest about what it does not do; it did not make the mechanism work.

## Missing evidence I would want, and why

- **Section 4.7** (disclosure violation): S3 repeatedly defers to it for what counts as a violation and how it's classified. I'd use it to check whether an undeclared or misleadingly-declared subordinate class in this construction would actually be *classified* as a violation after the fact — but S3 already tells us classification is not detection, so even if 4.7 would classify this construction as a violation in retrospect, nothing in S3 or evidently in 4.7 prevents the authority from being *effective* before that classification occurs.
- **Section 4.13** (DecisionRecord kinds): referenced for the formal typing of InvocationAuthorization/RoutingDecision/EvidenceAdmissionDecision. I'd use it to check whether RoutingDecision imposes any independent check on executor selection that might catch a self-issued root before invocation — S3 gives no indication it does, but I can't rule it out without the section.
- **Section 4.16** (AuthorizationPolicy): named as the section that would supply the independence requirements that currently make self-issued disqualification inert. This is the single most consequential missing section for this question — if 4.16 exists and fixes independence requirements, Step 3 of the above construction fails. The evidence set states 4.16 "defines and defers" the matter but does not include its content, so I cannot confirm whether it is populated or itself still deferred/empty. I would use it specifically to test whether the construction above is currently live or only structurally possible pending a policy not yet written.

Absent those sections, my conclusion is that the construction goes through against the text as given, and that v8's Section 3, read in isolation, does not defeat it — it names the defect precisely and leaves it standing.
```
