# COMP-0008: Provider Comparison — AI-Lab Memory Next Step

## Metadata

- comparison_id: `COMP-0008`
- title: `AI-Lab Memory Next Step`
- context_policy: `latest_context`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0008-ai-lab-memory-next-step.context.json`
- created_at: `2026-07-02T09:46:38.789484+00:00`
- command: `scripts/compare_providers.py Given the current AI-Lab memory implementation, what is the next safest implementation step and what risk should be avoided? --latest-context --token-budget 8000 --model-target gpt-5 --title AI-Lab Memory Next Step`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Given the current AI-Lab memory implementation, what is the next safest implementation step and what risk should be avoided?

## OpenAI Response

- model: `gpt-5`

```
Next safest implementation step:
- Wire deny-by-default ACL and redaction into the retrieval → rerank → budgeting → prompt-assembly path, using namespaces and dual redacted/full representations. Enforce that every retrieval call, candidate, and final manifest item carries its namespace/access level, and only redacted text is eligible unless the caller’s clearance explicitly allows full text. Add a small validator that fails the build if any manifest item violates ACL or mixes representations.

Risk to avoid:
- Redaction/namespace leakage. Do not mix redacted and full-text (or their embeddings) across namespaces during retrieval or reranking. Leakage can occur if ACL is applied only at the end of selection; apply deny-by-default filtering before ranking/packing and keep it enforced through to prompt assembly.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
Based on the reconciled memory implementation context, here is the next safest implementation step and key risk to avoid:

## Next Safest Implementation Step

**Implement the L0 chunk-level summarization layer with standardized schema first**, before building selection or retrieval mechanisms.

Specifically:
1. Define and validate the `ChunkReference` schema with:
   - `chunk_id`, `artifact_id`, `version`
   - Span bounds (start/end positions)
   - Embedding reference (`embedding_id` + `embedding_namespace`)
   - Core metadata (embedding_model, embedding_dimension)
   
2. Establish the citation format validation: `cid@version|span`

3. Set up external embedding storage with namespace isolation

**Why this is safest:**
- L0 is the foundation that all other layers depend on (retrieval, L1 summaries, citations)
- Schema changes after building dependent systems are expensive
- The reconciled proposal has converged on chunk-level L0 as the standard
- Citation integrity validation requires L0 structure to be stable

## Critical Risk to Avoid

**Do NOT mix L0 granularity models** (chunk-level vs artifact-level) during implementation.

The context reveals a fundamental divergence:
- OpenAI's reconciled proposal: chunk-level L0 with precise spans
- Claude's approach: artifact-level "L0" without chunk boundaries

**Specific risks if not avoided:**
1. **Citation ambiguity**: Span-bounded citations (`cid@version|span`) become meaningless without chunk-level granularity
2. **Retrieval precision loss**: Cannot surface specific relevant passages, only whole artifacts
3. **Schema confusion**: Mixing both approaches creates incompatible data that cannot be reconciled later
4. **Validation failure**: Citation integrity checks specified in the reconciled plan require chunk-level spans

**Mitigation:** Explicitly commit to chunk-level L0 as the standard before writing any storage or indexing code. Document this decision as an ADR to prevent scope creep back to artifact-level summaries.
```
