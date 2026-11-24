# VERIFY v2: R9-R12 implementation-review remediation

## Scope and actors

- Review base: `68f6f103b1e3cae37c8fb15b7214d10d941aa5a3`, PR #1.
- Authority: existing `PLAN-20261124-0001` / `WARR-20261124-0001`; these are corrections within S1-S9, not a new plan admission.
- Implementing/packaging executor: ChatGPT, taking the work assigned to Claude during Claude's temporary absence, as instructed by the operator. Three delegated helper invocations supported validator, writer and harness implementation. They are not treated as independent adjudicators.
- GitHub operations use the operator's `MustafaAksu` account. That account identity does not establish PI/implementer separation. Implementation review and operator admission remain separate from these changes.
- This is a remediation/evidence report, not an acceptance decision. No merge, plan closure, GAP closure, capability promotion, ruleset or required-check change is made.

## Reproduced counterexamples

The original validator was read from the review-base Git object, with blob id
`bd147bc5022dedd166d205cbc55474b57c1ad0a5` and SHA-256
`7e9bf79d248c76dcaa204b1ecbaff30e7365af6c58f738cd8389cf87e069f4fc`.

`verify_v2_review_probe.py` constructs temporary synthetic receipts, rehashes the
stored profile/receipt, derives matching canonical summaries, and calls the real
`validate_against_store`. No probe record is imported. The before/after JSON files
retain the validator digest and observed outcomes.

| Fixture | Original validator | Corrected validator |
| --- | --- | --- |
| Complete valid control | Accepted | Accepted |
| R9: required S1/S2 fields removed | Accepted as success | Rejected |
| R10: resolved argv/cwd contradict template | Accepted as success | Rejected |
| R11: secret-like literal profile variable | Accepted as success | Rejected |
| R11: negative profile timeout | Accepted as success | Rejected |
| Negative control: inconsistent result | Rejected | Rejected |

The corrected validator's exact digest is in `review_probe_after.json`. Reproduce
the current side with:

```bash
python docs/reviews/verify_v2/verify_v2_review_probe.py \
  ai_lab/documentation/verification_v2.py --repo .
```

For the historical side, extract the original module with `git show` into a
temporary file and supply that file as the first argument. The fixture source is
pinned to the review base independently of the tested validator.

## Changes

| Request | Correction and evidence |
| --- | --- |
| R9 | Required nested receipt and canonical fields, scalar types, explicit null rules, complete hashes, timezone-aware ordered timestamps, runner/PR fields and field relationships are checked. Contract tests delete each required field and exercise invalid values. |
| R10 | Python comes from `verifier.interpreter.path`; scratch is reconstructed from required `<run>/home` as sibling `<run>/scratch`. Complete resolved argv and `cwd="."` are compared to the stored profile. Receipt schema `/1` and historical bytes remain unchanged. |
| R11 | Stored-profile validation applies the standalone writer's supported domain. Agreement tests cover valid and invalid profiles, including fully rehashed secret-variable and negative-timeout fixtures. The writer still imports no AI-Lab module. |
| R12 | Each selected baseline must pass; exact nodeids and complete setup/call/teardown observations must match after mutation; only an ordinary call assertion/pytest-fail with exit 1 counts as caught. Collection, usage, internal, dependency, setup/teardown, unexpected exception and timeout errors do not count. |
| Reviewer section 6 | Receipts and schema state Git-status-reported paths only, not byte-level worktree equality. A test demonstrates the `assume-unchanged` limitation. |
| Reviewer section 7 | Atomic exclusive publication for receipts and CAS blobs; separate bounded, sanitized, nonimportable failure diagnostic; success/failure/refusal/incomplete exit semantics remain explicit. |

## Falsification evidence

The first run of the stricter harness reported **36 caught, 3 errors**. Two F15
tests raised `KeyError` when a required workflow key was absent; F16 propagated
the domain-specific `ImportRefusal` from the wrong-store-root mutant. None was
counted as caught. The complete first report is retained.

The F15 tests now assert the required values using `.get`, and F16 explicitly
fails its valid-import expectation on the importer/registry's named refusal
exceptions. The harness's error classification was not weakened.

The repeated complete run reported **39/39 caught, 0 errors**:

- Historical registry: **33/33**.
- Review additions: **6/6** (required nullable field; bool/index distinction;
  resolved argv; cwd; stored-profile policy; publication before fsync).

`falsification_initial.json.gz` and `falsification_final.json.gz` retain full
lossless baseline/mutant stdout/stderr, source-file hashes, selectors, exact
nodeids and phase/failure reports. `falsification_summary.json` contains outcomes,
failed nodeids and archive/uncompressed SHA-256 values. Reports describe the
captured working-tree snapshots, not a subsequently created commit. A minimal
environment was used so the deliberate parent-environment mutant could not
capture unrelated session credentials.

```bash
python -I scripts/falsify_verify_v2.py . --report /tmp/verify-v2-falsification.json
```

## Validation and historical standing

- Python 3.12.14; the repository's pinned requirements; full suite after the test
  refinements: **1398 passed in 62.96s**.
- Additional contract tests: 283; writer review tests: 74; harness tests: 37.
- CAS checker: `ok=true`, `problems=0`.
- Self-model audit: `ok=true`, `verification_outcome=verified_current`.
- All **58 pre-existing verification/CAS files** at the review base were compared
  byte-for-byte and unchanged (39 v1 records, 3 v2 records, 16 CAS files).
- Compatibility tests pin the three historical v2 canonical-file and receipt
  digests and validate their original pass/pass/deliberate-failure outcomes.

The above suite/mutation observations are packaging-executor evidence. New
commit-scoped local/CI receipts are recorded separately after the corrected
implementation is committed. Historical VERIFY-20261124-0001/0002/0003 retain
their original subject commits and lineage; they are not evidence for this
implementation. All new canonical receipts keep `origin_verification=unverified`
and `verifier_lineage_status=self_authored_unreviewed`.

## Limits

Internal consistency, stored-byte integrity, selected test success and the
listed mutations do not establish CI-origin authenticity, independent verifier
lineage, general correctness or epistemic admission. A PR receipt covers its
synthetic merge commit only. The eventual merged-main commit does not yet exist;
no equality of verification scope with it is claimed.
