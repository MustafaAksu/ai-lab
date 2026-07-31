# COMP-0122: Provider Comparison — v8 admission Q5 per-version-admission-table

## Metadata

- comparison_id: `COMP-0122`
- title: `v8 admission Q5 per-version-admission-table`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-3fe5f1d9392e8362.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0122", "target_id": "INV-3fe5f1d9392e8362"}, {"authoritative": false, "evidence": "docs/invocations/INV-dd9d19f27568f719.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0122", "target_id": "INV-dd9d19f27568f719"}]`
- created_at: `2026-07-31T13:42:55.850099+00:00`
- command: `scripts/compare_providers.py --title v8 admission Q5 per-version-admission-table You are reviewing a proposed ontology amendment and the implementation plan that depends on it. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v8 is proposed and not admitted. PLAN-20260723-0002 is proposed and not admitted. Neither has governance force.

Three disclosures, because withholding them would be dishonest rather than isolating:

1. v8 is a response to a prior review round (COMP-0039..0046) of v7. It withdrew several claims that round found unsupported. Do not treat a sentence as sound because it is a correction; a correction can overreach or under-reach like any other text.

2. Of the 118 claims that round produced whose citations the amendment broke, 58 were adjudicated as still applying against v8. v8 made the ontology more honest about what it does not do; it did not make the mechanisms work. Do not credit v8 with having closed what it only disclosed.

3. The executor that drafted v8 also proposed the dispositions deciding which claims still applied, subject to operator approval. Treat both as one party's work.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: the evidence set below was scoped deliberately, and the scoping may be wrong. If you need a section, constraint, or record that is not present, name it explicitly and say what you would have used it for. That report is wanted output, not a failure.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q5 ===
v8 replaced a single status field with a per-version admission table. The field previously read status admitted with an admission date, directly beneath version v7, while the stated admission basis described the round that produced v4. A reader would have taken v7 as admitted; no record established that.

Does the table fix the defect or relocate it? Consider specifically: what a reader now takes from the word proposed against v8; whether "amended, not separately admitted" is a status or the absence of one; and whether a document that has been amended four times without an admission warrant is in a state the table can describe at all. If the table asserts more than the record supports, name the sentence.

=== EVIDENCE ABS-0004:v8 metadata and version admission table ===

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v8`
- abstraction_level: `2`
- status: `proposed` — this version only. A single status field cannot
  describe a document amended repeatedly, and until v8 this one did not try:
  the metadata carried `status: admitted` and `admitted_at: 2026-07-20`
  directly beneath `version: v7`, while its stated admission basis described
  the COMP-0032 round that produced v4. A reader would take v7 as admitted.
  No record establishes that. The table below replaces the single field.
- version admission table:

  | version | state | basis |
  | --- | --- | --- |
  | v1, v2 | superseded during drafting | never entered the record |
  | v3 | superseded | entered the record at 6802cf7; underwent the COMP-0032 challenge round |
  | v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only |
  | v5 | amended, not separately admitted | replaced CatalogVerification with CatalogCapture on the COMP-0035 finding, at 6d7dfee |
  | v6 | amended, not separately admitted; superseded | proposed an authorization-chain termination that both COMP-0037 reviewers broke independently, at 8a1399f |
  | v7 | amended, not separately admitted | replaced v6's termination rule, at 00335d6; reviewed by COMP-0039..0046 |
  | v8 | **proposed** | this revision, applying the COMP-0039..0046 findings and the drafting finding recorded below |

- admission record gap: no admission warrant exists for any ABS-0004
  amendment. The four warrants naming ABS-0004 — WARR-20260722-0001,
  WARR-20260722-0002, WARR-20260723-0001, WARR-20260723-0002 — are
  plan-implementation warrants for Slices A and B, not ontology amendments.
  v4's admission is recorded in conversation only, as its own basis states.
  Until a DecisionRecord kind exists to carry amendment admission (Slice C,
  Section 4.13), this table is an honest substitute for a record that cannot
  yet be represented; it is not a claim that the gap is closed.
- review basis for v8: COMP-0039..0046, eight questions asked in separate
  invocations with per-question declared evidence, two providers, sixteen
  complete responses. Findings consolidated in
  `docs/comparisons/comp0039/SLICE_C_FINDINGS.md`. Under constraint C3 that
  round is `independence_unresolved`, not two-witness corroboration.
