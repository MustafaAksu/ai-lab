---
id: P-0001
title: AI-Lab Documentation Architecture Proposal
version: 0.2-draft
status: proposal
document_type: proposal
layer: document-layer
category: documentation-architecture
supersedes:
  - P-0001:v0.1-draft
relations:
  based_on:
    - SYN-0001
  reviewed_by:
    - R-0001
    - R-0002
  critiques_addressed:
    - document_layer_vs_knowledge_layer_boundary
    - semantic_ids_and_paths
    - document_isolation
    - git_history_fallacy
    - synthesis_consensus_bias
    - contributor_identity_vs_substrate
contributors:
  - peer_id: PEER-MUSTAFA-AKSU
    display_name: Mustafa Aksu
    kind: human
    role: project_lead
    substrate: human
  - peer_id: PEER-GPT-ARCHITECT
    display_name: GPT Architect
    kind: ai_peer
    role: drafter
    substrate: GPT-5.5 Thinking
  - peer_id: PEER-CLAUDE-REVIEWER
    display_name: Claude Reviewer
    kind: ai_peer
    role: independent_reviewer
    substrate: Claude
  - peer_id: PEER-GEMINI-REVIEWER
    display_name: Gemini Reviewer
    kind: ai_peer
    role: independent_reviewer
    substrate: Gemini
open_tensions:
  - document_layer_vs_knowledge_layer
  - graph_native_design_vs_bootstrap_markdown
  - provenance_rigor_vs_process_weight
  - stable_identity_vs_revisable_classification
  - synthesis_vs_epistemic_forking
---

# P-0001: AI-Lab Documentation Architecture Proposal

| Field | Value |
|---|---|
| **Document ID** | P-0001 |
| **Title** | AI-Lab Documentation Architecture Proposal |
| **Version** | 0.2-draft |
| **Status** | Proposal |
| **Date** | 2026-06-30 |
| **Supersedes** | P-0001 v0.1-draft |
| **Based on** | SYN-0001 |
| **Review history** | R-0001, R-0002 |
| **Prepared by** | GPT Architect |
| **Project Lead** | Mustafa Aksu |

---

## 1. Purpose

This proposal defines a provisional documentation architecture for **AI-Lab**, a long-lived research environment intended to support cumulative, traceable, and self-correcting scientific inquiry among human and AI research peers.

This proposal does **not** define the full AI-Lab knowledge layer.

It defines the first bootstrap form of the **document layer**: the human-readable and repository-manageable layer through which AI-Lab initially records specifications, proposals, reviews, syntheses, architecture decisions, and related provenance.

The central correction from P-0001 v0.1 is this:

> Documents are not the atomic unit of AI-Lab knowledge. Documents are carriers, views, and bootstrap graph nodes over a deeper layer of claims, questions, evidence, warrants, relationships, disputes, and revisions.

This proposal should be reviewed before any permanent documentation hierarchy is institutionalized.

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

P-0001 v0.1 attempted to create such a documentation architecture, but first-round peer review revealed a structural risk: it could accidentally make documents look like the durable unit of knowledge.

P-0001 v0.2 corrects that by introducing a three-layer distinction:

```text
Knowledge Layer
  The deeper target: claims, questions, evidence, warrants,
  relationships, disputes, provenance, revisions.

Document Layer
  The initial human-readable carriers: ALS, ADR, P, R, SYN,
  catalogs, and structured Markdown files.

Storage Layer
  The infrastructure: files, directories, Git, databases,
  object stores, and future graph engines.
```

The document layer is necessary, but it must not pretend to be the whole knowledge system.

---

## 3. Design Goals

The documentation architecture should satisfy the following goals.

### 3.1 Preserve Purpose

AI-Lab must preserve its foundational purpose independently of any particular implementation, provider, model, tool, or research program.

### 3.2 Preserve Reasoning

Important conclusions must retain their rationale, provenance, evidence, disagreements, review history, and revision path.

### 3.3 Keep Documents in Their Proper Layer

Documents are important human-readable carriers, but they are not the deepest durable knowledge units.

The documentation system must therefore preserve relationships among documents in a way that can later be imported into a deeper AI-Lab knowledge graph.

### 3.4 Make Relationships Explicit

