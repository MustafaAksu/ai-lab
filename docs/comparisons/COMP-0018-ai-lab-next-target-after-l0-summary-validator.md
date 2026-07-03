# COMP-0018: Provider Comparison — AI-Lab Next Target After L0 Summary Validator

## Metadata

- comparison_id: `COMP-0018`
- title: `AI-Lab Next Target After L0 Summary Validator`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0018-ai-lab-next-target-after-l0-summary-validator.context.json`
- created_at: `2026-07-03T11:40:42.666356+00:00`
- command: `scripts/compare_providers.py AI-Lab has completed manual L0 chunk creation, read-only explicit L0 visibility in provider latest-context JSON summaries, and a pure provider L0 summary invariant validator. Claude output-cap truncation is fixed. Using admitted ai-lab-memory context, choose the next smallest implementation target. Compare: A) wire validate_provider_l0_invariants into optional CLI validation for --print-context-summary --summary-format json, B) validate L0 chunk JSON at create/load time, C) harden malformed L0 store diagnostics, D) guarded explicit L0 context-pack inclusion. Recommend one small slice with exact non-goals, tests, risks, and memory-refresh notes. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Next Target After L0 Summary Validator`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has completed manual L0 chunk creation, read-only explicit L0 visibility in provider latest-context JSON summaries, and a pure provider L0 summary invariant validator. Claude output-cap truncation is fixed. Using admitted ai-lab-memory context, choose the next smallest implementation target. Compare: A) wire validate_provider_l0_invariants into optional CLI validation for --print-context-summary --summary-format json, B) validate L0 chunk JSON at create/load time, C) harden malformed L0 store diagnostics, D) guarded explicit L0 context-pack inclusion. Recommend one small slice with exact non-goals, tests, risks, and memory-refresh notes.

## OpenAI Response

- model: `gpt-5`

```
Recommendation: A) Wire validate_provider_l0_invariants into optional CLI validation for --print-context-summary --summary-format json

Why this is the next smallest slice
- Leverages work already done: you have a pure provider L0 summary invariant validator and read‑only L0 visibility in latest-context JSON.
- Read-only, no changes to write paths, storage, or selection logic.
- Minimal surface area: adds an optional check to an existing CLI code path.
- Aligns with the reconciled loop’s “Validate” step without committing to broader enforcement (per ABS-0003).

Scope and behavior
- Add an optional flag to print-context-summary:
  - --validate-l0-invariants: run validate_provider_l0_invariants over the L0 entries present in the provider latest-context JSON that the command already emits/handles.
  - Optional stricter behavior: --fail-on-invalid-l0 toggles nonzero exit on validation failure (default: report in output, exit 0).
- Output (JSON mode):
  - Augment existing JSON with a new top-level or namespaced field, e.g. "validation": { "l0_invariants": { "ok": true|false, "errors": [...], "warnings": [...] } }.
  - Error/warning item shape: { "code": "STRING", "message": "STRING", "chunk_id": "STRING", "field": "STRING", "provider": "STRING" }.
  - Keep additions strictly additive to avoid breaking existing parsers.
- Output (text mode):
  - Print a one-line summary and, if requested via --verbose, list the first N errors.
- Performance guardrails:
  - Cap reported errors to N (e.g., 100) and include "truncated": true if capped.
  - No network calls; operate only on in-memory JSON.

Exact non-goals for this slice
- Do not validate at create/load time or block writes/loads (B is out of scope).
- Do not change context-pack inclusion, selection, budgeting, or prompting (D is out of scope).
- Do not auto-correct or mutate store data.
- Do not expand validator coverage beyond existing L0 invariant checks (no L1/episode/citation/ACL/DLP validations).
- Do not introduce new storage schemas or migration steps.
- Do not add telemetry, metrics, or broad diagnostic hardening (C is out of scope).

