"""Admission invariants A1-A6 and query independence (PREREG §6).

Every instance passes through `audit` before any provider call; a failure
names the invariant and excludes the instance.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .model import Puzzle, Trial
from .render import decode, inference_derived_facts, render_flat, render_rm, state_block


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
    """A5: rendering and decoding never merge two handles, even when their
    visible clue neighbourhoods are identical."""
    for arm_text in (render_flat(puzzle), render_rm(puzzle)):
        clues, _ = decode(arm_text)
        persons = {c.person for c in clues} | set(puzzle.persons)
        items = {c.item for c in clues} | set(puzzle.items)
        if len(persons) != puzzle.n or len(items) != puzzle.n:
            return False
    return True
