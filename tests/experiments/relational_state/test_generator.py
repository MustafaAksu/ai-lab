import pytest

from ai_lab.experiments.relational_state.depth import depth
from ai_lab.experiments.relational_state.generator import TARGET_STATES, generate, generate_stratum, populated
from ai_lab.experiments.relational_state.oracle import oracle_status, solutions


@pytest.mark.parametrize("n", range(3, 10))
@pytest.mark.parametrize("d", (1, 2, 3, 4))
@pytest.mark.parametrize("state", TARGET_STATES)
def test_every_populated_stratum_yields_verified_instances(n, d, state):
    if not populated(n, d, state):
        assert generate(n, d, state, 1) is None
        return
    insts = generate_stratum(n, d, state, 3, 100)
    assert len(insts) == 3
    assert len({i.trial.puzzle.puzzle_id() for i in insts}) == 3
    for inst in insts:
        pz, t = inst.trial.puzzle, inst.trial.target
        pz.validate()
        status, omega = oracle_status(pz, t)
        assert status == state and omega == inst.omega
        assert len(solutions(pz)) == (1 if state == "unique" else 2)
        assert depth(pz, t) == (d, "singleton" if state == "unique" else "fixed_point")
        assert all(c.relation in ("EQUAL", "NOT_EQUAL") for c in pz.clues)


def test_occupancy_bound_is_the_recorded_one():
    # PROP-RS-0 = R1-only (v0.3.2): unique n >= d+1, ambiguous n >= d+2
    assert populated(5, 4, "unique") and not populated(4, 4, "unique")
    assert populated(6, 4, "ambiguous") and not populated(5, 4, "ambiguous")
    assert all(populated(n, d, s) for n in (6, 7, 8, 9) for d in (1, 2, 3, 4) for s in ("unique", "ambiguous"))
    assert not populated(9, 0, "unique")


def test_generation_is_deterministic_in_seed():
    a, b = generate(6, 3, "unique", 42), generate(6, 3, "unique", 42)
    assert a is not None and a.trial.puzzle == b.trial.puzzle and a.trial.target == b.trial.target
