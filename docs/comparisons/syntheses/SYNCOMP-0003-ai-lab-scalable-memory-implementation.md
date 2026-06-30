# SYNCOMP-0003: Comparison Synthesis — AI-Lab Scalable Memory Implementation

## Metadata

- synthesis_id: `SYNCOMP-0003`
- title: `AI-Lab Scalable Memory Implementation`
- created_at: `2026-06-30T18:27:17.938454+00:00`
- command: `scripts/synthesize_comparison.py docs/comparisons/COMP-0006-re-ask-ai-lab-scalable-memory-implementation.md --provider openai --title AI-Lab Scalable Memory Implementation`
- source_comparison: `docs/comparisons/COMP-0006-re-ask-ai-lab-scalable-memory-implementation.md`
- synthesizer_provider: `OpenAI`
- synthesizer_model: `gpt-5`

## Synthesis

~~~text
1) Shared agreement
- Both define two summary layers:
  - A lower-level artifact summary (OpenAI: chunk-level L0; Claude: artifact-level “ArtifactSummary”).
  - An episode-level summary (OpenAI: episode L1; Claude: EpisodeSummary).
- Both include embeddings tied to summaries and specify embedding model metadata.
- Both provide refresh triggers for summaries (content/dependency changes, staleness, manual refresh, model changes).
- Both propose a Context Pack Manifest with:
  - Separation of rule-based/mandatory inclusions and retrieval-based inclusions.
  - A token budget broken into allocations.
  - Metadata about the user/request/session.
- Both consider dependencies when selecting context (explicit refs and dependency expansion).
- Both introduce fields to aid selection and organization (tags/domains, dependencies, versioning).

2) Meaningful differences
- Granularity of L0:
  - OpenAI: per-chunk with chunk_id, precise spans, keyphrases/entities/claims/risks; used for retrieval and citations.
  - Claude: artifact-level summary with purpose/key elements/tags; no chunk_id/span structure shown.
- Citation format:
  - OpenAI: specifies mandatory cid@version|span and enforces span bounds.
  - Claude: no citation format specified.
- Embedding storage:
  - OpenAI: references embeddings by embedding_id and embedding_namespace.
  - Claude: stores embeddings inline (vector) with model/dimension.
- Access control/redaction:
  - OpenAI: ABAC with namespaces, deny-by-default, dual redacted/full representations, redaction maps.
  - Claude: no ACL/redaction handling in the excerpt.
- Selection algorithm and budgets:
  - OpenAI: detailed hybrid retrieval (BM25 + dense + reranker), rule-based boosts, novelty penalties, bucketed token allocations as percentages, dedup/ACL filters, version pinning.
  - Claude: manifest fields with token_budget totals (default 8000) and priorities but no algorithmic steps or reranking details.
- Write-back and validation:
  - OpenAI: complete pipeline (micro-summaries, ADR generation, embeddings, lineage updates, indices) and validations (schema, citation integrity, ACL audit, DLP, coverage, idempotency).
  - Claude: references MicroSummary and code snippets but lacks a full write-back pipeline and validations in the provided excerpt.
- L1 scope:
  - OpenAI: artifact-level L1 plus episode L1, with links to L0/keyrefs.
  - Claude: episode L1 only (artifacts_read/modified, tokens_used, duration, model_used).
- Metadata emphasis:
  - OpenAI L0: entities/claims/risks/keyphrases/source_meta; L1: highlights/decisions/open_questions.
  - Claude ArtifactSummary: language/size_bytes/complexity_score/tags; explicit dependencies list.
- End-to-end example:
  - OpenAI: full realistic scenario.
  - Claude: none in the provided excerpt.

3) Stronger points from OpenAI
- Fully specified, implementable schemas for chunk-level L0, artifact L1, and episode L1 with required fields and provenance.
- Clear, enforceable citation format (cid@version|span) and validation of spans.
- Concrete per-prompt selection algorithm combining rule-based inclusion, hybrid retrieval, cross-encoder reranking, deduplication, ACL filtering, and token budgeting with default percentages.
- Comprehensive write-back pipeline (micro-summaries, ADR creation, embeddings, lineage/index updates).
- Rigorous validation checks (schema, ACL/DLP, citation coverage, idempotency, reproducibility).
- Detailed access control and redaction model with namespaces and dual representations.
- End-to-end worked example demonstrating manifest, prompt assembly, citations, and write-back.

4) Stronger points from Claude
- Simpler, minimal schemas that are easy to adopt quickly:
  - Artifact-level summary focused on purpose, key elements, dependencies, and practical metadata (path, language, size, complexity).
  - EpisodeSummary includes operational telemetry (tokens_used, duration_seconds, model_used) and lists of generated artifacts.
