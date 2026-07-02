# AI-Lab Library Index

This document is a quick navigation index for AI-Lab source files, scripts, and
tests.

## Top-level files

### `README.md`

Primary user-facing project guide.

Includes:

- setup,
- provider smoke tests,
- provider comparison workflow,
- synthesis / re-ask workflow,
- artifact history,
- memory-aware context workflow,
- context-aware provider commands.

### `requirements.txt`

Python dependencies.

### `pyproject.toml`

Pytest configuration and project tooling configuration.

## Provider modules

### `ai_lab/providers/provider.py`

Defines the provider interface.

Main concept:

- `Provider`

### `ai_lab/providers/openai_provider.py`

OpenAI provider implementation.

Main concept:

- `OpenAIProvider`

### `ai_lab/providers/claude_provider.py`

Claude / Anthropic provider implementation.

Main concept:

- `ClaudeProvider`

### `ai_lab/providers/settings.py`

Provider model defaults.

Current model constants:

- `OPENAI_MODEL`
- `CLAUDE_MODEL`

## Configuration modules

### `ai_lab/config.py`

Local configuration and secret loading helpers.

Main functions:

- `project_root`
- `read_local_secret`
- `read_api_key`
- `read_claude_api_key`

## Documentation and artifact modules

### `ai_lab/documentation/edge_validation.py`

Bootstrap EDGE record validation.

Main concepts:

- immutable edge-like research records,
- validation of required fields,
- validation of evidence and timestamps.

### `ai_lab/documentation/artifact_history.py`

Artifact discovery, metadata parsing, lineage, source trees, and latest-context
selection.

Main concepts:

- `ArtifactRecord`
- `discover_artifacts`
- `format_artifact_history`
- `format_artifact_lineage`
- `format_artifact_source_tree`
- `format_latest_context`
- `latest_records_by_context_level`

### `ai_lab/documentation/abstraction.py`

Creates abstraction prompts and abstraction artifacts from lower-level artifacts.

Main concepts:

- abstraction levels,
- compacting source artifacts,
- abstraction metadata,
- abstraction artifact generation.

### `ai_lab/documentation/citations.py`

Citation parsing and validation.

Main concepts:

- `CitationSpan`
- `Citation`
- `parse_citation`
- `format_citation`

Citation format:

    cid@version|span

### `ai_lab/documentation/chunk_reference.py`

Span-bounded deterministic chunk references.

Main concepts:

- `ChunkReference`
- `compute_chunk_id`
- `create_chunk_reference`

### `ai_lab/documentation/l0_summary.py`

Compact chunk-level retrieval summaries.

Main concepts:

- `L0ChunkSummary`
- `Entity`
- `Claim`
- `Risk`

### `ai_lab/documentation/artifact_summary.py`

Lightweight artifact-level discovery records.

Main concepts:

- `ArtifactSummary`
- `ArtifactDependency`

### `ai_lab/documentation/context_pack.py`

Context pack manifest schema.

Main concepts:

- `ContextPackManifest`
- `ContextPackItem`
- `ContextPackExclusion`
- `compute_manifest_id`

### `ai_lab/documentation/context_pack_builder.py`

Builds context pack manifests from artifact history.

Main concepts:

- `build_latest_context_manifest`
- `context_item_from_record`
- `select_items_with_budget`
- `estimate_tokens_for_text`
- `estimate_tokens_for_path`

### `ai_lab/documentation/context_pack_renderer.py`

Renders context pack manifests into prompt-ready Markdown.

Main concept:

- `render_context_pack_markdown`

### `ai_lab/documentation/prompt_context.py`

Reusable prompt-context helpers shared by provider and comparison CLIs.

Main concepts:

- `read_context_pack`
- `build_latest_context_pack_text`
- `build_prompt`

### `ai_lab/documentation/citations.py`

Citation format parser and formatter.

Main concepts:

- `Citation`
- `CitationSpan`
- `parse_citation`
- `format_citation`

## Scripts

### `scripts/ask_provider.py`

Ask one configured provider.

Supports:

- OpenAI,
- Claude,
- rendered context pack file,
- generated latest context,
- token budget,
- prompt dry-run.

