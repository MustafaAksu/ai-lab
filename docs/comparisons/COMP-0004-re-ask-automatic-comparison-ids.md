# COMP-0004: Provider Comparison — Re-Ask Automatic Comparison IDs

## Metadata

- comparison_id: `COMP-0004`
- title: `Re-Ask Automatic Comparison IDs`
- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0001-automatic-comparison-ids.md`
- created_at: `2026-06-30T14:40:36.234957+00:00`
- command: `scripts/reask_from_synthesis.py docs/comparisons/syntheses/SYNCOMP-0001-automatic-comparison-ids.md --title Re-Ask Automatic Comparison IDs`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

In one sentence, explain how automatic, system-generated comparison IDs that uniquely link each artifact version to its exact code, data, and parameters improve artifact discipline, including how they ensure traceability and prevent mislabeling, collisions, drift, and version confusion.

## OpenAI Response

- model: `gpt-5`

```
By automatically generating unique comparison IDs that link each artifact version to its exact code, data, and parameters, the system enforces strong artifact discipline through end-to-end traceability and immutable provenance, while preventing mislabeling, ID collisions, configuration drift, and version confusion.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
Automatic, system-generated comparison IDs that cryptographically link each artifact version to its exact code, data, and parameters improve artifact discipline by ensuring perfect traceability (you can always trace back to the exact inputs that created an artifact), preventing mislabeling (humans can't accidentally assign wrong names), avoiding collisions (unique IDs guarantee no two different artifacts share the same identifier), eliminating drift (any change in code/data/parameters generates a new ID, making alterations immediately visible), and preventing version confusion (each unique combination gets its own immutable identifier, making it impossible to mistake one artifact version for another).
```