- Explicit default numeric token budget in the manifest and a priority field for mandatory artifacts.
- Inclusion_reason enumerates temporal signals explicitly (temporal), highlighting recency-based inclusion.
- Refresh triggers include dependency changes and validation failures, making maintenance straightforward.

5) Combined answer (derived)
- Schemas
  - Adopt OpenAI’s chunk-level L0 and artifact/episode L1 as the backbone.
  - Enrich Artifact metadata with Claude’s fields: artifact_type, path, language, size_bytes, complexity_score, tags, and explicit dependencies.
  - Keep OpenAI’s embedding_id + embedding_namespace for storage; add Claude’s embedding_dimension/model fields for traceability. Avoid storing full vectors inline to control record size.
  - Extend Episode L1 with Claude’s tokens_used, duration_seconds, model_used, and lists of artifacts_read/modified.
- Refresh triggers
  - Use OpenAI’s triggers (content change, TTLs, model upgrades, hotness, policy) plus Claude’s dependency_change and validation-failure triggers. Align TTLs per OpenAI; keep Claude’s staleness (>30 days) as a floor for artifact-level refreshes where TTLs aren’t set. (Inference: harmonization.)
- Manifest and citations
  - Use OpenAI’s Context Pack Manifest structure, rules_applied, candidate_set, ranking, inclusions, and acl_decisions.
  - Keep mandatory citation format cid@version|span from OpenAI.
  - Incorporate Claude’s priority for mandatory_artifacts and temporal as an explicit inclusion reason.
- Selection algorithm and budgets
  - Use OpenAI’s hybrid selection algorithm and bucketed percentage budgets.
  - Allow setting a fixed default total token budget (e.g., 8000 as in Claude) for small-context models; apply OpenAI’s percentages to that total. (Inference: compatibility option.)
- Write-back and validations
  - Implement OpenAI’s write-back pipeline and validations; interpret Claude’s MicroSummary as OpenAI’s L0 micro-summaries for generated artifacts.
- Access control/redaction
  - Use OpenAI’s ABAC + namespace model and redaction handling; propagate strictest labels to episode-level artifacts as specified by OpenAI.

6) Risks or missing assumptions
- Truncation/incompleteness: Claude’s plan in the provided excerpt is incomplete (missing citation format, retrieval/reranking details, access control/redaction, full write-back, ChunkReference schema). This leaves gaps if taken alone.
- L0 meaning divergence: OpenAI uses chunk-level L0, while Claude’s “L0 Artifact Summary” is artifact-level; mapping between these must be defined to prevent ambiguity.
- Embedding storage mismatch: Inline vectors (Claude) vs referenced embeddings (OpenAI) require a consolidation decision to avoid bloat or dereferencing complexity.
- Token budget policy: OpenAI uses percentage-of-context; Claude uses fixed totals. Without harmonization, runtime allocation could be inconsistent across models. (Inference: integration risk.)
- Dependency handling: Claude lists dependencies at artifact level; OpenAI’s dependency expansion is graph-based with depth/centrality. The combined system must specify how artifact-level dependency metadata feeds the graph traversal.
- Validation scope: Claude’s “failed validation” trigger isn’t defined; OpenAI defines validation checks but not which failures trigger refresh vs block. This needs alignment.

7) Suggested re-ask prompt
Design a reconciled minimal viable implementation that merges the two plans by:
- Finalizing L0/L1: confirm L0 is chunk-level with spans; define how an artifact-level summary (fields: artifact_type, path, language, size_bytes, complexity_score, tags, dependencies) coexists with L0 chunks and artifact L1. Provide the ChunkReference schema.
- Confirm embedding handling: use embedding_id + namespace storage; include embedding_model and embedding_dimension; state whether vectors are stored inline or referenced only.
- Specify the mandatory citation format (cid@version|span) and include an example; define span units and validation rules.
- Complete the Context Pack Manifest with fields for priority and temporal inclusion_reason; provide a full JSON example.
- Detail the per-prompt selection algorithm end-to-end: rule-based seeding (explicit/dependency/domain/temporal), hybrid retrieval (BM25 + dense), reranking, ACL filtering, deduplication, novelty handling, and token budgeting. State default budgets for both percentage-of-context and a fixed-total fallback.
- Define access control and redaction: ACL model, namespaces, redacted vs full text, and how embeddings respect clearance.
- Provide the write-back pipeline: micro-summaries, ADR generation, embeddings, lineage updates, indices, and validation checks (schema, citation integrity, ACL/DLP, coverage, idempotency).
- Include an end-to-end realistic example (request → manifest → prompt with citations → answer → write-back) using the finalized schemas.
~~~

