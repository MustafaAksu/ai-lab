# COMP-0020: Provider Comparison — AI-Lab Next Target After Structured L0 Validation Errors

## Metadata

- comparison_id: `COMP-0020`
- title: `AI-Lab Next Target After Structured L0 Validation Errors`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0020-ai-lab-next-target-after-structured-l0-validation-errors.context.json`
- created_at: `2026-07-03T15:21:50.646321+00:00`
- command: `scripts/compare_providers.py AI-Lab has completed manual L0 chunk creation, read-only explicit L0 visibility in provider latest-context JSON summaries, pure provider L0 summary invariant validation, optional CLI validation, and structured validation.l0_invariants errors with version/code/message/path/optional chunk_id. Using admitted ai-lab-memory context, choose the next smallest implementation target. Compare: A) collect all provider L0 invariant failures instead of first-error-only, B) L0 chunk JSON validation at create/load time using the actual L0ChunkSummary.to_dict shape, C) malformed L0 store diagnostics, D) guarded explicit L0 context-pack inclusion. Recommend one small slice with exact non-goals, tests, risks, and memory-refresh notes. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Next Target After Structured L0 Validation Errors`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has completed manual L0 chunk creation, read-only explicit L0 visibility in provider latest-context JSON summaries, pure provider L0 summary invariant validation, optional CLI validation, and structured validation.l0_invariants errors with version/code/message/path/optional chunk_id. Using admitted ai-lab-memory context, choose the next smallest implementation target. Compare: A) collect all provider L0 invariant failures instead of first-error-only, B) L0 chunk JSON validation at create/load time using the actual L0ChunkSummary.to_dict shape, C) malformed L0 store diagnostics, D) guarded explicit L0 context-pack inclusion. Recommend one small slice with exact non-goals, tests, risks, and memory-refresh notes.

## OpenAI Response

- model: `gpt-5`

```
Recommendation: A) Collect all provider L0 invariant failures

Why this is the smallest next slice
- It directly addresses a known gap called out in the current L1: “Only the first validation failure is reported because validate_provider_l0_invariants still raises on first violation.”
- It reuses the already-landed structured error surface (version/code/message/path/optional chunk_id) without introducing new schemas or touching L0 storage, loading, or prompt assembly.
- It requires localized changes to the validator and CLI wiring only; no new rules, no schema expansion, no store scanning, no selection/packing changes.

Scope (small slice)
- Add an accumulate_all option (default False) to validate_provider_l0_invariants to collect all violations instead of raising on the first.
- Wire ask_provider.py and compare_providers.py to pass accumulate_all=True when producing --validate-l0-invariants JSON.
- Ensure provider_l0_invariant_validation_result v1 ok/errors output supports multiple error entries (already does); do not change the JSON schema or version.
- Keep invariant logic and error mapping exactly the same; only change control flow to continue evaluation after each failure and append structured errors.

Non-goals (explicit)
- No new invariant rules, codes, or message mappings.
- No changes to L0 chunk JSON schema or validation at create/load time (defer B).
- No store scanning or corruption diagnostics (defer C).
- No changes to prompt assembly or context-pack inclusion behavior (defer D).
- No new CLI flags; preserve --validate-l0-invariants as-is.
- Do not change default programmatic behavior for callers expecting a raised exception on first failure.

Implementation notes
- Introduce a private helper collect_provider_l0_invariant_failures(...) that:
  - Runs the existing invariant checks in a fixed, documented order.
  - Converts each detected violation to the existing structured entry {code, message, path, chunk_id?}.
  - Returns a list[ValidationErrorEntry].
- Update validate_provider_l0_invariants(..., accumulate_all=False):
  - If accumulate_all is False: preserve current behavior (raise on first violation).
  - If True: call the collector, return normally; upstream code assembles provider_l0_invariant_validation_result with ok = (len(errors) == 0).
- Update ask_provider.py and compare_providers.py to set accumulate_all=True for the JSON validator path.
- Preserve deterministic error ordering by evaluating checks in the same sequence as today and sorting only when checks iterate unordered structures (e.g., sort by path then code for per-item checks across a dict).

Tests (additions)
- Unit: structured multiple failures
  - Construct a minimal latest-context summary that triggers at least two distinct invariant failures (e.g., duplicate cid and bad list shape).
  - Call validate_provider_l0_invariants(..., accumulate_all=True) through the CLI path and assert:
    - ok == False
    - len(errors) >= 2
    - Each entry has version=v1 fields: code, message, path present; chunk_id present when applicable.
    - Error order is deterministic against a fixed snapshot.
