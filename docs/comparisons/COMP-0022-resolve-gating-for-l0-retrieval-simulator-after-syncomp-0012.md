# COMP-0022: Provider Comparison — Resolve gating for L0 retrieval simulator after SYNCOMP-0012

## Metadata

- comparison_id: `COMP-0022`
- title: `Resolve gating for L0 retrieval simulator after SYNCOMP-0012`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- context_manifest: `docs/comparisons/COMP-0022-resolve-gating-for-l0-retrieval-simulator-after-syncomp-0012.context.json`
- created_at: `2026-07-06T07:33:28.103889+00:00`
- command: `scripts/compare_providers.py --latest-context --require-admission --title Resolve gating for L0 retrieval simulator after SYNCOMP-0012 Resolve gating assumptions before implementing a diagnostic-only L0 hybrid retrieval simulator.

Source artifacts:
- COMP-0021-ai-lab-backlog-prioritization-after-context-manifest-l0-diagnostics
- SYNCOMP-0012-ai-lab-backlog-prioritization-after-context-manifest-l0-diagnostics

Current boundaries:
- Explicit L0 inclusion is implemented.
- Read-only L0 candidate diagnostics are implemented.
- Context-manifest-connected L0 candidate diagnostics are implemented.
- PLAN-20260705-0001 and PLAN-20260706-0001 are completed.
- Automatic L0 retrieval is NOT implemented.
- Context selection changes are NOT implemented.
- Provider prompt changes are NOT implemented.
- GAP-0001 remains open.

Please answer these gating questions for the next diagnostic-only slice:

1. GAP-0001:
   - What current GAP-0001 target remains after completion of the read-only diagnostics?
   - Are existing recommended_next_targets stale? If yes, state the replacement target.

2. ABS-0003 / retrieval algorithm:
   - Should this simulator include BM25 only, dense only, BM25 + dense, or BM25 + dense + reranking?
   - If reranking is required, identify the governing artifact/claim.
   - If not admitted, defer reranking explicitly.

3. Manifest logging schema:
   - Provide canonical section/field names for logging retrieval simulator output.
   - Include per-candidate fields: chunk id, bm25_score, dense_score, retrieval_score, match reason, provenance/path, and selection_effect.

4. Embeddings/index policy:
   - Confirm whether production embedding creation and index mutation are out of scope.
   - State whether mock/file-based embeddings are allowed for tests.

5. Token budget telemetry:
   - Is diagnostic token-budget telemetry required in this slice?
   - If yes, give fields and placement.
   - If no, defer it explicitly.

6. Selection adapter:
   - Should this slice include a no-op pluggable context selection adapter?
   - Or should it be deferred to a separate PLAN?

7. Governance:
   - Is a new PLAN required before implementation?
   - Is a new WARRANT required before implementation?
   - What must the warrant explicitly forbid?

8. Recommended PLAN:
   - Provide exact PLAN title.
   - Provide objective.
   - Provide success criteria.
   - Provide out-of-scope boundary.

Output should be concise, implementation-oriented, and suitable for direct conversion into a PLAN record.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Resolve gating assumptions before implementing a diagnostic-only L0 hybrid retrieval simulator.

Source artifacts:
- COMP-0021-ai-lab-backlog-prioritization-after-context-manifest-l0-diagnostics
- SYNCOMP-0012-ai-lab-backlog-prioritization-after-context-manifest-l0-diagnostics

Current boundaries:
- Explicit L0 inclusion is implemented.
- Read-only L0 candidate diagnostics are implemented.
- Context-manifest-connected L0 candidate diagnostics are implemented.
- PLAN-20260705-0001 and PLAN-20260706-0001 are completed.
- Automatic L0 retrieval is NOT implemented.
- Context selection changes are NOT implemented.
- Provider prompt changes are NOT implemented.
- GAP-0001 remains open.

Please answer these gating questions for the next diagnostic-only slice:

1. GAP-0001:
   - What current GAP-0001 target remains after completion of the read-only diagnostics?
   - Are existing recommended_next_targets stale? If yes, state the replacement target.

2. ABS-0003 / retrieval algorithm:
   - Should this simulator include BM25 only, dense only, BM25 + dense, or BM25 + dense + reranking?
   - If reranking is required, identify the governing artifact/claim.
   - If not admitted, defer reranking explicitly.

3. Manifest logging schema:
   - Provide canonical section/field names for logging retrieval simulator output.
   - Include per-candidate fields: chunk id, bm25_score, dense_score, retrieval_score, match reason, provenance/path, and selection_effect.

4. Embeddings/index policy:
   - Confirm whether production embedding creation and index mutation are out of scope.
   - State whether mock/file-based embeddings are allowed for tests.

5. Token budget telemetry:
   - Is diagnostic token-budget telemetry required in this slice?
   - If yes, give fields and placement.
   - If no, defer it explicitly.

6. Selection adapter:
   - Should this slice include a no-op pluggable context selection adapter?
   - Or should it be deferred to a separate PLAN?

7. Governance:
   - Is a new PLAN required before implementation?
   - Is a new WARRANT required before implementation?
   - What must the warrant explicitly forbid?

8. Recommended PLAN:
   - Provide exact PLAN title.
   - Provide objective.
   - Provide success criteria.
   - Provide out-of-scope boundary.

Output should be concise, implementation-oriented, and suitable for direct conversion into a PLAN record.

## OpenAI Response

- model: `gpt-5`

```
Here are the gating decisions for the next diagnostic-only slice.

