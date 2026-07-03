# SYNCOMP-0011: Comparison Synthesis — AI-Lab Next Target After JSON Context Summary OpenAI Cross Check

## Metadata

- synthesis_id: `SYNCOMP-0011`
- title: `AI-Lab Next Target After JSON Context Summary OpenAI Cross Check`
- created_at: `2026-07-03T10:29:21.100374+00:00`
- command: `scripts/synthesize_comparison.py docs/comparisons/COMP-0015-ai-lab-next-target-after-json-context-summary.md --provider openai --title AI-Lab Next Target After JSON Context Summary OpenAI Cross Check --save docs/comparisons/syntheses/SYNCOMP-0011-ai-lab-next-target-after-json-context-summary-openai-cross-check.md`
- source_comparison: `docs/comparisons/COMP-0015-ai-lab-next-target-after-json-context-summary.md`
- synthesizer_provider: `OpenAI`
- synthesizer_model: `gpt-5`

## Synthesis

~~~text
1) Shared agreement
- Both providers consider three candidates: Manual L0 chunk creation helper, read-only L0 inclusion, and citation validation.
- Both view citation validation as downstream and not the immediate next step; it depends on having L0/citation structure available.
- Both reference ABS-0003 constraints (cid@version|span, tokenizer/span stability) as relevant to future citation work.
- Both propose tight, minimal vertical slices with explicit non-goals and strong test coverage.
- Both accept that read-only L0 inclusion is a legitimate target; disagreement is about ordering, not value.

2) Meaningful differences
- Next target choice:
  - OpenAI: Read-only L0 inclusion first (smallest, pure read path, immediate visibility in JSON summaries).
  - Claude: Manual L0 creation helper first (foundational, unblocks inclusion and validation).
- Assumptions about prerequisites:
  - OpenAI assumes fixtures can supply L0 so inclusion can ship now without a write path.
  - Claude treats absence of L0 as a blocker for inclusion/validation and prioritizes creating L0.
- Scope of “minimal” L0:
  - OpenAI’s loader expects minimal fields (cid, artifact_id, version, text/redacted_text).
  - Claude’s creator emits richer ABS-0003-aligned fields (span_bounds, content_hash, namespace/access, embedding_id placeholders, citations array).
- Immediate value surfaced:
  - OpenAI ties value to --print-context-summary JSON (l0_candidates/included/dropped with budget impact).
  - Claude focuses on establishing durable L0 data assets to enable subsequent features.

3) Stronger points from OpenAI
- Clear argument that read-only inclusion directly exercises and showcases the newly built dry-run and JSON summary work.
- Smaller-scope, pure read path with no write pipeline, embeddings, or tokenizer-span coupling.
- Detailed, additive JSON summary plan (l0_candidates, l0_included, l0_dropped) and deterministic inclusion/budget-drop policy.
- Well-specified CLI ergonomics, ordering, deduplication, budgeting behavior, and backward compatibility.
- Thoughtful risk posture: avoid locking in early L0 schema/layout by deferring write tools.

4) Stronger points from Claude
- Explicit dependency framing: inclusion and validation are blocked without L0 instances; the helper unblocks both.
- Emphasis on ABS-0003 compliance for L0 records (span bounds, citation format), aligning data early with future needs.
- Concrete deliverable for a file-based L0 JSON creator with schema validation and deterministic content hashing.
- Clear non-goals to keep complexity low and avoid premature retrieval/embedding/ACL work.
- Simple decision matrix highlighting unblocking power vs complexity.

5) Combined answer
- Recommended next smallest target: Read-only L0 inclusion.
  - Rationale: It is strictly smaller than adding a write path, immediately visible in the existing --print-context-summary JSON, and leverages the just-delivered dry-run and budgeting features. Per OpenAI, fixtures can supply minimal L0 to unblock this slice; per Claude, a richer L0 helper can follow to scale data creation and align to ABS-0003.
