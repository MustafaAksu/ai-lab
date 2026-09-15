# S5 calibration — result and STOP (2026-09-15)

**Run:** `docs/research/experiments/relational_state/runs/campaign-01/`, profile SHA-256 `0891dfe3…9cf0`, repo `4564d3407b48ce1572ce10431a8721b1128a76ed` (clean).  
**Subject:** `gpt-5.6-terra`, reasoning effort `medium`, Arm 1 only, non-evidential.  
**Volume:** 588 calls (589 expected; the finite stratum (n=3, d=1, ambiguous) yielded 8 distinct puzzles, not 9 — see below). `missing_after_retry: 0`, `excluded_at_admission: []`.

## Outcome

$$\boxed{\text{STOP — no eligible }N_{\rm main}}$$

Arm-1 accuracy by n: 3 → 1.000, 4 → 0.980, 5 → 1.000, 6 → 0.922, 7 → 0.955, 8 → 0.975, 9 → 0.975. The preregistered window is [0.30, 0.80]; every consecutive triple with all 24 main strata populated ({6,7,8} pooled 0.953; {7,8,9} pooled 0.969, 95% CI [0.950, 0.987]) is far above it. The deterministic rule therefore selects nothing and the run stops before the pilot, exactly as §8.1 provides.

This is the outcome predicted on record before any call (PREREG §2 F1; GAP-0009 note 3): the family sits at ceiling for a current frontier model. **It is a calibration outcome, not evidence about H_RS, and not a plan failure.** GAP-0009 remains open and unresolved; nothing has been learned about whether relational organization helps.

## What the surface shows beyond the STOP

- Difficulty is flat in depth: at n = 9 the model is at 0.95–1.00 for every d from 1 to 6. Depth in the R1-only sense is not what costs this subject anything.
- The only visible dip is n = 6 unique at d = 2 and d = 3 (0.60 and 0.80 in single cells of 10) — small-sample noise rather than a trend, since n = 7–9 at the same depths are at 0.90–1.00.
- Errors are spread thinly: 19 wrong answers in 588, no cell below 0.60.

So the family is not merely "a bit easy"; it is uninformative for this subject across its whole declared range. Making it harder within the frozen family is not available either: the vocabulary caps n at 9, and depth is already exhausted there.

## Finding F10 — finite-stratum realization

(n = 3, d = 1, ambiguous) realized **8** distinct puzzles, not the 9 recorded in the slice-1 notes. The earlier count came from a different base seed; the v0.3.3 wording ("exhaust the stratum, record requested and realized") covers this and the report shows `requested: 10, realized: 8`. No effect on selection — n = 3 is nowhere near the window.

## Decision (reviewing executor, 2026-09-15)

**Option 3, narrowly: one amendment to a weaker subject configuration, not a ladder.** The configuration chosen is **`gpt-5.6-luna` at `reasoning_effort = low`** — a tier change as well as a budget change, judged more likely than Terra/low to move Arm-1 off ceiling, at the cost that the claim is explicitly about Luna at low effort. The family, `FRAME-v0`, arms, SESOI, window, sample-size machinery and staged boundaries are untouched; only the subject specification and the consequence of this STOP change. The amendment is **v0.4** (not v0.3.4) because the subject's reasoning configuration is a frozen substantive parameter. `campaign_seed` stays 20260915 so the calibration puzzle sample is held approximately fixed and the medium→weaker comparison is clean; calibration remains non-evidential.

Branch: campaign-02 calibration under the amended subject → window found ⇒ pilot; STOP again ⇒ the cell ends.

**Governance correction accepted:** if campaign-02 also STOPs, the PLAN/cell closes as *completed-with-calibration-STOP* while **GAP-0009 remains open**. GAP-0009 asks for controlled evidence of the Arm-1/Arm-2 effect; a ceiling before the pilot produces none. The INCONCLUSIVE closure declared in §7 refers to a paired campaign whose interval failed to resolve the SESOI — a different thing.

## Calibration finding: the depth coordinate produced no difficulty gradient

At n = 9 the subject is at 0.95–1.00 for every d from 1 to 6; the only low cells are n = 6 unique at d = 2 and d = 3 (6/10 and 8/10), which neighbouring n at the same depths contradict. Recorded as a **calibration finding about this subject**, not an architecture conclusion. If the amended subject is also flat across depth, a future harder-family cell should reconsider the difficulty variable rather than merely extend n from 9 to 12 — a later design question, not one to settle inside this cell.

## Artifacts

`campaign-01` is committed unchanged: frozen profile, `calibration.jsonl`, `calibration_report.json`, `campaign_manifest.json` and this note. It is not debugging output; it is the provenance record explaining why the frozen primary configuration was amended. It is never overwritten or reused.
