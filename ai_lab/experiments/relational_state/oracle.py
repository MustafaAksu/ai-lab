"""Exhaustive oracle: the set of all assignments consistent with the clues.

Truth is defined by enumeration (PREREG §2 F7, §7). Backtracking over
persons with early pruning; `limit` stops enumeration once more than `limit`
solutions are known, which is all the generator needs.
"""

from __future__ import annotations

from .model import Puzzle

Assignment = dict[str, str]


def solutions(puzzle: Puzzle, limit: int | None = None) -> list[Assignment]:
    persons, items = puzzle.persons, puzzle.items
    forbidden: dict[str, set[str]] = {p: set() for p in persons}
    forced: dict[str, str] = {}
    for c in puzzle.clues:
        if c.relation == "EQUAL":
            if c.person in forced and forced[c.person] != c.item:
                return []
            forced[c.person] = c.item
        else:
            forbidden[c.person].add(c.item)
    out: list[Assignment] = []
    used: set[str] = set()
    current: Assignment = {}

    def rec(i: int) -> bool:
        if i == len(persons):
            out.append(dict(current))
            return limit is not None and len(out) > limit
        p = persons[i]
        candidates = (forced[p],) if p in forced else items
        for it in candidates:
            if it in used or it in forbidden[p]:
                continue
            used.add(it)
            current[p] = it
            stop = rec(i + 1)
            used.discard(it)
            del current[p]
            if stop:
                return True
        return False

    rec(0)
    return out


def admissible_for(puzzle: Puzzle, target: str) -> tuple[str, ...]:
    """Omega_q: the sorted set of items the target may have across all solutions."""
    return tuple(sorted({s[target] for s in solutions(puzzle)}))


def oracle_status(puzzle: Puzzle, target: str) -> tuple[str, tuple[str, ...]]:
    omega = admissible_for(puzzle, target)
    if not omega:
        return "inconsistent", ()
    return ("unique" if len(omega) == 1 else "ambiguous"), omega
