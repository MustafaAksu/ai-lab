# COMP-0119: Provider Comparison — v8 admission Q2 inert-clause-annotated-rather-than-removed

## Metadata

- comparison_id: `COMP-0119`
- title: `v8 admission Q2 inert-clause-annotated-rather-than-removed`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-80e994caca2983f5.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0119", "target_id": "INV-80e994caca2983f5"}, {"authoritative": false, "evidence": "docs/invocations/INV-a45455ed4fdecbdb.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0119", "target_id": "INV-a45455ed4fdecbdb"}]`
- created_at: `2026-07-31T13:37:57.723792+00:00`
- command: `scripts/compare_providers.py --title v8 admission Q2 inert-clause-annotated-rather-than-removed You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q2 ===
v8 keeps the rule that a self-issued authorization is disqualified from counting as independent, and adds a constraint stating that the disqualification is conditional, is currently inert because the policy that would fix independence requirements is deferred, and may not be presented as a control.

A prior round found the disqualification does no work because the issuing principal populates its own independence requirements. v8's response was to say so rather than to change it.

Is annotating an inert clause the honest form, or does keeping a rule that does nothing, with a note that it does nothing, leave a reader worse off than deleting it? Argue one side. Then state what would have to exist for the clause to do work, and whether v8's text commits to producing it.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:self-issued-authorization-is-marke ===
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

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:the-disqualification-is-conditiona ===
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

=== QUESTION Q2 ===
v8 keeps the rule that a self-issued authorization is disqualified from counting as independent, and adds a constraint stating that the disqualification is conditional, is currently inert because the policy that would fix independence requirements is deferred, and may not be presented as a control.

A prior round found the disqualification does no work because the issuing principal populates its own independence requirements. v8's response was to say so rather than to change it.

Is annotating an inert clause the honest form, or does keeping a rule that does nothing, with a note that it does nothing, leave a reader worse off than deleting it? Argue one side. Then state what would have to exist for the clause to do work, and whether v8's text commits to producing it.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:self-issued-authorization-is-marke ===
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

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:the-disqualification-is-conditiona ===
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

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
Keeping the clause with the inertness annotation is the more honest form than deleting it.

Deletion would remove two facts the ontology is trying to preserve: that a self-issued authorization is identifiable (`self_issued: true`), and that, if independence is externally required, such an authorization cannot satisfy that requirement. The retained text does not claim that the marker presently prevents anything. It says that “until an external policy fixes” independence requirements, “nothing is disqualified,” and that the marking “may not be presented … as a control.” That makes the current non-effect explicit rather than leaving an apparently meaningful rule whose trigger is hidden.

On this evidence, the reader is not worse off merely because the conditional rule remains. The reader would be worse off only if a record, summary, or plan represented the marker as an effective independence safeguard despite the stated prohibition. The clause presently supplies a label and a future conditional interpretation, not a control.

For the clause to do work, at least the following must exist:

1. An external `AuthorizationPolicy` that establishes when independence is required.
2. Requirements fixed externally rather than left for the issuing principal to populate on its own authorization.
3. A decision or validation process that evaluates an authorization against those requirements and treats `self_issued: true` as unable to count as the required independent authorization.

The first two are necessary for the disqualification even to be triggered. The third is necessary if “do work” means an operative control rather than only a stated semantic consequence.

v8 does not, in the supplied text, commit to producing those conditions. It says the matter “belongs to `AuthorizationPolicy`, which Section 4.16 defines and defers.” Deferral is not a commitment to publish, adopt, implement, or enforce such a policy. Moreover, ABS-0004 v8 is proposed and not admitted, so it has no governance force.

To assess whether Section 4.16 contains a concrete production commitment, its text is missing. I would use it to look for an owner, required policy content, adoption condition, deadline, enforcement mechanism, and any rule preventing the issuing principal from setting its own independence threshold. A corresponding implementation specification would also be needed to determine whether any evaluator actually applies the conditional disqualification.
```

## Claude Response

- model: `claude-sonnet-5`

```
**Position: keeping the disqualification with the inertness note leaves a reader worse off than deletion would.**

The clause does two things that pull against each other. It states a rule in imperative, rule-like language — "A self-issued authorization does not count as independent authorization wherever independence is required" — and then, in the same breath, discloses that the rule cannot currently fire: "The issuing principal populates its own authorization's independence requirements, so until an external policy fixes them, a self-issued authorization may be recorded with no independence requirement against it, and nothing is disqualified." That is not a rule with an exception; it is a rule that never triggers, because the only party who could trigger it is the party it targets. The clause's own text admits this is circular, not merely incomplete.

The problem with retaining it, annotated, is structural rather than a matter of wording. The disqualification language and its inertness disclosure sit in two separate adopted constraints (the marking behavior in one block, the "conditional... currently inert" admission in another). A record or plan citing the disqualification does not have to carry the inertness caveat with it — the two are severable at the level of citation, and the amendment's own history shows citations get taken up and adjudicated piecemeal rather than as inseparable wholes. So the instruction "it may not be presented, in a record or a summary or an implementation plan, as a control" is a norm addressed to future authors' good faith, not a structural bar. It depends on every downstream reader finding, reading, and honoring the second clause every time the first is invoked. Deletion removes that dependency entirely: there is no disqualification text to mis-cite as a control if it isn't there. What remains — `self_issued: true` as a bare marker — reads as a flag, not as a safeguard, and cannot be mistaken for one. Keeping the disqualifying language while disclosing its inertness preserves exactly the surface form (a named "disqualification," a record marking) that a control would have, which is the shape most likely to be misread or misquoted as one, even under an explicit prohibition against doing so.

**What would have to exist for the clause to do work:**
An AuthorizationPolicy that fixes independence requirements in a way the issuing principal does not itself populate. The text names where this is supposed to come from — "that belongs to AuthorizationPolicy, which Section 4.16 defines and defers" — but for the disqualification to stop being circular, whatever Section 4.16 defines must set independence requirements from outside the self-issuing party's control. If Section 4.16 still lets the issuing principal set its own independence requirement, adopting it would not fix anything; the same circularity would just relocate one layer down.

**Does v8 commit to producing it?**
No. The operative language is "must be described as such" and "may not be presented... as a control" — both are obligations about labeling and disclosure, not about building or scheduling AuthorizationPolicy. There is no commitment in this text to adopt Section 4.16, no trigger condition, and no timeline. v8 commits to accurate description of the deferral, not to ending it.

**Missing evidence:** Section 4.16 (the AuthorizationPolicy definition) is named but not included here. I would need it to check whether, once adopted, it actually assigns independence-requirement-setting to a party other than the issuing principal — i.e., whether it would resolve the circularity or merely restate it — and whether any governance record specifies a trigger or timeline for un-deferring it. Without that section, I can't assess whether the "fix" the clause points to is real or itself another deferral.
```
