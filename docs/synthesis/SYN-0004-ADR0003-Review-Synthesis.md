---
id: SYN-0004
origin_type: synthesis
current_type: synthesis
title: Synthesis of ADR-0003 Reviews
version: 0.1-draft
status: draft
layer: architecture
category: edge-architecture-synthesis
synthesizes:
  - R-0007
  - R-0008
reviewed_document:
  id: ADR-0003
  version: 0.1-draft
relations:
  - predicate: synthesizes
    target:
      id: R-0007
      scope: version
      version: 0.1
    warrant:
      summary: "Synthesizes Claude's review of ADR-0003."
  - predicate: synthesizes
    target:
      id: R-0008
      scope: version
      version: 0.1
    warrant:
      summary: "Synthesizes Gemini's review of ADR-0003."
  - predicate: targets
    target:
      id: ADR-0003
      scope: version
      version: 0.1-draft
    warrant:
      summary: "Synthesis of the first ADR-0003 review cycle."
contributors:
  - peer_id: PEER-0001
    display_name: Mustafa Aksu
    kind: human
    role: project_lead
    substrate: human
  - peer_id: PEER-0002
    display_name: Architect Peer
    kind: ai_peer
    role: synthesizer
    substrate: GPT-5.5 Thinking
open_tensions:
  - edge_structure_vs_predicate_semantics
  - immutable_edges_vs_staging_corrections
  - minimal_predicates_vs_future_epistemic_richness
  - edge_ledger_storage_vs_edge_identity
  - authorization_vs_open_peer_dialectic
  - bounded_meta_edges_vs_full_reification
---

# SYN-0004: ADR-0003 Review Synthesis

| Field | Value |
|---|---|
| **Document** | SYN-0004 |
| **Title** | Synthesis of ADR-0003 Reviews |
| **Status** | Draft |
| **Synthesizes** | R-0007, R-0008 |
| **Reviewed Document** | ADR-0003: Edge Identity, Immutability, and Addressing |
| **Prepared by** | Architect Peer |
| **Project Lead** | Mustafa Aksu |
| **Date** | 2026-06-30 |
| **Next Target** | ADR-0003 v0.2 and ALS-0004 |

---

## 1. Purpose

This synthesis records the first review cycle for **ADR-0003: Edge Identity, Immutability, and Addressing**.

It identifies which parts of ADR-0003 are ready to keep, which must be revised, and which semantic questions should move into a separate specification.

---

## 2. Reviewed Artifacts

This synthesis is based on:

```text
docs/architecture/ADR-0003-edge-identity-immutability-and-addressing.md
docs/reviews/R-0007-Claude-Review-of-ADR-0003.md
docs/reviews/R-0008-Gemini-Review-of-ADR-0003.md
```

---

## 3. Overall Review Result

Both reviewers judged ADR-0003 as a strong and largely successful architectural artifact.

Accepted as resolved:

- edge records are required;
- edges must be immutable after commitment;
- edges can target edges;
- references need version/lineage/exact scope;
- correction should happen by adding new edges;
- catalogs should be derived indexes;
- frozen nodes require mutable append-only graph topology.

The remaining problem has moved from structure to semantics and operations:

> ADR-0003 freezes edge structure safely, but it does not yet safely freeze predicate meaning, graph-state computation, or operational immutability boundaries.

---

## 4. Major Convergence: Edge Structure Is Accepted

Claude judged that ADR-0003 resolves the v0.3 edge-layer defects.

Gemini judged that ADR-0003 resolves the edge-layer vulnerability from P-0001 v0.3.

The synthesis accepts:

> ADR-0003’s structural model is sound: edges are independently addressable artifacts, can target other edges, and use explicit reference scope.

**Decision:** Accepted with high confidence.

---

## 5. Major Issue: Predicate Semantics Are Not Safe Yet

Claude identified the strongest semantic issue:

> The predicate vocabulary is too broad and underdefined for immutable edges.

If an immutable edge uses a predicate whose meaning is later redefined, the edge’s text does not change but its interpretation silently shifts.

This recreates the same failure pattern previously avoided for document identity and edge identity.

### Accepted correction

Use a minimal, explicitly defined bootstrap predicate vocabulary.

Candidate bootstrap set:

```text
based_on
reviews
supersedes
supports
disputes
resolves
```

Do not allow broad provisional predicates such as:

```text
qualifies
nullifies
narrows
broadens
contradicts
refines
```

until an epistemology or ontology specification defines them.

**Decision:** Accepted with high confidence.

---

## 6. Major Issue: Predicate Vocabulary Requires Versioning

Claude recommended binding every edge to a predicate vocabulary version or namespace.

Accepted correction:

> Every edge must declare the predicate vocabulary version under which its predicate is interpreted.

Example:

```yaml
predicate:
  id: disputes
  vocabulary: BOOTSTRAP-PREDICATES
  version: 0.1
```

or compact form:

```yaml
predicate: bootstrap.v0_1.disputes
```

The exact syntax is deferred.

**Decision:** Accepted with moderate-high confidence.

---

## 7. Major Issue: Append-Only Requires Ordering

Claude identified that `created_at` was optional in ADR-0003, but ordered replay is required for append-only graph-state computation.

Accepted correction:

> Every edge record must include deterministic ordering metadata.

Minimum requirement:

```yaml
created_at: 2026-06-30T00:00:00Z
```

Future systems may add:

```yaml
sequence: EDGESEQ-000001
```

**Decision:** Accepted with high confidence.

---

