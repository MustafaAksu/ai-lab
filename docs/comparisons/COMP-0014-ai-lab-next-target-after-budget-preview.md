# COMP-0014: Provider Comparison — AI-Lab Next Target After Budget Preview

## Metadata

- comparison_id: `COMP-0014`
- title: `AI-Lab Next Target After Budget Preview`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0014-ai-lab-next-target-after-budget-preview.context.json`
- created_at: `2026-07-03T10:04:01.490363+00:00`
- command: `scripts/compare_providers.py AI-Lab has closed the provider latest-context context-policy ergonomics chain and the dry-run Context Budget Preview implementation. Using admitted ai-lab-memory context, recommend the next smallest implementation target. Compare at least these candidates: JSON output for --print-context-summary, citation validation utility, manual L0 chunk creation helper, and read-only L0 inclusion in context packs. Choose one small vertical slice that is testable, low-risk, and suitable for one implementation commit plus memory refresh. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Next Target After Budget Preview`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has closed the provider latest-context context-policy ergonomics chain and the dry-run Context Budget Preview implementation. Using admitted ai-lab-memory context, recommend the next smallest implementation target. Compare at least these candidates: JSON output for --print-context-summary, citation validation utility, manual L0 chunk creation helper, and read-only L0 inclusion in context packs. Choose one small vertical slice that is testable, low-risk, and suitable for one implementation commit plus memory refresh.

## OpenAI Response

- model: `gpt-5`

```
Recommendation: Implement JSON output for --print-context-summary

Why this slice
- Smallest change surface: purely formatting of an already-computed dry-run preview; no runtime/provider behavior changes.
- Deterministic and testable: the existing preview has stable numbers and ABS-0003 percentages (15/10/75 with 40/45/10/5 context split), making golden-file tests straightforward.
- Low risk: gated behind an explicit flag; default text output remains unchanged to avoid breaking existing scripts.
- Immediate utility: enables machine-readable capture in CI, comparisons, and telemetry without waiting on L0 storage or citation enforcement.

Comparison of candidates
- JSON output for --print-context-summary
  - Pros: trivial to integrate with existing helpers; deterministic; no tokenizer or storage dependencies; enables downstream tooling quickly.
  - Cons: none material; just needs schema/versioning discipline.
- Citation validation utility
  - Pros: aligns with ABS-0003 mandatory cid@version|span.
  - Cons: requires tokenizer/version management and access to span-ground truth for meaningful validation; risks future rework if citation schema changes; higher complexity for a single-commit target.
- Manual L0 chunk creation helper
  - Pros: moves L0 forward.
  - Cons: forces early schema and storage decisions (IDs, spans, embedding metadata); likely spills into docs and validations; not a single-commit change without stubbing many parts.
- Read-only L0 inclusion in context packs
  - Pros: proves end-to-end selection pipeline with L0 presence.
  - Cons: touches selection/packing paths and budgeting behavior; needs at least a minimal L0 store and ACL/redaction handling; higher regression risk.

Proposed scope (one-commit vertical slice)
- CLI
  - Add a summary format flag without changing defaults:
    - --summary-format json|text (default: text), applies only when --print-context-summary is set.
    - Keep existing behavior for --print-prompt. If both are set, print the summary first, then the prompt, separated by a blank line.
- Helper
  - Add format_provider_context_budget_preview_json(...) alongside existing text formatter, reusing the same preview data structure.
  - Ensure deterministic key ordering and consistent numeric formatting.
- JSON schema (minimal, versioned)
  - schema_version: string (e.g., "v1")
  - provider: string
  - model: string
  - context_window_tokens: int
  - budget_policy:
    - system_pct, answer_pct, context_pct: numbers
    - context_split: explicit_pct, dependencies_pct, l1_pct, l0_pct: numbers
  - token_counts:
    - total_context_tokens_available: int
    - allocated:
      - explicit_tokens, dependencies_tokens, l1_tokens, l0_tokens: ints
    - preview_notes: array of strings (e.g., warnings about rounding)
  - inclusions: array of objects (ordered as packed)
    - id: string (e.g., manifest or chunk reference)
    - kind: enum ("explicit" | "dependency" | "l1" | "l0")
    - source: string (namespace or artifact ref if available)
    - tokens_estimated: int
    - inclusion_reason: string
    - priority: number or null (if available)
  - warnings: array of strings (e.g., over-budget trimming, if simulated)
- Integration points
  - scripts/ask_provider.py: honor --summary-format when --print-context-summary is used.
  - scripts/compare_providers.py: same behavior, enabling side-by-side JSON capture in CI.
- Backward compatibility
  - Default remains text; no change to existing output unless --summary-format json is provided.

Acceptance criteria
- Running ask_provider.py with --print-context-summary --summary-format json produces a single valid JSON object on stdout, followed by the prompt if --print-prompt is also set.
- Numbers and percentages match the current text preview for the same --context-window.
- Key order and numeric precision are deterministic across runs.
- compare_providers.py supports the same flag with consistent output per provider/model.
- No change to outputs when --summary-format is omitted (text remains the default).

