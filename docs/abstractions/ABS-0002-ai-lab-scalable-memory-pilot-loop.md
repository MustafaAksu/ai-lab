# ABS-0002: Abstraction — AI-Lab Scalable Memory Pilot Loop

## Metadata

- abstraction_id: `ABS-0002`
- title: `AI-Lab Scalable Memory Pilot Loop`
- abstraction_level: `1`
- source_artifacts: `docs/comparisons/COMP-0005-ai-lab-scalable-memory-architecture.md, docs/comparisons/syntheses/SYNCOMP-0002-ai-lab-scalable-memory-architecture.md, docs/comparisons/COMP-0006-re-ask-ai-lab-scalable-memory-implementation.md`
- created_at: `2026-06-30T18:05:04.519320+00:00`
- command: `scripts/create_abstraction.py docs/comparisons/COMP-0005-ai-lab-scalable-memory-architecture.md docs/comparisons/syntheses/SYNCOMP-0002-ai-lab-scalable-memory-architecture.md docs/comparisons/COMP-0006-re-ask-ai-lab-scalable-memory-implementation.md --title AI-Lab Scalable Memory Pilot Loop --level 1 --provider openai`
- abstracter_provider: `OpenAI`
- abstracter_model: `gpt-5`

## Source Artifacts

- `docs/comparisons/COMP-0005-ai-lab-scalable-memory-architecture.md`
- `docs/comparisons/syntheses/SYNCOMP-0002-ai-lab-scalable-memory-architecture.md`
- `docs/comparisons/COMP-0006-re-ask-ai-lab-scalable-memory-implementation.md`

## Abstraction

~~~text
AI-Lab Scalable Memory Pilot Loop
Abstraction level: 1

1) Stable claims
- Progressive memory: Both providers advocate hierarchical/progressive context (brief summaries by default, drill down to detail on demand).
- Small, always-on header: Include a compact, pinned set of project values/charter and lightweight metadata in every prompt.
- Dynamic per-prompt assembly: Select context based on relevance and recency; start with summaries, expand to detailed artifacts when needed.
- Versioned traceability: Use immutable IDs/versions and lineage pointers to maintain change tracking and reproducibility.
- Decision awareness: Maintain a decision log and reference specific artifact versions in context and outputs.
- Token budgeting: Allocate limited context to preserve room for generation while keeping focused, evidence-ready context.

2) Important distinctions
- Memory scope
  - OpenAI: Broad stack (values/guardrails, brief/glossary, ADRs, hierarchical task/episode summaries, content-addressable artifact/evidence store, conversation shards).
  - Claude: Artifact-centric (artifacts + L0/L1/L2 summaries), lighter mention of conversational/episode structure.
- Indexing and retrieval
  - OpenAI: Multi-index (vector + knowledge/lineage graph + relational metadata), hybrid retrieval (BM25 + embeddings + graph hops) with composite re-ranking.
  - Claude: Simpler metadata index and dependency graph with rule-based selection; semantic search mentioned without multi-index/rerank specifics.
- Output traceability enforcement
  - OpenAI: Mandates span-level citations in answers and emits a Context Pack Manifest per prompt.
  - Claude: Uses IDs, derived-from pointers, and hash chain but does not require citations or a manifest in the answer.
- Write-back and governance
  - OpenAI: Explicit post-answer updates (micro-summaries, ADRs, embeddings, graph edges), validations (citation/conflict checks), access control, observability, sharding.
  - Claude: Prioritizes simplicity; omits most operational/governance details.
- Budgeting style
  - OpenAI: Percentage-based budget across layers.
  - Claude: Concrete token example with large reserve for generation.
- Storage model
  - OpenAI: Content-addressable object store with modality-aware chunking/embeddings.
  - Claude: File-oriented layout with per-artifact L0/L1 alongside full content.

3) Unsupported strengthenings or risks
- Summary freshness: Neither specifies rigorous, proven refresh policies for summaries; stale L0/L1 or episode summaries can mislead. (Inference in source synthesis)
- Overhead risk: Hybrid retrieval + graph traversal + validations may add latency/cost; simpler rule-based approach is lighter but potentially less robust. (Inference in source synthesis)
- Citation enforcement gap: Only OpenAI mandates citations; without this, answer-time traceability may degrade. (From differences)
- Scope blind spots: Artifact-centric designs may under-represent conversational/episode context unless augmented. (From differences)
- Security/redaction variance: Access control/redaction details appear only in OpenAI’s plan; stricter deployments may need more. (From differences)
- Scaling claim caveat: O(log n) context growth depends on disciplined summarization/pruning; otherwise context can still bloat. (Inference in source synthesis)
- Implementation asymmetry: Claude’s implementation response is incomplete; relying on it for schemas/manifests/citations is risky.

4) Useful compression
- Pilot loop (as proposed across sources)
  - Always-on pins: Insert compact values/guardrails and minimal metadata header each prompt.
  - Progressive context: Start with artifact L0/L1 and episode/milestone summaries; expand to detailed chunks only for explicit refs and top-retrieved evidence.
  - Retrieval: Combine rule-based inclusion (explicit, dependency, domain, time) with hybrid search (sparse + dense; optionally graph hops); re-rank to fill budget.
  - Manifest and citations: Capture included IDs/versions/spans/scores in a Context Pack Manifest; require span-level citations for nontrivial claims.
  - Answer-time behavior: Surface conclusions with supporting/contradicting evidence, note gaps/confidence.
  - Write-back: Create micro-summaries; draft/update ADRs; chunk/embed new artifacts; update lineage/graph; bind output to manifest.
  - Governance: Validate citation coverage/integrity, conflicts, ACL/redaction, DLP; observe retrieval quality and staleness.
- Minimal mental models to carry
  - Header stays tiny; summaries first, details later.
  - Decisions are first-class, version-pinned, and cited.
  - Provenance is manifest-first; every output points to its assembled context.

5) Retrieval hints
- Need end-to-end pilot flow, prompt skeleton, or ops/governance details: Open COMP-0005 (OpenAI response) for context assembly pipeline, write-back, validations, minimal prompt, and example API flow.
- Need simple mental model, progressive levels, or lightweight storage layout: Open COMP-0005 (Claude response) for L0/L1/L2, rule-based inclusion, and directory structure.
- Want a balanced overview of agreements and differences, plus combined approach and risks: Open SYNCOMP-0002 for shared points, distinctions, blended design, and noted risks/assumptions.
- Need concrete schemas (L0/L1/episodes), manifest structure, mandatory citation format, selection algorithm, budgets, access control/redaction, validations, and a realistic example: Open COMP-0006 (OpenAI response).
- Beware gaps: COMP-0006 (Claude response) is incomplete; do not rely on it for schemas or manifest/citation specifications.
~~~
