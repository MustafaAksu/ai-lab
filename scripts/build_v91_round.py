#!/usr/bin/env python3
"""Build the re-review round for ABS-0004 v9.1.

Scope is fixed by DECISION-20260811-0001: re-run only the questions whose
evidence sets prevented reliable judgment, with the prerequisite artifacts
supplied. Five questions, not nine.

The dominant defect of the v9 round was mine. Seven of nine questions reported
material evidence insufficiency, and the question set and its evidence sets were
both the question author's choices. Q7 asked reviewers to assess fourteen
challenge questions while supplying the question list and metadata only; one
reviewer could substantively evaluate one of the fourteen.

So this builder enforces the rule I identified in July and never implemented: an
evidence unit's citations are part of its scope. Every constraint, principle,
section and record id a prompt names must either be present in that prompt's
evidence or be explicitly declared as omitted. The check is mechanical and runs
before any prompt is written. Four consecutive rounds shipped prompts citing
material they did not attach; a rule in a script remembers better than I do.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

ONTO = pathlib.Path("docs/abstractions/ABS-0004-invocation-authorization-ontology.md")
V4 = "56f18a2ab7b66b1855b631a32d540f654c62b2c2"
BASE = pathlib.Path("docs/comparisons/comp_v91")
CEILING = 13000  # tokens; 13474 completed with headroom, 17533 returned nothing

PREAMBLE = """You are reviewing a proposed ontology amendment. This is ONE question \
of five, each asked in a separate call with its own evidence set. Do not attempt to \
answer the others.

Status: ABS-0004 v9.1 is proposed and not admitted. v4 is the last version with an \
admission event. v9.1 has no governance force.

Disclosures:

1. v9.1 is the CORRECTED successor to v9. A prior round, COMP-0126 to COMP-0134, \
found eight defects in v9; all eight were accepted by the operator and answered. You \
are reviewing the answers, not the original. Do not assume a correction is sound \
because it was made in response to a finding.

2. THIS IS A RE-RUN. Each of these five questions was asked of v9 and returned an \
answer qualified by insufficient evidence. The evidence sets were the question \
author's choices, and they were wrong. If this evidence set is still insufficient, \
say so and name precisely what is missing; that report is wanted output and the last \
round's version of it is why this round exists.

3. The executor that drafted v9, the corrections, and the version bump self-reports \
as gpt-5.6-thinking. One reviewer slot in this round is gpt-5.6-terra. The provider's \
own catalog asserts these are distinct model identities, and that catalog is a \
provider self-report. Nothing establishes whether they are the same executor. Under \
the corrected C3 you are reading, an invocation may not adjudicate a claim whose \
evidence ancestry contains an executor of unresolved equivalence. Your output is \
evidence for the accountable principal, not an adjudication.

4. The question author drafted ABS-0004 v5 through v8, all withdrawn or superseded, \
and drafted none of v9 or v9.1.

Answer in whatever form fits, but include three things: a VERDICT SENTENCE before the \
reasoning; any evidence you needed and did not have; and anything you found that this \
question did not ask about.

Quote only text that appears below. Do not certify or praise. No provider product \
recommendations."""

QUESTIONS = {
    "R1": {
        "slug": "does-the-corrected-inherited-constraint-hold",
        "units": ["METADATA", "S6", "V4_CONSTRAINTS", "DEC_0727_0005"],
        "declared_omissions": [],
        "text": """v9 was found to relocate rather than resolve the defect that \
withdrew v8. Its tag definition said an inherited constraint's "current governance \
force derives from v4's admission, not from the proposed v9 document", and reviewers \
found that this needs a rule — that verbatim reproduction of admitted text inside a \
non-admitted document carries the original admission's force forward — which the \
ontology did not state.

v9.1's answer has three parts: the tag definition, a new limitation stating that \
textual continuity does not establish semantic identity when referents differ, and \
the retagging of C3 to [PROPOSED_CONSTRAINT] because v4 never admitted it in its \
current semantic environment.

Does that answer hold? Consider: whether a reader with only this document can now \
check any inherited claim; whether the limitation does work or restates the problem; \
and whether the same argument that moved C3 to proposed applies to any constraint \
still tagged inherited. If it does, name them.""",
    },
    "R2": {
        "slug": "do-the-eleven-limitations-do-work",
        "units": ["ALL_LIMITATIONS", "S3", "S9"],
        "declared_omissions": [],
        "text": """The v9 round asked whether the limitation statements do work or \
wrap failures in accurate disclaimers. Four of nine were supplied and the answer was \
qualified accordingly. All eleven now in v9.1 are below, with the sections that \
carry most of them.

A prior synthesis characterised v8's failure mode as: a failed control retained in \
control-shaped language, wrapped in an accurate disclaimer, and delegated to a future \
mechanism or a careful reader.

