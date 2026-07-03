# COMP-0019: Provider Comparison — AI-Lab Next Target After CLI L0 Validation

## Metadata

- comparison_id: `COMP-0019`
- title: `AI-Lab Next Target After CLI L0 Validation`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0019-ai-lab-next-target-after-cli-l0-validation.context.json`
- created_at: `2026-07-03T15:08:15.295661+00:00`
- command: `scripts/compare_providers.py AI-Lab has completed manual L0 chunk creation, read-only explicit L0 visibility in provider latest-context JSON summaries, a pure provider L0 summary invariant validator, and optional CLI validation for that validator. Using admitted ai-lab-memory context, choose the next smallest implementation target. Compare: A) structured validation error codes/fields for validation.l0_invariants, B) L0 chunk JSON validation at create/load time using actual L0ChunkSummary.to_dict shape, C) malformed L0 store diagnostics, D) guarded explicit L0 context-pack inclusion. Recommend one small slice with exact non-goals, tests, risks, and memory-refresh notes. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Next Target After CLI L0 Validation`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has completed manual L0 chunk creation, read-only explicit L0 visibility in provider latest-context JSON summaries, a pure provider L0 summary invariant validator, and optional CLI validation for that validator. Using admitted ai-lab-memory context, choose the next smallest implementation target. Compare: A) structured validation error codes/fields for validation.l0_invariants, B) L0 chunk JSON validation at create/load time using actual L0ChunkSummary.to_dict shape, C) malformed L0 store diagnostics, D) guarded explicit L0 context-pack inclusion. Recommend one small slice with exact non-goals, tests, risks, and memory-refresh notes.

## OpenAI Response

- model: `gpt-5`

```
Recommendation: A) Structured validation error codes/fields for validation.l0_invariants

Why this is the smallest next slice
- It’s additive to the already shipped summary-layer validator and CLI flags.
- No changes to store, creation/loading paths, prompt assembly, or provider calls.
- Minimal blast radius: confined to validator output schema and JSON emitted only when --validate-l0-invariants is used.
- Enables clearer downstream automation later (B/C/D) without committing to those larger surfaces now.

Scope and deliverables
- Extend validate_provider_l0_invariants to emit structured error entries alongside messages.
- Keep default CLI JSON unchanged unless --validate-l0-invariants is present (as today).
- Define a minimal, stable error object with a v1 schema and a small initial code set aligned to current summary-layer checks.

Proposed JSON shape (additive; only when --validate-l0-invariants is set)
- validation.l0_invariants:
  - ok: boolean
  - errors: list of objects with fields:
    - code: string enum (stable, machine-readable)
    - message: human-readable summary (existing content retained)
    - chunk_id: string (if available)
    - path: string indicating offending field location (e.g., JSONPath-like)
    - details: optional small object with helpful specifics (e.g., got, expected)
  - version: "v1" (schema version for the error objects)

Initial, minimal error code set (v1)
- L0I_MISSING_CHUNK_ID
- L0I_DUPLICATE_CHUNK_ID
- L0I_MISSING_CITATION
- L0I_BAD_CITATION_FORMAT
- L0I_INVALID_SPAN (covers nonsensical or out-of-order spans)
- L0I_UNSUPPORTED_SPAN_UNIT
Notes:
- These map to the existing summary invariant checks; do not add new validations.
- Codes are provider-agnostic and tie back to the reconciled citation/span rules described in ABS-0003.

Non-goals (explicit)
- No validation of on-disk L0 chunk files or L0ChunkSummary.to_dict (that’s B).
- No new invariants or rule changes; only structure the current messages.
- No changes to exit behavior or flags beyond current --validate-l0-invariants and --fail-on-invalid-l0.
- No changes to prompt assembly, selection, context packing, or explicit L0 inclusion (that’s D).
- No store scanning/repair or diagnostics tooling (that’s C).
- No non-JSON output changes.

Tests
- Unit tests for validator:
  - Given known-bad summaries, assert deterministic code values and field population (code, path, chunk_id, details).
  - Given valid summaries, assert ok=true and errors=[].
- CLI integration tests:
  - With --print-context-summary --summary-format json --validate-l0-invariants:
    - Valid case: validation.l0_invariants present with ok=true; errors=[].
    - Invalid case: ok=false; errors[] entries include non-empty code and path.
    - With --fail-on-invalid-l0: invalid case exits non-zero (unchanged behavior).
  - Without --validate-l0-invariants: ensure no validation.l0_invariants key appears (back-compat).
- Stability tests:
  - Snapshot test of an example errors[] payload to guard code churn (allow-list codes; enforce version="v1").
