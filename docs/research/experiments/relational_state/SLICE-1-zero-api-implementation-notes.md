# PREREG-RS-0001 — Slice 1 (zero-API) implementation notes

**Plan / warrant:** PLAN-20260912-0001 / WARR-20260912-0001 (scope S1–S3)  
**Base commit:** `073b84f1c6588959be3ea186c5b64b4339125bc1`  
**Status:** implemented; awaiting reviewing-executor implementation verification (warrant condition 8). No `runner.py`, no provider call.

## What was built

`ai_lab/experiments/relational_state/` — `model` (clue atoms, puzzles, trials, `puzzle_id`/`trial_id`), `oracle` (exhaustive backtracking enumeration; truth), `depth` (PROP-RS-0 synchronous waves R1+R2; depth coordinate), `generator` (constructed instances per stratum, oracle- and depth-verified), `render` (FLAT-v0, RM-v0, shared FRAME-v0, decoder, A4 detector), `equivalence` (A1–A6, query independence, A5 guard), `scoring` (output parsing, per-trial score, paired Wald CI, exact McNemar, `required_pairs`, FCR), `sequential` (Lan–DeMets O'Brien–Fleming spending, sequential critical values by grid recursion, look schedule, balanced blocks), `gate` (finite-sample simulation STOP gate). All standard-library-only; the two-tier membrane is asserted by `tests/experiments/relational_state/test_membrane.py`, which also asserts `CAPTURE_PATHS` unchanged.

Gate result (20,000 replications per cell, seed 20260912): **PASS**, max p_error 0.0533 ≤ 0.06 — `GATE-RS-0001-finite-sample-20260912.json`.

## Findings for the reviewing executor (none applied silently)

**F1 — Stratum occupancy under the frozen PROP-RS-0 is narrower than the preregistration assumes.** With both rules (R1 naked single, R2 hidden single), R2 fixes a chain's last person as soon as its item's column is otherwise empty; keeping the target's column open until round d requires a guard chain of d−1 further persons. Verified bound: unique needs **n ≥ 2d**, ambiguous needs **n ≥ d+2** (`generator.populated`). Consequently `(n ≤ 7, d = 4, unique)` and `(n = 5, d = 3, unique)` are unpopulated, and the 24-strata main design is fully populated only for n ∈ {8, 9}. Zero-API probe of an amendment candidate — **R1-only** (naked singles) — gives unique n ≥ d+1 and ambiguous n ≥ d+2, i.e. all 24 strata populated for n ≥ 6. `depth.depth(..., rules=...)` carries the frozen default; the parameter exists only for this evaluation. **Decision required before calibration:** amend §4.2 to R1-only (recommended: it restores the intended family and keeps depth a pure cascade coordinate), or keep R1+R2 and restrict eligible calibration triples to n ≥ 8, or shift depth strata. Either is a preregistration amendment.

**F2 — Spending-function convention.** The frozen formula α(t) = 2[1 − Φ(z₀.₉₇₅/√t)], α = 0.05, gives four-equal-look critical values **3.92, 2.78, 2.30, 2.04**. The reference values quoted in review R3 (4.333, 2.963, 2.359, 2.014) belong to the gsDesign/Reboussin *per-tail* convention (α = 0.025 spent per side). The recursion reproduces those values when fed that convention (self-check in `test_scoring_sequential.py`), so the routine is validated; the preregistration's own formula is what is implemented. Confirm which convention is intended; both control two-sided 0.05.

**F3 — `required_pairs` precision.** With full-precision quantiles, q = 0.30 gives 2640 > N_max, contradicting the frozen illustrative 2613 → 2616 = N_max, which used 1.96 + 0.84 = 2.80. Implemented with the two-decimal convention so the frozen values are reproduced; recorded for confirmation.

**F4 — Block arithmetic.** 2616 = 10 × 240 + 216, not 9 × 240 + 456; the final partial block is 216 (a multiple of 24, stratum-balanced).

**F5 — FRAME-v0 text.** The preregistration froze the *existence* of an identical instruction block but not its wording; the wording now lives in `render.frame` under version `FRAME-v0` and should be reviewed as part of this verification, since it is prompt content.
