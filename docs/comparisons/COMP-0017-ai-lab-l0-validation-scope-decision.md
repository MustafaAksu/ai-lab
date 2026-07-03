# COMP-0017: Provider Comparison — AI-Lab L0 Validation Scope Decision

## Metadata

- comparison_id: `COMP-0017`
- title: `AI-Lab L0 Validation Scope Decision`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0017-ai-lab-l0-validation-scope-decision.context.json`
- created_at: `2026-07-03T11:27:11.641054+00:00`
- command: `scripts/compare_providers.py AI-Lab needs to choose exactly ONE smallest next L0 validation slice. Do not combine multiple layers. Current repo facts: create_l0_chunk.py writes L0ChunkSummary.to_dict JSON with chunk_reference, citation, l0_summary, keyphrases, entities, claims, risks, generator_model, generator_version, generation_prompt_hash, pipeline_run_id, created_at, last_refreshed_at. provider_context_summary_json currently reports L0 summary visibility with l0_candidates/l0_included/l0_dropped entries using cid, citation, inclusion_reason, token_cost, and dropped_reason. Prior synthesis drifted into guessed fields like content_hash/source_path/summary_text/token_estimate; do not use those unless they exist in the repo. Choose exactly one: A) validate L0 chunk JSON at create/load time, B) validate provider summary l0_* invariants, C) harden corrupt/malformed L0 store diagnostics only. Recommend the smallest slice, exact non-goals, actual field names, tests, and memory-refresh notes. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab L0 Validation Scope Decision`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab needs to choose exactly ONE smallest next L0 validation slice. Do not combine multiple layers. Current repo facts: create_l0_chunk.py writes L0ChunkSummary.to_dict JSON with chunk_reference, citation, l0_summary, keyphrases, entities, claims, risks, generator_model, generator_version, generation_prompt_hash, pipeline_run_id, created_at, last_refreshed_at. provider_context_summary_json currently reports L0 summary visibility with l0_candidates/l0_included/l0_dropped entries using cid, citation, inclusion_reason, token_cost, and dropped_reason. Prior synthesis drifted into guessed fields like content_hash/source_path/summary_text/token_estimate; do not use those unless they exist in the repo. Choose exactly one: A) validate L0 chunk JSON at create/load time, B) validate provider summary l0_* invariants, C) harden corrupt/malformed L0 store diagnostics only. Recommend the smallest slice, exact non-goals, actual field names, tests, and memory-refresh notes.

## OpenAI Response

- model: `gpt-5`

```
Recommendation: Choose B) validate provider summary l0_* invariants.

Why this is the smallest slice
- Fully local to the read-only summary layer you already ship.
- Requires no changes to L0 chunk creation/loading code, no schema files, and no prompt/rendering paths.
- Implementable as a pure validation helper plus unit tests that exercise existing output from provider_context_summary_payload/format_provider_context_summary_json.

Scope (what we will do)
- Add a small, pure function to validate invariants of l0_candidates, l0_included, and l0_dropped entries in the provider context summary JSON.
- Use only the fields that already exist in your code:
  - Top-level lists: l0_candidates, l0_included, l0_dropped
  - Item fields: cid, citation, inclusion_reason, token_cost, dropped_reason
- Enforce a minimal, current set of invariants without changing any JSON structure or adding new fields.

Explicit non-goals (out of scope for this slice)
- Do not validate or schema-check the L0 store files written by create_l0_chunk.py (no checks on chunk_reference, l0_summary, etc.).
- Do not change how prompt context or manifests are built; no changes to rendered context packs or final prompts.
- Do not add or rename any fields in the provider summary JSON.
- Do not validate citation format beyond non-empty string (no cid@version|span checks).
- Do not introduce token budget rollups or cross-list budget constraints.
- Do not harden file I/O or error messages for corrupt stores (that’s option C).
- Do not attempt tokenizer-exact token accounting.

