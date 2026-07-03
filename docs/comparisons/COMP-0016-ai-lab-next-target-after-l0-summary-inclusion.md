# COMP-0016: Provider Comparison — AI-Lab Next Target After L0 Summary Inclusion

## Metadata

- comparison_id: `COMP-0016`
- title: `AI-Lab Next Target After L0 Summary Inclusion`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0016-ai-lab-next-target-after-l0-summary-inclusion.context.json`
- created_at: `2026-07-03T11:13:17.832360+00:00`
- command: `scripts/compare_providers.py AI-Lab has completed Manual L0 chunk creation and read-only explicit L0 visibility in provider latest-context dry-run JSON summaries. Using admitted ai-lab-memory context, choose the next smallest implementation target. Compare actual explicit L0 context-pack inclusion, L0 JSON/schema validation hardening, citation validation, and provider summary UX/docs. Recommend one target, exact non-goals, tests, risks, and memory-refresh notes. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Next Target After L0 Summary Inclusion`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has completed Manual L0 chunk creation and read-only explicit L0 visibility in provider latest-context dry-run JSON summaries. Using admitted ai-lab-memory context, choose the next smallest implementation target. Compare actual explicit L0 context-pack inclusion, L0 JSON/schema validation hardening, citation validation, and provider summary UX/docs. Recommend one target, exact non-goals, tests, risks, and memory-refresh notes.

## OpenAI Response

- model: `gpt-5`

```
Summary
- Current state: L0 chunk creation exists and explicit L0 visibility is available only in provider latest-context dry-run JSON summaries (schema_version v1) via l0_candidates, l0_included, and l0_dropped. This does not alter rendered context packs or final prompts. Deduplication is in place; dropped reasons include not_found and over_budget; rough deterministic token-cost estimates are computed.

Comparison of next targets
- Actual explicit L0 context-pack inclusion
  - Size/complexity: Medium–High. Touches prompt assembly, budgeting, and potentially ACL/redaction and downstream behaviors.
  - Risk: High. Changes prompt content; requires tighter validation (citations, spans) and token budgeting fidelity.
  - Dependencies: Strongly benefits from prior schema/validation hardening to avoid regressions.

- L0 JSON/schema validation hardening
  - Size/complexity: Low. Constrained to schema definition, validation routines, CLI hooks, and tests.
  - Risk: Low. Read-only path; no changes to prompt assembly.
  - Value: High leverage as a foundation for safe future inclusion and citation work; catches regressions early.

- Citation validation (cid@version|span)
  - Size/complexity: Medium. Requires manifest/candidate-to-citation integrity rules and tokenizer/version discipline. Highest value once citations actually appear in prompts/answers.
  - Risk: Medium. Easy to drift without stable inclusion logic and span policy wired in.
  - Dependencies: Strong dependency on L0 manifest stability and schema.

- Provider summary UX/docs
  - Size/complexity: Low (docs/CLI UX).
  - Risk: Low.
  - Value: Moderate; helpful but less foundational than validation hardening.

Recommendation
- Next smallest implementation target: L0 JSON/schema validation hardening.
- Rationale: It is the smallest, lowest-risk slice that solidifies the newly added L0 summary surface. It prepares the codebase for actual L0 inclusion and citation validation by enforcing invariants now, without changing prompts.

Scope and deliverables
- Define and enforce a strict schema for provider latest-context dry-run JSON, schema_version v1, covering:
  - Top-level controls:
    - include_l0: boolean (required when --include-l0 is passed).
    - schema_version: "v1".
  - L0 fields (required only when include_l0 is true):
    - l0_candidates: array of objects with:
      - chunk_id: string (required)
      - est_token_cost: integer >= 0 (required)
    - l0_included: array of objects with:
      - chunk_id: string (required)
      - est_token_cost: integer >= 0 (required)
    - l0_dropped: array of objects with:
      - chunk_id: string (required)
      - reason: enum {"not_found", "over_budget"} (required)
      - est_token_cost: integer >= 0 (optional; present if known pre-drop)
