# COMP-0023: Provider Comparison — Finalize unresolved gating for L0 retrieval simulator

## Metadata

- comparison_id: `COMP-0023`
- title: `Finalize unresolved gating for L0 retrieval simulator`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- context_manifest: `docs/comparisons/COMP-0023-finalize-unresolved-gating-for-l0-retrieval-simulator.context.json`
- created_at: `2026-07-06T08:03:06.611894+00:00`
- command: `scripts/compare_providers.py --latest-context --require-admission --title Finalize unresolved gating for L0 retrieval simulator Finalize unresolved gating for the next diagnostic-only L0 Hybrid Retrieval Simulator slice.

Maintain current boundaries:
- No automatic L0 retrieval.
- No context selection changes.
- No provider prompt changes.
- No production embedding creation.
- No vector/index mutation.
- Reranking is deferred unless explicitly admitted.
- Token budget telemetry is deferred unless explicitly admitted.

Prior artifacts:
- COMP-0021 / SYNCOMP-0012: backlog prioritization.
- COMP-0022 / SYNCOMP-0013: L0 retrieval simulator gating.

Resolve only these remaining decisions:

1. Manifest schema path:
   Choose ONE canonical location:
   - manifest.diagnostics.l0_retrieval_simulator
   - context_pack.selection_diagnostics.retrieval_candidates
   Provide exact section path and any compatibility alias, if allowed.

2. Per-candidate selection_effect semantics:
   For this slice, should selection_effect be fixed as "none"?
   Or should it use a richer enum?
   Give exact allowed value(s).

3. Schema fields:
   Approve or reject these fields:
   - header: simulator_id, run_id, timestamp_utc, request_id, episode_id, manifest_id, manifest_version, query_text, query_kind, algorithm, reranker, corpus_snapshot_id, l0_index_namespace
   - embedding_model: name, version, dimension
   - bm25_params: k1, b, tokenizer, stoplist
   - dense_params: metric, top_k, ef_search
   - combine_policy: method, weights.bm25, weights.dense
   - normalization: method, per_field
   - candidates: chunk_id, artifact_id, version, span.start_token, span.end_token, provenance_path, bm25_score, dense_score, retrieval_score, rank, match_reason, selection_effect, notes
   - aggregates: total_candidates, top_k, score_stats, normalization_applied, warnings
   - guardrails: side_effects_blocked, writes_performed, index_mutations, embedding_creations

4. Selection adapter:
   Decide yes/no:
   - Include a no-op, not-wired adapter interface in this slice.
   - Or defer entirely to a separate PLAN.
   Provide warrant impact.

5. Combine policy defaults:
   Choose one:
   - explicit required config only, no defaults
   - default equal weights
   - another concrete default
   Also choose normalization default or require explicit config.

6. GAP-0001 wording:
   Provide exact replacement wording for recommended_next_targets after completed read-only diagnostics.

7. Governance text:
   Provide exact warrant prohibition snippets for:
   - no prompt inclusion
   - no context selection changes
   - no production embeddings/index mutation
   - no reranking
   - no token budget enforcement/telemetry
   - no selection adapter integration, if deferred
   - no cross-namespace/redaction bypass
   - no persistent write-back

8. Final PLAN record wording:
   Provide exact:
   - plan_id suggestion
   - title
   - objective
   - proposed_change
   - rationale bullets
   - constraints
   - success_criteria
   - risk
   - next_action

Output should be concise and directly convertible into PLAN and WARRANT records.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Finalize unresolved gating for the next diagnostic-only L0 Hybrid Retrieval Simulator slice.

Maintain current boundaries:
- No automatic L0 retrieval.
- No context selection changes.
- No provider prompt changes.
- No production embedding creation.
- No vector/index mutation.
- Reranking is deferred unless explicitly admitted.
- Token budget telemetry is deferred unless explicitly admitted.

Prior artifacts:
- COMP-0021 / SYNCOMP-0012: backlog prioritization.
- COMP-0022 / SYNCOMP-0013: L0 retrieval simulator gating.

Resolve only these remaining decisions:

1. Manifest schema path:
   Choose ONE canonical location:
   - manifest.diagnostics.l0_retrieval_simulator
   - context_pack.selection_diagnostics.retrieval_candidates
   Provide exact section path and any compatibility alias, if allowed.

2. Per-candidate selection_effect semantics:
   For this slice, should selection_effect be fixed as "none"?
   Or should it use a richer enum?
   Give exact allowed value(s).

3. Schema fields:
   Approve or reject these fields:
   - header: simulator_id, run_id, timestamp_utc, request_id, episode_id, manifest_id, manifest_version, query_text, query_kind, algorithm, reranker, corpus_snapshot_id, l0_index_namespace
   - embedding_model: name, version, dimension
   - bm25_params: k1, b, tokenizer, stoplist
   - dense_params: metric, top_k, ef_search
   - combine_policy: method, weights.bm25, weights.dense
   - normalization: method, per_field
   - candidates: chunk_id, artifact_id, version, span.start_token, span.end_token, provenance_path, bm25_score, dense_score, retrieval_score, rank, match_reason, selection_effect, notes
   - aggregates: total_candidates, top_k, score_stats, normalization_applied, warnings
   - guardrails: side_effects_blocked, writes_performed, index_mutations, embedding_creations

4. Selection adapter:
   Decide yes/no:
   - Include a no-op, not-wired adapter interface in this slice.
   - Or defer entirely to a separate PLAN.
   Provide warrant impact.

5. Combine policy defaults:
   Choose one:
   - explicit required config only, no defaults
   - default equal weights
   - another concrete default
   Also choose normalization default or require explicit config.

6. GAP-0001 wording:
   Provide exact replacement wording for recommended_next_targets after completed read-only diagnostics.

7. Governance text:
   Provide exact warrant prohibition snippets for:
   - no prompt inclusion
   - no context selection changes
   - no production embeddings/index mutation
   - no reranking
   - no token budget enforcement/telemetry
   - no selection adapter integration, if deferred
   - no cross-namespace/redaction bypass
   - no persistent write-back

8. Final PLAN record wording:
   Provide exact:
   - plan_id suggestion
   - title
   - objective
   - proposed_change
   - rationale bullets
   - constraints
   - success_criteria
   - risk
   - next_action

Output should be concise and directly convertible into PLAN and WARRANT records.

## OpenAI Response

- model: `gpt-5`

```
Decisions for the diagnostic-only L0 Hybrid Retrieval Simulator slice

