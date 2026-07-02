# AI-Lab Development Directions

## Purpose

This document records medium- and long-term development directions for AI-Lab.

It is intentionally not an implementation backlog. Its purpose is to preserve
the ontology, design pattern, and strategic direction behind the code.

AI-Lab should continue to develop step by step:

    ontology
      -> primitives
      -> relations
      -> summaries
      -> context assembly
      -> validation
      -> controlled recurrence
      -> guarded automation
      -> possible autonomy later

The near-term goal is not autonomous intelligence. The near-term goal is a
traceable research platform that can preserve, compress, select, and reuse its
own work without losing provenance.

## Current milestone

AI-Lab currently has:

- provider-independent access,
- provider comparison,
- synthesis and re-ask artifacts,
- abstraction artifacts,
- artifact history and lineage,
- citation primitives,
- chunk references,
- L0 chunk summaries,
- artifact summaries,
- context pack manifests,
- budget-aware latest-context selection,
- rendered context packs,
- context-aware provider prompts,
- context-aware provider comparisons,
- sibling `.context.json` audit manifests,
- and anti-bloat protection for saved comparison artifacts.

The first real memory-aware loop showed that the platform can feed recent
observation artifacts back into later context packs.

## The issue discovered in the first memory-aware loop

The first context-aware next-step comparison created:

    COMP-0008-ai-lab-memory-next-step.md
    COMP-0008-ai-lab-memory-next-step.context.json

The context manifest selected only:

    ABS-0003

and excluded:

    SYNCOMP-0003
    COMP-0007

because those older artifacts exceeded the token budget.

This was mechanically correct, but it exposed a memory freshness problem.

ABS-0003 was created before a large implementation burst. It did not know that
the following had already been implemented:

- Citation parser
- ChunkReference
- L0ChunkSummary
- ArtifactSummary
- ContextPackManifest
- ContextPackRenderer
- context-aware provider prompts
- context-aware provider comparisons
- context manifest persistence
- sibling `.context.json` comparison audit files
- README, software spec, and library index updates

As a result, one provider recommended implementing primitives that were already
implemented. The provider was not necessarily wrong relative to the context it
received. The context was stale.

The important lesson:

    AI-Lab does not only need memory.
    AI-Lab needs memory freshness.

A later synthesis, SYNCOMP-0004, captured the observation. After that,
latest-context selected:

    ABS-0003
    SYNCOMP-0004
    COMP-0008

with no exclusions under the 8000-token budget.

This showed adaptive behavior:

    new observation artifact
      -> synthesis artifact
      -> next context pack includes the newer correction

The loop is working, but the memory model is still too coarse.

## Current memory model limitation

The current latest-context policy is artifact-type based:

    latest ABS
    latest SYNCOMP
    latest COMP

This is useful, but not sufficient.

It does not yet model:

- chronological interaction windows,
- rolling summaries,
- topic scopes,
- graph neighborhoods,
- stale summaries,
- supersession,
- or local/global context balance.

The original expectation was closer to a multi-level rolling and scoped memory
hierarchy.

## Target memory model

The target memory model should combine:

    chronological rolling memory
    + graph-local scoped memory
    + global ontology memory

A future prompt should not simply receive the latest artifact of each type.

Instead, it should receive a context bundle such as:

    current prompt / task node
    latest raw observation
    latest L1 summary for recent interactions
    latest L2 summary over recent L1 summaries
    relevant topic summary
    relevant graph neighborhood
    global project / ontology summary
    hard decisions and invariants
    raw evidence only when needed

## Rolling memory hierarchy

A simple rolling memory hierarchy would be:

### InteractionLogEntry

One raw chronological event.

Examples:

- user request,
- assistant response,
- shell command,
- command output,
- provider response,
- commit,
- test run,
- design decision,
- observed failure,
- observed contradiction.

### L1RecentSummary

Summary of the last N interaction log entries.

Example:

    last 20 interactions

L1 should answer:

- What just happened?
- What changed?
- What was decided?
- What failed?
- What should not be forgotten in the next step?

### L2RollingSummary

Summary of the last N L1 summaries.

Example:

    last 20 L1 summaries = approximately 400 interactions

L2 should answer:

- What has been happening across the recent development period?
- Which topics are active?
- Which decisions are stable?
- Which issues keep recurring?

### L3ProjectOntologySummary

Stable long-horizon summary.

It should preserve:

- project purpose,
- ontology basis,
- epistemic principles,
- architectural invariants,
- major design decisions,
- current capability ladder,
- long-term direction.

