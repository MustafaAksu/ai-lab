---
id: P-0001
origin_type: proposal
current_type: proposal
title: AI-Lab Documentation Architecture Proposal
version: 0.3-draft
status: proposal
layer: document-layer
category: documentation-architecture
supersedes:
  - P-0001:v0.2-draft
relations:
  - predicate: based_on
    target:
      id: SYN-0002
      version: 0.1-draft
    warrant:
      summary: "P-0001 v0.3 incorporates the second-round synthesis of reviews R-0003 and R-0004."
  - predicate: supersedes
    target:
      id: P-0001
      version: 0.2-draft
    warrant:
      summary: "v0.3 corrects the remaining identity and relationship issues identified in second-round review."
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
  - bootstrap_markdown_vs_future_graph_engine
  - human_legibility_vs_opaque_identity
  - immutable_documents_vs_evolving_relationships
  - relation_records_vs_front_matter_relations
  - provenance_rigor_vs_process_weight
---

# P-0001: AI-Lab Documentation Architecture Proposal

| Field | Value |
|---|---|
| **Document ID** | P-0001 |
| **Title** | AI-Lab Documentation Architecture Proposal |
| **Version** | 0.3-draft |
| **Status** | Proposal |
| **Date** | 2026-06-30 |
| **Supersedes** | P-0001 v0.2-draft |
| **Based on** | SYN-0002 |
| **Review history** | R-0001, R-0002, R-0003, R-0004 |
| **Prepared by** | Architect Peer |
| **Project Lead** | Mustafa Aksu |

---

## 1. Purpose

This proposal defines a provisional documentation architecture for **AI-Lab**, a long-lived research environment intended to support cumulative, traceable, and self-correcting scientific inquiry among human and AI research peers.

This proposal does **not** define the full AI-Lab knowledge layer.

It defines the first bootstrap form of the **document layer**: the human-readable and repository-manageable layer through which AI-Lab initially records specifications, proposals, reviews, syntheses, architecture decisions, relation records, and related provenance.

The central correction from P-0001 v0.2 is this:

> Documents may become immutable, but the graph around them must remain append-only and extendable.

Therefore P-0001 v0.3 adds:

- immutable birth-stamp identifiers,
- substrate-independent peer identities,
- canonical relation metadata,
- append-only relation records,
- generated catalog discipline,
- and the frozen-node / mutable-edge distinction.

---

## 2. Motivation

AI-Lab is not intended to be a conventional software project. It is intended to become a durable research environment where scientific understanding can accumulate across:

- changing human contributors,
- changing AI peers,
- changing providers,
- changing software stacks,
- changing storage systems,
- changing research domains,
- and changing generations of cognitive technology.

Ordinary project documentation is not sufficient for this purpose.

A long-lived research environment needs to preserve not only conclusions, but also:

- why decisions were made,
- what alternatives were considered,
- which peer contributed which idea,
- what was accepted,
- what was rejected,
- what was deferred,
- what remained contested,
- how documents relate to one another,
- and how understanding evolved.

P-0001 v0.1 introduced the need for multiple document families.

P-0001 v0.2 corrected the layer confusion by distinguishing the knowledge layer, document layer, and storage layer.

P-0001 v0.3 corrects the remaining identity and relationship problems:

1. A permanent ID must not become false when a document is promoted or reclassified.
2. A peer ID must not encode the provider or model substrate.
3. A frozen document must not need to be mutated when later challenged.
4. A catalog must not become the single authoritative source of graph truth.
5. Relationships must be represented as warranted, independently addressable records when they matter.

---

## 3. Layer Model

AI-Lab documentation is organized through three layers.

### 3.1 Knowledge Layer

The Knowledge Layer is the long-term target of AI-Lab.

It contains the durable structure of inquiry:

- questions,
- claims,
- evidence,
- warrants,
- relationships,
- disputes,
- revisions,
- provenance,
- open tensions,
- and status changes.

This layer is not fully implemented yet.

### 3.2 Document Layer

The Document Layer is the initial bootstrap layer.

It contains human-readable artifacts such as:

- proposals,
- specifications,
- reviews,
- syntheses,
- architecture decisions,
- relation records,
- catalogs,
- and methodology documents.