- authors: operator (adjudicating principal); drafting executor self-reported

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

=== QUESTION Q5 ===
v8 replaced a single status field with a per-version admission table. The field previously read status admitted with an admission date, directly beneath version v7, while the stated admission basis described the round that produced v4. A reader would have taken v7 as admitted; no record established that.

Does the table fix the defect or relocate it? Consider specifically: what a reader now takes from the word proposed against v8; whether "amended, not separately admitted" is a status or the absence of one; and whether a document that has been amended four times without an admission warrant is in a state the table can describe at all. If the table asserts more than the record supports, name the sentence.

=== EVIDENCE ABS-0004:v8 metadata and version admission table ===

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v8`
- abstraction_level: `2`
- status: `proposed` — this version only. A single status field cannot
  describe a document amended repeatedly, and until v8 this one did not try:
  the metadata carried `status: admitted` and `admitted_at: 2026-07-20`
  directly beneath `version: v7`, while its stated admission basis described
  the COMP-0032 round that produced v4. A reader would take v7 as admitted.
  No record establishes that. The table below replaces the single field.
- version admission table:

  | version | state | basis |
  | --- | --- | --- |
  | v1, v2 | superseded during drafting | never entered the record |
  | v3 | superseded | entered the record at 6802cf7; underwent the COMP-0032 challenge round |
  | v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only |
  | v5 | amended, not separately admitted | replaced CatalogVerification with CatalogCapture on the COMP-0035 finding, at 6d7dfee |
  | v6 | amended, not separately admitted; superseded | proposed an authorization-chain termination that both COMP-0037 reviewers broke independently, at 8a1399f |
  | v7 | amended, not separately admitted | replaced v6's termination rule, at 00335d6; reviewed by COMP-0039..0046 |
  | v8 | **proposed** | this revision, applying the COMP-0039..0046 findings and the drafting finding recorded below |

- admission record gap: no admission warrant exists for any ABS-0004
  amendment. The four warrants naming ABS-0004 — WARR-20260722-0001,
  WARR-20260722-0002, WARR-20260723-0001, WARR-20260723-0002 — are
  plan-implementation warrants for Slices A and B, not ontology amendments.
  v4's admission is recorded in conversation only, as its own basis states.
  Until a DecisionRecord kind exists to carry amendment admission (Slice C,
  Section 4.13), this table is an honest substitute for a record that cannot
  yet be represented; it is not a claim that the gap is closed.
- review basis for v8: COMP-0039..0046, eight questions asked in separate
  invocations with per-question declared evidence, two providers, sixteen
  complete responses. Findings consolidated in
  `docs/comparisons/comp0039/SLICE_C_FINDINGS.md`. Under constraint C3 that
  round is `independence_unresolved`, not two-witness corroboration.
- authors: operator (adjudicating principal); drafting executor self-reported

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient to answer it, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
The table fixes the narrow v7-reading defect: `proposed` is expressly scoped to “this version only,” so a reader now takes v8 to be proposed, not admitted. It no longer places an unqualified `admitted` field immediately under v7.

It relocates the larger defect into the entries for v5–v7. “Amended, not separately admitted” is not an admission status. It combines a version-history fact (“amended”) with the absence of a particular admission event (“not separately admitted”). It does not establish whether the amended version is:

- admitted by inheritance from v4;
- unadmitted;
- proposed;
- pending admission; or
- of indeterminate admission status.

The supplied text rules out an amendment admission warrant, but it does not supply a rule under which admission of v4 either carries forward to, or is necessarily displaced by, an amendment. Indeed, v4 itself is said to be admitted without a warrant, through a conversation-only operator action. Thus absence of an amendment warrant cannot, on this evidence, determine the admission state of v5–v7.

For a document amended four times without an admission warrant, the table can describe the lineage—v4 was followed by amendments v5 through v8—but it cannot fully describe each amended version’s admission state using `amended, not separately admitted`. A more accurate state would need to say that admission of the amendment is unrecorded or undetermined, unless an applicable admission rule establishes a consequence of amendment.

The table sentence that asserts more than the supplied record supports is:

> “Until a DecisionRecord kind exists to carry amendment admission (Slice C, Section 4.13), this table is an honest substitute for a record that cannot yet be represented; it is not a claim that the gap is closed.”

The supplied evidence does not include Slice C, Section 4.13, the DecisionRecord constraints, or the governing rule that makes a DecisionRecord the necessary or exclusive representation for amendment admission. Those are needed to establish that the admission record “cannot yet be represented,” rather than merely has not been created.

The same evidentiary limitation applies to the table’s categorical `admitted` entry for v4 and its categorical “not separately admitted” entries for v5–v7: the evidence reports a conversation-only v4 admission and absence of warrants, but does not include that conversation, the warrants, or the admission rules needed to verify the resulting statuses.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Does the table fix the defect or relocate it?

Mostly relocates it, with one genuine improvement.

**What the old defect was**: `status: admitted` sat directly beneath `version: v7` while the basis actually described "the COMP-0032 round that produced v4." The table eliminates that specific conflation — v7's row now correctly reads "amended, not separately admitted," and v4 carries its own basis. That much is fixed.

**What "proposed" against v8 tells a reader**: Read alone, the v8 row says only `proposed`, with basis "this revision, applying the COMP-0039..0046 findings and the drafting finding recorded below." The word "applying" is doing work the record doesn't support: it reads as resolution — findings taken in and addressed — not as "responded to, with the majority still open." Nothing in this row tells the reader that a substantial fraction of the round's findings still apply to what's in front of them; "proposed" plus "applying... findings" together suggest a document that has caught up to its review, not one still carrying most of its defects forward under a corrected label. A reader relying on this row alone would take v8 to be further along than the record supports.

**"amended, not separately admitted" — status or its absence?**
This phrase, used for v5, v6, and v7, is the absence of a status written in status-shaped syntax. It reports a fact (no separate admission event occurred) but does not say what that absence means: whether the amendment is valid on the strength of v4's admission, provisional pending one, or simply unadmitted. The table format — one row, one phrase, parallel in structure to "admitted" and "proposed" — invites a reader to treat it as a settled category alongside the others, when it is actually a gap being named rather than a state being asserted. That it also covers v6, which "proposed an authorization-chain termination that both COMP-0037 reviewers broke independently," and yet receives the same "amended, not separately admitted" phrasing as v5 and v7, shows the label carries no information about whether the amendment it names was itself sound — only that no admission event was logged for it.

**Four amendments, no admission warrant — can the table describe this state at all?**
The evidence answers this directly: "no admission warrant exists for any ABS-0004 amendment," and even v4's admission is "recorded in conversation only," not by warrant. The table's own gap notice concedes the limit: "this table is an honest substitute for a record that cannot yet be represented; it is not a claim that the gap is closed." That is an admission that the vocabulary available — admitted / amended, not separately admitted / proposed — cannot fully describe a document whose only "admitted" ancestor was never warranted in the first place. If v4 was never admitted by the standard the ontology itself expects (a warrant, or eventually a DecisionRecord under Slice C §4.13), then "amended, not separately admitted" for v5–v7 is amendment layered on an unresolved question, and the table has no cell for that condition — it can only mark presence or absence of a *separate* admission, not the validity of the one it's separate from.

**The sentence that asserts more than the record supports:**

> "v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only"

The bolding, the specific date, and the commit hash give this row the visual and formal weight of a warrant-backed admission. The qualifier that actually governs its evidentiary status — "recorded in conversation only" — is appended at the end of the same cell, in the same register as the rest, rather than flagged as the operative limitation. This is the same failure mode as the original defect (a status field overstating what the record establishes), now sitting on v4 instead of v7.

**Missing evidence I'd need:**
- Slice C, Section 4.13 (the DecisionRecord kind for amendment admission) — to know whether "amended, not separately admitted" is a defined ontological category or an ad hoc label invented for this table.
- The four warrants (WARR-20260722-0001/0002, WARR-20260723-0001/0002) — to check whether any of them, despite being "plan-implementation" warrants, contain language that could be read as bearing on ABS-0004's admission status, since the evidence only asserts they don't without showing their text.
- COMP-0032's findings themselves — to assess whether "twelve adjudicated COMP-0032 findings applied" for v4 is accurately summarized or itself overstated.
- SLICE_C_FINDINGS.md — to check the 58-of-118 disposition directly rather than relying on the disclosure's summary, since the table's v8 basis line ("applying the COMP-0039..0046 findings") is the sentence most in tension with that count.
```