1) Manifest schema path
- Canonical: manifest.diagnostics.l0_retrieval_simulator
- Compatibility alias (read-only, deprecated): context_pack.selection_diagnostics.retrieval_candidates → alias to manifest.diagnostics.l0_retrieval_simulator

2) Per-candidate selection_effect semantics
- Allowed values: ["none"] (fixed)

3) Schema fields: approval and constraints
- header: simulator_id, run_id, timestamp_utc, request_id, episode_id, manifest_id, manifest_version, query_text, query_kind, algorithm, reranker, corpus_snapshot_id, l0_index_namespace
  - Approved with constraints:
    - reranker = "none" only
    - corpus_snapshot_id required if candidates are present
    - l0_index_namespace must reference a read-only snapshot namespace
    - algorithm is descriptive only (no execution implied)
- embedding_model: name, version, dimension
  - Approved (metadata only; no embedding creation)
- bm25_params: k1, b, tokenizer, stoplist
  - Approved (diagnostic metadata only)
- dense_params: metric, top_k, ef_search
  - Approved (diagnostic metadata only; no index mutation)
- combine_policy: method, weights.bm25, weights.dense
  - Approved (simulated scoring only; see defaults decision)
- normalization: method, per_field
  - Approved (diagnostic metadata; see defaults decision)
- candidates: chunk_id, artifact_id, version, span.start_token, span.end_token, provenance_path, bm25_score, dense_score, retrieval_score, rank, match_reason, selection_effect, notes
  - Approved with constraints:
    - selection_effect = "none" only
    - retrieval_score and rank are simulated diagnostics (no selection impact)
- aggregates: total_candidates, top_k, score_stats, normalization_applied, warnings
  - Approved
- guardrails: side_effects_blocked, writes_performed, index_mutations, embedding_creations
  - Approved with constraints:
    - side_effects_blocked = true
    - writes_performed = 0
    - index_mutations = 0
    - embedding_creations = 0

