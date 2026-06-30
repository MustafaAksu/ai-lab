---
id: ADR-0003
origin_type: architecture_decision
current_type: architecture_decision
title: Edge Identity, Immutability, and Addressing
version: 0.1-draft
status: draft
layer: architecture
category: documentation-graph-bootstrap
relations:
  - predicate: based_on
    target:
      id: SYN-0003
      version: 0.1-draft
    warrant:
      summary: "SYN-0003 identified edge identity, immutability, and addressing as the remaining decision required before implementing the documentation graph bootstrap."
  - predicate: constrains
    target:
      id: P-0001
      version: 0.3-draft
    warrant:
      summary: "This ADR defines the edge model required by P-0001 v0.3."
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
open_tensions:
  - single_edge_files_vs_edge_ledgers
  - version_scoped_references_vs_lineage_scoped_references
  - structural_edges_vs_epistemic_edges
  - bootstrap_simplicity_vs_graph_completeness
---

# ADR-0003: Edge Identity, Immutability, and Addressing

| Field | Value |
|---|---|
| **Document ID** | ADR-0003 |
| **Title** | Edge Identity, Immutability, and Addressing |
| **Version** | 0.1-draft |
| **Status** | Draft |
| **Date** | 2026-06-30 |
| **Based on** | SYN-0003 |
| **Constrains** | P-0001 v0.3 |
| **Prepared by** | Architect Peer |
| **Project Lead** | Mustafa Aksu |

---

## 1. Context

P-0001 v0.3 established that AI-Lab documentation should begin as a bootstrap graph of human-readable Markdown nodes and append-only relation records.

The third review cycle accepted the node-level design:

- documents are carriers, not knowledge atoms;
- identifiers are immutable birth-stamps;
- peer IDs are substrate-independent;
- frozen documents should not be mutated;
- relations should be explicit and structured;
- catalogs should be derived indexes rather than authoritative graph truth.

However, the reviews identified a remaining edge-layer issue:

> Once edges become first-class artifacts, edges require the same identity, immutability, and addressing discipline as documents.

Without this decision, AI-Lab risks creating relation records that cannot themselves be disputed, corrected, retracted, inherited, scoped, or referenced reliably.

This ADR defines the bootstrap edge model.

---

## 2. Decision

AI-Lab will treat relation records as immutable, independently addressable edge artifacts.

An edge is not a mutable property of a document.

An edge is an artifact.

Therefore:

1. Each edge receives a stable ID.
2. Each edge is immutable after creation.
3. Edges may target documents, reviews, syntheses, proposals, ADRs, ALS documents, other edges, or future knowledge-layer objects.
4. Edge correction happens by creating another edge.
5. References must explicitly state whether they target a specific version or an artifact lineage.
6. Catalogs are derived from document metadata and edge records.
7. Physical edge storage is an implementation detail; logical edge identity is the architectural requirement.

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
SYN-0003
EDGE-0001
```

A node may be a document, review, synthesis, architecture decision, specification, relation record, or future knowledge-layer object.

### 3.2 Edge

An edge is a relation record that connects one subject to one object through a predicate and warrant.

Example:

```text
EDGE-0007:
  P-0042 disputes ALS-0002
```

### 3.3 Edge Artifact

An edge artifact is the stored representation of an edge.

In the bootstrap phase, this may be a YAML file or a record inside an append-only ledger.

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
- or one exact immutable edge.

---

## 4. Edge Immutability

Relation records are immutable after creation.

Do not edit an edge to change its meaning.

Do not mutate an edge by changing:

- predicate,
- subject,
- object,
- scope,
- warrant,
- status,
- or contributor attribution.

### 4.1 No Mutable Edge Status

Avoid this pattern:

```yaml
id: EDGE-0001
status: retracted
```

if `EDGE-0001` was previously active.

Changing status mutates the original edge and weakens provenance.

### 4.2 Correction by New Edge

To retract, dispute, refine, supersede, resolve, or nullify an edge, create a new edge targeting the prior edge.

Example:

```yaml
id: EDGE-0020
origin_type: relation_record
current_type: relation_record
title: Retraction of EDGE-0001

subject:
  id: PEER-0002
  scope: identity

predicate: retracts

object:
  id: EDGE-0001
  scope: exact

warrant:
  summary: "EDGE-0001 used an incorrect target reference."
```

This preserves the historical record while allowing the graph state to evolve.

---

## 5. Edges Can Target Edges

If relationships are first-class, then relationships must themselves be disputable.

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

subject:
  id: R-0012
  scope: version
  version: 0.1

predicate: disputes

object:
  id: EDGE-0007
  scope: exact

warrant:
  summary: "R-0012 argues that EDGE-0007 applies the wrong warrant."
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

> This edge applies to ALS-0002 as an artifact lineage unless later narrowed, resolved, nullified, or superseded by another edge.

### 6.3 `scope: exact`

Use `scope: exact` for immutable edge records or content-addressed artifacts where there is no version lineage ambiguity.

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

## 7. Edge Propagation and Inheritance

Edges do not propagate silently.

Their effect depends on scope.

### 7.1 Version-Scoped Edge

A version-scoped edge applies only to the named version.

Example:

```yaml
predicate: disputes
object:
  id: ALS-0002
  scope: version
  version: 1.0-frozen
```

If ALS-0002 v2.0 is created, this edge does not automatically dispute v2.0.

However, graph views should still show that earlier versions were disputed.

### 7.2 Lineage-Scoped Edge

A lineage-scoped edge applies to the artifact identity across versions until another edge narrows, resolves, nullifies, or supersedes it.

Example:

```yaml
predicate: disputes
object:
  id: ALS-0002
  scope: lineage