- Negative/path tests:
  - Missing fields (e.g., citation absent) yields L0I_MISSING_CITATION with appropriate path.
  - Bad citation format yields L0I_BAD_CITATION_FORMAT with details.got populated.

Risks and mitigations
- Taxonomy churn risk: Mitigate by keeping a minimal initial set plus version="v1" and documenting codes as stable.
- Consumer breakage risk: Additive only and gated behind --validate-l0-invariants; default JSON remains unchanged.
- Over-specific paths: Use consistent path formatting (e.g., JSONPath-like) and test it; do not promise full JSONPath semantics beyond string location hint.
- Scope creep: Resist adding new invariants or touching store-level validation in this slice.

Memory-refresh notes
- This slice does not introduce any refresh triggers or write-back actions.
- The structured codes can be referenced by future refresh/repair workflows outlined in the reconciled plan (e.g., treating specific codes as refresh or rebuild signals), but wiring those triggers is out of scope here.
- When we later implement B (store-level validation) or C (store diagnostics), reuse the same code taxonomy and version to keep signals consistent across summary- and store-level checks.

Effort estimate
- Small (hours to one day): define code enum + fields, update validator, adjust JSON emission, write/adjust tests.

Rationale versus alternatives
- B (create/load validation) touches I/O paths and schema coupling; higher risk and coordination cost.
- C (store diagnostics) requires new CLI surface and scanning logic; broader scope.
- D (explicit L0 inclusion guard) affects selection/assembly and provider behavior; not “small.”
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Next Implementation Target Recommendation

## Selection: **Option B** — L0 chunk JSON validation at create/load time using actual L0ChunkSummary.to_dict shape

---

## Rationale

Given completed work:
- Manual L0 chunk creation exists
- Provider summaries expose read-only L0 data
- Pure provider validator checks summary-layer invariants
- CLI optionally validates provider summaries

**Option B is the natural next step** because:

1. **Smallest scope with high value**: Validates L0 chunks *at the source* (create/load), catching malformation before it propagates to summaries or embeddings.
2. **Complements existing validation**: CLI validator checks *provider summaries*; this validates *underlying chunk files*.
3. **Unblocks safe L0 usage**: Before implementing guarded context-pack inclusion (D), you need confidence that loaded L0 chunks are well-formed.
4. **Defers complexity**: Option A (structured error codes) is pure polish; C (store diagnostics) requires scanning infrastructure; D (context-pack inclusion) changes prompt assembly and raises ACL/citation risks (per ABS-0003).

---

## Exact Scope

### In Scope
1. **Schema validation helper**: `validate_l0_chunk_dict(chunk_dict: dict) -> tuple[bool, list[str]]`
   - Checks required fields: `l0_id`, `namespace`, `source_artifact_id`, `chunk_index`, `content_text`, `content_hash`, `created_at`
   - Validates types: strings, ints, ISO timestamps
   - Validates `span_start`/`span_end` if present (non-negative, start ≤ end)
   - Validates `citations` list structure if present (each entry has `target_id`, `description`)

2. **Integration at create time**: `L0ChunkSummary.save()` calls validator, logs warnings for invalid fields, optionally raises on critical failures (missing `l0_id`, `content_text`).

3. **Integration at load time**: `load_l0_chunk(path)` calls validator after JSON parse, logs warnings, optionally skips loading invalid chunks (controlled by flag).

4. **Tests**:
   - Valid L0 chunk round-trip (create, save, load, validate)
   - Missing required field (e.g., no `l0_id`) → validation fails
   - Invalid type (e.g., `chunk_index` as string) → validation fails
   - Invalid span (e.g., `span_start` > `span_end`) → validation fails
   - Malformed citations list → validation fails
   - Flag-gated behavior: strict mode raises, lenient mode warns

### Non-Goals
- **No embedding validation**: Do not check `embedding_id`, `embedding_namespace`, or vector dimensions (defer to embedding pipeline).
- **No content_hash recomputation**: Accept `content_hash` as-is; do not verify it matches `content_text` (defer to coverage/integrity checks).
- **No cross-chunk checks**: Do not validate `chunk_index` sequence gaps or duplicate `l0_id` across files (defer to store diagnostics, option C).
- **No citation target resolution**: Do not verify `citations[].target_id` exists in the store (defer to citation integrity validator, per ABS-0003).
- **No ACL/redaction validation**: Do not check `access_level` or `redaction_level` semantics (defer to ACL enforcement layer).
- **No provider summary re-validation**: Do not modify CLI validator or `validate_provider_l0_invariants` (already complete).
- **No context-pack assembly changes**: Do not enable L0 inclusion in prompts (defer to option D).

---

## Tests (Explicit Coverage)