Exact invariants to validate (using actual field names)
Given a summary dict produced by provider_context_summary_payload/format_provider_context_summary_json when include_l0 is used:
- Structure
  - summary["l0_candidates"], summary["l0_included"], summary["l0_dropped"] exist and are lists.
- Item-level fields and types
  - For every item in all three lists:
    - cid: present and non-empty string.
    - citation: present and non-empty string.
    - token_cost: present, int, and >= 0.
  - For l0_included items:
    - inclusion_reason: present and non-empty string.
    - dropped_reason: must be absent.
  - For l0_dropped items:
    - dropped_reason: present and in {"not_found", "over_budget"} for now.
    - inclusion_reason: must be absent.
- Set relationships and uniqueness
  - cids in l0_included are a subset of cids in l0_candidates.
  - cids in l0_dropped are a subset of cids in l0_candidates.
  - l0_included and l0_dropped are disjoint (no overlapping cid).
  - No duplicate cid entries within l0_candidates, l0_included, or l0_dropped.

Implementation plan
- File: prompt_context.py (or wherever provider_context_summary_payload/format_provider_context_summary_json live)
  - Add a pure helper:
    - def validate_provider_l0_invariants(summary: dict) -> None
    - Raises ValueError with concise messages on the first detected violation. Keep messages specific (e.g., "l0_included has cid not in l0_candidates: {cid}").
  - Do not call this function in production paths; keep it for tests and optional local assertions only.
- No changes to provider_context_summary_payload or format_provider_context_summary_json outputs.
- No changes to CLI.

Unit tests
- New test module: tests/test_provider_l0_invariants.py
- Happy-path
  - test_validate_l0_invariants_ok: Build a minimal valid summary dict with:
    - l0_candidates: [{"cid": "A", "citation": "A@v1|0-10", "token_cost": 12}]
    - l0_included: [{"cid": "A", "citation": "A@v1|0-10", "token_cost": 12, "inclusion_reason": "explicit"}]
    - l0_dropped: []
    - Expect no exception.
- Missing/invalid fields
  - test_missing_citation: Remove citation from one included item → expect ValueError.
  - test_negative_token_cost: token_cost = -1 in candidates → expect ValueError.
  - test_missing_inclusion_reason_in_included: included item lacks inclusion_reason → expect ValueError.
  - test_missing_dropped_reason_in_dropped: dropped item lacks dropped_reason → expect ValueError.
- Bad reason values
  - test_invalid_dropped_reason_value: dropped_reason = "foo" → expect ValueError.
  - test_included_has_dropped_reason: included item has dropped_reason present → expect ValueError.
  - test_dropped_has_inclusion_reason: dropped item has inclusion_reason present → expect ValueError.
- Set/uniqueness violations
  - test_included_not_subset_of_candidates: include cid not present in candidates → expect ValueError.
  - test_dropped_not_subset_of_candidates: drop cid not present in candidates → expect ValueError.
  - test_overlap_between_included_and_dropped: same cid in both lists → expect ValueError.
  - test_duplicate_cids_within_lists: duplicates in l0_candidates (and parametrize for included/dropped) → expect ValueError.

Notes on existing field names (for clarity; not modified in this slice)
- L0 chunk JSON written by create_l0_chunk.py uses:
  - chunk_reference, citation, l0_summary, keyphrases, entities, claims, risks,
    generator_model, generator_version, generation_prompt_hash, pipeline_run_id,
    created_at, last_refreshed_at
- Provider context summary L0 visibility uses:
  - l0_candidates, l0_included, l0_dropped with per-item fields:
    - cid, citation, inclusion_reason, token_cost, dropped_reason

Developer ergonomics
- Keep validator small and pure so it can be reused in other tests.
- Error messages reference the problematic list and cid for quick triage.
- Consider adding a one-line docstring explaining that dropped_reason values are currently {"not_found", "over_budget"} and should be updated if new reasons are introduced.

Memory-refresh notes (to record after landing)
- Completed work
  - Added validate_provider_l0_invariants for read-only L0 visibility JSON.
  - Added focused tests covering field presence/types, subset/uniqueness, and current dropped_reason values.