## Source Comparison

~~~markdown
# COMP-0006: Provider Comparison — Re-Ask AI-Lab Scalable Memory Implementation

## Metadata

- comparison_id: `COMP-0006`
- title: `Re-Ask AI-Lab Scalable Memory Implementation`
- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0002-ai-lab-scalable-memory-architecture.md`
- created_at: `2026-06-30T15:34:05.898453+00:00`
- command: `scripts/reask_from_synthesis.py docs/comparisons/syntheses/SYNCOMP-0002-ai-lab-scalable-memory-architecture.md --title Re-Ask AI-Lab Scalable Memory Implementation`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

“Design a minimal viable implementation plan for the combined architecture that: Defines exact L0/L1 summary schemas for artifacts and episode summaries, including refresh triggers. Specifies the Context Pack Manifest schema and the mandatory citation format (cid@version|span). Details the per-prompt selection algorithm combining rule-based inclusion (explicit/dependency/domain/time) with hybrid retrieval and re-ranking, including default token budgets. Outlines the write-back pipeline (micro-summaries, ADR generation, embeddings, lineage updates) and validation checks. Describes access control/redaction handling for chunks and embeddings. Provides an end-to-end example (request → manifest → prompt → answer with citations → write-back) on a realistic project.”

## OpenAI Response

- model: `gpt-5`

```
Below is a minimal viable implementation plan that you can hand to engineering. It defines concrete schemas, selection logic, budgets, pipelines, validations, and an end-to-end example.

1) L0/L1 summary schemas and refresh triggers

1.1 L0 micro-summaries (for artifacts and chunks)
- Scope: per-chunk, minimal, fast to refresh. Basis for retrieval and provenance.
- Storage: document store and indexed in search/vector DB.

JSON schema (required fields denoted by “req: true”)
{
  "chunk_id": "uuid",                      // req
  "artifact_id": "string",                 // req (e.g., repo/path or doc id)
  "artifact_version": "string",            // req (semver, git sha, or monotonic int)
  "span": {"type": "lines|bytes", "start": int, "end": int}, // req
  "content_hash": "sha256",                // req; of raw text for this span
  "l0_summary": "string",                  // req; 1–3 sentences, <= 300 chars
  "keyphrases": ["string", ...],           // req; 3–10
  "entities": [{"type":"service|table|api|ticket|lib|env|person","name":"string"}], // opt
  "claims": [{"text":"string","polarity":"pro|con|neutral"}], // opt; short facty claims
  "risks": [{"text":"string","severity":"low|med|high"}],     // opt
  "embedding_id": "uuid",                  // req; references vector store row
  "embedding_namespace": "string",         // req; per-ACL/tenant namespace
  "acl": {"project":"string","labels":["confidential","pii",...],"owners":["user|group"]}, // req
  "source_meta": {"type":"code|doc|ticket|pr|runbook|log","path":"string","repo":"string","url":"string"}, // req-ish
  "created_at": "iso-datetime",            // req
  "last_refreshed_at": "iso-datetime",     // req
  "generator": {"model":"string","version":"string"}, // req
  "provenance": {"pipeline_run_id":"uuid"} // req
}

Refresh triggers (L0):
- Content change: artifact content_hash or file blob changed; re-chunk and regenerate dependent L0.
- TTL: default 14 days or 100 days for immutable versions; staggered background refresh.
- Model upgrade: when embedding or summarizer model changes; enqueue async re-embed/re-summarize.
- Hotness: chunk appears in top-K retrieved for N prompts/day; refresh L0 to incorporate better keyphrases/entities.
- Policy change: redaction/ACL labels updated.
- Manual: on-demand refresh via API.

1.2 L1 summaries (artifact-level and episode-level)
- Purpose: compressed context for larger units (entire artifact, PR, design doc, or a chat episode/meeting).

