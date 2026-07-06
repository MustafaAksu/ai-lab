# SYNCOMP-0012: Comparison Synthesis — Ai Lab Backlog Prioritization After Context Manifest L0 Diagnostics

## Metadata

- synthesis_id: `SYNCOMP-0012`
- title: `Ai Lab Backlog Prioritization After Context Manifest L0 Diagnostics`
- created_at: `2026-07-06T07:26:21.889066+00:00`
- command: `scripts/synthesize_comparison.py --provider openai docs/comparisons/COMP-0021-ai-lab-backlog-prioritization-after-context-manifest-l0-diagnostics.md`
- source_comparison: `docs/comparisons/COMP-0021-ai-lab-backlog-prioritization-after-context-manifest-l0-diagnostics.md`
- synthesizer_provider: `OpenAI`
- synthesizer_model: `gpt-5`

## Synthesis

~~~text
1) Shared agreement
- Current state
  - Completed: explicit L0 inclusion; read-only L0 candidate diagnostics; context-manifest-connected L0 diagnostics; PLAN-20260705-0001 and PLAN-20260706-0001 done.
  - Not implemented: automatic L0 retrieval; context selection changes; provider prompt changes.
  - GAP-0001 remains open.
- Next step shape
  - Proceed with a diagnostic-only L0 hybrid retrieval simulator (BM25 + dense), no provider prompt or context selection changes.
  - Log retrieval candidates and scores to manifest/telemetry; do not inject into prompts.
  - ACL/namespace and citation/schema validation are useful near-term, read-only.
  - Execution mode: simulator/diagnostic-only slice before any governed behavior-changing retrieval.

2) Meaningful differences
- Reranking scope in the simulator
  - OpenAI: include reranking per ABS-0003 within the diagnostic simulator.
  - Claude: defer reranking beyond initial hybrid score for this slice.
- Embeddings/index mutation
  - OpenAI: explicitly out-of-scope to create embeddings or mutate indices.
  - Claude: permits a mock/file-based embedding storage interface; bars “production training” but does not explicitly forbid mock embedding creation for tests.
- Governance and warrants
  - Claude: cites existing warrants and calls out new warrant needs for behavior-changing retrieval.
  - OpenAI: does not mention warrants.
- Plan identifiers
  - OpenAI: PLAN-20260708-0001.
  - Claude: PLAN-20260706-0002.
- Foundational scaffolding emphasis
  - OpenAI: telemetry separation (retrieval vs selection), pluggable no-op selection adapter, manifest pinning/versioning, tokenizer/version pinning.
  - Claude: token budget policy telemetry (specific split numbers), explicit context-pack assembly changes for behavior-changing plan, detailed success criteria.
- Behavior-changing candidate path
  - OpenAI: feature-flagged automatic retrieval, disabled by default (non-enforcing).
  - Claude: full automatic retrieval that modifies prompts/selection.

3) Stronger points from OpenAI
- Clear safety rails: no prompt/selection changes; explicit prohibition on embedding creation and index mutation in the simulator.
- Architectural readiness: pluggable no-op selection adapter; retrieval vs selection telemetry separation to prevent metric confusion.
- Reproducibility: manifest pinning/versioning; tokenizer/version pinning; citation/span integrity checks.
- Gradual rollout path: feature-flagged (disabled-by-default) auto-retrieval as a follow-on.

4) Stronger points from Claude
- Governance framing: references to warrants, when a new warrant is needed for behavior changes, and verification artifacts.
- Concrete success criteria for the simulator: retrieval_score, bm25_score, dense_score; manifest section for candidate_retrieval_results; explicit test cases.
- Token budget telemetry plan (diagnostic) and when to shift to behavior-changing retrieval.
- Behavior-changing plan details: inject top-k with inclusion_reason and prompt/selection updates when enabled.

5) Combined answer
- Backlog inventory (condensed)
  - Implement L0 hybrid retrieval simulator (BM25 + dense), log to manifest/telemetry.
  - Add diagnostic validators: citation/span integrity; tokenizer/version pinning; schema for L0 chunk and citation id format.
  - Introduce pluggable context selection adapter with no-op default and clear telemetry split.
  - Add namespace/ACL tagging and read-only diagnostic filtering.
  - Optional: token budget telemetry (diagnostic).
- Open GAPs and staleness
  - GAP-0001 remains open. If its recommended_next_targets were diagnostic L0 work, they are now stale; if they target automatic retrieval/selection, they remain current. Gating assumption: GAP-0001 details are not fully admitted here.