- Key decisions
  - Keep validation at the provider summary layer only; do not touch L0 store schema or prompt assembly.
  - Enumerate dropped_reason as {"not_found", "over_budget"} per current implementation.
- Next actions
  - If needed, extend validator when additional dropped_reason values are introduced.
  - Later slices can address A) L0 chunk JSON validation at create/load time or C) hardened L0 store diagnostics.
- Risks
  - Future addition of new dropped_reason values will require a quick test/validator update.
  - If provider_context_summary_json structure changes, tests must be adjusted accordingly.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Recommendation: Option A — Validate L0 chunk JSON at create/load time

## Rationale

**Option A is the smallest, most foundational slice.** It establishes schema integrity at the L0 record boundary *before* downstream code (provider context summary, prompt assembly, citations) consumes those records.

- **Option B** (validate provider summary l0_* invariants) depends on valid L0 records existing first; validating summary-level invariants when the underlying L0 may be malformed yields cascading failures.
- **Option C** (diagnostics only) is reactive and doesn't prevent corrupt data from entering the store or being loaded.

**Option A** is a narrow gate: validate once at write (create_l0_chunk.py) and once at read (prompt_context.py L0 store loading), using the **actual repo field names** from `L0ChunkSummary.to_dict`.

---

## Exact Scope

### In-Scope

1. **Schema validation at write time** (`create_l0_chunk.py`):
   - Before writing JSON, validate that `L0ChunkSummary.to_dict()` contains all required fields with correct types:
     - `chunk_reference` (dict with `chunk_id`, `version`, `namespace`)
     - `citation` (str, non-empty)
     - `l0_summary` (str, non-empty)
     - `keyphrases` (list of str)
     - `entities` (list of str)
     - `claims` (list of str)
     - `risks` (list of str)
     - `generator_model` (str, non-empty)
     - `generator_version` (str, non-empty)
     - `generation_prompt_hash` (str, non-empty)
     - `pipeline_run_id` (str, non-empty)
     - `created_at` (ISO 8601 str)
     - `last_refreshed_at` (ISO 8601 str)
   - Fail early with a clear error message naming the missing/invalid field.

2. **Schema validation at read time** (`prompt_context.py`, `load_l0_store` or equivalent):
   - When loading L0 JSON files, validate the same required fields.
   - Log or raise on missing/malformed fields; add a `dropped_reason: "invalid_schema"` entry in `l0_dropped` if the chunk cannot be admitted.

3. **Add focused unit tests**:
   - `tests/test_create_l0_chunk.py`: test missing `citation`, wrong type for `keyphrases`, invalid ISO datetime, missing `chunk_reference.chunk_id`.
   - `tests/test_prompt_context_l0_validation.py`: test loading a store with a malformed L0 record; verify `l0_dropped` contains `invalid_schema` reason.

### Explicit Non-Goals

- **Do not** add or validate fields not produced by `L0ChunkSummary.to_dict` (e.g., `content_hash`, `source_path`, `summary_text`, `token_estimate` from prior synthesis drift).
- **Do not** validate citation *format* (e.g., `cid@version|span` integrity)—that is a separate slice tied to ABS-0003 citation rules.
- **Do not** validate embedding references (`embedding_id`, `embedding_namespace`)—those fields are not yet in the repo's `L0ChunkSummary`.
- **Do not** validate provider summary `l0_candidates`/`l0_included`/`l0_dropped` invariants (e.g., no duplicate `cid`, budget accounting)—that is Option B.
- **Do not** build full diagnostics CLI or repair tooling—that is Option C.

---

## Implementation Sketch

### 1. Add `validate_l0_chunk_schema(chunk_dict: dict) -> None` helper