JSON schema (artifact L1)
{
  "artifact_id": "string",                // req
  "artifact_version": "string",           // req
  "content_hash": "sha256",               // req; of full artifact version
  "l1_summary": "string",                 // req; <= 1200 chars
  "sections": [{"title":"string","summary":"string"}], // opt; 2–6 sections
  "highlights": ["string", ...],          // req; 5–10 bullets
  "decisions": [{"id":"string","text":"string","status":"proposed|accepted|rejected"}], // opt
  "open_questions": ["string", ...],      // opt
  "keyrefs": [{"chunk_id":"uuid","span":{"type":"lines|bytes","start":int,"end":int}}], // req; pointers to L0
  "embedding_id": "uuid",                 // req
  "embedding_namespace": "string",        // req
  "acl": {...},                           // req, same as L0
  "created_at": "iso-datetime",           // req
  "last_refreshed_at": "iso-datetime",    // req
  "generator": {"model":"string","version":"string"}, // req
  "provenance": {"pipeline_run_id":"uuid"} // req
}

JSON schema (episode L1; chat/meeting/ticket thread)
{
  "episode_id": "uuid",                   // req
  "title": "string",                      // req
  "participants": ["user_id", ...],       // req
  "time_window": {"start":"iso","end":"iso"}, // req
  "goals": ["string", ...],               // req
  "summary": "string",                    // req; <= 1200 chars
  "decisions": [{"text":"string","confidence":0.0-1.0}], // req
  "actions": [{"text":"string","assignee":"user","due":"iso"}], // opt
  "citations": [{"cid":"string","version":"string","span":"string"}], // req; links to artifacts
  "embedding_id": "uuid",                 // req
  "embedding_namespace": "string",        // req
  "acl": {...},                           // req
  "created_at": "iso-datetime",           // req
  "last_refreshed_at": "iso-datetime",    // req
  "provenance": {"pipeline_run_id":"uuid"} // req
}

Refresh triggers (L1):
- Artifact L1: on content_hash change or any descendant L0 changed > X% or critical sections modified; TTL 30 days; model upgrade; usage hotness.
- Episode L1: on episode closure/inactivity > 24h; after N new turns (default N=10) or decision detected; TTL 7 days for active projects.

2) Context Pack Manifest schema and citation format

2.1 Mandatory citation format
- Syntax: cid@version|span
- cid: canonical chunk identifier string (chunk_id, UUID).
- version: artifact_version string for the chunk’s parent artifact (e.g., git SHA or semver).
- span: “Lstart-Lend” for line-based or “Bstart-Bend” for byte-based. Examples: L10-42 or B120-450.
- Example: 8d3f2c5e-9e9a-4b6a-91ef-1d0a5e3a1a1f@a1b2c3d|L10-42

2.2 Context Pack Manifest (what we assemble per prompt)
{
  "manifest_id": "uuid",
  "request_id": "uuid",
  "user": {"id":"string","roles":["string",...],"projects":["string",...]},
  "timestamp": "iso-datetime",
  "task": {"intent":"qa|code|design|ops|plan","prompt":"string"},
  "model": {"name":"string","context_tokens": int},
  "budgets": {
    "total_tokens": int,
    "allocations": {
      "system": int,
      "user_prompt": int,
      "explicit": int,
      "dependencies": int,
      "retrieved": int,
      "summaries_l1": int,
      "headroom": int
    }
  },
  "rules_applied": {
    "explicit_refs": [{"type":"url|path|id","value":"string"}],
    "dependency_expansion": {"depth":1,"max_artifacts":20},
    "domain_includes": ["adr|runbook|rfc|recent_changelogs"],
    "time_window": {"days": 30}
  },
  "candidate_set": {
    "rule_based": [{"cid":"uuid","version":"string","span":"string","reason":"explicit|dependency|domain|recent"}],
    "retrieval": {
      "query_terms": ["string",...],
      "bm25_topk": [{"cid":"uuid","score":float}],
      "dense_topk": [{"cid":"uuid","score":float}],
      "filters": {"type":["code","doc"],"project":["string"],"acl":"enforced"}
    }
  },
  "ranking": {
    "method": "hybrid+bce_rerank",
    "final": [{"cid":"uuid","version":"string","span":"string","score":float,"source":"explicit|dep|bm25|dense"}]
  },
  "inclusions": {
    "l0_chunks": [{"cid":"uuid","version":"string","span":"string","estimated_tokens":int}],
    "l1_summaries": [{"artifact_id":"string","version":"string","estimated_tokens":int}],
    "exclusions": [{"cid":"uuid","reason":"acl|dup|budget|low_score"}]
  },
  "acl_decisions": {
    "allowed_namespaces": ["string",...],
    "redactions": [{"cid":"uuid","type":"pii|secret","count":int}]
  },
  "final_context_bytes": int,
  "hash": "sha256"  // of serialized manifest
}

3) Per-prompt selection algorithm

3.1 Inputs
- user_prompt, episode context (last N turns), user/role/project, time_now, model context window.