### TopicSummary

Scoped summary for a particular area.

Examples:

- provider layer,
- comparison/synthesis loop,
- artifact history,
- memory primitives,
- context packs,
- graph memory,
- ACL/redaction,
- retrieval,
- RTG support,
- epistemic ontology.

A prompt about AI-Lab memory should receive memory/topic summaries.
A prompt about provider bugs should receive provider/topic summaries.
A prompt about RTG should receive RTG/topic summaries.

## Graph-based scoped memory

Earlier epistemic discussions pointed toward a graph of nodes and relations.
This remains important.

The core idea:

    context = graph-local neighborhood
              + rolling abstraction summaries
              + global ontology frame

Every meaningful object can become a node.

Example node types:

- InteractionLogEntry
- Commit
- COMP artifact
- SYNCOMP artifact
- ABS artifact
- ContextManifest
- Schema
- Module
- Test
- Decision / ADR
- Risk
- Bug
- Concept
- TopicSummary
- ProjectSummary
- OntologyPrinciple

Relations should be explicit.

Example edge types:

- derived_from
- summarizes
- supersedes
- refreshes
- implements
- tests
- validates
- depends_on
- mentions
- contradicts
- belongs_to_topic
- belongs_to_scope
- is_stale_relative_to

A prompt should be located in this graph. Then context assembly can include:

    current node
    neighboring nodes
    important relations
    local summaries
    global summaries
    raw evidence when needed

## Should AI-Lab implement a full graph now?

Probably not yet.

A full graph database or complex traversal engine would be premature.

The safer sequence is:

    1. Document the graph ontology.
    2. Add lightweight MemoryNode and MemoryEdge schemas.
    3. Generate graph metadata from existing artifacts.
    4. Add simple neighborhood queries.
    5. Connect neighborhood summaries to context packs.
    6. Only later consider a real graph database.

The graph should first exist as explicit, tested data structures and artifact
metadata. Implementation should stay lightweight until the use cases are clear.

## Recommended memory architecture direction

The next memory system should move from:

    latest artifact type

to:

    latest scoped memory state

A future context pack may contain:

    latest raw observation
    latest L1RecentSummary
    latest L2RollingSummary
    latest relevant TopicSummary
    latest ProjectOntologySummary
    relevant graph-neighborhood nodes
    relevant raw artifacts only if necessary

This would solve the stale ABS problem more directly than simply increasing the
token budget.

## Possible next memory primitives

### InteractionLogEntry

A structured record of one interaction or system event.

Potential fields:

- entry_id
- entry_type
- created_at
- actor
- text
- command
- output_path
- artifact_ids
- commit_hash
- topics
- scope
- importance
- relations

### MemoryNode

A graph node representing a meaningful object.

Potential fields:

- node_id
- node_type
- title
- path
- created_at
- scope
- topics
- abstraction_level
- freshness
- source_ref

### MemoryEdge

A typed relation between nodes.

Potential fields:

- source_id
- target_id
- relation_type
- confidence
- created_at
- evidence
- note

### ScopeSummary

A summary over a scope or topic.

Potential fields:

- summary_id
- scope
- level
- source_nodes
- source_summaries
- summary
- created_at
- supersedes
- freshness_status

### ContextNeighborhood

The selected graph-local neighborhood for a task.

Potential fields:

- task
- selected_nodes
- selected_edges
- selected_summaries
- exclusions
- token_budget
- assembly_policy

## Memory refresh / write-back direction

The first memory-aware loop showed that AI-Lab needs refresh/write-back.

Possible refresh triggers:

- after N commits,
- after N interactions,
- after new COMP/SYNCOMP/ABS artifacts,
- after implementation burst,
- when latest abstraction is older than relevant implementation nodes,
- when provider output indicates stale context,
- manual refresh request.

Possible refresh outputs:

- L1RecentSummary,
- L2RollingSummary,
- updated TopicSummary,
- updated ProjectOntologySummary,
- new ABS artifact,
- ADR / decision record.

A refresh process should answer:

    What changed?
    What is now implemented?
    What earlier summary is stale?
    What should future prompts know?
    Which old risks are closed?
    Which risks remain open?

## Retrieval direction

Retrieval should come after stable memory and graph primitives.

Potential retrieval layers:

- simple keyword search,
- BM25,
- semantic embeddings,
- hybrid retrieval,
- reranking,
- dependency expansion,
- graph-neighborhood expansion,
- freshness-aware ranking,
- scope-aware filtering.

