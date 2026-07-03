# SYNCOMP-0009: Comparison Synthesis — AI-Lab Next Target After Budget Preview

## Metadata

- synthesis_id: `SYNCOMP-0009`
- title: `AI-Lab Next Target After Budget Preview`
- created_at: `2026-07-03T10:05:46.429423+00:00`
- command: `scripts/synthesize_comparison.py docs/comparisons/COMP-0014-ai-lab-next-target-after-budget-preview.md --title AI-Lab Next Target After Budget Preview`
- source_comparison: `docs/comparisons/COMP-0014-ai-lab-next-target-after-budget-preview.md`
- synthesizer_provider: `OpenAI`
- synthesizer_model: `gpt-5`

## Synthesis

~~~text
1) Shared agreement
- The next target should be a small, testable, low-risk vertical slice suitable for a single commit plus a memory refresh.
- JSON output for --print-context-summary is low complexity, deterministic, and easy to test; it mainly adds machine-readable formatting around the existing dry-run preview.
- Citation validation utility depends on citation spans and/or tokenizer decisions and is premature without an L0 substrate; complexity is higher than ideal for the “next smallest” slice.
- Read-only L0 inclusion in context packs touches runtime selection/packing and depends on L0 data; it carries higher regression risk and is not the next smallest step.

2) Meaningful differences
- Primary recommendation:
  - OpenAI: JSON output for --print-context-summary.
  - Claude: Manual L0 chunk creation helper.
- Assessment of L0 helper scope:
  - OpenAI: Not a single-commit change; it forces early schema/storage decisions (IDs, spans, embedding metadata), plus docs/validations.
  - Claude: Self-contained, write-only, low risk; unlocks downstream work (citation validator, L0 inclusion) and can be fully tested now.
- Perceived value of JSON output:
  - OpenAI: Immediate CI/telemetry utility; enables comparisons without changing runtime.
  - Claude: Ergonomic only; limited value until downstream tooling consumes it; still needs schema design.

3) Stronger points from OpenAI
- Clear, minimal, and reversible scope with no runtime/provider impacts; default text remains unchanged behind an explicit flag.
- Detailed plan: flags, schema_version, deterministic key ordering, acceptance criteria, and tests (snapshot/golden, CLI parse validation).
- Leverages just-finished dry-run preview and ABS-0003 defaults; straightforward integration into ask_provider.py and compare_providers.py.

4) Stronger points from Claude
- Dependency-unlock framing: an L0 helper creates the substrate required for citation validation and L0 inclusion.
- Concrete, single-purpose CLI sketch that reads files and emits schema-valid L0 JSON; write-only and provider-agnostic.
- Emphasizes a complete vertical (create → validate → commit) with immediate practical utility for existing design docs.

5) Combined answer
- Recommendation: Implement JSON output for --print-context-summary as the next smallest vertical slice.
  - Rationale derived from both: It is the least risky, entirely formatting-only, deterministic, and immediately testable; it requires no tokenizer, storage, or runtime changes and fits cleanly in one commit with a memory refresh. It also prepares the ground for CI/telemetry and side-by-side comparisons.
- Sequencing note (synthesis/inference): Follow this with a Manual L0 chunk creation helper as the next step to unlock L0-dependent features. Keep that helper narrowly scoped to avoid schema churn (minimal IDs/spans, optional/null embedding fields, simple validator) and aim for a separate single-commit change.

6) Risks or missing assumptions
- JSON output
  - Risk: Consumers may assume JSON becomes default; mitigation via explicit --summary-format flag and docs (OpenAI).
  - Risk: Schema drift; mitigation via schema_version and minimal initial schema (OpenAI).
  - Assumption: Dry-run preview structure and numbers are stable enough for golden tests.
  - Open question: Immediate consumers for the JSON (Claude’s concern).
- Manual L0 helper
  - Risk: Scope creep into schema/storage decisions (IDs, span units, embedding metadata) and documentation (OpenAI).
  - Assumption: A minimal ABS-0003-aligned L0 schema can be frozen quickly (Claude implies yes; OpenAI implies not yet).
  - Operational: Manual workflow is acceptable initially; auto-chunking and embeddings can remain out-of-scope (Claude).
- Deferred items
  - Citation validator remains gated on L0 data and tokenizer/span unit decisions.
  - L0 inclusion in context packs remains higher risk due to runtime impacts and budgeting integration.

7) Suggested re-ask prompt
“Given we’ve completed the dry-run Context Budget Preview, should we prioritize:
A) JSON output for --print-context-summary (explicit --summary-format json, schema_version v1, no runtime changes, golden tests, immediate CI parsing), or
B) A narrowly scoped Manual L0 chunk creation helper (write-only CLI that outputs minimal ABS-0003-aligned L0 JSON with ids and line-span bounds, embeddings optional/null, plus a validator and tests)?
Please confirm:
- Do we need immediate machine-readable summaries in CI for compare_providers.py?
- Are we ready to freeze a minimal L0 schema (ids, span unit, required fields) for a single-commit helper?
- Any hard constraints on flags, output locations, or schema_versioning we must follow?”
~~~

## Source Comparison

~~~markdown
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

~~~
