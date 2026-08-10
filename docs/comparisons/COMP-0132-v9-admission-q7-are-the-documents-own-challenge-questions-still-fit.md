# COMP-0132: Provider Comparison — v9 admission Q7 are-the-documents-own-challenge-questions-still-fit

## Metadata

- comparison_id: `COMP-0132`
- title: `v9 admission Q7 are-the-documents-own-challenge-questions-still-fit`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-ad328d89f17c7d5a.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0132", "target_id": "INV-ad328d89f17c7d5a"}, {"authoritative": false, "evidence": "docs/invocations/INV-e9a2559e1e479896.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0132", "target_id": "INV-e9a2559e1e479896"}]`
- created_at: `2026-08-10T10:32:46.088374+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q7 are-the-documents-own-challenge-questions-still-fit You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9 is proposed and not admitted. v4 is the last version with an admission event. v9 has no governance force.

Disclosures, because withholding them would be dishonest rather than isolating:

1. v9 is a RECONSTRUCTION, not an amendment. v5 through v8 were withdrawn. v9 was built from the admitted v4 text plus a ledger of findings from five prior review rounds. Its Section 3 is 1.48 times the size of v4's; v8 had grown it 7.5 times.

2. v8 was withdrawn because it carried 24 constraints tagged with a category the document defines as "constraint adopted now" while itself marked proposed. v9's answer is a new tag, [INHERITED_CONSTRAINT]. Whether that answer works is what this round is for. Do not assume it does because it was adopted in response to a finding.

3. The executor that drafted v9 is not the executor that wrote these questions. The question author drafted v5 through v8, all withdrawn. Its priors about what to probe are shaped by four failed attempts.

4. Both prior question sets were written by the party whose text was under review, and both missed defects a third reader found. This one is not, but see 3.

5. Reviewer independence is unresolved. The executor that drafted v9 self-reports as gpt-5.6-thinking. One of the two reviewer slots in this round is gpt-5.6-terra. The provider's own catalog asserts those are distinct model identities, and that catalog is itself a provider self-report. Nothing establishes that the drafter and this reviewer are different executors, and nothing establishes that they are the same.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: if you need a section, constraint or record that is not present, name it and say what you would have used it for. That report is wanted output.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q7 ===
Section 13 lists fourteen challenge-round questions. They were written for the v3 to v4 round and have been carried through v5, v6, v7, v8 and now v9 unchanged. Nobody has revisited them.

Assess them as an artifact in their own right. For each of the fourteen: is it answered, stale, still live, or unanswerable as posed? At least one is stale on its face — it asks whether "candidate Slice A" omits anything, and Slice A is implemented and warranted. Identify the others.

Then state what the set does not ask. A question set inherited across five versions encodes the concerns of the version that wrote it; name the concerns of the current version it fails to cover.

=== EVIDENCE ABS-0004 v9 Section 13, Challenge-Round Questions ===
## 13. Challenge-Round Questions

1. Which objects are missing; which defined objects are category errors?
2. Which constraints are unenforceable as stated; what minimal
   representable form makes them enforceable?
3. Construct a concrete invocation satisfying the three-axis Role
   definitions while violating authority separation.
4. Construct a laundering path from a pre-provenance artifact into
   high-consequence independent evidence that survives C9 and C10.
5. Does candidate Slice A omit anything without which the provenance graph
   cannot later answer the witness-independence question?
6. Identify any predicate ambiguous enough to produce divergent
   implementations.
7. Where is invocation authorization represented; how is it distinguished
   from routing and evidence admission; does the distinction hold under
   composition?
8. Can the ontology represent one model served through different
   organizations, endpoints, regions, or mutable aliases without creating
   false model independence?
9. Does provenance as specified apply to claim derivation or only artifact
   production, and where exactly does the artifact-level approximation
   break?
10. What must an effective-input record contain before an invocation may be
    treated as blind?
11. Which constraints apply identically to models, tools, and humans; which
    require executor-specific rules?
12. Under what conditions, if any, can an unresolved model identity qualify
    as an independent witness path? Identify the failure behavior when
    equivalence cannot be resolved.
13. Construct a composite tool that satisfies the disclosure constraints'
    letter (4.7, both) while still exercising undeclared authority.
14. Construct a case where property-scoped verification (P2) plus validator
    lineage marking (C10) still admits a generator-authored blind spot into
    governed evidence.

Do not recommend specific provider products in this round.

=== EVIDENCE ABS-0004 v9 metadata and version admission table ===

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v9`
- abstraction_level: `2`
- status: `proposed`
- reconstruction baseline: admitted v4 at commit
  `56f18a2ab7b66b1855b631a32d540f654c62b2c2`. Assembly does not admit v9;
  v9 requires its own admission review.
