# COMP-0005: Provider Comparison — AI-Lab Scalable Memory Architecture

## Metadata

- comparison_id: `COMP-0005`
- title: `AI-Lab Scalable Memory Architecture`
- created_at: `2026-06-30T15:22:07.792500+00:00`
- command: `scripts/compare_providers.py For AI-Lab, propose a concise architecture for scalable artifact memory that avoids loading all history into every prompt while preserving traceability, project values, high-level understanding, focused context, and detailed evidence. --title AI-Lab Scalable Memory Architecture`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

For AI-Lab, propose a concise architecture for scalable artifact memory that avoids loading all history into every prompt while preserving traceability, project values, high-level understanding, focused context, and detailed evidence.

## OpenAI Response

- model: `gpt-5`

```
Here’s a concise, scalable memory architecture for AI-Lab that avoids loading full histories while preserving traceability, values, high-level understanding, focused context, and detailed evidence.

1) Memory stack (5 layers, smallest-to-largest in prompts)
- Pinned Values and Guardrails (KV store)
  - 10–20 lines: project values, safety constraints, definition of done.
  - Scoped by org/project; versioned; rarely changes.
- Project Brief and Glossary (short canonical summary)
  - 200–400 tokens: goals, scope boundaries, stakeholders, glossary of terms.
  - Auto-refreshed via rolling hierarchical summaries.
- Decision Log (ADR-style)
  - Atomic decisions with rationale, alternatives, links to evidence and artifacts.
  - Indexed by topic; summarized per topic; full content retrievable.
- Task/Episode Summaries
  - Hierarchical: per-turn micro-summaries → per-episode → per-milestone.
  - Each node links to underlying turns and artifacts; embeddings maintained.
- Artifact and Evidence Store
  - Content-addressable object store (hash-based IDs) for files, code, datasets.
  - Evidence chunks (text/code/image) with embeddings, tags, and lineage.
  - Conversation shards stored as chunks with embeddings and turn IDs.

2) Indices and metadata
- Vector index for semantic retrieval over:
  - Brief + glossary, ADRs, episode summaries, artifact/evidence chunks.
- Graph index (knowledge/lineage)
  - Nodes: concepts, tasks, decisions, artifacts.
  - Edges: supports, contradicts, derived_from, supersedes, depends_on, owned_by.
- Relational metadata
  - Tables for projects, artifacts (hash, version, mime, owner), ADRs, tasks, episodes, citations, tags.
- Stable IDs and versioning
  - Content hashes (CID) for artifacts/evidence.
  - Monotonic versions for mutable summaries and ADRs.
  - All claims cite [type:id@version|span].

3) Context assembly pipeline (per prompt)
- Inputs: user query, current task, token budget.
- Step A: Intent parse
  - Detect task type, domain terms, required modalities; extract constraints.
- Step B: Core pins (fixed)
  - Insert Values/Guardrails (<=100 tokens).
  - Insert Project Brief/Glossary slice most relevant to detected terms (<=200 tokens).
- Step C: High-level
  - Retrieve 1–3 nearest episode/milestone summaries by embedding+task overlap, recency-decayed.
  - Include their 1–2 line abstracts and links.
- Step D: Decisions
  - Retrieve top 3 ADRs relevant to detected terms.
  - Inline 1–2 sentence rationale each; include citations.
- Step E: Focused context
  - Retrieve k evidence/artifact chunks using hybrid search (BM25 + embedding + graph hop).
  - Re-rank by composite score: w1*semantic + w2*recency + w3*authority + w4*lineage_depth + w5*usage_frequency.
  - Compress to extractive snippets with highlighted span IDs.
- Step F: Budget and assembly
  - Budget split (default): 10% values/brief, 15% high-level, 15% decisions, 50% evidence, 10% task state.
  - Produce Context Pack:
    - Preamble: goal + constraints
    - Values/Brief (short)
    - High-level summary bullets (with IDs)
    - Recent decisions (with IDs)
    - Evidence snippets (with [cid:offset..] citations)
    - Request: answer + cite set, note gaps
  - Emit a Context Pack Manifest (JSON) alongside the prompt: list of item IDs, versions, retrieval criteria, scores.
- Step G: Answer-time tooling
  - Require the model to include a Citations section listing all IDs used.
  - If confidence low or conflicts found, prompt to propose next-evidence retrieval.

4) Write-back/updates (post-answer)
- Generate micro-summary of this turn (claims, decisions, open questions).
- If a decision was made, write an ADR with rationale and citations.
- Chunk new artifacts; compute embeddings; store with lineage to source inputs.
- Update hierarchical summaries (episode → milestone) using rolling windows.
- Update graph: add supports/contradicts edges from claims to evidence.
- Log a Context-to-Output Provenance record: {output_id -> context_manifest_ids}.

5) Scaling policies
- Hierarchical summarization
  - Time/size-triggered rollups; keep only last N raw turns per episode in hot storage; everything else cold but retrievable by citation.
- Eviction and pinning
  - LRU with recency decay; user-pinned items bypass eviction.
- Freshness weighting
  - Decay factor per index; bump on reuse and explicit user endorsement.
- Sharding
  - Per-project shards for vector and graph; global shard for values/patterns.
- Modality-aware chunking
  - Code by function/class; text by semantic units; images by region descriptors.

6) Traceability mechanisms
- Content-addressable storage ensures immutable evidence; citations use cid@version with byte/line spans.
- Every answer includes:
  - What: conclusion
  - Why: top 3 supportive citations (+ any contradicting citations if present)
  - How: brief method
  - Confidence and gaps
- Manifest-first provenance: store the exact Context Pack Manifest with the output ID.
- Decision diffs: ADR supersedes links with auto-generated diff summaries.

7) Governance and quality
- Validations
  - Citation checker ensures every nontrivial claim maps to at least one evidence or ADR.
  - Conflict detector flags contradicts edges without resolution.
- Access control
  - Row-level permissions per project; redaction at chunk level; embeddings for redacted text are tagged and access-checked.
- Observability
  - Metrics: retrieval precision@k (via feedback), token budget usage, unresolved contradictions count, stale-brief age.

8) Minimal prompt skeleton
- System: Role + Values/Guardrails (short)
- Context:
  - Project brief/glossary (selected slice)
  - High-level: 3–5 bullets with IDs
  - Decisions: 2–3 ADRs with 1–2 lines each
  - Evidence snippets with [cid@v|span]
- Instruction:
  - Answer the user’s request.
  - Ground every claim with citations. If evidence is insufficient, state gaps and propose next retrieval.
  - Follow project values and constraints.

9) Suggested tech stack (swappable)
- Object store: S3/GCS + content hashes
- Vector DB: Qdrant/Weaviate/FAISS
- Graph DB: Neo4j/ArangoDB
- Relational metadata: Postgres
- KV/cache: Redis
- Orchestrator: Context Builder service with pluggable rerankers
- Schema: JSONLines for manifests and ADRs; OpenAPI endpoints for get_context_pack, post_artifact, post_decision

10) Example API flow (concise)
- POST /turn
  - Body: {project_id, task_id, query}
- Context Builder:
  - fetch pins → retrieve summaries/ADRs → hybrid search over evidence → re-rank → assemble pack + manifest
- LLM call with pack
- POST /turn_result
  - Body: {turn_id, output, citations, confidence}
  - Service updates ADRs/summaries/graph/artifact registry and stores provenance manifest

This design keeps prompts small and focused, yet maintains end-to-end traceability and access to high-level context and detailed evidence on demand.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Scalable Artifact Memory Architecture

## Core Principle
**Hierarchical context with dynamic depth**: Load summaries by default, drill down on demand.

## Architecture Layers

### 1. **Metadata Index** (Always loaded - ~200 tokens)
```
- Project charter & core values
- Artifact registry with IDs, types, timestamps
- Dependency graph (artifact relationships)
- Current session context pointer
```

### 2. **Progressive Summarization** (Load as needed)
```
Level 0: Executive summary (per artifact, ~50 tokens)
  - Purpose, key decisions, current state
  
