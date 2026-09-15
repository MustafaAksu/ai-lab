# PREREG-RS-0001 — Slice 2 (S4 runner) implementation notes

**Plan / warrant:** PLAN-20260912-0001 / WARR-20260912-0001 (scope S4)  
**Authorization:** reviewing executor, 2026-09-15, after slice-1 PASS at `afe7aab`  
**Base commit:** `afe7aab2006dbcf8d092291a7056f97d822fdd79`  
**Status:** implemented with fake-provider tests; **no provider call has been made**. Calibration (S5) requires the reviewing executor's runner verification and the operator's go.

## What was built

`ai_lab/experiments/relational_state/runner.py` — the only module importing `ai_lab.providers.*` (lazily, inside `default_provider_factory` / `resolve_profile`), so the zero-API modules never need the SDKs and tests inject a fake provider.

- `profile` — resolves model / reasoning effort / max output tokens from `ai_lab.providers.settings`, records unexposed parameters as `provider_default`, git commit and dirty state, `FRAME_SHA256`, serializer versions, `campaign_seed`, frozen operator values; refuses to overwrite. Every later stage reloads it and **aborts before any call** if `FRAME_SHA256` or `integration_effect` differ or the provider's model differs from the frozen one.
- `calibration` — Arm 1 only; 10 unique + 10 ambiguous per populated (n, d), n ∈ 3..9, d ∈ 1..6; seeded order; accuracy surface by n and by (n, d, state); deterministic triple selection (window [0.30, 0.80], nearest 0.55, smaller n) → `N_main` or `STOP`.
- `pilot` — 10 per stratum on `N_main`, both arms back-to-back per trial in SHA-256(trial_id)-parity order, seeded trial order; blinding sequence exactly as §8.2: (1) `b+c` → q, (2) `N_req`, blocks, looks, `t_k`, `z_k` written to the manifest, (3) manifest hashed, (4) only then the pilot report exposes direction. If `N_req > N_max`: STOP recorded, direction never unlocked. Direction never enters the manifest.
- `main --stage k` — one balanced block per invocation (240; final partial block), stages must run in order, each stage JSONL hashed into the manifest before the next; puzzles excluded by `puzzle_id` from the pilot and earlier stages; adjudication only when the cumulative trial count is a preregistered look, with the manifest-frozen `z_k`; POSITIVE/NEGATIVE (or the final look) writes `closure` and later stages refuse to run.
- Every provider call: `admit_instance()` first (A1–A6 + query independence; non-admitted instances are logged and skipped), one retry on exception, then a missing pair. Every row carries `integration_effect = "none"`, puzzle/trial ids, arm, serializer version, prompt SHA-256, raw response, response SHA-256, parsed output, score, provider outcome (stop reason, tokens), timestamps.

Tests (`test_runner.py`, 7): profile freeze and membrane fields; stage refusal without profile / on model mismatch; frame-drift abort before any call; arm-order parity and balance; full fake pipeline (calibration → pilot → main to closure) checking pairing, blinding order, manifest hashes, look-only adjudication, stage ordering, pilot/main quarantine, admission before every prompt; provider-error retry semantics; pilot budget STOP path.

Verification triple at this commit: full suite 916 passed; audit ok / verified_current.

## Findings for the reviewing executor

**F6 — bug fix in slice-1 generator.** `generate_stratum` could loop forever on a stratum with fewer distinct puzzles than requested (duplicates were not counted as misses). Fixed; duplicates now count as misses.

**F7 — tiny calibration stratum.** (n = 3, d = 1, ambiguous) has only 9 distinct puzzles; calibration records `requested: 10, total: 9` for that cell rather than padding or hiding it. n = 3 is far from any plausible selection window, so this does not affect selection.

**F8 — triple eligibility requires full occupancy.** Implementing v0.3.2 §4.2 (all 24 strata populated for n ≥ 6): a consecutive triple is eligible for `N_main` only if every (n, d ∈ {1..4}, state) stratum is populated, i.e. triples {6,7,8} and {7,8,9}. The calibration surface is still measured for n = 3..9. Recorded here because it narrows the §8.1 rule's candidate set; it follows from the amendment rather than adding to it.

**F9 — reasoning effort is configured by environment.** The OpenAI adapter reads `AI_LAB_OPENAI_REASONING_EFFORT`; the profile records whatever is configured when `profile` runs. The frozen operator choice for Terra was `medium`, so the operator must `export AI_LAB_OPENAI_REASONING_EFFORT=medium` (and `AI_LAB_OPENAI_MODEL=gpt-5.6-terra`) before `profile`, and the reviewing executor should check the written profile before calibration.

## Operator run-book (after runner verification; calibration only)

```bash
cd /root/AI-Lab
export AI_LAB_OPENAI_MODEL=gpt-5.6-terra AI_LAB_OPENAI_REASONING_EFFORT=medium
OUT=docs/research/experiments/relational_state/runs/campaign-01
python3 -m ai_lab.experiments.relational_state.runner profile --out $OUT --provider openai --seed 20260915
cat $OUT/campaign_execution_profile.json        # send to the reviewing executor; nothing has been called yet
python3 -m ai_lab.experiments.relational_state.runner calibration --out $OUT   # ~1180 Arm-1 calls
cat $OUT/calibration_report.json                # N_main or STOP; non-evidential
```
Pilot and main are separate operator decisions after the calibration report.
