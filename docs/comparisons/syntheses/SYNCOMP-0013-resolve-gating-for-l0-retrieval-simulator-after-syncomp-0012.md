# SYNCOMP-0013: Comparison Synthesis — Resolve Gating For L0 Retrieval Simulator After Syncomp 0012

## Metadata

- synthesis_id: `SYNCOMP-0013`
- title: `Resolve Gating For L0 Retrieval Simulator After Syncomp 0012`
- created_at: `2026-07-06T07:52:35.630572+00:00`
- command: `scripts/synthesize_comparison.py --provider openai docs/comparisons/COMP-0022-resolve-gating-for-l0-retrieval-simulator-after-syncomp-0012.md`
- source_comparison: `docs/comparisons/COMP-0022-resolve-gating-for-l0-retrieval-simulator-after-syncomp-0012.md`
- synthesizer_provider: `OpenAI`
- synthesizer_model: `gpt-5`

## Synthesis

~~~text
1) Shared agreement
- Scope: Implement a diagnostic-only L0 hybrid retrieval simulator now; no automatic L0 retrieval; no context selection or provider prompt changes.
- Retrieval algorithm: BM25 + dense only; reranking is explicitly deferred to a future governed slice.
- Embeddings/index: Production embedding creation and index mutation are out of scope; mock/file-based embeddings and ephemeral/in-memory indices are allowed for tests.
- Token telemetry: Not required for this slice; explicitly deferred.
- Governance: New PLAN and new WARRANT are required.
- Warrant prohibitions (overlap): Forbid automatic L0 inclusion in prompts; forbid any change to context selection/prompt assembly; forbid production embedding/index writes; forbid reranking in this slice; enforce feature-flag/test-only usage.

2) Meaningful differences
- GAP-0001 status:
  - OpenAI: Remaining target is to implement the read-only L0 hybrid retrieval simulator.
  - Claude: Original GAP-0001 target is completed; recommended_next_targets about read-only diagnostics are stale; replacement target is the diagnostic-only hybrid simulator.
- Selection adapter:
  - OpenAI: Include a pluggable context selection adapter with a default no-op implementation.
  - Claude: Defer adapter (even no-op) to a separate PLAN to avoid scope creep.
- Manifest logging schema:
  - OpenAI: Location manifest.diagnostics.l0_retrieval_simulator with rich header/params/candidates/aggregates/guardrails; per-candidate selection_effect="none".
  - Claude: Location context_pack.selection_diagnostics.retrieval_candidates[] with leaner top-level telemetry; per-candidate selection_effect includes exclusion reasons (e.g., excluded_by_budget), despite no behavioral selection in this slice.
- Governance emphasis:
  - OpenAI: Adds explicit forbiddance for cross-namespace exposure/redaction bypass and environment gating (feature flag).
  - Claude: Adds explicit forbiddance for token-budget enforcement and reranking under the warrant.
- PLAN metadata:
  - OpenAI: PLAN-20260706-0002; title emphasizes “Diagnostic-only L0 Hybrid Retrieval Simulator.”
  - Claude: PLAN-20260707-0001; title emphasizes mock embeddings and manifest logging.

3) Stronger points from OpenAI
- Detailed, implementation-ready manifest schema: clear namespacing, parameters (bm25_params, dense_params), combine_policy, normalization, aggregates, and guardrails (side_effects_blocked, writes_performed, index_mutations, embedding_creations).
- Governance guardrails include cross-namespace/redaction constraints and feature-flag default-off requirement.
- Forward-compat hooks: suggests a pluggable selection adapter interface to future-proof integration (while keeping behavior no-op).

4) Stronger points from Claude
- Clear admission discipline: ties ABS-0003 admission to deferring reranking due to lack of admitted governing artifacts.
- Testability discipline: mandates dense scores trace to mock fixtures; prohibits any external embedding calls.
- Concise success criteria focused on simulator inputs/outputs and test harness integration.
- Simpler schema colocated with selection diagnostics, emphasizing compatibility with existing diagnostics sections.

5) Combined answer
- GAP-0001:
  - Remaining target after read-only diagnostics: Implement the diagnostic-only L0 hybrid retrieval simulator that computes BM25 and dense scores for L0 candidates and logs results to the manifest; zero selection/prompt effects; zero index/embedding writes.
  - Staleness: Any recommended_next_targets that refer to “read-only L0 diagnostics” are stale.
  - Replacement target: Diagnostic-only L0 hybrid retrieval simulator with manifest-connected logging; feature-flagged; test/dev only.
- ABS-0003 / retrieval algorithm:
  - Simulator includes BM25 + dense hybrid only; reranking explicitly deferred and not implemented in this slice. Governing admission: ABS-0003 admits hybrid; reranking lacks current admission for this slice.
- Manifest logging schema (canonical for this slice):
  - Section path: manifest.diagnostics.l0_retrieval_simulator.
  - Header: simulator_id; run_id; timestamp_utc; request_id; episode_id; manifest_id; manifest_version; query_text; query_kind; algorithm="bm25+dense"; reranker="none"; corpus_snapshot_id; l0_index_namespace; embedding_model.{name,version,dimension}; bm25_params.{k1,b,tokenizer,stoplist}; dense_params.{metric,top_k,ef_search}; combine_policy.{method="weighted_sum",weights.{bm25,dense}}; normalization.{method,per_field}.
  - Candidates[]: chunk_id; artifact_id; version; span.{start_token,end_token}; provenance_path; bm25_score; dense_score; retrieval_score; rank; match_reason; selection_effect="none"; notes(optional).
  - Aggregates: total_candidates; top_k; score_stats.{bm25,dense,retrieval}.{min,max,mean,std}; normalization_applied(bool); warnings[].
  - Guardrails: side_effects_blocked=true; writes_performed=0; index_mutations=0; embedding_creations=0.
  - Compatibility note: Fields from Claude’s schema (e.g., source_path, included/excluded counts) may be added as optional aliases mapped to provenance_path and aggregates.included_count/excluded_count; since selection is no-op, set included/excluded counts to 0 and selection_effect="none".