4) Selection adapter
- Decision: Defer entirely to a separate PLAN (no no-op interface in this slice)
- Warrant impact: Explicit prohibition on any selection adapter integration or invocation

5) Combine policy defaults
- Combine policy: explicit required config only (no implicit defaults)
- Normalization: explicit required config only (no implicit defaults)

6) GAP-0001 wording (replacement for recommended_next_targets)
- Recommended next targets after read-only diagnostics:
  - Design a governed evaluation slice that admits a pluggable selection adapter and offline reranker evaluation against synthetic/read-only corpora, with strict write protection and no prompt/context changes.
  - Prepare schema extensions for a richer selection_effect enum and reranker telemetry, gated behind explicit PLAN and WARRANT.

7) Governance warrant prohibitions (exact snippets)
- No prompt inclusion: Simulator outputs SHALL NOT be included in any provider prompt.
- No context selection changes: This slice SHALL NOT modify selection logic, inputs, or outcomes.
- No production embeddings/index mutation: This slice SHALL NOT create embeddings in production namespaces nor mutate any vector or document index.
- No reranking: This slice SHALL NOT perform reranking nor record reranker telemetry; reranker MUST be "none".
- No token budget enforcement/telemetry: This slice SHALL NOT enforce token budgets nor emit token budget telemetry.
- No selection adapter integration: This slice SHALL NOT integrate, call, or ship any selection adapter; such work is deferred.
- No cross-namespace/redaction bypass: This slice SHALL NOT bypass namespace ACLs or redaction boundaries under any circumstance.
- No persistent write-back: This slice SHALL NOT persist artifacts; diagnostics are per-request/ephemeral within the manifest only.

8) Final PLAN record wording
- plan_id (suggested): PLAN-20260706-0002
- title: Diagnostic-only L0 Hybrid Retrieval Simulator — Manifest Diagnostics
- objective: Add a read-only, per-request manifest diagnostics section to capture simulated hybrid L0 candidate metadata and scores without affecting prompts, selection, or indexes.
- proposed_change:
  - Introduce manifest.diagnostics.l0_retrieval_simulator with approved fields and constraints.
  - Provide a read-only compatibility alias at context_pack.selection_diagnostics.retrieval_candidates (deprecated).
  - Emit diagnostics only when explicitly requested; no defaults for combine_policy or normalization.
  - Enforce governance prohibitions via guardrails fields and tests.
- rationale:
  - Enables reproducible, read-only diagnostics aligned with context-manifest usage.
  - Keeps separation from selection to avoid ambiguity with production behavior.
  - Prepares ground for later governed adapter/reranker evaluation with clear telemetry.
  - Aligns with reconciled memory loop abstractions while remaining diagnostic-only.
- constraints:
  - No automatic L0 retrieval; inputs are simulated or externally provided.
  - No context selection changes or prompt inclusion.
  - No production embedding creation or index mutation.
  - Reranking deferred; reranker must be "none".
  - No token budget enforcement or telemetry.
  - No selection adapter integration in this slice.
  - No cross-namespace/redaction bypass.
  - No persistent write-back; manifest records are ephemeral.
- success_criteria:
  - Manifest entries validate against the approved schema with guardrails indicating zero side effects.
  - selection_effect is always "none".
  - combine_policy and normalization are present only when explicitly supplied; no implicit defaults applied.
  - Self-model updated to reflect diagnostic-only capability with no provider prompt or selection changes.
- risk:
  - Risk of confusion with selection semantics; mitigated by canonical path under manifest.diagnostics and deprecating the alias.
  - Risk of implicit policy creep; mitigated by requiring explicit config and prohibitions in WARRANT.
- next_action:
  - Implement schema emission and validation tests for manifest.diagnostics.l0_retrieval_simulator.
  - Add WARRANT with the exact prohibitions above.
  - Update SELF_MODEL.json and verification to reflect read-only diagnostics completion.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Diagnostic-Only L0 Hybrid Retrieval Simulator Slice: Final Gating Decisions

## 1. Manifest Schema Path

**Canonical location:**
```
manifest.diagnostics.l0_retrieval_simulator
```

**Compatibility alias (read-only):**
```
context_pack.selection_diagnostics.retrieval_candidates
```