- Unit: backward compatibility (first-error)
  - Call validate_provider_l0_invariants(..., accumulate_all=False) on the same bad input and assert it raises the first error as before and maps to the same structured entry if wrapped.
- CLI: ask_provider --validate-l0-invariants
  - Golden JSON snapshot showing multiple errors collected with stable ordering.
- CLI: compare_providers --validate-l0-invariants
  - Ensure each provider’s results include all their errors independently and the tool exits/fails the same as before on any not-ok, but with full error lists.
- Regression: success case unchanged
  - On a known-good latest-context summary, ok == True and errors == [] in both accumulate modes.

Risks and mitigations
- Runtime overhead: Evaluating all checks may be slightly slower on large summaries.
  - Mitigation: Checks are summary-layer only; document that worst-case remains acceptable. Add a lightweight benchmark in CI guard if needed.
- Ordering instability across Python versions/containers if iterating dicts inconsistently.
  - Mitigation: Explicitly sort per-item checks by path then code before appending.
- Downstream code relying on exception semantics.
  - Mitigation: Default remains accumulate_all=False. Only CLI paths opt into collection.
- Future message changes breaking code mapping remain a risk (unchanged from today).
  - Mitigation: Keep tests keyed to codes/paths and maintain mapping table alongside checks.

Rollout/compatibility
- No schema/version changes to provider_l0_invariant_validation_result (stays v1).
- No CLI surface changes; behavior is strictly additive (more complete errors).
- No changes to provider calls, L0 creation/loading, or context assembly.

Memory-refresh notes
- Update L1-20260703-structured-l0-validation-errors:
  - completed_work: “Collect all provider L0 invariant failures in CLI validator output.”
  - key_decisions: “Default validator keeps first-error raise; CLI paths use accumulate_all=True.”
  - risks: Remove/soften the “first-error-only” risk; retain message-to-code mapping risk.
  - next_actions: Reorder the remaining options by size: B (L0 chunk JSON validation), C (malformed store diagnostics), D (guarded explicit L0 inclusion).
- No L0/L1 content TTL or refresh policy changes required.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# Recommendation: Option B – L0 Chunk JSON Validation at Create/Load Time

## Rationale

Option **B** is the smallest, most self-contained next step:

- **A** (collect-all failures) is a pure enhancement to existing validator behavior—valuable but cosmetic until you have more validation rules to batch.
- **C** (malformed store diagnostics) depends on knowing what "malformed" means at the file level; B establishes the baseline shape.
- **D** (guarded L0 in context packs) is a runtime assembly feature that depends on robust L0 load validation; you must trust the shape before packing it.

**B establishes the L0 chunk-file contract** before any other tool (diagnostics, context-pack inclusion, or batch validation) touches persisted chunks.

---

## Slice Definition

### Goal
Validate the JSON shape of L0 chunk files when `L0ChunkSummary.from_dict(data)` is called during **creation** (write) and **load** (read) operations.

### Scope
1. **Add `validate_l0_chunk_shape(data: dict) → tuple[bool, list[ValidationError]]`** helper to `memory/validation.py`:
   - Check required top-level keys: `chunk_id`, `version`, `content_hash`, `source_path`, `span`, `created_at`, `embedding_id`, `embedding_namespace`, `summary_text`.
   - Check required `span` sub-keys: `start`, `end`, `unit`.
   - Check types: strings for IDs/paths/hashes/text, dict for `span`, list for optional arrays (`topics`, `citations`, `dependencies`).
   - Check non-empty constraints: `chunk_id`, `version`, `content_hash` must be non-empty strings.
   - Return `(True, [])` on success or `(False, [ValidationError(...)])` on failure, where each `ValidationError` has `code`, `message`, `path`, `chunk_id`.

2. **Integrate into `L0ChunkSummary.from_dict`**:
   - Call `validate_l0_chunk_shape(data)` before unpacking fields.
   - Raise `ValueError` with structured message if validation fails (keep existing exception contract).

3. **Integrate into write path** (`MemoryProvider.create_l0_chunk` or equivalent):
   - Call `validate_l0_chunk_shape(chunk.to_dict())` before writing JSON to disk.
   - Fail-fast on invalid shape (do not persist).

4. **Test coverage**:
   - Valid minimal L0 chunk → success.
   - Missing required top-level key → structured error with path `chunk_id` or `span.start`.
   - Wrong type (e.g., `span` is a string, not dict) → structured error.
   - Empty `chunk_id` → structured error.
   - Optional fields missing or empty (e.g., `topics: []`) → success.

