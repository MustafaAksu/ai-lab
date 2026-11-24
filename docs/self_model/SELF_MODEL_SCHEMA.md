# AI-Lab SELF-MODEL v1 Schema

SELF-MODEL v1 is a mechanism-honest layer for describing AI-Lab's current capabilities, open gaps, verification evidence, audits, and governed-improvement plans.

It must not claim that AI-Lab is self-aware or conscious.

## Canonical vocabulary

```text
SELF-MODEL declares.
SELF-AUDIT checks.
VERIFY evidences.
PLAN reasons.
CADM-PLAN approves.
GOVERNED IMPROVEMENT acts only after admission.
```

## Artifact families

```text
CAP-*     Capability record
GAP-*     Gap / missing-capability record
VERIFY-*  Verification evidence record
AUDIT-*   Self-audit result record
PLAN-*    Proposed governed-improvement plan
```

ID grammar:

```text
CAP-NNNN
GAP-NNNN
VERIFY-YYYYMMDD-NNNN
AUDIT-YYYYMMDD-NNNN
PLAN-YYYYMMDD-NNNN
```

All SELF-MODEL v1 artifact IDs are immutable birth stamps. Corrections are represented by new records. The date embedded in VERIFY, AUDIT, and PLAN IDs is a creation stamp only, not a live classification or freshness marker.

## CAP records

A CAP record is a falsifiable claim about an implemented, partial, experimental, planned, or deprecated capability.

CAP evidence must use full commit hashes and structured references. File evidence includes `content_hash`; this may be `null` in v1, but SELF-AUDIT warns when it is missing. When `content_hash` is present, SELF-AUDIT compares it to the current file SHA-256 and reports match or mismatch findings.

## GAP records

A GAP record describes a missing or incomplete capability. Open GAPs must not be silently treated as implemented capabilities.

## VERIFY records

VERIFY v1 records are attributed testimony about execution evidence. They include `recorded_by` so the evidence claim is attributed.

VERIFY v1 does not independently execute commands. Its records stay attributed testimony; nothing in v2 converts a v1 record into observed execution.

### VERIFY v2 (PLAN-20261124-0001, WARR-20261124-0001)

VERIFY v2 separates two objects.