1) GAP-0001
- Remaining target: Implement a read-only L0 hybrid retrieval simulator that computes BM25 and dense scores for L0 candidates and logs results in the context manifest diagnostics, with zero selection/prompt effects and zero index/embedding writes.
- Staleness check: Any “next targets” that imply automatic L0 retrieval, selection changes, or provider prompt changes are now stale.
- Replacement target: Diagnostic-only L0 hybrid retrieval simulator with manifest-connected logging; no-op selection effect; feature-flagged and test-only by default.

2) ABS-0003 / retrieval algorithm
- Simulator scope: BM25 + dense (hybrid), no reranking in this slice.
- Rationale: ABS-0003 stable claim admits hybrid retrieval (BM25 + dense). Reranking is referenced in more detailed plans (via ABS-0003 retrieval hints to COMP-0006/0007) but is not admitted for this diagnostic-only slice.
- Deferral: Reranking explicitly deferred to a future governed slice.

3) Manifest logging schema (canonical sections/fields)
- Location: manifest.diagnostics.l0_retrieval_simulator
- Header fields:
  - simulator_id, run_id, timestamp_utc
  - request_id, episode_id, manifest_id, manifest_version
  - query_text, query_kind (user|system|composite)
  - algorithm ("bm25+dense"), reranker ("none")
  - corpus_snapshot_id, l0_index_namespace
  - embedding_model.name, embedding_model.version, embedding_model.dimension
  - bm25_params.k1, bm25_params.b, bm25_params.tokenizer, bm25_params.stoplist
  - dense_params.metric, dense_params.top_k, dense_params.ef_search
  - combine_policy.method ("weighted_sum"), combine_policy.weights.bm25, combine_policy.weights.dense
  - normalization.method ("zscore"|"maxmin"), normalization.per_field (true|false)
- Candidates[] (per candidate):
  - chunk_id, artifact_id, version
  - span.start_token, span.end_token
  - provenance_path (namespace/path)
  - bm25_score, dense_score, retrieval_score, rank
  - match_reason (explicit_ref|dependency|lexical|semantic|temporal|boosted)
  - selection_effect ("none")
  - notes (optional)
- Aggregates:
  - total_candidates, top_k
  - score_stats.bm25.{min,max,mean,std}
  - score_stats.dense.{min,max,mean,std}
  - score_stats.retrieval.{min,max,mean,std}
  - normalization_applied (bool), warnings[]
- Guardrails:
  - side_effects_blocked: true
  - writes_performed: 0
  - index_mutations: 0
  - embedding_creations: 0

4) Embeddings/index policy
- Production embedding creation and index mutation: Out of scope and forbidden for this slice.
- Tests: Mock/file-based embeddings and ephemeral in-memory indexes are allowed for tests and local dev.

5) Token budget telemetry
- Not required in this slice. Defer explicitly.
- Deferral note: No token-budget fields or effects are added; future slice may add manifest.telemetry.token_budget.* if admitted.

6) Selection adapter
- Include a pluggable context selection adapter interface with a default no-op implementation.
- Purpose: Allow logging of “selection_effect=none” and future injection; must not alter selection, order, or prompt contents.

7) Governance
- New PLAN: Required (this is a new governed diagnostic slice).
- New WARRANT: Required to pin non-effects.
- Warrant must explicitly forbid:
  - Any automatic L0 retrieval or inclusion in prompts.
  - Any change to context selection algorithms, ordering, or provider prompts.
  - Any index/embedding writes or mutations outside mock/test fixtures.
  - Any write-back (L1, ADR, lineage) or persistent side effects.
  - Enabling the simulator outside test/dev without an explicit feature flag.
  - Cross-namespace data exposure or redaction bypass.