Level 1: Section summaries (~200 tokens)
  - Major components, rationale, open questions
  
Level 2: Full content (load selectively)
  - Complete artifact text
```

### 3. **Smart Context Assembly**

**For each prompt, dynamically include:**
- Metadata index (always)
- Level 0 summaries for related artifacts
- Level 1-2 for artifacts directly referenced
- Semantic search results from artifact corpus (when querying history)

**Example context budget (8K tokens):**
- 200: Metadata
- 500: Current artifact full detail
- 300: Related artifacts (Level 0)
- 2000: Relevant deep context (Level 1-2, pulled as needed)
- 5000: Reserved for conversation & generation

## Implementation Strategy

### Storage Format
```
/artifacts/
  _index.md              # Metadata registry
  _summaries/
    {artifact-id}.l0.md  # Executive summaries
    {artifact-id}.l1.md  # Section summaries
  {artifact-id}.md       # Full artifacts
```

### Context Selection Rules
1. **Explicit reference**: Load full content (Level 2)
2. **Dependency relationship**: Load Level 1
3. **Same domain/type**: Load Level 0
4. **Search query**: Semantic retrieval across all levels
5. **Time-based**: Recent artifacts get higher priority

### Traceability Mechanism
- Every artifact has immutable ID + version
- Summaries include "derived from" pointers
- Decisions log references specific artifact versions
- Git-like hash chain for change tracking

## Key Benefits
- **Scalable**: O(log n) context growth instead of O(n)
- **Traceable**: Full lineage without full load
- **Focused**: Only relevant detail surfaces
- **Flexible**: Can always drill deeper when needed
- **Practical**: Works within LLM context limits

## Example Usage

```
User: "Update the testing strategy to align with our API design"

Context loaded:
✓ Metadata index (200 tokens)
✓ testing-strategy.md - Level 2 (1500 tokens)
✓ api-design.md - Level 1 (300 tokens)
✓ project-charter.md - Level 0 (50 tokens)
Total: ~2050 tokens

If inconsistency detected:
→ Prompt: "Load api-design.md Level 2 for detailed comparison"
```

This architecture preserves institutional memory while staying within practical limits.
````