Go statement by statement. For each, say what a reader could do differently because \
it is present, and what would be lost if it were deleted. Distinguish those that \
constrain how the ontology may be described from those that merely record an \
absence. If the set as a whole substitutes disclosure for remedy, say so.""",
    },
    "R3": {
        "slug": "does-the-fail-closed-c3-actually-close",
        "units": ["C3_FULL", "S4_3_4_4", "S4_18", "P5_FULL", "S9"],
        "declared_omissions": [],
        "text": """Two defects were accepted against v9 here. P5 said unknown facts \
block qualification while Section 4.18's derivation rule sent an unresolved dimension \
WITH a named compensating control to qualified_independent. And C3's prohibition \
applied only where equivalence was established, so an unresolved relation yielded a \
label rather than a bar.

v9.1 removes the compensating-control clause and adds an explicit fail-closed rule to \
C3.

Does it close? Construct a path by which an invocation adjudicates a claim whose \
evidence ancestry contains an executor it may be equivalent to, while satisfying \
every sentence below. If the corrected text prevents your construction, say which \
sentence stops it. Then state what "may not adjudicate" obliges of an implementation \
that has no mechanism to detect ancestry, and whether the rule is checkable or \
depends on the adjudicating party disclosing a relation it may not know it has.""",
    },
    "R4": {
        "slug": "seed-authority-after-correction",
        "units": ["S3", "S4_13", "METADATA"],
        "declared_omissions": [],
        "text": """One party drafts the root records, approves them, activates them, \
and relies on them as the terminus of every authorization chain. The version \
admission table records that v4 was admitted "by the operator as accountable \
principal in session, recorded in conversation only", and that no admission warrant \
exists for any amendment.

The v9 round found that the ontology does not distinguish that arrangement from one \
in which the seed is fabricated, and that AccountablePrincipal permits a pseudonymous \
identity with no required external anchor. Nothing in the A1 to A8 corrections \
addressed this.

Say whether that finding still holds against the text below. If it does, state what a \
record would have to contain to make the distinction, and whether such a record could \
exist inside the repository at all. Do not treat the operator's actual \
trustworthiness as evidence; the question is what the ontology represents.""",
    },
    "R5": {
        "slug": "are-the-inherited-challenge-questions-fit",
        "units": ["S13", "S6", "S9", "METADATA"],
        "declared_omissions": [
            "Section 4 object definitions, which several challenge questions reference "
            "by number. Attaching Section 4 would put this prompt over the size that "
            "has been demonstrated to complete. Where a question cannot be assessed "
            "without a definition, say which definition and treat that question as "
            "unassessed rather than guessing."
        ],
        "text": """Section 13 lists fourteen challenge-round questions. They were \
written for the v3 to v4 round and have been carried through v5, v6, v7, v8, v9 and \
v9.1 unchanged. Nobody has revisited them.

The v9 round asked this and supplied only the question list and the metadata; one \
reviewer could substantively assess one of the fourteen. The constraints and the \
enforcement matrix those questions refer to are now attached.

For each of the fourteen: answered, stale, still live, or unassessable on this \
evidence. At least one is stale on its face, asking whether "candidate Slice A" omits \
anything when Slice A is implemented and warranted.

Then state what the set does not ask. A question set inherited across six versions \
encodes the concerns of the version that wrote it; name the concerns of v9.1 it fails \
to cover, including any raised by the eight corrections just made.""",
    },
}

# what a prompt may cite without attaching: ids that name records outside the
# ontology, which a reviewer is told about rather than expected to read
EXEMPT = re.compile(r"COMP-\d{4}|WARR-\d{8}-\d{4}|VERIFY-\d{8}-\d{4}|PLAN-\d{8}-\d{4}")


def sec(text: str, start: str, end: str | None) -> str:
    i = text.index(start)
    return text[i:] .rstrip() if end is None else text[i:text.index(end, i + len(start))].rstrip()


