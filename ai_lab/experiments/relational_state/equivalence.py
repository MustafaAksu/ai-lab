"""Admission invariants A1-A6 and query independence (PREREG §6).

Every instance passes through `audit` before any provider call; a failure
names the invariant and excludes the instance.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .model import Puzzle, Trial
from .render import decode, frame, inference_derived_facts, render_flat, render_index, render_rm, state_block


@dataclass(frozen=True)
class AuditResult:
    ok: bool
    failed: tuple[str, ...]


def _multiset(clues) -> Counter:
    return Counter(c.line() for c in clues)


def audit(puzzle: Puzzle) -> AuditResult:
    failed: list[str] = []
    canonical = _multiset(puzzle.canonical_multiset())
    flat, rm = render_flat(puzzle), render_rm(puzzle)
    d1, _ = decode(flat)
    d2, _ = decode(rm)
    if _multiset(d1) != canonical:
        failed.append("A1")
    if _multiset(d2) != canonical:
        failed.append("A2")
    if _multiset(d1) != _multiset(d2):
        failed.append("A3")
    if inference_derived_facts(rm, puzzle):
        failed.append("A4")
    # A6: every clue body occurs exactly once per rendering
    for label, text in (("A6", flat), ("A6", rm)):
        counts = Counter(ln for ln in text.splitlines() if ln and not ln.startswith((" ", "\t")))
        if any(counts[c.line()] != 1 for c in puzzle.clues):
            if label not in failed:
                failed.append(label)
    return AuditResult(not failed, tuple(failed))


def query_independent(puzzle: Puzzle) -> bool:
    """Both state blocks are byte-identical under every possible target."""
    blocks = {
        arm: {state_block(Trial(puzzle, t), arm) for t in puzzle.persons}
        for arm in (1, 2)
    }
    return all(len(v) == 1 for v in blocks.values())


def distinct_handles_preserved(puzzle: Puzzle) -> bool:
    """A5: the serialized artefacts (frame, clue table, index) carry exactly the
    declared distinct handles — derived from the rendered TEXT, never restored
    from the source object — so two handles with identical clue neighbourhoods
    cannot have been merged and no handle can have been dropped."""
    instruction, _ = frame(puzzle, puzzle.persons[0])
    lines = instruction.splitlines()
    frame_persons = [h.strip() for h in lines[1][len("Persons: "):-1].split(",")]
    frame_items = [h.strip() for h in lines[2][len("Items: "):-1].split(",")]
    index_handles = [ln.split(":")[0] for ln in render_index(puzzle).splitlines()]
    for arm_text in (render_flat(puzzle), render_rm(puzzle)):
        clues, _ = decode(arm_text)
        if not {c.person for c in clues} <= set(frame_persons) or not {c.item for c in clues} <= set(frame_items):
            return False
    n = puzzle.n
    return (
        len(frame_persons) == n == len(set(frame_persons))
        and len(frame_items) == n == len(set(frame_items))
        and set(frame_persons) == set(puzzle.persons)
        and set(frame_items) == set(puzzle.items)
        and set(index_handles) == set(puzzle.persons) | set(puzzle.items)
        and len(index_handles) == 2 * n
    )


def admit_instance(puzzle: Puzzle) -> AuditResult:
    """The single admission entry point: A1-A6 plus query independence.
    The runner calls this before every provider call (PREREG §6)."""
    base = audit(puzzle)
    failed = list(base.failed)
    if not distinct_handles_preserved(puzzle):
        failed.append("A5")
    if not query_independent(puzzle):
        failed.append("QI")
    failed = sorted(set(failed))
    return AuditResult(not failed, tuple(failed))