Test plan
- Unit tests
  - Snapshot test for format_provider_context_budget_preview_json with a fixed preview fixture.
  - Percent and token allocation consistency with the text formatter.
  - Invalid --context-window still errors out as today; JSON not emitted when validation fails.
- CLI tests
  - ask_provider.py emits valid JSON (validate parse) and, if combined with --print-prompt, prints prompt after a blank line.
  - compare_providers.py emits valid JSON per provider; outputs can be parsed and compared in tests.
- Determinism
  - Ensure stable ordering of inclusions and keys; test compares exact JSON strings.

Risks and mitigations
- Risk: Consumers might assume JSON becomes the default.
  - Mitigation: Keep default as text; require explicit --summary-format json; document clearly.
- Risk: Schema drift.
  - Mitigation: Include schema_version and keep the initial schema minimal; treat additions as non-breaking by only adding optional fields.

Rollout
- One implementation commit:
  - New flag + JSON formatter + tests + docs.
- Memory refresh:
  - Add an L1 entry summarizing the feature, tests, and no-runtime-impact note, referencing ABS-0003 budgeting defaults.
  - Update CLI help and a short doc snippet for machine-readable summaries.

Why this is the right “next smallest” slice
- It leverages the just-finished dry-run preview work (L1-20260703) and ABS-0003 budget defaults.
- It’s orthogonal to runtime selection/packing, L0 storage, and tokenizer subtleties.
- It unlocks downstream validation/comparison tooling and prepares for future features (e.g., adding citation and L0 details later) without committing to heavier architectural choices now.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Recommendation: Manual L0 Chunk Creation Helper

## Analysis of Candidates

### 1. JSON output for --print-context-summary
**Scope:** Add `--format json` flag to provider scripts' context summary output.

**Pros:**
- Natural extension of just-completed dry-run work
- Low complexity (output formatting only)
- Testable with deterministic JSON assertions

**Cons:**
- Purely ergonomic; no new capability
- Requires schema design (context budget, admission verdicts, item list)
- Value limited until downstream tooling consumes it

**Risk:** Low | **Testability:** High | **Vertical slice:** Incomplete (no consumer)

---

### 2. Citation validation utility
**Scope:** Standalone validator for `cid@version|span` format per ABS-0003.

**Pros:**
- Core memory primitive from reconciled design
- Reusable across future L0/L1 write-back
- Clear pass/fail unit tests

**Cons:**
- Requires L0 chunk infrastructure to validate *against*
- ABS-0003 specifies token/character/line span units—needs tokenizer coupling decision
- No existing citations to validate (chicken-and-egg)

**Risk:** Medium (premature without L0 data) | **Testability:** High | **Vertical slice:** Incomplete (no L0 substrate)

---

### 3. Manual L0 chunk creation helper ⭐
**Scope:** CLI tool to generate chunk-level L0 JSON from artifact files, with span bounds and metadata stub.

**Pros:**
- **Unlocks L0 substrate** for citation validator, context packs, and write-back pipeline
- Directly implements ABS-0003 chunk-level L0 schema (chunk_id, span, summary_text, source_artifact)
- Self-contained: reads file → writes L0 JSON; no provider or embedding dependencies
- Testable with sample artifacts (create L0 from test markdown → validate schema)
- Immediate value: can manually create L0 for ABS-0003, episode L1s, and other design docs
- **Low risk:** write-only helper, no runtime integration; failures are user-visible file errors

**Cons:**
- Manual workflow (no auto-chunking yet)
- Embedding placeholders (embedding_id can be null initially)

**Risk:** Low | **Testability:** High | **Vertical slice:** ✅ Complete (create → validate → commit L0 files)

**Implementation sketch:**
```bash
scripts/create_l0_chunk.py \
  docs/abstractions/ABS-0003-*.md \
  --chunk-id L0-20260703-abs-0003-token-budgets \
  --span "lines:42-89" \
  --summary "ABS-0003 context budget allocation: 15% system..." \
  --namespace public \
  --output docs/memory/l0/
```

---

### 4. Read-only L0 inclusion in context packs
**Scope:** Extend context pack assembly to retrieve and include L0 chunks.

**Pros:**
- Demonstrates L0 → prompt flow
- Integrates with admission gating

**Cons:**
- **Depends on L0 data existing** (currently none)
- Requires selection/budgeting policy (explicit refs? hybrid retrieval? just manual seed?)
- Token budget enforcement already complex; L0 adds 5% sub-budget from ABS-0003
- Changes runtime context assembly (higher risk than dry-run)

**Risk:** Medium-High (runtime, needs L0 data) | **Testability:** Medium | **Vertical slice:** Incomplete (no L0 to include)

---

## Recommendation: **Manual L0 Chunk Creation Helper**

### Rationale

1. **Dependency unlock:** Citation validator and context pack L0 inclusion both require L0 chunks. This helper unblocks both.

2. **Smallest complete vertical:**
   - Input: artifact file + metadata flags
   - Transform: parse/chunk/bound spans
   - Output: schema-valid L0 JSON
   - Verification: load JSON, validate schema, pytest assertions
   - Memory: L1 episode documenting the helper + sample L0s created

3. **Low risk:** No provider calls, no runtime changes, no admission policy changes
````