def build_units(onto: str) -> dict[str, tuple[str, str]]:
    v4 = subprocess.run(["git", "show", f"{V4}:{ONTO}"], capture_output=True, text=True).stdout
    lines = onto.splitlines()
    limitation_blocks = []
    for m in re.finditer(r"`\[LIMITATION\]`(.*?)(?=\n\n|`\[)", onto, re.S):
        limitation_blocks.append("`[LIMITATION]`" + m.group(1).rstrip())
    dec = json.loads(pathlib.Path(
        "docs/self_model/decisions/DECISION-20260727-0005.json").read_text())
    return {
        "METADATA": ("ABS-0004 v9.1 metadata and version admission table",
                     "\n".join(lines[3:60])),
        "S3": ("Section 3, Three Decisions", sec(onto, "## 3. Three Decisions", "## 4. ")),
        "S4_3_4_4": ("Sections 4.3 and 4.4, ModelIdentity and CatalogSnapshot",
                     sec(onto, "### 4.3 ", "### 4.5 ")),
        "S4_13": ("Section 4.13, DecisionRecord and AccountablePrincipal",
                  sec(onto, "### 4.13 ", "### 4.14 ")),
        "S4_18": ("Section 4.18, IndependenceAssessment",
                  sec(onto, "### 4.18 ", "## 5. ")),
        "S6": ("Section 6, Epistemic Constraints, carrying every constraint C1 to C11",
               sec(onto, "## 6. Epistemic Constraints", "## 7. ")),
        "S9": ("Section 9, Enforcement Matrix", sec(onto, "## 9. Enforcement Matrix", "## 10. ")),
        "S13": ("Section 13, Challenge-Round Questions", sec(onto, "## 13. ", None)),
        "C3_FULL": ("Constraint C3 as corrected, in full",
                    re.search(r"`\[PROPOSED_CONSTRAINT\]` C3 .*?(?=`\[)", onto, re.S).group(0).rstrip()),
        "P5_FULL": ("Principle P5, in full",
                    re.search(r"`\[PRINCIPLE\]` P5\..*?(?=`\[)", onto, re.S).group(0).rstrip()),
        "ALL_LIMITATIONS": (f"All {len(limitation_blocks)} [LIMITATION] statements in v9.1",
                            "\n\n".join(limitation_blocks)),
        "V4_CONSTRAINTS": ("Admitted ABS-0004 v4, Section 6, for comparison with the "
                           "inherited constraints",
                           sec(v4, "## 6. Epistemic Constraints", "## 7. ")),
        "DEC_0727_0005": ("DECISION-20260727-0005, which adopted the "
                          "[INHERITED_CONSTRAINT] category",
                          json.dumps(dec, indent=2, sort_keys=True)),
    }


def crossrefs(text: str) -> set[str]:
    """Constraints, principles and sections a prompt names."""
    out = set()
    out |= {f"C{n}" for n in re.findall(r"\bC(\d{1,2})\b", text)}
    out |= {f"P{n}" for n in re.findall(r"\bP(\d)\b", text)}
    out |= {f"S{n}" for n in re.findall(r"[Ss]ection (\d+(?:\.\d+)?)", text)}
    return out


def main() -> int:
    onto = ONTO.read_text()
    units = build_units(onto)
    BASE.mkdir(parents=True, exist_ok=True)
    manifest = {"round_label": "abs-0004-v9.1-re-review",
                "scope": "the five questions whose v9 evidence sets prevented judgment",
                "question_author": "packaging executor, per DECISION-20260811-0001",
                "questions": []}
    problems: list[str] = []

    print(f"{'question':<50}{'chars':>8}{'est tok':>9}  units")
    for qid, q in QUESTIONS.items():
        ev_text = "\n\n".join(units[u][1] for u in q["units"])
        # every constraint, principle or section the QUESTION names must be present
        # in the evidence it is given, or be declared omitted.
        named = crossrefs(q["text"])
        declared = " ".join(q["declared_omissions"])
        for ref in sorted(named):
            if EXEMPT.fullmatch(ref):
                continue
            token = ref if ref.startswith(("C", "P")) else ref[1:]
            present = (re.search(rf"`\[[A-Z_]+\]` {token}[ .]", ev_text) is not None
                       or re.search(rf"^\| {token} ", ev_text, re.M) is not None
                       or (ref.startswith("S") and f"{token} " in ev_text[:400])
                       or re.search(rf"### {token} |## {token}\. ", ev_text) is not None)
            if not present and token not in declared:
                problems.append(f"{qid} names {ref} but its evidence does not contain "
                                f"it and it is not a declared omission")

        parts = [PREAMBLE, f"=== QUESTION {qid} ===\n{q['text']}"]
        if q["declared_omissions"]:
            parts.append("=== DECLARED OMISSIONS ===\n" +
                         "\n".join(f"- {o}" for o in q["declared_omissions"]))
        ev_meta = []
        for u in q["units"]:
            label, body = units[u]
            parts.append(f"=== EVIDENCE {label} ===\n{body}")
            ev_meta.append({"unit_id": label, "chars": len(body),
                            "source_sha256": hashlib.sha256(body.encode()).hexdigest()})
        parts.append("--- END OF EVIDENCE ---\n\nAnswer only the question above.")
        prompt = "\n\n".join(parts)
        est = int(len(prompt) / 2.7)
        if est > CEILING:
            problems.append(f"{qid} is {est} est tokens, over the {CEILING} ceiling")
        path = BASE / f"{qid}-{q['slug']}.txt"
        path.write_text(prompt + "\n")
        manifest["questions"].append({
            "question_id": qid, "slug": q["slug"], "prompt_path": str(path),
            "evidence_units": ev_meta,
            "declared_omissions": q["declared_omissions"],
            "prompt_chars": len(prompt), "est_input_tokens": est,
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()})
        print(f"  {qid} {q['slug']:<46}{len(prompt):>8}{est:>9}  {len(q['units'])}")

    if problems:
        print("\nCROSS-REFERENCE CHECK FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1

    (BASE / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    big = max(manifest["questions"], key=lambda x: x["est_input_tokens"])
    print(f"\ncross-reference check passed: every constraint, principle and section "
          f"named by a question is present in its evidence or declared omitted")
    print(f"largest: {big['question_id']} at {big['est_input_tokens']} est tok "
          f"(ceiling {CEILING})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
