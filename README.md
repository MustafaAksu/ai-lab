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