- Candidate next PLAN items (unified)
  - A) L0 Hybrid Retrieval Simulator (Diagnostic-only)
    - Risk: low; Scope: BM25 + dense hybrid retrieval, score logging to manifest/telemetry, tests; Size: M; Prompt change: no; Selection change: no.
    - Reranking: unresolved; include reranking only if ABS-0003 mandates it; otherwise defer. Gating assumption.
    - Embeddings: do not create in production; allow mocks in tests; no index mutation.
  - B) Context Selection Policy Adapter (No-op default)
    - Risk: low; Scope: adapter interface, config, tests, telemetry separation; Size: S; Prompt: no; Selection: no.
  - C) L0 Schema + Citation/Tokenizer Validation (Diagnostic)
    - Risk: low; Scope: chunk schema, cid@version|span validation, tokenizer/version pinning, tests; Size: S; Prompt: no; Selection: no.
  - D) Namespace/ACL Diagnostics (Read-only)
    - Risk: low; Scope: namespace tagging and deny-by-default diagnostic filtering, logs, tests; Size: S; Prompt: no; Selection: no.
  - E) Behavior-changing Auto Retrieval (Governed)
    - Risk: high; Scope: retrieval integration with context assembly and prompt injection; flags/governance; tests; Size: M–L; Prompt: yes; Selection: yes.
- Recommendation
  - Proceed with A) L0 Hybrid Retrieval Simulator (Diagnostic-only) as the next item.
- Safe PLAN title and objective
  - Title: PLAN-20260706-0002 — L0 Hybrid Retrieval Simulator and Manifest-Linked Diagnostics
    - Gating assumption: if 20260706-0002 is already used, allocate the next chronological ID; ID assignment is non-functional.
  - Objective: Implement a diagnostic-only BM25 + dense hybrid retriever that returns ranked L0 candidates with bm25_score, dense_score, and combined retrieval_score; write results to a manifest-linked diagnostics section; add tests; no provider prompt or context selection changes; no production embedding creation or index mutation; allow mock embeddings for tests.
  - Note on reranking: include only if specified by ABS-0003; otherwise defer to a later slice.
- Out-of-scope boundary
  - No automatic inclusion of retrieved L0 into prompts/context; no context selection/budget policy enforcement; no provider prompt changes; no write-back or index mutation; no production embedding creation; ACL effects are diagnostic/logging only; no non-L0 retrieval; no L1 summary changes.
- Execution mode
  - Another diagnostic-only simulator slice.

6) Risks or missing assumptions
- GAP-0001 specifics are not admitted; need confirmation of its current recommended_next_targets.
- ABS-0003 retrieval details (and whether reranking is required) are referenced but not admitted here.
- Manifest schema fields for logging (e.g., candidate_set/ranking vs candidate_retrieval_results) are unspecified; need canonical names and versions.
- Embedding store availability and policy: clarify whether test-only mock embeddings are permitted and confirm prohibition on production embedding creation/index mutation in this slice.
- Token budget telemetry policy and exact splits are only cited by Claude; need admission/confirmation if required now.
- Governance artifacts (warrants/verify IDs) presence and naming need confirmation.
- Plan ID assignment policy is unspecified.

7) Suggested re-ask prompt
scripts/compare_providers.py --latest-context --require-admission --title "Resolve gating for L0 retrieval simulator (COMP-0021 follow-up)" --prompt "Resolve gating assumptions before implementing a diagnostic-only L0 hybrid retrieval simulator.

Given current boundaries:
- Explicit L0 inclusion, read-only L0 diagnostics, and context-manifest-connected L0 diagnostics are complete.
- Automatic L0 retrieval, context selection changes, and provider prompt changes are NOT implemented.
- GAP-0001 is open.