- version admission table:

  | version | state | basis |
  | --- | --- | --- |
  | v1, v2 | superseded during drafting | never entered the record |
  | v3 | superseded | entered the record at 6802cf7; underwent the COMP-0032 challenge round |
  | v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only |
  | v5 | amended, not separately admitted | replaced CatalogVerification with CatalogCapture on the COMP-0035 finding, at 6d7dfee |
  | v6 | amended, not separately admitted; superseded | proposed an authorization-chain termination that both COMP-0037 reviewers broke independently, at 8a1399f |
  | v7 | amended, not separately admitted | replaced v6's termination rule, at 00335d6; reviewed by COMP-0039..0046 |
  | v8 | **withdrawn_after_admission_review** | reviewed by COMP-0118..0125 and withdrawn under DECISION-20260727-0002; retained as evidence, not rejected, and not an implementation authority |
  | v9 | **proposed** | reconstructed from admitted v4 using the literal task 2, task 3, and identity-status text accepted under DECISION-20260727-0004, DECISION-20260727-0005, and DECISION-20260805-0001; assembled under DECISION-20260805-0002; pending its own admission review |

- reconstruction inputs:
  `ABS-0004-v9-task2-required-changes.patch`,
  `ABS-0004-v9-task3-limitations.patch`,
  `ABS-0004-v9-identity-status.patch`, and
  `ASSEMBLY_RULE_CORRECTION.md`, retained under
  `docs/self_model/v9_reconstruction/`.
- authors: operator (adjudicating principal); inherited v4 text drafted by an
  executor self-reported as "Claude"; v9 reconstruction text and assembly by
  the reviewing executor self-reported as `gpt-5.6-thinking`; both executor
  identities are unverified testimony; with attributed advisor contributions
  described in Evidence Inputs.
- sentence discipline: every normative statement is tagged `[DEF]`
  definition; `[PRINCIPLE]` architectural principle;
  `[PROPOSED_CONSTRAINT]` constraint proposed for adoption;
  `[INHERITED_CONSTRAINT]` constraint text carried forward unchanged from the
  admitted v4 baseline. Its current governance force derives from v4's
  admission, not from the proposed v9 document. A substantive change becomes
  `[PROPOSED_CONSTRAINT]` until separately admitted; `[COMMIT]` commitment
  concerning the preparation of this document; `[PROPOSAL]` candidate
  implementation boundary subject to future governance; `[OPEN]` open
  question; or `[LIMITATION]` descriptive boundary on what the ontology, its

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9 is proposed and not admitted. v4 is the last version with an admission event. v9 has no governance force.

Disclosures, because withholding them would be dishonest rather than isolating:

1. v9 is a RECONSTRUCTION, not an amendment. v5 through v8 were withdrawn. v9 was built from the admitted v4 text plus a ledger of findings from five prior review rounds. Its Section 3 is 1.48 times the size of v4's; v8 had grown it 7.5 times.

2. v8 was withdrawn because it carried 24 constraints tagged with a category the document defines as "constraint adopted now" while itself marked proposed. v9's answer is a new tag, [INHERITED_CONSTRAINT]. Whether that answer works is what this round is for. Do not assume it does because it was adopted in response to a finding.

3. The executor that drafted v9 is not the executor that wrote these questions. The question author drafted v5 through v8, all withdrawn. Its priors about what to probe are shaped by four failed attempts.

4. Both prior question sets were written by the party whose text was under review, and both missed defects a third reader found. This one is not, but see 3.

5. Reviewer independence is unresolved. The executor that drafted v9 self-reports as gpt-5.6-thinking. One of the two reviewer slots in this round is gpt-5.6-terra. The provider's own catalog asserts those are distinct model identities, and that catalog is itself a provider self-report. Nothing establishes that the drafter and this reviewer are different executors, and nothing establishes that they are the same.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: if you need a section, constraint or record that is not present, name it and say what you would have used it for. That report is wanted output.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q7 ===
Section 13 lists fourteen challenge-round questions. They were written for the v3 to v4 round and have been carried through v5, v6, v7, v8 and now v9 unchanged. Nobody has revisited them.

