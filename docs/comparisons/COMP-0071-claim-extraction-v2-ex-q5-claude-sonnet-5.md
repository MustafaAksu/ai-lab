# COMP-0071: Provider Comparison — Claim extraction v2 EX-Q5-claude-sonnet-5

## Metadata

- comparison_id: `COMP-0071`
- title: `Claim extraction v2 EX-Q5-claude-sonnet-5`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-e15a532dbca21244.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0071", "target_id": "INV-e15a532dbca21244"}, {"authoritative": false, "evidence": "docs/invocations/INV-aa53045886fa82bb.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0071", "target_id": "INV-aa53045886fa82bb"}]`
- created_at: `2026-07-28T20:13:02.595936+00:00`
- command: `scripts/compare_providers.py --title Claim extraction v2 EX-Q5-claude-sonnet-5 You are extracting claims from a review answer so they can be recorded as separate, addressable records. You are not evaluating the answer and not deciding whether any claim is correct.

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
**Does the field prevent the reading, or only allow the system to point at something afterward?**

A field is data, not a control. `check_depth` is written by the same `authorize()` call that already decided to permit; nothing about its presence changes what the check inspected, and nothing about its presence forces a downstream consumer to branch on it. The plan's own scope text confirms the check inspects only "the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization" — a single relation, checked once. `check_depth` is appended to the outcome to *record* that fact. Whether a consumer reads the outcome correctly depends entirely on whether the consumer's logic treats `check_depth != full-ancestry` as a reason to withhold a broader conclusion — which is downstream behavior this plan does not implement (the plan is explicit elsewhere that "Authorization classifies; it does not gate"). So: the field gives the system somewhere honest to point when asked; it does not stop a consumer from reading a permitted, undifferentiated-looking result as clearance. The plan's sentence — "a consumer cannot read a permitted result as a general independence finding" — overstates what a field does. Nothing about a field's mere presence makes a misreading impossible; it makes a misreading *avoidable by an attentive reader*, which is a different and weaker claim.

**Two-hop case the one-hop check misses**

Let executor A produce artifact X (`X produced_by A`). Executor B, reviewing or transforming X, produces artifact Y, where Y's evidence ancestry includes X (Y derived from/spawned from X, X `produced_by` A). A is now asked to adjudicate a claim resting on Y.

The one-hop check looks only at Y's direct `produced_by` relation, which names B, not A. A ≠ B, so the check passes and authorization is permitted — even though A sits in Y's evidence ancestry exactly two hops back, which is precisely the condition C3 prohibits: "an invocation cannot adjudicate a claim whose evidence ancestry contains an invocation by an equivalent executor identity." C3's own language is ancestry-wide ("evidence ancestry contains"), not one-hop; the plan's non-goals concede this directly — "the one-hop check implements C3's most direct case only."

**Is `check_depth` sufficient disclosure for this case?**

Only in a narrow, self-referential sense: it correctly tells a reader that the check that produced this outcome examined a single hop and no further. That is honest disclosure of the *check's* limitation. It is not disclosure of *this case*: `check_depth` is a fixed label attached to every outcome, permitted or refused — it carries no information about whether an actual two-hop collision exists for this particular artifact. A consumer who wants to know "is A independent of everything that fed into Y" gets no signal from `check_depth` beyond "this result didn't check that." It cannot distinguish the two-hop-clean case from the two-hop-colliding case above; both come back permitted, both carry the identical `check_depth: direct` value. So the field discloses the shape of the gap, not the presence of a gap instance. That is necessary but not sufficient to prevent the independence misreading in the actual two-hop case — the actual prevention would require either (a) a consumer that refuses to treat any `check_depth: direct` permitted-result as evidence for adjudicator independence, or (b) the ancestry traversal itself, which is explicitly deferred to Slice D.

**Honest replacement for the plan's wording**

Replace "a consumer cannot read a permitted result as a general independence finding" with something like: *"the outcome discloses that the self-adjudication check examined only the artifact's direct producer relation; a consumer that treats a permitted result as ruling out same-executor conflicts further back in the evidence ancestry is misusing the field, and no mechanism in this slice prevents that misuse — only Slice D's ancestry traversal can establish or rule out such a conflict."* This keeps the field's actual function (an honest, checkable label of scope) without claiming it does the work of a control it isn't.

**Evidence gaps worth naming**

- No definition in the evidence set of what values `check_depth` may take beyond "direct" (is it an enum anticipating future multi-hop depths, or a constant?) — needed to know whether this field is designed to compose with a future Slice D depth value or is a one-off marker.
- No Slice D specification present (traversal rules, what "evidence ancestry" resolves to as a graph operation, termination conditions for cycles/joins). Needed to evaluate how the two-hop case above would actually be caught once implemented, and whether `check_depth` values would need to change retroactively for records produced under Slice C.
- No documentation excerpt from `AUTHORIZATION_RECORDS.md` (an expected output, not included here) showing how the "stated limitations including the one-hop bound" are worded for consumers — needed to check whether the *documentation* makes the honest claim this answer recommends, independent of the field.

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
**Does the field prevent the reading, or only allow the system to point at something afterward?**

A field is data, not a control. `check_depth` is written by the same `authorize()` call that already decided to permit; nothing about its presence changes what the check inspected, and nothing about its presence forces a downstream consumer to branch on it. The plan's own scope text confirms the check inspects only "the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization" — a single relation, checked once. `check_depth` is appended to the outcome to *record* that fact. Whether a consumer reads the outcome correctly depends entirely on whether the consumer's logic treats `check_depth != full-ancestry` as a reason to withhold a broader conclusion — which is downstream behavior this plan does not implement (the plan is explicit elsewhere that "Authorization classifies; it does not gate"). So: the field gives the system somewhere honest to point when asked; it does not stop a consumer from reading a permitted, undifferentiated-looking result as clearance. The plan's sentence — "a consumer cannot read a permitted result as a general independence finding" — overstates what a field does. Nothing about a field's mere presence makes a misreading impossible; it makes a misreading *avoidable by an attentive reader*, which is a different and weaker claim.

**Two-hop case the one-hop check misses**

Let executor A produce artifact X (`X produced_by A`). Executor B, reviewing or transforming X, produces artifact Y, where Y's evidence ancestry includes X (Y derived from/spawned from X, X `produced_by` A). A is now asked to adjudicate a claim resting on Y.

The one-hop check looks only at Y's direct `produced_by` relation, which names B, not A. A ≠ B, so the check passes and authorization is permitted — even though A sits in Y's evidence ancestry exactly two hops back, which is precisely the condition C3 prohibits: "an invocation cannot adjudicate a claim whose evidence ancestry contains an invocation by an equivalent executor identity." C3's own language is ancestry-wide ("evidence ancestry contains"), not one-hop; the plan's non-goals concede this directly — "the one-hop check implements C3's most direct case only."

**Is `check_depth` sufficient disclosure for this case?**

Only in a narrow, self-referential sense: it correctly tells a reader that the check that produced this outcome examined a single hop and no further. That is honest disclosure of the *check's* limitation. It is not disclosure of *this case*: `check_depth` is a fixed label attached to every outcome, permitted or refused — it carries no information about whether an actual two-hop collision exists for this particular artifact. A consumer who wants to know "is A independent of everything that fed into Y" gets no signal from `check_depth` beyond "this result didn't check that." It cannot distinguish the two-hop-clean case from the two-hop-colliding case above; both come back permitted, both carry the identical `check_depth: direct` value. So the field discloses the shape of the gap, not the presence of a gap instance. That is necessary but not sufficient to prevent the independence misreading in the actual two-hop case — the actual prevention would require either (a) a consumer that refuses to treat any `check_depth: direct` permitted-result as evidence for adjudicator independence, or (b) the ancestry traversal itself, which is explicitly deferred to Slice D.

**Honest replacement for the plan's wording**

Replace "a consumer cannot read a permitted result as a general independence finding" with something like: *"the outcome discloses that the self-adjudication check examined only the artifact's direct producer relation; a consumer that treats a permitted result as ruling out same-executor conflicts further back in the evidence ancestry is misusing the field, and no mechanism in this slice prevents that misuse — only Slice D's ancestry traversal can establish or rule out such a conflict."* This keeps the field's actual function (an honest, checkable label of scope) without claiming it does the work of a control it isn't.

**Evidence gaps worth naming**

- No definition in the evidence set of what values `check_depth` may take beyond "direct" (is it an enum anticipating future multi-hop depths, or a constant?) — needed to know whether this field is designed to compose with a future Slice D depth value or is a one-off marker.
- No Slice D specification present (traversal rules, what "evidence ancestry" resolves to as a graph operation, termination conditions for cycles/joins). Needed to evaluate how the two-hop case above would actually be caught once implemented, and whether `check_depth` values would need to change retroactively for records produced under Slice C.
- No documentation excerpt from `AUTHORIZATION_RECORDS.md` (an expected output, not included here) showing how the "stated limitations including the one-hop bound" are worded for consumers — needed to check whether the *documentation* makes the honest claim this answer recommends, independent of the field.

--- END OF ANSWER ---

Output the JSON now.

## OpenAI Response

- model: `gpt-5.6-terra`

```
{"claims":[{"text":"A field is data, not a control.","type":"finding","about":"check_depth field on the authorization outcome","quote":"A field is data, not a control."},{"text":"The presence of check_depth does not force a downstream consumer to branch on it.","type":"finding","about":"downstream consumers of check_depth","quote":"nothing about its presence forces a downstream consumer to branch on it."},{"text":"The plan does not implement downstream behavior that treats a non-full-ancestry check_depth as a reason to withhold a broader conclusion.","type":"finding","about":"plan downstream consumer behavior for check_depth","quote":"downstream behavior this plan does not implement"},{"text":"check_depth does not stop a consumer from reading a permitted result as clearance.","type":"finding","about":"check_depth field on permitted authorization results","quote":"it does not stop a consumer from reading a permitted, undifferentiated-looking result as clearance."},{"text":"The plan's statement that a consumer cannot read a permitted result as a general independence finding overstates what a field does.","type":"finding","about":"plan wording about consumer interpretation of permitted results","quote":"overstates what a field does."},{"text":"A field makes a misreading avoidable by an attentive reader, rather than making a misreading impossible.","type":"finding","about":"check_depth field disclosure effect","quote":"it makes a misreading *avoidable by an attentive reader*, which is a different and weaker claim."},{"text":"In the two-hop case, the one-hop check passes and authorization is permitted even though A is in Y's evidence ancestry two hops back.","type":"finding","about":"two-hop A-to-X-to-Y self-adjudication case","quote":"A ≠ B, so the check passes and authorization is permitted — even though A sits in Y's evidence ancestry exactly two hops back"},{"text":"The one-hop check implements only C3's most direct case.","type":"finding","about":"C3 implementation scope","quote":"the one-hop check implements C3's most direct case only."},{"text":"check_depth correctly tells a reader that the check examined a single hop and no further.","type":"finding","about":"check_depth disclosure of check scope","quote":"it correctly tells a reader that the check that produced this outcome examined a single hop and no further."},{"text":"check_depth is not disclosure of whether an actual two-hop collision exists for a particular artifact.","type":"finding","about":"check_depth disclosure in the two-hop case","quote":"It is not disclosure of *this case*:"},{"text":"check_depth carries no information about whether an actual two-hop collision exists for a particular artifact.","type":"finding","about":"check_depth value on authorization outcomes","quote":"it carries no information about whether an actual two-hop collision exists for this particular artifact."},{"text":"check_depth cannot distinguish a two-hop-clean case from the described two-hop-colliding case.","type":"finding","about":"check_depth value in two-hop ancestry cases","quote":"It cannot distinguish the two-hop-clean case from the two-hop-colliding case above"},{"text":"check_depth is necessary but not sufficient to prevent the independence misreading in the actual two-hop case.","type":"finding","about":"check_depth sufficiency for two-hop independence interpretation","quote":"That is necessary but not sufficient to prevent the independence misreading in the actual two-hop case"},{"text":"Actual prevention would require either a consumer that refuses to treat direct-only permitted results as evidence of adjudicator independence or ancestry traversal.","type":"recommendation","about":"prevention of independence misreading for direct-only authorization results","quote":"the actual prevention would require either (a) a consumer that refuses to treat any `check_depth: direct` permitted-result as evidence for adjudicator independence, or (b) the ancestry traversal itself"},{"text":"The plan wording should replace the claim that a consumer cannot read a permitted result as a general independence finding.","type":"recommendation","about":"plan wording about consumer interpretation of permitted results","quote":"Replace \"a consumer cannot read a permitted result as a general independence finding\""},{"text":"The evidence set does not define what values check_depth may take beyond \"direct.\"","type":"evidence_gap","about":"check_depth permitted values","quote":"No definition in the evidence set of what values `check_depth` may take beyond \"direct\""},{"text":"No Slice D specification is present for traversal rules, evidence-ancestry graph resolution, or cycle and join termination conditions.","type":"evidence_gap","about":"Slice D ancestry traversal specification","quote":"No Slice D specification present (traversal rules, what \"evidence ancestry\" resolves to as a graph operation, termination conditions for cycles/joins)."},{"text":"No documentation excerpt from AUTHORIZATION_RECORDS.md is included showing how the one-hop bound's limitations are worded for consumers.","type":"evidence_gap","about":"AUTHORIZATION_RECORDS.md consumer-facing limitation documentation","quote":"No documentation excerpt from `AUTHORIZATION_RECORDS.md`"}],"claims_omitted":0}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"claims":[
{"text":"A field is data, not a control.","type":"finding","about":"check_depth field nature","quote":"A field is data, not a control."},
{"text":"check_depth is written by the same authorize() call that already decided to permit; its presence doesn't change what the check inspected and doesn't force a downstream consumer to branch on it.","type":"finding","about":"check_depth field mechanics","quote":"nothing about its presence changes what the check inspected, and nothing about its presence forces a downstream consumer to branch on it"},
{"text":"The plan's scope text confirms the check inspects only a single produced_by relation to an InvocationRecord matching the executor, checked once.","type":"finding","about":"one-hop check scope","quote":"the artifact carries a produced_by relation to an InvocationRecord whose executed_by equals the executor under authorization"},
{"text":"Whether a consumer reads the outcome correctly depends entirely on whether the consumer's logic treats check_depth != full-ancestry as a reason to withhold a broader conclusion, which is downstream behavior this plan does not implement.","type":"finding","about":"consumer logic dependency on check_depth","quote":"Whether a consumer reads the outcome correctly depends entirely on whether the consumer's logic treats `check_depth != full-ancestry` as a reason to withhold a broader conclusion — which is downstream behavior this plan does not implement"},
{"text":"The plan states elsewhere that authorization classifies but does not gate.","type":"finding","about":"plan's stated authorization behavior","quote":"Authorization classifies; it does not gate"},
{"text":"The field gives the system somewhere honest to point when asked; it does not stop a consumer from reading a permitted, undifferentiated-looking result as clearance.","type":"finding","about":"check_depth field's actual function","quote":"the field gives the system somewhere honest to point when asked; it does not stop a consumer from reading a permitted, undifferentiated-looking result as clearance"},
{"text":"The plan's sentence that a consumer cannot read a permitted result as a general independence finding overstates what a field can do.","type":"finding","about":"plan's wording overstatement","quote":"The plan's sentence — \"a consumer cannot read a permitted result as a general independence finding\" — overstates what a field does."},
{"text":"A field's mere presence makes a misreading avoidable by an attentive reader, not impossible, which is a weaker claim than the plan asserts.","type":"finding","about":"limits of field's protective effect","quote":"it makes a misreading *avoidable by an attentive reader*, which is a different and weaker claim"},
{"text":"A constructed two-hop case: executor A produces artifact X; executor B produces artifact Y whose evidence ancestry includes X; A is then asked to adjudicate a claim resting on Y, creating a same-executor conflict two hops back that the one-hop check would miss.","type":"finding","about":"constructed two-hop adjudication case","quote":"Let executor A produce artifact X (`X produced_by A`). Executor B, reviewing or transforming X, produces artifact Y, where Y's evidence ancestry includes X"},
{"text":"In this case the one-hop check looks only at Y's direct produced_by relation naming B, so A≠B and authorization is permitted even though A sits two hops back in Y's evidence ancestry, which is the condition C3 prohibits.","type":"finding","about":"two-hop case outcome under one-hop check","quote":"A ≠ B, so the check passes and authorization is permitted — even though A sits in Y's evidence ancestry exactly two hops back, which is precisely the condition C3 prohibits"},
{"text":"C3's language is ancestry-wide, not one-hop, and the plan's non-goals concede the one-hop check implements only C3's most direct case.","type":"finding","about":"C3 requirement vs one-hop check scope","quote":"the one-hop check implements C3's most direct case only"},
{"text":"check_depth is sufficient disclosure only in a narrow, self-referential sense: it correctly tells a reader that the check examined a single hop and no further, which is honest disclosure of the check's own limitation but not of the specific case.","type":"finding","about":"sufficiency of check_depth disclosure","quote":"Only in a narrow, self-referential sense: it correctly tells a reader that the check that produced this outcome examined a single hop and no further"},
{"text":"check_depth is a fixed label attached to every outcome and carries no information about whether an actual two-hop collision exists for a particular artifact, so it cannot distinguish a two-hop-clean case from a two-hop-colliding case.","type":"finding","about":"check_depth's inability to signal actual collisions","quote":"it carries no information about whether an actual two-hop collision exists for this particular artifact"},
{"text":"check_depth discloses the shape of the gap, not the presence of a gap instance, which is necessary but not sufficient to prevent the independence misreading in the actual two-hop case.","type":"finding","about":"sufficiency limits of check_depth disclosure","quote":"the field discloses the shape of the gap, not the presence of a gap instance"},
{"text":"Actual prevention of the misreading would require either a consumer that refuses to treat check_depth:direct permitted results as evidence for adjudicator independence, or the ancestry traversal deferred to Slice D.","type":"recommendation","about":"requirements for preventing independence misreading","quote":"the actual prevention would require either (a) a consumer that refuses to treat any `check_depth: direct` permitted-result as evidence for adjudicator independence, or (b) the ancestry traversal itself, which is explicitly deferred to Slice D"},
{"text":"The plan's wording should be replaced with language stating the outcome discloses only that the check examined the direct producer relation, that a consumer treating a permitted result as ruling out further-back same-executor conflicts is misusing the field, and that no mechanism in this slice prevents that misuse.","type":"recommendation","about":"proposed honest replacement wording","quote":"the outcome discloses that the self-adjudication check examined only the artifact's direct producer relation; a consumer that treats a permitted result as ruling out same-executor conflicts further back in the evidence ancestry is misusing the field, and no mechanism in this slice prevents that misuse"},
{"text":"There is no definition in the evidence set of what values check_depth may take beyond 'direct', needed to know whether the field is designed to compose with a future Slice D depth value or is a one-off marker.","type":"evidence_gap","about":"check_depth possible value definitions","quote":"No definition in the evidence set of what values `check_depth` may take beyond \"direct\""},
{"text":"There is no Slice D specification present (traversal rules, ancestry graph resolution, cycle/join termination), needed to evaluate how the two-hop case would be caught once implemented and whether check_depth values would need to change retroactively.","type":"evidence_gap","about":"Slice D specification","quote":"No Slice D specification present (traversal rules, what \"evidence ancestry\" resolves to as a graph operation, termination conditions for cycles/joins)"},
{"text":"There is no documentation excerpt from AUTHORIZATION_RECORDS.md showing how stated limitations including the one-hop bound are worded for consumers, needed to check whether the documentation independently makes the honest claim recommended.","type":"evidence_gap","about":"AUTHORIZATION_RECORDS.md documentation excerpt","quote":"No documentation excerpt from `AUTHORIZATION_RECORDS.md` (an expected output, not included here) showing how the \"stated limitations including the one-hop bound\" are worded for consumers"}
],
"claims_omitted":0}
```
