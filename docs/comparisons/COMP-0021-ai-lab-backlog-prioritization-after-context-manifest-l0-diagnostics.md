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
