# COMP-0027: Provider Comparison — GAP-0002 Next Governed Slice Review

## Metadata

- comparison_id: `COMP-0027`
- title: `GAP-0002 Next Governed Slice Review`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `explicit`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0027-gap-0002-next-governed-slice-review.context.json`
- created_at: `2026-07-16T20:46:18.500319+00:00`
- command: `scripts/compare_providers.py Review the next governed slice for AI-Lab GAP-0002:
“Graph-local scoped memory context selection.”

Certified state:

- CAP-0005: authoritative read-only graph-neighborhood advisor.
- CAP-0006 through CAP-0008: evidence and readiness evaluation.
- CAP-0009: explicit, default-off library integration of graph-neighborhood
  candidates into context-pack candidates.
- CAP-0011: explicit standalone CLI exposure.
- GAP-0002 remains open.
- Provider exposure, automatic target selection, automatic inclusion, graph
  persistence, retrieval, embeddings, reranking, and prompt changes are out
  of scope.

Repository audit:

- 43 artifacts; 26 authoritative lineage relations.
- 33 targets have neighborhoods; 10 are lineage-isolated.
- All selected paths are authoritative.
- Neighborhood size is 1–6 candidates; median 1.
- Only 9 targets expand beyond depth one.
- Whole-artifact cost is 494–13,208 tokens; median 2,223.
- At 500 tokens, many targets retain no neighbor.
- At 1,500 tokens, many retain only one neighbor.
- Some individual neighbors cost 2,000–4,000 tokens.

Candidate next slices:

A. Evidence-only distance-aware representation evaluation:
   rich distance-one, compact distance-two, deterministic token accounting,
   isolated-target diagnostics, and local/global balance.

B. Define target-selection semantics first.

C. Define a persisted compact/scoped-summary contract first.

D. Improve lineage coverage for isolated targets first.

E. Another prerequisite you identify.

Recommend exactly one next slice.

Use exactly these eight headings and keep the entire response under 900 words:

1. Blocker diagnosis
2. Option comparison
3. Recommended next slice
4. Existing representation inventory
5. Isolated targets
6. Graph-local versus global context
7. Mandatory non-goals
8. Evidence before later implementation

Required decisions:

- Should existing L0/L1/ABS or other compact representations first be
  inventoried?
- Can inventory and hypothetical distance-aware evaluation be combined into
  one evidence-only slice?
- Is a new persisted compact representation contract required now?
- Should isolated targets block the slice?

The recommended slice must remain selection_effect none. It must not change:

- ContextPackManifest.items;
- context selection;
- provider or prompt paths;
- CLI behavior;
- automatic target selection or inclusion;
- graph persistence;
- retrieval, embeddings, reranking, or indexes;
- memory stores or runtime manifests.

Distinguish:

- lineage isolation from token-budget exclusion;
- hypothetical representation from implemented representation;
- graph-local context from global ontology, invariants, and governance.

Avoid implementation detail beyond what is necessary to define evidence,
guardrails, and success criteria.

End with exactly:

END OF RESPONSE --title GAP-0002 Next Governed Slice Review --latest-context --scope ai-lab-memory --require-admission --max-warning-admissions 1 --token-budget 8000 --model-target gpt-5`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Review the next governed slice for AI-Lab GAP-0002:
“Graph-local scoped memory context selection.”

Certified state:

- CAP-0005: authoritative read-only graph-neighborhood advisor.
- CAP-0006 through CAP-0008: evidence and readiness evaluation.
- CAP-0009: explicit, default-off library integration of graph-neighborhood
  candidates into context-pack candidates.
- CAP-0011: explicit standalone CLI exposure.
- GAP-0002 remains open.
- Provider exposure, automatic target selection, automatic inclusion, graph
  persistence, retrieval, embeddings, reranking, and prompt changes are out
  of scope.

Repository audit:

- 43 artifacts; 26 authoritative lineage relations.
- 33 targets have neighborhoods; 10 are lineage-isolated.
- All selected paths are authoritative.
- Neighborhood size is 1–6 candidates; median 1.
- Only 9 targets expand beyond depth one.
- Whole-artifact cost is 494–13,208 tokens; median 2,223.
- At 500 tokens, many targets retain no neighbor.
- At 1,500 tokens, many retain only one neighbor.
- Some individual neighbors cost 2,000–4,000 tokens.

Candidate next slices:

A. Evidence-only distance-aware representation evaluation:
   rich distance-one, compact distance-two, deterministic token accounting,
   isolated-target diagnostics, and local/global balance.

B. Define target-selection semantics first.

C. Define a persisted compact/scoped-summary contract first.

D. Improve lineage coverage for isolated targets first.

E. Another prerequisite you identify.

Recommend exactly one next slice.

Use exactly these eight headings and keep the entire response under 900 words:

1. Blocker diagnosis
2. Option comparison
3. Recommended next slice
4. Existing representation inventory
5. Isolated targets
6. Graph-local versus global context
7. Mandatory non-goals
8. Evidence before later implementation

Required decisions:

- Should existing L0/L1/ABS or other compact representations first be
  inventoried?
- Can inventory and hypothetical distance-aware evaluation be combined into
  one evidence-only slice?
- Is a new persisted compact representation contract required now?
- Should isolated targets block the slice?

The recommended slice must remain selection_effect none. It must not change:

- ContextPackManifest.items;
- context selection;
- provider or prompt paths;
- CLI behavior;
- automatic target selection or inclusion;
- graph persistence;
- retrieval, embeddings, reranking, or indexes;
- memory stores or runtime manifests.

Distinguish:

- lineage isolation from token-budget exclusion;
- hypothetical representation from implemented representation;
- graph-local context from global ontology, invariants, and governance.

Avoid implementation detail beyond what is necessary to define evidence,
guardrails, and success criteria.

End with exactly:

END OF RESPONSE

## OpenAI Response

- model: `gpt-5`

```
1. Blocker diagnosis
- We lack evidence on how much graph-local context can fit within realistic token budgets without altering selection. The audit shows small neighborhoods but expensive neighbors; at 500–1,500 tokens many targets shed neighbors. Without distance-aware, deterministic token accounting across existing representations, we cannot set guardrails for GAP-0002.
- Confusion persists between lineage isolation (no edges) and token-budget exclusion (edges exist but are unaffordable).
- CAP-0005 provides a read-only neighborhood advisor, but we have not evaluated how existing L0/L1/ABS representations behave by distance (1 vs 2) under strict budgets.

2. Option comparison
- A. Evidence-only distance-aware representation evaluation: Fits selection_effect none, uses CAP-0005 read-only, produces the missing measurements (ring costs, isolated diagnostics), and informs later policy. In scope.
- B. Define target-selection semantics first: Out of scope (automatic target selection/inclusion are explicitly excluded).
- C. Define a persisted compact/scoped-summary contract first: Premature and risks violating non-goals (no graph persistence or store/schema changes).
- D. Improve lineage coverage for isolated targets first: Alters graph persistence/lineage; out of scope for this slice.
- E. Another prerequisite: Any tokenizer pinning and accounting utilities can be embedded within A without changing runtime behavior.

3. Recommended next slice
Select A: Evidence-only distance-aware representation evaluation.
- Goal: Quantify token costs and coverage for graph-local neighborhoods using existing representations, with rich distance-one and compact distance-two hypothetical formats, without persisting or integrating them.
- Deliverables:
  - Per-target reports for all 33 targets with neighborhoods (plus the 10 isolated) showing:
    - Distance-1 “rich” cost using current L0/L1 text (no schema changes).
    - Distance-2 “compact” hypothetical summaries derived ephemerally from L0/L1/ABS (not persisted).
    - Deterministic token accounting at budgets 500 and 1,500, with whole-artifact baselines.
    - Isolation vs budget-exclusion labeling.
    - Local (rings) vs headroom for global content balance estimates.
- Success criteria:
  - 100% coverage of targets; stable, reproducible token counts (pinned tokenizer).
  - No change to selection behavior, manifests, stores, or CLI.
  - Clear evidence to decide later whether a new persisted compact contract is warranted.

4. Existing representation inventory
Yes—inventory first, then evaluate.
- L0: Chunk-level summaries with spans and citations (from ABS-0003).
- L1: Artifact-level and episode-level summaries linking to L0 (from ABS-0003).
- ABS: The reconciled abstraction fields and budgeting concepts (ABS-0003) used only as interpretive scaffolding.
- No new schemas; rely solely on current L0/L1/ABS material available in the repo.

