"""Finite-sample simulation STOP gate (PREREG §7; WARR-20260912-0001 cond. 9).

The exact implemented staged procedure — block structure, look schedule,
Lan-DeMets critical values, paired-Wald interval, POSITIVE/NEGATIVE rules —
is simulated at the boundary case Delta = SESOI over the preregistered grid
of discordance rates q and every attainable schedule. The primary statistic
depends only on (b, c, N), so per-block binomial draws of discordant pairs
are an exact simulation of iid pairs. Pass: P(ever POSITIVE or NEGATIVE at
Delta = SESOI) <= alpha + epsilon in every cell.
"""

from __future__ import annotations

import bisect
import json
import math
import random
from dataclasses import asdict, dataclass

from .scoring import Paired, adjudicate, required_pairs
from .sequential import ALPHA, Schedule, blocks, schedule_for

Q_GRID = (0.05, 0.10, 0.20, 0.30, 0.40)
N_FIXED = (1200, 1752, 2616)
SESOI = 0.03
EPSILON = 0.01
N_MAX = 2616


class _Binomial:
    """Inverse-CDF binomial sampler with cached CDF tables (standard library only)."""

    def __init__(self) -> None:
        self._cdf: dict[tuple[int, float], list[float]] = {}

    def table(self, n: int, p: float) -> list[float]:
        key = (n, round(p, 12))
        t = self._cdf.get(key)
        if t is None:
            logp, log1p = (math.log(p) if p > 0 else -math.inf), (math.log1p(-p) if p < 1 else -math.inf)
            acc, t = 0.0, []
            for k in range(n + 1):
                if p == 0:
                    pk = 1.0 if k == 0 else 0.0
                elif p == 1:
                    pk = 1.0 if k == n else 0.0
                else:
                    pk = math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * logp + (n - k) * log1p)
                acc += pk
                t.append(acc)
            t[-1] = 1.0
            self._cdf[key] = t
        return t

    def draw(self, n: int, p: float, rng: random.Random) -> int:
        if n == 0:
            return 0
        return bisect.bisect_left(self.table(n, p), rng.random())


@dataclass(frozen=True)
class CellResult:
    q: float
    n_req: int
    looks: tuple[int, ...]
    z: tuple[float, ...]
    reps: int
    p_positive: float
    p_negative: float
    p_error: float
    passed: bool


def attainable_schedules() -> list[tuple[float, int]]:
    """(q, N_req) cells: fixed N values crossed with the q grid, plus the N
    implied by each q (when within budget)."""
    cells: list[tuple[float, int]] = []
    for q in Q_GRID:
        for n in N_FIXED:
            cells.append((q, n))
        n_q = required_pairs(q)
        if n_q <= N_MAX and n_q not in N_FIXED:
            cells.append((q, n_q))
    return sorted(set(cells))


def simulate_cell(q: float, schedule: Schedule, delta: float, reps: int, seed: int, sesoi: float = SESOI) -> CellResult:
    rng = random.Random(f"RS-gate|{q}|{schedule.n_req}|{delta}|{seed}")
    binom = _Binomial()
    p_b = min(1.0, max(0.0, (q + delta) / (2 * q)))  # P(arm2-only correct | discordant)
    blks = blocks(schedule.n_req)
    look_at = {n: i for i, n in enumerate(schedule.looks)}
    pos = neg = 0
    for _ in range(reps):
        b = c = n = 0
        verdict = "INCONCLUSIVE"
        for m in blks:
            d = binom.draw(m, q, rng)
            bb = binom.draw(d, p_b, rng)
            b, c, n = b + bb, c + (d - bb), n + m
            if n in look_at:
                verdict = adjudicate(Paired(n, b, c), schedule.z[look_at[n]], sesoi)
                if verdict != "INCONCLUSIVE":
                    break
        if verdict == "POSITIVE":
            pos += 1
        elif verdict == "NEGATIVE":
            neg += 1
    p_err = (pos + neg) / reps
    return CellResult(q, schedule.n_req, schedule.looks, schedule.z, reps, pos / reps, neg / reps, p_err, p_err <= ALPHA + EPSILON)


def run_gate(reps: int = 20000, seed: int = 20260912, delta: float = SESOI) -> dict:
    schedules: dict[int, Schedule] = {}
    results: list[CellResult] = []
    for q, n_req in attainable_schedules():
        if n_req not in schedules:
            schedules[n_req] = schedule_for(n_req)
        results.append(simulate_cell(q, schedules[n_req], delta, reps, seed))
    return {
        "gate": "PREREG-RS-0001 v0.3.1 finite-sample check",
        "delta": delta,
        "sesoi": SESOI,
        "alpha": ALPHA,
        "epsilon": EPSILON,
        "reps_per_cell": reps,
        "seed": seed,
        "passed": all(r.passed for r in results),
        "cells": [asdict(r) for r in results],
    }


if __name__ == "__main__":  # python -m ai_lab.experiments.relational_state.gate [reps]
    import sys

    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    print(json.dumps(run_gate(reps), indent=1))