Please produce:
1) Confirm GAP-0001: list its current recommended_next_targets and mark any now-stale items (post L0 diagnostics completion).
2) ABS-0003 retrieval specifics: does the intended simulator include reranking beyond BM25 + dense hybrid scoring? Answer yes/no and cite the exact ABS-0003 clause or file path if yes.
3) Manifest logging schema: provide canonical field/section names and versions for logging candidate retrieval results (e.g., section name, per-candidate fields for bm25_score, dense_score, retrieval_score, provenance, inclusion_reason).
4) Embeddings/index policy: confirm that production embedding creation and index mutation are disallowed in this slice; state the approved approach for tests (e.g., mock/file-based embeddings).
5) Token budget telemetry: is a diagnostic token budget policy required in this slice? If yes, provide the exact split and where to log it; if no, defer explicitly.
6) Governance: confirm current warrant/verify artifacts relevant to retrieval; state whether a new warrant is required only when moving to behavior-changing auto-retrieval.
7) Plan scaffolding: should a no-op pluggable context selection adapter and retrieval-vs-selection telemetry separation be included now? Answer yes/no with brief rationale.
8) Plan ID: confirm the next available PLAN id (suggest PLAN-YYYYMMDD-0002 or next chronological); provide the exact ID to use.

Output format:
- Answer each item 1–8 with concise, authoritative statements and any file paths/IDs needed for immediate implementation.
- Do not propose behavior-changing steps; keep within diagnostic-only scope."
~~~

## Source Comparison

~~~markdown
# COMP-0021: Provider Comparison — AI-Lab backlog prioritization after context-manifest L0 diagnostics

## Metadata

- comparison_id: `COMP-0021`
- title: `AI-Lab backlog prioritization after context-manifest L0 diagnostics`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- context_manifest: `docs/comparisons/COMP-0021-ai-lab-backlog-prioritization-after-context-manifest-l0-diagnostics.context.json`
- created_at: `2026-07-06T07:19:07.976869+00:00`
- command: `scripts/compare_providers.py --latest-context --require-admission --title AI-Lab backlog prioritization after context-manifest L0 diagnostics Review the current AI-Lab repository/self-model state and propose the next backlog items and priority order.

Important current boundary:
- Explicit L0 inclusion is implemented.
- Read-only L0 candidate diagnostics are implemented.
- Context-manifest-connected L0 candidate diagnostics are implemented.
- PLAN-20260705-0001 and PLAN-20260706-0001 are completed.
- Automatic L0 retrieval is NOT implemented.
- Context selection changes are NOT implemented.
- Provider prompt changes are NOT implemented.
- Current open GAP is GAP-0001.

Please produce:
1. A short backlog inventory.
2. Which open GAPs remain and whether existing recommended_next_targets are stale.
3. 3-5 candidate next PLAN items.
4. For each candidate: risk, scope, implementation size, and whether it changes provider prompts or context selection.
5. A recommended next item.
6. A safe PLAN title and objective for the recommended item.
7. A clear out-of-scope boundary.
8. Whether we should proceed with another diagnostic-only slice, a simulator, or a governed behavior-changing retrieval slice.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Review the current AI-Lab repository/self-model state and propose the next backlog items and priority order.

Important current boundary:
- Explicit L0 inclusion is implemented.
- Read-only L0 candidate diagnostics are implemented.
- Context-manifest-connected L0 candidate diagnostics are implemented.
- PLAN-20260705-0001 and PLAN-20260706-0001 are completed.
- Automatic L0 retrieval is NOT implemented.
- Context selection changes are NOT implemented.
- Provider prompt changes are NOT implemented.
- Current open GAP is GAP-0001.

Please produce:
1. A short backlog inventory.
2. Which open GAPs remain and whether existing recommended_next_targets are stale.
3. 3-5 candidate next PLAN items.
4. For each candidate: risk, scope, implementation size, and whether it changes provider prompts or context selection.
5. A recommended next item.
6. A safe PLAN title and objective for the recommended item.
7. A clear out-of-scope boundary.
8. Whether we should proceed with another diagnostic-only slice, a simulator, or a governed behavior-changing retrieval slice.

## OpenAI Response

- model: `gpt-5`

```
Here’s a concise, source-aligned proposal.

1) Short backlog inventory
- Completed
  - Explicit L0 inclusion.
  - Read-only L0 candidate diagnostics.
  - Context-manifest-connected L0 candidate diagnostics.
  - PLAN-20260705-0001 and PLAN-20260706-0001 completed; self-model updated and verified.
- Not implemented
  - Automatic L0 retrieval.
  - Context selection changes.
  - Provider prompt changes.
- Supporting gaps to prepare for future governed changes (diagnostic-friendly)
  - Clear separation of retrieval diagnostics vs. selection telemetry to avoid confusion noted in L1.
  - Pluggable selection adapter with no-op default to enable future behavior changes safely.
  - ACL/namespace filtering in candidate diagnostics (read-only).
  - Citation/span integrity checks and tokenizer/version pinning in diagnostics.
  - Manifest pinning/versioning and test harness for reproducibility.

