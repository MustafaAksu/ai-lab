# COMP-0076: Provider Comparison — Claim extraction v2 EX-Q7-gpt-5-6-terra

## Metadata

- comparison_id: `COMP-0076`
- title: `Claim extraction v2 EX-Q7-gpt-5-6-terra`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-c806e8609a358ce6.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0076", "target_id": "INV-c806e8609a358ce6"}, {"authoritative": false, "evidence": "docs/invocations/INV-f1459a2b1851c438.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0076", "target_id": "INV-f1459a2b1851c438"}]`
- created_at: `2026-07-28T20:16:51.957558+00:00`
- command: `scripts/compare_providers.py --title Claim extraction v2 EX-Q7-gpt-5-6-terra You are extracting claims from a review answer so they can be recorded as separate, addressable records. You are not evaluating the answer and not deciding whether any claim is correct.

WHAT COUNTS AS A CLAIM. A claim is an assertion a reader could accept, reject, or act on. It is defined by function, not by sentence boundaries. Do NOT extract:
  - restatements of the material the answer was given;
  - intermediate steps of an argument whose conclusion you are already extracting;
  - transitions, framing, or summaries of what the answer is about.
Extract the conclusions the answer asserts, not the reasoning that reaches them.

HOW MANY. Most answers contain between 5 and 15 such claims. Extract at most 20. If more than 20 meet the definition, extract the 20 the answer's conclusions depend on most and report the number you left out in "claims_omitted". Do not pad toward 20 and do not split a claim to reach it.

Rules:

1. One assertion per claim.
2. Extract only what the answer says. Do not add, infer, complete, or improve.
3. PRESERVE HEDGES EXACTLY. If the answer says "may", "appears to", "I cannot determine", "only in the narrow sense that", or "less certain", the claim text must carry that same force. Never state a hedged claim flatly. A claim recorded more confidently than it was made is the most damaging error you can make here.
4. Give each claim a type, one of:
   - "finding": an assertion about the reviewed material
   - "recommendation": something the answer says should be done or changed
   - "evidence_gap": material the answer says it needed and did not have
   - "limitation": a stated bound on the answer's own reliability or reach
5. For each claim give "about": the specific thing it concerns, as precisely as the answer allows - for example "ABS-0004 v7 Section 3 visibility constraint", "PLAN-20260723-0002 scope[12]", "refusal reason 9". Use "unspecified" if the answer does not say.
6. QUOTE RULES, applied strictly. "quote" must be ONE contiguous span copied character-for-character from the answer, under 30 words.
   - No ellipsis. Never use "..." to bridge omitted material.
   - Never join text across bullets, list items, paragraphs, or headings.
   - Never add or remove quotation marks, brackets, or punctuation at either end.
   If no single contiguous span states the claim, choose a shorter span that supports it, or extract a different claim. A quote that reads as verbatim while having been shortened or rejoined is worse than no quote, because it cannot be checked by eye.

Output STRICT JSON and nothing else. No preamble, no commentary, no markdown fences. Exactly this shape:

{"claims":[{"text":"...","type":"finding","about":"...","quote":"..."}],
 "claims_omitted":0}

If the answer makes no extractable claim, output {"claims":[],"claims_omitted":0}.

=== QUESTION THAT WAS ASKED (Q7) ===
Which of the plan's ten success criteria are mechanically checkable as written, and which are not?

Address specifically: the audit criterion, which supplies no procedure, command, or semantics for verified_current; the cross-environment reproduction criterion, which names no environments, build inputs, or normalization rules; the coverage criterion; and criterion 4's "demonstrated against a real captured InvocationRecord", which names no record and gives no acceptance rule for "real".

Consider also whether the consequence-classification criterion can be tested at all given the state of Section 8. Name any constraint in the plan that has no corresponding check.

=== ANSWER TO EXTRACT FROM ===
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

--- END OF ANSWER ---

Output the JSON now.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are extracting claims from a review answer so they can be recorded as separate, addressable records. You are not evaluating the answer and not deciding whether any claim is correct.

WHAT COUNTS AS A CLAIM. A claim is an assertion a reader could accept, reject, or act on. It is defined by function, not by sentence boundaries. Do NOT extract:
  - restatements of the material the answer was given;
  - intermediate steps of an argument whose conclusion you are already extracting;
  - transitions, framing, or summaries of what the answer is about.
Extract the conclusions the answer asserts, not the reasoning that reaches them.

HOW MANY. Most answers contain between 5 and 15 such claims. Extract at most 20. If more than 20 meet the definition, extract the 20 the answer's conclusions depend on most and report the number you left out in "claims_omitted". Do not pad toward 20 and do not split a claim to reach it.

Rules:

1. One assertion per claim.
2. Extract only what the answer says. Do not add, infer, complete, or improve.
3. PRESERVE HEDGES EXACTLY. If the answer says "may", "appears to", "I cannot determine", "only in the narrow sense that", or "less certain", the claim text must carry that same force. Never state a hedged claim flatly. A claim recorded more confidently than it was made is the most damaging error you can make here.
4. Give each claim a type, one of:
   - "finding": an assertion about the reviewed material
   - "recommendation": something the answer says should be done or changed
   - "evidence_gap": material the answer says it needed and did not have
   - "limitation": a stated bound on the answer's own reliability or reach
5. For each claim give "about": the specific thing it concerns, as precisely as the answer allows - for example "ABS-0004 v7 Section 3 visibility constraint", "PLAN-20260723-0002 scope[12]", "refusal reason 9". Use "unspecified" if the answer does not say.
6. QUOTE RULES, applied strictly. "quote" must be ONE contiguous span copied character-for-character from the answer, under 30 words.
   - No ellipsis. Never use "..." to bridge omitted material.
   - Never join text across bullets, list items, paragraphs, or headings.
   - Never add or remove quotation marks, brackets, or punctuation at either end.
   If no single contiguous span states the claim, choose a shorter span that supports it, or extract a different claim. A quote that reads as verbatim while having been shortened or rejoined is worse than no quote, because it cannot be checked by eye.

Output STRICT JSON and nothing else. No preamble, no commentary, no markdown fences. Exactly this shape:

{"claims":[{"text":"...","type":"finding","about":"...","quote":"..."}],
 "claims_omitted":0}

If the answer makes no extractable claim, output {"claims":[],"claims_omitted":0}.

=== QUESTION THAT WAS ASKED (Q7) ===
Which of the plan's ten success criteria are mechanically checkable as written, and which are not?

Address specifically: the audit criterion, which supplies no procedure, command, or semantics for verified_current; the cross-environment reproduction criterion, which names no environments, build inputs, or normalization rules; the coverage criterion; and criterion 4's "demonstrated against a real captured InvocationRecord", which names no record and gives no acceptance rule for "real".

Consider also whether the consequence-classification criterion can be tested at all given the state of Section 8. Name any constraint in the plan that has no corresponding check.

=== ANSWER TO EXTRACT FROM ===
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

--- END OF ANSWER ---

Output the JSON now.

## OpenAI Response

- model: `gpt-5.6-terra`

```
{"claims":[{"text":"Criterion 1 is checkable at the stated fixture level.","type":"finding","about":"criterion 1 governed versus experimental classification","quote":"**Checkable at the stated fixture level**"},{"text":"Criterion 2 is mostly checkable.","type":"finding","about":"criterion 2 ten refusal reasons and no unauthorised permitted fixture path","quote":"**Mostly checkable**"},{"text":"Criterion 3 is only partly checkable as a general criterion.","type":"finding","about":"criterion 3 unterminated chain and out-of-scope standing authority","quote":"**Only partly checkable as a general criterion**"},{"text":"Criterion 4 is partly checkable but not fully mechanically checkable as written.","type":"finding","about":"criterion 4 one-hop self-adjudication and real captured InvocationRecord","quote":"**Partly checkable; not fully checkable as written**"},{"text":"Criterion 5 is not fully mechanically checkable against Section 8 as it stands.","type":"finding","about":"criterion 5 consequence classification and Section 8","quote":"**Not fully mechanically checkable against Section 8 as it stands**"},{"text":"Criterion 6 is partly checkable.","type":"finding","about":"criterion 6 qualification scope","quote":"**Partly checkable**"},{"text":"Criterion 7 is partly checkable.","type":"finding","about":"criterion 7 self-issued marking and independence","quote":"**Partly checkable**"},{"text":"Criterion 8 is checkable at the stated fixture level.","type":"finding","about":"criterion 8 Slice A/B regression","quote":"**Checkable at the stated fixture level**"},{"text":"Criterion 9 is not fully mechanically checkable as written.","type":"finding","about":"criterion 9 test coverage and offline suite","quote":"**Not fully mechanically checkable as written**"},{"text":"Criterion 10 is not mechanically checkable as written.","type":"finding","about":"criterion 10 audit and cross-environment reproduction","quote":"**Not mechanically checkable as written**"},{"text":"The admission-warrant scope and expansion constraint has no corresponding direct success-criterion check.","type":"finding","about":"admission-warrant scope and expansion constraint","quote":"has no success criterion that checks an admission warrant or compares implementation scope against it."},{"text":"The exact ABS-0004 v7 field names and semantics constraint has no corresponding direct success-criterion check.","type":"finding","about":"ABS-0004 v7 field names and semantics","quote":"No criterion performs a general conformance comparison against v7."},{"text":"The GraphRelation and registered Slice A/B/C predicate restriction has no corresponding direct success-criterion check.","type":"finding","about":"GraphRelation and registered Slice A/B/C predicate restriction","quote":"No criterion checks that all relations use `GraphRelation` or that no predicate falls outside the registered lists."},{"text":"The purity of `authorize()` constraint has no corresponding direct success-criterion check.","type":"finding","about":"purity of authorize()","quote":"No criterion directly checks that `authorize()` has “no I/O, no clock, no network,”"},{"text":"The no-alteration constraint for Slice A/B fields, paths, or defaults has no corresponding direct success-criterion check.","type":"finding","about":"Slice A/B fields, paths, and defaults","quote":"does not directly check the constraint’s stronger prohibition on changing any field, path, or default."},{"text":"The combined constraint of no provider-call behavior change and no execution refusal has no corresponding direct success-criterion check.","type":"finding","about":"provider-call behavior and execution refusal","quote":"**No provider-call behavior change and no execution refusal**"},{"text":"The standing-authority constraint has a partial corresponding check in criterion 3.","type":"finding","about":"standing-authority constraint and criterion 3","quote":"The standing-authority constraint does have a partial corresponding check in criterion 3】【：】【“】【"},{"text":"None of these criteria or constraints presently has governance force.","type":"finding","about":"the criteria and constraints","quote":"none of these criteria or constraints presently has governance force."}],"claims_omitted":0}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"claims":[
{"text":"The success criteria are not uniformly mechanically checkable as written; some specify fixture-level assertions that can be automated while others depend on undefined terms, missing procedures, or open ontology material.","type":"finding","about":"overall mechanical checkability of the ten success criteria","quote":"The criteria are not uniformly mechanically checkable as written. Several specify fixture-level assertions that can be automated; others depend on undefined terms, missing procedures, or ontology material explicitly left open."},
{"text":"Criterion 1 (governed vs experimental classification) is checkable at the stated fixture level, though the meaning of 'valid authorization' depends on the authorization validator and authorize() rules.","type":"finding","about":"Criterion 1 governed/experimental classification","quote":"It supplies an operational outcome rule—“governed when a valid authorization covers it and experimental otherwise”—and requires fixtures for both outcomes."},
{"text":"Criterion 2 (ten refusal reasons, no unauthorised-permitted path) is mostly checkable via fixtures, but it is not a proof that all possible implementation paths behave so, since no path model or exhaustive-input domain is specified.","type":"finding","about":"Criterion 2 refusal reasons and unauthorised-permitted path","quote":"It is not a proof that *all possible* implementation paths behave so, because neither a path model nor exhaustive-input domain is specified."},
{"text":"Criterion 3 (unterminated chain / out-of-scope standing authority) is only partly checkable because authority_scope has no supplied grammar or matching semantics, so a machine cannot generally determine that an authorization is outside a declared scope.","type":"finding","about":"Criterion 3 authority_scope check","quote":"Without those, a machine cannot generally determine that a particular authorization is “outside” a declared scope; it can only test implementation-selected examples."},
{"text":"Criterion 4's requirement of demonstration against a 'real captured InvocationRecord' is not checkable because no InvocationRecord is named, no capture record is supplied, and no acceptance rule distinguishes 'real captured' from a constructed fixture.","type":"finding","about":"Criterion 4 real captured InvocationRecord requirement","quote":"The required demonstration “against a real captured InvocationRecord” is not: no InvocationRecord is named, no capture record is supplied, and no acceptance rule distinguishes “real captured” from a constructed fixture."},
{"text":"Testing criterion 4 fully would require the identified InvocationRecord and a rule or provenance criterion establishing that it is a captured record.","type":"evidence_gap","about":"Criterion 4 real captured InvocationRecord requirement","quote":"The evidence set would need the identified InvocationRecord and a rule or provenance criterion establishing that it is a captured record."},
{"text":"Criterion 5 (consequence classification) is not fully mechanically checkable against Section 8 because Section 8 labels the 'Detailed classification function' as [OPEN], leaving no definition of how modifiers acquire applicable_modifier_levels or how applicability is determined.","type":"finding","about":"Criterion 5 consequence classification vs Section 8","quote":"Section 8 labels the “Detailed classification function” `[OPEN]`."},
{"text":"Criterion 5 fixtures can only test an implementation's chosen fixture mapping, not conformity to a complete Section 8 classification function.","type":"finding","about":"Criterion 5 consequence classification testability","quote":"Thus this can test an implementation’s chosen fixture mapping, not conformity to a complete Section 8 classification function."},
{"text":"Criterion 6 (qualification scope) is only partly checkable because matching semantics for 'permitted ExecutionProfile constraints' and what makes a profile 'materially different' are not defined.","type":"finding","about":"Criterion 6 qualification scope","quote":"General enforcement is underspecified because the supplied material does not define matching semantics for “permitted ExecutionProfile constraints” or what makes a profile “materially different.”"},
{"text":"Criterion 7 (self-issued marking and independence) is only partly checkable; the 'reported as not independent by any check that asks for independent authorization' clause has no supplied interface, set of checks, or complete semantics of independence, so it is not mechanically bounded as written.","type":"finding","about":"Criterion 7 self-issued marking and independence","quote":"It is therefore not mechanically bounded as written."},
{"text":"Criterion 8 (Slice A/B regression) is checkable at the stated fixture level via byte comparison, but does not establish the broader constraint that no field, path, or default of either slice is altered for all inputs.","type":"finding","about":"Criterion 8 Slice A/B regression","quote":"It does not establish the broader constraint that “no field, path, or default of either is altered” for all inputs, but the success criterion itself is mechanically executable."},
{"text":"Criterion 9 (test coverage and offline suite) is not fully mechanically checkable as written because 'every public entrypoint' lacks a definition of public API, 'covered by tests' lacks a coverage rule, and the offline suite clause names no test command, runner, dependency-installation conditions, or offline enforcement method.","type":"finding","about":"Criterion 9 test coverage and offline suite","quote":"However, “every public entrypoint” lacks a definition of public API, and “covered by tests” lacks a coverage rule."},
{"text":"Criterion 10's audit clause cannot be evaluated because it gives no audit procedure, command, report schema, or semantics for verified_current.","type":"finding","about":"Criterion 10 audit clause / verified_current","quote":"The audit clause gives no audit procedure, command, report schema, or semantics for `ok true verified_current`."},
{"text":"Criterion 10's cross-environment reproduction clause names no environments, build inputs, dependency-resolution rules, file-selection rule, checksum algorithm, or normalization rules, making 'byte-identical checksums' incomplete.","type":"finding","about":"Criterion 10 cross-environment reproduction clause","quote":"The reproduction clause names no environments, build inputs, dependency-resolution rules, file-selection rule, checksum algorithm, or normalization rules."},
{"text":"To make criterion 5 mechanically checkable, a completed Section 8 classification function would be needed defining modifier levels, applicability conditions, evidence representation/validation rules, ordering/max behavior, and machine-validatable form of the governed downward exception.","type":"evidence_gap","about":"Criterion 5 / Section 8 classification function","quote":"the level assigned by each modifier;"},
{"text":"The admission-warrant scope and expansion constraint has no success criterion checking an admission warrant or comparing implementation scope against it.","type":"finding","about":"Admission-warrant scope and expansion constraint","quote":"The constraint that implementation is authorized only within a future admission warrant, and that expansion needs a separate plan, has no success criterion that checks an admission warrant or compares implementation scope against it."},
{"text":"No criterion performs a general conformance comparison against ABS-0004 v7's exact field names and semantics, and the omission of referenced Sections 4.9 and 4.13 plus Section 8's open status means a complete conformance check could not be constructed from the evidence set.","type":"finding","about":"ABS-0004 v7 field-and-semantics conformance constraint","quote":"Moreover, the supplied evidence omits the referenced Sections 4.9 and 4.13 and leaves Section 8’s detailed function open, so a complete conformance check could not be constructed from this evidence set."},
{"text":"No criterion checks that all relations use GraphRelation or that no predicate falls outside the registered Slice A/B/C lists, and the GraphRelation shape and predicate lists are not supplied.","type":"finding","about":"GraphRelation and registered Slice A/B/C predicate restriction constraint","quote":"No criterion checks that all relations use `GraphRelation` or that no predicate falls outside the registered lists."},
{"text":"No criterion directly checks the purity of authorize() (no I/O, no clock, no network, caller-supplied timestamp), and criterion 9's offline-suite condition does not establish purity.","type":"finding","about":"Purity constraint on authorize()","quote":"No criterion directly checks that `authorize()` has “no I/O, no clock, no network,” or that its timestamp is supplied by the caller."},
{"text":"No success criterion executes an invocation flow to verify that classification or authorization refusal does not block execution, despite the plan stating no provider-call behavior change and no execution refusal.","type":"finding","about":"No provider-call behavior change / no execution refusal constraint","quote":"No success criterion executes an invocation flow and verifies that classification or authorization refusal does not block execution."},
{"text":"Because both the amendment and plan remain proposed and not admitted, none of the discussed criteria or constraints presently has governance force.","type":"limitation","about":"governance force of the plan's criteria and constraints","quote":"Because both the amendment and plan remain proposed and not admitted, none of these criteria or constraints presently has governance force."}
],
"claims_omitted":6}
```