Documents are treated as graph-shaped carriers. They must expose enough structured metadata that they can later become nodes and edges in the Knowledge Layer.

### 3.3 Storage Layer

The Storage Layer contains infrastructure mechanisms:

- files,
- directories,
- Git,
- databases,
- object stores,
- and future graph engines.

The Storage Layer must not be treated as the authoritative source of meaning. A file path is a locator, not an ontology.

---

## 4. Core Design Principles

### 4.1 Documents Are Carriers, Not Knowledge Atoms

Documents are human-readable carriers and bootstrap graph nodes.

They are not the atomic unit of AI-Lab knowledge.

The deeper target remains warranted, traceable, revisable relationships among claims, questions, evidence, warrants, and artifacts.

### 4.2 Metadata Is Authoritative Over Paths

File paths may support human navigation, but they must not be treated as authoritative classification.

The file path is a locator.

The metadata describes identity, type, version, status, contributors, and relationships.

### 4.3 Identifiers Are Immutable Birth-Stamps

An identifier is assigned once and never changes.

An identifier records where an artifact began, not what it currently is.

For example:

```yaml
id: P-0001
origin_type: proposal
current_type: specification
```

This means:

- the artifact originated as a proposal;
- it may later become a specification;
- its ID remains stable;
- the current type is metadata.

This avoids breaking provenance when documents are promoted, reclassified, forked, or superseded.

### 4.4 Peer IDs Must Not Encode Substrate

A peer ID must not include model, provider, or vendor identity.

Use:

```yaml
peer_id: PEER-0002
display_name: Architect Peer
kind: ai_peer
substrate: GPT-5.5 Thinking
```

Do not use:

```yaml
peer_id: PEER-GPT-ARCHITECT
```

The substrate may change. The peer identity must remain stable.

### 4.5 Frozen Nodes, Mutable Edges

A frozen document should not be edited merely because a later document disputes, refines, or supersedes it.

Instead, new relationships should be added through append-only relation records.

The document node may freeze.

The graph topology around it must remain extendable.

### 4.6 Catalogs Are Derived Indexes

A catalog is a navigation and validation tool.

It should be generated from document metadata and relation records when possible.

It must not become the sole authoritative source of relationships.

### 4.7 Disagreement Must Travel With the Conclusion

A frozen document should remain structurally discoverable as contested if later relation records dispute it.

Disagreement must not be archived away from the conclusion it challenges.

---

## 5. Proposed Document Families

AI-Lab should maintain several document-layer families.

These families are bootstrap artifact types, not knowledge-layer primitives.

### 5.1 ALS — AI-Lab Specifications

ALS documents are normative project specifications.

They define stable AI-Lab concepts, principles, and structures.

Example:

```text
ALS-0001: Vision
ALS-0002: Principles
ALS-0003: Specification Methodology
ALS-0004: Epistemic Foundations
ALS-0005: Core Ontology
```

The prefix is an origin birth-stamp. It should not be interpreted as a mutable classification system.

### 5.2 ADR — Architecture Decision Records

ADR documents record engineering and architectural decisions.

They answer:

> Why did we choose this implementation or design direction?

ADR documents are more implementation-facing than ALS documents.

### 5.3 P — Proposals

Proposal documents are pre-specification design documents.

They are used when an idea is not yet mature enough to become an ALS or ADR.

A proposal may later be:

- promoted,
- superseded,
- forked,
- retired,
- rejected,
- or incorporated into another document.

If promoted, its ID remains unchanged.

### 5.4 R — Reviews

Review documents preserve independent critiques from human or AI research peers.

Reviews should not be silently merged into final documents.

They should be preserved as first-class records and structurally linked to the documents they review.

### 5.5 SYN — Syntheses

Synthesis documents reconcile reviews, identify convergences and divergences, and explain final decisions.

A synthesis must not erase dissent.

It must explicitly preserve unresolved objections, deferred questions, and open tensions.

### 5.6 EDGE — Relation Records

Relation records are append-only edge artifacts.

They declare relationships between documents, claims, artifacts, reviews, specifications, or future graph nodes.

They are required when:

- a frozen document is being disputed, refined, superseded, or supported;
- a relationship requires its own warrant;
- a relationship must be independently cited;
- a relationship should survive without mutating the related documents.

