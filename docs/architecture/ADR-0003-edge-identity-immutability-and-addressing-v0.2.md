---
id: ADR-0003
origin_type: architecture_decision
current_type: architecture_decision
title: Edge Identity, Immutability, and Addressing
version: 0.2-draft
status: draft
layer: architecture
category: documentation-graph-bootstrap
relations:
  - predicate:
      id: based_on
      vocabulary: bootstrap_predicates
      version: 0.1
    target:
      id: SYN-0004
      scope: version
      version: 0.1-draft
    warrant:
      summary: "SYN-0004 identified predicate semantics, ordering, and graph-state fold as implementation-critical fixes for ADR-0003."
  - predicate:
      id: supersedes
      vocabulary: bootstrap_predicates
      version: 0.1
    target:
      id: ADR-0003
      scope: version
      version: 0.1-draft
    warrant:
      summary: "v0.2 revises ADR-0003 v0.1 with minimal predicate semantics, required edge ordering, staging/committed immutability, and fold rules."
contributors:
  - peer_id: PEER-0001
    display_name: Mustafa Aksu
    kind: human
    role: project_lead
    substrate: human
  - peer_id: PEER-0002
    display_name: Architect Peer
    kind: ai_peer
    role: drafter
    substrate: GPT-5.5 Thinking
  - peer_id: PEER-0003
    display_name: Independent Reviewer A
    kind: ai_peer
    role: reviewer
    substrate: Gemini
  - peer_id: PEER-0004
    display_name: Independent Reviewer B
    kind: ai_peer
    role: reviewer
    substrate: Claude
open_tensions:
  - edge_files_vs_edge_ledgers
  - predicate_minimalism_vs_epistemic_expressiveness
  - authorization_vs_open_peer_dialectic
  - structural_edges_vs_epistemic_edges
  - bootstrap_simplicity_vs_graph_completeness
---

# ADR-0003: Edge Identity, Immutability, and Addressing

| Field | Value |
|---|---|
| **Document ID** | ADR-0003 |
| **Title** | Edge Identity, Immutability, and Addressing |
| **Version** | 0.2-draft |
| **Status** | Draft |
| **Date** | 2026-06-30 |
| **Supersedes** | ADR-0003 v0.1-draft |
| **Based on** | SYN-0004 |
| **Constrains** | P-0001 v0.3 |
| **Prepared by** | Architect Peer |
| **Project Lead** | Mustafa Aksu |

---

## 1. Context

P-0001 v0.3 established that AI-Lab documentation should begin as a bootstrap graph of human-readable Markdown nodes and append-only relation records.

ADR-0003 v0.1 then defined the structural edge model:

- edge records are independently addressable artifacts;
- edge records are immutable after creation;
- edges can target documents, reviews, syntheses, proposals, ADRs, ALS documents, other edges, and future knowledge-layer objects;
- references must distinguish `version`, `lineage`, and `exact` scope;
- edge correction happens by creating new edges;
- catalogs are derived indexes rather than authoritative graph truth.

The first ADR-0003 review cycle accepted the structure but identified semantic and operational gaps:

1. the predicate vocabulary was too broad and underdefined;
2. immutable edges require predicate vocabulary versioning;
3. append-only replay requires deterministic ordering;
4. graph-state fold semantics must be defined;
5. immutability should begin at commit/merge, not during local drafting;
6. physical storage must allow both edge files and edge ledgers.

ADR-0003 v0.2 addresses those gaps while preserving the structural model.

---

## 2. Decision

AI-Lab will treat relation records as immutable, independently addressable edge artifacts **after they enter the tracked project baseline**.

An edge is not a mutable property of a document.

An edge is an artifact.

Therefore:

1. Each edge receives a stable ID.
2. Each committed edge is immutable.
3. Edges may target documents, reviews, syntheses, proposals, ADRs, ALS documents, other edges, peers, or future knowledge-layer objects.
4. Edge correction happens by creating another edge.
5. References must explicitly state whether they target a specific version, an artifact lineage, or an exact immutable artifact.
6. Every edge must declare a predicate from a versioned predicate vocabulary.
7. Every edge must include deterministic ordering metadata.
8. Catalogs are derived from document metadata and edge records.
9. Physical edge storage may be one file per edge or append-only edge ledgers.
10. The bootstrap predicate set is intentionally minimal.