- Embeddings/index policy:
  - Production embedding creation and index mutation: Out of scope and forbidden.
  - Tests: Mock/file-based embeddings and ephemeral in-memory indices allowed; all dense scores must be attributable to mocks/stubs (no external embedding API calls).
- Token budget telemetry:
  - Not required; explicitly deferred. No manifest.telemetry.token_budget fields added in this slice.
- Selection adapter:
  - Decision: Defer to a separate PLAN to avoid touching selection/packing. No adapter interface or hooks included in this slice.
  - Note: Future PLAN may introduce a pluggable adapter; warrant must preserve no automatic selection without explicit opt-in.
- Governance:
  - New PLAN: Required.
  - New WARRANT: Required; must explicitly forbid:
    - Any automatic L0 retrieval or inclusion in prompts.
    - Any changes to context selection algorithms, ordering, packing, or provider prompts.
    - Any production embedding creation or index mutations; any external embedding/vector service calls.
    - Any reranking or learned ranking in this slice.
    - Any token-budget enforcement or telemetry integration.
    - Enabling simulator outside test/dev without explicit feature flag.
    - Cross-namespace data exposure or redaction bypass.
    - Any write-backs (L1, ADR, lineage) or other persistent side effects.
- Recommended PLAN:
  - Title: PLAN-20260706-0002 Diagnostic-only L0 Hybrid Retrieval Simulator.
  - Objective: Implement a feature-flagged, read-only hybrid (BM25 + dense) L0 retrieval simulator that computes and logs per-candidate scores to manifest.diagnostics.l0_retrieval_simulator using mock embeddings, with no selection/prompt effects and no index/embedding writes.
  - Success criteria:
    - CLI/API to run simulator per request; outputs manifest.diagnostics.l0_retrieval_simulator conforming to schema above.
    - BM25 and dense scores computed against a fixed corpus snapshot or mocks; configurable combine_policy and normalization; reranking disabled and marked deferred.
    - Tests: prove zero writes (index/embeddings), feature-flag default off, dense scores derived from mock fixtures, schema contract validated.
    - Governance: warrant containing prohibitions listed; self-verification notes.
  - Out of scope:
    - Automatic L0 retrieval or any selection changes; provider prompt changes.
    - Production embedding creation or index mutation; external embedding calls.
    - Reranking; token budget telemetry or enforcement.
    - Selection adapter interface/integration.
    - Any write-back pipelines.

6) Risks or missing assumptions
- GAP-0001 semantics: Minor disagreement on whether the “remaining target” vs “replacement target” framing matters; operationally the next target is the diagnostic-only hybrid simulator.
- Manifest schema location: OpenAI vs Claude paths differ; this synthesis adopts manifest.diagnostics.l0_retrieval_simulator; if downstream consumers expect context_pack.selection_diagnostics, add an adapter or alias field.
- selection_effect semantics: With no selection integration, value is "none"; Claude’s richer enum implies future integration. Consumers must not infer inclusion/exclusion from this slice.
- Combine policy defaults: Weights and normalization defaults are unspecified in artifacts; inference: default to equal weights and z-score or max-min normalization only if configured. Require explicit configuration to avoid silent assumptions. (Inference)
- Parameter set: bm25_params/dense_params presence is agreed; exact defaults (k1, b, top_k, metric) are not specified; require configuration or safe test defaults. (Inference)
- Mock embeddings provenance: Ensure manifest captures embedding_model fields even when mocked; tie mocks to corpus_snapshot_id for reproducibility.
- Reranking governance: Future admission must cite the governing artifact; both providers defer but name different references; keep reranking blocked by warrant until admitted.
- Feature flag discipline: Ensure simulator cannot be enabled in production environments without explicit override and audit.
- Cross-namespace/redaction: Only OpenAI stated this; include in warrant to avoid leakage during diagnostics.

7) Suggested re-ask prompt
scripts/compare_providers.py --latest-context --require-admission --title Finalize unresolved gating for Diagnostic-only L0 Hybrid Retrieval Simulator Resolve these specific unresolved items for the next slice. Maintain current boundaries (no automatic retrieval, no selection/prompt changes, no production embedding/index writes).

Decide:
1) Manifest schema path and fields:
   - Choose ONE canonical location: manifest.diagnostics.l0_retrieval_simulator (OpenAI) vs context_pack.selection_diagnostics.retrieval_candidates (Claude).
   - Confirm per-candidate selection_effect semantics for this slice: fixed "none" vs richer enum; if richer, specify allowed values and defaults given no selection integration.
   - Approve inclusion of header params (bm25_params, dense_params), combine_policy, normalization, aggregates, and guardrails fields as proposed by OpenAI; list any removals.

2) Selection adapter:
   - Include a no-op, not-wired adapter interface in this slice, or defer entirely to a separate PLAN. Provide rationale and warrant text impact.

3) Combine policy defaults:
   - Approve concrete defaults for weights (bm25, dense) and normalization method, or require explicit configuration with no defaults.

4) GAP-0001 wording:
   - Confirm exact phrasing for remaining target vs replacement target in GAP-0001 after read-only diagnostics.

5) Governance deltas:
   - Confirm warrant must include cross-namespace/redaction forbiddance and explicit ban on token-budget enforcement for this slice.

Output: a single, implementation-ready resolution with explicit yes/no on each decision above, exact field names/paths, and any required warrant text snippets.
~~~

## Source Comparison

~~~markdown
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

~~~
