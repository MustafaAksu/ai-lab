#!/usr/bin/env python3
"""Build the atomic admission round for ABS-0004 v9.

Question authorship: the packaging executor, under DECISION-20260805-0002. It
drafted none of v9. It did draft v5 through v8, which v9 replaces, so its sense
of what to probe is shaped by four failed attempts rather than by none. That is
a different bias, not an absence of one, and Q8 exists to expose it.

Question selection is driven by what the ledger recorded as NEVER PROBED, not by
what the drafting executor found interesting. Five of the nine unprobed surfaces
become questions here: identity equivalence under aliases, authorization graph
cycles and retroactivity, seed-authority bootstrap, ordinary-language reading of
the labels, and question-author capture itself. The two new sentence categories
have never been reviewed by anyone and take the first two slots.

Q7 asks reviewers to review the document's own challenge questions, which v9
inherited unchanged from v4 and which nobody has revisited. At least one is
already stale: it asks about "candidate Slice A", which is now CAP-0015 and
implemented.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

ABS = pathlib.Path("docs/abstractions/ABS-0004-invocation-authorization-ontology.md")
BASE = pathlib.Path("docs/comparisons/comp_v9")

PREAMBLE = """You are reviewing a proposed ontology amendment. This is ONE question \
of eight, each asked in a separate call with its own evidence set. Do not attempt to \
answer the others.

Status: ABS-0004 v9 is proposed and not admitted. v4 is the last version with an \
admission event. v9 has no governance force.

Disclosures, because withholding them would be dishonest rather than isolating:

1. v9 is a RECONSTRUCTION, not an amendment. v5 through v8 were withdrawn. v9 was \
built from the admitted v4 text plus a ledger of findings from five prior review \
rounds. Its Section 3 is 1.48 times the size of v4's; v8 had grown it 7.5 times.

2. v8 was withdrawn because it carried 24 constraints tagged with a category the \
document defines as "constraint adopted now" while itself marked proposed. v9's \
answer is a new tag, [INHERITED_CONSTRAINT]. Whether that answer works is what this \
round is for. Do not assume it does because it was adopted in response to a finding.

3. The executor that drafted v9 is not the executor that wrote these questions. The \
question author drafted v5 through v8, all withdrawn. Its priors about what to probe \
are shaped by four failed attempts.

4. Both prior question sets were written by the party whose text was under review, \
and both missed defects a third reader found. This one is not, but see 3.

5. Reviewer independence is unresolved. The executor that drafted v9 self-reports as \
gpt-5.6-thinking. One of the two reviewer slots in this round is gpt-5.6-terra. The \
provider's own catalog asserts those are distinct model identities, and that catalog \
is itself a provider self-report. Nothing establishes that the drafter and this \
reviewer are different executors, and nothing establishes that they are the same.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: if you need a section, constraint or record that is not present, name it \
and say what you would have used it for. That report is wanted output.

Do not certify or praise. No provider product recommendations."""

QUESTIONS = {
    "Q1": {
        "slug": "does-inherited-constraint-resolve-or-relocate",
        "sections": ["METADATA", "S3"],
        "text": """v9 introduces [INHERITED_CONSTRAINT]: "constraint text carried \
forward unchanged from the admitted v4 baseline. Its current governance force derives \
from v4's admission, not from the proposed v9 document."

Sixteen constraints carry it. Each is byte-identical to its v4 text; that was \
verified mechanically before adoption.

Does this resolve the defect that withdrew v8, or relocate it? Consider \
specifically: whether a proposed document can carry text with present force without \
that force attaching to the document; what a reader takes from a document in which \
some constraints bind and some do not; and whether "derives from v4's admission" is \
checkable by a reader who does not have v4. If the tag asserts more than the \
arrangement supports, name the sentence.""",
    },
    "Q2": {
        "slug": "do-limitations-do-work-or-wrap-failures",
        "sections": ["S3", "S4_3_4_4"],
        "text": """v9 adds nine [LIMITATION] statements, a category defined as "a \
descriptive boundary on what the ontology, its records, or current enforcement \
establish. A limitation imposes no constraint and claims no adoption."

A prior synthesis characterised v8's failure mode as: a failed control retained in \
control-shaped language, wrapped in an accurate disclaimer, and delegated to a future \
mechanism or a careful reader.

Are these limitations that same pattern under a different tag? Go statement by \
statement for those below. For each, say what a reader could do differently because \
it is present, and what would be lost if it were deleted. Where a limitation only \
restates what the surrounding text already implies, say so. If some earn their place \
and others do not, distinguish them.""",
    },
    "Q3": {
        "slug": "authorization-graph-cycles-expiry-retroactivity",
        "sections": ["S3", "S4_13", "S4_16"],
        "text": """Five review rounds have not probed the temporal and structural \
behaviour of the authorization graph. Construct concrete failures for each of the \
following, or state that the ontology as written prevents it and identify the \
sentence that does:

