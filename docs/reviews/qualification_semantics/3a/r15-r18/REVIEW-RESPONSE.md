# Step 3A R15–R18 correction package

[ALG] **FIXED / REVIEW_PENDING.** Response to
[review 6070899882](https://github.com/MustafaAksu/ai-lab/pull/5#pullrequestreview-6070899882)
on `877b94922fc9acf882930cd275d2889038cada33`.
Correction source: [`6ebe167d0a1465f84e789ab58619af00ef2c6c35`](https://github.com/MustafaAksu/ai-lab/commit/6ebe167d0a1465f84e789ab58619af00ef2c6c35).
Existing WARR-20261126-0001 A1–A4 applies. This package records implementation
and execution evidence; it does not issue technical acceptance or completion.

## Corrections

| Finding | Implemented behavior | Regression evidence |
| --- | --- | --- |
| R15 | Every qualification-loader Git call uses `git --no-replace-objects`. Strict object/tree/batch parsing returns typed refusal for malformed or missing responses. | Real A→B replacement cannot hide A's adverse source or admit B's pruned inventory under A's identity; separate tree/blob replacement and malformed-batch cases. |
| R16 | The exact witnessed source must have been available by witness assessment, in addition to the event/knowledge cutoff. Accepted source/witness proof references and timing remain in diagnostics. | Full evaluator tests for witness-before-capture, witness-before-availability, same-MID proof borrowing, equality/offset boundaries, retrospective bounds, permutation and nullable-reference proof retention. |
| R17 | Both CAS and `by-id` destinations are checked before either publication. Real parents must remain in the isolated store and outside the checkout; descendant symlinks are refused, including file leaves. | Full `write_assessment()` tests cover 18 redirected-path combinations; rejected calls leave all observed destinations unchanged. Valid replay, atomic publication and collision controls remain. |
| R18 | Explicit `QualificationBootstrapError` contract, constructed without schema access. Both public evaluators bootstrap before Query handling; bootstrap failure yields no AssessmentResult. | Missing/changed schema in both entry points; malformed Query precedence, decoding/metaschema errors, load-once behavior, legacy blocking and ordinary invalid-input control. |

[ALG] R16 enforces, for the same accepted capture–snapshot–payload–MID chain:

\[
t_{capture}\le t_{source\ available}\le t_{assessed}
\le t_{witness\ available}\le t_{bound}.
\]

[ALG] R18 adopts the review's explicit bootstrap-exception alternative.
`QUALIFICATION_SCHEMA_UNAVAILABLE`, `QUALIFICATION_SCHEMA_DIGEST_MISMATCH` and
`QUALIFICATION_SCHEMA_INVALID` are exception codes, not additions to frozen r2
Reason or historical v1 RES vocabularies. The detailed behavior and cache
boundary are in [CONTRACT-DELTA.md](CONTRACT-DELTA.md).

## Retained exact-subject executions

[NUM] All three receipts and their outputs were imported separately through
the existing v2 importer. [VALIDATION.json](VALIDATION.json) records full commit,
tree, record/receipt/output digests, timestamps and command-boundary observations.

| Canonical VERIFY | Subject | Python | Stored pytest result |
| --- | --- | --- | --- |
| [20261126-0003](../../../../self_model/verifications/VERIFY-20261126-0003.json) | `6ebe167d` — first local run | 3.12.14 | **2 failed, 1696 passed, 92.72 s** |
| [20261126-0004](../../../../self_model/verifications/VERIFY-20261126-0004.json) | `6ebe167d` — one sequential repeat | 3.12.14 | **1698 passed, 85.39 s** |
| [20261126-0005](../../../../self_model/verifications/VERIFY-20261126-0005.json) | `c721c65e` — CI synthetic merge | 3.12.16 | **1698 passed, 76.51 s** |

[NUM] Both failures in 0003 were in unchanged `test_falsify_verify_v2.py`
infrastructure tests. `shutil.copytree` raised `shutil.Error` when a temporary
`.git/objects/maintenance.lock` disappeared during copying. The full failure
output remains in CAS. No source/harness change or failure reclassification was
used: one repeat of the same commit/profile ran after the parallel mutation
run completed. This package does not claim to eliminate that historical
filesystem-copy race.

[NUM] [Source CI 45795395979](https://github.com/MustafaAksu/ai-lab/actions/runs/45795395979):
writer, upload and job **SUCCESS**. Artifact `15103779338` was downloaded and its
archive SHA-256 checked. The actual CI subject is `c721c65ec5e5a14ce285c0d5ef6274ba066771a0`,
not the PR head. Both subjects have tree
`8831c3043fc329362b2e71981ef0d11a740f398f`.
This establishes content equivalence, not equal verification scope.

## Falsification and regression scope

[NUM] [FALSIFICATION.json](FALSIFICATION.json): **28/28** valid baseline–mutant
pairs, **0** infrastructure/selection errors. The unchanged historical 20-guard
manifest contributes 20/20; eight R15–R18 guards contribute 8/8. Totals:
53 passing baseline test executions, 51 distinct selected node IDs, and
49 ordinary mutant assertion failures. Every caught mutation had a passing
baseline and an intended call-phase assertion failure. The retained 112 output
streams were checked for byte length and SHA-256.

[NUM] The captured source was clean at `6ebe167d`. All **1433/1433** recorded
file hashes and modes match that raw Git subject, with replacement objects
disabled; no source paths are missing or extra. The report digest is
`ae10fa98d44207dbe7dd68bbeadc27d1108890f2a606968b80095ab057dd2af0`.
These 28 guards are a selected subset, not completion of all 48 planned
scenario families or the separate historical 39 VERIFY v2 mutations.

[NUM] **61 new pytest cases**: R15/R17 = 35, R16 = 11, R18 = 15.
Development before/after logs are retained as working-tree observations,
separate from the three canonical executions:

| Cases | Before correction | After correction |
| --- | --- | --- |
| [R15/R17](R15-R17-BEFORE.txt) | 28 failed, 7 passed | [74 passed](R15-R17-AFTER.txt): 35 new + 39 existing cases |
| [Initial R16 cases](R16-BEFORE.txt) | 6 failed, 4 passed | [11 passed](R16-AFTER.txt), including the subsequently added proof-retention case |
| [R16 nullable proof reference](R16-NULL-PROOF-BEFORE.txt) | 1 failed, 10 deselected | Included in the final 11-case result above |
| [R18](R18-BEFORE.txt) | 11 failed, 4 passed | [15 passed](R18-AFTER.txt) |

## Integrity and current standing

[NUM] **217/217** historical files at reviewed head `877b9492` remain byte-identical:
49 VERIFY, 47 CAS, 65 warrants, 17 decisions, 10 GAP files and 29 qualification
preparation/review files. The old implementation report, mutation report and
VERIFY-0001/0002 keep their original subjects and coverage.

[NUM] Added **3 VERIFY + 12 CAS objects / 41,282 bytes**. Repository totals:
52 canonical VERIFY records, including 13 v2; 59 CAS objects / 145,983 bytes.
All canonical validators and CAS digest checks pass. The frozen r2 schema,
historical mutation manifest, strict classifier and VERIFY writer are unchanged.

[ALG] PLAN keeps its initial `implementation_evidence_3a` and appends
`implementation_review_corrections_3a`; `next_action` requests review of this
package. SELF_MODEL is regenerated from these records. No warrant, decision,
GAP or capability standing is changed.

[OPEN] R17 assumes a stable filesystem namespace during validation/publication;
it does not provide a sandbox against a hostile concurrent path-renaming OS
actor. R18 uses a successfully pinned in-memory schema for the process lifetime;
a new process/cleared cache must bootstrap again.

[OPEN] PR #5 remains draft/open; 3A completion and merge await review and a
separate authorized decision. PLAN remains admitted for 3A only; **3B/3C
NOT_ADMITTED**. Production qualification is closed, all C3/C10/Q_C3_C10 results
remain unresolved, and `blocks_adjudication=True`. Origin remains `unverified`,
lineage `self_authored_unreviewed`; writer–PI separation and independent
adjudication are not established. Autonomy is not activated.
