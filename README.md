# AI-Lab

AI-Lab is a modular AI research environment built to support long-term, testable, and traceable research workflows.

Its first major purpose is to support RTG research by combining:
- provider-independent AI access,
- disciplined prompt construction,
- DSN-aware context selection,
- versioned research artifacts,
- tests,
- logs,
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
- OpenAI API call verified.
- GitHub repository configured.
- SSH authentication configured.
- Initial config module and tests added.

## Local Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest
