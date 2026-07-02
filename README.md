# AI-Lab

AI-Lab is a modular AI research environment built to support long-term, testable, and traceable research workflows.

Its first major purpose is to support RTG research by combining:

- provider-independent AI access,
- disciplined prompt construction,
- DSN-aware context selection,
- versioned research artifacts,
- tests,
- logs,
- comparison artifacts,
- and architectural decision records.

## Engineering Principles

1. No throwaway code.
2. Every development step must be testable.
3. Every important design must preserve its "why".
4. Main branch should remain working.
5. Secrets must never be committed.
6. RTG support is first-class, but implemented as a modular research layer.
7. Ontology precedes implementation.
8. AI-Lab should converge toward the underlying structure of the domain rather than inventing one.

## Current Status

- Python environment working.
- OpenAI provider verified.
- Claude provider verified.
- Provider-independent interface implemented.
- Provider comparison CLI implemented.
- Comparison artifacts can be saved as Markdown.
- Bootstrap EDGE record validator implemented.
- GitHub repository configured.
- SSH authentication configured.
- Initial config module and tests added.

## Local Setup

Run:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python -m pytest

## Local Secrets

API keys must be stored only in local git-ignored files.

Local secret files:

    api_key.txt
    claude_api_key.txt

Do not commit API keys.

## Provider Smoke Tests

Ask a single provider:

    python scripts/ask_provider.py openai "Reply with exactly: OpenAI provider works."
    python scripts/ask_provider.py claude "Reply with exactly: Claude provider works."

## Provider Comparison

Run the same prompt against OpenAI and Claude:

    python scripts/compare_providers.py "In one sentence, explain why immutable edge records help provenance."

Save a comparison as a Markdown artifact with an explicit path:

    python scripts/compare_providers.py \
      "In one sentence, explain why provider comparison should be saved as an artifact." \
      --save docs/comparisons/COMP-0001-provider-comparison-artifact.md

Save a comparison with an automatic COMP-XXXX ID:

    python scripts/compare_providers.py \
      "In one sentence, explain why automatic comparison IDs improve artifact discipline." \
      --title "Automatic Comparison IDs"

This creates the next available file under:

    docs/comparisons/

## EDGE Record Validation

Validate bootstrap EDGE records:

    python scripts/validate_edges.py

If no EDGE records exist yet, the script reports:

    No EDGE records found.

## Cognitive comparison workflow

AI-Lab now supports a small but complete reasoning loop over provider outputs.

The loop is:

    prompt
      -> provider comparison
      -> COMP artifact
      -> synthesis
      -> SYNCOMP artifact
      -> suggested re-ask prompt
      -> new provider comparison
      -> lineage/history inspection

The important discipline is that raw provider responses remain preserved.
Synthesis and re-ask outputs are derived artifacts, not replacements for the
original comparison.

### 1. Compare providers

Run the same prompt against OpenAI and Claude:

    python scripts/compare_providers.py \
      "In one sentence, explain why automatic comparison IDs improve artifact discipline." \
      --title "Automatic Comparison IDs"

This creates an artifact such as:

    docs/comparisons/COMP-0003-automatic-comparison-ids.md

### 2. Synthesize a comparison

Create a synthesis artifact from a saved comparison:

    python scripts/synthesize_comparison.py \
      docs/comparisons/COMP-0003-automatic-comparison-ids.md \
      --provider openai \
      --title "Automatic Comparison IDs"

This creates an artifact such as:

    docs/comparisons/syntheses/SYNCOMP-0001-automatic-comparison-ids.md

The synthesis records:

    synthesis_id
    source_comparison
    synthesizer_provider
    synthesizer_model
    synthesis response
    original source comparison

### 3. Re-ask from a synthesis

Extract the suggested re-ask prompt from a synthesis artifact and run a new
provider comparison:

    python scripts/reask_from_synthesis.py \
      docs/comparisons/syntheses/SYNCOMP-0001-automatic-comparison-ids.md \
      --title "Re-Ask Automatic Comparison IDs"

This creates a new comparison artifact such as:

    docs/comparisons/COMP-0004-re-ask-automatic-comparison-ids.md

The new comparison records:

    source_synthesis

so the reasoning chain is explicit.

To preview the extracted prompt without calling providers:

    python scripts/reask_from_synthesis.py \
      docs/comparisons/syntheses/SYNCOMP-0001-automatic-comparison-ids.md \
      --print-only

### 4. Inspect artifact history