**Rationale:** Aligns with diagnostic scope; `manifest.diagnostics.*` namespaces non-production telemetry. Alias permitted for backward read compatibility but schema generation targets canonical path only.

---

## 2. Per-Candidate selection_effect Semantics

**Fixed value for this slice:**
```
"none"
```

**Type:** `enum` with single admitted value `"none"`

**Rationale:** This slice performs read-only diagnostics. Any selection_effect other than "none" implies context selection mutation, violating slice boundaries. Future slices may expand enum to `["none", "included", "excluded", "boosted", "penalized"]` under separate governance.

---

## 3. Schema Fields Approval

### APPROVED fields:

**Header:**
- `simulator_id`, `run_id`, `timestamp_utc`, `request_id`, `episode_id`, `manifest_id`, `manifest_version`, `query_text`, `query_kind`, `algorithm`, `corpus_snapshot_id`, `l0_index_namespace`

**Embedding model:**
- `embedding_model.name`, `embedding_model.version`, `embedding_model.dimension`

**BM25 params:**
- `bm25_params.k1`, `bm25_params.b`, `bm25_params.tokenizer`, `bm25_params.stoplist`

**Dense params:**
- `dense_params.metric`, `dense_params.top_k`, `dense_params.ef_search`

**Combine policy:**
- `combine_policy.method`, `combine_policy.weights.bm25`, `combine_policy.weights.dense`

**Normalization:**
- `normalization.method`, `normalization.per_field`

**Candidates:**
- `chunk_id`, `artifact_id`, `version`, `span.start_token`, `span.end_token`, `provenance_path`, `bm25_score`, `dense_score`, `retrieval_score`, `rank`, `match_reason`, `selection_effect`, `notes`

**Aggregates:**
- `total_candidates`, `top_k`, `score_stats`, `normalization_applied`, `warnings`

**Guardrails:**
- `side_effects_blocked`, `writes_performed`, `index_mutations`, `embedding_creations`

### REJECTED fields:

**Header:**
- `reranker` — **REJECTED.** Reranking deferred unless explicitly admitted; field presence implies capability not in scope.

---

## 4. Selection Adapter

**Decision:** **DEFER entirely to separate PLAN.**

**Rationale:** A no-op, not-wired interface suggests future integration and risks scope creep. Clean boundary: this slice produces diagnostics; a future PLAN explicitly governs adapter interface, wiring, and warrant prerequisites.

**Warrant impact:** No adapter-related prohibitions needed; omission is sufficient.

---

## 5. Combine Policy Defaults

**Combine policy:**
- **Require explicit configuration; no defaults.**

**Normalization:**
- **Require explicit configuration; no defaults.**

**Rationale:** Diagnostic slice prioritizes transparency over convenience. Implicit defaults obscure algorithmic behavior under audit. Explicit config ensures each run documents exact retrieval semantics.

---

## 6. GAP-0001 Wording Replacement

**Exact replacement for `recommended_next_targets` after completed read-only diagnostics:**

```
"Automatic L0 retrieval integration with context selection and provider prompt assembly; requires: (a) separate PLAN with explicit admission of context selection changes, provider prompt changes, and automatic retrieval behavior; (b) WARRANT certifying compliance with citation integrity, ACL filtering, token budgeting, and deduplication constraints per ABS-0003; (c) selection adapter interface definition and integration tests; (d) reranking admission if candidate ordering affects selection."
```

---

## 7. Governance Text: Warrant Prohibition Snippets

### No prompt inclusion:
```
"Diagnostic output shall not be included in provider prompts, system messages, or user-facing context. Retrieval candidates are logged for audit only."
```

### No context selection changes:
```
"This implementation shall not modify context selection logic, candidate filtering, or inclusion/exclusion rules. selection_effect shall remain fixed at 'none'."
```

### No production embeddings/index mutation:
```
"No embeddings shall be generated, updated, or persisted. No vector index writes, deletions, or metadata mutations are permitted. Existing production embeddings and indices shall be read-only."
```

### No reranking:
```
"Reranking logic shall not be invoked. Candidate ordering reflects raw retrieval scores only. Future reranking requires separate PLAN admission and governance."
```

