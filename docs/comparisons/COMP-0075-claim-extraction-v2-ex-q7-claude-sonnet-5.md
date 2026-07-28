# COMP-0075: Provider Comparison — Claim extraction v2 EX-Q7-claude-sonnet-5

## Metadata

- comparison_id: `COMP-0075`
- title: `Claim extraction v2 EX-Q7-claude-sonnet-5`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-5f30909660ca8ee2.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0075", "target_id": "INV-5f30909660ca8ee2"}, {"authoritative": false, "evidence": "docs/invocations/INV-f89e21820a5f76ca.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0075", "target_id": "INV-f89e21820a5f76ca"}]`
- created_at: `2026-07-28T20:15:53.431356+00:00`
- command: `scripts/compare_providers.py --title Claim extraction v2 EX-Q7-claude-sonnet-5 You are extracting claims from a review answer so they can be recorded as separate, addressable records. You are not evaluating the answer and not deciding whether any claim is correct.

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
## Mechanically checkable vs. not, by criterion (in the order given in `success_criteria`)

**1. Governed/experimental classification (fixtures for both outcomes).**
Checkable. The classify function and its two outcomes are fully specified in `scope`, and the criterion asks only for fixture demonstration of a binary condition.

**2. Ten refusal reasons, each exercised by fixture; no permitted outcome without a matching authorization record.**
Checkable. The ten reasons are enumerated in `scope`, `authorize()` is specified as pure, and "yields that reason" / "no fixture path returns permitted without a match" are both binary, fixture-testable conditions.

**3. Chain-terminates-nowhere refusal; authority-scope-violation refusal.**
Checkable. Both conditions are named refusal reasons over stored records, testable by constructing the corresponding fixture.

**4. One-hop self-adjudication check.**
Partially checkable, partially not. The mechanical parts — refuse when executor identities match, permit when they differ, `check_depth` field present and marked direct-only — are testable against any fixture InvocationRecord; nothing about that logic requires a "real" one. But **"demonstrated against a real captured InvocationRecord"** supplies no record identifier, no source, and no acceptance rule distinguishing a "real captured" record from a synthetic fixture. As written there is no check that can fail this clause specifically — a reviewer cannot tell whether a given fixture satisfies "real" or not. This sub-clause is not mechanically checkable; the identity-collision logic around it is.

**5. Consequence classification over the enumerated modifier set.**
Checkable only in the narrow sense the plan itself claims ("enumerated-fixture coverage... not a proof of monotonicity"). Section 8 defines `effective_consequence = max(default_consequence, applicable_modifier_levels)` precisely, so a fixture asserting the max-formula holds for a *given* set of modifier levels is testable, and "downward adjustment without a recorded governed exception is refused" is testable against the `[ADOPTED_CONSTRAINT]` on governed exceptions.
However, Section 8 also marks `[OPEN] Detailed classification function` — there is no adopted rule for *deriving* which modifier levels apply to a given invocation's actual content. So the fixtures can only assert internal consistency of the combination formula for levels the test author assigns by hand; they cannot check that the classification of any real invocation is correct, because the mapping from invocation facts to modifier levels doesn't yet exist as governance text. The criterion is checkable as a formula-consistency test, not as a classification-correctness test, and the plan's own hedge ("not a proof of monotonicity over all inputs") is doing real work here — it is narrower than "consequence classification is exercised," which could be misread as testing the classifier itself.

**6. Qualification execution-scope rejection.**
Checkable. Section 4.6 gives the scope fields explicitly (endpoint, ExecutionProfile constraints, session-state constraints, policy version); "lacking an execution scope" and "outside its scope" are both testable against the validator.

**7. Self-issued authorization: accepted, `self_issued` true, reported not-independent.**
Checkable, given the plan's own stated rule (mitigation: "exact identifier equality only"). That rule supplies the missing semantics that a bare "same party" test would otherwise lack.

**8. Regression: byte-identical Slice A/B outputs before and after.**
Checkable. "Byte-identical" is an unambiguous, mechanically comparable output; the fixture procedure (run before/after import) is stated.

**9. Coverage criterion ("every public entrypoint and every enumerated outcome," full suite passes offline).**
Not fully checkable as written. "The full suite passes offline with no network access" is checkable (pass/fail, no network calls). But "covered by tests exercising every public entrypoint and every enumerated outcome" supplies no completeness procedure: no coverage tool, no threshold, no enumerated list of "public entrypoints" against which fixtures are checked off, no definition of what counts as an "enumerated outcome" beyond the ten refusal reasons already covered by criterion 2. Whether a given test suite satisfies "every" entrypoint is a judgment call, not a mechanical check, absent a named coverage instrument or an explicit checklist artifact.

**10. Audit criterion and cross-environment reproduction.**
Not mechanically checkable as written, on both halves:
- "The repository audit reports `ok true verified_current`" — no procedure, command, tool, or semantics for `verified_current` appears anywhere in the evidence set. There is no audit specification to check this against. **Missing:** an audit-tool specification or schema document (not present in evidence) that would define what `verified_current` asserts and how it's computed — needed to know whether this is even a boolean flag, a timestamp comparison, a hash check, or something else.
- "commit-level cross-environment reproduction... yields byte-identical checksums for every delivered file" — no environments are named, no build inputs are specified, and no normalization rules (line endings, timestamps, path separators, toolchain/interpreter versions) are given. Without at least two named environments and a build procedure, "reproduction" cannot be executed, let alone checked. **Missing:** an environment/build specification (e.g., a CI matrix or reproducibility spec) that is not present in this evidence set.

## Constraints with no corresponding check

Checking the plan's top-level `constraints` list against the ten success criteria:

- **"Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan."** No success criterion tests scope containment against a warrant; there is nothing to check this against until a warrant exists, and none of the ten criteria references warrant scope at all.
- **"Field names and semantics follow ABS-0004 v7 exactly; deviations require an ABS revision first."** No criterion checks field-name/semantic conformance to the ontology text. "Field reconciliation with ABS-0004 4.13" appears in `scope`, not in `success_criteria` — it is a deliverable, not a checked outcome.
- **"All relations use the GraphRelation shape; no predicate outside the registered Slice A, B, and C lists."** No criterion checks predicate-registry conformance or relation shape; the predicate-registry entries appear as an expected output, not as something any success criterion verifies.
- **"authorize() is pure over stored records: no I/O, no clock, no network; the decision timestamp is supplied by the caller."** Only the network half is indirectly covered ("full suite passes offline with no network access" in criterion 9). "No I/O," "no clock," and "timestamp supplied by caller" have no corresponding fixture or check anywhere in the ten criteria.

## What I would have used but don't have

- ABS-0004 v7 Section 4.9 (RoleDefinition constraint fields) and Section 4.13 (DecisionRecord inherited fields) — referenced in `scope` but not in evidence; needed to assess whether criterion 3's "own reason" and the field-reconciliation deliverable are actually checkable against defined field lists.
- Any audit-tool or CI/reproducibility specification — not in evidence — needed to assess criterion 10 at all, beyond noting its absence.

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
## Mechanically checkable vs. not, by criterion (in the order given in `success_criteria`)

**1. Governed/experimental classification (fixtures for both outcomes).**
Checkable. The classify function and its two outcomes are fully specified in `scope`, and the criterion asks only for fixture demonstration of a binary condition.

**2. Ten refusal reasons, each exercised by fixture; no permitted outcome without a matching authorization record.**
Checkable. The ten reasons are enumerated in `scope`, `authorize()` is specified as pure, and "yields that reason" / "no fixture path returns permitted without a match" are both binary, fixture-testable conditions.

**3. Chain-terminates-nowhere refusal; authority-scope-violation refusal.**
Checkable. Both conditions are named refusal reasons over stored records, testable by constructing the corresponding fixture.

**4. One-hop self-adjudication check.**
Partially checkable, partially not. The mechanical parts — refuse when executor identities match, permit when they differ, `check_depth` field present and marked direct-only — are testable against any fixture InvocationRecord; nothing about that logic requires a "real" one. But **"demonstrated against a real captured InvocationRecord"** supplies no record identifier, no source, and no acceptance rule distinguishing a "real captured" record from a synthetic fixture. As written there is no check that can fail this clause specifically — a reviewer cannot tell whether a given fixture satisfies "real" or not. This sub-clause is not mechanically checkable; the identity-collision logic around it is.

**5. Consequence classification over the enumerated modifier set.**
Checkable only in the narrow sense the plan itself claims ("enumerated-fixture coverage... not a proof of monotonicity"). Section 8 defines `effective_consequence = max(default_consequence, applicable_modifier_levels)` precisely, so a fixture asserting the max-formula holds for a *given* set of modifier levels is testable, and "downward adjustment without a recorded governed exception is refused" is testable against the `[ADOPTED_CONSTRAINT]` on governed exceptions.
However, Section 8 also marks `[OPEN] Detailed classification function` — there is no adopted rule for *deriving* which modifier levels apply to a given invocation's actual content. So the fixtures can only assert internal consistency of the combination formula for levels the test author assigns by hand; they cannot check that the classification of any real invocation is correct, because the mapping from invocation facts to modifier levels doesn't yet exist as governance text. The criterion is checkable as a formula-consistency test, not as a classification-correctness test, and the plan's own hedge ("not a proof of monotonicity over all inputs") is doing real work here — it is narrower than "consequence classification is exercised," which could be misread as testing the classifier itself.

**6. Qualification execution-scope rejection.**
Checkable. Section 4.6 gives the scope fields explicitly (endpoint, ExecutionProfile constraints, session-state constraints, policy version); "lacking an execution scope" and "outside its scope" are both testable against the validator.

**7. Self-issued authorization: accepted, `self_issued` true, reported not-independent.**
Checkable, given the plan's own stated rule (mitigation: "exact identifier equality only"). That rule supplies the missing semantics that a bare "same party" test would otherwise lack.

**8. Regression: byte-identical Slice A/B outputs before and after.**
Checkable. "Byte-identical" is an unambiguous, mechanically comparable output; the fixture procedure (run before/after import) is stated.

**9. Coverage criterion ("every public entrypoint and every enumerated outcome," full suite passes offline).**
Not fully checkable as written. "The full suite passes offline with no network access" is checkable (pass/fail, no network calls). But "covered by tests exercising every public entrypoint and every enumerated outcome" supplies no completeness procedure: no coverage tool, no threshold, no enumerated list of "public entrypoints" against which fixtures are checked off, no definition of what counts as an "enumerated outcome" beyond the ten refusal reasons already covered by criterion 2. Whether a given test suite satisfies "every" entrypoint is a judgment call, not a mechanical check, absent a named coverage instrument or an explicit checklist artifact.

**10. Audit criterion and cross-environment reproduction.**
Not mechanically checkable as written, on both halves:
- "The repository audit reports `ok true verified_current`" — no procedure, command, tool, or semantics for `verified_current` appears anywhere in the evidence set. There is no audit specification to check this against. **Missing:** an audit-tool specification or schema document (not present in evidence) that would define what `verified_current` asserts and how it's computed — needed to know whether this is even a boolean flag, a timestamp comparison, a hash check, or something else.
- "commit-level cross-environment reproduction... yields byte-identical checksums for every delivered file" — no environments are named, no build inputs are specified, and no normalization rules (line endings, timestamps, path separators, toolchain/interpreter versions) are given. Without at least two named environments and a build procedure, "reproduction" cannot be executed, let alone checked. **Missing:** an environment/build specification (e.g., a CI matrix or reproducibility spec) that is not present in this evidence set.

## Constraints with no corresponding check

Checking the plan's top-level `constraints` list against the ten success criteria:

- **"Implementation is authorized only within the scope admitted by the future admission warrant; any expansion requires a separate proposed and admitted plan."** No success criterion tests scope containment against a warrant; there is nothing to check this against until a warrant exists, and none of the ten criteria references warrant scope at all.
- **"Field names and semantics follow ABS-0004 v7 exactly; deviations require an ABS revision first."** No criterion checks field-name/semantic conformance to the ontology text. "Field reconciliation with ABS-0004 4.13" appears in `scope`, not in `success_criteria` — it is a deliverable, not a checked outcome.
- **"All relations use the GraphRelation shape; no predicate outside the registered Slice A, B, and C lists."** No criterion checks predicate-registry conformance or relation shape; the predicate-registry entries appear as an expected output, not as something any success criterion verifies.
- **"authorize() is pure over stored records: no I/O, no clock, no network; the decision timestamp is supplied by the caller."** Only the network half is indirectly covered ("full suite passes offline with no network access" in criterion 9). "No I/O," "no clock," and "timestamp supplied by caller" have no corresponding fixture or check anywhere in the ten criteria.

## What I would have used but don't have

- ABS-0004 v7 Section 4.9 (RoleDefinition constraint fields) and Section 4.13 (DecisionRecord inherited fields) — referenced in `scope` but not in evidence; needed to assess whether criterion 3's "own reason" and the field-reconciliation deliverable are actually checkable against defined field lists.
- Any audit-tool or CI/reproducibility specification — not in evidence — needed to assess criterion 10 at all, beyond noting its absence.

--- END OF ANSWER ---

Output the JSON now.

## OpenAI Response

- model: `gpt-5.6-terra`

```
{"claims":[{"text":"Criterion 1's governed/experimental classification is checkable.","type":"finding","about":"success criterion 1 governed/experimental classification","quote":"Checkable."},{"text":"Criterion 2's ten refusal reasons and authorization-match condition are checkable.","type":"finding","about":"success criterion 2 refusal reasons and authorization records","quote":"Checkable."},{"text":"Criterion 3's chain-termination and authority-scope-violation refusals are checkable.","type":"finding","about":"success criterion 3 refusal reasons","quote":"Checkable."},{"text":"Criterion 4's identity-collision logic is mechanically testable against any fixture InvocationRecord.","type":"finding","about":"success criterion 4 one-hop self-adjudication identity-collision logic","quote":"are testable against any fixture InvocationRecord"},{"text":"Criterion 4's requirement for a real captured InvocationRecord is not mechanically checkable.","type":"finding","about":"success criterion 4 real captured InvocationRecord sub-clause","quote":"This sub-clause is not mechanically checkable"},{"text":"Criterion 5 is checkable only as a formula-consistency test, not as a classification-correctness test.","type":"finding","about":"success criterion 5 consequence classification","quote":"The criterion is checkable as a formula-consistency test, not as a classification-correctness test"},{"text":"The fixtures cannot check whether classification of any real invocation is correct because the mapping from invocation facts to modifier levels does not yet exist as governance text.","type":"finding","about":"Section 8 detailed classification function and success criterion 5","quote":"they cannot check that the classification of any real invocation is correct"},{"text":"Criterion 6's qualification execution-scope rejection is checkable.","type":"finding","about":"success criterion 6 qualification execution-scope rejection","quote":"Checkable."},{"text":"Criterion 7's self-issued authorization behavior is checkable under the plan's exact-identifier-equality rule.","type":"finding","about":"success criterion 7 self-issued authorization","quote":"Checkable, given the plan's own stated rule"},{"text":"Criterion 8's byte-identical Slice A/B regression output is checkable.","type":"finding","about":"success criterion 8 Slice A/B regression","quote":"Checkable."},{"text":"Criterion 9's requirement that the full suite pass offline with no network access is checkable.","type":"finding","about":"success criterion 9 offline full-suite requirement","quote":"The full suite passes offline with no network access\" is checkable"},{"text":"Criterion 9's coverage requirement is not fully checkable as written.","type":"finding","about":"success criterion 9 public-entrypoint and enumerated-outcome coverage","quote":"Not fully checkable as written."},{"text":"Criterion 10's audit requirement is not mechanically checkable because no procedure, command, tool, or semantics for verified_current is provided.","type":"finding","about":"success criterion 10 repository audit verified_current","quote":"no procedure, command, tool, or semantics for `verified_current` appears anywhere in the evidence set"},{"text":"Criterion 10's cross-environment reproduction requirement is not mechanically checkable because environments, build inputs, and normalization rules are unspecified.","type":"finding","about":"success criterion 10 cross-environment reproduction","quote":"no environments are named, no build inputs are specified, and no normalization rules"},{"text":"The constraint requiring implementation to remain within a future admission warrant's scope has no corresponding success-criterion check.","type":"finding","about":"top-level constraint on future admission-warrant scope","quote":"No success criterion tests scope containment against a warrant"},{"text":"The constraint requiring field names and semantics to follow ABS-0004 v7 exactly has no corresponding criterion check.","type":"finding","about":"top-level ABS-0004 v7 field-name and semantic conformance constraint","quote":"No criterion checks field-name/semantic conformance to the ontology text."},{"text":"The constraint requiring GraphRelation shape and registered Slice A, B, and C predicates has no corresponding criterion check.","type":"finding","about":"top-level GraphRelation and predicate-registry constraint","quote":"No criterion checks predicate-registry conformance or relation shape"},{"text":"The authorize() purity constraint's no-I/O, no-clock, and caller-supplied-timestamp requirements have no corresponding fixture or check among the ten criteria.","type":"finding","about":"top-level authorize() purity constraint","quote":"\"No I/O,\" \"no clock,\" and \"timestamp supplied by caller\" have no corresponding fixture or check"},{"text":"ABS-0004 v7 Sections 4.9 and 4.13 were not in the evidence and were needed to assess criterion 3's own-reason requirement and field reconciliation.","type":"evidence_gap","about":"ABS-0004 v7 Sections 4.9 and 4.13","quote":"referenced in `scope` but not in evidence; needed to assess whether criterion 3's \"own reason\""},{"text":"An audit-tool or CI/reproducibility specification was not in the evidence and was needed to assess criterion 10 beyond noting its absence.","type":"evidence_gap","about":"audit-tool or CI/reproducibility specification for success criterion 10","quote":"not in evidence — needed to assess criterion 10 at all, beyond noting its absence."}],"claims_omitted":0}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"claims":[
{"text":"Criterion 1 (governed/experimental classification with fixtures for both outcomes) is mechanically checkable because the classify function and its two outcomes are fully specified in scope and the criterion requires only fixture demonstration of a binary condition.","type":"finding","about":"success criterion 1 (classification fixtures)","quote":"Checkable. The classify function and its two outcomes are fully specified in `scope`, and the criterion asks only for fixture demonstration of a binary condition."},
{"text":"Criterion 2 (ten refusal reasons each exercised by fixture, no permitted outcome without matching authorization) is mechanically checkable because the ten reasons are enumerated, authorize() is specified as pure, and the pass conditions are binary and fixture-testable.","type":"finding","about":"success criterion 2 (refusal reasons)","quote":"Checkable. The ten reasons are enumerated in `scope`, `authorize()` is specified as pure, and \"yields that reason\" / \"no fixture path returns permitted without a match\" are both binary, fixture-testable conditions."},
{"text":"Criterion 3 (chain-terminates-nowhere and authority-scope-violation refusals) is mechanically checkable because both are named refusal reasons over stored records testable via fixture construction.","type":"finding","about":"success criterion 3 (chain-terminates and authority-scope refusals)","quote":"Checkable. Both conditions are named refusal reasons over stored records, testable by constructing the corresponding fixture."},
{"text":"Criterion 4's mechanical logic (refuse when executor identities match, permit when they differ, check_depth field present and marked direct-only) is testable against any fixture InvocationRecord and does not require a real one.","type":"finding","about":"success criterion 4 identity-collision logic","quote":"The mechanical parts — refuse when executor identities match, permit when they differ, `check_depth` field present and marked direct-only — are testable against any fixture InvocationRecord; nothing about that logic requires a \"real\" one."},
{"text":"The 'demonstrated against a real captured InvocationRecord' sub-clause of criterion 4 supplies no record identifier, source, or acceptance rule distinguishing 'real captured' from synthetic, so no check can fail this clause specifically and it is not mechanically checkable.","type":"finding","about":"success criterion 4 'real captured InvocationRecord' clause","quote":"As written there is no check that can fail this clause specifically — a reviewer cannot tell whether a given fixture satisfies \"real\" or not."},
{"text":"Criterion 5 (consequence classification) is checkable only in the narrow sense the plan itself claims, as enumerated-fixture coverage rather than proof of monotonicity, since Section 8's max-formula and the governed-exception constraint are testable for hand-assigned modifier levels.","type":"finding","about":"success criterion 5 consequence classification","quote":"Checkable only in the narrow sense the plan itself claims (\"enumerated-fixture coverage... not a proof of monotonicity\")."},
{"text":"Because Section 8 marks the Detailed classification function as [OPEN], there is no adopted rule for deriving which modifier levels apply to an invocation's actual content, so fixtures cannot check that classification of any real invocation is correct, only internal consistency of the combination formula.","type":"finding","about":"success criterion 5 vs Section 8 [OPEN] classification function","quote":"they cannot check that the classification of any real invocation is correct, because the mapping from invocation facts to modifier levels doesn't yet exist as governance text"},
{"text":"Criterion 6 (qualification execution-scope rejection) is mechanically checkable because Section 4.6 gives the scope fields explicitly and the relevant test conditions are testable against the validator.","type":"finding","about":"success criterion 6 (execution-scope rejection)","quote":"Checkable. Section 4.6 gives the scope fields explicitly (endpoint, ExecutionProfile constraints, session-state constraints, policy version); \"lacking an execution scope\" and \"outside its scope\" are both testable against the validator."},
{"text":"Criterion 7 (self-issued authorization accepted, self_issued true, reported not-independent) is checkable given the plan's stated 'exact identifier equality only' rule, which supplies the missing semantics.","type":"finding","about":"success criterion 7 (self-issued authorization)","quote":"Checkable, given the plan's own stated rule (mitigation: \"exact identifier equality only\"). That rule supplies the missing semantics that a bare \"same party\" test would otherwise lack."},
{"text":"Criterion 8 (byte-identical Slice A/B outputs before and after regression) is mechanically checkable because byte-identical output is unambiguous and the fixture before/after procedure is stated.","type":"finding","about":"success criterion 8 (regression check)","quote":"Checkable. \"Byte-identical\" is an unambiguous, mechanically comparable output; the fixture procedure (run before/after import) is stated."},
{"text":"The coverage criterion is not fully checkable as written because 'covered by tests exercising every public entrypoint and every enumerated outcome' supplies no completeness procedure, coverage tool, threshold, enumerated entrypoint list, or definition of 'enumerated outcome' beyond the ten refusal reasons.","type":"finding","about":"success criterion 9 (coverage criterion)","quote":"supplies no completeness procedure: no coverage tool, no threshold, no enumerated list of \"public entrypoints\" against which fixtures are checked off, no definition of what counts as an \"enumerated outcome\""},
{"text":"The 'full suite passes offline with no network access' portion of the coverage criterion is checkable as a pass/fail condition with no network calls.","type":"finding","about":"success criterion 9 offline/no-network sub-clause","quote":"The full suite passes offline with no network access\" is checkable (pass/fail, no network calls)."},
{"text":"The audit criterion's 'verified_current' clause is not mechanically checkable because no procedure, command, tool, or semantics for verified_current appears anywhere in the evidence set.","type":"finding","about":"success criterion 10 audit criterion 'verified_current'","quote":"no procedure, command, tool, or semantics for `verified_current` appears anywhere in the evidence set."},
{"text":"An audit-tool specification or schema document defining what verified_current asserts and how it is computed is missing from the evidence and would be needed to check the audit criterion.","type":"evidence_gap","about":"audit-tool specification for verified_current","quote":"an audit-tool specification or schema document (not present in evidence) that would define what `verified_current` asserts and how it's computed"},
{"text":"The cross-environment reproduction criterion is not mechanically checkable because no environments, build inputs, or normalization rules are specified, so reproduction cannot be executed or checked.","type":"finding","about":"success criterion 10 cross-environment reproduction","quote":"no environments are named, no build inputs are specified, and no normalization rules (line endings, timestamps, path separators, toolchain/interpreter versions) are given."},
{"text":"An environment/build specification such as a CI matrix or reproducibility spec is missing from the evidence set and would be needed to check the cross-environment reproduction criterion.","type":"evidence_gap","about":"environment/build specification for cross-environment reproduction","quote":"an environment/build specification (e.g., a CI matrix or reproducibility spec) that is not present in this evidence set."},
{"text":"No success criterion tests scope containment against a warrant, so the constraint that implementation is authorized only within the scope admitted by the future admission warrant has no corresponding check among the ten criteria.","type":"finding","about":"warrant-scope constraint vs success criteria","quote":"No success criterion tests scope containment against a warrant; there is nothing to check this against until a warrant exists, and none of the ten criteria references warrant scope at all."},
{"text":"No success criterion checks field-name/semantic conformance to ABS-0004 v7, since field reconciliation appears in scope as a deliverable rather than as a checked outcome in success_criteria.","type":"finding","about":"ABS-0004 v7 field-name/semantics constraint vs success criteria","quote":"No criterion checks field-name/semantic conformance to the ontology text. \"Field reconciliation with ABS-0004 4.13\" appears in `scope`, not in `success_criteria` — it is a deliverable, not a checked outcome."},
{"text":"No success criterion checks predicate-registry conformance or GraphRelation shape, since predicate-registry entries appear only as an expected output rather than something any criterion verifies.","type":"finding","about":"GraphRelation shape / predicate-registry constraint vs success criteria","quote":"No criterion checks predicate-registry conformance or relation shape; the predicate-registry entries appear as an expected output, not as something any success criterion verifies."},
{"text":"Only the network-access half of the authorize() purity constraint is indirectly covered by criterion 9; the 'no I/O', 'no clock', and 'timestamp supplied by caller' parts have no corresponding fixture or check in the ten criteria.","type":"finding","about":"authorize() purity constraint vs success criteria","quote":"\"No I/O,\" \"no clock,\" and \"timestamp supplied by caller\" have no corresponding fixture or check anywhere in the ten criteria."}
],
"claims_omitted":0}
```