3.2 Steps
1) Parse and seed
- Extract explicit refs (URLs, file paths, ticket IDs), entities, time hints, task intent.
- Seed set S0 with explicit refs mapped to chunk_ids (resolve to latest or versioned).
- Expand dependencies: for each artifact in S0, traverse artifact_dependency_graph up to depth=1 (configurable), add top-M dependent chunks by centrality/size cap.

2) Domain/time heuristics
- If intent=design or code-change, include latest ADRs and relevant RFCs in same project; if ops, include last 7 days incidents/runbooks; include last 30 days changes touching same components. Add to S1.

3) Hybrid retrieval
- Build query from: user_prompt + extracted entities + episode L1 summary.
- Run BM25 (k=100) with filters (project, type).
- Run dense retrieval (k=200) in user’s embedding_namespace; query = mean-pooled embedding of prompt + entities; use ANN index.
- Merge by normalized score: score = 0.5*bm25 + 0.5*dense; keep top 200.
- Re-rank top 200 with cross-encoder/bce-reranker (e.g., bge-reranker-large) to top 60.

4) Merge, dedup, boost, and filter
- Combine S0 (explicit, boost +2.0), S_dep (+1.0), domain/time (+0.5), and re-ranked list.
- Deduplicate by artifact_id+span overlap (IoU>0.5 keeps higher score).
- Apply ACL filter; drop chunks not allowed in user’s namespaces.
- Apply novelty penalty for chunks already included in last manifest for same episode unless updated (−0.3).

5) Token budgeting and selection
- Defaults (percent of model context):
  - system: 5%
  - user_prompt: 10%
  - explicit: 25%
  - dependencies: 15%
  - retrieved: 25%
  - summaries_l1: 10%
  - headroom: 10%
- Example for 128k tokens: system=6.4k, user_prompt=12.8k, explicit=32k, dependencies=19.2k, retrieved=32k, summaries_l1=12.8k, headroom=12.8k.
- Selection per bucket:
  - For explicit: pack highest-priority exact spans first; if overflow, replace low-value L0 with corresponding L1 artifact summary.
  - For dependencies: include 1–3 key chunks per dependent artifact (by centrality/intro sections).
  - For retrieved: add top-ranked until budget hit; prefer L0; if many small chunks from same artifact, switch to L1 to collapse.
  - For summaries_l1: include artifact-level or episode-level L1 that covers excluded yet relevant parts.
- Ensure minimum 2 citations per major claim category (design decision, SLA, code API) when available.

6) Manifest finalize
- Record inclusions, exclusions, redactions, and computed allocations.
- Freeze versions: resolve latest→pinned artifact_version to maintain reproducibility.

4) Write-back pipeline and validations

4.1 Pipeline stages (post-answer)
- A) Micro-summaries for generated content
  - If assistant produced new artifacts (ADR draft, code diff, plan), store as artifact with version=v1.
  - Chunk and create L0 for each chunk; generate embeddings.
- B) ADR detection and generation
  - If answer contains a “Decision” section or explicit ADR intent, create an ADR artifact:
    - Convert to ADR template (Title, Context, Decision, Consequences, Status).
    - Assign artifact_id (e.g., docs/adr/NNN-…). Store as version=v1, status=Draft.
- C) Embeddings
  - Embed new artifacts in the same embedding_namespace as user; upsert into vector store.
- D) Lineage and episode updates
  - Store answer object with backreferences to manifest_id and citations.
  - Update episode L1: adjust goals/decisions/actions; add citations to newly created artifacts.
  - Update artifact_dependency_graph if new links implied (e.g., ADR references a service).
- E) Index and caches
  - Update BM25 index for new text; warm query cache for popular entities in answer.

4.2 Validation checks (block writes on failure unless marked “warn”)
- Schema validation: L0, L1, manifest; required fields present.
- Citation integrity: every citation cid exists, version matches stored artifact_version, spans within bounds; warn if overlapping spans conflict.
- ACL audit: ensure every included/exposed chunk was allowed for the user; if answer text contains redacted placeholders, ensure mapping not exposed.
- DLP/secret scan: run detectors over answer and any new artifacts; block if secret/PII appears without corresponding ACL.
- Coverage: at least 60% of non-trivial factual sentences in the answer backed by >=1 citation; warn if below.
- Reproducibility: recompute manifest hash and store; store content_hash of answer.
- Embedding conformance: vector dim matches model; namespace present; upsert acknowledged.
- Idempotency: if content_hash already exists, skip duplicate write; increment version only on diff.

5) Access control and redaction handling