2) Open GAPs and staleness
- GAP-0001 remains open. Based on admitted context, the missing capability is automatic L0 retrieval (and any behavior-changing selection).
- Recommended_next_targets in GAP-0001 may need a refresh if they imply behavior-changing selection or provider prompt modifications. Given current boundaries, the next target should be a diagnostic-only/simulator step first. If GAP-0001 already recommends a simulator/diagnostic step, it is not stale; if it recommends behavior changes, revise to a simulator-first approach.

3) 3–5 candidate next PLAN items
- Candidate A: L0 Retrieval Simulator + Manifest Annotations (Diagnostic-Only)
  - Build hybrid retrieval (BM25 + dense) and reranking per ABS-0003, write results to manifest candidate_set/ranking and separate diagnostics, do not alter prompt assembly.
- Candidate B: Feature-Flagged Automatic L0 Retrieval (Non-Enforcing)
  - Compute retrieval and, behind a disabled-by-default flag, optionally populate inclusions; default remains diagnostic-only to avoid behavior change.
- Candidate C: Context Selection Policy Adapter (No-Op Default)
  - Introduce a pluggable selector interface and config with current behavior preserved, plus tests/telemetry separation.
- Candidate D: Citation Span Integrity and Tokenizer Pinning (Diagnostic)
  - Add validators that check cid@version|span shape and tokenizer/version consistency for candidate L0 references; report-only.
- Candidate E: ACL/Namespace Filtering in Candidate Diagnostics (Read-Only)
  - Apply deny-by-default namespace/ACL filtering to candidate sets in diagnostics to surface potential leakage issues early without changing selection.

4) Per-candidate risk, scope, size, and whether it changes provider prompts or context selection
- A: L0 Retrieval Simulator + Manifest Annotations
  - Risk: Low (diagnostic-only).
  - Scope: Retrieval scoring/ranking, manifest candidate/ranking writes, diagnostics, tests.
  - Size: M.
  - Changes provider prompts? No. Changes context selection? No.
- B: Feature-Flagged Automatic L0 Retrieval (Non-Enforcing)
  - Risk: Medium (path to behavior change; must guard telemetry).
  - Scope: Retrieval + optional inclusions under flag, safety rails, tests.
  - Size: M.
  - Changes provider prompts? No. Changes context selection? No by default; yes if flag enabled (governed).
- C: Context Selection Policy Adapter (No-Op)
  - Risk: Low.
  - Scope: Adapter layer, config, tests, telemetry split.
  - Size: S.
  - Changes provider prompts? No. Changes context selection? No.
- D: Citation Span Integrity and Tokenizer Pinning
  - Risk: Low to Medium (tokenizer/version handling).
  - Scope: Validators, reporting, tests, manifest links.
  - Size: S.
  - Changes provider prompts? No. Changes context selection? No.
- E: ACL/Namespace Filtering in Diagnostics
  - Risk: Low.
  - Scope: Read-only ACL filters on candidates, diagnostics, tests.
  - Size: S.
  - Changes provider prompts? No. Changes context selection? No.

5) Recommended next item
- Candidate A: L0 Retrieval Simulator + Manifest Annotations (Diagnostic-Only).
- Rationale: It directly advances GAP-0001 while respecting the current boundary against behavior changes. It also addresses the L1 risk about confusing telemetry by keeping the work clearly diagnostic and manifest-linked.

6) Safe PLAN title and objective for the recommended item
- Title: PLAN-20260708-0001 — L0 Retrieval Simulator and Manifest-Linked Diagnostics
- Objective: Implement a diagnostic-only L0 retrieval simulator that computes hybrid retrieval (BM25 + dense) with reranking (per ABS-0003), writes results to context manifest candidate_set/ranking and a dedicated diagnostics log, and adds tests and telemetry separation. No provider prompt or context selection behavior changes.

7) Out-of-scope boundary for the recommended item
- No automatic inclusion of retrieved L0 into final prompt/context.
- No modifications to context selection/budgeting policies.
- No provider prompt content or formatting changes.
- No write-back, embedding creation, or index mutation.
- No ACL enforcement that would alter selections; filtering remains diagnostic-only.
- No non-L0 retrieval or changes to L1 summaries.