Relationships such as `reviews`, `synthesizes`, `supersedes`, `implements`, `critiques`, `depends_on`, and `disputes` must not exist only in filenames, folder paths, or prose.

They should be declared in structured metadata.

### 3.5 Separate Identity from Classification

Permanent document IDs should not encode mutable categories such as philosophy, epistemology, ontology, or architecture.

Classification should be metadata.

### 3.6 Support Independent Peer Review

Human and AI research peers should be able to review proposals independently before synthesis.

### 3.7 Preserve Disagreement Structurally

Disagreement should not be erased by synthesis. Reviews, objections, unresolved tensions, and alternative branches must remain structurally linked to the documents they affect.

### 3.8 Support Versioned Freezing

Important documents should be frozen as stable baselines without pretending to be final. Later revisions should supersede earlier versions without erasing them.

### 3.9 Avoid Premature Institutionalization

The documentation system should remain lightweight while its methodology matures.

Heavyweight specifications should be rare. Lightweight proposals and reviews should remain cheap.

---

## 4. Layer Model

P-0001 v0.2 introduces an explicit layer model.

### 4.1 Knowledge Layer

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

### 4.2 Document Layer

The Document Layer is the initial bootstrap layer.

It contains human-readable artifacts such as:

- proposals,
- specifications,
- reviews,
- syntheses,
- architecture decisions,
- catalogs,
- and methodology documents.

Documents are treated as graph-shaped carriers. They must expose enough structured metadata that they can later become nodes and edges in the Knowledge Layer.

### 4.3 Storage Layer

The Storage Layer contains infrastructure mechanisms:

- files,
- directories,
- Git,
- databases,
- object stores,
- and future graph engines.

The Storage Layer must not be treated as the authoritative source of meaning. A file path is a locator, not an ontology.

---

## 5. Core Distinctions

This proposal distinguishes between five conceptual categories of AI-Lab specification content.

These categories are metadata labels, not permanent identity schemes.

### 5.1 Philosophy

Philosophy content answers:

> Why does AI-Lab exist?

Example topics:

- vision,
- purpose,
- human and AI peer collaboration,
- scientific continuity,
- self-correction,
- long-term ambition.

### 5.2 Epistemology

Epistemology content answers:

> What is knowledge, and how does scientific understanding become justified?

Example topics:

- claims,
- questions,
- evidence,
- warrants,
- provenance,
- disagreement,
- self-correction,
- justification structures.

### 5.3 Ontology

Ontology content answers:

> What exists in the AI-Lab research domain?

Example topics:

- identity,
- research program,
- research session,
- claim,
- question,
- artifact,
- evidence,
- warrant,
- relationship,
- perspective,
- experience.

### 5.4 Architecture

Architecture content answers:

> How should AI-Lab be structurally organized?

Example topics:

- provider abstraction,
- context packs,
- memory boundaries,
- artifact archive,
- graph structure,
- session persistence,
- multi-peer dialogue.

### 5.5 Engineering

Engineering content answers:

> How is the architecture implemented?

Example topics:

- code structure,
- tests,
- APIs,
- storage,
- command-line tools,
- deployment,
- continuous integration.

---

## 6. Proposed Document Families

AI-Lab should maintain several document families, each with a distinct purpose.

These families are document-layer types. They are not the same as knowledge-layer ontology primitives.

### 6.1 ALS — AI-Lab Specifications

ALS documents are normative project specifications.

They define stable AI-Lab concepts, principles, and structures.

Examples:

```text
ALS-0001: Vision
ALS-0002: Principles
ALS-0003: Specification Methodology
ALS-0004: Epistemic Foundations
ALS-0005: Core Ontology
```

The numbering is intentionally sequential and minimally semantic. The category of each ALS belongs in metadata, not in the ID itself.

### 6.2 ADR — Architecture Decision Records

ADR documents record engineering and architectural decisions.

They answer:

> Why did we choose this implementation or design direction?

ADR documents are more implementation-facing than ALS documents.

### 6.3 P — Proposals

Proposal documents are pre-specification design documents.

They are used when an idea is not yet mature enough to become an ALS or ADR.

This document is an example:

```text
P-0001: AI-Lab Documentation Architecture Proposal
```

Proposals may later be promoted, superseded, forked, retired, or rejected.

### 6.4 R — Reviews

Review documents preserve independent critiques from human or AI research peers.