(a) a cycle in the authorization chain, where A's authority derives from B's and B's \
from A's;
(b) two authorization records that both cover an invocation and contradict each \
other;
(c) an authorization relied upon after the standing authority behind it was \
superseded or withdrawn;
(d) an authorization issued after the invocation it covers, and a record that cannot \
distinguish this from one issued before.

For each, say whether the defect is in the ontology's definitions, in the absence of \
a rule, or outside the ontology's scope.""",
    },
    "Q4": {
        "slug": "identity-equivalence-aliases-and-unresolved",
        "sections": ["S4_3_4_4", "C3", "S12"],
        "text": """v9 states that identity_verification_status is the immutable \
capture-time status of an executor reference, that the value verified means an \
admitted capture path established a unique identity under a property-scoped \
verification rule, and that no admitted capture path can presently substantiate it. \
Every captured record carries unresolved.

Constraint C3 forbids an invocation from adjudicating a claim whose evidence ancestry \
contains an invocation by an equivalent executor identity.

This is live rather than hypothetical: the executor that drafted v9 self-reports as \
gpt-5.6-thinking, and one reviewer in this round is gpt-5.6-terra. The provider's \
catalog asserts they are distinct identities. That catalog is a provider self-report.

Can two executor references be shown NOT equivalent under this ontology? If \
equivalence can never be established and non-equivalence can never be established \
either, state what C3 does in practice, and whether independence_unresolved carries \
any information that distinguishes one pairing from another. If the honest \
consequence is that C3 cannot be satisfied, say so and say what follows.""",
    },
    "Q5": {
        "slug": "seed-authority-who-drafts-approves-and-relies",
        "sections": ["S3", "S4_13", "METADATA"],
        "text": """v9's Section 3 leaves the authorization-chain bootstrap open, as \
v4 did, and adds limitations stating that repository records do not establish a \
principal's extra-systemic entitlement to govern.

Examine the seed. In this system one party drafts the root records, approves them, \
activates them, and then relies on them as the terminus of every authorization chain. \
The document's own version admission table records that v4 was admitted "by the \
operator as accountable principal in session, recorded in conversation only", and \
that no admission warrant exists for any amendment.

Does the ontology as written distinguish that arrangement from one in which the seed \
is fabricated? If not, say what a record would have to contain to make the \
distinction, and whether such a record could exist inside the repository at all. Do \
not treat the operator's actual trustworthiness as evidence; the question is what the \
ontology represents.""",
    },
    "Q6": {
        "slug": "what-the-labels-mean-to-a-reader",
        "sections": ["S3", "S4_13", "S8"],
        "text": """Read as an ordinary reader who sees a record and not the ontology.

The system emits and uses the terms governed, permitted, valid authorization, \
self-standing, and verified. A prior round established that an invocation with \
undisclosed subordinate execution can be classified governed.

For each term as it appears below, state what an ordinary reader would take it to \
mean, what it actually means under this ontology, and the gap. Then answer the \
question no round has adjudicated: is a system that only classifies, and never \
refuses, performing authorization at all? If it is better described as \
authorization assessment or record-coverage classification, say which and say what \
would have to change in the text.""",
    },
    "Q7": {
        "slug": "are-the-documents-own-challenge-questions-still-fit",
        "sections": ["S13", "METADATA"],
        "text": """Section 13 lists fourteen challenge-round questions. They were \
written for the v3 to v4 round and have been carried through v5, v6, v7, v8 and now \
v9 unchanged. Nobody has revisited them.

Assess them as an artifact in their own right. For each of the fourteen: is it \
answered, stale, still live, or unanswerable as posed? At least one is stale on its \
face — it asks whether "candidate Slice A" omits anything, and Slice A is implemented \
and warranted. Identify the others.

Then state what the set does not ask. A question set inherited across five versions \
encodes the concerns of the version that wrote it; name the concerns of the current \
version it fails to cover.""",
    },
    "Q8a": {
        "slug": "what-this-question-set-missed-definitions",
        "sections": ["PART_A"],
        "text": """The eight questions in this round were written by the executor \
that drafted v5, v6, v7 and v8, every one of which was withdrawn or superseded. It \
drafted none of v9.

Someone who has failed four times at a document tends to probe the places they \
failed.

YOU ARE SEEING PART OF THE DOCUMENT. Below are the metadata, evidence inputs, and \
Sections 1 through 4: anchoring principles, scope, the three decisions, and the \
object definitions. Sections 5 through 13 are being reviewed by the same question in \
a separate call. The whole document did not fit in one call: at 17,533 input tokens \
it exhausted the entire output budget on reasoning and returned no text, which is the \
same failure that produced the empty response in COMP-0038. Say so if the split \
prevents you from answering.

Read what you can see as though no review round had happened. Find what is weakest in \
it. Then report anything significant that this question set does not ask about, and \
anything that is unsound rather than merely incomplete.""",
    },
    "Q8b": {
        "slug": "what-this-question-set-missed-constraints",
        "sections": ["PART_B"],
        "text": """The eight questions in this round were written by the executor \
that drafted v5, v6, v7 and v8, every one of which was withdrawn or superseded. It \
drafted none of v9.

YOU ARE SEEING PART OF THE DOCUMENT. Below are Sections 5 through 13: canonical \
relations, epistemic constraints, legacy and phase-in, consequence classes, the \
enforcement matrix, the implementation sequence, deferred definitions, open \
questions, and the challenge-round questions. The metadata and Sections 1 through 4 \
are being reviewed by the same question in a separate call. The whole document did \
not fit in one call. Say so if the split prevents you from answering.

Read what you can see as though no review round had happened. Find what is weakest in \
it. Then report anything significant that this question set does not ask about, and \
anything that is unsound rather than merely incomplete.

Pay particular attention to the enforcement matrix: it records for each constraint \
whether it is evidenced, and it is the one place the document states its own \
enforcement status in a form a reader can check against the rest."""
    },
}


