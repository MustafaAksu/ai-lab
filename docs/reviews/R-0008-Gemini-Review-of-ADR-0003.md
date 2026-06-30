---
id: R-0008
origin_type: review
current_type: review
title: Gemini Review of ADR-0003
version: 0.1
status: archived_review
layer: architecture
category: edge-architecture-review
reviewed_document:
  id: ADR-0003
  version: 0.1-draft
relations:
  - predicate: reviews
    target:
      id: ADR-0003
      scope: version
      version: 0.1-draft
    warrant:
      summary: "Independent review of ADR-0003 edge identity, immutability, and addressing model."
contributors:
  - peer_id: PEER-0003
    display_name: Independent Reviewer A
    kind: ai_peer
    role: reviewer
    substrate: Gemini
open_tensions:
  - staging_vs_committed_immutability
  - edge_ledgers_vs_micro_files
  - predicate_authorization
  - lineage_resolution_compilation
  - unbounded_meta_edge_traversal
---

# R-0008: Gemini Review of ADR-0003

| Field | Value |
|---|---|
| **Document** | R-0008 |
| **Title** | Gemini Review of ADR-0003 |
| **Status** | Archived Review |
| **Reviewed Document** | ADR-0003: Edge Identity, Immutability, and Addressing |
| **Reviewer** | Gemini |
| **Date** | 2026-06-30 |

---

This review evaluates **ADR-0003** as the concrete architectural extension of `P-0001 v0.3`. By reifying relationships into independent, addressable, and immutable artifacts, this document successfully transitions AI-Lab from a document repository into a formalized, file-based hypergraph.

---

### 1. Does ADR-0003 resolve the remaining edge-layer issue from P-0001 v0.3?

**Yes.** It directly and elegantly resolves the *Epistemic Slate-Wiping Vulnerability* identified in the v0.3 review.

By introducing the explicit distinction between `scope: version` and `scope: lineage`, the system prevents authors from laundering away structural critiques via minor version updates. Requiring a dedicated, independent edge record (`predicate: resolves`) to explicitly clear a lineage-scoped dispute ensures that historical counter-arguments remain structurally bound to an evolving document until they are systematically addressed and validated by the community.

---

### 2. Is any part over-engineered for the bootstrap phase?

**Yes. The "No Mutable Edge Status" rule for uncommitted human error is overly dogmatic for a flat-file environment.**

The ADR dictates that if a contributor makes a simple mistake (such as a typo in a target ID or an incorrect predicate definition) when creating an edge file, they cannot modify that file; they must write a separate, new edge file (`EDGE-0020 retracts EDGE-0001`).

While conceptually pure for a mature, distributed database state machine, enforcing this during a **manual Git/Markdown bootstrap phase** introduces unnecessary friction. If a file has not yet been merged into the repository's main branch (i.e., it is still in a local working directory or a pull request), treating it as an immutable historical monument turns simple administrative corrections into an overly complex process.

---

### 3. Is any part still underspecified?

Two critical operational areas remain undefined:

* **Predicate Authorization and Identity Ownership:** The ADR notes that `EDGE-0030` can declare that a new document version `resolves` a historic dispute (`EDGE-0021`). However, it does not specify *who* holds the right to assert that predicate. Can the author of the disputed document unilaterally declare their own work "resolved," or must the resolution edge be authored or co-signed by the peer who raised the original objection? Without explicit authorization constraints, the graph is highly vulnerable to unmediated edit wars carried out via competing edge creations.
* **Compilation Semantics for Lineage Resolution:** Section 7.2 states that a lineage-scoped edge remains visible across future versions until resolved. The document does not specify whether the *catalog generator tool* should copy the inherited edge references directly into the generated entry for `v2.0`, or if graph tools must dynamically compute the lineage state on every traversal.

---

### 4. What is the hardest-to-repair mistake if we adopt this ADR?

#### The Fatal Choice: The Unbounded Meta-Graph Traversal Churn (The Edge-on-Edge Trap)

The most dangerous systemic flaw introduced by ADR-0003 is the combination of **unbounded edge-on-edge targeting** and the **one-file-per-edge physical storage model**.

Because edges are fully reified nodes that can target other edges without structural limits (`EDGE-0021 disputes EDGE-0007`), and corrections must occur via append-only edge expansion, you introduce an arbitrary-depth recursive evaluation path.

To determine whether a single relationship between two foundational specifications is currently active, disputed, qualified, or retracted, a bootstrap script cannot simply look at the files in question. It must read, parse, and recursively reconstruct an entire tree of meta-edges (e.g., *Edge 4 retracts Edge 3, which disputed Edge 2, which qualified Edge 1*).

Because these are stored as individual small files in `docs/edges/`, calculating basic graph status requires intensive disk I/O operations to parse hundreds or thousands of micro-YAML files. As the repository grows over several years, the execution time of your `generated-catalog` validation script will scale quadratically, eventually causing your local pre-commit hooks and continuous integration workflows to stall under heavy disk churn.

---

### 5. Targeted Strategic Recommendations

#### Recommendation 1: Shift from Micro-Files to Scoped Edge Ledgers

Abandon the "one file per edge" physical model before implementation begins. Instead, group edges into family-scoped append-only ledger files (e.g., `docs/edges/ALS-0002.edges.yaml`).

* **Why it matters:** This preserves the logical requirements of independent edge immutability and addressing, but dramatically optimizes disk I/O. It allows compilation scripts to fetch an entire neighborhood of relationships in a single read operation while saving humans from navigating an overwhelming directory of micro-files.
* *Classification: High confidence*

#### Recommendation 2: Introduce a "Staging vs. Committed" Immutability Boundary

Explicitly state that edge immutability only begins once an artifact is merged into a protected tracking branch (e.g., `main`). Allow local file modification, deletion, and rebasing within unmerged feature branches or local environments.

* **Why it matters:** This prevents the historical graph from becoming cluttered with trivial retractions caused by simple typos, copy-paste syntax mistakes, or formatting errors introduced during draft preparation.
* *Classification: High confidence*

#### Recommendation 3: Enforce a Maximum Meta-Edge Depth Layer

Restrict the structural depth of edge-on-edge targeting. Establish a rule that edges can modify or target other edges *only* through a tightly controlled set of structural meta-predicates (like `retracts` or `amends`), and explicitly forbid an epistemic predicate (like `disputes`) from targeting a structural modification edge.

* **Why it matters:** This bounds graph-traversal complexity to a predictable depth, ensuring that bootstrap validation scripts can accurately compute node status without executing open-ended, recursive graph-walking routines.
* *Classification: Moderate confidence*

#### Recommendation 4: Explicitly Define Predicate Ownership Rules

Incorporate a permission mapping matrix into the ontology. For example, mandate that a `resolves` edge can only be validated if its author matches the identity of the peer who created the original dispute edge, or if it is signed by a designated project administrator.

* **Why it matters:** This stops administrative overreaches and ensures that a consensus or resolution is genuinely achieved rather than simply declared unilaterally through edge accretion.
* *Classification: Speculative*