8) Execution mode
- Proceed with a simulator (diagnostic-only slice).
- Reason: It de-risks the step toward automatic retrieval, aligns with the L1 guidance to avoid unintended behavior changes, and sets up clean telemetry and manifest linkages needed for a later governed, behavior-changing retrieval slice.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# AI-Lab Repository Backlog Review & Next-Item Proposal

## 1. Short Backlog Inventory

**Completed:**
- ✅ PLAN-20260705-0001: Explicit L0 inclusion
- ✅ PLAN-20260706-0001: Read-only context-manifest-connected L0 candidate diagnostics
- ✅ 2 supported warrants (WARR-20260706-0002 + 1 prior)
- ✅ Self-model infrastructure with plan/warrant/verification lifecycle

**Current State:**
- Diagnostic-only L0 context_match telemetry present
- No automatic retrieval, selection changes, or provider prompt modifications
- GAP-0001 open (details not in context pack)

**Key Implementation Boundary:**
- System can *see* L0 candidates but does not *select* or *inject* them automatically

---

## 2. Open GAPs & Staleness Check

**GAP-0001:** Status unknown from provided context; recommend reviewing whether it addresses:
- Automatic L0 retrieval
- Hybrid retrieval (BM25 + dense)
- Context selection algorithm implementation
- Citation format enforcement
- Write-back pipeline

**Staleness Assessment:**
Given the completion of diagnostic-only work, any GAP-0001 `recommended_next_targets` pointing to "add L0 diagnostics" would now be **stale**. If GAP-0001 targets automatic retrieval or selection behavior, it remains **current**.

---

## 3. Candidate Next PLAN Items (5)

### PLAN-A: L0 Hybrid Retrieval Simulator (Read-Only)
**Objective:** Implement BM25 + dense embedding retrieval simulation that logs candidate L0 chunks with scores but does not modify provider prompts.

**Risk:** Low  
**Scope:** Retrieval logic + embeddings infrastructure  
**Size:** Medium (2-3 files: retriever module, embedding store interface, tests)  
**Changes provider prompts?** No  
**Changes context selection?** No (simulation only)

### PLAN-B: Automatic L0 Retrieval with Manifest Integration (Behavior-Changing)
**Objective:** Implement automatic L0 chunk retrieval based on query + manifest, inject top-k candidates into Context Pack with `inclusion_reason: "retrieval_bm25_dense"`.

**Risk:** High (changes production context selection)  
**Scope:** Retrieval + context pack assembly + provider prompt changes  
**Size:** Large (4-6 files: retriever, context assembler, prompt templates, tests)  
**Changes provider prompts?** Yes  
**Changes context selection?** Yes

### PLAN-C: L0 Chunk Schema & Citation Format Foundation
**Objective:** Define and validate L0 chunk schema with `chunk_id`, `span`, `embedding_id`, `cid@version|span` citation format; add schema validation tests.

**Risk:** Low  
**Scope:** Schema definition + validation infrastructure  
**Size:** Small (1-2 files: schema doc, validation tests)  
**Changes provider prompts?** No  
**Changes context selection?** No

### PLAN-D: Token Budget Policy Implementation (Diagnostic)
**Objective:** Implement token budget allocation per ABS-0003 (15% system, 10% answer, 75% context with 40/45/10/5 split); log budget usage per context pack without enforcing limits.

**Risk:** Low  
**Scope:** Budget calculation + telemetry  
**Size:** Small (1-2 files: budget calculator, manifest augmentation)  
**Changes provider prompts?** No  
**Changes context selection?** No (diagnostic logging only)

### PLAN-E: Namespace & ACL Infrastructure Foundation
**Objective:** Implement namespace tagging for L0/L1 records and deny-by-default ACL filtering (read-only enforcement in diagnostic mode).

**Risk:** Medium (security-sensitive)  
**Scope:** ACL model + namespace tagging + filter logic  
**Size:** Medium (3-4 files: ACL module, namespace tagger, filter, tests)  
**Changes provider prompts?** No  
**Changes context selection?** No (filter logs denials but does not alter inclusions)

---

## 4. Risk, Scope & Implementation Detail

| PLAN | Risk | Scope | Size | Prompt Δ? | Selection Δ? |
|------|------|-------|------|-----------|--------------|
| **A** | Low | Retrieval sim | Medium | No | No |
| **B** | High | Full retrieval | Large | Yes | Yes |
| **C** | Low | Schema/validation | Small | No | No |
| **D** | Low | Budget telemetry | Small | No | No |
| **E** | Medium | ACL foundation | Medium | No | No |