Reviews should not be silently merged into final documents.

They should be preserved as first-class records and structurally linked to the documents they review.

### 6.5 SYN — Syntheses

Synthesis documents reconcile reviews, identify convergences and divergences, and explain final decisions.

They answer:

> What did we learn from the reviews, and what did we decide?

A synthesis must not erase dissent. It must explicitly preserve unresolved objections and open tensions.

### 6.6 Catalogs

Catalogs are index documents or structured data files that record document-layer relationships.

A catalog may include:

- document IDs,
- paths,
- versions,
- statuses,
- relationships,
- contributors,
- supersession links,
- review links,
- and content hashes.

Catalogs are bootstrap tools for the future AI-Lab knowledge graph.

---

## 7. Research Artifacts and Repository Boundary

P-0001 v0.1 placed research artifacts under the same proposed documentation tree as AI-Lab framework specifications.

First-round review identified this as a category risk.

AI-Lab framework documentation and research program outputs must be distinguished.

### 7.1 Framework Documentation

Framework documentation defines AI-Lab itself:

- its vision,
- principles,
- epistemology,
- ontology,
- architecture,
- engineering decisions,
- and documentation methodology.

### 7.2 Research Program Artifacts

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

### 7.3 Deferred Repository Decision

It remains unresolved whether research program artifacts should live:

- in separate repositories,
- in a future AI-Lab-managed research graph,
- in a separate `research-programs/` area,
- or in another content-addressed archive.

This proposal only establishes the boundary.

---

## 8. Bootstrap Format: Graph-Shaped Markdown

Before AI-Lab has a full graph engine, documents should be written as **graph-shaped Markdown**.

A graph-shaped Markdown file is:

- readable by humans,
- editable with ordinary tools,
- stored as a normal file,
- but structured enough to become graph-importable later.

### 8.1 Required Front Matter

Important documents should include YAML front matter.

Example:

```yaml
---
id: P-0001
title: AI-Lab Documentation Architecture Proposal
version: 0.2-draft
status: proposal
document_type: proposal
layer: document-layer
category: documentation-architecture

relations:
  supersedes:
    - P-0001:v0.1-draft
  reviewed_by:
    - R-0001
    - R-0002
  synthesized_by:
    - SYN-0001
  depends_on: []
  implements: []
  disputes: []

contributors:
  - peer_id: PEER-MUSTAFA-AKSU
    display_name: Mustafa Aksu
    kind: human
    role: project_lead
    substrate: human

open_tensions:
  - document_layer_vs_knowledge_layer
---
```

### 8.2 Metadata Is Authoritative Over Paths

The front matter should be treated as the authoritative source for:

- identity,
- version,
- status,
- category,
- relationships,
- contributors,
- and open tensions.

The file path is a locator.

It may support human navigation, but it must not be treated as authoritative classification.

---

## 9. Proposed Bootstrap Directory Structure

Because paths are locators rather than ontology, the initial directory structure should remain simple and family-based.

Proposed bootstrap structure:

```text
docs/
  proposals/
    P-0001-AI-Lab-Documentation-Architecture-v0.1.md
    P-0001-AI-Lab-Documentation-Architecture-v0.2.md

  reviews/
    R-0001-Claude-Review-of-P0001-v0.1.md
    R-0002-Gemini-Review-of-P0001-v0.1.md

  synthesis/
    SYN-0001-P0001-v0.1-Review-Synthesis.md

  als/
    ALS-0001-Vision.md
    ALS-0002-Principles.md
    ALS-0003-Specification-Methodology.md

  adr/
    ADR-0001-Engineering-Constitution.md
    ADR-0002-Ontology-Precedes-Implementation.md

  catalog/
    documents.yaml
```

This structure is provisional.

It should be optimized for clarity and low friction, not treated as the ontology itself.

---

## 10. Document Catalog

AI-Lab should introduce a lightweight document catalog before implementing a full graph engine.

A catalog may initially be a YAML file:

```text
docs/catalog/documents.yaml
```

Example:

```yaml
documents:
  - id: P-0001
    version: 0.2-draft
    title: AI-Lab Documentation Architecture Proposal
    path: docs/proposals/P-0001-AI-Lab-Documentation-Architecture-v0.2.md
    document_type: proposal
    status: proposal
    category: documentation-architecture
    supersedes:
      - P-0001:v0.1-draft
    reviewed_by:
      - R-0001
      - R-0002
    synthesized_by:
      - SYN-0001
```