5.1 Enforcement
- ABAC over RBAC: evaluate user roles, project, environment, data-classification labels against chunk acl.
- Namespaces: each embedding belongs to embedding_namespace = tenant/project/label set; retrieval queries only that namespace plus public ones allowed by policy.
- Positive security model: deny-by-default; manifest assembly filters before ranking.

5.2 Redaction
- Redaction at source-chunk: replace detected PII/secrets with tokens like <SECRET:API_KEY>; store a redaction map in a secure vault keyed by chunk_id for authorized rehydration.
- Dual representation:
  - text_redacted: used for embeddings for non-cleared users; embeddings generated from redacted text to prevent leakage.
  - text_full: used for embeddings only in restricted namespaces for cleared users.
- During inclusion:
  - If user lacks clearance, only redacted versions are retrievable; manifest.redactions records applied counts.
  - Citations remain stable (same cid@version|span); add flag “redacted”: true in inclusion metadata if needed.

5.3 Chunk-level permissions
- Chunk acl labels propagate to L1 summaries; L1 never includes more sensitive data than any constituent L0.
- Episode L1 inherits the strictest label of included citations.

6) End-to-end example

Scenario
- Project: ACME Billing Service
- Task: “Draft an ADR to migrate payments from Stripe to Adyen, referencing our SLA and incident INC-1042. Update PaymentService example code and list open risks.”

Artifacts present
- docs/sla/payments-sla.md v7
- incidents/INC-1042.md v3
- rfcs/payment-gateway-eval.md v5
- code/services/billing/PaymentService.ts v12
- docs/adr/0001-use-stripe.md v2

6.1 Request
user: {id: "alice", roles: ["staff-eng"], projects:["acme-billing"]}
prompt: as above
model: gpt-4o, 128k context

6.2 Selection summary
- Explicit refs detected: “SLA”, “INC-1042”, “PaymentService”
- Dependency expansion: PaymentService depends on GatewayClient and IdempotencyMiddleware (from code graph)
- Domain/time heuristics: include ADRs and RFCs in project; last 30 days show updated RFC v5.

6.3 Manifest (abridged)
{
  "manifest_id":"d6d2…",
  "request_id":"a1f9…",
  "user":{"id":"alice","roles":["staff-eng"],"projects":["acme-billing"]},
  "timestamp":"2026-06-30T12:34:56Z",
  "task":{"intent":"design","prompt":"Draft an ADR..."},
  "model":{"name":"gpt-4o","context_tokens":128000},
  "budgets":{"total_tokens":128000,"allocations":{
    "system":6400,"user_prompt":12800,"explicit":32000,"dependencies":19200,
    "retrieved":32000,"summaries_l1":12800,"headroom":12800
  }},
  "rules_applied":{
    "explicit_refs":[{"type":"id","value":"INC-1042"},{"type":"file","value":"PaymentService.ts"},{"type":"doc","value":"payments-sla.md"}],
    "dependency_expansion":{"depth":1,"max_artifacts":10},
    "domain_includes":["adr","rfc"],
    "time_window":{"days":30}
  },
  "candidate_set":{
    "rule_based":[
      {"cid":"c_sla_01","version":"v7","span":"L10-120","reason":"explicit"},
      {"cid":"c_inc_02","version":"v3","span":"L1-80","reason":"explicit"},
      {"cid":"c_pay_11","version":"v12","span":"L1-200","reason":"explicit"},
      {"cid":"c_gate_03","version":"v4","span":"L1-60","reason":"dependency"},
      {"cid":"c_adr_0001","version":"v2","span":"L1-70","reason":"domain"},
      {"cid":"c_rfc_pg_eval","version":"v5","span":"L1-200","reason":"domain"}
    ],
    "retrieval":{
      "query_terms":["ADR","Stripe","Adyen","SLA","incident INC-1042","PaymentService"],
      "bm25_topk":[{"cid":"c_rfc_pg_eval","score":12.2},{"cid":"c_sla_01","score":11.8}],
      "dense_topk":[{"cid":"c_adn_sdk","score":0.82},{"cid":"c_str_limits","score":0.79}],
      "filters":{"type":["doc","code"],"project":["acme-billing"],"acl":"enforced"}
    }
  },
  "ranking":{"method":"hybrid+bce_rerank","final":[
    {"cid":"c_sla_01","version":"v7","span":"L10-120","score":0.92,"source":"explicit"},
    {"cid":"c_inc_02","version":"v3","span":"L1-80","score":0.90,"source":"explicit"},
    {"cid":"c_rfc_pg_eval","version":"v5","span":"L1-200","score":0.88,"source":"bm25"},
    {"cid":"c_pay_11","version":"v12","span":"L1-160","score":0.86,"source":"explicit"},
    {"cid":"c_adn_sdk","version":"v1","span":"L1-120","score":0.78,"source":"dense"},
    {"cid":"c_adr_0001","version":"v2","span":"L1-70","score":0.70,"source":"domain"}
  ]},
  "inclusions":{
    "l0_chunks":[
      {"cid":"c_sla_01","version":"v7","span":"L10-120","estimated_tokens":2200},
      {"cid":"c_inc_02","version":"v3","span":"L1-80","estimated_tokens":1700},
      {"cid":"c_rfc_pg_eval","version":"v5","span":"L1-140","estimated_tokens":2600},
      {"cid":"c_pay_11","version":"v12","span":"L1-120","estimated_tokens":1800},
      {"cid":"c_adn_sdk","version":"v1","span":"L1-60","estimated_tokens":900}
    ],
    "l1_summaries":[
      {"artifact_id":"docs/adr/0001-use-stripe.md","version":"v2","estimated_tokens":900}
    ],
    "exclusions":[{"cid":"c_gate_03","reason":"budget"}]
  },
  "acl_decisions":{"allowed_namespaces":["acme-billing/confidential"],"redactions":[]},
  "final_context_bytes": 64000,
  "hash":"sha256:…"
}