1. **test_valid_l0_chunk_dict**: Minimal valid chunk passes validation.
2. **test_missing_l0_id**: Validator returns `(False, ["Missing required field: l0_id"])`.
3. **test_missing_content_text**: Validator returns `(False, ["Missing required field: content_text"])`.
4. **test_invalid_chunk_index_type**: `chunk_index: "five"` fails with type error.
5. **test_invalid_span_bounds**: `span_start=100, span_end=50` fails.
6. **test_malformed_citations**: `citations: [{"target_id": "C1"}]` (missing `description`) fails.
7. **test_save_invalid_chunk_strict**: `L0ChunkSummary.save(strict=True)` raises `ValidationError`.
8. **test_save_invalid_chunk_lenient**: `L0ChunkSummary.save(strict=False)` logs warning, saves anyway.
9. **test_load_invalid_chunk_strict**: `load_l0_chunk(path, strict=True)` raises or returns `None`.
10. **test_load_invalid_chunk_lenient**: `load_l0_chunk(path, strict=False)` logs warning, returns chunk with validation errors attached.
11. **test_round_trip_preserves_validity**: Create valid chunk → save → load → re-validate → still valid.

---

## Risks

| Risk | Mitigation |
|------|-----------|
| **False positives on optional fields**: Validator rejects valid chunks with missing optional fields (e.g., `keyphrases`, `embedding_id`). | Use explicit required-field whitelist; do not fail on unknown or optional fields. |
| **Breaking existing L0 chunks**: Strict validation at load breaks workflows if legacy chunks lack new required fields. | Default to lenient mode; add `--strict-l0-validation` CLI flag for opt-in strictness. |
| **Performance cost on large stores**: Validating every chunk at load scales poorly. | Validate only on explicit load (not batch scans); defer store-wide diagnostics to option C. |
| **Inconsistent error messages**: Validator messages diverge from CLI validator (`validate_provider_l0_invariants`). | Reuse message templates; consider shared `ValidationError` class (punt structured codes to option A). |
| **No citation/embedding target checks**: Invalid references pass validation. | Document non-goal clearly; defer to later invariant checks (ABS-0003 citation integrity). |

---

## Memory Refresh Notes

### L1 Episode Entry (Post-Implementation)
```json
{
  "episode_id": "EP-<date>-l0-chunk-json-validation",
  "scope": "ai-lab-memory",
  "summary_text": "Added schema validation for L0 chunk JSON at create/load time. validate_l0_chunk_dict checks required fields (l0_id, content_text, chunk_index, etc.), types, span bounds, and citations structure. Integrated into L0ChunkSummary.save() and load_l0_chunk() with strict/lenient mode flag. Does not validate embeddings, content_hash integrity, cross-chunk consistency, or citation targets (deferred). Tested with 11 cases covering valid/invalid fields, types, spans, citations, and flag behavior.",
  "completed_work": [
    "Implemented validate_l0_chunk_dict with required-field, type, span, and citations checks.",
    "Integrated validator into L0ChunkSummary.save() with strict/lenient flag.",
    "Integrated validator into load_l0_chunk() with strict/lenient flag.",
    "Added 11 tests covering valid/invalid schemas, round-trip, and flag modes."
  ],
  "key_decisions": [
    "Default to lenient mode to avoid breaking existing L0 chunks.",
    "Validate only required fields and basic structure; defer embeddings, content_hash, cross-chunk, and citation target checks.",
    "Use boolean + error list return (defer structured codes to option A)."
  ],
  "next_actions": [
    "Consider structured validation error codes (option A), malformed L0 store diagnostics (option C), or guarded L0 context-pack inclusion (option D)."
  ],
  "risks": [
    "Lenient mode may allow invalid chunks to persist; require explicit opt-in to strict mode.",
    "No validation of citation targets or embedding references; invalid links can exist."
  ]
}
```

### Links to Update
- **L1-20260703-cli-l0-summary-validation**: Add forward link in `next_actions` → "Implemented L0 chunk JSON validation (EP-<date>-l0-chunk-json-validation)".
- **ABS-0003**: Add footnote under "Validate: schema, citation integrity..." → "L0 chunk schema validation implemented; citation target resolution deferred."

---

## Summary Table: Why B > A, C, D

| Option | Why Defer |
|--------|-----------|
| **A. Structured error codes** | Pure polish; current string messages sufficient for debugging. No functional blocker. |
| **C. Store diagnostics** | Requires store-scanning infrastructure; higher complexity, less incremental value. Deferred until cross-chunk issues observed. |
| **D. Context-pack inclusion** | Changes prompt assembly; introduces ACL, citation, and token-budget risks (per ABS-0003). Requires validated L0 chunks first (→ option B prerequisite). |

**Option B** is the **minimal, safe, high-leverage** step that validates data quality at the source without changing assembly behavior.
````