- **Receipt.** The raw output of `scripts/verify_v2.py`. The writer runs a declared profile itself, in a detached git worktree of one exact commit, with an allowlisted command environment (PATH, a fresh HOME, LANG, TZ and the profile's literal variables). It records per command the termination, exit code, timeout and the stdout/stderr bytes under content addresses, and checks HEAD and `git status --porcelain=v1 --untracked-files=all --ignored` at every command boundary. The receipt is a producer's claim of observation (`observation_basis: observed_by_writer`). Its `verifier_lineage_status` is always `self_authored_unreviewed`, and `environment_capture` is `partial`: it does not supply the full effective-input coverage of ABS-0004 Section 4.7.
- **Canonical VERIFY v2 record.** A `VERIFY-YYYYMMDD-NNNN` file written only by `scripts/import_verification_v2.py`. It carries the shared VERIFY fields (`repo_commit` equals the receipt's subject commit), the receipt's SHA-256, a summary derived from the receipt, `origin.origin_verification: unverified` and import metadata kept apart from the observation time.

Result is a total function with precedence `incomplete` (the profile is empty, a command did not terminate by exiting, a command is missing, or HEAD or the tree differed at any boundary), then `one_or_more_commands_failed`, then `all_commands_exit_zero`. `incomplete` is never a success. The boundary observation does not detect a path changed and restored within one command.

Validation recomputes every derived field and never copies it: the receipt's result and output retention from its commands; completeness against the stored profile bytes (command count, order, argv templates, timeouts, declared properties); stream lengths against `capture_complete`; the command environment against the stored profile's allowlist and literal values; and on the record, the summary, `repo_commit`, `observed_at`, origin and lineage. Store paths must equal the path derived from the digest and stay inside the store root. Checks that need the store take the repository root explicitly (`validate_verification_record_in_repo`); no check resolves a path from the working directory.

Store: `docs/self_model/verification_outputs/sha256/<2 hex>/<digest>`, holding outputs, profiles, distribution lists and receipts. Each stream is retained up to 8 MiB, and a truncated stream is marked `capture_complete: false`. `scripts/check_verification_outputs.py` checks that every blob hashes to its address and that every v2 record validates against its receipt. Integrity means stored bytes equal recorded digests. It does not establish where or whether a run took place.

What v2 does not establish: independence of the writer from the code it checks (the same executor authors both); CI origin (a self-consistent receipt with a fabricated run id passes import, which is why origin stays `unverified`); that a command tests its declared property (P2); confidentiality beyond the environment-transfer property (the allowlist does not stop a command reading files, so local raw outputs are checked before import into this public repository).

CI (`.github/workflows/verify-v2.yml`): runs on pull requests and pushes to `main` with `fetch-depth: 0`, `persist-credentials: false`, contents read permission and no secrets, and uploads the receipt even after a failure. A pull_request receipt covers only its synthetic merge commit (M_PR). M_PR = M_main is not assumed. A push-to-main receipt is never pre-merge evidence. Tree equality between two commits is `content_equivalence` (tracked-content equality only), not equality of verification scope, because the audit also depends on git history. Artifacts are transport (GitHub's default retention is 90 days); only import makes a receipt durable. The workflow is not a required check: that is an operator arrangement, and GAP-0010's required-check dimension remains open.

## SELF-AUDIT v1 checks

SELF-AUDIT v1 checks:

```text
1. CAP, GAP, and VERIFY JSON records are valid.
2. CAP evidence paths exist.
3. CAP commits are full hashes and exist in git history.
4. CAP memory and admission records exist.
5. CAP last_verified points to a valid VERIFY artifact.
6. CAP last_verified commit exists.
7. stale_verification warns when the verification commit is older than the configured commit-distance threshold.
8. warrant-state check resolves the latest admission verdict for warrant evidence and warns if it is no longer admitting.
9. content_hash = null is a warning, not an error, in v1.
10. content_hash mismatch is a warning, because file change means verification may be stale, not necessarily false.
```

Severity semantics:

```text
error: a declared claim is demonstrably false or structurally invalid.
warn: a claim is stale, weakly evidenced, incomplete, unverifiable, or dependent on a v1 approximation.
info: a claim was checked successfully.
```

## Freshness limitation

Commit-distance freshness is a v1 proxy. It may warn after unrelated commits. The intended v2 semantics is path-sensitive freshness over each capability's declared mechanism/test files.




## WARRANT records

WARRANT records are evidence-backed adjudications for self-model items such as capabilities, gaps, plans, verifications, or the generated self-model index.

They are separate from context admission records. Context admission decides whether an item may enter a context pack. WARRANT records justify or approve claims and governed-improvement actions.

Required fields:

```json
{
  "schema_version": "v1",
  "warrant_id": "WARR-YYYYMMDD-NNNN",
  "target_item_id": "PLAN-20260705-0001",
  "target_item_type": "plan",
  "decision": "admit",
  "warrant_state": "supported",
  "created_at": "...",
  "author": "...",
  "substrate": "process",
  "reason": "...",
  "scope": "...",
  "evidence_ids": ["..."]
}
```

Allowed target types are `capability`, `gap`, `plan`, `verification`, and `self_model_index`.

Allowed decisions are `admit`, `admit_with_warning`, `reject`, and `defer`.

Allowed warrant states are `supported`, `disputed`, `rejected`, `superseded`, and `unreviewed`.

## PLAN records

PLAN records describe proposed governed improvements before implementation work begins.

Required fields:

```json
{
  "schema_version": "v1",
  "plan_id": "PLAN-YYYYMMDD-NNNN",
  "title": "...",
  "status": "proposed",
  "created_at": "...",
  "source_gap_id": "GAP-0001",
  "objective": "...",
  "proposed_change": "...",
  "rationale": ["..."],
  "constraints": ["..."],
  "success_criteria": ["..."],
  "risk": "...",
  "next_action": "..."
}
```

Allowed PLAN statuses are `proposed`, `admitted`, `rejected`, `completed`, and `superseded`.

PLAN records are not implementation permission by themselves. A proposed PLAN still requires admission before governed improvement work proceeds.

## SELF_MODEL.json index

`SELF_MODEL.json` is generated by `scripts/build_self_model.py` from CAP, GAP, VERIFY, and audit records.

The index is aggregation-only. It may copy, count, sort, group, filter, and link back to source records. It must not invent recommendations or infer unstated capabilities.

Every generated recommendation must point back to a source record and source field, such as `GAP-0001.recommended_first_slice`.

The generated index also includes PLAN records, `open_plans`, WARRANT records, and `admitted_plans` so proposed and admitted governed improvements are visible to the self-model.

## Generated SELF_MODEL.json rule

When introduced, `SELF_MODEL.json` must be aggregation-only. It may copy, sort, count, filter, group, and link to source records. It must not invent recommendations, infer capabilities, or synthesize risk explanations.


## SELF_MODEL.json staleness audit

A committed `SELF_MODEL.json` does not require `repo_head` to equal current `HEAD`, because the commit that stores the generated index necessarily advances `HEAD`.

Therefore index staleness is checked by:

```text
1. Whether CAP/GAP/VERIFY source records changed since the stored repo_head.
2. Whether a normalized rebuild differs from the stored index.
```

The normalized rebuild comparison ignores `generated_at` and `repo_head`, and compares the aggregation content.

This avoids noisy warnings after unrelated memory or documentation commits.

## Non-goals

SELF-MODEL v1 does not:

```text
- claim AI-Lab is self-aware;
- automatically modify code;
- automatically approve plans;
- infer capabilities from arbitrary prose;
- automatically repair stale capabilities;
- provide semantic verification that a mechanism file still implements the claimed behavior.
- treat content_hash mismatch as proof that the capability is false.
```