6.4 Prompt assembled (abridged)
- System (policies/instructions)
- User prompt text
- Context excerpts with headers and mandatory citations inline:
  - Payments SLA (excerpt) [c_sla_01@v7|L10-120]
  - Incident INC-1042 (postmortem) [c_inc_02@v3|L1-80]
  - RFC: Payment Gateway Evaluation (Adyen vs Stripe) [c_rfc_pg_eval@v5|L1-140]
  - PaymentService.ts (current integration points) [c_pay_11@v12|L1-120]
  - Adyen SDK notes [c_adn_sdk@v1|L1-60]
  - ADR-0001 (current Stripe decision) summary [c_adr_0001@v2|L1-70]

6.5 Model answer (excerpt, with citations)
Title: ADR-00NN: Migrate Payments from Stripe to Adyen
Context
- Current system relies on Stripe with 99.9% SLA but observed provider error spikes during retries in us-east-1 on 2026-06-10 [c_inc_02@v3|L12-34]. Our business SLA for payments is 99.95% monthly with <200ms P50 authorization latency [c_sla_01@v7|L22-45].
Decision
- Adopt Adyen as primary PSP for card payments; retain Stripe as failover for specific BIN ranges during phase 1 [c_rfc_pg_eval@v5|L30-88].
Consequences
- Update PaymentService to implement Adyen’s /payments authorization and capture flows with idempotency keys preserved [c_pay_11@v12|L40-78][c_adn_sdk@v1|L10-44].
- Expected improvement in decline code fidelity; re-certification effort estimated 2 weeks [c_rfc_pg_eval@v5|L90-120].
Open Risks
- Chargeback workflows differ; need mapping and reconciliation plan [c_rfc_pg_eval@v5|L110-132].
- Latency SLO risk in eu-west during peak—requires canary and regional routing [c_sla_01@v7|L60-72].
Code Update (example)
- Introduce AdyenClient with retry and idempotency middleware; update PaymentService.authorize():
  // snippet…
  // Source: current PaymentService integration points [c_pay_11@v12|L55-88]
Rollout Plan
- Phase 0: sandbox parity tests; Phase 1: 10% traffic EU cards; Phase 2: global [c_rfc_pg_eval@v5|L140-160].
Status: Proposed

6.6 Write-back
- New artifacts created:
  1) docs/adr/00NN-migrate-to-adyen.md v1 (Draft)
     - Chunk, L0 generated; embedding in acme-billing/confidential.
     - L1 summary created (sections: Context, Decision, Consequences, Risks).
  2) code/services/billing/PaymentService.patch v1
     - Diff snippet; L0+embedding.
- Lineage:
  - answer_id → manifest_id d6d2…; citations list persisted.
  - episode L1 updated: new decision with confidence 0.82; actions: “Create canary in eu-west”, assignee “alice”, due +7d; citations include new ADR cid.
- Validations:
  - Citations resolve and spans valid (OK).
  - Coverage: 78% of factual sentences cited (OK).
  - DLP: no secrets detected (OK).
  - Schema: L0/L1/manifest valid (OK).
  - Indices: BM25 and vector upserted (OK).

7) Defaults, configuration, and components

