# COMP-0123: Provider Comparison — v8 admission Q6 refusal-enumeration-and-the-4-7-exclusion

## Metadata

- comparison_id: `COMP-0123`
- title: `v8 admission Q6 refusal-enumeration-and-the-4-7-exclusion`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-f35084e232e73a58.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0123", "target_id": "INV-f35084e232e73a58"}, {"authoritative": false, "evidence": "docs/invocations/INV-5df27cab8cd67f07.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0123", "target_id": "INV-5df27cab8cd67f07"}]`
- created_at: `2026-07-31T13:44:25.992946+00:00`
- command: `scripts/compare_providers.py --title v8 admission Q6 refusal-enumeration-and-the-4-7-exclusion You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q6 ===
The plan now enumerates fourteen refusal reasons and states expressly that ABS-0004 Section 4.7's disclosure constraints are excluded from what authorize() checks, with the reason that none is checkable from stored records.

Two things to test. First, is fourteen complete for what the plan means by a valid authorization? Name any refusal the enumeration still lacks. Second, a prior reviewer's condition on excluding 4.7 was that the plan must then not describe its result as a valid authorization under the adopted constraints. Does the plan's current wording meet that condition, or does it exclude the checks while retaining language that implies they were made?

=== EVIDENCE PLAN-20260723-0002#scope[4] ===
A pure authorize() function over stored records returning an authorization outcome or one of the enumerated refusal reasons: (1) no qualification for this executor and role; (2) qualification out of execution scope; (3) consequence above the role ceiling; (4) unterminated authorization chain; (5) standing authority claimed outside its declared scope; (6) an authorization condition is unmet; (7) the authorization is malformed; (8) required conditions are absent; (9) authorized executor does not match the executor performing the invocation; (10) the authorization or a record it relies on is inactive or superseded; (11) subordinate execution represented as an Invocation but outside the classes its parent authorization declares; (12) self-adjudication conflict; (13) no authorization record covers this invocation; (14) an independence requirement recorded on the authorization is unmet. Fourteen reasons, each with a fixture. COMP-0037 found four missing from the six originally proposed. COMP-0043 found three further defects in the resulting ten: reasons 6 to 8 above were a single reason combining a failed condition, malformed data, and absent conditions, which differ in diagnostic and remedial meaning; reason 13 was absent, since "authorized executor does not match" presupposes an authorization exists; and reason 14 was absent, so an unmet independence requirement could not refuse unless the one-hop artifact test happened to trigger. EXCLUDED, EXPRESSLY: the three ABS-0004 Section 4.7 disclosure constraints are not checked by authorize() in this slice. They are not checkable from stored records: OutboundInteractionLog is in Section 11, Defined but Deferred, so no such record exists; EffectiveInputManifest carries completeness_attestation partial_declared_channels_only on every record, so a manifest attesting its own partiality cannot ground a refusal for undeclared configuration; and an undisclosed subordinate execution requires detecting an absence, which no stored record supplies. Reason 11 therefore reaches a subordinate that IS represented and exceeds its declared classes, and does not reach one never disclosed as an Invocation at all, which ABS-0004 Section 3 calls not an implicitly authorized act. An invocation with a required disclosure absent can pass every check in this slice and be classified governed. That is a stated limit of the slice, not a gap the fixtures will catch.

=== EVIDENCE PLAN-20260723-0002#scope[7] ===
The experimental-versus-governed boundary: a classify function marking an invocation governed only when a valid authorization covers it, experimental otherwise. Classification only; no invocation is refused execution by this slice. "Valid authorization" here means only that an authorization record covers the invocation and none of the fourteen refusal reasons applies. It does not certify disclosure compliance, and a governed classification asserts nothing about whether ABS-0004 Section 4.7's constraints were met. Neither the documentation nor any summary may describe a governed result as a valid authorization under the full set of adopted ABS-0004 constraints, because the Section 4.7 constraints are excluded from what is checked.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:a-disclosure-violation-under-4-7-i ===
A disclosure violation under 4.7 is a classification,
not a detection. Nothing in this ontology detects that a subordinate
execution went undeclared. A violation is recorded when someone establishes
it by other means. No statement in this document or in any summary of it may
describe undeclared execution as surfaced, caught, or prevented by these
constraints.

=== EVIDENCE ABS-0004:v8:S3#def:subordinate-authorization-inherita ===
Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

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

=== QUESTION Q6 ===
The plan now enumerates fourteen refusal reasons and states expressly that ABS-0004 Section 4.7's disclosure constraints are excluded from what authorize() checks, with the reason that none is checkable from stored records.

Two things to test. First, is fourteen complete for what the plan means by a valid authorization? Name any refusal the enumeration still lacks. Second, a prior reviewer's condition on excluding 4.7 was that the plan must then not describe its result as a valid authorization under the adopted constraints. Does the plan's current wording meet that condition, or does it exclude the checks while retaining language that implies they were made?

=== EVIDENCE PLAN-20260723-0002#scope[4] ===
A pure authorize() function over stored records returning an authorization outcome or one of the enumerated refusal reasons: (1) no qualification for this executor and role; (2) qualification out of execution scope; (3) consequence above the role ceiling; (4) unterminated authorization chain; (5) standing authority claimed outside its declared scope; (6) an authorization condition is unmet; (7) the authorization is malformed; (8) required conditions are absent; (9) authorized executor does not match the executor performing the invocation; (10) the authorization or a record it relies on is inactive or superseded; (11) subordinate execution represented as an Invocation but outside the classes its parent authorization declares; (12) self-adjudication conflict; (13) no authorization record covers this invocation; (14) an independence requirement recorded on the authorization is unmet. Fourteen reasons, each with a fixture. COMP-0037 found four missing from the six originally proposed. COMP-0043 found three further defects in the resulting ten: reasons 6 to 8 above were a single reason combining a failed condition, malformed data, and absent conditions, which differ in diagnostic and remedial meaning; reason 13 was absent, since "authorized executor does not match" presupposes an authorization exists; and reason 14 was absent, so an unmet independence requirement could not refuse unless the one-hop artifact test happened to trigger. EXCLUDED, EXPRESSLY: the three ABS-0004 Section 4.7 disclosure constraints are not checked by authorize() in this slice. They are not checkable from stored records: OutboundInteractionLog is in Section 11, Defined but Deferred, so no such record exists; EffectiveInputManifest carries completeness_attestation partial_declared_channels_only on every record, so a manifest attesting its own partiality cannot ground a refusal for undeclared configuration; and an undisclosed subordinate execution requires detecting an absence, which no stored record supplies. Reason 11 therefore reaches a subordinate that IS represented and exceeds its declared classes, and does not reach one never disclosed as an Invocation at all, which ABS-0004 Section 3 calls not an implicitly authorized act. An invocation with a required disclosure absent can pass every check in this slice and be classified governed. That is a stated limit of the slice, not a gap the fixtures will catch.

=== EVIDENCE PLAN-20260723-0002#scope[7] ===
The experimental-versus-governed boundary: a classify function marking an invocation governed only when a valid authorization covers it, experimental otherwise. Classification only; no invocation is refused execution by this slice. "Valid authorization" here means only that an authorization record covers the invocation and none of the fourteen refusal reasons applies. It does not certify disclosure compliance, and a governed classification asserts nothing about whether ABS-0004 Section 4.7's constraints were met. Neither the documentation nor any summary may describe a governed result as a valid authorization under the full set of adopted ABS-0004 constraints, because the Section 4.7 constraints are excluded from what is checked.

=== EVIDENCE ABS-0004:v8:S3#adopted_constraint:a-disclosure-violation-under-4-7-i ===
A disclosure violation under 4.7 is a classification,
not a detection. Nothing in this ontology detects that a subordinate
execution went undeclared. A violation is recorded when someone establishes
it by other means. No statement in this document or in any summary of it may
describe undeclared execution as surfaced, caught, or prevented by these
constraints.

=== EVIDENCE ABS-0004:v8:S3#def:subordinate-authorization-inherita ===
Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
For the plan’s deliberately narrowed definition, fourteen is complete by definition: “valid authorization” means coverage plus absence of those fourteen reasons. It is not complete for authorization under the full ABS-0004 constraint set.

The enumeration lacks refusals for the three excluded Section 4.7 disclosure constraints, including refusal where:

1. required outbound-interaction disclosure/logging is absent;
2. required input/configuration disclosure cannot be established from the partial manifest; and
3. a subordinate execution was never disclosed as an Invocation.

The third is particularly material. Reason 11 reaches only a subordinate execution that is represented and outside its parent’s declared classes. It does not refuse an undeclared subordinate execution. The plan expressly acknowledges that such an invocation can pass every slice check and be classified governed.

The current wording does meet the prior reviewer’s stated condition on terminology. Scope 7 confines “valid authorization” to the fourteen-check slice, says it “does not certify disclosure compliance,” and prohibits describing a governed result as valid under the full adopted ABS-0004 constraints. Thus it excludes Section 4.7 checks without retaining the implication that those checks were performed.

The evidence does not include the actual text of ABS-0004 Section 4.7. That text would be needed to state the exact normative names and conditions of the three missing disclosure refusals, and to determine whether Section 4.7 contains any further constraints beyond the three described by the plan.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Q6 — Two-part analysis

### Part 1: Is fourteen complete for what the plan means by "valid authorization"?

The enumeration in scope[4] is presented as complete for what **authorize() can check from stored records** — that is a narrower claim than completeness for "valid authorization" as such. The evidence itself names the gap directly:

> "An invocation with a required disclosure absent can pass every check in this slice and be classified governed. That is a stated limit of the slice, not a gap the fixtures will catch."

So the missing refusal is: **a refusal reason for undisclosed subordinate execution under 4.7** — an invocation "never disclosed as an Invocation at all," which the evidence distinguishes from reason 11:

> "Reason 11 therefore reaches a subordinate that IS represented and exceeds its declared classes, and does not reach one never disclosed as an Invocation at all, which ABS-0004 Section 3 calls not an implicitly authorized act."

This is not an oversight of the kind COMP-0037/COMP-0043 caught (missing reasons, conflated reasons) — it is a structural exclusion, defended on the grounds that "none is checkable from stored records." Whether that defense is sound cannot be verified from what's here: **the actual text of ABS-0004 Section 4.7's three disclosure constraints is not in evidence**, only scope[4]'s characterization of them (OutboundInteractionLog deferred, EffectiveInputManifest self-attesting partiality, undisclosed subordinate requiring absence-detection). I would need Section 4.7 itself to check whether the claim "none is checkable from stored records" holds for all three constraints or only some, and whether a fifteenth reason could be constructed from records other than the three named.

So: fourteen is internally complete for the authorize() function's declared scope (checkable-from-stored-records refusals). It is **not** complete for "valid authorization" in any sense that includes disclosure compliance — and the plan does not claim otherwise for authorize() itself. The gap is transferred to the classify() layer, addressed in Part 2.

### Part 2: Does the wording meet the prior reviewer's condition?

Note first: **the prior reviewer's condition itself is not in evidence** — only the question's paraphrase of it ("the plan must then not describe its result as a valid authorization under the adopted constraints"). I am checking the plan's wording against that paraphrase, not against a quoted ruling.

Against that paraphrase, scope[7]'s language tracks it closely:

> "Neither the documentation nor any summary may describe a governed result as a valid authorization under the full set of adopted ABS-0004 constraints, because the Section 4.7 constraints are excluded from what is checked."

and

> "'Valid authorization' here means only that an authorization record covers the invocation and none of the fourteen refusal reasons applies. It does not certify disclosure compliance, and a governed classification asserts nothing about whether ABS-0004 Section 4.7's constraints were met."

On its face this satisfies the condition: it explicitly disclaims the reading the reviewer was guarding against, using close to the same phrase ("valid authorization under the full set of adopted ABS-0004 constraints").

But the retained term is still "valid authorization" and the retained classification label is still "governed" — words that carry an affirmative connotation independent of the disclaimer attached to them here. The disclaimer is scoped to *this* passage ("here means only..."). Nothing in the evidence shows whether "governed" or "valid authorization" is used elsewhere in the plan (summaries, other sections) without the qualifying sentence attached — and that is exactly the failure mode the condition was written to prevent: excluding the checks while the label continues to do the work of implying they were made. This evidence set doesn't include the rest of the plan's documentation or any external summary, so I can't confirm the qualifier travels with the term everywhere it's used.

Given disclosure 3 — that the same executor who drafted v8's disclosure language also proposed the dispositions on which broken-citation claims still applied — there is reason not to take the presence of one well-worded disclaimer as settling the matter. A party correcting its own prior overreach has an incentive to write the disclaimer precisely once, at the definition site, while the operative label ("governed") continues to circulate elsewhere carrying its ordinary meaning.

**Conclusion:** The quoted passage in scope[7] meets the condition as stated, textually and directly. Whether the plan as a whole meets it depends on usage outside this passage, which is not in evidence — that is the specific gap: a survey of every place "governed" or "valid authorization" appears in the plan's documentation and summaries, to confirm the disclaimer is not confined to one definitional sentence while the label does unqualified work elsewhere.
```