Show all comparison and synthesis artifacts:

    python scripts/artifact_history.py

Show the lineage for a specific artifact:

    python scripts/artifact_history.py --lineage COMP-0004

Example lineage:

    COMP-0003 [COMP] Automatic Comparison IDs
      ↓ synthesized into
      SYNCOMP-0001 [SYNCOMP] Automatic Comparison IDs
        ↓ re-asked into
        COMP-0004 [COMP] Re-Ask Automatic Comparison IDs

### Design note: history must not become the prompt

The artifact history is expected to grow quickly. AI-Lab should not solve this
by loading all previous artifacts into every prompt.

Instead, history should be treated as indexed evidence. Future abstraction
artifacts should summarize selected sets of lower-level artifacts:

    raw artifacts
      -> abstraction level 1
      -> abstraction level 2
      -> ...
      -> abstraction level n

These levels do not need fixed cognitive names. They are generic compression,
summarization, and selection layers over prior artifacts.

A future prompt should retrieve only:

    relevant raw artifacts when needed
    nearest useful abstraction artifact
    lineage chain
    current task prompt

This keeps reasoning traceable without making every provider call slow,
expensive, or overloaded.

## Memory-aware context workflow

AI-Lab now supports budget-aware context packs for provider prompts and provider
comparisons.

The core flow is:

    artifact history
      -> latest-context selection
      -> token-budget filtering
      -> exclusion recording
      -> context pack manifest
      -> prompt-ready Markdown
      -> provider ask or provider comparison

The context pack system is designed to avoid loading all project history into
every prompt. It selects the latest useful abstraction, synthesis, and
comparison artifacts, then keeps only the items that fit within the requested
token budget.

Build a latest-context pack as JSON:

    python scripts/build_context_pack.py \
      "Prepare context for the next AI-Lab memory implementation step." \
      --token-budget 8000 \
      --model-target gpt-5

Build a prompt-ready Markdown context pack:

    python scripts/build_context_pack.py \
      "Prepare context for the next AI-Lab memory implementation step." \
      --token-budget 8000 \
      --model-target gpt-5 \
      --format markdown

Save a rendered context pack to a file:

    python scripts/build_context_pack.py \
      "Prepare context for the next AI-Lab memory implementation step." \
      --token-budget 8000 \
      --model-target gpt-5 \
      --format markdown \
      --output /tmp/ai_lab_context_pack.md

## Context-aware provider prompts

Ask one provider with a generated latest-context pack:

    python scripts/ask_provider.py openai \
      "What is the next safest implementation step for AI-Lab memory?" \
      --latest-context \
      --token-budget 8000 \
      --model-target gpt-5

Preview the final prompt without calling the provider:

    python scripts/ask_provider.py openai \
      "What is the next safest implementation step for AI-Lab memory?" \
      --latest-context \
      --token-budget 8000 \
      --model-target gpt-5 \
      --print-prompt

Ask one provider with a previously rendered context pack:

    python scripts/ask_provider.py openai \
      "What is the next safest implementation step for AI-Lab memory?" \
      --context-pack /tmp/ai_lab_context_pack.md

## Context-aware provider comparisons

Run a provider comparison with generated latest context:

    python scripts/compare_providers.py \
      "What is the next safest implementation step for AI-Lab memory?" \
      --latest-context \
      --token-budget 8000 \
      --model-target gpt-5 \
      --title "Next AI-Lab Memory Step"

Preview the final comparison prompt without calling providers:

    python scripts/compare_providers.py \
      "What is the next safest implementation step for AI-Lab memory?" \
      --latest-context \
      --token-budget 8000 \
      --model-target gpt-5 \
      --print-prompt

### Anti-bloat rule

Context-aware comparisons send the full rendered context pack to providers, but
saved comparison artifacts store only:

    raw user prompt
    context metadata
    provider responses

They do not save the full rendered context pack inside the comparison artifact.
This prevents recursive prompt/history growth.

## Memory implementation primitives

The current memory-related software primitives are:

    Citation
      exact evidence pointer in cid@version|span format

    ChunkReference
      deterministic span-bounded chunk identity

    L0ChunkSummary
      compact chunk-level retrieval summary

    ArtifactSummary
      artifact-level discovery record

    ContextPackManifest
      selected context items, scores, token estimates, and exclusions

    ContextPackRenderer
      prompt-ready Markdown rendering

These are intentionally small, testable building blocks. They provide a
foundation for future retrieval, indexing, summary refresh, and write-back
pipelines.