Examples:

    python scripts/ask_provider.py openai "Hello"
    python scripts/ask_provider.py openai "Task" --latest-context --token-budget 8000
    python scripts/ask_provider.py openai "Task" --latest-context --print-prompt

### `scripts/compare_providers.py`

Run the same prompt against OpenAI and Claude.

Supports:

- saving comparison artifacts,
- automatic COMP IDs,
- rendered context pack file,
- generated latest context,
- token budget,
- prompt dry-run,
- anti-bloat artifact saving.

Examples:

    python scripts/compare_providers.py "Task"
    python scripts/compare_providers.py "Task" --title "My Comparison"
    python scripts/compare_providers.py "Task" --latest-context --token-budget 8000
    python scripts/compare_providers.py "Task" --latest-context --print-prompt

### `scripts/synthesize_comparison.py`

Synthesize a comparison artifact into a synthesis artifact.

Creates:

- `SYNCOMP-XXXX`

### `scripts/reask_from_synthesis.py`

Extract a re-ask prompt from a synthesis artifact and run a new comparison.

Creates:

- `COMP-XXXX`

### `scripts/artifact_history.py`

Inspect artifact history.

Supports:

- flat artifact list,
- lineage,
- source tree,
- latest-context seed view.

Examples:

    python scripts/artifact_history.py
    python scripts/artifact_history.py --lineage COMP-0007
    python scripts/artifact_history.py --source-tree ABS-0003
    python scripts/artifact_history.py --latest-context

### `scripts/create_abstraction.py`

Create an abstraction artifact from source artifacts.

Creates:

- `ABS-XXXX`

### `scripts/build_context_pack.py`

Build a context pack manifest.

Supports:

- JSON output,
- Markdown output,
- output files,
- latest-context policy,
- token budget,
- model target.

Examples:

    python scripts/build_context_pack.py "Task"
    python scripts/build_context_pack.py "Task" --format markdown
    python scripts/build_context_pack.py "Task" --token-budget 8000 --format markdown

### `scripts/validate_citation.py`

Validate citation strings from the command line.

### `scripts/validate_edges.py`

Validate bootstrap EDGE records.

## Artifact directories

### `docs/comparisons/`

Provider comparison artifacts.

Pattern:

    COMP-XXXX-title.md

### `docs/comparisons/syntheses/`

Synthesis artifacts derived from comparison artifacts.

Pattern:

    SYNCOMP-XXXX-title.md

### `docs/abstractions/`

Abstraction artifacts over lower-level artifacts.

Pattern:

    ABS-XXXX-title.md

## Tests

### Provider and config tests

- `tests/test_config.py`
- `tests/test_identity.py`
- `tests/test_openai_provider.py` if present
- `tests/test_claude_provider.py`

### Comparison workflow tests

- `tests/test_compare_providers.py`
- `tests/test_comparison_synthesis.py`
- `tests/test_reask.py`

### Artifact history tests

- `tests/test_artifact_history.py`
- `tests/test_artifact_lineage.py`
- `tests/test_artifact_source_tree.py`
- `tests/test_latest_context.py`

### Abstraction tests

- `tests/test_abstraction.py`

### Memory primitive tests

- `tests/test_citations.py`
- `tests/test_chunk_reference.py`
- `tests/test_l0_summary.py`
- `tests/test_artifact_summary.py`
- `tests/test_context_pack.py`
- `tests/test_context_pack_builder.py`
- `tests/test_context_pack_renderer.py`
- `tests/test_prompt_context.py`

### Provider prompt tests

- `tests/test_ask_provider.py`

### EDGE validation tests

- `tests/test_edge_validation.py`

### Research session tests

- `tests/test_research_session.py`

## Current architectural invariants

1. Provider implementations stay behind provider interfaces.
2. Raw comparison artifacts are preserved.
3. Synthesis, re-ask, and abstraction artifacts are derived artifacts.
4. Latest context is selected, not loaded wholesale.
5. Token budgets are enforced when provided.
6. Excluded context is recorded.
7. Rendered context is sent to providers but not recursively stored inside saved
   comparison artifacts.
8. CLI workflows should support dry-runs before expensive provider calls.
9. Every new implementation slice should have tests.