The catalog is not the ultimate graph.

It is a bootstrap map.

Later, it may be generated from document front matter or replaced by a true graph engine.

---

## 11. Document Lifecycle

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

### 11.1 Idea

An early concept without a stable document.

### 11.2 Proposal

A structured document describing a possible direction.

### 11.3 Independent Review

Human and AI peers critique the proposal independently.

### 11.4 Synthesis

Reviews are compared and synthesized.

The synthesis must preserve dissent and unresolved tensions.

### 11.5 Draft

A coherent document is produced.

### 11.6 Review

The draft receives a final review pass.

### 11.7 Frozen

The document becomes a stable baseline for implementation or future specifications.

Frozen does not mean final.

It means stable enough to build against.

### 11.8 Superseded

A later version replaces the frozen document, while the earlier version is preserved for provenance.

### 11.9 Retired

A document is no longer active but is not replaced by a direct successor.

### 11.10 Forked

A document or proposal splits into multiple warranted branches when synthesis cannot honestly converge.

---

## 12. Document Status, Confidence, and Warrant

P-0001 v0.1 mixed several different status systems.

P-0001 v0.2 separates them.

### 12.1 Document Maturity

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

### 12.2 Reviewer Confidence

Reviewer confidence describes confidence in a recommendation or critique.

Suggested values:

```text
high_confidence
moderate_confidence
speculative
```

### 12.3 Claim Warrant

Claim warrant describes epistemic status of a claim.

This belongs primarily to a later epistemology or ontology specification and should not be finalized here.

P-0001 should not attempt to define the full claim-warrant system.

---

## 13. Review Methodology

For important documents, AI-Lab should use independent peer review.

### 13.1 Independent Drafting or Critique

Multiple peers may draft or critique the same document independently.

### 13.2 Comparison

Responses are compared for:

- convergence,
- disagreement,
- missing concepts,
- category errors,
- level mismatches,
- implementation leakage,
- hidden assumptions,
- and hard-to-repair design risks.

### 13.3 Synthesis

A synthesis document identifies:

- accepted observations,
- rejected observations,
- deferred observations,
- unresolved disagreements,
- open tensions,
- and final recommendations.

### 13.4 Freezing

A document is frozen only after synthesis and review.

### 13.5 Forking

If synthesis cannot honestly resolve a disagreement, the process may produce multiple competing branches.

Forking should be rare but explicitly permitted.

---

## 14. Contributor Attribution

AI-Lab should preserve intellectual provenance.

Contributor records should be unified across human and AI contributors, while still distinguishing kind, role, and substrate.

Example:

```yaml
contributors:
  - peer_id: PEER-MUSTAFA-AKSU
    display_name: Mustafa Aksu
    kind: human
    role: project_lead
    substrate: human

  - peer_id: PEER-GPT-ARCHITECT
    display_name: GPT Architect
    kind: ai_peer
    role: drafter
    substrate: GPT-5.5 Thinking

  - peer_id: PEER-CLAUDE-REVIEWER
    display_name: Claude Reviewer
    kind: ai_peer
    role: independent_reviewer
    substrate: Claude
```

Attribution does not imply equal responsibility.

Human contributors retain accountability for claims released into the world.

AI contributors may be credited for reasoning contributions, critiques, drafts, and alternative perspectives.

---

## 15. Explicit Version Preservation

Git history is useful but insufficient as the sole long-term provenance mechanism.

Frozen and superseded documents should remain explicitly discoverable through:

- document ID,
- version,
- status,
- successor/predecessor links,
- content hash when available,
- and catalog entries.

The exact storage pattern is deferred.

Possible future approaches include:

- explicit versioned files,
- history directories,
- content-addressed archives,
- generated immutable snapshots,
- or graph-managed artifact storage.

The requirement is stable provenance, not a specific mechanism.

---

## 16. Open Tensions

Open tensions should be preserved in significant AI-Lab documents.

They are not ordinary open questions. They are durable design tensions that future contributors should not mistake for solved problems.

Current open tensions for this proposal:

### 16.1 Document Layer vs Knowledge Layer

Documents are necessary for bootstrapping, but must not become the deepest knowledge unit.