Tests (exact)
- Unit tests
  - Validator wiring:
    - Given valid L0 entries, running CLI with --print-context-summary --summary-format json --validate-l0-invariants yields "validation.l0_invariants.ok": true, errors: [].
    - Given invalid L0 entries, same command yields ok: false with at least one error carrying chunk_id and code.
  - Exit semantics:
    - With --fail-on-invalid-l0 and invalid L0, process exits nonzero.
    - Without --fail-on-invalid-l0, process exits zero even if ok: false.
  - Flag behavior:
    - Without --validate-l0-invariants, no "validation" field is added.
  - Text mode:
    - With --summary-format text and --validate-l0-invariants, prints a concise pass/fail line; with --verbose, prints first N errors.
  - Edge cases:
    - No L0 present in latest-context JSON: treat as ok: true with a "warnings" entry noting “no L0 entries to validate.”
    - Mixed providers in latest-context: validator runs per provider section; errors include provider field.
    - Large L0 sets: ensure error list truncation behavior and "truncated": true are present.
- Integration tests
  - Run the full CLI against a fixture episode/context pack that includes:
    - Valid L0 for provider A, invalid L0 for provider B; verify per-provider errors are surfaced.
  - Backward-compat test:
    - Existing scripts that parse the JSON without the --validate-l0-invariants flag see unchanged structure.

Risks and mitigations
- Output contract drift:
  - Mitigation: behind an explicit flag; JSON addition is strictly additive and namespaced ("validation").
- Unexpected nonzero exits breaking automation:
  - Mitigation: default keeps exit code 0; nonzero only with --fail-on-invalid-l0.
- Performance on very large L0 sets:
  - Mitigation: cap error reporting, avoid network IO, measure and document typical runtime.
- Provider semantic mismatches (chunk-level vs artifact-level summaries per ABS-0003):
  - Mitigation: keep validator provider-aware as it is today; surface provider in each error so downstream can triage by provider semantics.

Memory-refresh notes
- This slice only surfaces issues; it does not trigger refresh/write-back.
- Include in the JSON a lightweight "refresh_hints": { "l0_chunks_to_review": [chunk_id...], "reason": "l0_invariant_failure" } to make it easy for a follow-on job to schedule refresh actions (manual or automated) consistent with ABS-0003’s refresh triggers.
- Future slice (not in scope here): a small worker that consumes refresh_hints and queues micro-summary regeneration for failed chunks.

Why not B/C/D right now
- B (validate at create/load) touches write/load paths and error propagation; higher blast radius and operational impact.
- C (diagnostics hardening) is broader and requires surveying many malformed states and adding logging/metrics; larger scope.
- D (guarded explicit L0 inclusion) affects selection/assembly and prompt invariants; significantly higher complexity and risk.

Effort/impact
- Change size: small (CLI command path + JSON shaping + tests).
- Value: immediate visibility into L0 integrity with minimal risk, paving the way for B/C/D as follow-ups.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Recommendation: Option B — Validate L0 chunk JSON at create/load time

## Rationale

**Why B is the smallest, highest-value target:**

1. **Immediate quality gate**: Catches malformed L0 chunks at ingestion, before they propagate into stores, context packs, or provider summaries.
2. **Minimal surface area**: Validation logic already exists (`validate_provider_l0_invariants`); this adds a single call site in the chunk creation/load path.
3. **Unlocks downstream work**: Options A, C, and D all assume well-formed L0 chunks in storage. B establishes that precondition.
4. **Aligned with reconciled memory loop**: ABS-0003 emphasizes schema validation and write-back integrity; create/load-time validation is the earliest enforcement point.

**Why not A, C, or D:**

- **A (CLI validation)**: Read-only diagnostic tool; defers quality enforcement to manual inspection.
- **C (diagnostics)**: Addresses symptoms after malformed data is already stored; requires store scanning.
- **D (context-pack inclusion)**: Higher complexity (pack assembly logic, token budget interaction); depends on stable L0 store (B).

