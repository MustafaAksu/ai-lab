# S5 calibration-02 — result, second STOP, and cell closure (2026-09-15)

**Run:** `runs/campaign-02/`, profile SHA-256 `5c504acb…df5b`, repo `52d55bf67f148fec9b3bcbee789c2f19a03232dd` (clean).
**Subject (PREREG v0.4 §3):** `gpt-5.6-luna`, `reasoning_effort = low`, Arm 1 only, non-evidential. Same `campaign_seed = 20260915` as campaign-01.
**Volume:** 588 calls, `missing_after_retry: 0`, `excluded_at_admission: []`, every row `stop_reason: completed`, every row bound to the frozen profile digest and to the clean commit above.
**Digests:** `calibration.jsonl` `f5f474e8…1832`; `calibration_report.json` `6d617bcf…eae9`; manifest (excluding self) `127f707b…0f1f`.

## Outcome

$$\boxed{\text{STOP — no eligible }N_{\rm main}\ \text{(second and final)}}$$

Arm-1 accuracy by n: 3 → 0.679, 4 → 0.920, 5 → 0.957, 6 → 0.989, 7 → 0.955, 8 → 0.983, 9 → 0.983. Eligible triples: {6,7,8} = 0.975, {7,8,9} = 0.974. The window is [0.30, 0.80]; neither qualifies. Under PREREG v0.4 §8.1 this is the declared second STOP: **the cell ends, the PLAN closes as completed-with-calibration-STOP, and GAP-0009 remains open.**

Nothing has been learned about $H_{\rm RS}$. No paired trial was ever run; Arm 2 was never sent to a provider. A ceiling before the pilot produces no controlled evidence of the Arm-1/Arm-2 effect, which is why this is not the INCONCLUSIVE closure of §7.

## Comparison with campaign-01 (both non-evidential)

| pooled | Terra / medium | Luna / low |
|---|---|---|
| {6,7,8} | 0.953 | 0.975 |
| {7,8,9} | 0.969 | 0.974 |
| all n | 0.968 | 0.956 |

Dropping a model tier *and* a reasoning-budget notch did not move the eligible triples at all; on {6,7,8} Luna/low scored slightly higher than Terra/medium. The two configurations differ only where the puzzles are trivially small: n = 3 falls from 1.000 to 0.679, driven almost entirely by one cell, (n=3, d=2, unique) = 2/10 (Terra: 10/10). n = 3 is outside every eligible triple, so this affects no decision — but it is the one place the subjects visibly differ, and it is the *smallest* puzzle, not the largest.

## Calibration findings (exploratory design findings about these subjects and this family; not evidence about $H_{\rm RS}$)

**F12 — neither $n$ nor R1-depth is a reliable difficulty coordinate here.** At the pooled, main-eligible level both subjects sit at ceiling: {6,7,8} 0.953 / 0.975 and {7,8,9} 0.969 / 0.974 (Terra/medium, Luna/low). Restricted to $n\ge4$ the two campaigns pool to 0.966 and 0.970. Individual cells do vary — Terra/medium has (n=6, d=2, unique) = 6/10 and (n=6, d=3, unique) = 8/10 — but the variation is not monotone in either coordinate: the same subject is at 0.90–1.00 for every cell at $n=8,9$ and $d=1\dots6$. So the claim is not that every cell is at ceiling; it is that neither declared difficulty knob produces a usable, monotone gradient in this range.

**F13 — the low cells are non-monotonic and subject-specific.** Across 1176 calls the cells below 0.80 are: Terra/medium (n=6, d=2, unique) = 0.60; Luna/low (n=3, d=2, unique) = 0.20. They occur at different $n$, under different subjects, and larger $n$ and larger depth return to ceiling in both campaigns. That pattern is inconsistent with a capacity limit that grows with problem size. Two hypotheses worth recording for a future design, neither tested here: the failures may be format- or instruction-shaped rather than reasoning-capacity-shaped; and if so, extending the vocabulary from $n=9$ to $n=12$ would not by itself produce a discriminating family. **Both are leads, not findings.** A future harder-family cell should first establish a difficulty variable whose gradient is demonstrable, rather than assume $n$ or cascade depth.

**F14 — ambiguity did not appear to be a bottleneck in these calibrations.** Computed over both campaigns: unique-target cells 305/320 = 0.953 (Terra/medium) and 300/320 = 0.938 (Luna/low); ambiguous-target cells 264/268 = 0.985 and 262/268 = 0.978. Ambiguous scored at least as well as unique in both, so the false-certainty endpoint (§7, Secondary 2) would have had little room to move on this family. Stated as an observation about these two Arm-1 calibrations only; no paired data exists and no general claim about ambiguity handling is made.

## Closure

- PLAN-20260912-0001: **completed-with-calibration-STOP**. Scope items S1–S5 executed; S6 (pilot) and S7 (main campaign) never authorized and never run. No provider call was made outside the two Arm-1 calibrations (1176 calls total).
- GAP-0009: **remains open**. Its evidence requirement — a controlled paired measurement of the Arm-1/Arm-2 effect — is untouched.
- The visitor boundary held throughout: `INTEGRATION_EFFECT = "none"` on every artifact, no InvocationRecords, `CAPTURE_PATHS` and `docs/invocations/` unchanged, no AI-Lab runtime behaviour modified. The package, tests, gate and both campaigns remain in the repository as the record of what was built and why it stopped.
- What a future cell would have to change first: the difficulty variable itself (F12, F13), not the subject and not `n`. That is a new GAP/PLAN, with its own preregistration.