- Chunking: code by logical blocks or 120–300 lines max; docs by headings or ~2k chars.
- Embedding models: e5-large (text), code-specific model for code (e.g., code-embedding-ada-002 equivalent); reranker: bge-reranker-large.
- Storage:
  - Document store: Postgres/CloudSQL for metadata; blob store for raw text.
  - Vector DB: pgvector/Weaviate/Pinecone with namespace per ACL.
  - Search: OpenSearch/BM25.
- Dependency graph: built from code index (imports/calls), docs cross-links, ticket references.
- Schedulers: queues for refresh triggers; rate limits per repo/project.
- Observability: pipeline_run_id correlates logs, latency SLOs set (p95 < 2s manifest build; p95 < 10s full write-back async).

This plan is intentionally minimal but complete enough to implement: exact schemas, selection and budgets, enforcement and redaction, write-back plus validations, and a realistic end-to-end example with the mandated citation format.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Minimal Viable Implementation Plan: Combined Architecture

## 1. L0/L1 Summary Schemas

### 1.1 L0 Artifact Summary Schema

```yaml
ArtifactSummary:
  artifact_id: string          # Unique identifier
  artifact_type: enum          # code|doc|config|test|data
  path: string                 # Filesystem path
  version: string              # Git SHA or semantic version
  created_at: timestamp
  last_modified: timestamp
  
  # Core summary fields
  purpose: string              # 1-2 sentence purpose (max 200 chars)
  key_elements: list[string]   # Top 5-7 important elements
  dependencies: list[string]   # Direct dependency artifact_ids
  tags: list[string]           # Domain tags (auth, payment, ml, etc.)
  
  # Technical metadata
  language: string             # Programming/markup language
  size_bytes: integer
  complexity_score: float      # Optional: cyclomatic complexity, etc.
  
  # Refresh metadata
  summary_version: integer
  last_summarized: timestamp
  refresh_trigger: enum        # manual|auto|dependency_change
  
  # Embeddings
  embedding_model: string      # text-embedding-3-small, etc.
  embedding_dimension: integer
  embedding: vector[float]     # Dense embedding of summary text
```

**Refresh Triggers:**
- File modification (size or content hash change)
- Dependency change (any direct dependency updated)
- Manual refresh request
- Staleness threshold (>30 days since last summary)
- Failed validation (embedding dimension mismatch)

### 1.2 L1 Episode Summary Schema

```yaml
EpisodeSummary:
  episode_id: string           # UUID
  session_id: string           # Groups related episodes
  timestamp: timestamp
  user_id: string              # Actor identifier
  
  # Episode content
  request_type: enum           # query|implementation|debug|review|refactor
  user_query: string           # Original question (max 500 chars)
  key_outcome: string          # What was accomplished (max 300 chars)
  artifacts_read: list[string] # artifact_ids accessed
  artifacts_modified: list[string] # artifact_ids changed
  
  # Generated content references
  micro_summaries: list[MicroSummary] # See section 4.1
  adrs_generated: list[string] # ADR document IDs
  code_snippets: list[CodeSnippet]
  
  # Metadata
  tokens_used: integer
  duration_seconds: float
  model_used: string
  
  # Embeddings
  embedding_model: string
  embedding: vector[float]     # Episode semantic embedding
  
  # Refresh (episodes are generally immutable, but embeddings may refresh)
  embedding_version: integer
  last_embedding_refresh: timestamp
```

**Episode Refresh Triggers:**
- Embedding model upgrade (migrate all episodes)
- Access control change (redact episode)
- Manual correction/annotation
- Consolidation (merge related episodes into summary)

---

## 2. Context Pack Manifest Schema

```yaml
ContextPackManifest:
  manifest_id: string          # UUID for this context pack
  created_at: timestamp
  user_query: string           # Original request
  request_metadata:
    user_id: string
    session_id: string
    workspace_path: string
    
  # Token budget allocation
  token_budget:
    total: 8000                # Default total budget
    mandatory: 2000            # Reserved for rule-based
    retrieval: 4000            # For hybrid retrieval
    reserve: 2000              # Buffer for formatting
    
  # Included artifacts (rule-based)
  mandatory_artifacts:
    - artifact_id: string
      version: string          # Git SHA
      inclusion_reason: enum   # explicit|dependency|domain|temporal
      priority: integer        # 1 (highest) to 5
      chunks: list[ChunkReference]
      
  # Retrieved artifacts (embedding-based)
  retrieved_artifacts:
    - artifact_id: string
      version: string
      retrieval_score: float   # 0.0
````

~~~
