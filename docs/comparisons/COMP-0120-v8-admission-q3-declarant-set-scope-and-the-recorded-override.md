# COMP-0120: Provider Comparison — v8 admission Q3 declarant-set-scope-and-the-recorded-override

## Metadata

- comparison_id: `COMP-0120`
- title: `v8 admission Q3 declarant-set-scope-and-the-recorded-override`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-22cf7594a478a150.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0120", "target_id": "INV-22cf7594a478a150"}, {"authoritative": false, "evidence": "docs/invocations/INV-2f432ce9bf320fa4.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0120", "target_id": "INV-2f432ce9bf320fa4"}]`
- created_at: `2026-07-31T13:39:38.348762+00:00`
- command: `scripts/compare_providers.py --title v8 admission Q3 declarant-set-scope-and-the-recorded-override You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q3 ===
v8 declines to impose a maximum authority_scope breadth. Its reason: the prior round defeated the scope rule from two directions, one using a scope too wide and one narrowly tailored to authorize exactly itself, so a breadth bound stops one and not the other, and what both share is that the declarant fixed its own scope. v8 records that it is overriding an explicit recommendation to reject universal scopes.

Test the reasoning, not the honesty of recording it. Does "the declarant fixed its own scope" correctly name what the two constructions share, or is it a generalisation that happens to cover both? Is there a property they share that would support a control, which this framing hides? If the framing is right, say what follows: whether any internal rule can bear on a declarant-set scope, and if not, what the open question is actually asking for.

=== EVIDENCE ABS-0004:v8:S3#open:what-makes-a-scope-declaration-som ===
What makes a scope declaration something other than self-assertion.
COMP-0037 defeated v6's scope rule from two directions, not one. One reviewer
declared a scope wide enough to cover the intended invocation; the other
declared one narrowly tailored to authorize exactly itself, observing that a
declaration so tailored "should not be an acceptable root merely because it
has a stated scope". A maximum-breadth rule stops the first construction and
not the second. Breadth is therefore not the property at fault. What both
constructions share is that the declarant fixed its own scope, and that is
the open question this ontology does not answer.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:the-decision-not-to-bound-breadth ===
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

=== QUESTION Q3 ===
v8 declines to impose a maximum authority_scope breadth. Its reason: the prior round defeated the scope rule from two directions, one using a scope too wide and one narrowly tailored to authorize exactly itself, so a breadth bound stops one and not the other, and what both share is that the declarant fixed its own scope. v8 records that it is overriding an explicit recommendation to reject universal scopes.

Test the reasoning, not the honesty of recording it. Does "the declarant fixed its own scope" correctly name what the two constructions share, or is it a generalisation that happens to cover both? Is there a property they share that would support a control, which this framing hides? If the framing is right, say what follows: whether any internal rule can bear on a declarant-set scope, and if not, what the open question is actually asking for.

=== EVIDENCE ABS-0004:v8:S3#open:what-makes-a-scope-declaration-som ===
What makes a scope declaration something other than self-assertion.
COMP-0037 defeated v6's scope rule from two directions, not one. One reviewer
declared a scope wide enough to cover the intended invocation; the other
declared one narrowly tailored to authorize exactly itself, observing that a
declaration so tailored "should not be an acceptable root merely because it
has a stated scope". A maximum-breadth rule stops the first construction and
not the second. Breadth is therefore not the property at fault. What both
constructions share is that the declarant fixed its own scope, and that is
the open question this ontology does not answer.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:the-decision-not-to-bound-breadth ===
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

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
“The declarant fixed its own scope” identifies a fact common to the two examples, but it is too general to identify the decisive defect.

It covers both a scope “wide enough to cover the intended invocation” and one “narrowly tailored to authorize exactly itself.” But those examples more specifically suggest that the scope was selected by the party benefiting from it so that the declaration supplies the authorization the party needs. The narrow construction is expressly self-authorizing: it is “tailored to authorize exactly itself.” The potentially control-relevant common property is therefore not breadth, nor merely that a declarant authored a scope, but absence of an independent constraint or authorization source governing the scope-to-invocation fit.

That distinction matters. A declarant can fix wording while still being constrained by an independently established mandate, issuer, delegation, policy, or review rule. Conversely, a syntactically valid and bounded scope remains self-assertion if the declarant may choose its contents to make its own intended act authorized. The quoted material does not establish whether either construction lacked such an external basis, or whether the ontology has a mechanism capable of requiring one.

If v8’s framing is right in the stronger sense—that any scope fixed by its declarant is inherently self-assertion—then no internal rule that only inspects the declaration’s breadth, parseability, circular wording, or other intrinsic features can make that scope authoritative. Such rules can reject forms of self-assertion, including the universal case, but cannot supply the missing authority. An internal rule could bear on the problem only if it requires something not fixed by the declarant—for example, an independently established authority source or constraint. At that point, the open question is not simply whether a scope is broad. It is: what makes a scope declaration binding rather than self-assertion, including who may establish it, what constrains its content, and how the invocation is checked against that independent basis.

The evidence is insufficient to determine whether “declarant fixed its own scope” is only a descriptive generalisation or accurately captures the actual shared failure of the two COMP-0037 constructions. Missing material needed for that determination is:

- the full COMP-0037 record, especially the two actual constructions and the reasoning that defeated v6’s rule;
- the v6 scope rule and the relevant v8 definitions of `authority_scope`, declarant, invocation, and authorization;
- any ontology provisions concerning delegation, provenance, independent issuance, review, or enforcement of scope declarations.

Those materials would show whether the two cases share a demonstrated lack of independent authorization, rather than merely the stated fact that each reviewer declared a scope.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Testing "the declarant fixed its own scope" as the shared property

**The claim as stated proves too much.** By definition, an *authority_scope declaration* is an act in which some declarant states a scope. If "the declarant fixed its own scope" is sufficient to name the defect shared by the two COMP-0037 constructions, it is hard to see how it does not equally describe *every* scope declaration this ontology would ever accept — including any it treats as legitimate. A property that is true of the entire category cannot, by itself, explain why these two particular instances "defeated" the v6 rule while others (if any exist) did not. The evidence set does not include a description of what a *non*-self-asserted, or otherwise accepted, authority_scope declaration looks like under this ontology, so there is no way to confirm whether self-declaration is (a) a universal, non-diagnostic feature of the mechanism, or (b) a defect specific to these two cases. That is a real gap: **I would need the ontology's baseline definition of how authority_scope is normally established (issuer, attestation chain, or absence thereof) to know whether "self-fixing" distinguishes anything.**

**A more specific shared property is available and is arguably what the text is actually gesturing at, but doesn't name.** Look at what the two constructions did, not just what they were:

- Construction 1: "declared a scope wide enough to cover the intended invocation" — the scope was set *with reference to* the specific act the declarant already meant to perform.
- Construction 2: "declared one narrowly tailored to authorize exactly itself" — the scope was set *with reference to* the declaration act itself.

Both share not merely "the declarant set it," but **the declarant set it by reference to the very thing it was going to use it to authorize** — a reverse-fit between scope and use, with no anchor independent of the declarant's own intended outcome. That is a narrower, more actionable property than "self-assertion" in general: it is a *correlation* defect (scope derived from target), not merely an *origin* defect (scope stated by the party who benefits). A control could target the correlation defect directly — e.g., requiring that a scope be fixed and recorded prior to, and independent of, knowledge of the specific invocation it will later be used to cover — without requiring that scope-setting be taken away from the declarant entirely. The "declarant fixed its own scope" framing collapses this into a broader, less tractable claim and thereby hides the possibility of a narrower fix.

**If the framing is taken at face value anyway** — i.e., if self-assertion itself, not the reverse-fit, is what disqualifies both constructions — then the consequence the text draws is internally consistent: no rule that evaluates the *content* of a declared scope (breadth, parseability, circularity — exactly the recommendation v8 overrides: "reject scopes that are universal, unparseable, or circular") can reach the defect, because the defect is about *who* fixes the scope, not *what* the scope says. A content-level rule operates downstream of the moment where self-assertion already occurred. Under this reading, "any internal rule bearing on a declarant-set scope" is a category error: internal rules here are rules about scope shape, and shape is not where the problem sits.

**What the open question is then actually asking for**, under that reading, is not a better shape-rule but a *source* of scope external to the declarant — some issuer, attester, or registry distinct from the party invoking the authority, whose involvement would make "has a stated scope" (the second reviewer's phrase) insufficient on its own. Nothing in the evidence supplied describes such a mechanism, or even states whether one is contemplated elsewhere in the ontology; the section header itself concedes this is unanswered ("that is the open question this ontology does not answer").

**Missing evidence I would want before treating either reading as settled:**
- The full COMP-0037 record (only paraphrased here) — to check whether the reviewers' own diagnoses matched "self-assertion" or the narrower "reverse-fit" account.
- Any ontology section defining how authority_scope is normally established, to test whether self-declaration is universal (making the framing tautological) or exceptional (making it diagnostic).
- The full text of the declined recommendation, to check whether "reject universal, unparseable, or circular scopes" was proposed as a complete fix or as one of several layered controls — the adopted_constraint text characterizes it as addressing only "one of the two constructions," but I cannot verify that characterization against the recommendation's own scope without the source text.
```
