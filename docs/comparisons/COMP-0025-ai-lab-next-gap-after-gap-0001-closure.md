# COMP-0025: Provider Comparison — AI-Lab next gap after GAP-0001 closure

## Metadata

- comparison_id: `COMP-0025`
- title: `AI-Lab next gap after GAP-0001 closure`
- context_pack: `/tmp/ailab-next-gap-source-context.md`
- created_at: `2026-07-09T15:17:31.570308+00:00`
- command: `scripts/compare_providers.py AI-Lab has closed GAP-0001. Based only on the supplied explicit source context, should the next self-model gap be graph-local scoped memory context selection? Review whether this should become GAP-0002, whether it is already covered by existing capabilities, and what the safest first governed slice should be. Do not propose implementation yet. --context-pack /tmp/ailab-next-gap-source-context.md --title AI-Lab next gap after GAP-0001 closure`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has closed GAP-0001. Based only on the supplied explicit source context, should the next self-model gap be graph-local scoped memory context selection? Review whether this should become GAP-0002, whether it is already covered by existing capabilities, and what the safest first governed slice should be. Do not propose implementation yet.

## OpenAI Response

- model: `gpt-5`

```
Short answer
Yes. The next self-model gap should be graph‑local scoped memory context selection, and it is not covered by the existing capabilities. It should be opened as GAP-0002, framed as a read-only, advisor-grade neighborhood selector that explains suggested inclusions without modifying context selection.

Why this is the right next gap (from supplied context)
- Development directions explicitly call out the limitation of the current “latest artifact type” policy and target “graph-local scoped memory + rolling summaries” for context assembly. The document also recommends adding lightweight node/edge schemas and simple neighborhood queries before any full graph engine.
- Current implementation selects latest-by-level artifacts (artifact_history.latest_records_by_context_level) and does not assemble context using a graph neighborhood.
- The edge model is maturing (ADR-0003 draft, bootstrap predicates, validator, interaction_log future_edge_seed_records), but there is no read-only graph-neighborhood selector wired into context assembly.
- Existing capabilities do not cover this:
  - CAP-0001: Explicit L0 latest-context inclusion, not graph-local.
  - CAP-0002: Read-only L0 candidate diagnostics.
  - CAP-0003: Diagnostic-only L0 hybrid retrieval simulator.
  - CAP-0004: Read-only L0 discovery advisor.
  These focus on L0 discovery/diagnostics and hybrid retrieval simulation, not graph-local neighborhood selection for context.
- A related plan exists (PLAN-20260706-0001) to extend L0 diagnostics over latest-context manifest items, but it still operates at L0 and does not introduce graph-local selection.

Proposed gap definition for GAP-0002
- Title: Graph-local scoped memory context selection (read-only, advisor-grade)
- Problem: Latest-context selection by artifact type leads to stale or incomplete context. The project needs a way to suggest a small, justified graph-local neighborhood around a target task or artifact without changing selection automatically.
- Scope (read-only):
  - Inputs: a target artifact/task ID (e.g., current prompt node, comparison, or memory-refresh candidate).
  - Sources: existing front-matter relations, artifact_history lineage/relations, any committed docs/edges EDGE records, and deterministic edge-seed information exposed by interaction logs (advisory only).
  - Output: a human-auditable recommendation that lists candidate neighboring artifacts, the relation(s) that justify each inclusion, and a token-budget estimate; includes explicit rationales for exclusions. No writes, no changes to manifests, no new edges persisted.
- Out of scope (for this gap):
  - Modifying context-pack selection policies.
  - Persisting new nodes/edges or adopting a graph database.
  - Expanding predicate vocabulary beyond the bootstrap set.
  - Retrieval ranking beyond simple, relation-based neighborhood selection.
  - ACL/redaction changes.

Why it is not already covered
- None of CAP-0001 through CAP-0004 provide graph-local neighborhood selection for context. They are L0 discovery/diagnostics and a hybrid retrieval simulator, not neighborhood-based context assembly.
- PLAN-20260706-0001 complements but does not replace this need; it extends diagnostics over existing latest-context items rather than proposing graph-scoped neighborhood suggestions.

Safest first governed slice
- A single-task, read-only neighborhood advisor:
  - Given one target artifact/task, produce a dry-run recommendation of N nearby artifacts with:
    - the explicit relations that connect each neighbor to the target (e.g., derived_from, supersedes, based_on, disputes),
    - scope interpretation (version/lineage/exact) when applicable,
    - a token cost estimate,
    - and an explanation of why each item is included or excluded under a stated budget.
  - Uses only existing front matter, artifact_history lineage/relations, and any committed EDGE records; may cite interaction_log edge seeds as non-authoritative hints.
  - Produces a human-readable report (advice-only) and does not modify the context manifest or write any graph artifacts.
- Acceptance criteria (governance/testability oriented, not implementation detail):
  - Deterministic, explainable recommendations from the same repo state.
  - No file writes or manifest changes.
  - Clear provenance: every suggested neighbor cites its relation(s) and scope.
  - Budget-aware: shows estimated tokens per item and total, with a reasoned cut line.
  - Safe with ADR-0002 (“ontology precedes implementation”) and ADR-0003 (treat edges as immutable artifacts; read-only consumption only).

Recommendation
- Open GAP-0002 with the above definition and boundaries.
- Treat PLAN-20260706-0001 as complementary (L0 diagnostics over selected items). The GAP-0002 first slice should be an advisor-grade, read-only neighborhood recommender that can inform, but not alter, context selection.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Analysis: Next Gap After GAP-0001 Closure

## Current State Review

### What GAP-0001 Closed
GAP-0001 was "Automatic L0 discovery from selected context." This has been closed, with CAP-0004 implementing "Read-only L0 discovery advisor."

### Current Memory/Context Capabilities
From the context pack:

**Implemented capabilities:**
- CAP-0001: Explicit L0 latest-context inclusion
- CAP-0002: Read-only L0 candidate diagnostics  
- CAP-0003: Diagnostic-only L0 hybrid retrieval simulator
- CAP-0004: Read-only L0 discovery advisor

**Current context selection mechanism:**
```python
# From context_pack_builder.py line 631-635
# Selection is delegated to artifact_history.latest_records_by_context_level
latest_by_level = latest_records_by_context_level(records)
```

The `latest_records_by_context_level` function (line 299) appears to provide artifact-type-based selection, which aligns with the development_directions observation:

> "The current latest-context policy is artifact-type based:
>     latest ABS
>     latest SYNCOMP
>     latest COMP
> This is useful, but not sufficient."

### The Documented Problem

From development_directions "Current memory model limitation":

> "The current latest-context policy is artifact-type based... It does not yet model:
> - chronological interaction windows,
> - rolling summaries,
> - topic scopes,
> - **graph neighborhoods**,
> - stale summaries,
> - supersession,
> - or local/global context balance."

The stale ABS-0003 incident showed this concretely: ABS-0003 was selected by type-based recency but was stale relative to actual implementation state.

## Should Graph-Local Scoped Memory Become GAP-0002?

### Evidence This Is a Real Gap

1. **Documented limitation**: development_directions explicitly identifies this as missing
2. **Observed failure**: The ABS-0003 staleness incident demonstrated the problem
3. **Not covered by current CAPs**: 
   - CAP-0001 through CAP-0004 focus on L0 discovery
   - None address graph-neighborhood-based context selection
4. **Edge infrastructure exists but isn't used for context**: 
   - `edge_validation.py` validates edge records
   - `artifact_history.py` has `lineage_for_artifact` and relation tracking
   - But context selection doesn't use graph relationships

### Distinguishing This From Existing Capabilities

This gap is distinct from:
- **L0 discovery** (GAP-0001/CAP-0004): That's about finding chunk-level sources
- **Artifact lineage display** (implemented): `format_artifact_lineage` exists but is for human rendering, not selection
- **Edge validation** (implemented): Structure validation exists but doesn't drive context selection

This gap is specifically: **Using graph relationships to select contextually relevant items rather than only type+recency.**

## Recommended Gap Definition

### GAP-0002 Proposed Definition

**Title**: Graph-neighborhood-aware context selection

**Summary**: Context pack assembly currently uses `latest_records_by_context_level`, which selects items by artifact type and recency only. It does not consider graph relationships between the current task and available artifacts. This causes context staleness when newer artifacts exist that are relationally closer to the task than the latest artifact of a given type.

**Observed manifestation**: 
- ABS-0003 was selected as "latest abstraction" but was stale relative to implementation
- SYNCOMP-0004 corrected this but was initially excluded by token budget
- Selection policy cannot distinguish "latest by timestamp" from "most relevant to current task"

**Not implemented by current capabilities**:
- CAP-0001-0004 address L0 discovery, not graph-based selection
- `artifact_history.py` has lineage tracking but only for display
- Edge validation exists but edges aren't used for context assembly

## Safest First Governed Slice

Following ADR-0001 principles (small vertical slices, testable steps):

### Recommended First Slice: Read-Only Graph Neighborhood Query

**Objective**: Add a diagnostic function that, given a task node ID and available artifact records, returns the graph-local neighborhood without modifying context selection.

**Why this is safest**:
1. **Read-only**: No changes to production context assembly
2. **Observable**: Can be tested against existing artifacts
3. **Validates model**: Proves the graph data exists and is usable
4. **Small**: Single query function, single test
5. **Prepares integration**: Once validated, can be wired into context_pack_builder

**What it should do**:
```python
def graph_neighborhood_for_task(
    task_node_id: str,
    available_records: list[ArtifactRecord],
    edge_records: list[dict],  # from docs/edges/*.yaml
    max_depth: int = 2
) -> tuple[list[str], dict[str, str]]:
    """
    Return (selected_ids, selection_reasons) for artifacts within
    graph distance of task_node_id.
    
    This is diagnostic only and does not modify context selection.
    """