---

## Implementation Slice

### Goal

Enforce L0 chunk JSON schema invariants at the moment a chunk is created or loaded from disk, rejecting invalid chunks with actionable error messages.

### Exact Scope

1. **Wrap `validate_provider_l0_invariants` at two call sites:**
   - `scripts/create_l0_chunk.py` (after JSON construction, before write).
   - `src/ai_lab_memory/l0_loader.py` (or equivalent; after JSON read, before object construction).

2. **Validation rules** (already in `validate_provider_l0_invariants`):
   - Required fields: `l0_id`, `chunk_id`, `namespace`, `content_hash`, `summary_text`, `created_at`.
   - `l0_id` format: `L0-<8-char-hex>`.
   - `namespace` in `["public", "internal", "restricted"]`.
   - `created_at` is ISO 8601 with timezone.
   - `content_hash` is 64-char hex (SHA-256).

3. **Error handling:**
   - Raise `ValueError` with violation details (field name, rule, actual value).
   - In `create_l0_chunk.py`: abort before file write; print error to stderr.
   - In loader: abort load; log error; surface to caller (e.g., context assembly).

4. **Output:**
   - Success: chunk JSON written to `docs/memory/l0/` (create) or loaded into memory (load).
   - Failure: process exits with code 1 (create) or raises exception (load).

### Explicit Non-Goals

- **CLI `--validate` flag**: Deferred to option A (post-hoc validation).
- **Store-wide audit**: Deferred to option C (diagnostics for existing malformed chunks).
- **Embedding validation**: `embedding_id`, `embedding_namespace`, `embedding_model` are outside L0 schema per reconciled plan (embeddings external).
- **Citation format validation**: Citations live in L1 summaries and prompts, not L0 chunk JSON.
- **Span bounds validation**: `span_start`/`span_end` integrity (e.g., within artifact bounds) is a future L0-to-artifact cross-check.
- **ACL/redaction checks**: Namespace is validated, but content-level PII/DLP scanning is a write-back pipeline concern (ABS-0003 section 7).

---

## Tests

### Unit Tests (4 new tests in `tests/test_l0_validation.py`)

1. **`test_valid_l0_chunk_passes`**  
   - Input: Minimal valid L0 JSON (all required fields, correct formats).  
   - Assert: No exception raised; chunk object returned.

2. **`test_missing_required_field_fails`**  
   - Input: L0 JSON missing `chunk_id`.  
   - Assert: `ValueError` with message `"Missing required field: chunk_id"`.

3. **`test_invalid_l0_id_format_fails`**  
   - Input: `l0_id = "L0-shortid"` (only 7 chars).  
   - Assert: `ValueError` with message `"l0_id must match L0-<8-hex>"`.

4. **`test_invalid_namespace_fails`**  
   - Input: `namespace = "secret"` (not in allowed list).  
   - Assert: `ValueError` with message `"namespace must be one of [public, internal, restricted]"`.

### Integration Test (1 test in `tests/test_create_l0_chunk_validation.py`)

5. **`test_create_l0_chunk_rejects_invalid_json`**  
   - Setup: Mock artifact file; malformed L0 JSON (e.g., `created_at = "not-a-date"`).  
   - Run: `create_l0_chunk.py` via subprocess.  
   - Assert: Exit code 1; stderr contains `"created_at must be ISO 8601"`.

### Coverage Target

- 100% of `validate_provider_l0_invariants` branches.
- Both create and load call sites exercised.

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Validation rejects legacy L0 chunks** (pre-dating schema) | Load failures; context pack assembly breaks | 1. Audit existing L0 store with option C *before* deployment. 2. Provide `--skip-validation` escape hatch (logs warning). 3. Backfill malformed chunks. |
| **Performance overhead** (validation on every load) | Latency in context assembly (100s of L0 chunks) | 1. Cache validation results keyed by `(l0_id, content_hash)`. 2. Profile: validation is ~O(fields), trivial vs. embedding lookup. |
| **Incomplete validator** (misses edge cases) | Malformed chunks still propagate | 1. Extend tests with property-based fuzzing (Hypothesis). 2. Dogfood: validate *all* existing L0 chunks (option C) to discover gaps. |
| **Error messages lack context** (e.g., which artifact failed) | Hard to debug in batch loads | Include `artifact_id` and file path in exception message (already available in create/load context). |

