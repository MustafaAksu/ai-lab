# COMP-0124: Provider Comparison — v8 admission Q7 do-stated-bounds-make-criteria-checkable

## Metadata

- comparison_id: `COMP-0124`
- title: `v8 admission Q7 do-stated-bounds-make-criteria-checkable`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-0e214be0a8312181.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0124", "target_id": "INV-0e214be0a8312181"}, {"authoritative": false, "evidence": "docs/invocations/INV-66d544450701c648.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0124", "target_id": "INV-66d544450701c648"}]`
- created_at: `2026-07-31T13:46:54.947982+00:00`
- command: `scripts/compare_providers.py --title v8 admission Q7 do-stated-bounds-make-criteria-checkable You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q7 ===
Eight of the plan's ten success criteria now carry a stated bound describing what the criterion does and does not establish, added after a round found them not mechanically checkable as written.

Does stating a bound make a criterion checkable, or does it record that it is not and leave it in place? Go criterion by criterion for those that carry a bound, and say for each whether a person could now determine pass or fail without further judgment. Where a bound does not achieve that, give the wording that would, or say that the criterion should be removed rather than bounded.

=== EVIDENCE PLAN-20260723-0002#success_criteria (all) ===
[0] A stored invocation is classified governed when a valid authorization covers it and experimental otherwise, demonstrated by fixtures for both outcomes.

[1] Each of the fourteen enumerated refusal reasons is exercised by a fixture and yields that reason; no fixture path returns a permitted outcome without a matching authorization record. This is enumerated-fixture coverage of the fourteen named reasons; it does not establish that no implementation path can return permitted without a matching authorization.

[2] An authorization whose chain terminates nowhere is refused, and an authorization issued outside a principal's declared authority_scope is refused, each with its own reason. Checkable for the chain-termination case. The authority_scope case is checkable only against fixtures whose scopes are hand-constructed: ABS-0004 supplies no scope grammar and no matching semantics, so "outside its declared scope" cannot be evaluated in general.

[3] The one-hop self-adjudication check refuses an adjudicator authorization over an artifact produced by the same executor identity, demonstrated against a real captured InvocationRecord, permits it when the identities differ, and carries a check_depth field marking the result as direct-only in both cases. The identity-collision logic and the presence and value of check_depth are mechanically checkable against any fixture InvocationRecord. The requirement to demonstrate against a real captured InvocationRecord is not: no record is named and no selection rule is given. The criterion is met by naming the specific InvocationRecord used.

[4] Consequence classification is exercised over the enumerated modifier set: for each modifier, a fixture asserts the effective class equals the maximum of the default and the modifier level, and a downward adjustment without a recorded governed exception is refused. This is enumerated-fixture coverage of the named cases, not a proof of monotonicity over all inputs.

[5] A qualification lacking an execution scope is rejected, and a qualification is not honoured for an endpoint or execution profile outside its scope. Checkable only against fixtures whose ExecutionProfile constraints are hand-constructed: ABS-0004 Section 4.6 gives the scope fields but no matching semantics for "permitted ExecutionProfile constraints" and no definition of a materially different profile.

[6] A self-issued authorization is accepted, carries self_issued true, and is reported as not independent by any check that asks for independent authorization. Checkable under the plan's exact-identifier-equality rule for party sameness. "Any check that asks for independent authorization" is unbounded and is not checkable as written; the criterion is met against the enumerated checks this slice defines.

[7] Regression: Slice A capture and Slice B resolution are unchanged, demonstrated by a fixture that runs both against stored records before and after authorization code is importable and asserts byte-identical outputs. COMP-0037 found this constraint had no corresponding check. Byte-identical output over the fixture set is unambiguous and checkable. It does not establish the broader constraint that no field, path, or default of Slice A or Slice B was altered.

[8] The new modules are covered by tests exercising every public entrypoint and every enumerated outcome; the full suite passes offline with no network access. The offline-with-no-network condition is checkable as pass or fail. "Every public entrypoint" is not checkable as written: the criterion is met against an enumerated list of entrypoints recorded with the tests.

[9] The repository audit reports ok true verified_current, and commit-level cross-environment reproduction from the public repository yields byte-identical checksums for every delivered file. Not mechanically checkable as written and restated as two conditions with named procedures: the audit reports ok true and verification_outcome verified_current when scripts/audit_self_model_index.py is run at the delivered commit; and a second clone of the public repository at that commit yields identical sha256 for each delivered file under a recorded file list. Without the procedure, the commands, and the semantics of verified_current, neither clause could be evaluated.

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

=== QUESTION Q7 ===
Eight of the plan's ten success criteria now carry a stated bound describing what the criterion does and does not establish, added after a round found them not mechanically checkable as written.

Does stating a bound make a criterion checkable, or does it record that it is not and leave it in place? Go criterion by criterion for those that carry a bound, and say for each whether a person could now determine pass or fail without further judgment. Where a bound does not achieve that, give the wording that would, or say that the criterion should be removed rather than bounded.

=== EVIDENCE PLAN-20260723-0002#success_criteria (all) ===
[0] A stored invocation is classified governed when a valid authorization covers it and experimental otherwise, demonstrated by fixtures for both outcomes.

[1] Each of the fourteen enumerated refusal reasons is exercised by a fixture and yields that reason; no fixture path returns a permitted outcome without a matching authorization record. This is enumerated-fixture coverage of the fourteen named reasons; it does not establish that no implementation path can return permitted without a matching authorization.

[2] An authorization whose chain terminates nowhere is refused, and an authorization issued outside a principal's declared authority_scope is refused, each with its own reason. Checkable for the chain-termination case. The authority_scope case is checkable only against fixtures whose scopes are hand-constructed: ABS-0004 supplies no scope grammar and no matching semantics, so "outside its declared scope" cannot be evaluated in general.

[3] The one-hop self-adjudication check refuses an adjudicator authorization over an artifact produced by the same executor identity, demonstrated against a real captured InvocationRecord, permits it when the identities differ, and carries a check_depth field marking the result as direct-only in both cases. The identity-collision logic and the presence and value of check_depth are mechanically checkable against any fixture InvocationRecord. The requirement to demonstrate against a real captured InvocationRecord is not: no record is named and no selection rule is given. The criterion is met by naming the specific InvocationRecord used.

[4] Consequence classification is exercised over the enumerated modifier set: for each modifier, a fixture asserts the effective class equals the maximum of the default and the modifier level, and a downward adjustment without a recorded governed exception is refused. This is enumerated-fixture coverage of the named cases, not a proof of monotonicity over all inputs.

[5] A qualification lacking an execution scope is rejected, and a qualification is not honoured for an endpoint or execution profile outside its scope. Checkable only against fixtures whose ExecutionProfile constraints are hand-constructed: ABS-0004 Section 4.6 gives the scope fields but no matching semantics for "permitted ExecutionProfile constraints" and no definition of a materially different profile.

[6] A self-issued authorization is accepted, carries self_issued true, and is reported as not independent by any check that asks for independent authorization. Checkable under the plan's exact-identifier-equality rule for party sameness. "Any check that asks for independent authorization" is unbounded and is not checkable as written; the criterion is met against the enumerated checks this slice defines.

[7] Regression: Slice A capture and Slice B resolution are unchanged, demonstrated by a fixture that runs both against stored records before and after authorization code is importable and asserts byte-identical outputs. COMP-0037 found this constraint had no corresponding check. Byte-identical output over the fixture set is unambiguous and checkable. It does not establish the broader constraint that no field, path, or default of Slice A or Slice B was altered.

[8] The new modules are covered by tests exercising every public entrypoint and every enumerated outcome; the full suite passes offline with no network access. The offline-with-no-network condition is checkable as pass or fail. "Every public entrypoint" is not checkable as written: the criterion is met against an enumerated list of entrypoints recorded with the tests.

[9] The repository audit reports ok true verified_current, and commit-level cross-environment reproduction from the public repository yields byte-identical checksums for every delivered file. Not mechanically checkable as written and restated as two conditions with named procedures: the audit reports ok true and verification_outcome verified_current when scripts/audit_self_model_index.py is run at the delivered commit; and a second clone of the public repository at that commit yields identical sha256 for each delivered file under a recorded file list. Without the procedure, the commands, and the semantics of verified_current, neither clause could be evaluated.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
A stated bound does not by itself make a criterion checkable. It can make a narrower claim checkable only when the bound replaces the broader claim with a finite, specified test proposition. Where the broad claim remains as the criterion and the bound merely says what the test does not establish, the criterion remains uncheckable in that respect.

1. **Enumerated refusal reasons**

   The bounded claim—fixture coverage for fourteen named reasons and no permitted result on the tested fixture paths without a matching authorization record—could be checkable as a finite test.

   It is not checkable from this evidence without further judgment because the fourteen reasons, the fixture set, and the rule for a “matching authorization record” are not supplied here. The bound properly disclaims universal implementation-path coverage, but it does not itself identify the finite universe to test.

   Required replacement content: a recorded list of the fourteen reasons; one or more named fixtures for each; expected refusal results; and a defined authorization-record matching predicate. The universal implication that no implementation path can permit without authorization should be removed rather than retained as an implied success claim.

2. **Chain termination and authority scope**

   The chain-termination half is checkable if the fixture and its expected refusal reason are specified.

   The authority-scope half is not checkable in general. The criterion itself says that ABS-0004 supplies neither a scope grammar nor matching semantics. A hand-constructed fixture can test an implementation’s chosen behavior, but cannot determine whether an authorization is actually “outside its declared scope” under an unspecified ontology rule.

   The authority-scope clause should be removed rather than bounded as an assertion about scope compliance. If the intended claim is only a regression test, it should be rewritten as a fixed input/output assertion over named fixtures, without claiming that those results establish scope matching.

   Missing evidence: the ABS-0004 scope grammar and matching semantics referred to in the criterion.

3. **One-hop self-adjudication**

   The following parts are mechanically checkable against a specified fixture: same-identity refusal, different-identity permission, and the presence and direct-only value of `check_depth`.

   The requirement to use “a real captured InvocationRecord” is not checkable as written. No record is named, no selection rule is stated, and no provenance rule is provided for distinguishing captured from constructed records. Naming a record makes the test target determinate; it does not, by itself, establish that the record is real and captured.

   Replace the requirement with a named immutable record location and identifier, or define the provenance evidence required for a record to count as captured. If captured provenance is not material to the behavior being tested, remove “real captured” and retain only the named-record test.

   Missing evidence: the identified `InvocationRecord`, its immutable identifier or path, and any capture-provenance definition.

4. **Consequence classification**

   The bounded assertion can be checkable as finite fixture coverage only if the modifier set, modifier levels, default levels, effective-class ordering, and governed-exception representation are all fixed.

   It is not checkable from this evidence as written. “Enumerated modifier set” does not enumerate the set here, and “recorded governed exception” is not defined here. The bound correctly says that the tests do not prove monotonicity over all inputs; it does not supply the finite test domain or the semantics needed to evaluate the claimed fixture results.

   Required replacement content: a recorded modifier manifest, exact fixture inputs, expected effective classes, a defined ordering used by “maximum,” and a defined field or record condition for a governed exception. The criterion should then state only coverage of that manifest, not monotonicity over unspecified inputs.

   Missing evidence: the enumerated modifier set, class-level ordering, and governed-exception record semantics.

5. **Qualification execution scope**

   The rejection of a qualification that lacks an execution scope may be checkable if “lacking” means a specified missing or null field condition.

   The endpoint/profile clause is not checkable. The criterion acknowledges that there are no matching semantics for permitted `ExecutionProfile` constraints and no definition of “materially different profile.” Consequently, a person cannot determine whether an endpoint or profile is outside scope without supplying judgment that the criterion does not define.

   The endpoint/profile clause should be removed as a scope-compliance claim. It may instead be replaced by fixed fixture assertions over explicitly encoded profile values, but such assertions would test only the selected implementation behavior, not whether profiles are actually in or out of scope.

   Missing evidence: the ABS-0004 Section 4.6 matching semantics and a definition of material difference between execution profiles.

6. **Self-issued authorization and independence**

   Under the stated exact-identifier-equality rule, acceptance of a self-issued authorization, `self_issued true`, and a negative independence result are checkable for each named check.

   The phrase “any check that asks for independent authorization” is not checkable. The stated bound narrows that phrase to “the enumerated checks this slice defines,” but this evidence does not contain that enumeration. Thus the broad claim remains unbounded, and the narrowed target is not identified here.

   Replace “any check” with a recorded exhaustive list of checks in the slice, each with an expected negative-independence assertion. The general “any” claim should be removed.

   Missing evidence: the enumerated list of independence-authorization checks defined by the slice.

7. **Slice A and Slice B regression**

   Byte-identical output for a specified fixture set is mechanically checkable, provided that the stored records, baseline, post-change revision, command, and byte serialization being compared are fixed.

   It does not make “Slice A capture and Slice B resolution are unchanged” checkable as a general claim. The criterion expressly says that fixture equality does not establish that no field, path, or default changed. The bound therefore records the limit while leaving the broader unchanged claim in place.

   The criterion should be rewritten to say only that the named fixture records produce byte-identical outputs at the named before and after revisions. The broader assertion that the slices are unchanged should be removed unless a complete, defined comparison domain is supplied.

   Missing evidence: the named fixture, stored-record set, baseline revision, comparison revision, execution procedure, and serialization/output definition.

8. **Public entrypoints, outcomes, and offline execution**

   The full-suite offline/no-network condition is checkable if the test invocation and the means of enforcing or observing no network access are specified.

   “Every public entrypoint” is not checkable as written. The criterion proposes an enumeration, but no entrypoint list appears in this evidence. “Every enumerated outcome” likewise requires the outcome enumeration and a mapping from each item to test coverage. The bound does not make either universal claim checkable until those finite lists exist.

   Replace the universal wording with coverage of a recorded list of public entrypoints and a recorded list of outcomes, with tests mapped to each item. The claim should not imply coverage of public entrypoints or outcomes outside those lists.

   Missing evidence: the new-module inventory, public-entrypoint list, outcome list, test mapping, test command, and no-network enforcement procedure.

9. **Repository audit and cross-environment reproduction**

   This criterion is not mechanically checkable from the supplied text. It says that it has been restated as conditions with named procedures, but it does not provide the actual procedure, commands, semantics of `verified_current`, delivered-file list, or reproduction-environment conditions. The criterion itself recognizes that those omissions prevent evaluation.

   A script name alone does not define the inputs, invocation, expected output interpretation, or meaning of `verified_current`. Likewise, “a second clone” does not define the revision acquisition, file manifest, checksum command, exclusions, or environment conditions for comparison.

   Required replacement content: the exact audit command and expected machine-readable fields; the definition of `verified_current`; the delivered-file manifest; the exact SHA-256 procedure; the commit identifier; and the defined conditions for the second clone and comparison. Without those, this criterion should not remain as a pass/fail success criterion.

   Missing evidence: `scripts/audit_self_model_index.py` procedure and output semantics, the delivered-file list, the exact commands, and the reproduction protocol.

Overall, the bounds in 1, 4, 7, and 8 can support narrower fixture- or manifest-bounded criteria, but only after the finite domain and procedure are actually recorded. In 2 and 5, the missing scope semantics prevent a scope-compliance criterion rather than merely limiting its coverage. In 3, 6, and 9, the bounds identify missing determiners but do not provide them.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Framing

A stated bound does two different things depending on which criterion you look at:

- Sometimes it **narrows the claim** to a fixture-enumerable subset and disclaims the rest — in which case the narrowed claim can be checked, but only if the criterion's operative pass/fail rule is actually confined to that subset.
- Sometimes it **names an undefined term or missing artifact** (a grammar, a record, a list) — in which case the bound only documents that the criterion cannot be evaluated yet, and nothing has been made checkable.

A bound is not itself a fix. It is a diagnosis. Whether the diagnosis also supplies the cure varies criterion by criterion.

**Count discrepancy, flagged as requested:** the question states eight of ten criteria carry a bound. In the evidence supplied, bound-type qualifying language ("this is enumerated-fixture coverage… it does not establish…" or equivalent) appears on nine of the ten items — [1] through [9]. Only [0] is presented with no bound at all. I cannot reconcile "eight" against what's in front of me without seeing which of [1]–[9] the plan itself does *not* count as bounded; I flag this as a discrepancy rather than silently picking one to drop. I address all ten below.

## Criterion by criterion

**[0]** — No bound attached. As written: a stored invocation classified governed/experimental against fixtures for both outcomes. This is a binary classification with paired fixtures; a person can determine pass/fail without further judgment. Consistent with it not needing a bound.

**[1]** — Bound scopes the claim to "enumerated-fixture coverage of the fourteen named reasons" and disclaims a general implementation-path proof. Since both the fourteen reasons and the fixture set are finite and enumerated, this is checkable as bounded: run the fixtures, confirm each yields its reason, confirm no fixture path returns permitted without a matching record. **Determinable without further judgment.**

**[2]** — Splits into two. Chain-termination: checkable. Authority_scope: the bound states ABS-0004 supplies no scope grammar and no matching semantics, so "outside its declared scope" cannot be evaluated in general — only against hand-constructed fixture scopes, which means the fixture author's construction *is* the judgment. **Not determinable without further judgment**, and no wording in the plan can fix this — it requires a scope grammar and matching semantics from ABS-0004 (a section not present in this evidence set; I would need ABS-0004's authority_scope definition to say whether one exists elsewhere). Until that exists, this sub-clause should be removed or explicitly deferred rather than left standing as if bounded.

**[3]** — Identity-collision logic and check_depth: mechanically checkable now. The "real captured InvocationRecord" clause: not checkable as written, but the evidence itself states the fix — "The criterion is met by naming the specific InvocationRecord used." That wording has not yet been applied to the criterion. **Not yet determinable**, but the fix is trivial and already specified: name the record.

**[4]** — Bound disclaims a monotonicity proof over all inputs, but the criterion's actual claim is fixture-level (enumerated modifier set, finite). **Determinable without further judgment** as scoped.

**[5]** — Bound states ABS-0004 §4.6 gives scope fields but no matching semantics for "permitted ExecutionProfile constraints" and no definition of "materially different profile." **Not determinable without further judgment**, and not fixable by plan wording alone — it requires ABS-0004 to define ExecutionProfile matching semantics and "materially different." That definition is not in this evidence set; naming it is the missing piece I'd need.

**[6]** — "Any check that asks for independent authorization" is unbounded; the bound says the criterion is met only against "the enumerated checks this slice defines." **Not determinable as written.** Wording that would fix it: replace "any check that asks for independent authorization" with the literal list — e.g., "...is reported as not independent by each of [check A], [check B], [check C]" — and drop "any." Until the open-ended phrase is replaced with the named list, a person cannot check it without deciding for themselves what counts as such a check.

**[7]** — Byte-identical output over a fixture set is unambiguous; the bound only disclaims a broader "no field/path/default altered" claim the criterion doesn't actually assert. **Determinable without further judgment.**

**[8]** — Offline/no-network is a clean pass/fail. "Every public entrypoint" is not checkable as written, but the bound says it's "met against an enumerated list of entrypoints recorded with the tests." **Partially determinable**: offline condition, yes now; entrypoint coverage, only once the criterion text is changed from "every public entrypoint" to a reference to that specific recorded list (e.g., "the entrypoints enumerated in [named file]"). Until that substitution is made in the criterion itself, "every" remains open to dispute about whether the list is complete.

**[9]** — Restated with named procedures (audit script, commit-level checksum comparison), which is more concrete than the original. But the bound itself says: "Without the procedure, the commands, and the semantics of verified_current, neither clause could be evaluated." That means the restatement names *where* the check happens but the evidence set does not contain the actual procedure, commands, or the definition of `verified_current`. **Not determinable from what's here.** Missing artifact: the specification of `scripts/audit_self_model_index.py`'s behavior and the definition of `verified_current` — presumably in ABS-0004 or an operations doc not included in this evidence set. I'd need that document to say whether [9] is checkable even after restatement.

## Summary

Of the ten, as currently worded: **[0], [1], [4], [7]** are determinable without further judgment now. **[3], [6], [8]** have known, stated fixes not yet applied to the criterion text (name the record; name the checks; name the entrypoint list). **[2], [5]** cannot be fixed by rewording the plan at all — they depend on definitions (scope grammar, ExecutionProfile matching semantics) that this evidence set says ABS-0004 does not supply, and I did not have the current ABS-0004 text to check whether that gap has since been closed elsewhere. **[9]** depends on a procedure and a term (`verified_current`) not present in this evidence; I cannot rule on it without that document.

Stating a bound, by itself, only records that the criterion was found not mechanically checkable. In four cases here it also happened to narrow the claim enough that the narrowed version is checkable. In three more, the bound names its own fix but the fix hasn't been written into the criterion yet. In the remaining three, the bound documents a dependency this evidence set does not resolve, and no amount of plan-level wording closes that gap — either the missing ontology provisions need to be supplied, or those clauses should be removed rather than carried forward as "bounded."
```
