# ABS-0003: Abstraction — AI-Lab Reconciled Memory Implementation Loop

## Metadata

- abstraction_id: `ABS-0003`
- title: `AI-Lab Reconciled Memory Implementation Loop`
- abstraction_level: `1`
- source_artifacts: `docs/comparisons/COMP-0006-re-ask-ai-lab-scalable-memory-implementation.md, docs/comparisons/syntheses/SYNCOMP-0003-ai-lab-scalable-memory-implementation.md, docs/comparisons/COMP-0007-re-ask-ai-lab-reconciled-memory-implementation.md`
- created_at: `2026-06-30T18:36:59.572342+00:00`
- command: `scripts/create_abstraction.py docs/comparisons/COMP-0006-re-ask-ai-lab-scalable-memory-implementation.md docs/comparisons/syntheses/SYNCOMP-0003-ai-lab-scalable-memory-implementation.md docs/comparisons/COMP-0007-re-ask-ai-lab-reconciled-memory-implementation.md --title AI-Lab Reconciled Memory Implementation Loop --level 1 --provider openai`
- abstracter_provider: `OpenAI`
- abstracter_model: `gpt-5`

## Source Artifacts

- `docs/comparisons/COMP-0006-re-ask-ai-lab-scalable-memory-implementation.md`
- `docs/comparisons/syntheses/SYNCOMP-0003-ai-lab-scalable-memory-implementation.md`
- `docs/comparisons/COMP-0007-re-ask-ai-lab-reconciled-memory-implementation.md`

## Abstraction

~~~text
Abstraction level: 1

1) Stable claims
- Two-layer summarization exists across providers:
  - Lower-level unit used for retrieval and context (OpenAI: chunk-level L0; Claude: artifact-level summary). Both tie embeddings to summaries and track model metadata.
  - Episode-level summary is captured (both).
- Context Pack Manifest is assembled per prompt, capturing:
  - Rule-based/mandatory inclusions and retrieval-based inclusions separately.
  - Token budget allocations and request/user/session metadata.
- Selection considers explicit references and dependencies; hybrid retrieval is used (BM25 + dense) with reranking in the more detailed plan.
- Refresh triggers exist for summaries (content/dependency changes, staleness/TTL, manual, model changes).
- A reconciled proposal exists that standardizes:
  - L0 as chunk-level with span bounds and a mandatory citation format cid@version|span.
  - Embeddings referenced by embedding_id and namespace (vectors external), with embedding_model and embedding_dimension in metadata.
  - A full per-prompt selection algorithm combining rule-based seeding, hybrid retrieval, reranking, ACL filtering, dedup, novelty handling, and token budgeting.
  - Access control via namespaces and deny-by-default filtering, with dual redacted/full text handling.
  - A write-back pipeline with micro-summaries/ADR generation, embeddings, lineage, index updates, and validations.

2) Important distinctions
- Granularity of L0:
  - OpenAI: chunk-level with precise spans, keyphrases/entities/claims/risks; enables span-bounded citations.
  - Claude: artifact-level “ArtifactSummary” (no chunk_id/span in provided excerpt).
- Citations:
  - OpenAI: mandatory cid@version|span with span unit rules and validation.
  - Claude: no citation format specified.
- Embeddings:
  - OpenAI: stored externally; records carry embedding_id + embedding_namespace.
  - Claude: vectors inline with model/dimension in records.
- Access control/redaction:
  - OpenAI: ABAC + namespaces; dual redacted/full representations; redaction maps; enforced during retrieval and prompt assembly.
  - Claude: not covered in the excerpt.
- Selection/budgeting detail:
  - OpenAI: explicit algorithmic steps, boosts/penalties, default percentage budgets tied to context window.
  - Claude: manifest fields plus fixed numeric budget example (total 8000) and per-item priority; fewer algorithmic details.
- L1 scope:
  - OpenAI: artifact-level L1 and episode L1 with links to L0.
  - Claude: episode L1 with operational telemetry (tokens_used, duration, model_used), no artifact L1 in excerpt.
