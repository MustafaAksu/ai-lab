# AI-Lab Software Specification

## Purpose

AI-Lab is a modular research environment for long-running, traceable, and
testable AI-assisted research workflows.

Its current software purpose is to support:

- provider-independent model access,
- provider comparison,
- synthesis and re-ask loops,
- artifact history and lineage,
- generic abstraction artifacts,
- memory-aware context selection,
- budget-aware prompt construction,
- and anti-bloat research artifact generation.

AI-Lab is not a monolithic agent. It is a set of small tested primitives that can
be composed into increasingly capable research workflows.

## Core principles

1. Keep main branch working.
2. Preserve raw evidence.
3. Make derived artifacts explicit.
4. Keep context selection bounded.
5. Avoid recursive prompt/history growth.
6. Prefer small schemas over implicit conventions.
7. Add tests before relying on a workflow.
8. Keep provider-specific logic behind provider interfaces.

## Provider layer

The provider layer exposes a common interface for AI models.

Current providers:

- OpenAI
- Claude / Anthropic

Main files:

- `ai_lab/providers/provider.py`
- `ai_lab/providers/openai_provider.py`
- `ai_lab/providers/claude_provider.py`
- `ai_lab/providers/settings.py`

Provider scripts:

- `scripts/ask_provider.py`
- `scripts/compare_providers.py`

## Artifact model

AI-Lab records major reasoning steps as Markdown artifacts.

Current artifact families:

- `COMP-XXXX`: provider comparison artifacts
- `SYNCOMP-XXXX`: synthesized comparison artifacts
- `ABS-XXXX`: abstraction artifacts

Default locations:

- `docs/comparisons/`
- `docs/comparisons/syntheses/`
- `docs/abstractions/`

Artifact history and lineage are handled by:

- `ai_lab/documentation/artifact_history.py`
- `scripts/artifact_history.py`

## Reasoning workflow

The current reasoning loop is:

    prompt
      -> provider comparison
      -> COMP artifact
      -> synthesis
      -> SYNCOMP artifact
      -> re-ask prompt
      -> new COMP artifact
      -> abstraction
      -> ABS artifact
      -> latest-context seed

The important invariant is that each derived artifact preserves its source
relationship rather than replacing the source.

## Memory and context primitives

### Citation

A citation is an exact evidence pointer:

    cid@version|span

Examples:

    3ac9f2b1d0af@a1c2d3e|b:1024-2047
    3ac9f2b1d0af@a1c2d3e|t:10-40;tok=mistral-v3

Implemented in:

- `ai_lab/documentation/citations.py`

### ChunkReference

A chunk reference is a deterministic span-bounded memory unit.

It binds:

- artifact content ID,
- version,
- citation span,
- path,
- artifact type,
- language,
- embedding IDs,
- redaction level.

Implemented in:

- `ai_lab/documentation/chunk_reference.py`

### L0ChunkSummary

An L0 chunk summary is a compact retrieval summary for one chunk.

It contains:

- chunk reference,
- compact summary,
- keyphrases,
- entities,
- claims,
- risks,
- generator metadata,
- provenance metadata.

Implemented in:

- `ai_lab/documentation/l0_summary.py`

### ArtifactSummary

An artifact summary is a lightweight discovery record for an artifact.

It contains:

- artifact reference,
- path,
- artifact type,
- language,
- size,
- complexity score,
- tags,
- dependencies,
- synopsis,
- generator metadata,
- provenance metadata.

Implemented in:

- `ai_lab/documentation/artifact_summary.py`

### ContextPackManifest

A context pack manifest records the exact context selected for a task.

It contains:

- task,
- assembly policy,
- selected context items,
- relevance scores,
- token estimates,
- token budget,
- exclusions,
- model target,
- provenance metadata.

Implemented in:

- `ai_lab/documentation/context_pack.py`

### Context pack builder

The context pack builder turns artifact history into a selected manifest.

Current policy:

- `latest_context`

The latest-context policy selects the latest useful artifact per context level:

- latest abstraction level,
- latest synthesis,
- latest comparison.

It estimates token use, applies a budget, and records exclusions.

Implemented in:

- `ai_lab/documentation/context_pack_builder.py`
- `scripts/build_context_pack.py`

### Context pack renderer

The renderer turns a manifest into prompt-ready Markdown.

It marks source sections as context, not user instructions.

Implemented in:

- `ai_lab/documentation/context_pack_renderer.py`

### Prompt context helper

Reusable prompt-context logic is implemented in:

- `ai_lab/documentation/prompt_context.py`

It supports:

- reading rendered context packs,
- building latest-context packs,
- wrapping prompts with context.

## Context-aware command-line workflows

### Build context pack

JSON output:

    python scripts/build_context_pack.py \
      "Prepare context for the next AI-Lab memory implementation step." \
      --token-budget 8000 \
      --model-target gpt-5

Markdown output:

    python scripts/build_context_pack.py \
      "Prepare context for the next AI-Lab memory implementation step." \
      --token-budget 8000 \
      --model-target gpt-5 \
      --format markdown

Save output:

    python scripts/build_context_pack.py \
      "Prepare context for the next AI-Lab memory implementation step." \
      --token-budget 8000 \
      --model-target gpt-5 \
      --format markdown \
      --output /tmp/ai_lab_context_pack.md

### Ask one provider with context

    python scripts/ask_provider.py openai \
      "What is the next safest implementation step?" \
      --latest-context \
      --token-budget 8000 \
      --model-target gpt-5

Dry-run final prompt:

    python scripts/ask_provider.py openai \
      "What is the next safest implementation step?" \
      --latest-context \
      --token-budget 8000 \
      --model-target gpt-5 \
      --print-prompt

### Compare providers with context

    python scripts/compare_providers.py \
      "What is the next safest implementation step?" \
      --latest-context \
      --token-budget 8000 \
      --model-target gpt-5 \
      --title "Next AI-Lab Memory Step"

Dry-run final prompt:

    python scripts/compare_providers.py \
      "What is the next safest implementation step?" \
      --latest-context \
      --token-budget 8000 \
      --model-target gpt-5 \
      --print-prompt

## Anti-bloat invariant

Context-aware comparisons send the full rendered context pack to providers.

Saved comparison artifacts must not store the full rendered context pack.

They store:

- raw user prompt,
- context metadata,
- provider responses.

This prevents recursive growth where each new artifact embeds previous context
packs inside itself.

## Current limitations

AI-Lab does not yet provide:

- persistent vector indexing,
- BM25 retrieval,
- semantic retrieval,
- ACL-aware retrieval,
- summary refresh scheduling,
- automated write-back pipelines,
- chunk extraction from arbitrary documents,
- stable content-addressed artifact storage.

The current implementation establishes the tested primitives needed to build
those systems safely.

## Testing

Run the full test suite:

    pytest

The expected project discipline is:

- implement a small slice,
- run focused tests,
- run full tests,
- commit,
- push.
