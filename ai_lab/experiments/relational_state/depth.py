"""PROP-RS-0: synchronous-wave propagator defining the depth coordinate.

PREREG §4.2. Depth is a difficulty coordinate only; it does not define truth
and no completeness claim is made (§2 F1, F7).

Board: admissible[person][item] booleans. Round 0 applies every clue atom.
One round = one simultaneous wave computed from the board at the start of the
round: R1 a person with exactly one admissible item removes that item from
every other person. (R2, the hidden-single rule, was removed by amendment
v0.3.2 — finding F1 — and remains available only through the `rules`
parameter for zero-API evaluation; it is never used for labelling.) The rule
reads the start-of-round board only; consequences derived within a round are
not re-applied until the next round.
"""

from __future__ import annotations

from .model import Puzzle

Board = dict[str, dict[str, bool]]


def initial_board(puzzle: Puzzle) -> Board:
    board: Board = {p: {it: True for it in puzzle.items} for p in puzzle.persons}
    for c in puzzle.clues:  # round 0
        if c.relation == "EQUAL":
            for it in puzzle.items:
                if it != c.item:
                    board[c.person][it] = False
        else:
            board[c.person][c.item] = False
    return board


RULES_FROZEN = ("R1",)  # PREREG-RS-0001 v0.3.2 §4.2 (amended from R1+R2; see F1)


def wave(puzzle: Puzzle, board: Board, rules: tuple[str, ...] = RULES_FROZEN) -> Board:
    """One synchronous round; reads only `board`, writes a fresh board.

    `rules` exists only so that amendment candidates can be evaluated
    zero-API; the frozen rule set is the default and the only one the
    generator labels with.
    """
    persons, items = puzzle.persons, puzzle.items
    nxt: Board = {p: dict(board[p]) for p in persons}
    # R1: a person with exactly one admissible item -> that item leaves every other row
    for p in (persons if "R1" in rules else ()):
        row = [it for it in items if board[p][it]]
        if len(row) == 1:
            for q in persons:
                if q != p:
                    nxt[q][row[0]] = False
    # R2: an item admissible for exactly one person -> that person loses every other item
    for it in (items if "R2" in rules else ()):
        col = [p for p in persons if board[p][it]]
        if len(col) == 1:
            for jt in items:
                if jt != it:
                    nxt[col[0]][jt] = False
    return nxt


def row_set(board: Board, person: str) -> tuple[str, ...]:
    return tuple(sorted(it for it, ok in board[person].items() if ok))


def depth(puzzle: Puzzle, target: str, max_rounds: int = 64, rules: tuple[str, ...] = RULES_FROZEN) -> tuple[int, str]:
    """Return (d, kind): kind 'singleton' when the target row became a
    singleton at round d, or 'fixed_point' when the board stopped changing at
    round d without the target becoming a singleton. Round 0 is clue application.
    """
    board = initial_board(puzzle)
    if len(row_set(board, target)) == 1:
        return 0, "singleton"
    for r in range(1, max_rounds + 1):
        nxt = wave(puzzle, board, rules)
        if len(row_set(nxt, target)) == 1:
            return r, "singleton"
        if nxt == board:
            return r - 1, "fixed_point"
        board = nxt
    raise RuntimeError("PROP-RS-0 did not converge")