- Write-back and validation:
  - OpenAI: fully specified pipeline and checks (schema, citation integrity, ACL/DLP, coverage, idempotency).
  - Claude: references MicroSummary/code snippets; lacks full pipeline/validations in excerpt.

3) Unsupported strengthenings or risks
- L0 meaning divergence:
  - Risk: Claude’s artifact-level “L0” vs OpenAI’s chunk-level L0 can cause ambiguity. The reconciled plan selects chunk-level L0, but this is a provider proposal, not a project truth.
- Token budget policy mismatch:
  - Percentage-of-context (OpenAI) vs fixed-total defaults (Claude). Without harmonization, allocations may be inconsistent across models.
- Embedding storage mismatch:
  - Inline (Claude) vs referenced external vectors (OpenAI). Consolidation choice affects storage size and dereference complexity.
- Dependency handling:
  - Claude lists dependencies as IDs; OpenAI proposes graph traversal with depth/centrality. Integration details may be underspecified.
- Validation/refresh coupling:
  - Claude mentions “failed validation” as a refresh trigger; exact failure conditions are only fully defined in OpenAI’s validations.
- Redaction fidelity:
  - Dual embeddings/text per clearance level (OpenAI) introduces operational complexity; incorrect namespace use risks leakage.
- Span reproducibility:
  - Token-based spans require strict tokenizer versioning; mixing span units may complicate validation. This is specified by OpenAI but unaddressed by Claude.

4) Useful compression
- Minimal loop (shared/reconciled view):
  - Input: user request + episode context + ACL.
  - Selection: seed with explicit refs and dependencies; add domain/time heuristics; hybrid retrieval (BM25 + dense) → rerank → ACL filter → dedup/overlap control → novelty fill.
  - Budgeting: allocate context by policy (OpenAI: percentages; Claude: fixed 8k default), pack explicit/dependency/L1/L0 to meet budgets.
  - Prompt: assemble with inline citations in cid@version|span format.
  - Output: answer with citations.
  - Write-back: generate micro-summaries/L1, ADR (if applicable), embeddings; update lineage and indices.
  - Validate: schema, citation integrity, ACL/DLP, coverage, idempotency; pin versions/manifests for reproducibility.
- Key schema anchors worth reopening for implementation:
  - OpenAI (COMP-0006): exact L0/L1 fields, manifest structure with rules/candidate_set/ranking/inclusions, ACL/redaction, write-back, validations, end-to-end example.
  - Reconciled (COMP-0007, OpenAI): ChunkReference schema, finalized citation rules, manifest item priority/inclusion_reason, budgeting defaults (15% system, 10% answer, 75% context with 40/45/10/5 split), end-to-end example.
  - Synthesis (SYNCOMP-0003): side-by-side agreements/differences and integration risks.
  - Claude (both COMPs): lightweight ArtifactSummary/EpisodeSummary fields, fixed token budget default (8000), priority and temporal inclusion_reason examples.

5) Retrieval hints
- For citation rules, span units, and integrity checks: open COMP-0006 (OpenAI, sections 2.1 and validations) and COMP-0007 (OpenAI, citations section).
- For per-prompt selection algorithm, boosts/penalties, and budgeting percentages: open COMP-0006 (OpenAI, section 3) and COMP-0007 (OpenAI, selection and default budgets).
- For ACL, namespaces, and redaction strategies: open COMP-0006 (OpenAI, section 5) and COMP-0007 (OpenAI, access control and redaction).
- For schemas:
  - Chunk-level L0, artifact L1, episode L1, manifest fields: open COMP-0006 (OpenAI).
  - ChunkReference and reconciled embedding metadata: open COMP-0007 (OpenAI).
  - Minimal ArtifactSummary/EpisodeSummary and telemetry fields: open Claude responses in COMP-0006 and COMP-0007.
- For end-to-end worked examples (manifest → prompt → citations → write-back): prioritize COMP-0006 (OpenAI, section 6) and COMP-0007 (OpenAI, section 10).
- For areas of disagreement and integration risks: open SYNCOMP-0003.
~~~