---

## 3. Definitions

### 3.1 Node

A node is any addressable artifact in the bootstrap documentation graph.

Examples:

```text
P-0001
ALS-0001
ADR-0003
R-0006
SYN-0004
EDGE-0001
PEER-0001
```

A node may be a document, review, synthesis, architecture decision, specification, relation record, peer record, or future knowledge-layer object.

### 3.2 Edge

An edge is a relation record that connects one subject to one object through a versioned predicate and warrant.

Example:

```text
EDGE-0007:
  P-0042 disputes ALS-0002
```

### 3.3 Edge Artifact

An edge artifact is the stored representation of an edge.

In the bootstrap phase, this may be:

- a YAML file;
- a record inside an append-only ledger;
- or later, a graph-managed record.

### 3.4 Birth-Stamp ID

A birth-stamp ID is assigned once and never changes.

The prefix records the artifact family at creation time. It is not a mutable live classification.

Example:

```text
P-0001
```

means:

> This artifact originated as a proposal.

It does not mean:

> This artifact must forever remain only a proposal.

### 3.5 Reference Scope

Reference scope defines whether an edge targets:

- one exact version of an artifact;
- an artifact lineage across versions;
- or one exact immutable artifact.

---

## 4. Staging vs Committed Immutability

Edge immutability begins only after the edge enters the tracked project baseline.

For the current repository workflow, the tracked baseline is the protected committed project history on `main`.

### 4.1 Before Commitment

Before an edge is committed or merged, ordinary editing is allowed.

A contributor may fix:

- typos;
- malformed YAML;
- wrong target IDs;
- wrong predicate selection;
- missing metadata;
- formatting errors.

These local corrections do not require retraction edges.

### 4.2 After Commitment

After an edge is committed or merged, it is immutable.

Do not edit a committed edge to change its meaning.

Do not mutate a committed edge by changing:

- predicate;
- subject;
- object;
- scope;
- warrant;
- created_at;
- sequence;
- vocabulary version;
- or contributor attribution.

### 4.3 Correction by New Edge

To retract, dispute, supersede, resolve, or narrow a committed edge, create a new edge targeting the prior edge.

Example:

```yaml
id: EDGE-0020
origin_type: relation_record
current_type: relation_record
title: Retraction of EDGE-0001
created_at: 2026-06-30T00:00:00Z

subject:
  id: PEER-0002
  scope: exact

predicate:
  id: resolves
  vocabulary: bootstrap_predicates
  version: 0.1

object:
  id: EDGE-0001
  scope: exact

warrant:
  summary: "EDGE-0001 used an incorrect target reference."

contributors:
  - peer_id: PEER-0002
    role: relation_author
    substrate: GPT-5.5 Thinking
```

This preserves the historical record while allowing the graph state to evolve.

---

## 5. Edges Can Target Edges

If relationships are first-class, then relationships must themselves be disputable, resolvable, and supersedable.

Therefore the `subject` and `object` fields of an edge may refer to any addressable artifact, including another edge.

Allowed target families include, but are not limited to:

```text
P
ALS
ADR
R
SYN
EDGE
PEER
future CLAIM
future QUESTION
future EVIDENCE
future WARRANT
future ARTIFACT
```

Example:

```yaml
id: EDGE-0021
origin_type: relation_record
current_type: relation_record
title: Dispute of EDGE-0007
created_at: 2026-06-30T00:00:00Z

subject:
  id: R-0012
  scope: version
  version: 0.1

predicate:
  id: disputes
  vocabulary: bootstrap_predicates
  version: 0.1

object:
  id: EDGE-0007
  scope: exact

warrant:
  summary: "R-0012 argues that EDGE-0007 applies the wrong warrant."

contributors:
  - peer_id: PEER-0004
    role: relation_author
    substrate: Claude
```

This completes edge reification.

---

## 6. Reference Scope

Every edge reference must declare scope.

### 6.1 `scope: version`

Use `scope: version` when the relation applies only to a specific version of an artifact.

```yaml
object:
  id: ALS-0002
  scope: version
  version: 1.0-frozen
```

Meaning:

> This edge applies to ALS-0002 v1.0-frozen only.

### 6.2 `scope: lineage`

