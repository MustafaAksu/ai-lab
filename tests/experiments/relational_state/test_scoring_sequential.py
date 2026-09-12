import pytest

from ai_lab.experiments.relational_state.scoring import Paired, adjudicate, fcr, parse_output, required_pairs, score
from ai_lab.experiments.relational_state.sequential import blocks, critical_values, look_schedule, schedule_for, spending


def test_parse_and_score():
    p = parse_output('Sure. {"status": "ambiguous", "answer": ["nail", "lamp"]} trailing')
    assert p.ok and p.status == "ambiguous" and p.answer == ("lamp", "nail")
    assert score(p, "ambiguous", ("lamp", "nail"))
    assert not score(p, "unique", ("lamp",))
    assert not parse_output("no json here").ok
    assert not parse_output('{"status": "maybe", "answer": []}').ok
    assert not score(parse_output(""), "unique", ("kite",))


def test_required_pairs_matches_preregistered_examples():
    assert required_pairs(0.10) == 1200   # 871 -> floor
    assert required_pairs(0.20) == 1752   # 1742 -> next multiple of 24
    assert required_pairs(0.30) == 2616   # 2613 -> 2616
    assert required_pairs(0.40) > 2616


def test_paired_wald_and_adjudication():
    p = Paired(1200, 90, 30)
    lo, hi = p.wald_ci(1.96)
    assert p.delta_hat == pytest.approx(0.05)
    assert lo < 0.05 < hi
    assert adjudicate(Paired(1200, 120, 20), 1.96, 0.03) == "POSITIVE"
    assert adjudicate(Paired(1200, 20, 20), 1.96, 0.03) == "NEGATIVE"
    assert adjudicate(Paired(1200, 60, 30), 1.96, 0.03) == "INCONCLUSIVE"
    assert Paired(100, 5, 5).mcnemar_p() == 1.0


def test_fcr():
    rows = [(2, "unique", ("kite",)), (2, "ambiguous", ("kite", "lamp")), (1, "unique", ("kite",))]
    assert fcr(rows) == 0.5
    assert fcr([(1, "unique", ("kite",))]) is None


def test_spending_function_endpoints():
    assert spending(0.0) == 0.0 and spending(1.0) == pytest.approx(0.05)
    assert spending(0.25) == pytest.approx(2 * (1 - 0.999955), abs=2e-5)


def test_critical_values_frozen_formula_and_reference_fixture():
    # Frozen PREREG formula alpha(t) = 2[1 - Phi(z_.975 / sqrt t)], four equal looks.
    z = critical_values((0.25, 0.5, 0.75, 1.0))
    assert [round(c, 2) for c in z] == [3.92, 2.78, 2.30, 2.04]
    # Reference fixture (NOT used operatively): the gsDesign/Reboussin
    # per-tail convention (alpha = 0.025 spent per side) gives 4.333, 2.963,
    # 2.359, 2.014. It differs from the frozen formula and is recorded here
    # only so the two conventions are never confused.
    assert critical_values((1.0,))[0] == pytest.approx(1.96, abs=1e-3)
    assert list(z) == sorted(z, reverse=True)


def test_schedules_and_blocks():
    assert look_schedule(1200) == (720, 1200)
    assert look_schedule(1752) == (720, 1440, 1752)
    assert look_schedule(2616) == (720, 1440, 2160, 2616)
    assert blocks(2616) == (240,) * 10 + (216,) and sum(blocks(2616)) == 2616 and 216 % 24 == 0
    assert blocks(1200) == (240,) * 5
    s = schedule_for(1200)
    assert s.t == (0.6, 1.0) and len(s.z) == 2
