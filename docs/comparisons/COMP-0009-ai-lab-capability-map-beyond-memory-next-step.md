# COMP-0009: Provider Comparison — AI-Lab Capability Map Beyond Memory Next Step

## Metadata

- comparison_id: `COMP-0009`
- title: `AI-Lab Capability Map Beyond Memory Next Step`
- context_policy: `latest_context`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0009-ai-lab-capability-map-beyond-memory-next-step.context.json`
- created_at: `2026-07-02T12:01:43.669627+00:00`
- command: `scripts/compare_providers.py Decide the next AI-Lab implementation step after the capability-map discussion. Options: (A) InteractionLog/L1 summaries, (B) predicate vocabulary plus WarrantEdge/MemoryEdge schema, (C) topological context packing. Given current code and development_directions.md, choose one, justify ordering, and give plan, tests, non-goals, risks. --latest-context --token-budget 8000 --model-target gpt-5 --title AI-Lab Capability Map Beyond Memory Next Step`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Decide the next AI-Lab implementation step after the capability-map discussion. Options: (A) InteractionLog/L1 summaries, (B) predicate vocabulary plus WarrantEdge/MemoryEdge schema, (C) topological context packing. Given current code and development_directions.md, choose one, justify ordering, and give plan, tests, non-goals, risks.

## OpenAI Response

- model: `gpt-5`

```
Decision: Choose (A) InteractionLog/L1 summaries.

Why this ordering
- Foundational and low-risk: Episode-level L1 summaries are part of the minimal reconciled loop and are explicitly used in selection, budgeting, write-back, and validation. They are required building blocks before either (B) typed edges or (C) topological packing.
- De-risks later semantics: Predicate vocab and WarrantEdge/MemoryEdge depend on stable provenance and episode context; L1s provide that provenance and a validated citation surface.
- Keeps us aligned with current safety priorities: L1 generation can be wired to the same deny-by-default ACL/redaction and citation integrity checks already prioritized in the reconciled plan, avoiding leakage while we add capabilities.
- Enables measurable wins now: Even without edges or advanced packing, Episode L1 improves retrieval quality, reduces prompt bloat, and gives telemetry for the capability map.

Why not (B) or (C) yet
- (B) predicate vocabulary + WarrantEdge/MemoryEdge: Introduces early ontology lock-in and migration overhead without a stable summarization/provenance layer; edges should point to L0 spans and L1 episode context to be auditable.
- (C) topological context packing: Depends on having consistent episode L1s and stable ACL-aware selection; optimizing packing before we have high-quality L1 inputs risks premature complexity and leakage pathways.

Implementation plan

P0: Schemas, write path, and validators
- Schemas
  - InteractionLogEvent (append-only, per turn):
    - ids: event_id, episode_id, turn_id, created_at
    - roles/actors: role (user/assistant/system/tool), actor_id (optional), model_used, model_version
    - inputs/outputs: prompt_manifest_id, selected_context_manifest_id, request_text_hash, response_text_hash
    - telemetry: tokens_prompt, tokens_completion, duration_ms, outcome_code, error_code/message
    - security: namespace, access_level, redaction_level
    - citations_used: list of ChunkReference ids present in the generated answer
  - EpisodeL1Summary (artifact-level L1 can come later; start with episode):
    - ids: episode_id, l1_id, created_at, summary_version
    - text fields: summary_text, key_decisions, open_questions, risks, next_actions
    - references: list of ChunkReference objects (chunk_id, artifact_id, version, span_start, span_end, embedding_ref) using cid@version|span in text
    - meta: generation_model, generation_prompt_id, coverage_score (0–1), freshness_state (fresh/stale), ttl_until
    - security: namespace, access_level, redacted/full flag
- Write path
  - On configured triggers (see below), build an L1 summary prompt from the InteractionLog for the episode, limited to ACL-eligible content, and require span-bounded citations to included L0 chunks.
  - Generate redacted and (optionally) full variants in separate namespaces if policy allows; default to redacted only.
- Validators (build-failing on CI and runtime reject)
  - Schema validation for InteractionLogEvent and EpisodeL1Summary.
  - Citation integrity: every citation in L1 must be a valid cid@version|span that maps to an allowed ChunkReference; spans must resolve under the pinned tokenizer/version.
  - ACL/redaction: no mixing of redacted/full text or embeddings across namespaces; deny-by-default if clearance not present.
  - Idempotency: re-running generation with unchanged inputs must produce the same L1_id or a content-hash-stable new version.

