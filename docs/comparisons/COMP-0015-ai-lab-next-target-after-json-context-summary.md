# COMP-0015: Provider Comparison — AI-Lab Next Target After JSON Context Summary

## Metadata

- comparison_id: `COMP-0015`
- title: `AI-Lab Next Target After JSON Context Summary`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0015-ai-lab-next-target-after-json-context-summary.context.json`
- created_at: `2026-07-03T10:20:03.902736+00:00`
- command: `scripts/compare_providers.py AI-Lab has completed provider latest-context policy ergonomics, dry-run context budget preview, and JSON output for --print-context-summary. Using admitted ai-lab-memory context, decide the next smallest implementation target. Evaluate whether the Manual L0 chunk creation helper should now be implemented as the next vertical slice. Compare it against citation validation and read-only L0 inclusion. Recommend one target, exact non-goals, tests, and memory-refresh notes. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Next Target After JSON Context Summary`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has completed provider latest-context policy ergonomics, dry-run context budget preview, and JSON output for --print-context-summary. Using admitted ai-lab-memory context, decide the next smallest implementation target. Evaluate whether the Manual L0 chunk creation helper should now be implemented as the next vertical slice. Compare it against citation validation and read-only L0 inclusion. Recommend one target, exact non-goals, tests, and memory-refresh notes.

## OpenAI Response

- model: `gpt-5`

```
Recommendation: Implement read-only L0 inclusion as the next smallest vertical slice. Defer the Manual L0 chunk creation helper to immediately follow, and postpone citation validation.

Why this order
- Read-only L0 inclusion plugs directly into the just-delivered dry-run and JSON summary work, exercising budgeting and manifest surfacing with minimal scope.
- It is a pure read path: no write pipeline, embeddings, or tokenizer-span coupling required.
- It creates an immediate, visible improvement in --print-context-summary by showing concrete L0 items consuming budget.
- Manual L0 creation is useful, but it doesn’t add observable value to the provider summary on its own; fixtures can supply L0 for this slice.
- Citation validation depends on having citations in prompts/answers and tokenizer-stable spans (per ABS-0003), which is premature relative to our current dry-run focus.

Comparison of candidates
- Read-only L0 inclusion
  - Scope: Load minimal L0 records and allow explicit inclusion into the manifest; show their budget impact in the JSON summary.
  - Dependencies: Minimal loader + deterministic token counting already used for budget preview.
  - Value: Immediate end-to-end visibility in the new JSON summaries.
  - Risk: Low; schema fields added are additive per v1 JSON summary.
- Manual L0 chunk creation helper
  - Scope: CLI/utility to create minimal, schema-compliant L0 chunk files/records.
  - Dependencies: Schema definition, validation, storage location; touches write path.
  - Value: Medium; accelerates dataset creation but not visible in provider summaries until inclusion exists.
  - Risk: Medium; locks in early schema ergonomics and storage layout.
- Citation validation
  - Scope: Enforce cid@version|span integrity and tokenizer-span rules (per ABS-0003).
  - Dependencies: Tokenizer pinning, manifest-to-prompt integration, answer-time or prompt-assembly citation emission.
  - Value: Low now; we don’t yet emit citations in answers.
  - Risk: Medium; early adoption without citations can cause churn.

Exact target scope: Read-only L0 inclusion
- CLI ergonomics
  - Add --include-l0 <cid> flags (repeatable) and/or --include-l0-file <path-to-jsonl> with records of {cid, maybe version}.
  - Add --l0-store <path> (directory or SQLite/JSONL) to resolve included cids.
- L0 loader
  - Minimal fields: chunk_id (cid), artifact_id, version, text or redacted_text, created_at/updated_at optional.
  - No embeddings, no dependencies, no ACL enforcement beyond preferring redacted_text when present.
- Selection/inclusion
  - Only explicit inclusions (inclusion_reason=explicit). No retrieval, no dependency expansion.
  - Deduplicate duplicate cids; stable deterministic ordering: CLI order, then cid lexical as tiebreaker.
- Budgeting
  - Compute token_cost per included chunk using existing token counting; consume from context budget; if over budget, drop overflow items with dropped_reason=over_budget.
  - Whole-chunk inclusion only; no partial span trimming.
- JSON summary extensions (schema_version v1 additive)
  - Add fields to the summary payload:
    - l0_candidates: list of resolved {cid, token_cost, inclusion_reason: "explicit"} before budgeting.
    - l0_included: subset that fit the budget with {cid, token_cost, inclusion_reason}.
    - l0_dropped: list with {cid, dropped_reason, token_cost}.
  - Keep existing latest-context policy and budget preview intact.

Non-goals for this slice
- No Manual L0 creation helper (no write/ingest).
- No retrieval (BM25/dense), reranking, or novelty fill.
- No dependency traversal.
- No citation integrity validation or tokenizer-span enforcement.
- No ACL/namespace redaction mechanics beyond preferring redacted_text if present.
- No chunk partial-span inclusion; no prompt assembly changes.

Test plan
- Unit tests
  - Loader resolves known cids from a test store; unknown cids yield warnings and exclusion.
  - Deduplication: repeated --include-l0 inputs result in one candidate/included entry.
  - Deterministic ordering: inputs in a given order produce stable l0_candidates and l0_included ordering.
  - Token counting is invoked and returned token_cost is non-negative and consistent across runs.
- Budget behavior
  - When total token_cost <= budget, all candidates appear in l0_included and none in l0_dropped.
  - When total token_cost > budget:
    - Items are admitted in order until budget is exhausted; remainder appear in l0_dropped with dropped_reason=over_budget.
    - Budget numbers in the summary reflect the consumed tokens.