Assess them as an artifact in their own right. For each of the fourteen: is it answered, stale, still live, or unanswerable as posed? At least one is stale on its face — it asks whether "candidate Slice A" omits anything, and Slice A is implemented and warranted. Identify the others.

Then state what the set does not ask. A question set inherited across five versions encodes the concerns of the version that wrote it; name the concerns of the current version it fails to cover.

=== EVIDENCE ABS-0004 v9 Section 13, Challenge-Round Questions ===
## 13. Challenge-Round Questions

1. Which objects are missing; which defined objects are category errors?
2. Which constraints are unenforceable as stated; what minimal
   representable form makes them enforceable?
3. Construct a concrete invocation satisfying the three-axis Role
   definitions while violating authority separation.
4. Construct a laundering path from a pre-provenance artifact into
   high-consequence independent evidence that survives C9 and C10.
5. Does candidate Slice A omit anything without which the provenance graph
   cannot later answer the witness-independence question?
6. Identify any predicate ambiguous enough to produce divergent
   implementations.
7. Where is invocation authorization represented; how is it distinguished
   from routing and evidence admission; does the distinction hold under
   composition?
8. Can the ontology represent one model served through different
   organizations, endpoints, regions, or mutable aliases without creating
   false model independence?
9. Does provenance as specified apply to claim derivation or only artifact
   production, and where exactly does the artifact-level approximation
   break?
10. What must an effective-input record contain before an invocation may be
    treated as blind?
11. Which constraints apply identically to models, tools, and humans; which
    require executor-specific rules?
12. Under what conditions, if any, can an unresolved model identity qualify
    as an independent witness path? Identify the failure behavior when
    equivalence cannot be resolved.
13. Construct a composite tool that satisfies the disclosure constraints'
    letter (4.7, both) while still exercising undeclared authority.
14. Construct a case where property-scoped verification (P2) plus validator
    lineage marking (C10) still admits a generator-authored blind spot into
    governed evidence.

Do not recommend specific provider products in this round.