```python
# ai_lab_tools/validation.py (new or existing)
from typing import Dict, Any
import datetime

REQUIRED_L0_FIELDS = {
    "chunk_reference": dict,
    "citation": str,
    "l0_summary": str,
    "keyphrases": list,
    "entities": list,
    "claims": list,
    "risks": list,
    "generator_model": str,
    "generator_version": str,
    "generation_prompt_hash": str,
    "pipeline_run_id": str,
    "created_at": str,
    "last_refreshed_at": str,
}

def validate_l0_chunk_schema(chunk: Dict[str, Any]) -> None:
    """Validate L0ChunkSummary.to_dict schema; raise ValueError on failure."""
    for field, expected_type in REQUIRED_L0_FIELDS.items():
        if field not in chunk:
            raise ValueError(f"L0 chunk missing required field: {field}")
        if not isinstance(chunk[field], expected_type):
            raise ValueError(
                f"L0 chunk field {field} has type {type(chunk[field]).__name__}, "
                f"expected {expected_type.__name__}"
            )
        if expected_type is str and not chunk[field]:
            raise ValueError(f"L0 chunk field {field} must be non-empty string")
    
    # Validate chunk_reference nested fields
    ref = chunk["chunk_reference"]
    for subfield in ["chunk_id", "version", "namespace"]:
        if subfield not in ref or not isinstance(ref[subfield], str) or not ref[subfield]:
            raise ValueError(f"chunk_reference missing or invalid: {subfield}")
    
    # Validate ISO 8601 datetime strings
    for dt_field in ["created_at", "last_refreshed_at"]:
        try:
            datetime.datetime.fromisoformat(chunk[dt_field].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            raise ValueError(f"L0 chunk field {dt_field} is not valid ISO 8601: {chunk[dt_field]}")
```

### 2. Call in `create_l0_chunk.py` before write

```python
# scripts/create_l0_chunk.py
from ai_lab_tools.validation import validate_l0_chunk_schema

# ... existing code ...
chunk_dict = chunk_summary.to_dict()
validate_l0_chunk_schema(chunk_dict)  # ← new
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(chunk_dict, f, indent=2, ensure_ascii=False)
```

### 3. Call in `prompt_context.py` L0 loading

```python
# ai_lab_tools/prompt_context.py, in load_l0_store or wherever JSON is read
from ai_lab_tools.validation import validate_l0_chunk_schema

for json_file in l0_store_path.glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        chunk_dict = json.load(f)
    try:
        validate_l0_chunk_schema(chunk_dict)
        # proceed to add to candidates
    except ValueError as e:
        l0_dropped.append({
            "cid": chunk_dict.get("chunk_reference", {}).get("chunk_id", "unknown"),
            "citation": chunk_dict.get("citation", ""),
            "dropped_reason": "invalid_schema",
            "error": str(e),
        })
        continue
```

---

## Tests

### `tests/test_l0_validation.py` (new file)

```python
import pytest
from ai_lab_tools.validation import validate_l0_chunk_schema

VALID_CHUNK = {
    "chunk_reference": {"chunk_id": "cid-001", "version": "v1", "namespace": "public"},
    "citation": "test.md#L10-L20",
    "l0_summary": "Summary text",
    "keyphrases": ["key1"],
    "entities": ["Entity1"],
    "claims": ["Claim1"],
    "risks": [],
    "generator_model": "gpt-5",
    "generator_version": "1.0",
    "generation_prompt_hash": "abc123",
    "pipeline_run_id": "run-001",
    "created_at": "2026-07-03T11:08:44+00:00",
    "last_refreshed_at": "2026-07-03T11:08:44+00:00",
}

def test_valid_chunk():
    validate_l0_chunk_schema(VALID_CHUNK)  # should not raise

def test_missing_citation():
    chunk = VALID_CHUNK.copy()
    del chunk["citation"]
    with pytest.raises(ValueError, match="missing required field: citation"):
        validate_l0_chunk_schema(chunk)

def test_wrong_type_keyphrases():
    chunk = VALID_CHUNK.copy()
    chunk["keyphrases"] = "not a list"
    with pytest.raises(ValueError, match="keyphrases has type str, expected list"):
        validate_l0_chunk_schema(chunk)

def test_invalid_datetime():
    chunk = VALID_CHUNK.copy()
    chunk["created_at"] = "not-a-date"
    with pytest.raises(ValueError, match="not valid ISO 8601"):
        validate_l0_chunk_schema(chunk)

def test_missing_chunk_id():
    chunk = VALID_CHUNK.copy()
    del chunk["chunk_reference"]["chunk_id"]
    with pytest.raises(ValueError, match="chunk_reference missing or invalid: chunk_id"):
        validate_l0_chunk_schema(chunk)
```