Example ID:

```text
EDGE-0001
```

The exact prefix is provisional.

The concept is required; the naming may evolve.

### 5.7 Catalogs

Catalogs are generated or derived maps of document-layer artifacts and relation records.

They may include:

- document IDs,
- paths,
- versions,
- statuses,
- relationships,
- contributors,
- supersession links,
- review links,
- edge records,
- and content hashes.

Catalogs are bootstrap tools for the future AI-Lab knowledge graph.

---

## 6. Canonical Metadata Schema

P-0001 v0.3 defines one canonical front-matter pattern for important Markdown artifacts.

### 6.1 Document Metadata

```yaml
---
id: P-0001
origin_type: proposal
current_type: proposal
title: AI-Lab Documentation Architecture Proposal
version: 0.3-draft
status: proposal
layer: document-layer
category: documentation-architecture
---
```

### 6.2 Contributor Metadata

```yaml
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
```

### 6.3 Local Relation Metadata

Local relations may be declared in front matter when the document is mutable and the relation is simple.

Use object-shaped relations, not freeform string arrays.

```yaml
relations:
  - predicate: based_on
    target:
      id: SYN-0002
      version: 0.1-draft
    warrant:
      summary: "This proposal incorporates the second-round review synthesis."
```

### 6.4 Avoid Freeform Pseudo-Edges

Do not create relation-like fields that point to unresolvable labels.

Avoid:

```yaml
critiques_addressed:
  - document_layer_vs_knowledge_layer_boundary
```

Prefer resolvable targets:

```yaml
relations:
  - predicate: addresses
    target:
      id: R-0004
      section: "The hardest-to-repair remaining mistake"
    warrant:
      summary: "v0.3 introduces birth-stamp IDs and substrate-independent peer IDs."
```

---

## 7. Relation Records / Edge Artifacts

Relation records are append-only artifacts used to represent relationships that must remain independently addressable.

### 7.1 When to Use a Relation Record

Use a relation record when:

- the relationship targets a frozen document;
- the relationship itself may be disputed;
- the relationship needs a warrant;
- the relationship should be independently cited;
- the relationship connects multiple artifacts across versions;
- the relationship should be visible without editing the target.

### 7.2 Example Relation Record

```yaml
---
id: EDGE-0001
origin_type: relation_record
current_type: relation_record
title: P-0042 disputes ALS-0002
version: 0.1
status: active

subject:
  id: P-0042
  version: 0.1-draft

predicate: disputes

object:
  id: ALS-0002
  version: 1.0-frozen

warrant:
  summary: "P-0042 identifies a contradiction in an assumption used by ALS-0002."
  evidence:
    - id: P-0042
      section: "Argument"

contributors:
  - peer_id: PEER-0007
    role: relation_author
    substrate: human
---
```

### 7.3 Relation Records Are Not Backlinks

A relation record is not a backlink inserted into the target document.

It is an independent edge artifact.

This prevents frozen documents from needing mutation when later contested.

### 7.4 Relation Records Can Be Indexed

Catalogs, rendered graph views, and future graph engines may index relation records to show incoming and outgoing edges for any document.

---

## 8. Inverse-Edge Discipline

Inverse edges should be derivable, not manually duplicated.

If one artifact declares:

```yaml
predicate: reviews
subject: R-0004
object: P-0001:v0.2-draft
```

the inverse relationship:

```text
P-0001:v0.2-draft is_reviewed_by R-0004
```

should be generated by tooling or graph traversal.

It should not be manually authored in another location unless there is a strong reason.

This avoids relation drift.

---

## 9. Document Catalog

AI-Lab should introduce a lightweight catalog only as a derived index.

A catalog may initially be generated manually, but the design target is:

```text
document metadata + relation records → generated catalog
```

A catalog should include:

```yaml
documents:
  - id: P-0001
    version: 0.3-draft
    path: docs/proposals/P-0001-AI-Lab-Documentation-Architecture-v0.3.md
    current_type: proposal
    status: proposal

relations:
  - id: EDGE-0001
    subject: P-0042
    predicate: disputes
    object: ALS-0002
```

The catalog is useful for navigation and validation.

It is not the ultimate authority.

---

## 10. Explicit Version Preservation

Git history is useful but insufficient as the sole long-term provenance mechanism.

Frozen and superseded documents should remain explicitly discoverable through:

- document ID,
- version,
- status,
- successor/predecessor links,
- content hash when available,
- and relation records.

The exact storage pattern is deferred.

Possible future approaches include:

- explicit versioned files,
- history directories,
- content-addressed archives,
- generated immutable snapshots,
- or graph-managed artifact storage.

The requirement is stable provenance, not a specific mechanism.

---

## 11. Research Artifacts and Repository Boundary

AI-Lab framework documentation and research program outputs must be distinguished.

### 11.1 Framework Documentation

Framework documentation defines AI-Lab itself:

- vision,
- principles,
- epistemology,
- ontology,
- architecture,
- engineering decisions,
- and documentation methodology.

### 11.2 Research Program Artifacts

Research program artifacts are scientific outputs produced using AI-Lab or eventually managed by AI-Lab.

Examples:

- RTG DSNs,
- papers,
- experiments,
- certificates,
- datasets,
- notebooks,
- simulation outputs.

These are not merely project documentation. They are scientific artifacts.

### 11.3 Deferred Repository Decision

It remains unresolved whether research program artifacts should live:

- in separate repositories,
- in a future AI-Lab-managed research graph,
- in a separate `research-programs/` area,
- or in another content-addressed archive.

This proposal only establishes the boundary.

---

## 12. Proposed Bootstrap Directory Structure

Because paths are locators rather than ontology, the initial directory structure should remain simple and family-based.

Proposed bootstrap structure:

```text
docs/
  proposals/
    P-0001-AI-Lab-Documentation-Architecture-v0.1.md
    P-0001-AI-Lab-Documentation-Architecture-v0.2.md
    P-0001-AI-Lab-Documentation-Architecture-v0.3.md

  reviews/
    R-0001-Claude-Review-of-P0001-v0.1.md
    R-0002-Gemini-Review-of-P0001-v0.1.md
    R-0003-Gemini-Review-of-P0001-v0.2.md
    R-0004-Claude-Review-of-P0001-v0.2.md

  synthesis/
    SYN-0001-P0001-v0.1-Review-Synthesis.md
    SYN-0002-P0001-v0.2-Review-Synthesis.md

  als/
    ALS-0001-Vision.md
    ALS-0002-Principles.md
    ALS-0003-Specification-Methodology.md

  adr/
    ADR-0001-Engineering-Constitution.md
    ADR-0002-Ontology-Precedes-Implementation.md

  edges/
    EDGE-0001.yaml

  catalog/
    documents.yaml
```

This structure is provisional.

It should be optimized for clarity and low friction, not treated as the ontology itself.

---

## 13. Document Lifecycle

AI-Lab documents should follow a scientific lifecycle rather than a purely bureaucratic one.

Proposed lifecycle:

```text
Idea
  ↓
Proposal
  ↓
Independent Review
  ↓
Synthesis
  ↓
Draft
  ↓
Review
  ↓
Frozen
  ↓
Superseded / Retired / Forked
```

### 13.1 Idea

An early concept without a stable document.

### 13.2 Proposal

A structured document describing a possible direction.

### 13.3 Independent Review

Human and AI peers critique the proposal independently.

### 13.4 Synthesis

Reviews are compared and synthesized.

The synthesis must preserve dissent and unresolved tensions.

### 13.5 Draft

A coherent document is produced.

### 13.6 Review

The draft receives a final review pass.

### 13.7 Frozen

The document becomes a stable baseline for implementation or future specifications.

Frozen does not mean final.

It means stable enough to build against.

### 13.8 Superseded

A later version replaces the frozen document, while the earlier version is preserved for provenance.

### 13.9 Retired

A document is no longer active but is not replaced by a direct successor.

### 13.10 Forked

A document or proposal splits into multiple warranted branches when synthesis cannot honestly converge.

---

## 14. Status, Confidence, and Warrant

P-0001 separates several axes.

### 14.1 Document Maturity

Document maturity describes lifecycle state.

Suggested values:

```text
idea
proposal
draft
reviewed
synthesized
frozen
superseded
retired
forked
```

### 14.2 Reviewer Confidence

Reviewer confidence describes confidence in a recommendation or critique.

Suggested values:

```text
high_confidence
moderate_confidence
speculative
```

### 14.3 Claim Warrant

Claim warrant describes epistemic status of a claim.

This belongs primarily to a later epistemology or ontology specification and should not be finalized here.

---

## 15. Open Tensions

Open tensions should be preserved in significant AI-Lab documents.

Current open tensions for this proposal:

### 15.1 Bootstrap Markdown vs Future Graph Engine

AI-Lab ultimately needs graph-native reasoning, but the early project must begin with ordinary files.

### 15.2 Human Legibility vs Opaque Identity

Fully opaque IDs are robust, but family-prefixed birth-stamps help early human navigation.

### 15.3 Immutable Documents vs Evolving Relationships

Frozen documents must not mutate, but later disputes and refinements must remain visible.

### 15.4 Relation Records vs Front-Matter Relations

Simple local relations may live in front matter, but warranted or post-freeze relations require independent edge artifacts.

### 15.5 Provenance Rigor vs Process Weight

More structure preserves more reasoning, but excessive ceremony can prevent reasoning from being documented at all.

### 15.6 Framework Documentation vs Research Outputs

AI-Lab must define itself without prematurely binding itself to RTG or any other specific research program.

---

## 16. Alternatives Considered

### 16.1 Use Only README and ADRs

Rejected.

A README and ADRs are useful but insufficient for a long-lived research environment.

### 16.2 Put Everything into ALS Documents

Rejected.

External reviews, proposals, syntheses, and relation records should remain distinct from normative specifications.

### 16.3 Treat Documents as the Knowledge Layer

Rejected.

Documents are carriers and views. The durable knowledge target is a graph of warranted, traceable, revisable relationships.

### 16.4 Rely on Git History Alone

Rejected.

Git history is useful infrastructure but should not be the only long-term provenance mechanism.

### 16.5 Use Live-Type IDs

Rejected.

IDs must not change meaning when documents are promoted or reclassified.

### 16.6 Use Substrate-Encoded Peer IDs

Rejected.

Peer IDs must not encode provider, vendor, or model identity.

### 16.7 Store All Relations Only in Front Matter

Rejected.

Frozen documents cannot be mutated to add later backlinks. Important evolving relationships require relation records.

### 16.8 Treat Catalog as Authoritative Graph Truth

Rejected.

The catalog should be derived or generated, not the sole source of relationship truth.

### 16.9 Implement a Full Graph Engine Immediately

Rejected for now.

The graph engine is the right long-term direction, but the bootstrap phase should use structured Markdown, relation records, and lightweight catalogs.

---

## 17. Recommendation

This proposal recommends that AI-Lab adopt a bootstrap documentation architecture consisting of:

- graph-shaped Markdown documents,
- immutable birth-stamp IDs,
- substrate-independent peer IDs,
- canonical metadata,
- object-shaped local relations,
- append-only relation records,
- generated catalog discipline,
- independent reviews,
- synthesis records,
- explicit version preservation,
- and a clear separation between document layer, knowledge layer, and storage layer.

P-0001 v0.3 should now be reviewed as the candidate implementation proposal.

If no further hard-to-repair structural flaw is identified, the next step should be to create the initial documentation infrastructure in the repository.

---

## 18. Review Request for P-0001 v0.3

Reviewers are asked to answer:

1. Does P-0001 v0.3 resolve the remaining identity and relationship issues from v0.2?
2. Are immutable birth-stamp IDs sufficient, or should IDs become fully opaque now?
3. Is the frozen-node / mutable-edge distinction correct?
4. Are append-only relation records necessary at this stage, or too heavy?
5. Is the canonical relation schema adequate?
6. Is the generated-catalog discipline clear enough?
7. What architectural mistake in P-0001 v0.3 would be hardest to repair later?

Please classify major recommendations as:

- high_confidence
- moderate_confidence
- speculative

The goal is not agreement.

The goal is convergence toward a documentation system that can preserve the evolution of understanding.

---

## 19. Closing Statement

P-0001 v0.3 reframes AI-Lab documentation as a bootstrap graph of persistent nodes and append-only edges.

The immediate implementation is still simple Markdown and YAML.

The long-term target is not a folder tree.

The long-term target is a warranted, traceable, revisable graph of understanding.