8) Recommended PLAN
- Title: PLAN-20260706-0002 Diagnostic-only L0 Hybrid Retrieval Simulator
- Objective: Implement a feature-flagged, read-only hybrid (BM25 + dense) L0 retrieval simulator that logs per-candidate diagnostics into the context manifest without affecting selection or prompts and without any index/embedding writes.
- Success criteria:
  - CLI/API to run the simulator for a request, producing manifest.diagnostics.l0_retrieval_simulator.
  - BM25 and dense scores computed against a fixed corpus snapshot or mocks; configurable combine_policy and normalization.
  - Reranking disabled and clearly marked as deferred.
  - No selection or prompt changes; selection_effect logged as "none".
  - Tests proving zero writes (index/embeddings), correct logging schema, feature-flag default off.
  - Self-model verification and a minimal warrant stating prohibitions above.
- Out-of-scope boundary:
  - Automatic L0 retrieval or any selection changes.
  - Provider prompt changes.
  - Production embedding creation or index mutation.
  - Reranking implementations.
  - Token budget telemetry integration.
  - Write-back pipelines (L1, ADR, embeddings, lineage).
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Gating Assumption Resolution: Diagnostic-Only L0 Hybrid Retrieval Simulator

## 1. GAP-0001 Status

**Current target after read-only diagnostics completion:**
GAP-0001 originally targeted "read-only, context-manifest-connected L0 candidate diagnostics." PLAN-20260706-0001 completed this target.

**Stale targets:**
Yes. Any `recommended_next_targets` referring to "read-only diagnostics" or "context-manifest telemetry" are stale.

**Replacement target:**
`"Diagnostic-only hybrid retrieval simulation with mock embeddings and manifest-logged candidate scoring (BM25 + dense), no automatic selection, no provider prompt changes."`

---

## 2. ABS-0003 / Retrieval Algorithm

**Algorithm scope for this simulator:**
**BM25 + dense only** (no reranking).

**Rationale:**
- ABS-0003 states: *"hybrid retrieval is used (BM25 + dense) with reranking in the more detailed plan."*
- Reranking is specified in the "more detailed plan" (COMP-0006/COMP-0007 OpenAI responses).
- **COMP-0021 and SYNCOMP-0012 are excluded by policy** (no admission verdict).
- Without admitted governing artifacts specifying reranking implementation, **defer reranking explicitly**.

**Explicit deferral:**
Reranking (score fusion, cross-encoder models, or learned ranking) is **out of scope** for this diagnostic slice. Future reranking requires a separate PLAN and admitted governing artifact.

---

## 3. Manifest Logging Schema

**Canonical section:**
`context_pack.selection_diagnostics.retrieval_candidates[]`

**Per-candidate fields:**

```json
{
  "chunk_id": "string (L0 chunk identifier)",
  "source_path": "string (file path or artifact URI)",
  "bm25_score": "float | null (lexical match score)",
  "dense_score": "float | null (embedding cosine similarity)",
  "retrieval_score": "float (combined score, e.g., weighted sum or max)",
  "match_reason": "string (e.g., 'bm25_keyword_match', 'dense_semantic_match', 'hybrid_top_k')",
  "selection_effect": "string enum: 'included' | 'excluded_by_budget' | 'excluded_by_dedup' | 'excluded_by_score_threshold' | 'candidate_only'",
  "provenance": {
    "artifact_id": "string | null",
    "namespace": "string",
    "version": "string | null"
  }
}
```

**Additional top-level telemetry fields:**

```json
{
  "retrieval_query": "string (user query or reformulated query)",
  "retrieval_method": "string (e.g., 'hybrid_bm25_dense')",
  "total_candidates": "integer",
  "included_count": "integer",
  "excluded_count": "integer",
  "retrieval_timestamp": "ISO 8601 string"
}
```

---

## 4. Embeddings/Index Policy

**Production embedding creation:**
**Out of scope.** No production embedding generation, no vector index mutation, no external embedding service calls.

**Mock/file-based embeddings:**
**Allowed for tests.** Test fixtures may include:
- Pre-computed mock embedding vectors (JSON/numpy arrays).
- Stub dense retrieval returning fixed scores based on query/chunk keyword overlap or random assignment.
- File-based mock index (e.g., a JSON manifest of chunk_id → mock_vector).