- Exact scope
  - CLI:
    - --include-l0 <cid> (repeatable) and/or --include-l0-file <jsonl> containing {cid, maybe version}
    - --l0-store <path> to resolve included cids from a simple store (directory/SQLite/JSONL)
  - L0 loader:
    - Minimal fields: chunk_id (cid), artifact_id, version, text or redacted_text; created_at/updated_at optional
    - Prefer redacted_text when present; no embeddings; no ACL enforcement
  - Selection/inclusion:
    - Explicit inclusions only (inclusion_reason=explicit)
    - Deduplicate by cid; stable deterministic ordering (CLI order, then cid lexical)
  - Budgeting:
    - Compute token_cost per chunk with existing counter; admit in order until budget exhausted
    - Overflow goes to l0_dropped with dropped_reason=over_budget; no partial spans
  - JSON summary (additive to v1):
    - l0_candidates: [{cid, token_cost, inclusion_reason:"explicit"}]
    - l0_included: subset that fit budget
    - l0_dropped: [{cid, token_cost, dropped_reason}]
- Exact non-goals
  - No Manual L0 creation helper or any write/ingest
  - No retrieval/reranking/novelty or dependency traversal
  - No citation integrity validation or tokenizer-span rules
  - No embeddings, ACL mechanisms, or partial-span inclusion
  - No prompt assembly changes
- Tests
  - Loader/unit:
    - Resolve known cids; unknown cids warn and are excluded
    - Deduplication correctness and deterministic ordering
    - Token counting invoked; non-negative, stable costs
  - Budget behavior:
    - All fit under budget vs over-budget drop behavior and accurate consumption reporting
    - Single oversized chunk yields candidates listed, none included, dropped marked over_budget
  - CLI/JSON integration:
    - JSON output contains new l0_* lists and remains backward compatible when unused
    - Deterministic JSON across runs given fixed inputs
- Memory-refresh notes (ai-lab-memory)
  - New L1 entry:
    - Title: L1-YYYYMMDD-readonly-l0-inclusion-dry-run
    - Completed: explicit L0 inclusion via CLI; dry-run manifest surfaces l0_candidates/included/dropped; integrated budgeting
    - Decisions: explicit-only inclusion, additive JSON fields, stable ordering and drop policy
    - Risks: future retrieval/dependency expansion may require evolving schema; plan for backward-compatible additions
    - Tests: summarize unit/CLI/determinism additions and updated pytest counts
  - ABS-0003 linkage:
    - Implements rule-based/mandatory inclusions and budgeting in minimal form (explicit-only)
  - Next actions:
    - Follow-up: Manual L0 chunk creation helper (write-only tool producing files consumable by this slice)
    - Defer citation validation until citations/spans are present in prompts/answers

6) Risks or missing assumptions
- Existence of L0 data:
  - OpenAI’s plan presumes minimal L0 fixtures or a seed store; Claude assumes none exist and prioritizes their creation. If no L0 are available and no fixtures are acceptable, inclusion may lack demo value until the helper lands.
- Schema depth:
  - OpenAI’s minimal loader fields vs Claude’s ABS-0003-richer L0 record differ; locking in either too early may cause churn. Keeping the read path tolerant to extra fields mitigates this.
- Citation span/tokenizer pinning:
  - Both imply future coupling to tokenizer-stable spans; deferring validation is prudent but leaves a future integration risk.
- ACL/redaction and privacy:
  - Both defer enforcement; inclusion could unintentionally surface unredacted text if stores are misconfigured; preferring redacted_text helps but is not full ACL.
- Ordering/fairness:
  - Strict CLI order admission could bias inclusion; acceptable for explicit-only MVP but should be revisited with retrieval.

7) Suggested re-ask prompt
- “Confirming next slice selection: Do we currently have acceptable L0 fixtures or a seed L0 store to drive read-only inclusion visibility in --print-context-summary? If yes, proceed with the read-only L0 inclusion slice as specified (CLI flags, loader fields, budgeting, and JSON l0_* lists). If no, should we first implement a minimal Manual L0 creation helper that emits the smallest schema necessary for inclusion (cid, artifact_id, version, text/redacted_text), deferring span_bounds/embedding placeholders to a later iteration? Please confirm field expectations for L0 records, desired CLI flag names, and whether the proposed JSON summary extensions (l0_candidates/included/dropped) fit the current schema versioning plan.”
~~~

## Source Comparison

~~~markdown
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

~~~
