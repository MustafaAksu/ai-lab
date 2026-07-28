# COMP-0072: Provider Comparison — Claim extraction v2 EX-Q5-gpt-5-6-terra

## Metadata

- comparison_id: `COMP-0072`
- title: `Claim extraction v2 EX-Q5-gpt-5-6-terra`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-11a6e1ee0b2c8f93.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0072", "target_id": "INV-11a6e1ee0b2c8f93"}, {"authoritative": false, "evidence": "docs/invocations/INV-6674f95e9b23da23.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0072", "target_id": "INV-6674f95e9b23da23"}]`
- created_at: `2026-07-28T20:13:44.564213+00:00`
- command: `scripts/compare_providers.py --title Claim extraction v2 EX-Q5-gpt-5-6-terra You are extracting claims from a review answer so they can be recorded as separate, addressable records. You are not evaluating the answer and not deciding whether any claim is correct.

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

=== QUESTION THAT WAS ASKED (Q5) ===
The plan makes the one-hop bound machine-visible through a check_depth field on the authorization outcome, and states that as a result "a consumer cannot read a permitted result as a general independence finding."

Does a field on the result prevent that reading, or does it only give the system somewhere to point afterwards? Construct a two-hop case the one-hop check misses, and say whether check_depth is sufficient disclosure for that case. If the plan's wording claims more than a field can do, give the honest replacement.

=== ANSWER TO EXTRACT FROM ===
No. A `check_depth` field does not prevent a consumer from treating a permitted outcome as a general independence finding. It records the limit of the check; it does not constrain a consumer’s interpretation or make the unexamined ancestry safe.

A two-hop case:

1. Invocation A, executed by executor identity X, produces evidence used in preparing a target artifact.
2. Invocation B, executed by executor identity Y, produces the target artifact from that evidence.
3. Executor identity X is authorized to adjudicate a claim about the target artifact.

The proposed one-hop check examines the target artifact’s direct `produced_by` invocation, B. Since B was executed by Y rather than X, it permits the authorization.

But the target artifact’s evidence ancestry contains A, executed by X. Under proposed C3, that is a conflict: “an invocation cannot adjudicate a claim whose evidence ancestry contains an invocation by an equivalent executor identity.” The fact that X appears one hop farther back does not make X independent. The plan itself recognizes that “The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision.”

`check_depth` is useful disclosure only if its semantics unambiguously state that the outcome reflects a direct-only check and that no conclusion about deeper ancestry follows. It is not sufficient disclosure to support the stronger proposition that a consumer cannot misread the result. A consumer still can ignore, misunderstand, drop, or fail to propagate the field; and a “permitted” result still does not establish independence across untraversed lineage.

An honest replacement for the plan’s wording is:

> The self-adjudication outcome records that only a direct check was performed. A permitted result establishes no general independence finding and does not exclude equivalent-executor conflicts in deeper evidence ancestry.

The supplied evidence is sufficient to identify the conceptual two-hop miss and the overclaim. It is insufficient to determine whether the implementation would make the disclosure effective for downstream consumers. For that, the missing material is:

- the authorization-outcome schema and normative semantics for `check_depth`, including its permitted values and whether it is mandatory;
- the consumer/API/UI contract governing how consumers must retain and interpret `check_depth`; and
- the Slice D lineage representation and traversal rules needed to detect the two-hop conflict rather than merely disclose that it was not checked.

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

=== QUESTION THAT WAS ASKED (Q5) ===
The plan makes the one-hop bound machine-visible through a check_depth field on the authorization outcome, and states that as a result "a consumer cannot read a permitted result as a general independence finding."

Does a field on the result prevent that reading, or does it only give the system somewhere to point afterwards? Construct a two-hop case the one-hop check misses, and say whether check_depth is sufficient disclosure for that case. If the plan's wording claims more than a field can do, give the honest replacement.

=== ANSWER TO EXTRACT FROM ===
No. A `check_depth` field does not prevent a consumer from treating a permitted outcome as a general independence finding. It records the limit of the check; it does not constrain a consumer’s interpretation or make the unexamined ancestry safe.

A two-hop case:

1. Invocation A, executed by executor identity X, produces evidence used in preparing a target artifact.
2. Invocation B, executed by executor identity Y, produces the target artifact from that evidence.
3. Executor identity X is authorized to adjudicate a claim about the target artifact.

The proposed one-hop check examines the target artifact’s direct `produced_by` invocation, B. Since B was executed by Y rather than X, it permits the authorization.

But the target artifact’s evidence ancestry contains A, executed by X. Under proposed C3, that is a conflict: “an invocation cannot adjudicate a claim whose evidence ancestry contains an invocation by an equivalent executor identity.” The fact that X appears one hop farther back does not make X independent. The plan itself recognizes that “The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision.”

`check_depth` is useful disclosure only if its semantics unambiguously state that the outcome reflects a direct-only check and that no conclusion about deeper ancestry follows. It is not sufficient disclosure to support the stronger proposition that a consumer cannot misread the result. A consumer still can ignore, misunderstand, drop, or fail to propagate the field; and a “permitted” result still does not establish independence across untraversed lineage.

An honest replacement for the plan’s wording is:

> The self-adjudication outcome records that only a direct check was performed. A permitted result establishes no general independence finding and does not exclude equivalent-executor conflicts in deeper evidence ancestry.

The supplied evidence is sufficient to identify the conceptual two-hop miss and the overclaim. It is insufficient to determine whether the implementation would make the disclosure effective for downstream consumers. For that, the missing material is:

- the authorization-outcome schema and normative semantics for `check_depth`, including its permitted values and whether it is mandatory;
- the consumer/API/UI contract governing how consumers must retain and interpret `check_depth`; and
- the Slice D lineage representation and traversal rules needed to detect the two-hop conflict rather than merely disclose that it was not checked.

--- END OF ANSWER ---

Output the JSON now.

## OpenAI Response

- model: `gpt-5.6-terra`

```
{"claims":[{"text":"A `check_depth` field does not prevent a consumer from treating a permitted outcome as a general independence finding.","type":"finding","about":"`check_depth` field on the authorization outcome","quote":"A `check_depth` field does not prevent a consumer from treating a permitted outcome as a general independence finding."},{"text":"In the two-hop case, the proposed one-hop check permits authorization because the target artifact’s direct producing invocation B was executed by Y rather than X.","type":"finding","about":"two-hop case target artifact direct `produced_by` invocation B","quote":"Since B was executed by Y rather than X, it permits the authorization."},{"text":"In the two-hop case, the target artifact’s evidence ancestry containing A executed by X is a conflict under proposed C3.","type":"finding","about":"two-hop case evidence ancestry invocation A under proposed C3","quote":"Under proposed C3, that is a conflict:"},{"text":"X appearing one hop farther back does not make X independent.","type":"finding","about":"two-hop case executor identity X","quote":"The fact that X appears one hop farther back does not make X independent."},{"text":"`check_depth` is useful disclosure only if its semantics unambiguously state that the outcome reflects a direct-only check and that no conclusion about deeper ancestry follows.","type":"finding","about":"`check_depth` semantics","quote":"`check_depth` is useful disclosure only if its semantics unambiguously state that the outcome reflects a direct-only check and that no conclusion about deeper ancestry follows."},{"text":"`check_depth` is not sufficient disclosure to support the proposition that a consumer cannot misread the result.","type":"finding","about":"`check_depth` disclosure","quote":"It is not sufficient disclosure to support the stronger proposition that a consumer cannot misread the result."},{"text":"A permitted result does not establish independence across untraversed lineage.","type":"finding","about":"permitted authorization result","quote":"a “permitted” result still does not establish independence across untraversed lineage."},{"text":"The plan’s wording should be replaced with wording that says the self-adjudication outcome records that only a direct check was performed.","type":"recommendation","about":"plan wording about the self-adjudication outcome","quote":"The self-adjudication outcome records that only a direct check was performed."},{"text":"The supplied evidence is sufficient to identify the conceptual two-hop miss and the overclaim.","type":"finding","about":"supplied evidence","quote":"The supplied evidence is sufficient to identify the conceptual two-hop miss and the overclaim."},{"text":"The supplied evidence is insufficient to determine whether the implementation would make the disclosure effective for downstream consumers.","type":"limitation","about":"implementation effectiveness of disclosure for downstream consumers","quote":"It is insufficient to determine whether the implementation would make the disclosure effective for downstream consumers."},{"text":"The authorization-outcome schema and normative semantics for `check_depth`, including permitted values and whether it is mandatory, are missing material needed to assess disclosure effectiveness.","type":"evidence_gap","about":"authorization-outcome schema and normative `check_depth` semantics","quote":"the authorization-outcome schema and normative semantics for `check_depth`, including its permitted values and whether it is mandatory;"},{"text":"The consumer/API/UI contract governing retention and interpretation of `check_depth` is missing material needed to assess disclosure effectiveness.","type":"evidence_gap","about":"consumer/API/UI contract for `check_depth`","quote":"the consumer/API/UI contract governing how consumers must retain and interpret `check_depth`; and"},{"text":"The Slice D lineage representation and traversal rules needed to detect the two-hop conflict are missing material.","type":"evidence_gap","about":"Slice D lineage representation and traversal rules","quote":"the Slice D lineage representation and traversal rules needed to detect the two-hop conflict rather than merely disclose that it was not checked."}],"claims_omitted":0}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"claims":[{"text":"A check_depth field does not prevent a consumer from treating a permitted outcome as a general independence finding.","type":"finding","about":"check_depth field's effect on consumer interpretation","quote":"A `check_depth` field does not prevent a consumer from treating a permitted outcome as a general independence finding."},{"text":"The check_depth field records the limit of the check; it does not constrain a consumer's interpretation or make the unexamined ancestry safe.","type":"finding","about":"check_depth field's function","quote":"It records the limit of the check; it does not constrain a consumer’s interpretation or make the unexamined ancestry safe."},{"text":"In the constructed two-hop case, the proposed one-hop check examines only the target artifact's direct produced_by invocation (B), and since B was executed by Y rather than X, it permits the authorization.","type":"finding","about":"two-hop case / one-hop check behavior","quote":"Since B was executed by Y rather than X, it permits the authorization."},{"text":"In the constructed two-hop case, the target artifact's evidence ancestry contains invocation A executed by X, which under proposed C3 constitutes a conflict.","type":"finding","about":"two-hop case / C3 conflict","quote":"But the target artifact’s evidence ancestry contains A, executed by X. Under proposed C3, that is a conflict"},{"text":"The fact that X appears one hop farther back does not make X independent.","type":"finding","about":"two-hop case / independence of executor X","quote":"The fact that X appears one hop farther back does not make X independent."},{"text":"The plan itself recognizes that the one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision.","type":"finding","about":"the plan's own stated acknowledgment about the one-hop check","quote":"The one-hop self-adjudication check has the same hazard at a finer grain, since it will pass every deeper collision."},{"text":"check_depth is useful disclosure only if its semantics unambiguously state that the outcome reflects a direct-only check and that no conclusion about deeper ancestry follows.","type":"finding","about":"conditions for check_depth to be useful disclosure","quote":"`check_depth` is useful disclosure only if its semantics unambiguously state that the outcome reflects a direct-only check and that no conclusion about deeper ancestry follows."},{"text":"check_depth is not sufficient disclosure to support the stronger proposition that a consumer cannot misread the result.","type":"finding","about":"sufficiency of check_depth as disclosure","quote":"It is not sufficient disclosure to support the stronger proposition that a consumer cannot misread the result."},{"text":"A consumer can still ignore, misunderstand, drop, or fail to propagate the check_depth field.","type":"finding","about":"consumer handling of check_depth field","quote":"A consumer still can ignore, misunderstand, drop, or fail to propagate the field"},{"text":"A permitted result still does not establish independence across untraversed lineage.","type":"finding","about":"permitted authorization outcome and untraversed lineage","quote":"a “permitted” result still does not establish independence across untraversed lineage"},{"text":"An honest replacement for the plan's wording should state that the self-adjudication outcome records that only a direct check was performed, and that a permitted result establishes no general independence finding and does not exclude equivalent-executor conflicts in deeper evidence ancestry.","type":"recommendation","about":"replacement wording for the plan's claim about check_depth","quote":"The self-adjudication outcome records that only a direct check was performed. A permitted result establishes no general independence finding and does not exclude equivalent-executor conflicts in deeper evidence ancestry."},{"text":"The supplied evidence is sufficient to identify the conceptual two-hop miss and the overclaim, but insufficient to determine whether the implementation would make the disclosure effective for downstream consumers.","type":"limitation","about":"scope of the answer's conclusions given available evidence","quote":"The supplied evidence is sufficient to identify the conceptual two-hop miss and the overclaim. It is insufficient to determine whether the implementation would make the disclosure effective for downstream consumers."},{"text":"The authorization-outcome schema and normative semantics for check_depth, including its permitted values and whether it is mandatory, are missing material needed to determine disclosure effectiveness.","type":"evidence_gap","about":"authorization-outcome schema and check_depth semantics","quote":"the authorization-outcome schema and normative semantics for `check_depth`, including its permitted values and whether it is mandatory"},{"text":"The consumer/API/UI contract governing how consumers must retain and interpret check_depth is missing material needed to determine disclosure effectiveness.","type":"evidence_gap","about":"consumer/API/UI contract for check_depth","quote":"the consumer/API/UI contract governing how consumers must retain and interpret `check_depth`"},{"text":"The Slice D lineage representation and traversal rules needed to detect the two-hop conflict, rather than merely disclose that it was not checked, are missing material.","type":"evidence_gap","about":"Slice D lineage representation and traversal rules","quote":"the Slice D lineage representation and traversal rules needed to detect the two-hop conflict rather than merely disclose that it was not checked"}],"claims_omitted":0}
```
