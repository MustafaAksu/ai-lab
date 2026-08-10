# COMP-0126: Provider Comparison — v9 admission Q1 does-inherited-constraint-resolve-or-relocate

## Metadata

- comparison_id: `COMP-0126`
- title: `v9 admission Q1 does-inherited-constraint-resolve-or-relocate`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-fd34e81ff3f35d2a.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0126", "target_id": "INV-fd34e81ff3f35d2a"}, {"authoritative": false, "evidence": "docs/invocations/INV-23f92c02b095b2d2.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0126", "target_id": "INV-23f92c02b095b2d2"}]`
- created_at: `2026-08-10T10:21:54.084975+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q1 does-inherited-constraint-resolve-or-relocate You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

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

=== QUESTION Q1 ===
v9 introduces [INHERITED_CONSTRAINT]: "constraint text carried forward unchanged from the admitted v4 baseline. Its current governance force derives from v4's admission, not from the proposed v9 document."

Sixteen constraints carry it. Each is byte-identical to its v4 text; that was verified mechanically before adoption.

Does this resolve the defect that withdrew v8, or relocate it? Consider specifically: whether a proposed document can carry text with present force without that force attaching to the document; what a reader takes from a document in which some constraints bind and some do not; and whether "derives from v4's admission" is checkable by a reader who does not have v4. If the tag asserts more than the arrangement supports, name the sentence.

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

=== EVIDENCE ABS-0004 v9 Section 3, Three Decisions ===
## 3. Three Decisions

`[DEF]` The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

`[DEF]` A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

`[DEF]` Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

`[OPEN]` Authorization-chain bootstrap: how an authorization chain terminates
in a standing policy, delegated authority, or AccountablePrincipal authority
scope rather than requiring an infinite sequence of prior authorizations.

`[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and
authorization records can state and attribute authority claims. Repository
records do not by themselves establish a principal's extra-systemic
entitlement to govern.

`[LIMITATION]` A recorded authorization-chain terminus identifies where the
represented chain stops. It does not by itself establish that the underlying
invocation is substantively authorized.

`[LIMITATION]` Record and relation requirements expose only what was declared,
recorded, linked, traversable, and correctly attributed. They do not establish
that every material invocation, authorization, input, dependency, or external
interaction is present in the record.

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

=== QUESTION Q1 ===
v9 introduces [INHERITED_CONSTRAINT]: "constraint text carried forward unchanged from the admitted v4 baseline. Its current governance force derives from v4's admission, not from the proposed v9 document."

Sixteen constraints carry it. Each is byte-identical to its v4 text; that was verified mechanically before adoption.

Does this resolve the defect that withdrew v8, or relocate it? Consider specifically: whether a proposed document can carry text with present force without that force attaching to the document; what a reader takes from a document in which some constraints bind and some do not; and whether "derives from v4's admission" is checkable by a reader who does not have v4. If the tag asserts more than the arrangement supports, name the sentence.

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

=== EVIDENCE ABS-0004 v9 Section 3, Three Decisions ===
## 3. Three Decisions

`[DEF]` The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

`[DEF]` A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

`[DEF]` Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

`[OPEN]` Authorization-chain bootstrap: how an authorization chain terminates
in a standing policy, delegated authority, or AccountablePrincipal authority
scope rather than requiring an infinite sequence of prior authorizations.

`[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and
authorization records can state and attribute authority claims. Repository
records do not by themselves establish a principal's extra-systemic
entitlement to govern.

`[LIMITATION]` A recorded authorization-chain terminus identifies where the
represented chain stops. It does not by itself establish that the underlying
invocation is substantively authorized.

`[LIMITATION]` Record and relation requirements expose only what was declared,
recorded, linked, traversable, and correctly attributed. They do not establish
that every material invocation, authorization, input, dependency, or external
interaction is present in the record.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
It relocates rather than fully resolves the v8 defect.

`[INHERITED_CONSTRAINT]` removes the direct contradiction in which a proposed document labels constraints as “adopted now.” It instead says that their force is external to v9. That arrangement can be coherent: v9 may reproduce already-binding v4 text without itself admitting or re-admitting that text.

But the arrangement works only if v9 is clearly a non-authoritative carrier of an identifiable, accessible v4 authority. On this evidence, the tag asks the reader to treat sixteen passages as presently binding while providing neither v4 nor a reader-verifiable way to establish that the passages are the v4 passages with the v4 meaning and admission status.

The sentence that asserts more than the supplied arrangement supports is:

> “Its current governance force derives from v4's admission, not from the proposed v9 document.”

The evidence reports that v4 was “**admitted** 2026-07-20” and that the sixteen constraints were mechanically verified as byte-identical before adoption, but a reader without v4 cannot check either the asserted identity or the operative scope of v4’s admission. The stated v4 admission was also “recorded in conversation only,” while that conversation is not included here.

Consequently, a reader of v9 is told to make a live distinction:

- `[INHERITED_CONSTRAINT]` text is said to bind now through v4;
- `[PROPOSED_CONSTRAINT]` text does not bind unless v9 is separately admitted;
- other tags have still other stated roles.

That distinction is legible as a claim, but not independently usable from v9 alone. A reader cannot determine whether an inherited constraint was actually admitted, whether its surrounding v4 definitions or qualifications alter its meaning, or whether v4’s admission applied to the relevant text as reproduced.

The evidence is insufficient to determine whether the sixteen tags are properly attached in fact. Missing materials:

1. The admitted v4 text, including the sixteen corresponding constraints and their surrounding definitions, to check byte identity and contextual identity.
2. The record of v4’s admission, to determine what precisely was admitted and whether any conditions or exclusions applied.
3. A stable reader-facing locator or integrity mechanism connecting each v9 `[INHERITED_CONSTRAINT]` to its v4 source—for example, section-level references and a v4 artifact identifier usable by a reader.
4. The sixteen v9 constraints themselves, to assess whether their placement or new surrounding v9 text changes how a reader would understand their force.

Thus, the tag can distinguish provenance of force from the status of the proposed reconstruction, but on the supplied record it leaves the binding/nonbinding distinction dependent on an unavailable external source.
```

## Claude Response

- model: `claude-sonnet-5`

```
**Short answer: relocates, does not resolve.**

**What v8's defect actually was.** Per the disclosures, v8 was withdrawn because 24 constraints were tagged with a category the document itself defined as "constraint adopted now" while the document carrying that category was itself marked proposed — i.e., a proposed instrument asserting present adoptive force for its own content. The defect is the mismatch between the document's status (`proposed`) and a tag's claim (`adopted now`) applied to sentences inside that same document.

**What the new tag changes, and what it doesn't.** `[INHERITED_CONSTRAINT]` no longer says "adopted now." It says: "constraint text carried forward unchanged from the admitted v4 baseline. Its current governance force derives from v4's admission, not from the proposed v9 document." This substitutes a *sourcing* claim for an *adoption* claim. That is a real distinction in principle — a document can reproduce text whose force lies elsewhere (v4) without itself being the operative instrument for that force. Nothing in the evidence forbids that arrangement, and the admission table does show v4 as `admitted 2026-07-20`, so the sourcing claim has a real referent rather than being invented.

But three things the question asks me to check don't hold up:

1. **Can a proposed document carry text with present force without that force attaching to the document?** Only if the document is explicit that *it* is not the operative locus — e.g., "for the following sentences, consult and comply with v4 at commit 56f18a2ab7…; this document reproduces them for reference only." The tag doesn't do that. It says force "derives from v4's admission," but the sentence carrying that force is presented *as v9 Section 3 text*, under v9's own sentence-discipline scheme, alongside `[PROPOSED_CONSTRAINT]`, `[DEF]`, `[OPEN]`, and `[LIMITATION]` sentences that plainly do belong to v9 and do not bind until v9's own admission. Nothing in the evidence states a rule that verbatim reproduction of admitted text in a different, non-admitted document carries the original admission's force forward into that new document. That rule is assumed, not established. Absent it, the 16 sentences read as *v9 asserting current force*, which is the same shape of claim v8 made — the label of the source of force has moved, but the document's practical posture (proposed instrument containing sentences that presently bind) has not.

2. **What does a reader take from a document where some constraints bind and some don't?** The evidence doesn't include any in-situ example of `[INHERITED_CONSTRAINT]` sitting next to `[PROPOSED_CONSTRAINT]` sentences in Section 3 — the Section 3 excerpt provided contains only `[DEF]`, `[OPEN]`, and `[LIMITATION]` tags, no constraint tags at all. I cannot assess from what's given whether the split is legible in context or whether a reader would in practice apply uniform weight to the whole section. **Missing evidence:** an actual passage of Section 3 (or wherever the 16 constraints sit) showing `[INHERITED_CONSTRAINT]` and `[PROPOSED_CONSTRAINT]` sentences adjacent, which is what would let me judge whether the tag is legible rather than merely defined. Without it, the risk the question flags — a document that functions as one instrument to a reader but binds unevenly by hidden provenance — is unaddressed, not disproved.

3. **Is "derives from v4's admission" checkable by a reader without v4?** No, and the evidence itself concedes this by describing v4's admission as "recorded in conversation only" — there is no persisted admission record independent of the metadata's own say-so. A reader without v4 has three unverifiable premises stacked: (a) that the 16 sentences are byte-identical to v4's text (asserted "verified mechanically" in the question's framing, but no hash, diff, or verification artifact is in the evidence — **missing**: the verification record itself); (b) that v4's admission has not since been superseded, narrowed, or withdrawn by anything outside this document's own account of itself (the admission table is v9's own metadata, so this is the document vouching for its own premise); (c) that admission of v4-the-document transmits force to this-text-wherever-reproduced rather than only to v4-the-document. None of (a)–(c) is checkable from v9 alone, and v4 itself is not in evidence. **Missing:** the admitted v4 text, and any `[DEF]`/`[PRINCIPLE]` establishing a cross-document force-transfer rule.

**The sentence that asserts more than the arrangement supports:**

> "Its current governance force derives from v4's admission, not from the proposed v9 document."

This asserts a *result* (force presently attaches, sourced elsewhere) resting on premises — continued, unmodified v4 admission; a transfer rule; verified textual identity — none of which is established in what's in evidence, and the last of which (v4's own admission) is explicitly only "recorded in conversation," i.e., not independently checkable even in principle from documentary evidence.

**Conclusion.** v9 replaces v8's overt error (claiming adoption for proposed content) with a covert version of the same problem: a proposed, non-admitted document still containing sentences meant to function as currently binding, now justified by an unverifiable and undemonstrated provenance claim rather than by a false present-tense adoption claim. The defect has moved from "wrongly labeled as adopted" to "labeled as inherited in a way the reader cannot check and the document does not itself establish a rule for." That is relocation, not resolution.
```
