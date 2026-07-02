# SYNCOMP-0004: Comparison Synthesis — AI-Lab Memory Next Step

## Metadata

- synthesis_id: `SYNCOMP-0004`
- title: `AI-Lab Memory Next Step`
- created_at: `2026-07-02T10:06:08.088667+00:00`
- command: `scripts/synthesize_comparison.py docs/comparisons/COMP-0008-ai-lab-memory-next-step.md --provider openai --title AI-Lab Memory Next Step`
- source_comparison: `docs/comparisons/COMP-0008-ai-lab-memory-next-step.md`
- synthesizer_provider: `OpenAI`
- synthesizer_model: `gpt-5`

## Synthesis

~~~text
1) Shared agreement
- Enforce strict data isolation via namespaces.
- Add validation gates early: schema/citation validation (Claude) and build-failing ACL/redaction checks (OpenAI).
- Safety-first sequencing to prevent leaks or integrity drift before scaling other features.

2) Meaningful differences
- Next step focus:
  - OpenAI: Wire deny-by-default ACL and redaction end-to-end in retrieval → rerank → budgeting → prompt assembly, with dual redacted/full representations and a validator.
  - Claude: Lock down the L0 chunk-level data model and citation schema first (ChunkReference, span bounds, embedding references), plus namespace-isolated embedding storage.
- Primary risk framing:
  - OpenAI: Redaction/namespace leakage if ACL is applied late or redacted/full text (or embeddings) are mixed.
  - Claude: Mixing L0 granularity models (chunk-level vs artifact-level) causing citation ambiguity and schema incompatibility.
- Context claim:
  - Claude asserts a divergence between chunk-level (OpenAI’s reconciled proposal) vs artifact-level (Claude’s earlier approach). OpenAI’s response does not address L0 granularity.

3) Stronger points from OpenAI
- Concrete, actionable guardrails in the serving path: deny-by-default filtering before ranking/packing, propagation of namespace/access level with every candidate, and a build-failing validator for manifest violations.
- Clear articulation of how leakage occurs (mixing redacted/full text or embeddings; applying ACL only at the end).

4) Stronger points from Claude
- Foundation-first: stabilize the L0 chunk-level schema, citations, and embedding namespace isolation to avoid expensive downstream rework.
- Specific schema elements and citation format that enable precise, span-bounded referencing and validation.

5) Combined answer
- Recommended next safest step (sequenced to satisfy both):
  1) Finalize and validate the L0 chunk-level schema and citation format (ChunkReference with chunk_id, artifact_id, version, span bounds, embedding refs/namespace/metadata). Record the decision (e.g., ADR). Add citation integrity validation (cid@version|span).
  2) Set up namespace-isolated embedding storage consistent with the L0 spec.
  3) Wire deny-by-default ACL and redaction through retrieval → rerank → budgeting → prompt assembly:
     - Propagate namespace/access level on every retrieval result and manifest item.
     - Use redacted text by default; allow full text only with explicit clearance.
     - Keep redacted and full-text (and their embeddings) in separate representations; never mix across namespaces.
  4) Add validators:
     - Schema/citation integrity checks at ingest.
     - A build-failing manifest validator that rejects any ACL violations or mixed representations.
- This path locks the data model foundation (Claude) and prevents leakage in the serving pipeline (OpenAI).

6) Risks or missing assumptions
- If L0 granularity is not explicitly decided, teams may mix artifact-level and chunk-level data (Claude’s risk).
- If ACL/redaction is enforced only after ranking/packing, sensitive content can leak via candidates or embeddings (OpenAI’s risk).
- Unclear current state of L0 implementation and retrieval pipeline may affect which step is truly “next” (inference).

7) Suggested re-ask prompt
Given our current AI-Lab memory state, which of these is already implemented and which is not: (a) chunk-level L0 schema with span-bounded citations, (b) namespace-isolated embedding storage, (c) deny-by-default ACL/redaction enforced before ranking/packing, and (d) build-failing validators for schema/citation integrity and ACL/representation mixing? Based on your answer, propose the immediate next implementation step with concrete acceptance tests and failure modes to guard against both granularity mixing and redaction/namespace leakage.
~~~

## Source Comparison

~~~markdown
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

~~~