## 8. Major Issue: Graph-State Fold Must Be Defined

Claude and Gemini both identified the need for compilation semantics.

The system needs a deterministic way to compute current graph state from an append-only edge log.

Accepted correction:

> ADR-0003 v0.2 or ALS-0004 must define a simple bootstrap fold rule.

Initial fold principle:

1. Sort edges by deterministic ordering metadata.
2. Interpret predicates using the edge’s declared vocabulary version.
3. Apply lineage-scoped edges across artifact versions unless later resolved.
4. Treat version-scoped edges as applying only to the named version.
5. Treat exact-scoped edges as applying only to the exact referenced artifact.
6. Compute active/disputed/resolved state by applying structural predicates such as `resolves` to prior edges.

**Decision:** Accepted with high confidence.

---

## 9. Major Issue: Staging vs Committed Immutability

Gemini identified a practical operational correction.

Edge immutability should begin when an artifact is committed to the protected project history, not while a contributor is still editing a local draft or pull request.

Accepted correction:

> Immutability applies after commit/merge into the tracked baseline, not during local drafting.

This avoids cluttering the graph with retractions for uncommitted typos.

**Decision:** Accepted with high confidence.

---

## 10. Major Issue: Edge Storage Should Be Ledger-Compatible

Gemini warned that one-file-per-edge may create file-system and cognitive overhead.

ADR-0003 treated storage as an implementation detail and initially preferred one file per edge.

Synthesis position:

> Logical edge identity is required. Physical storage remains flexible. The bootstrap implementation should not hard-code a one-file-per-edge assumption into the architecture.

Acceptable physical forms:

```text
one file per edge
append-only edge ledgers
future graph store
```

However, because Gemini’s scalability concern is practical, ADR-0003 v0.2 should make edge ledgers a first-class permitted bootstrap option.

**Decision:** Accepted with moderate-high confidence.

---

## 11. Major Issue: Authorization and Ownership

Gemini identified a semantic/governance question:

> Who is allowed to declare that a dispute has been resolved?

This is real, but it may be too early to formalize fully.

Synthesis position:

- ADR-0003 should not define full governance.
- ADR-0003 should acknowledge that predicates like `resolves` may require validation or countersignature rules.
- The actual authorization model should be deferred to a governance or epistemology specification.

**Decision:** Deferred with moderate confidence.

---

## 12. Major Issue: Bounded Meta-Edge Traversal

Gemini warned against unbounded meta-edge recursion.

Claude argued that edge-as-target is necessary.

Synthesis position:

> Edge-as-target must remain allowed, but bootstrap tooling should use a conservative predicate set and deterministic fold rules to bound practical traversal.

We should not forbid epistemic edges from targeting structural edges yet; that may overconstrain the model prematurely.

But we should define:

- minimal predicates;
- deterministic fold;
- no silent semantic interpretation;
- graph views may impose traversal depth limits for performance;
- validators should detect cycles or excessive recursion.

**Decision:** Accepted as an implementation warning; hard limit deferred.

---

## 13. Minor Correction: ADR-0003 Header Must Use Scope

Claude identified that ADR-0003’s own front matter relations omitted `scope`, violating the document’s own rule.

ADR-0003 v0.2 must fix its front matter.

**Decision:** Accepted.

---

## 14. Required Changes for ADR-0003 v0.2

ADR-0003 v0.2 must:

1. Require `created_at` or equivalent deterministic ordering metadata.
2. Add a staging vs committed immutability boundary.
3. Replace the broad provisional predicate list with a minimal defined bootstrap vocabulary.
4. Require predicate vocabulary versioning.
5. Define a simple graph-state fold.
6. Fix front matter relation scopes.
7. Clarify that storage can be edge files or edge ledgers.
8. Keep edge-as-target support.
9. Acknowledge authorization questions without solving them.
10. Defer full predicate ontology to ALS-0004 or equivalent.

---

## 15. Should We Write ADR-0003 v0.2 or ALS-0004 First?

Two paths exist.

### Option A — Revise ADR-0003 First

This keeps edge architecture and minimal predicate semantics together for implementation.

Advantages:

- fewer files before bootstrap implementation;
- all immediate implementation rules are in one place;
- easier to validate.

### Option B — Write ALS-0004 First

This separates semantics from architecture.

Advantages:

- cleaner ontology/epistemology boundary;
- avoids making predicates look like implementation details;
- better long-term conceptual separation.

### Synthesis Recommendation

Do both, but in sequence:

1. Write **ADR-0003 v0.2** as the immediate implementation-safe edge architecture.
2. Include only the minimal bootstrap predicate definitions required for validation.
3. Create **ALS-0004: Bootstrap Predicate Semantics** afterward if the predicate system needs broader conceptual treatment.

This avoids blocking implementation while preserving the long-term semantic boundary.

---

## 16. Final Recommendation

Proceed to draft:

```text
docs/architecture/ADR-0003-edge-identity-immutability-and-addressing-v0.2.md
```

This revised ADR should be implementation-safe.

After ADR-0003 v0.2 is reviewed and accepted, AI-Lab can implement:

- `docs/edges/`,
- optional edge ledgers,
- graph-shaped Markdown validation,
- catalog generation,
- and bootstrap predicate checking.

---

## 17. Closing Note

The review cycle confirms that AI-Lab’s documentation architecture has matured through a stable pattern:

```text
document identity
→ edge identity
→ predicate meaning
→ graph-state computation
```

The next correction should not reopen the whole design.

It should make the edge architecture semantically safe enough to implement.