- CLI/JSON integration
  - ask_provider.py and compare_providers.py with --print-context-summary --summary-format json and explicit --include-l0 produce parseable JSON containing the three new lists and unchanged existing fields.
  - Backward-compatibility: running without any --include-l0 yields empty l0_* lists and identical payload to prior release otherwise.
- Error handling and edge cases
  - Mixed presence of text vs redacted_text: loader prefers redacted_text when present.
  - Unknown cid: appears in no l0_* lists; warning text is emitted to stderr; JSON remains valid.
  - Large L0 chunk exceeding entire budget alone: results in l0_candidates with that cid, l0_included empty, l0_dropped with over_budget.
- Determinism tests
  - Round-trip JSON formatting is stable across runs given fixed inputs (extend existing deterministic JSON tests).

Memory-refresh notes (ai-lab-memory)
- New L1 entry
  - Title: L1-YYYYMMDD-readonly-l0-inclusion-dry-run
  - Completed work: Explicit L0 inclusion via CLI; dry-run manifest now surfaces l0_candidates/included/dropped; budget integration.
  - Key decisions: Explicit-only inclusion for first slice; additive v1 JSON fields; stable ordering and budget drop policy.
  - Risks: Future retrieval/dependency expansion may require schema v1 additive fields; clear backward-compatible plan.
  - Tests: Summarize new unit/CLI tests and deterministic JSON extensions; record total pytest count update.
- ABS-0003 linkage
  - Note that this implements the “rule-based/mandatory inclusions” and “budgeting” pieces in minimal form (explicit-only, no retrieval), aligning with the reconciled loop.
- Next-actions pointer
  - Queue Manual L0 chunk creation helper as the follow-up (write-only tool, schema-validated, produces files consumable by this slice).
  - Defer citation validation until prompts/answers emit citations or we introduce span-bounded inclusions.

If you prefer to do Manual L0 creation helper first, do it behind a feature flag and ship both within the same iteration; otherwise, read-only inclusion alone is the strictly smaller, independently valuable slice.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# Next Implementation Target Recommendation

## Analysis

Based on the admitted context, AI-Lab has completed the provider context ergonomics layer (L1-20260703). The reconciled memory implementation loop (ABS-0003) establishes that L0 chunks are the foundational unit with span bounds and mandatory citation format `cid@version|span`.

### Candidate Evaluation

**1. Manual L0 Chunk Creation Helper**
- **Prerequisites met**: Schema understanding from ABS-0003; no prior L0 implementation needed
- **Vertical slice**: Creates first concrete L0 instances, enabling all downstream work
- **Incremental value**: Unblocks citation validation, read-only inclusion, and write-back pipeline
- **Complexity**: Low—file-based input/output with schema validation

**2. Citation Validation**
- **Prerequisites**: Requires L0 chunks to exist for validation targets
- **Blocker**: Cannot validate `cid@version|span` format without L0 instances
- **Complexity**: Medium—requires citation parsing and chunk lookup

**3. Read-Only L0 Inclusion**
- **Prerequisites**: Requires L0 chunks to exist for retrieval
- **Blocker**: Cannot include non-existent L0 chunks in context packs
- **Complexity**: Medium—requires integration with provider context assembly

### Decision Matrix

| Target | Prerequisites Met | Unblocks Others | Complexity | Testability |
|--------|------------------|-----------------|------------|-------------|
| Manual L0 Helper | ✓ | ✓✓✓ | Low | High |
| Citation Validation | ✗ (needs L0) | ✓ | Medium | High |
| Read-Only L0 Inclusion | ✗ (needs L0) | ✓✓ | Medium | Medium |

## Recommendation: **Manual L0 Chunk Creation Helper**

### Target Scope

**Implementation:**
- CLI script `scripts/create_l0_chunk.py` that accepts:
  - Source file path
  - Chunk content (text span or auto-extract)
  - Metadata: namespace, access_level, topics, optional parent artifact
- Generate conformant L0 JSON with:
  - `chunk_id` (L0-YYYYMMDD-{slug})
  - `content_hash` (SHA-256)
  - `span_bounds` (character offsets for source files)
  - `embedding_id` and `embedding_namespace` (placeholder/manual)
  - `created_at`, `namespace`, `access_level`
  - Empty `citations` array (for bootstrap)
- Write to `docs/memory/l0/{chunk_id}.json`
- Basic schema validation against ABS-0003 L0 requirements

**Test Coverage:**
- Valid L0 JSON structure with all required fields
- Content hash determinism
- Span bounds calculation for text input
- Namespace and access level defaults
- File write location correctness
- Schema validation catches missing fields

### Exact Non-Goals

**Explicitly excluded from this vertical slice:**
- ❌ Automatic chunk segmentation or splitting strategies
- ❌ Embedding vector generation (embedding_id is placeholder)
- ❌ Citation extraction or validation
- ❌ L1 artifact or episode summary generation
- ❌ Integration with retrieval or context pack assembly
- ❌ ACL enforcement or redaction logic
- ❌ Automatic refresh triggers or staleness detection
- ❌ Dependency graph tracking
- ❌ Keyphrases, entities, claims, or risks extraction
- ❌ Versioning beyond v1 initial creation

### Memory-Refresh Notes

**For next AI-Lab session:**

1. **Context to re-admit:**
   - This recommendation (save as episode L1)
   - ABS-0003 (L0 schema reference)
   - L1-20260703 (confirms prior completion)

2. **Schema anchor points** (from ABS-0003):
   - L0 requires: `chunk_id`, `content_hash`, `span_bounds`, `embedding_id`, `embedding_namespace`, `namespace`, `access_level`, `created_at`, `citations`
   - Citation format: `cid@version|span` (span unit rules in COMP-0006/COMP-0007)
   - Embedding
```