### 16.2 Graph-Native Design vs Bootstrap Markdown

AI-Lab ultimately needs graph-native reasoning, but the early project must begin with ordinary files.

### 16.3 Provenance Rigor vs Process Weight

More structure preserves more reasoning, but excessive ceremony can prevent reasoning from being documented at all.

### 16.4 Stable Identity vs Revisable Classification

Identifiers should remain stable, while categories and interpretations must remain revisable.

### 16.5 Synthesis vs Epistemic Forking

Synthesis creates coherence, but forced synthesis can erase legitimate disagreement.

### 16.6 Framework Documentation vs Research Outputs

AI-Lab must define itself without prematurely binding itself to RTG or any other specific research program.

---

## 17. Alternatives Considered

### 17.1 Use Only README and ADRs

Rejected.

A README and ADRs are useful but insufficient for a long-lived research environment. They do not adequately distinguish philosophy, epistemology, ontology, architecture, engineering, review, and synthesis.

### 17.2 Put Everything into ALS Documents

Rejected.

External reviews, proposals, and syntheses should remain distinct from normative specifications.

### 17.3 Treat Documents as the Knowledge Layer

Rejected.

Documents are carriers and views. The durable knowledge target is a graph of warranted, traceable, revisable relationships.

### 17.4 Rely on Git History Alone

Rejected.

Git history is useful infrastructure but should not be the only long-term provenance mechanism.

### 17.5 Use Category-Based Numbering

Rejected.

IDs such as `ALS-100` for epistemology and `ALS-200` for ontology encode mutable classification into permanent identity.

### 17.6 Implement a Full Graph Engine Immediately

Rejected for now.

The graph engine is the right long-term direction, but the bootstrap phase should use structured Markdown and lightweight catalogs.

---

## 18. Recommendation

This proposal recommends that AI-Lab adopt a bootstrap documentation architecture consisting of:

- graph-shaped Markdown documents,
- minimally semantic stable IDs,
- structured metadata,
- explicit relationship declarations,
- lightweight catalogs,
- independent reviews,
- synthesis records,
- explicit version preservation,
- and a clear separation between document layer, knowledge layer, and storage layer.

The next step should be a second independent review cycle of P-0001 v0.2.

Reviewers should focus especially on:

- whether the layer distinction is now clear,
- whether the bootstrap method is too heavy or too light,
- whether semantic relationships are adequately preserved,
- whether the proposed metadata is sufficient,
- whether the framework/research boundary is correct,
- and what mistake would still be hardest to repair in twenty years.

---

## 19. Open Questions

1. Should document IDs remain family-prefixed (`P-0001`, `ALS-0001`) or become fully opaque?

2. Should a catalog be written manually at first, generated from front matter, or postponed?

3. Which metadata fields are mandatory for all documents, and which are optional?

4. How should frozen versions be stored before content-addressing exists?

5. How should epistemic forks be named and related?

6. Should SYN remain a distinct document family, or become a subtype of review?

7. Should ontology and epistemology documents eventually become dual human-readable and machine-executable schema documents?

8. Should RTG artifacts live outside the AI-Lab framework repository from the beginning?

9. What is the minimum viable metadata set that preserves relationships without making documentation too costly?

---

## 20. Review Request for P-0001 v0.2

Reviewers are asked to answer the following:

1. Does P-0001 v0.2 adequately correct the document-layer / knowledge-layer confusion?

2. Does graph-shaped Markdown solve the bootstrap problem well enough?

3. Are the proposed document families still necessary, or is the system too complex?

4. Is the proposed ID strategy sufficiently robust for decades-scale provenance?

5. Does the proposal now preserve disagreement structurally rather than merely archiving it?

6. Does the framework documentation / research artifact boundary make sense?

7. What architectural mistake in P-0001 v0.2 would be hardest to repair later?

Please classify major recommendations as:

- high_confidence
- moderate_confidence
- speculative

The goal is not agreement.

The goal is convergence toward a documentation system that can preserve the evolution of understanding.

---

## 21. Closing Statement

P-0001 v0.2 reframes AI-Lab documentation as a bootstrap document graph.

The immediate implementation is simple Markdown.

The long-term target is not a folder tree.

The long-term target is a warranted, traceable, revisable graph of understanding.