```

If ALS-0002 v2.0 is created, the dispute remains visible until explicitly resolved.

### 7.3 Resolving a Lineage-Scoped Edge

Resolution requires a new edge.

```yaml
id: EDGE-0030
origin_type: relation_record
current_type: relation_record
title: ALS-0002 v2.0 resolves EDGE-0021

subject:
  id: ALS-0002
  scope: version
  version: 2.0-draft

predicate: resolves

object:
  id: EDGE-0021
  scope: exact

warrant:
  summary: "ALS-0002 v2.0 removes the assumption disputed by EDGE-0021."
```

This prevents both critique laundering and unfair propagation.

---

## 8. Canonical Edge Schema

The bootstrap edge schema is:

```yaml
id: EDGE-0001
origin_type: relation_record
current_type: relation_record
title: Short human-readable title
created_at: 2026-06-30

subject:
  id: P-0042
  scope: version
  version: 0.1-draft

predicate: disputes

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

### 8.1 Required Fields

For bootstrap edge records, required fields are:

```text
id
origin_type
current_type
title
subject.id
subject.scope
predicate
object.id
object.scope
warrant.summary
contributors
```

### 8.2 Optional Fields

Optional fields include:

```text
created_at
subject.version
object.version
warrant.evidence
warrant.confidence
section
content_hash
```

---

## 9. Allowed Bootstrap Predicates

P-0001 and ADR-0003 do not define the full epistemic predicate system.

However, the bootstrap may use a small initial predicate set.

### 9.1 Structural Predicates

```text
based_on
reviews
synthesizes
supersedes
constrains
implements
depends_on
forks_from
```

### 9.2 Epistemic / Dialectic Predicates

```text
supports
disputes
contradicts
qualifies
refines
warrants
resolves
nullifies
retracts
narrows
broadens
```

This set is provisional and may later be formalized in an ALS ontology or epistemology specification.

---

## 10. Front-Matter Relations vs Edge Records

### 10.1 Front-Matter Relations

Front-matter relations are allowed only for simple local relations that are safe to freeze with the node.

Example:

```yaml
relations:
  - predicate: based_on
    target:
      id: SYN-0003
      scope: version
      version: 0.1-draft
    warrant:
      summary: "This document incorporates SYN-0003."
```

### 10.2 Edge Records

Use edge records when:

- the relation targets a frozen artifact;
- the relation itself may be disputed;
- the relation has a nontrivial warrant;
- the relation should be independently cited;
- the relation targets another edge;
- the relation needs lineage/version scope;
- or the relation should remain append-only.

### 10.3 No Duplicate Assertion

The same logical relation should not be asserted both in front matter and in a separate edge record.

If a relation becomes important enough to become an edge record, the edge record is authoritative.

---

## 11. Catalog Discipline

Catalogs are derived indexes.

They should be generated from:

- document front matter,
- edge records,
- and, eventually, content hashes.

A catalog should not be manually maintained as the only source of truth.

### 11.1 Initial Bootstrap

During the earliest phase, the catalog may be absent.

The first implementation should prioritize:

```text
well-formed document metadata
well-formed edge records
simple validation script
```

### 11.2 Early Generator

As soon as practical, AI-Lab should include a small generator that reads Markdown/YAML front matter and edge records to produce:

```text
docs/catalog/documents.yaml
```

The generator reduces drift and prepares the project for a future graph engine.

---

## 12. Physical Storage

Logical edge identity is required.

Physical storage is an implementation detail.

Acceptable forms include:

### 12.1 One File Per Edge

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

### 12.2 Append-Only Edge Ledgers

```text
docs/edges/P-0001.edges.yaml
docs/edges/ALS-0002.edges.yaml
```

Advantages:

- fewer files;
- easier human browsing for dense edge neighborhoods.

Disadvantages:

- requires stricter append-only discipline;
- harder to hash individual edges unless carefully structured.

### 12.3 Decision for Bootstrap

AI-Lab will initially prefer one file per edge for simplicity and clarity.

Edge ledgers remain a deferred optimization.

---

## 13. Prefix Discipline

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

## 14. Consequences

### 14.1 Positive Consequences

- Frozen documents remain immutable.
- Later disputes remain possible.
- Edges can be disputed, corrected, or resolved.
- Provenance is append-only.
- Version-specific and lineage-wide relations are distinguishable.
- Catalogs can be generated rather than hand-maintained.
- The document layer becomes graph-importable.

### 14.2 Costs

- Edge records introduce additional files.
- Contributors must understand scope.
- Tooling will be needed to validate references.
- The bootstrap documentation system becomes more structured than ordinary Markdown.

### 14.3 Accepted Trade-Off

The added structure is accepted because the alternative would make AI-Lab vulnerable to critique laundering, broken provenance, and untraceable relation drift.

---

## 15. Status

Accepted as draft architecture guidance.

This ADR should be reviewed before extensive edge records are created.

After review, it may become the stable baseline for implementing:

- `docs/edges/`,
- graph-shaped Markdown validation,
- document catalog generation,
- and future knowledge-graph import.

---

## 16. Open Questions

1. Should the initial implementation use one edge file per edge, or an edge ledger from the beginning?

2. Should structural and epistemic predicates be separated into different schemas?

3. Should `scope: lineage` apply forward automatically, or should graph views mark it as inherited rather than directly asserted?

4. Should every edge eventually receive a content hash?

5. Should `PEER` records become first-class node artifacts before or after edge validation?

6. Should relation records live under `docs/edges/` or a more general `graph/edges/` path?

---

## 17. Closing Statement

AI-Lab’s documentation graph should not evolve by rewriting history.

It should evolve by adding warranted relations to prior artifacts, including prior relations.

This ADR establishes the rule:

> Nodes may freeze. Edges may accumulate. History is corrected by new edges, not by mutating old ones.