**Boundary:**
All embeddings and dense scores must be traceable to mock fixtures or test stubs. Implementations must not invoke embedding models or modify persistent vector stores.

---

## 5. Token Budget Telemetry

**Requirement:**
**No.** Token budget telemetry is **deferred** to a future slice.

**Rationale:**
- Current boundaries confirm no context selection changes or provider prompt changes.
- Token budgeting (per ABS-0003: "15% system, 10% answer, 75% context") requires selection adapter integration.
- Diagnostic retrieval simulation logs candidate scores and selection effects but does not enforce or log token allocation.

**Explicit deferral:**
Token budget enforcement, allocation percentages, and per-section token consumption telemetry are **out of scope**. Future work requires a PLAN admitting selection adapter integration and manifest token fields.

---

## 6. Selection Adapter

**Recommendation:**
**Defer to a separate PLAN.**

**Rationale:**
- A pluggable context selection adapter touches provider prompt assembly and context packing logic.
- Current boundary: "Context selection changes are NOT implemented."
- Introducing even a no-op adapter risks scope creep into automatic behavior.

**Explicit deferral:**
Selection adapter interface definition, no-op stub, and integration hooks are **out of scope**. Future PLAN must define adapter contract, call sites, and warrant forbidding automatic selection without explicit user/config opt-in.

---

## 7. Governance

**New PLAN required:**
**Yes.**

**New WARRANT required:**
**Yes.**

**Warrant must explicitly forbid:**

1. **Automatic L0 retrieval in production context packs** — simulator output must be logged to diagnostics only; no automatic inclusion of retrieved candidates in provider prompts.
2. **Modification of provider prompt assembly logic** — no changes to context pack assembly, inclusion rules, or prompt formatting outside diagnostic logging.
3. **Production embedding generation or index writes** — no external embedding API calls, no vector store mutations.
4. **Token budget enforcement or selection policy changes** — no integration with context selection, packing, or budget allocation logic.
5. **Reranking or learned ranking** — hybrid retrieval is limited to BM25 + dense score combination; no cross-encoder, LLM-as-judge, or learned reranker.

---

## 8. Recommended PLAN

**PLAN ID suggestion:**
`PLAN-20260707-0001`

**Title:**
`"Diagnostic-Only L0 Hybrid Retrieval Simulator with Mock Embeddings and Manifest Logging"`

**Objective:**
Implement a read-only hybrid retrieval simulator (BM25 + dense) that scores L0 chunk candidates against a user query, logs per-candidate scores and selection effects to `context_pack.selection_diagnostics.retrieval_candidates[]`, and uses mock embeddings for dense retrieval. Output is diagnostic-only and does not alter provider prompts or context selection.

**Success Criteria:**

1. Simulator accepts:
   - User query string
   - Corpus of L0 chunks with mock embeddings
   - Retrieval parameters (top-k, score weights)

2. Simulator outputs:
   - Per-candidate: `chunk_id`, `source_path`, `bm25_score`, `dense_score`, `retrieval_score`, `match_reason`, `selection_effect`, `provenance`
   - Top-level: `retrieval_query`, `retrieval_method`, `total_candidates`, `included_count`, `excluded_count`, `retrieval_timestamp`

3. All dense scores derived from mock embeddings (file-based fixtures or test stubs).

4. Simulator integrated into a test harness; output serialized to context pack diagnostics section.

5. No changes to:
   - Provider prompt assembly
   - Context pack inclusion rules
   - Production embedding generation
   - Vector index persistence

6. Documentation:
   - Simulator CLI/API reference
   - Mock embedding fixture format
   - Diagnostic output schema
   - Deferred features: reranking, token budgeting, selection adapter integration

**Out of Scope:**

- Reranking (cross-encoder, learned ranking, score fusion beyond weighted sum).
- Token budget enforcement or telemetry.
- Selection adapter interface or integration.
- Production embedding generation or vector index mutation.
- Automatic inclusion of retrieved candidates in provider prompts.
- Changes to context selection, packing, or assembly logic.
- Integration with GAP-0001 targets beyond diagnostic logging.

**Dependencies:**
- PLAN-20260705-0001 (completed)
- PLAN-20260706-0001 (completed)
- ABS-0003 (admitted, warrant-supported)

**Estimated Effort:**
3–5 engineering days (BM25 scoring, mock dense retrieval stub, manifest schema extension, test fixtures, documentation).

---

**END OF GATING RESOLUTION**
````
