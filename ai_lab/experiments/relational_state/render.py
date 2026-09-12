"""FLAT-v0 (Arm 1) and RM-v0 (Arm 2) renderings and the shared prompt frame.

PREREG §5. Both renderings are lossless serializations of the canonical clue
multiset. RM-v0 = the clue table ONCE (byte-identical to FLAT-v0) followed by
an adjacency index of clue IDs only, in canonical handle order (first
appearance in the clue list; never target-first). The query names the target
and alters nothing in either state block (query independence).
"""

from __future__ import annotations

from .model import Clue, Puzzle, Trial

FLAT_VERSION = "FLAT-v0"
RM_VERSION = "RM-v0"
FRAME_VERSION = "FRAME-v0"

CLUES_HEADER = "CLUES"
INDEX_HEADER = "INDEX"


def clue_table(puzzle: Puzzle) -> str:
    return "\n".join(c.line() for c in puzzle.clues)


def render_flat(puzzle: Puzzle) -> str:
    return f"{CLUES_HEADER}\n{clue_table(puzzle)}"


def canonical_handle_order(puzzle: Puzzle) -> list[str]:
    """Handles in order of first appearance in the clue list; handles that
    appear in no clue follow in puzzle order (persons then items)."""
    seen: list[str] = []
    for c in puzzle.clues:
        for h in (c.person, c.item):
            if h not in seen:
                seen.append(h)
    for h in (*puzzle.persons, *puzzle.items):
        if h not in seen:
            seen.append(h)
    return seen


def render_index(puzzle: Puzzle) -> str:
    lines = []
    for h in canonical_handle_order(puzzle):
        ids = [c.id for c in puzzle.clues if h in (c.person, c.item)]
        lines.append(f"{h}: {' '.join(ids) if ids else '-'}")
    return "\n".join(lines)


def render_rm(puzzle: Puzzle) -> str:
    return f"{CLUES_HEADER}\n{clue_table(puzzle)}\n\n{INDEX_HEADER}\n{render_index(puzzle)}"


def frame(puzzle: Puzzle, target: str) -> tuple[str, str]:
    """(instruction block, query line) — identical across arms."""
    persons = ", ".join(puzzle.persons)
    items = ", ".join(puzzle.items)
    instruction = (
        "You are given a logic puzzle.\n"
        f"Persons: {persons}.\n"
        f"Items: {items}.\n"
        "Rules: every person has exactly one item and every item belongs to exactly one person.\n"
        "Clue lines have the form: <clue-id> <RELATION> <Person> <Item>, where EQUAL means the person "
        "has the item and NOT_EQUAL means the person does not have the item.\n"
        "If an INDEX section is present, each line lists, for one person or item, the ids of the clues "
        "that mention it; an index entry is a reference to a clue, not an additional clue.\n"
        "Answer with a single JSON object and nothing else, of the form "
        '{"status": "unique" | "ambiguous" | "inconsistent", "answer": ["<item>", ...]}. '
        "Use \"unique\" with one item when exactly one item is possible for the queried person, "
        "\"ambiguous\" with all possible items when more than one is possible, and "
        "\"inconsistent\" with an empty list when the clues admit no assignment."
    )
    query = f"Question: which item belongs to {target}?"
    return instruction, query


def prompt(trial: Trial, arm: int) -> str:
    instruction, query = frame(trial.puzzle, trial.target)
    state = render_flat(trial.puzzle) if arm == 1 else render_rm(trial.puzzle)
    return f"{instruction}\n\n{state}\n\n{query}"


def state_block(trial: Trial, arm: int) -> str:
    return render_flat(trial.puzzle) if arm == 1 else render_rm(trial.puzzle)


# --- decoding (A1-A4) -------------------------------------------------------

def decode(text: str) -> tuple[list[Clue], list[str]]:
    """Parse a rendering back to (clue list in rendered order, non-clue lines).

    Non-clue lines are the headers and index lines. Anything else is an
    inference-derived fact and is returned in the second list too, where the
    equivalence auditor will reject it.
    """
    clues: list[Clue] = []
    other: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            clues.append(Clue.parse(line))
        except ValueError:
            other.append(line)
    return clues, other


def inference_derived_facts(rm_text: str, puzzle: Puzzle) -> list[str]:
    """Lines of an RM-v0 rendering that are neither verbatim clue lines nor
    lines of the deterministic ID-only index (A4)."""
    allowed_index = set(render_index(puzzle).splitlines())
    allowed = allowed_index | {CLUES_HEADER, INDEX_HEADER}
    _, other = decode(rm_text)
    return [ln for ln in other if ln not in allowed]