Retrieval should not replace the rolling/graph memory hierarchy. It should
augment it.

## ACL, redaction, and namespace direction

COMP-0008 identified a serious future risk:

    redaction / namespace leakage

Before serious retrieval is introduced, AI-Lab should define:

- namespace metadata,
- access level metadata,
- redacted vs full representations,
- deny-by-default filtering,
- separation of redacted/full embeddings,
- manifest validation for representation mixing.

ACL and redaction should be enforced before ranking and packing, not only after
retrieval.

## Validation direction

AI-Lab should grow validation before growing autonomy.

Important validators:

- citation format validator,
- chunk reference validator,
- L0 summary validator,
- artifact summary validator,
- context manifest validator,
- context budget validator,
- stale context validator,
- graph edge validator,
- ACL/redaction validator,
- saved artifact anti-bloat validator.

## Decision record direction

Some decisions should be made explicit as ADRs.

Candidate ADRs:

- chunk-level L0 is canonical,
- rendered context is not stored recursively in comparison artifacts,
- vectors are stored externally,
- context manifests are audit artifacts,
- latest-context is budget-bound,
- full graph implementation is deferred until lightweight schemas prove useful,
- graph-local memory and rolling summaries are complementary.

## Possible non-memory capability directions

AI-Lab should not focus only on memory forever. Other capability tracks may be
needed, but they should be introduced carefully.

### Code execution requested by providers

A provider may propose code to run. AI-Lab could execute it in a guarded
environment and feed results back.

This would require:

- explicit user approval or policy,
- sandbox boundaries,
- command allowlist or denylist,
- timeout limits,
- artifacted command results,
- provenance records,
- test integration,
- rollback discipline.

This is powerful but risky. It should not be implemented as unrestricted
provider-controlled shell access.

### Provider-specific memory fields

Each provider may benefit from a small memory field describing what that
provider should remember about its own prior behavior.

Examples:

- OpenAI was stronger on ACL/redaction risk in COMP-0008.
- Claude was stronger on L0/schema granularity risk in COMP-0008.
- Provider X tends to over-focus on architecture.
- Provider Y tends to over-focus on immediate code.

This should be handled carefully. Provider memory should not become bias or
unverified reputation. It should be evidence-backed and refreshable.

### Communication formats

Different tasks may need different interaction formats:

- direct answer,
- dialogue,
- debate,
- forum,
- reviewer / author,
- planner / critic,
- implementation / test,
- red team / blue team,
- provider comparison,
- synthesis panel.

These formats could become explicit prompt templates and artifact types.

### Evaluator / judge layer

AI-Lab may need a third model or deterministic evaluator to judge:

- provider disagreements,
- whether a response used stale context,
- whether a proposed step is already implemented,
- whether tests prove the claim,
- whether a comparison should trigger refresh.

This should begin with deterministic checks where possible.

### Task execution workflows

AI-Lab could eventually manage tasks:

- plan,
- implement,
- test,
- commit,
- summarize,
- refresh memory.

This should remain guarded and stepwise.

### Observability

AI-Lab should track:

- context token estimates,
- selected vs excluded items,
- stale summaries,
- provider disagreement patterns,
- implementation/test/commit loops,
- artifact growth,
- retrieval quality.

## Autonomy ladder

Autonomous intelligence is a far target and requires several fundamental
components.

A possible capability ladder:

### Level 0: Scripts

Manual CLI commands.

### Level 1: Context-aware tools

Tools can include selected memory context.

### Level 2: Self-auditing loops

The platform can compare, synthesize, and detect stale context.

### Level 3: Planned refresh/write-back

The platform can update summaries after implementation bursts.

### Level 4: Guarded task execution

The platform can propose and execute bounded tasks with tests and approval.

### Level 5: Autonomous research assistant

The platform can plan and execute research loops with strong safety, validation,
and rollback constraints.

AI-Lab is currently between Level 1 and early Level 2.

## Near-term recommendation

The next implementation should probably not be a full graph.

Recommended near-term path:

    1. Keep graph as documented direction.
    2. Add InteractionLogEntry and L1RecentSummary schemas.
    3. Add a manual or semi-automatic memory refresh command.
    4. Add stale-context detection.
    5. Add lightweight MemoryNode/MemoryEdge only after refresh summaries exist.
    6. Later connect graph neighborhoods to context packs.

This keeps the project aligned with its ontology-first design while avoiding
premature infrastructure complexity.