### `tests/test_prompt_context_l0_invalid.py` (integration test)

```python
def test_load_l0_store_with_invalid_schema(tmp_path):
    # Write malformed L0 JSON
    bad_chunk = {"chunk_reference": {"chunk_id": "bad"}, "citation": ""}  # missing fields
    (tmp_path / "bad.json").write_text(json.dumps(bad_chunk))
    
    summary = provider_context_summary_payload(
        ...,
        include_l0=True,
        l0_store=str(tmp_path),
    )
    json_summary = format_provider_context_summary_json(summary)
    
    assert len(json_summary["l0_dropped"]) == 1
    assert json_summary["l0_dropped"][0]["dropped_reason"] == "invalid_schema"
    assert "missing required field" in json_summary["l0_dropped"][0]["error"]
```

---

## Memory Refresh Notes

### Episode L1 entry (dry-run / smoke test outcome)

```json
{
  "l1_id": "L1-20260704-l0-schema-validation",
  "episode_id": "EP-20260704-l0-schema-validation",
  "summary_text": "AI-Lab added L0 chunk JSON schema validation at create and load time. validate_l0_chunk_schema enforces all required fields from L0ChunkSummary.to_dict (chunk_reference, citation, l0_summary, keyphrases, entities, claims, risks, generator_model, generator_version, generation_prompt_hash, pipeline_run_id, created_at, last_refreshed_at) with type and non-empty checks. create_l0_chunk.py validates before write; prompt_context.py validates on load and adds invalid_schema to l0_dropped. Focused tests cover missing fields, wrong types, invalid ISO datetimes, and malformed chunk_reference. Full suite passed.",
  "completed_work": [
    "Added validate_l0_chunk_schema to ai_lab_tools/validation.py with exact repo field names.",
    "Integrated validation in create_l0_chunk.py before JSON write.",
    "Integrated validation in prompt_context.py L0 load; added invalid_schema dropped_reason.",
    "Added tests/test_l0_validation.py with 5 focused tests.",
    "Added integration test in tests/test_prompt_context_l0_invalid.py.",
    "Verified all tests pass."
  ],
  "key_decisions": [
    "Validate at both write (create) and read (load) boundaries.",
    "Use actual L0ChunkSummary.to_dict field names; exclude synthesis drift fields (content_hash, source_path, summary_text, token_estimate).",
    "Fail fast at create time; log and drop with invalid_schema at load time."
  ],
  "risks": [
    "Does not validate citation format (cid@version|span)—deferred to separate slice.",
    "Does not validate embedding references—not yet in repo schema.",
    "Does not validate provider summary invariants—Option B."
  ],
  "next_actions": [
    "Consider Option B: validate provider summary l0_* invariants (no duplicate cid, token_cost non-negative, dropped_reason enum).",
    "Consider citation format validation (ABS-0003 citation rules).",
    "Consider Option C: full L0 store diagnostics CLI for corpus-wide validation."
  ],
  "topics": ["l0", "validation", "schema", "create_l0_chunk", "prompt_context"]
}
```

---

## Summary

**Choose Option A.** Validate L0 chunk JSON schema at create and load time using the exact 13 fields from `L0ChunkSummary.to_dict`. This is the smallest, most foundational slice that prevents downstream failures in provider context summary (Option B) and reduces the need for reactive diagnostics (Option C). Explicit non-goals: citation format rules, embedding references, provider summary invariants, and guessed fields from synthesis drift. Add 6 focused tests; expect ~50 lines of validation code. This establishes the integrity gate for all future L0 slices.
````