---

## Explicit Non-Goals

- **Do NOT** validate citation format (`cid@version|span`) inside `citations` array (that is citation-integrity validation, not shape validation).
- **Do NOT** validate `span.unit` enum values or token/line/char-offset semantics (future span-validation task).
- **Do NOT** validate cross-chunk or cross-provider invariants (e.g., duplicate `chunk_id` across chunks in a provider store).
- **Do NOT** change the existing provider L0 summary invariant validator (`validate_provider_l0_invariants`) or its first-error-only behavior.
- **Do NOT** add batch/collect-all-errors logic yet (option A).
- **Do NOT** add store-level diagnostics (option C).
- **Do NOT** add context-pack L0 inclusion logic (option D).

---

## Risks

| Risk | Mitigation |
|------|------------|
| **Message-derived error codes** (existing pattern) | Accept for now; consider enum-based codes in future refactor. |
| **Schema drift**: `L0ChunkSummary.to_dict` evolves, tests stale | Pin one test to serialize a live `L0ChunkSummary` and validate its own dict. |
| **Validation at write only**: malformed legacy chunks still load | Validate on load too; log/warn for legacy chunks, fail-fast for new writes. |
| **Performance**: validating every chunk on load in tight loops | Measure first; defer caching/skip-on-trusted-source optimization until proven necessary. |

---

## Tests (Minimum 5)

1. **`test_l0_chunk_shape_valid_minimal`**: all required fields, no optional → `(True, [])`.
2. **`test_l0_chunk_shape_missing_chunk_id`**: omit `chunk_id` → error with `path="chunk_id"`, `code="MISSING_REQUIRED_FIELD"`.
3. **`test_l0_chunk_shape_span_wrong_type`**: `span: "invalid"` → error with `path="span"`, `code="INVALID_TYPE"`.
4. **`test_l0_chunk_shape_empty_version`**: `version: ""` → error with `code="EMPTY_VALUE"`.
5. **`test_l0_chunk_from_dict_invalid_shape_raises`**: call `L0ChunkSummary.from_dict(bad_data)` → `ValueError` with structured message.
6. **`test_l0_chunk_roundtrip_validates_self`**: create chunk, serialize `.to_dict()`, validate shape → success (schema-drift canary).

---

## Memory Refresh Notes

### What to write back after implementation
Create **L1-20260704-l0-chunk-json-shape-validation** with:

- **completed_work**:
  - Added `validate_l0_chunk_shape(data)` to `memory/validation.py` with required/type/non-empty checks.
  - Integrated into `L0ChunkSummary.from_dict` and write path (provider `create_l0_chunk` or equivalent).
  - Added 6 tests covering valid minimal, missing field, wrong type, empty value, ValueError contract, and roundtrip self-validation.
  - Verified full suite: 251 passed (6 new).

- **key_decisions**:
  - Validate both at write (fail-fast persistence) and load (detect legacy corruption).
  - Use existing `ValidationError` structure (code/message/path/chunk_id) for consistency with provider L0 invariants.
  - Do not validate citation format, span semantics, or cross-chunk invariants yet.

- **risks**:
  - Schema drift between `to_dict`/`from_dict` and validator if fields added without test updates (mitigated by roundtrip test).
  - Legacy chunks in store may fail load validation; decision needed: warn-and-continue vs fail-fast (document choice).

- **next_actions**:
  - Consider option A (collect-all validation failures), option C (malformed store diagnostics), or option D (guarded L0 context-pack inclusion).
  - Add span-unit enum validation and citation-format validation as separate tasks.

### Where to update
- **Provider latest-context summaries** (`openai.json`, `anthropic.json`, etc.):
  - Add to `l0_chunks.validation` section: `"JSON shape validated at create and load with required fields chunk_id, version, content_hash, source_path, span (start/end/unit), created_at, embedding_id, embedding_namespace, summary_text; enforces types and non-empty constraints."`.
  - Increment `last_validation_at` timestamp.

- **`docs/memory/validation.md`** (if exists):
  - Document `validate_l0_chunk_shape` signature, error codes (`MISSING_REQUIRED_FIELD`, `INVALID_TYPE`, `EMPTY_VALUE`), and integration points.

---

## Summary

**Choose B.** It is the foundational validation that options C and D depend on, and it is strictly smaller than A (which is a control-flow change to an existing validator). Implement shape validation, write 6 tests, document the new L1 episode, update provider summaries, and you will have a clean checkpoint before tackling batch validation, diagnostics, or context-pack inclusion.
```