def section(text: str, start: str, end: str | None) -> str:
    """Slice from start to end. end=None means to the end of the document,
    which Section 13 needs: it is the last section and nothing follows it."""
    i = text.index(start)
    if end is None:
        return text[i:].rstrip()
    j = text.index(end, i + len(start))
    return text[i:j].rstrip()


def main() -> int:
    v9 = ABS.read_text()
    lines = v9.splitlines()
    meta = "\n".join(lines[3:46])

    units = {
        "METADATA": ("ABS-0004 v9 metadata and version admission table", meta),
        "S3": ("ABS-0004 v9 Section 3, Three Decisions",
               section(v9, "## 3. Three Decisions", "## 4. Object Definitions")),
        "S4_3_4_4": ("ABS-0004 v9 sections 4.3 and 4.4",
                     section(v9, "### 4.3 ", "### 4.5 ")),
        "S4_13": ("ABS-0004 v9 section 4.13, DecisionRecord and AccountablePrincipal",
                  section(v9, "### 4.13 ", "### 4.14 ")),
        "S4_16": ("ABS-0004 v9 section 4.16, RoutingPolicy and AuthorizationPolicy",
                  section(v9, "### 4.16 ", "### 4.17 ")),
        "S8": ("ABS-0004 v9 Section 8, Consequence Classes",
               section(v9, "## 8. Consequence Classes", "## 9. ")),
        "S12": ("ABS-0004 v9 constraint C3 and neighbours",
                section(v9, "`[INHERITED_CONSTRAINT]` C3 ", "`[PROPOSED_CONSTRAINT]` C5 ")),
        "C3": ("ABS-0004 v9 constraint C3, no self-adjudication",
               section(v9, "`[INHERITED_CONSTRAINT]` C3 ", "`[PROPOSED_CONSTRAINT]` C4 ")),
        "S13": ("ABS-0004 v9 Section 13, Challenge-Round Questions",
                section(v9, "## 13. ", None)),
        "PART_A": ("ABS-0004 v9, metadata and Sections 1 to 4 (of 13)",
                   v9[:v9.index("## 5. Canonical Relations")].rstrip()),
        "PART_B": ("ABS-0004 v9, Sections 5 to 13 (of 13)",
                   v9[v9.index("## 5. Canonical Relations"):].rstrip()),
    }

    BASE.mkdir(parents=True, exist_ok=True)
    manifest = {"round_label": "abs-0004-v9-admission-review",
                "question_author": "packaging executor, per DECISION-20260805-0002",
                "questions": []}
    print(f"{'question':<52}{'chars':>8}{'est tok':>9}")
    for qid, q in QUESTIONS.items():
        parts = [PREAMBLE, f"=== QUESTION {qid} ===\n{q['text']}"]
        ev = []
        for key in q["sections"]:
            label, body = units[key]
            parts.append(f"=== EVIDENCE {label} ===\n{body}")
            ev.append({"unit_id": label, "chars": len(body),
                       "source_sha256": hashlib.sha256(body.encode()).hexdigest()})
        parts.append("--- END OF EVIDENCE ---\n\nAnswer only the question above. If the "
                     "evidence set is insufficient, say so and name what is missing.")
        prompt = "\n\n".join(parts)
        path = BASE / f"{qid}-{q['slug']}.txt"
        path.write_text(prompt + "\n")
        manifest["questions"].append({
            "question_id": qid, "slug": q["slug"], "prompt_path": str(path),
            "evidence_units": ev, "prompt_chars": len(prompt),
            "est_input_tokens": int(len(prompt) / 2.7),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()})
        print(f"  {qid} {q['slug']:<48}{len(prompt):>8}{int(len(prompt)/2.7):>9}")

    (BASE / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    big = max(manifest["questions"], key=lambda x: x["est_input_tokens"])
    print(f"\nlargest: {big['question_id']} at {big['est_input_tokens']} est input tokens")
    print(f"PRE-FLIGHT: python3 preflight_prompt.py {big['prompt_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
