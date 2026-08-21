# COMP-0141: Provider Comparison — PLAN-20260817-0002 deliberate establishment run

## Metadata

- comparison_id: `COMP-0141`
- title: `PLAN-20260817-0002 deliberate establishment run`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-bf521665213e8e83.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0141", "target_id": "INV-bf521665213e8e83"}, {"authoritative": false, "evidence": "docs/invocations/INV-9d3f9a646709af76.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0141", "target_id": "INV-9d3f9a646709af76"}]`
- created_at: `2026-08-21T07:12:28.361533+00:00`
- command: `scripts/compare_providers.py State the single-source principle for evidence binding in one paragraph. --title PLAN-20260817-0002 deliberate establishment run`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

State the single-source principle for evidence binding in one paragraph.

## OpenAI Response

- model: `gpt-5.6-terra`
- invocation_id: `INV-bf521665213e8e83`

```
The single-source principle for evidence binding requires that each evidentiary claim, datum, or conclusion be traceable to one clearly identified authoritative source of record, rather than being assembled from ambiguous, duplicated, or conflicting materials. The binding must preserve the source’s identity, provenance, version, integrity, and relevant context—typically through stable references, timestamps, hashes, or equivalent controls—so that a reviewer can independently verify exactly what source supports the claim. Any extracts, summaries, transformations, or derivative analyses must remain explicitly linked to that original source and must not be treated as independent evidence.
```

## Claude Response

- model: `claude-sonnet-5`
- invocation_id: `INV-9d3f9a646709af76`

```
# The Single-Source Principle for Evidence Binding

The single-source principle holds that any given piece of evidence, data, or factual claim within a system should be bound to one authoritative origin point, rather than being duplicated, re-derived, or independently asserted across multiple locations. When evidence must be referenced in multiple contexts—whether in documentation, code, reports, or decision-making processes—those references should point back to (or be traceably derived from) that single canonical source rather than existing as separate, potentially divergent copies. This matters because when the same fact is captured or restated in multiple places, those copies can drift out of sync as the underlying reality changes, creating ambiguity about which version is authoritative and increasing the risk of contradictions going undetected. By binding evidence to a single source of truth, systems maintain consistency, simplify verification and auditing (since there's only one place to check or update), and make provenance clear—anyone consuming the evidence can trace it back to where it originated and assess its reliability. In practice, this often means using references, pointers, or citations to the original source rather than copy-pasting or re-stating facts, and it underlies good practices in software engineering (e.g., "don't repeat yourself"), scientific reporting (citing primary sources), and knowledge management systems more broadly.
```