**Key Trade-offs:**
- **PLAN-B** delivers end-user value (automatic retrieval) but requires new WARRANT and crosses the diagnostic boundary.
- **PLAN-A** extends diagnostic capability and prepares for PLAN-B without risk.
- **PLAN-C** and **PLAN-D** are low-risk foundational work that ABS-0003 depends on.
- **PLAN-E** is necessary for production but introduces security surface area.

---

## 5. Recommended Next Item

**PLAN-A: L0 Hybrid Retrieval Simulator (Read-Only)**

**Rationale:**
1. **Natural progression** from completed diagnostic work
2. **Prepares for automatic retrieval** (PLAN-B) without crossing the behavior boundary
3. **Validates ABS-0003 retrieval algorithm** in read-only mode
4. **Low risk** — no prompt or selection changes
5. **Enables telemetry** for tuning before production deployment
6. **Addresses GAP-0001** if it concerns retrieval implementation

---

## 6. Safe PLAN Title & Objective

**PLAN-20260706-0002**

**Title:**  
*L0 Hybrid Retrieval Simulator — Read-Only Candidate Scoring and Logging*

**Objective:**  
Implement BM25 + dense embedding hybrid retrieval for L0 chunks that:
- Accepts query + namespace + optional explicit references as input
- Returns ranked candidate list with scores and inclusion_reason metadata
- Logs candidates to context manifest telemetry without modifying provider prompts
- Validates retrieval correctness via test fixtures
- Does NOT change context selection or provider behavior

**Success Criteria:**
- Retrieval module returns candidates with `retrieval_score`, `bm25_score`, `dense_score`
- Context manifest logs `candidate_retrieval_results` section
- Tests cover empty results, exact match, and relevance ranking
- No provider prompt changes
- VERIFY-20260706-0002 confirms read-only behavior

---

## 7. Clear Out-of-Scope Boundary

**In Scope:**
- Retrieval algorithm implementation (BM25 + dense)
- Embedding storage interface (mock/file-based acceptable)
- Logging retrieval candidates to manifest telemetry
- Unit and integration tests

**Out of Scope:**
- **Automatic injection** of retrieved L0 into provider prompts
- **Context selection changes** (no modification to what providers see)
- **Token budget enforcement** (logging only)
- **Reranking** beyond initial hybrid score
- **ACL filtering** (deferred to PLAN-E)
- **Write-back pipeline** for new L0 generation
- **Citation format enforcement** in responses (deferred to PLAN-C)
- **Production embedding model training** (mock embeddings acceptable)

---

## 8. Next Slice Type Recommendation

**Recommendation: Continue with another diagnostic-only slice (PLAN-A / PLAN-20260706-0002)**

**Justification:**
1. **Preserves safety:** Two completed diagnostic slices establish a pattern; a third reinforces the governed approach before behavior changes.
2. **Builds confidence:** Retrieval simulator telemetry will reveal edge cases and tuning needs before automatic injection.
3. **Defers warrant complexity:** Automatic retrieval (PLAN-B) requires a new WARRANT addressing:
   - Correctness claims for hybrid retrieval
   - Privacy/security implications of automatic L0 inclusion
   - Rollback criteria if retrieval quality degrades
4. **Aligns with abstraction:** ABS-0003 specifies a detailed selection algorithm; simulating it first validates the design.

**Alternative Path (Lower Priority):**
- **Simulator for budget policy** (PLAN-D) is even lower risk but delivers less strategic value.
- **Schema foundation** (PLAN-C) is necessary but non-blocking; can parallelize with PLAN-A.

**When to Shift to Behavior-Changing:**
After PLAN-A completion and telemetry review, **PLAN-B** (automatic retrieval) becomes the natural next governed slice with a new WARRANT that admits:
- Retrieval correctness claims
- Fallback to explicit-only mode
- Monitoring for quality regression

---

## Summary

**Recommended Next PLAN:** PLAN-20260706-0002 (L0 Hybrid Retrieval Simulator — Read-Only)  
**Type:** Diagnostic-only slice  
**Estimated effort:** Medium (2-3 files, ~1-2 sessions)  
**Risk:** Low  
**Strategic value:** High (prepares for automatic retrieval, validates ABS-0003)  
**Governance:** Requires new PLAN and VERIFY; no new WARRANT (diagnostic-only)

This continues the safe, incremental approach while making measurable progress toward the full reconciled memory loop described in ABS-0003.
```

~~~