P1: Storage, indexing, and retrieval integration
- Storage
  - Persist InteractionLogEvents and EpisodeL1Summary records under namespace isolation; keep redacted and full variants in distinct namespaces.
  - Store L1 embeddings as references (embedding_id + embedding_namespace) with embedding_model and dimension metadata; do not inline vectors.
- Indexing
  - Create an L1 index keyed by episode_id and time; add embeddings for L1 to enable retrieval as a first-class candidate.
- Selection integration
  - Modify context assembly to:
    - Seed with the current EpisodeL1Summary when the user request is within the same episode.
    - Allocate a small, explicit budget slice for L1 (e.g., 5–10% of context budget as per reconciled defaults), with hard caps and truncation rules.
  - Ensure the manifest records inclusion_reason = "episode_l1" with priority consistent with reconciled budgeting.

P2: Triggers, refresh, and ops
- Triggers
  - End-of-episode
  - N turns elapsed (configurable, e.g., every 5 turns)
  - Manual refresh
  - Staleness TTL or dependency content change
- Refresh policy
  - Recompute only when coverage_score drops or TTL expires; otherwise reuse cached summary.
- Observability
  - Dashboards for L1 generation rate, failure reasons, latency, token cost, and validator failures.

Acceptance tests

Unit tests
- Schema round-trip: serialize/deserialize InteractionLogEvent and EpisodeL1Summary; required/optional field coverage.
- Citation validator:
  - Accepts valid cid@version|span that map to known chunk spans under the pinned tokenizer.
  - Rejects malformed spans, missing chunk ids, wrong versions, or tokenizer mismatches.
- ACL/redaction guard:
  - Rejects L1 generation if any included ChunkReference is outside caller’s namespace/access level.
  - Rejects any attempt to mix redacted and full text/embeddings across namespaces.

Integration tests
- E2E Episode
  - Create an episode, log 3 user/assistant turns with known L0 citations.
  - Generate EpisodeL1; verify:
    - summary_text present, citations resolve, coverage_score >= threshold.
    - Stored under correct namespace; redacted variant exists; no full variant without clearance.
  - Run context assembly for a new query in the same episode; confirm EpisodeL1 appears in the manifest with reason "episode_l1" and within its token budget.
  - Answer generation includes only citations from allowed namespaces and passes citation integrity validation.
- Idempotency
  - Re-run L1 generation with unchanged InteractionLog; content hash stable; either same l1_id or versioned with identical payload.
- Refresh
  - After adding a new critical turn, TTL or coverage trigger causes a new L1; version increments; old remains retrievable but not default.
- Performance
  - L1 generation completes under configured latency SLO (e.g., p95 < 3s) and token budget (e.g., < 2k tokens).

Negative tests
- Mixed-representation attempt: injecting a full-text ChunkReference into a redacted L1 fails with explicit error.
- Cross-namespace leakage: referencing a chunk from a different namespace fails early.
- Citation drift: changing tokenizer version without reindexing causes validator failure as expected.

Non-goals for this increment
- No predicate vocabulary, WarrantEdge/MemoryEdge, or graph persistence.
- No topological context packing or dependency graph traversal beyond seeding EpisodeL1.
- No cross-episode synthesis or global timelines.
- No artifact-level L1 unless trivial to add; focus on Episode L1 first.
- No UI dashboards beyond basic metrics/logging.

Key risks and mitigations
- Citation granularity drift (artifact vs chunk): Mitigate by enforcing chunk-level ChunkReference and failing validation on artifact-level “summaries” without spans.
- Redaction/namespace leakage: Deny-by-default in selection and generation; separate namespaces for redacted/full; validator blocks mixing.
- Hallucinated L1 content or fabricated citations: Instruct models to cite only provided L0; enforce validator; sample spot-checks.
- Cost/latency creep: Hard token/latency budgets; early truncation; background batching for refresh.
- Staleness and coverage gaps: TTL + coverage metrics as triggers; prompts that include “unresolved questions” to surface gaps explicitly.
- Concurrency/idempotency: Content-hash-based dedupe; episode-level locks during L1 write; retry-safe writes.