- Invariants to validate when include_l0 is true:
  - Uniqueness: chunk_id values are unique within each of l0_candidates, l0_included, and l0_dropped.
  - Partition: set(l0_included) ∪ set(l0_dropped) == set(l0_candidates) and the two are disjoint.
  - not_found: any l0_dropped item with reason == not_found must not appear in the L0 store.
  - over_budget: if --context-window is provided and an L0 budget bucket is computed, the sum(est_token_cost of l0_included) <= computed L0 budget.
  - Determinism: est_token_cost is non-negative and derived from the deterministic rough estimator already in prompt_context.py.
- Tooling:
  - JSON Schema file for v1 placed under docs/schemas/provider_context_summary.v1.json.
  - Runtime validator:
    - Python validation module called from format_provider_context_summary_json (or just after) when --print-context-summary --summary-format json is used.
    - New CLI flag --validate-summary (on by default for tests; off by default for end users initially if needed).
  - Errors are precise: include which invariant failed and which ids are affected.
- Telemetry/logging:
  - Log validation result with counts for candidates/included/dropped and reasons for drops.
- Backward compatibility:
  - No changes to rendered context packs or final prompts.
  - l0_* fields remain omitted entirely when --include-l0 is not set.

Explicit non-goals
- Do not include L0 chunks in rendered context packs or final prompts.
- Do not introduce tokenizer-exact token accounting; keep the existing rough deterministic estimator.
- Do not change budgeting policy or percentages.
- Do not implement citation emission or answer-time citation validation.
- Do not modify ACL/redaction or embedding storage behavior.

Tests
- Unit tests (prompt_context and summary formatting):
  - Shape validation: valid record with include_l0=false omits l0_*; with include_l0=true requires l0_*.
  - Dedup invariant: ensure no duplicates within each list; inject duplicates to assert validator failure messages.
  - Partition invariant: included + dropped equals candidates; simulate missing-dropped or extra-included to assert failure.
  - not_found behavior: provide an explicit chunk_id absent in L0 store; ensure it appears only in l0_dropped with reason=not_found.
  - over_budget behavior: with a constrained --context-window causing a tight L0 budget, ensure overflow candidates are in l0_dropped with reason=over_budget and included sum <= budget.
  - Deterministic est_token_cost: same inputs yield identical estimates across runs.
- CLI integration tests:
  - ask_provider.py with --include-l0 --l0-store --print-context-summary --summary-format json --validate-summary passes.
  - compare_providers.py same as above passes for multiple providers.
  - Negative cases: malformed l0_* arrays or mismatched partition cause non-zero exit with clear messages.
- Property-based tests (optional but small):
  - Generate random candidate sets and budgets; assert partition and budget invariants hold after selection/dropping.
- Golden JSON fixtures:
  - Store a small set of validated summaries for regression.

Risks and mitigations
- Schema churn as we learn: Mitigate with schema_version pinned to "v1" and additive-only changes; document breaking change policy.
- Budget mismatch due to rough token estimates: Treat budget check as a best-effort warning-level validation that can be elevated to error behind a flag if needed.
- Provider divergence: Keep schema provider-agnostic; where provider fields differ, restrict validation to L0-related keys introduced in this slice.
- Test brittleness across environments: Use fixed test L0 store fixtures and stable inputs; avoid environment-dependent paths in summaries.

Memory-refresh notes
- Add an episode L1 entry:
  - Title: L1-202607XX-l0-schema-validation-hardening
  - Completed work: Introduced JSON Schema v1 for provider latest-context dry-run summaries; implemented runtime validator gated by --validate-summary; enforced invariants for l0_candidates/included/dropped; added unit/integration/property tests and golden fixtures.
  - Key decisions: Keep L0 visibility read-only; validation applies only to --print-context-summary --summary-format json; no prompt/context-pack changes.
  - Risks: Schema evolution; rough token estimate can under/over-count vs tokenizer; provider divergence. Mitigations documented.
  - Next actions: After stabilization, consider actual explicit L0 context-pack inclusion (guarded by a feature flag) and then citation validation aligned with cid@version|span rules from ABS-0003.