Use `scope: lineage` when the relation applies to the artifact identity across versions.

```yaml
object:
  id: ALS-0002
  scope: lineage
```

Meaning:

> This edge applies to ALS-0002 as an artifact lineage unless later resolved by another edge.

### 6.3 `scope: exact`

Use `scope: exact` for immutable edge records, peer identities, or content-addressed artifacts where there is no version lineage ambiguity.

```yaml
object:
  id: EDGE-0007
  scope: exact
```

Meaning:

> This edge targets exactly EDGE-0007.

### 6.4 Scope Is Required

Do not omit scope.

Avoid:

```yaml
object:
  id: ALS-0002
```

Prefer:

```yaml
object:
  id: ALS-0002
  scope: lineage
```

or:

```yaml
object:
  id: ALS-0002
  scope: version
  version: 1.0-frozen
```

---

## 7. Bootstrap Predicate Vocabulary

ADR-0003 v0.2 intentionally limits the bootstrap predicate vocabulary.

Because edges are immutable after commitment, predicates must not be used before their meaning is defined.

### 7.1 Vocabulary Identity

Every edge predicate must declare the vocabulary and version under which it is interpreted.

Canonical form:

```yaml
predicate:
  id: disputes
  vocabulary: bootstrap_predicates
  version: 0.1
```

Do not use unversioned predicates in committed edge records.

### 7.2 Minimal Bootstrap Predicates

The initial bootstrap vocabulary is:

| Predicate | Definition |
|---|---|
| `based_on` | The subject was produced using the target as input, basis, or prior context. |
| `reviews` | The subject evaluates, critiques, or comments on the target. |
| `supersedes` | The subject replaces the target as the newer active artifact or version. |
| `supports` | The subject provides positive warrant or evidence for the target. |
| `disputes` | The subject challenges the correctness, applicability, warrant, or interpretation of the target. |
| `resolves` | The subject addresses a prior dispute, problem, or open issue represented by the target edge. |

This vocabulary is intentionally small.

### 7.3 Disallowed Until Defined

Do not use the following predicates in committed edge records until a later ALS or ADR defines them:

```text
contradicts
qualifies
refines
warrants
nullifies
retracts
narrows
broadens
implements
depends_on
forks_from
```

These concepts may be important later, but their semantics are not yet stable enough for immutable edges.

### 7.4 Predicate Expansion

New predicates may be added only by a later specification or decision record that defines:

- predicate name;
- vocabulary version;
- meaning;
- valid subject/object types if constrained;
- fold behavior if relevant;
- and interaction with existing predicates.

---

## 8. Required Ordering Metadata

Every committed edge must include deterministic ordering metadata.

Minimum required field:

```yaml
created_at: 2026-06-30T00:00:00Z
```

`created_at` must use ISO-8601 UTC form.

A future implementation may add a monotonic sequence field:

```yaml
sequence: EDGESEQ-000001
```

If both `created_at` and `sequence` exist, the sequence field should be used for deterministic replay.

---

## 9. Edge Propagation and Inheritance

Edges do not propagate silently.

Their effect depends on scope.

### 9.1 Version-Scoped Edge

A version-scoped edge applies only to the named version.

Example:

```yaml
predicate:
  id: disputes
  vocabulary: bootstrap_predicates
  version: 0.1

object:
  id: ALS-0002
  scope: version
  version: 1.0-frozen
```

If ALS-0002 v2.0 is created, this edge does not automatically dispute v2.0.

However, graph views should still show that earlier versions were disputed.

### 9.2 Lineage-Scoped Edge

A lineage-scoped edge applies to the artifact identity across versions until another edge resolves it.

Example:

```yaml
predicate:
  id: disputes
  vocabulary: bootstrap_predicates
  version: 0.1

object:
  id: ALS-0002
  scope: lineage
```

If ALS-0002 v2.0 is created, the dispute remains visible until explicitly resolved.

### 9.3 Resolving a Lineage-Scoped Edge

Resolution requires a new edge.