Exit criteria (definition of done)
- EpisodeL1Summary schema and validator merged; CI fails on violations.
- L1 generation available via API/CLI with triggers; summaries stored with namespace isolation and embeddings referenced.
- Context assembly includes EpisodeL1 with budget slice and passes ACL/citation validations.
- E2E test suite green; dashboards show generation rate, failure modes, and within SLOs.

This sequencing delivers immediate retrieval and quality gains with strong safety guarantees, and it lays the groundwork for (B) typed edges (linking warrants to cited spans and episode context) and (C) topological packing (using Episode L1 as a compact, validated seed).
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# AI-Lab Next Implementation Step Decision

## Analysis of Context

The context pack reveals two competing "next step" recommendations from prior discussions:
- **OpenAI**: Wire deny-by-default ACL/redaction through retrieval pipeline
- **Claude**: Implement L0 chunk-level schema foundation first

However, the user's task presents **three different options** that appear to come *after* a "capability-map discussion":
- (A) InteractionLog/L1 summaries
- (B) Predicate vocabulary + WarrantEdge/MemoryEdge schema  
- (C) Topological context packing

**Critical observation**: These options suggest the foundational L0/ACL work may already be decided or in progress, and we're now choosing between *memory layer* features.

## Recommendation: **Option B – Predicate Vocabulary + WarrantEdge/MemoryEdge Schema**

### Justification for Ordering

**Why B before A:**
- **Foundation before collection**: Option B defines *how* we represent relationships and warrants between memory elements. Option A (InteractionLog/L1) will *generate* those elements but needs the schema to store them correctly.
- **Prevents rework**: If we build L1 summaries (A) without a warrant/edge schema, we'll either store unstructured relationships or need to migrate data later when we add structured edges.
- **Citation integrity dependency**: The context emphasizes citation validation (`cid@version|span`). WarrantEdge likely captures *why* a citation is valid (provenance), which must be defined before we generate summaries that reference chunks.

**Why B before C:**
- **Topology requires labels**: Topological packing (C) needs to traverse a *labeled graph*. Without predicate vocabulary and edge types (WarrantEdge, MemoryEdge), topological algorithms have no semantics to guide traversal (e.g., "follow dependency edges with depth 2" requires `dependency` to be a defined predicate).
- **Budget allocation needs edge weights**: The context mentions boosts/penalties in selection. Edge schemas likely encode relationship strength/type that informs budgeting.

**Why B is safest now:**
- Aligns with context emphasis on schema stability ("schema changes after building dependent systems are expensive")
- Small, well-scoped task with clear validation (schema tests)
- Unblocks both A and C

---

## Implementation Plan: Option B

### 1. Define Predicate Vocabulary

**Deliverable**: `docs/schema/predicates.md` and `src/memory/predicates.py`

**Core predicates** (inferred from context):
```python
# Structural predicates
CONTAINS = "contains"           # artifact contains chunk
REFERENCES = "references"       # chunk/artifact references another
DEPENDS_ON = "depends_on"       # logical dependency
DERIVED_FROM = "derived_from"   # L1 derived from L0(s)

# Temporal predicates  
PRECEDES = "precedes"           # episode/interaction order
SUPERSEDES = "supersedes"       # version relationship

# Epistemic predicates
SUPPORTS = "supports"           # warrant: evidence supports claim
CONFLICTS_WITH = "conflicts_with"
EXPLAINS = "explains"

# Access control predicates
REDACTS = "redacts"             # redacted version of full text
GRANTS_ACCESS = "grants_access" # namespace permission edge
```

**Schema**:
```python
@dataclass
class Predicate:
    name: str
    inverse: Optional[str]  # e.g., CONTAINS ↔ CONTAINED_BY
    transitive: bool
    symmetric: bool
    allowed_source_types: Set[str]  # {"chunk", "artifact", "episode"}
    allowed_target_types: Set[str]
```

### 2. Define WarrantEdge Schema

**Deliverable**: `src/memory/warrant_edge.py`

```python
@dataclass
class WarrantEdge:
    edge_id: str                    # Unique edge identifier
    source_id: str                  # chunk_id or artifact_id
    target_id: str                  # chunk_id or artifact_id
    predicate: str                  # From predicate vocabulary
    
    # Warrant metadata
    confidence: float               # [0.0, 1.0]
    evidence_span:
````