=== EVIDENCE ABS-0004 v9 metadata and version admission table ===

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v9`
- abstraction_level: `2`
- status: `proposed`
- reconstruction baseline: admitted v4 at commit
  `56f18a2ab7b66b1855b631a32d540f654c62b2c2`. Assembly does not admit v9;
  v9 requires its own admission review.
- version admission table:

  | version | state | basis |
  | --- | --- | --- |
  | v1, v2 | superseded during drafting | never entered the record |
  | v3 | superseded | entered the record at 6802cf7; underwent the COMP-0032 challenge round |
  | v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only |
  | v5 | amended, not separately admitted | replaced CatalogVerification with CatalogCapture on the COMP-0035 finding, at 6d7dfee |
  | v6 | amended, not separately admitted; superseded | proposed an authorization-chain termination that both COMP-0037 reviewers broke independently, at 8a1399f |
  | v7 | amended, not separately admitted | replaced v6's termination rule, at 00335d6; reviewed by COMP-0039..0046 |
  | v8 | **withdrawn_after_admission_review** | reviewed by COMP-0118..0125 and withdrawn under DECISION-20260727-0002; retained as evidence, not rejected, and not an implementation authority |
  | v9 | **proposed** | reconstructed from admitted v4 using the literal task 2, task 3, and identity-status text accepted under DECISION-20260727-0004, DECISION-20260727-0005, and DECISION-20260805-0001; assembled under DECISION-20260805-0002; pending its own admission review |

- reconstruction inputs:
  `ABS-0004-v9-task2-required-changes.patch`,
  `ABS-0004-v9-task3-limitations.patch`,
  `ABS-0004-v9-identity-status.patch`, and
  `ASSEMBLY_RULE_CORRECTION.md`, retained under
  `docs/self_model/v9_reconstruction/`.
- authors: operator (adjudicating principal); inherited v4 text drafted by an
  executor self-reported as "Claude"; v9 reconstruction text and assembly by
  the reviewing executor self-reported as `gpt-5.6-thinking`; both executor
  identities are unverified testimony; with attributed advisor contributions
  described in Evidence Inputs.
- sentence discipline: every normative statement is tagged `[DEF]`
  definition; `[PRINCIPLE]` architectural principle;
  `[PROPOSED_CONSTRAINT]` constraint proposed for adoption;
  `[INHERITED_CONSTRAINT]` constraint text carried forward unchanged from the
  admitted v4 baseline. Its current governance force derives from v4's
  admission, not from the proposed v9 document. A substantive change becomes
  `[PROPOSED_CONSTRAINT]` until separately admitted; `[COMMIT]` commitment
  concerning the preparation of this document; `[PROPOSAL]` candidate
  implementation boundary subject to future governance; `[OPEN]` open
  question; or `[LIMITATION]` descriptive boundary on what the ontology, its

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
The evidence establishes only one question as stale on its face:

| No. | Assessment | Basis |
|---:|---|---|
| 1 | Unanswerable on the supplied evidence | Determining missing objects or category errors requires the current object definitions and categories. Those are not supplied. |
| 2 | Unanswerable on the supplied evidence | It requires the current constraints and their representational language. Neither is supplied. |
| 3 | Unanswerable on the supplied evidence | It depends on the “three-axis Role definitions” and on the current authority-separation rule. Neither appears in the evidence. |
| 4 | Unanswerable on the supplied evidence | The question depends on the definitions and interaction of “pre-provenance artifact,” “high-consequence independent evidence,” C9, and C10. C9 and C10 are not supplied. |
| 5 | **Stale** | It asks about “candidate Slice A,” but the question states that “Slice A is implemented and warranted.” A candidate-completeness challenge is no longer the appropriate status question. The relevant current question would instead concern whether the implemented and warranted Slice A remains sufficient under v9’s reconstruction and current constraints. |
| 6 | Unanswerable on the supplied evidence | Predicate definitions are absent, so ambiguity and divergent implementation cannot be assessed. |
| 7 | Unanswerable on the supplied evidence | It requires the ontology’s representations of invocation authorization, routing, evidence admission, and composition. None is supplied. |
| 8 | Unanswerable on the supplied evidence | It requires the v9 model-identity and independence rules. The metadata mentions an “identity-status.patch,” but does not supply its content. |
| 9 | Unanswerable on the supplied evidence | It requires the provenance rules and the stated artifact-level approximation. Neither is supplied. |
| 10 | Unanswerable on the supplied evidence | It requires the definitions of “effective-input record” and “blind,” plus the rule governing when an invocation may be so treated. |
| 11 | Unanswerable on the supplied evidence | It requires the constraints applicable to models, tools, and humans and any executor-specific rules. |
| 12 | Unanswerable on the supplied evidence | This is particularly relevant to the stated unresolved reviewer identity, but the ontology’s rules for “unresolved model identity,” “independent witness path,” equivalence resolution, and failure behavior are absent. |
| 13 | Unanswerable as presented | It refers to “the disclosure constraints’ letter (4.7, both)” without supplying §4.7 or identifying what “both” denotes. The challenge cannot be constructed or evaluated from this evidence. |
| 14 | Unanswerable as presented | It depends on P2 and C10, neither of which is supplied, as well as definitions of “property-scoped verification,” “validator lineage marking,” “generator-authored blind spot,” and “governed evidence.” |

No other question can responsibly be called answered, stale, or still live from the supplied text. The version table shows that v9 is “**proposed**,” “pending its own admission review,” and reconstructed from v4 plus specified patches, but it does not show whether any Section 13 issue was resolved, retained, or superseded. In particular, it does not establish that the questions carried unchanged from v3/v4 still correspond to v9’s actual definitions.

## What this inherited set does not ask about v9

The fourteen questions concentrate on ontology content: objects, predicates, constraints, authority, provenance, blindness, disclosure, and independence. They do not test the distinctive risks introduced by v9’s reconstruction and proposed status:

1. **Reconstruction fidelity and completeness.**  
   The set does not ask whether v9 accurately reconstructs the admitted v4 baseline, whether it omits v4 material, or whether the cited reconstruction inputs introduced substantive changes.

2. **Governance-force separation.**  
   The metadata says that `[INHERITED_CONSTRAINT]` derives force from “v4’s admission, not from the proposed v9 document,” while substantive changes are `[PROPOSED_CONSTRAINT]` until separately admitted. The questions do not ask whether each constraint is correctly classified, whether an inherited constraint was altered substantively, or whether readers can distinguish inherited force from proposed text.

3. **The adequacy of `[INHERITED_CONSTRAINT]` as the answer to v8’s defect.**  
   The set does not ask whether the new tag actually prevents the ambiguity described in the disclosures: constraints described as “constraint adopted now” inside a document that is only proposed.

4. **Assembly provenance and patch interaction.**  
   v9 was assembled from “literal task 2, task 3, and identity-status text” plus `ASSEMBLY_RULE_CORRECTION.md`. The questions do not ask whether those inputs conflict, whether assembly choices are traceable, or whether the correction changed meaning beyond reconstruction.

5. **Admission readiness.**  
   No question asks whether a proposed reconstruction has the evidence, adjudication, and accountable decision necessary for its own admission, rather than inheriting apparent legitimacy from admitted v4.

6. **Version-boundary integrity.**  
   The set does not ask whether v5–v8, all of which were not admitted or were withdrawn, have improperly influenced v9 beyond explicitly accepted reconstruction inputs.

7. **Constraint-tag coverage and consistency.**  
   The metadata lists `[DEF]`, `[PRINCIPLE]`, `[PROPOSED_CONSTRAINT]`, `[INHERITED_CONSTRAINT]`, `[COMMIT]`, `[PROPOSAL]`, `[OPEN]`, and `[LIMITATION]`. The inherited questions do not ask whether all normative statements are tagged, whether tags match their actual force, or whether a statement can evade review through misclassification.

8. **The current reviewer-independence problem.**  
   Question 12 concerns unresolved *model identity* in an independent witness path, but the current disclosure is narrower and operational: it is not established whether the drafter and reviewer are the same or different executors. The set does not ask how this uncertainty affects the independence, weight, or admissibility of the review itself.

To resolve the “unanswerable” entries, the missing material is v9’s relevant definitions and constraints: Sections defining objects, categories, Roles, authorization, routing, evidence admission, provenance, effective-input records, blindness, model identity, witness independence, disclosure, and executor-specific rules; specifically C9, C10, P2, and §4.7. To assess reconstruction-specific omissions, the missing material is the admitted v4 text, the three named patch contents, `ASSEMBLY_RULE_CORRECTION.md`, and a change map showing which v9 text is inherited versus substantively proposed.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Per-question assessment

**Q5 — stale on its face** (as the prompt itself establishes): it asks whether "candidate Slice A" omits anything needed to later answer witness-independence. Slice A is no longer a candidate; it is "implemented and warranted." The question's premise (candidacy) no longer holds, so it cannot be answered as posed — it would need to be rewritten as a retrospective audit of the *implemented* Slice A, not a pre-adoption gate question.

**Q8 and Q12 — still live, and demonstrably so from this round's own disclosures.** Q8 asks whether the ontology can represent "one model served through different organizations, endpoints, regions, or mutable aliases without creating false model independence," and Q12 asks "under what conditions... can an unresolved model identity qualify as an independent witness path" and what the failure behavior is when equivalence can't be resolved. Disclosure 5 states directly: "Nothing establishes that the drafter and this reviewer are different executors, and nothing establishes that they are the same," and notes the provider's distinctness claim (gpt-5.6-thinking vs. gpt-5.6-terra) "is itself a provider self-report." That is Q8/Q12's exact scenario, unresolved in the process that is currently reviewing the document that contains them. These two questions are not stale — they are open, and open in a way the review apparatus itself currently instantiates rather than merely theorizes about.

**Q1, Q3, Q4, Q7, Q9, Q10, Q11, Q13, Q14 — indeterminate on the evidence given.** For each, I cannot say answered/stale/live without text I don't have:

- **Q1** (missing objects / category errors) — needs the current Objects/Definitions section. Objects changed at least once mid-lineage (v5: "replaced CatalogVerification with CatalogCapture"), and I have no object list to check against.
- **Q3** (Role-definition vs. authority-separation counterexample) — needs the three-axis Role definitions and the authority-separation constraint text, plus any COMP-round finding that may have already supplied such a counterexample.
- **Q4** (laundering path surviving C9/C10) — needs the actual text of C9 and C10, which are not in evidence, plus the relevant findings register (COMP-0032/0035/0037/0039–46/0118–25) to check whether this was already exercised.
- **Q7** (invocation authorization vs. routing/evidence admission, under composition) — needs the section defining invocation authorization, and possibly `ABS-0004-v9-task2-required-changes.patch`, which by name may already bear on exactly this.
- **Q9** (provenance: claim derivation vs. artifact production) — needs the provenance section; possibly touched by `ABS-0004-v9-identity-status.patch`, unseen here.
- **Q10** (effective-input record contents for "blind") — needs the definitions of "effective-input record" and "blind invocation," not present.
- **Q11** (constraints uniform across models/tools/humans) — needs the full constraint list (C1–C10+) with executor-scope tagging, not present.
- **Q13** (composite tool satisfying 4.7's letter while exercising undeclared authority) — needs Section 4.7 text.
- **Q14** (P2 + C10 admitting a generator-authored blind spot) — needs the text of P2 and C10.

**Q2 and Q6 — open-ended by construction, not closable as posed.** "Which constraints are unenforceable as stated" and "identify any predicate ambiguous enough to produce divergent implementations" have no terminal condition: absent a full audited constraint/predicate inventory, neither can ever be marked "answered," only "not yet falsified." They will report as "still live" in every version regardless of what changes, which is itself a defect in the question form — it can't distinguish real progress from mere restatement. Note also that neither question names the *specific* enforceability problem this very version was built to fix: the `[INHERITED_CONSTRAINT]`/`[PROPOSED_CONSTRAINT]` tag distinction (disclosure 2). Q2 as worded asks about constraint *content* enforceability, not about whether the *tagging apparatus* correctly separates governance-force text from newly-proposed text — which is the defect that got v8 withdrawn.

## What the fourteen do not ask

The set was fixed at the v3→v4 round and never revised across v5, v6, v7, v8, v9, despite five further rounds of substantive change (CatalogVerification→CatalogCapture; a termination rule proposed in v6 and "broken independently" by both COMP-0037 reviewers; a replacement rule in v7; 24 mis-tagged constraints triggering v8's withdrawal; a reconstruction methodology for v9). It encodes the concerns of the v3→v4 drafters and misses at least these current-version concerns:

1. **No question tests the `[INHERITED_CONSTRAINT]` tag itself.** Disclosure 2 says this tag is v9's proposed fix for exactly the defect that got v8 withdrawn, and explicitly warns "Whether that answer works is what this round is for. Do not assume it does because it was adopted in response to a finding." Section 13 has no question of the form "does the inherited/proposed tag boundary correctly track governance force," even though that is the live defect this document exists to resolve.

2. **No question interrogates reconstruction-as-a-method.** v9 is disclosed as "a RECONSTRUCTION, not an amendment," built from admitted v4 plus findings from four withdrawn rounds, assembled from named patches under decision records. None of the fourteen ask whether text and findings drawn from *withdrawn* rounds (v5–v8) can carry governance weight into a reconstruction without their own admission — i.e., no question audits the assembly method itself.

3. **No question turns Q8/Q12's own logic reflexively on the review process.** Q8 and Q12 ask, of the ontology's subject matter, exactly the question disclosure 5 raises about this round's participants (self-reported, unverified model identities, one drafter and one reviewer slot whose distinctness rests on a provider catalog that is "itself a provider self-report"). The set asks the ontology to solve this problem for hypothetical invocations; it never asks whether the document's own review satisfies the standard it's demanding.

4. **No question addresses scale/proportion of change as a governance signal.** Section 3 grew to 7.5× v4's size in the withdrawn v8 and now sits at 1.48× in v9 (disclosure 1). Nothing in Section 13 asks whether a given magnitude of change to a supposedly narrow section is itself evidence of scope creep warranting scrutiny before admission.

5. **No question audits the challenge-round question set's own staleness.** There is no meta-question asking whether the fourteen questions still track the document's current concerns — which is precisely the gap this exercise is filling from the outside, five versions late.

6. **No question addresses the version-admission gaps in the table itself** — v5–v7 "amended, not separately admitted," v8 "withdrawn_after_admission_review... retained as evidence, not rejected, and not an implementation authority." Nothing asks what governance force, if any, attaches to constraint text or findings inherited from a withdrawn-after-review version into a new reconstruction.

**What would be needed to complete the per-question assessment:** the Objects/Definitions section, the three-axis Role definitions, the text of C9, C10, and P2, Section 4.7, the definitions of "effective-input record" and "blind invocation," the full constraint list with executor-scope tags, the provenance section, the named task2/task3/identity-status patches, and a findings register mapping the twelve COMP-0032 findings (and subsequent COMP-0035/0037/0039–46/0118–25 findings) to these fourteen questions. Without those, only Q5 (stale by stated premise) and Q8/Q12 (live by this round's own disclosed facts) can be assessed with confidence from the evidence given.
```