```yaml
id: EDGE-0030
origin_type: relation_record
current_type: relation_record
title: ALS-0002 v2.0 resolves EDGE-0021
created_at: 2026-06-30T00:00:00Z

subject:
  id: ALS-0002
  scope: version
  version: 2.0-draft

predicate:
  id: resolves
  vocabulary: bootstrap_predicates
  version: 0.1

object:
  id: EDGE-0021
  scope: exact

warrant:
  summary: "ALS-0002 v2.0 removes the assumption disputed by EDGE-0021."
```

This prevents both critique laundering and unfair propagation.

---

## 10. Bootstrap Graph-State Fold

The current state of the bootstrap graph is computed by folding over ordered edge records.

### 10.1 Fold Inputs

The fold consumes:

- document metadata;
- committed edge records;
- predicate vocabulary definitions;
- ordering metadata;
- reference scope;
- and artifact versions.

### 10.2 Fold Order

Edges are applied in deterministic order:

1. sort by `sequence` if present;
2. otherwise sort by `created_at`;
3. if timestamps tie, sort by edge ID.

### 10.3 Fold Rules

Initial fold rules:

1. A `based_on` edge records provenance.
2. A `reviews` edge records review relation.
3. A `supersedes` edge marks the target as superseded by the subject.
4. A `supports` edge records positive warrant.
5. A `disputes` edge marks the target as disputed.
6. A `resolves` edge marks the target edge as resolved by the subject.

### 10.4 Scope-Aware State

- If a `disputes` edge targets `scope: version`, only that version is disputed.
- If a `disputes` edge targets `scope: lineage`, the lineage is disputed until the dispute edge is resolved.
- If a `resolves` edge targets a prior dispute edge, that dispute edge is considered resolved from the resolving edge onward.

### 10.5 No Silent Deletion

Resolved does not mean deleted.

A resolved dispute remains part of history.

Graph views may show both:

```text
historical dispute
current resolved state
```

---

## 11. Front-Matter Relations vs Edge Records

### 11.1 Front-Matter Relations

Front-matter relations are allowed only for simple local relations that are safe to freeze with the node.

Example:

```yaml
relations:
  - predicate:
      id: based_on
      vocabulary: bootstrap_predicates
      version: 0.1
    target:
      id: SYN-0004
      scope: version
      version: 0.1-draft
    warrant:
      summary: "This document incorporates SYN-0004."
```

### 11.2 Edge Records

Use edge records when:

- the relation targets a frozen artifact;
- the relation itself may be disputed;
- the relation has a nontrivial warrant;
- the relation should be independently cited;
- the relation targets another edge;
- the relation needs lineage/version/exact scope;
- or the relation should remain append-only.

### 11.3 No Duplicate Assertion

The same logical relation should not be asserted both in front matter and in a separate edge record.

If a relation becomes important enough to become an edge record, the edge record is authoritative.

---

## 12. Canonical Edge Schema

The bootstrap edge schema is:

```yaml
id: EDGE-0001
origin_type: relation_record
current_type: relation_record
title: Short human-readable title
created_at: 2026-06-30T00:00:00Z

subject:
  id: P-0042
  scope: version
  version: 0.1-draft

predicate:
  id: disputes
  vocabulary: bootstrap_predicates
  version: 0.1

object:
  id: ALS-0002
  scope: lineage

warrant:
  summary: "P-0042 argues that ALS-0002 relies on an invalid assumption."
  evidence:
    - id: P-0042
      scope: version
      version: 0.1-draft
      section: "Argument"

contributors:
  - peer_id: PEER-0001
    role: relation_author
    substrate: human
```

### 12.1 Required Fields

For bootstrap edge records, required fields are:

```text
id
origin_type
current_type
title
created_at
subject.id
subject.scope
predicate.id
predicate.vocabulary
predicate.version
object.id
object.scope
warrant.summary
contributors
```

### 12.2 Optional Fields

Optional fields include:

```text
subject.version
object.version
warrant.evidence
warrant.confidence
section
content_hash
sequence
```

---

## 13. Physical Storage

Logical edge identity is required.

Physical storage is an implementation detail.

### 13.1 One File Per Edge

```text
docs/edges/EDGE-0001.yaml
docs/edges/EDGE-0002.yaml
```

Advantages:

- simple;
- independently addressable;
- easy to inspect;
- easy to hash.

Disadvantages:

- may create many small files.

### 13.2 Append-Only Edge Ledgers

```text
docs/edges/P-0001.edges.yaml
docs/edges/ALS-0002.edges.yaml
```