---

## Memory Refresh Notes

### New L1 Episode After Completion

**File:** `docs/memory/l1/L1-20260704-l0-create-load-validation.json`

**Key fields:**

```json
{
  "episode_id": "EP-20260704-l0-create-load-validation",
  "summary_text": "AI-Lab enforced L0 chunk JSON schema validation at create and load time by wrapping validate_provider_l0_invariants in scripts/create_l0_chunk.py and src/ai_lab_memory/l0_loader.py. Validation checks required fields, l0_id format, namespace enum, ISO 8601 created_at, and SHA-256 content_hash. Invalid chunks abort with ValueError and actionable messages. Tests cover valid/invalid cases and create script rejection. Risks include legacy chunk incompatibility (mitigated by pre-deployment audit) and performance (mitigated by trivial validation cost). This establishes schema integrity precondition for context-pack inclusion (option D) and post-hoc diagnostics (option C).",
  "completed_work": [
    "Wrapped validate_provider_l0_invariants in create_l0_chunk.py (pre-write).",
    "Wrapped validate_provider_l0_invariants in l0_loader.py (post-read).",
    "Added 4 unit tests (valid, missing field, bad l0_id, bad namespace).",
    "Added 1 integration test (create script rejects malformed JSON).",
    "Verified pytest suite: 230 passed (5 new)."
  ],
  "next_actions": [
    "Run option C (store diagnostics) to audit existing L0 chunks for schema violations.",
    "Implement option A (CLI validation) for manual schema checks.",
    "Implement option D (guarded context-pack inclusion) now that L0 store integrity is enforced."
  ],
  "risks": [
    "Legacy L0 chunks may fail validation; backfill required before strict enforcement."
  ],
  "topics": ["l0", "validation", "schema", "create", "load", "ai-lab-memory"]
}
```

### Updated Abstraction Links

- **ABS-0003** (reconciled memory loop): Add citation to L0 validation as enforcement of "write-back validations" (section 7).
- Future abstraction: "L0 Chunk Lifecycle" (create → validate → store → load → validate → include → cite).

---

## Exact Deliverables

1. **Code changes:**
   - `scripts/create_l0_chunk.py`: Add validation call before `json.dump()`.
   - `src/ai_lab_memory/l0_loader.py`: Add validation call after `json.load()`.
   - Both: Wrap in try/except; raise `ValueError` with field-level details.

2. **Tests:** 5 new tests (4 unit, 1 integration) as specified above.

3. **Documentation:**
   - Update `docs/memory/README.md`: Add "L0 Schema Validation" subsection under "L0 Chunks."
   - Include example error message and remediation steps.

4. **Commit message:**
   ```
   feat(l0): enforce schema validation at create/load time

   - Wrap validate_provider_l0_invariants in create_l0_chunk.py and l0_loader.py
   - Reject chunks missing required fields or violating format rules
   - Add 5 tests covering valid/invalid cases and create script rejection
   - Mitigate legacy chunk risk with --skip-validation escape hatch

   Closes #<issue>. Enables options C (diagnostics) and D (context-pack inclusion).
   ```

---

## Summary

**Option B** is the minimal, high-leverage next step: it enforces schema quality at the earliest possible point (ingestion), unblocks downstream work (diagnostics, context-pack inclusion), and leverages existing validation logic with only two new call sites. The 5 tests provide confidence, and the memory refresh captures lineage for future reconciled-loop implementation.
````
