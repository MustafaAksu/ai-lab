"""Canonical puzzle model: clue atoms, puzzles, trials, identifiers.

The canonical clue multiset is the single source of truth (PREREG §4.2). Both
renderings are lossless serializations of it and decode back to it (A1-A3).
Handles are never deduplicated by descriptor equality (A5): a person or item is
an index into the puzzle's handle list, not its visible clue neighbourhood.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable

RELATIONS = ("EQUAL", "NOT_EQUAL")

# Disjoint neutral vocabularies (PREREG §4.1): invented person tokens, generic
# object tokens. No real-person names, no culturally loaded items.
PERSON_VOCAB = ("Ando", "Brix", "Calo", "Dren", "Evi", "Fen", "Gol", "Hux", "Ilo")
ITEM_VOCAB = ("kite", "lamp", "mask", "nail", "oar", "pen", "quill", "rope", "sail")
N_MAX_VOCAB = min(len(PERSON_VOCAB), len(ITEM_VOCAB))


@dataclass(frozen=True, order=True)
class Clue:
    """One clue atom: C<k> RELATION Person Item."""

    id: str
    relation: str
    person: str
    item: str

    def line(self) -> str:
        return f"{self.id} {self.relation} {self.person} {self.item}"

    @staticmethod
    def parse(text: str) -> "Clue":
        parts = text.split()
        if len(parts) != 4:
            raise ValueError(f"not a clue line: {text!r}")
        cid, rel, person, item = parts
        if rel not in RELATIONS:
            raise ValueError(f"unknown relation {rel!r} in {text!r}")
        return Clue(cid, rel, person, item)


@dataclass(frozen=True)
class Puzzle:
    """n persons, n items, one-to-one assignment, clue list in instance order."""

    persons: tuple[str, ...]
    items: tuple[str, ...]
    clues: tuple[Clue, ...]

    @property
    def n(self) -> int:
        return len(self.persons)

    def canonical_multiset(self) -> tuple[Clue, ...]:
        """Sorted clue atoms; equality of multisets is equality of this tuple."""
        return tuple(sorted(self.clues))

    def puzzle_id(self) -> str:
        payload = {
            "persons": list(self.persons),
            "items": list(self.items),
            "clues": [c.line() for c in self.canonical_multiset()],
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def validate(self) -> None:
        if len(set(self.persons)) != self.n or len(set(self.items)) != self.n:
            raise ValueError("handles must be distinct within their class")
        if set(self.persons) & set(self.items):
            raise ValueError("person and item vocabularies must be disjoint")
        ids = [c.id for c in self.clues]
        if len(set(ids)) != len(ids):
            raise ValueError("clue ids must be unique")
        for c in self.clues:
            if c.person not in self.persons or c.item not in self.items:
                raise ValueError(f"clue {c.id} references an unknown handle")


@dataclass(frozen=True)
class Trial:
    puzzle: Puzzle
    target: str

    def trial_id(self) -> str:
        return hashlib.sha256(f"{self.puzzle.puzzle_id()}|{self.target}".encode("utf-8")).hexdigest()


def clue_lines(clues: Iterable[Clue]) -> list[str]:
    return [c.line() for c in clues]