Advantages:

- fewer files;
- easier human browsing for dense edge neighborhoods;
- less file-system churn.

Disadvantages:

- requires stricter append-only discipline;
- individual logical edges still need stable IDs;
- tooling must parse ledger records.

### 13.3 Decision for Bootstrap

AI-Lab will permit both one-file-per-edge and append-only ledgers.

The initial implementation may choose the simpler form.

The architectural requirement is:

> Each logical edge remains independently addressable, immutable after commitment, and foldable into graph state.

---

## 14. Catalog Discipline

Catalogs are derived indexes.

They should be generated from:

- document front matter;
- edge records;
- and, eventually, content hashes.

A catalog should not be manually maintained as the only source of truth.

### 14.1 Initial Bootstrap

During the earliest phase, the catalog may be absent.

The first implementation should prioritize:

```text
well-formed document metadata
well-formed edge records
simple validation script
```

### 14.2 Early Generator

As soon as practical, AI-Lab should include a small generator that reads Markdown/YAML front matter and edge records to produce:

```text
docs/catalog/documents.yaml
```

The generator reduces drift and prepares the project for a future graph engine.

---

## 15. Authorization and Ownership

ADR-0003 v0.2 does not fully define governance or authorization.

However, it recognizes that some predicates may require validation rules.

Example issue:

> Can the author of a disputed artifact unilaterally create a `resolves` edge, or must the original disputing peer or a designated human maintainer validate it?

Bootstrap stance:

- Anyone may propose a relation record.
- Human maintainers decide what enters the tracked baseline.
- Predicate-specific authorization rules are deferred to a later governance or epistemology specification.

This is intentionally minimal.

---

## 16. Prefix Discipline

Prefixes are birth-stamps and are never redefined.

Examples:

```text
P
ALS
ADR
R
SYN
EDGE
PEER
```

If a new artifact family is needed, create a new prefix.

Do not reinterpret an existing prefix.

A promoted artifact keeps its original ID.

---

## 17. Consequences

### 17.1 Positive Consequences

- Frozen documents remain immutable.
- Committed edges remain immutable.
- Later disputes remain possible.
- Edges can be disputed, corrected, or resolved.
- Provenance is append-only after commitment.
- Version-specific and lineage-wide relations are distinguishable.
- Predicate meaning is versioned.
- Catalogs can be generated rather than hand-maintained.
- The document layer becomes graph-importable.

### 17.2 Costs

- Edge records introduce additional structure.
- Contributors must understand scope and predicate vocabulary.
- Tooling will be needed to validate references.
- Graph-state computation requires a fold over ordered edge records.
- The bootstrap documentation system becomes more structured than ordinary Markdown.

### 17.3 Accepted Trade-Off

The added structure is accepted because the alternative would make AI-Lab vulnerable to:

- critique laundering;
- broken provenance;
- untraceable relation drift;
- silent predicate redefinition;
- and inconsistent graph-state computation.

---

## 18. Status

Accepted as draft architecture guidance.

This ADR should be reviewed before extensive edge records are created.

After review, it may become the stable baseline for implementing:

- `docs/edges/`;
- optional edge ledgers;
- graph-shaped Markdown validation;
- bootstrap predicate validation;
- document catalog generation;
- and future knowledge-graph import.

---

## 19. Open Questions

1. Should the initial implementation use one edge file per edge, or an edge ledger from the beginning?

2. Should structural and epistemic predicates be separated into different vocabularies?

3. Should graph views display lineage-scoped inherited disputes as inherited rather than directly asserted?

4. Should every edge eventually receive a content hash?

5. Should `PEER` records become first-class node artifacts before or after edge validation?

6. Should relation records live under `docs/edges/` or a more general `graph/edges/` path?

7. What predicate-specific authorization rules should apply beyond human maintainer review?

8. Should future predicate vocabularies be defined in ALS documents, ADRs, or machine-readable schemas?

---

## 20. Closing Statement

AI-Lab’s documentation graph should not evolve by rewriting history.

It should evolve by adding warranted relations to prior artifacts, including prior relations.

This ADR establishes the rule:

> Nodes may freeze. Edges may accumulate. Predicate meanings must be versioned. Graph state must be computed, not guessed.