```

**Success criteria**:
- Can load edge records from `docs/edges/`
- Can traverse subject→object relationships
- Returns artifact IDs within specified depth
- Includes relation path explanation
- Has unit test with synthetic graph
- Has integration test with real edge records (if any exist)

**What it explicitly does NOT do**:
- Modify `latest_records_by_context_level`
- Change `ContextPackBuilder.build_latest_context_pack`
- Introduce scoping/filtering policy
- Handle edge disputes/retractions
- Implement freshness scoring
- Make selection decisions

### Why NOT Go Directly to Implementation

Development_directions warns:

> "A full graph database or complex traversal engine would be premature.
> The safer sequence is:
>     1. Document the graph ontology.
>     2. Add lightweight MemoryNode and MemoryEdge schemas.
>     3. **Generate graph metadata from existing artifacts.**
>     4. **Add simple neighborhood queries.**
>     5. Connect neighborhood summaries to context packs."

We have:
- ✅ Edge ontology documented (ADR-0003)
- ✅ Edge schema defined and validated
- ❌ Graph metadata not yet generated from artifacts
- ❌ Neighborhood queries don't exist

The diagnostic query is step 4. Integration into context selection would be step 5.

## Open Questions for Future Review

1. **Should artifact front-matter relations be included?** Many artifacts have `relations:` in their front matter. Should these be unified with edge records or kept separate?

2. **How to handle version vs lineage scope in queries?** Edge records distinguish these, but context selection may need different traversal rules.

3. **What is the integration policy?** Should graph-neighborhood be:
   - Additional to type-based selection?
   - A filter on type-based selection?
   - A replacement for type-based selection?
   - A separate budget pool?

4. **Is there already partial infrastructure?** The `interaction_log.py` has `future_edge_seed_records()` (line 456) suggesting some graph-aware capability exists at the L1 summary level.

## Recommendation

**YES**, graph-local scoped memory context selection should become **GAP-0002**.

**The safest first governed slice is:** Implement read-only graph-neighborhood diagnostic query that traverses edge records but does not modify context selection.

**This follows the pattern established by GAP-0001 → CAP-0002/CAP-0003/CAP-0004:** Start with read-only diagnostics, validate the model, then integrate.

**The gap is real, distinct from existing capabilities, and has documented architectural support in ADR-0003 and development_directions.**
````
