# Verification Outcome Vocabulary

Introduced by PLAN-20260719-0001 under GAP-0004 via WARR-20260719-0001.

The self-model index and registry audits report a three-valued
`verification_outcome`:

- `verified_current`: evidence available, no drift.
- `stale`: evidence available, drift confirmed.
- `unverifiable`: required evidence unavailable; no claim about drift.

Each finding carries a `class` field: `drift` (confirmed defect),
`evidence_unavailable` (verification impossible), or `other`
(informational). The rollup is deterministic: any `drift` yields `stale`;
otherwise any `evidence_unavailable` yields `unverifiable`; otherwise
`verified_current`. The shared definitions live in
`ai_lab/documentation/verification_outcome.py`, which imports from neither
the self-model module nor any sidecar implementation.

## Severity reclassification

Findings classified `evidence_unavailable` (for example
`SELF_MODEL_INDEX_REPO_HEAD_MISSING` without a resolvable git history, or
`SELF_MODEL_INDEX_CONTENT_STALE` when git is unavailable) now carry `warn`
severity instead of `error`. This is an intentional behavior change: the
audit previously reported errors when it had merely failed to verify.

Consumers must gate on the `ok` field or on `verification_outcome`, not on
error counts by finding code. The `ok` field remains boolean and
fail-closed: `true` only when the outcome is `verified_current`, `false`
for both `stale` and `unverifiable`, never null. No findings are
suppressed in unverifiable contexts; only severity and classification
change.

When the outcome is `unverifiable`, an optional top-level
`evidence_status` explains the cause: `no_git_dir` or
`unreachable_repo_head`.

## Registry audit scope note

`audit_self_model_registry` performs no git-evidence verification; its
findings are record-integrity defects classified `drift`. It therefore
reports only `verified_current` or `stale` today. An unverifiable registry
outcome would require an evidence-dependent registry check, which does not
yet exist.
