import itertools
import random

from ai_lab.experiments.relational_state.depth import RULES_FROZEN, depth, initial_board, row_set, wave
from ai_lab.experiments.relational_state.model import ITEM_VOCAB, PERSON_VOCAB, Clue, Puzzle, Trial
from ai_lab.experiments.relational_state.oracle import admissible_for, oracle_status, solutions


def _random_puzzle(rng, n):
    persons, items = PERSON_VOCAB[:n], ITEM_VOCAB[:n]
    clues = []
    for i in range(rng.randint(0, 2 * n)):
        rel = rng.choice(("EQUAL", "NOT_EQUAL"))
        clues.append(Clue(f"C{i + 1}", rel, rng.choice(persons), rng.choice(items)))
    return Puzzle(persons, items, tuple(clues))


def _brute(puzzle):
    out = []
    for perm in itertools.permutations(puzzle.items):
        a = dict(zip(puzzle.persons, perm))
        if all((a[c.person] == c.item) == (c.relation == "EQUAL") for c in puzzle.clues):
            out.append(a)
    return sorted(sorted(s.items()) for s in out)


def test_oracle_matches_brute_force_enumeration():
    rng = random.Random(1)
    for _ in range(300):
        pz = _random_puzzle(rng, rng.randint(2, 5))
        assert sorted(sorted(s.items()) for s in solutions(pz)) == _brute(pz)


def test_oracle_limit_stops_early_but_never_undercounts_below_limit():
    rng = random.Random(2)
    for _ in range(100):
        pz = _random_puzzle(rng, 4)
        full, limited = solutions(pz), solutions(pz, limit=2)
        assert len(limited) == min(len(full), 3) or len(limited) == len(full)


def test_ids_are_content_addressed_and_target_specific():
    pz = Puzzle(PERSON_VOCAB[:3], ITEM_VOCAB[:3], (Clue("C1", "EQUAL", "Ando", "kite"),))
    pz2 = Puzzle(PERSON_VOCAB[:3], ITEM_VOCAB[:3], (Clue("C1", "EQUAL", "Ando", "kite"),))
    assert pz.puzzle_id() == pz2.puzzle_id()
    assert Trial(pz, "Ando").trial_id() != Trial(pz, "Brix").trial_id()
    pz.validate()


def test_depth_rounds_are_synchronous_waves():
    # chain: Ando fixed at round 0; Brix keeps {kite, lamp}; Calo keeps {lamp, mask}
    persons, items = PERSON_VOCAB[:4], ITEM_VOCAB[:4]
    clues = (
        Clue("C1", "EQUAL", "Ando", "kite"),
        Clue("C2", "NOT_EQUAL", "Brix", "mask"), Clue("C3", "NOT_EQUAL", "Brix", "nail"),
        Clue("C4", "NOT_EQUAL", "Calo", "kite"), Clue("C5", "NOT_EQUAL", "Calo", "nail"),
        Clue("C6", "NOT_EQUAL", "Dren", "kite"), Clue("C7", "NOT_EQUAL", "Dren", "lamp"),
    )
    pz = Puzzle(persons, items, clues)
    b0 = initial_board(pz)
    assert row_set(b0, "Brix") == ("kite", "lamp") and row_set(b0, "Calo") == ("lamp", "mask")
    b1 = wave(pz, b0)
    assert row_set(b1, "Brix") == ("lamp",)          # R1 from Ando removes kite
    assert row_set(b1, "Calo") == ("lamp", "mask")   # Brix's singleton is NOT re-applied in the same round
    b2 = wave(pz, b1)
    assert row_set(b2, "Calo") == ("mask",)
    assert depth(pz, "Brix") == (1, "singleton")
    assert depth(pz, "Calo") == (2, "singleton")
    assert RULES_FROZEN == ("R1",)


def test_r2_is_not_applied_under_frozen_rules():
    # Only Ando's row admits kite; hidden-single (R2) would fix Ando at round 1,
    # the frozen R1-only propagator leaves the board at its fixed point.
    persons, items = PERSON_VOCAB[:3], ITEM_VOCAB[:3]
    clues = (Clue("C1", "NOT_EQUAL", "Brix", "kite"), Clue("C2", "NOT_EQUAL", "Calo", "kite"))
    pz = Puzzle(persons, items, clues)
    assert depth(pz, "Ando") == (0, "fixed_point")
    assert depth(pz, "Ando", rules=("R1", "R2")) == (1, "singleton")


def test_depth_fixed_point_kind_for_ambiguous_target():
    persons, items = PERSON_VOCAB[:3], ITEM_VOCAB[:3]
    pz = Puzzle(persons, items, (Clue("C1", "EQUAL", "Ando", "kite"),))
    assert oracle_status(pz, "Brix") == ("ambiguous", ("lamp", "mask"))
    d, kind = depth(pz, "Brix")
    assert kind == "fixed_point"
    assert admissible_for(pz, "Ando") == ("kite",)