- TTL: none; mark as fresh upon landing.
- Link to content hash and schema path in the entry for reproducibility.

Why this sequence
- Hardening the JSON/schema now gives us a stable, validated surface to safely implement actual L0 inclusion next and then citation validation, reducing risk of regressions and ensuring provider comparisons remain apples-to-apples.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Next Implementation Target Recommendation

## Analysis of Candidate Targets

Based on the completed work (manual L0 chunk creation + read-only JSON summary visibility) and the reconciled memory loop abstraction, I've evaluated four candidates:

### 1. **Actual Explicit L0 Context-Pack Inclusion**
- **Scope**: Render admitted L0 chunks into the final context pack string sent to providers
- **Complexity**: Medium – requires format_context_pack modifications, citation template integration, budget enforcement
- **Dependencies**: Current L0 admission logic (✓ exists), citation format definition (ABS-0003 specifies `cid@version|span`)
- **Value**: Enables end-to-end L0 retrieval → prompt flow

### 2. **L0 JSON/Schema Validation Hardening**
- **Scope**: Add schema validation for L0 chunk JSON files, enforce required fields, validate citation format in stored chunks
- **Complexity**: Low – isolated validation layer, no provider integration
- **Dependencies**: L0 schema definition (implicit in current create_l0_chunk.py), JSON schema library
- **Value**: Prevents malformed L0 data from entering the pipeline

### 3. **Citation Validation**
- **Scope**: Validate provider output citations against included L0 chunks, check `cid@version|span` format
- **Complexity**: Medium-High – requires output parsing, span validation rules, tokenizer alignment
- **Dependencies**: L0 inclusion in prompts (✗ not yet implemented), span unit standardization
- **Value**: Ensures citation integrity, but premature without L0 in prompts

### 4. **Provider Summary UX/Docs**
- **Scope**: Document --include-l0 flag usage, add examples, improve JSON schema documentation
- **Complexity**: Low – documentation only
- **Dependencies**: Stable L0 summary API (✓ exists in v1 schema)
- **Value**: Developer ergonomics, but feature is read-only/dry-run only

---

## Recommendation: **L0 JSON/Schema Validation Hardening**

### Rationale
1. **Smallest safe increment**: Validation is self-contained and guards the foundation before building inclusion logic
2. **Risk mitigation first**: Per L1-20260703 risks, token cost is rough and L0 isn't in prompts yet – hardening the data layer prevents cascading errors when inclusion is implemented
3. **Unblocks parallel work**: With schema validation in place, L0 inclusion can proceed confidently; citation validation depends on inclusion existing
4. **Natural dependency order**: Validate → Include → Cite

### Exact Target Scope

**In scope:**
- JSON schema definition for L0 chunk summary format (required fields: `chunk_id`, `content_hash`, `source_path`, `summary_text`, `token_estimate`, `topics`, `namespace`, `access_level`)
- Schema validation in `create_l0_chunk.py` at write time
- Schema validation in `prompt_context.py` L0 store loading (reject malformed chunks early)
- Unit tests for schema compliance (missing fields, type mismatches, invalid enums)
- Validation for `citations` array structure if present (must be list of dicts with `target_id`, `relationship`)

**Explicit non-goals:**
- ❌ Citation format validation (`cid@version|span`) – deferred to citation validation slice
- ❌ Semantic validation (e.g., whether `source_path` file exists) – file-level checks are create-time only
- ❌ Cross-chunk consistency checks (e.g., citation target existence) – deferred
- ❌ Embedding metadata validation – L0 chunks don't yet include embeddings per current implementation
- ❌ Span bounds validation – no spans in current L0 schema
- ❌ Token estimate accuracy – keep rough word-count method, validate presence only
- ❌ Modification of inclusion logic or provider integration

---

## Implementation Plan

### Tests Required
```python
# tests/test_l0_schema_validation.py

def test_valid_l0_chunk_passes_validation()
def test_missing_required_field_chunk_id_fails()
def test_missing_required_field_content_hash_fails()
def test_invalid_access_level_enum_fails()
def test_invalid_namespace_
````
