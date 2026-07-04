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

CAP evidence must use full commit hashes and structured references. File evidence includes `content_hash`; this may be `null` in v1, but SELF-AUDIT warns when it is missing.

## GAP records

A GAP record describes a missing or incomplete capability. Open GAPs must not be silently treated as implemented capabilities.

## VERIFY records

VERIFY v1 records are attributed testimony about execution evidence. They include `recorded_by` so the evidence claim is attributed.

VERIFY v1 does not independently execute commands. A future v2 writer should run commands, capture exit code/output, bind results to repo HEAD, and write the VERIFY record automatically.

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
```

Severity semantics:

```text
error: a declared claim is demonstrably false or structurally invalid.
warn: a claim is stale, weakly evidenced, incomplete, unverifiable, or dependent on a v1 approximation.
info: a claim was checked successfully.
```

## Freshness limitation

Commit-distance freshness is a v1 proxy. It may warn after unrelated commits. The intended v2 semantics is path-sensitive freshness over each capability's declared mechanism/test files.

## Generated SELF_MODEL.json rule

When introduced, `SELF_MODEL.json` must be aggregation-only. It may copy, sort, count, filter, group, and link to source records. It must not invent recommendations, infer capabilities, or synthesize risk explanations.

## Non-goals

SELF-MODEL v1 does not:

```text
- claim AI-Lab is self-aware;
- automatically modify code;
- automatically approve plans;
- infer capabilities from arbitrary prose;
- automatically repair stale capabilities;
- provide semantic verification that a mechanism file still implements the claimed behavior.
```
