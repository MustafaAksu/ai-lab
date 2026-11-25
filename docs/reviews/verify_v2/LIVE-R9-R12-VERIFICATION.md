# VERIFY v2: fresh evidence after R9-R12

## Scope

Implementation commit: [`613afe553618266e5bb1ac0c88043f7e45e44bb3`](https://github.com/MustafaAksu/ai-lab/commit/613afe553618266e5bb1ac0c88043f7e45e44bb3).
Its tree is `5f690f0512abef974fddd0192ac5a31743a6aa5a`.

These observations supplement [the remediation report](REVIEW-R9-R12-REMEDIATION.md)
under the existing PLAN-20261124-0001 / WARR-20261124-0001. ChatGPT performed the
implementation and packaging work assigned to Claude during Claude's absence.
They do not constitute an implementation-review acceptance or admission decision.

## Imported receipts

All three runs used VPROF-0001 and the corrected standalone writer. The corrected
validator accepted each receipt against its retained CAS before import.

| Canonical record | Exact subject | Python | Retained pytest result | Receipt result |
| --- | --- | --- | --- | --- |
| [VERIFY-20261124-0004](../../self_model/verifications/VERIFY-20261124-0004.json) | `613afe553618266e5bb1ac0c88043f7e45e44bb3` | 3.12.14 | 1398 passed in 62.73s | `all_commands_exit_zero` |
| [VERIFY-20261124-0005](../../self_model/verifications/VERIFY-20261124-0005.json) | `da523c45f42efdca7605ff70b9b36e18e80379f4` | 3.12.16 | 1398 passed in 54.15s | `all_commands_exit_zero` |
| [VERIFY-20261124-0006](../../self_model/verifications/VERIFY-20261124-0006.json) | `2ea18fda8b62a115c31300fbc4676cdf38da8840` | 3.12.16 | 1 failed, 1398 passed in 53.02s | `one_or_more_commands_failed` |

Receipt SHA-256 values, in the same order:

```text
f13f323e989ae4acadb56547814b75b1f8b6bc52fd30e71e79e7c38906517ae2
7394cc90838a2aa26dfb10e62e8b07e5f5ea040ef229ed5716c681eb23ecc6cd
d1782cc64dca4045f9032a31ce2159ddae865dd48f57fd006ae2bb492e875dfd
```

The local run covers the implementation commit. The two CI receipts cover their
own synthetic merge commits, with PR head/base metadata retained. The successful
PR #1 merge tree equals the implementation tree; that is content equality, not
an expansion of the receipt's commit scope. The failing PR #3 tree adds exactly
one deliberately failing test.

For every run, the pre-run and three post-command observations report HEAD equal
to the recorded subject and no paths reported as changed by Git status. This is
not byte-level worktree immutability: assume-unchanged/skip-worktree paths and
changes reverted within a command remain outside this observation.

Output retention is complete in all three receipts. Every canonical record has
`recorded_by.peer_id=chatgpt`, `role=packaging_executor`,
`origin_verification=unverified`, and
`verifier_lineage_status=self_authored_unreviewed`.

## Live CI success and failure observations

| Run | PR | Writer step | Artifact upload | Job |
| --- | --- | --- | --- | --- |
| [45434431208](https://github.com/MustafaAksu/ai-lab/actions/runs/45434431208) | #1 | success | success | success |
| [45434593937](https://github.com/MustafaAksu/ai-lab/actions/runs/45434593937) | #3 | failure | success | failure |

The GitHub job/step observations and artifact metadata are retained in
[`live_ci_observations.json`](live_ci_observations.json). Each downloaded ZIP's
SHA-256 was compared to the digest reported by GitHub before extraction. The
retained CAS supplies the receipt and command-output bytes after artifact expiry.
These API observations do not promote the receipt's origin-verification field.

The negative fixture was a draft
[PR #3](https://github.com/MustafaAksu/ai-lab/pull/3), based on the corrected
implementation branch. Its sole change was
`tests/test_verify_v2_review_deliberate_failure.py`, an explicit failing assertion.
The expected failure was visible in retained pytest stdout. PR #3 was closed
without merging after the run; its test is absent from PR #1.

## Historical preservation and remaining review

VERIFY-20261124-0001/0002/0003 retain their exact bytes, original subject commits
and lineage. All 39 v1 records and the original 16 CAS files also remain unchanged.
They are historical evidence, not evidence for the corrected implementation.
The three new canonical records and their CAS objects are additive; SELF_MODEL.json
is rebuilt to index them.

After import, the full integration suite passed again: **1398 passed in 61.59s**
on Python 3.12.14. The CAS checker reported `ok=true`, `problems=0`; the self-model
audit reported `ok=true`, `verification_outcome=verified_current`, with a matching
normalized rebuild. This working-tree check is separate from the three receipts
and does not change their recorded subjects.

The code, profiles, workflow and tests are unchanged by this evidence addition.
The complete 39-mutation run and all four reproduced counterexamples are retained
with the implementation, as described in the remediation report. The initial
strict mutation run's three errors remain recorded alongside the corrected
39/39 result; an environment or test-infrastructure error is not counted as a
caught mutation.

PR #1 remains open for renewed implementation review. Main remains at
`5c6404284e074055c1a4dad7d348ed8df2f83262`; no main-commit verification, plan closure,
GAP closure or independent verifier lineage is asserted.
