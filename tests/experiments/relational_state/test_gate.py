from ai_lab.experiments.relational_state.gate import EPSILON, Q_GRID, attainable_schedules, run_gate


def test_attainable_schedules_cover_fixed_n_and_within_budget_q():
    cells = attainable_schedules()
    assert all(n <= 2616 for _, n in cells)
    assert {n for _, n in cells} == {1200, 1752, 2616}
    assert {q for q, _ in cells} == set(Q_GRID)


def test_gate_passes_at_reduced_replications():
    # The admitted gate runs at >= 20,000 replications per cell (report filed
    # under docs/research/experiments/relational_state/); this regression
    # exercises the identical code path at 1,500 with a fixed seed.
    # At 1,500 replications the Monte-Carlo standard error of p_error is about
    # 0.006, so the reduced-replication check allows epsilon + 3 SE.
    report = run_gate(reps=1500, seed=7)
    assert report["epsilon"] == EPSILON
    se = (0.05 * 0.95 / 1500) ** 0.5
    for c in report["cells"]:
        assert c["p_error"] <= 0.05 + EPSILON + 3 * se, c
        assert c["p_error"] >= 0.02, c