### No token budget enforcement/telemetry:
```
"Token budget calculation, enforcement, and telemetry are deferred. Candidates shall not be truncated, packed, or scored based on token budget constraints."
```

### No cross-namespace/redaction bypass:
```
"ACL filtering and namespace isolation are out of scope for this diagnostic slice. No redaction, clearance-based filtering, or cross-namespace access control logic shall be implemented or tested."
```

### No persistent write-back:
```
"Diagnostic output shall be ephemeral or written to transient logs only. No write-back to L0, L1, manifest, lineage, or audit records is permitted."
```

---

## 8. Final PLAN Record Wording

### plan_id:
```
PLAN-20260706-0002
```

### title:
```
L0 Hybrid Retrieval Simulator (Diagnostic-Only)
```

### objective:
```
Implement read-only hybrid retrieval (BM25 + dense) simulator producing diagnostic manifests for L0 chunk candidate scoring, ranking, and match attribution, with no context selection, prompt assembly, embedding generation, index mutation, or persistent write-back.
```

### proposed_change:
```
Add manifest schema at manifest.diagnostics.l0_retrieval_simulator, simulator runtime (query → BM25 + dense retrieval → score normalization → candidate logging), guardrails enforcing no side effects, and JSON output format. Canonical schema fields per Section 3 (approved), with selection_effect fixed at "none" and reranker field omitted. Combine policy and normalization require explicit configuration (no defaults).
```

### rationale:
```
- Diagnostic-only slice enables auditable scoring/ranking visibility for future automatic L0 retrieval without coupling to context selection or prompt assembly.
- Fixed selection_effect "none" enforces read-only constraint and defers selection integration to separate PLAN.
- Explicit config-only policy documents retrieval algorithm semantics for each run.
- Guardrails block embedding creation, index writes, and write-back, ensuring no production data mutation.
- Compatibility alias (context_pack.selection_diagnostics.retrieval_candidates) supports prior tooling without schema migration.
```

### constraints:
```
- No automatic L0 retrieval triggered by provider requests.
- No context selection logic changes; selection_effect fixed at "none".
- No provider prompt assembly or inclusion of diagnostic output.
- No production embedding generation or vector/index mutation.
- No reranking invocation (field omitted from schema).
- No token budget enforcement or telemetry.
- No ACL filtering, namespace isolation, or redaction logic.
- No selection adapter interface (deferred to separate PLAN).
- No persistent write-back to L0, L1, manifest, lineage, or audit records.
- Combine policy and normalization parameters require explicit configuration; no defaults provided.
```

### success_criteria:
```
1. manifest.diagnostics.l0_retrieval_simulator schema validated against approved fields (Section 3).
2. Simulator accepts query_text, algorithm, bm25_params, dense_params, combine_policy, normalization; produces candidates with bm25_score, dense_score, retrieval_score, rank, match_reason.
3. All candidates have selection_effect = "none".
4. guardrails section logs side_effects_blocked = true, writes_performed = 0, index_mutations = 0, embedding_creations = 0.
5. Output written to transient log or ephemeral file; no persistent write-back to production records.
6. VERIFY artifact confirms: schema compliance, guardrail enforcement, no side effects.
7. WARRANT prohibits: prompt inclusion, context selection changes, embedding/index mutation, reranking, token budget enforcement, ACL/redaction logic, adapter integration, persistent write-back.
8. GAP-0001 updated with recommended_next_targets wording per Section 6.
```

### risk:
```
Future work may conflate diagnostic retrieval_score with selection_effect unless clear governance distinguishes read-only scoring from actionable candidate filtering. WARRANT must explicitly prohibit automatic promotion of diagnostics into context selection logic without separate PLAN admission.
```

### next_action:
```
1. Create PLAN-20260706-0002.json with wording from Section 8.
2. Create WARR-20260706-0003.json with prohibitions from Section 7 plus promoted_at, artifact_coverage, and compliance_checks.
3. Implement schema, simulator, guardrails; validate with test query producing diagnostic manifest.
4. Create VERIFY-20260706-0002.json confirming success_criteria 1–7.
5. Update GAP-0001 recommended_next_targets with Section 6 wording.
6. Mark PLAN-20260706-0002 completed; regenerate SELF_MODEL.json.
```

---

**End of gating resolution. All decisions are implementation-ready.**
````