5. Isolated targets
- They should not block the slice. Treat them as a distinct diagnostic class:
  - Lineage isolation: truly no neighbors per CAP-0005.
  - Token-budget exclusion: neighbors exist but become unaffordable under 500/1,500-token caps.
- Report both states distinctly and quantify the minimum budget at which neighbors appear.

6. Graph-local versus global context
- Scope is graph-local: distance-one (rich) and distance-two (compact) rings only.
- Global ontology, invariants, and governance are out of scope; we neither alter nor assess them here.
- Use CAP-0005 as the authoritative, read-only neighborhood source; do not enable CAP-0009 integration.

7. Mandatory non-goals
- No change to ContextPackManifest.items.
- No context selection, provider, or prompt-path changes.
- No CLI behavior changes.
- No automatic target selection or inclusion.
- No graph persistence or lineage edits.
- No retrieval, embeddings, reranking, or index changes.
- No memory store or runtime manifest changes.
- No new persisted compact representation in this slice.

8. Evidence before later implementation
- Guardrails:
  - selection_effect none; read-only use of CAP-0005.
  - Pin a single tokenizer/version for deterministic counts (not tied to runtime prompts).
  - Ephemeral transforms only; do not persist “compact” summaries.
- Method:
  - For each target: collect distance-1 and distance-2 neighborhoods (authoritative paths only).
  - Compute token costs for: whole neighbors; rich d=1 (existing L0/L1); compact d=2 (hypothetical, derived from existing text).
  - Evaluate fit at 500 and 1,500 tokens; record which neighbors survive.
  - Distinguish lineage-isolated vs budget-excluded cases.
- Outputs:
  - JSON/CSV evidence bundle and a short narrative report with per-target and aggregate stats (median/percentiles of neighbor retention, costs by ring).
  - Recommendations framed as questions (e.g., is a persisted compact contract necessary?) without proposing implementation.
- Exit checks:
  - Reproducible runs; unchanged manifests/CLI; coverage of all audited targets.

END OF RESPONSE
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# 1. Blocker diagnosis

No hard blockers exist. CAP-0005 through CAP-0011 provide a read-only advisor and explicit library integration. However, the repository audit exposes three evidence gaps that must be closed before any distance-aware representation can be designed or evaluated:

- **Representation inventory gap**: No catalog exists of which compact representations (L0, L1, ABS, or other) are available, their token costs, or their suitability for graph-local scoping.
- **Distance-aware cost gap**: Median neighborhood size is one; whole-artifact cost is 494–13,208 tokens. At 500-token budgets, many targets retain no neighbor; at 1,500 tokens, only one. No evidence quantifies how distance-two or compact representations would change these outcomes.
- **Isolated-target diagnostic gap**: Ten targets are lineage-isolated. The audit does not distinguish whether isolation is permanent (missing lineage), temporary (recoverable via coverage improvements), or acceptable (self-contained targets).

Without this evidence, option A (distance-aware representation evaluation) would be hypothetical guesswork, option C (new compact contract) would be premature specification, and option B (target-selection semantics) would lack the cost data required for principled tradeoffs.

---

# 2. Option comparison

**Option A** (distance-aware evaluation) is the correct *direction* but conflates inventory, diagnostics, and hypothetical evaluation into one slice. It risks specification creep.

**Option B** (target-selection semantics) requires cost and representation evidence first. Defining "which targets qualify" without knowing "what can fit" inverts the dependency order.

**Option C** (compact-summary contract) is premature. L0/L1/ABS already exist; their fitness for graph-local use is unknown. Specifying a new contract before evaluating existing representations wastes design effort.

**Option D** (improve lineage coverage) is a general repository-health task, orthogonal to GAP-0002. Lineage improvements benefit all memory operations, not just graph-local selection.

**Option E** (inventory + diagnostics slice): The missing prerequisite is a combined evidence artifact that inventories existing compact representations, diagnoses isolated targets, and provides deterministic token accounting for distance-aware scenarios—without specifying, implementing, or evaluating any new representation contract.

---

# 3. Recommended next slice

**Evidence-only inventory and diagnostics for graph-local representation fitness**, covering:

1. **Representation inventory**: catalog all existing compact representations (L0 chunk summaries, L1 episode/artifact summaries, ABS abstractions) with schema references, typical token costs, and current availability across the 43-artifact corpus.
2. **Isolated-target diagnostics**: classify each of the 10 isolated targets as permanently isolated (no recoverable lineage), temporarily isolated (lineage exists but is not yet authoritative), or acceptably isolated (self-contained scope).
3. **Distance-aware token accounting**: for a representative sample of targets (≥5, spanning small/median/large neighborhoods), calculate hypothetical token costs under distance-one whole-artifact, distance-two whole-artifact, distance-one compact (using inventoried L0/L1/ABS), and distance-two compact scenarios. Report budget survival rates at 500, 1,500, and 3,000-token thresholds.

**Outputs**: one evidence document (markdown or JSON), no implementation, no schema changes, no new representations, no selection-effect changes. This slice remains `selection_effect: none` and satisfies all mandatory non-goals.

---

# 4. Existing representation inventory

L1-20260703 and ABS-0003 confirm that **L0 chunk summaries**, **L1 episode summaries**, **L1 artifact summaries**, and **ABS abstractions** exist. L1-20260703 references `L0ChunkSummary.to_dict` and provider L0 invariant validation, implying structured L0 records with `chunk_id`, `cid`, `version`, `span`, and `summary_text`. ABS-0003 describes two-layer summarization (chunk-level L0, episode-level L1) and references `ChunkReference` schema, `embedding_id`, and `embedding_namespace`.

However, the context pack provides no:

- Exhaustive schema definitions or token-cost distributions for L0/L1/ABS across the 43-artifact corpus.
- Mapping of which artifacts have L0 chunks, L1 summaries, or ABS abstractions.
- Comparison of whole-artifact versus compact-representation token costs for typical graph neighborhoods.

The inventory slice must fill these gaps by auditing `docs/memory/l0/`, `docs/memory/l1/`, `docs/abstractions/`, and referencing governance schemas to produce a complete representation catalog with token statistics.

---

# 5. Isolated targets

Ten targets are lineage-isolated. The audit does not report *why*. Possible causes:

- **Permanently isolated**: foundational or self-contained artifacts (e.g., top-level ontologies, standalone tools) with no logical lineage.
- **Temporarily isolated**: lineage exists but relations are not yet authoritative or indexed.
- **Acceptably isolated**: targets whose scope is narrow enough that graph-local context adds no value.

The diagnostics slice must classify each isolated target and document whether coverage improvements (option D) are necessary or whether isolation is expected. This informs whether graph-local selection should gracefully degrade (return empty neighborhood) or raise warnings for isolated targets.

Isolated targets must *not* block the evidence slice. Diagnostics clarify their status; they do not require remediation before evidence collection.

---

# 6. Graph-local versus global context

**Graph-local context** comprises lineage-connected artifacts within a bounded distance (depth one or two) from a specific target, governed by authoritative relations and token budgets. It is target-specific, scope-limited, and ephemeral (assembled per prompt).

**Global context** comprises ontology definitions (e.g., domain-L0 schemas), governance invariants (e.g., CAP/GAP certification rules), and cross-cutting abstractions (e.g., ABS-0003's memory loop). Global context is target-independent and applies universally.

Graph-local selection augments, does not replace, global context. The evidence slice must account for both: inventoried representations must support graph-local scoping, while global invariants and governance remain in mandatory inclusion sets.

---

# 7. Mandatory non-goals

Per GAP-0002 scope and certified state, the evidence slice must **not**:

- Change `ContextPackManifest.items`, selection algorithms, or prompt assembly.
- Add provider calls, CLI flags, or automatic inclusion.
- Implement graph persistence, retrieval, embeddings, reranking, or indexing.
- Specify or implement new compact-summary contracts.
- Modify memory stores, runtime manifests, or validation schemas.

The slice is **evidence-only**: inventory, diagnostics, and hypothetical cost projections. All data derives from existing artifacts and read-only graph queries (CAP-0005).

---

# 8. Evidence before later implementation

Distance-aware representation evaluation (option A's intent) requires this evidence first. Without the inventory, any "compact distance-two" proposal is underspecified. Without token accounting, "deterministic budget survival" claims are unverifiable. Without isolated-target diagnostics, "local/global balance" lacks a failure-mode analysis.

The evidence slice is a *mandatory prerequisite* for option A, option B (target-selection semantics require cost data), and option C (any new contract requires fitness comparison with existing representations). Combining inventory and diagnostics into one slice is efficient and preserves `selection_effect: none`.

Defer all representation design, selection semantics, and compact-summary contracts until evidence is certified.

END OF RESPONSE
```
