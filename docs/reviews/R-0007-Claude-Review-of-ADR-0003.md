---
id: R-0007
origin_type: review
current_type: review
title: Claude Review of ADR-0003
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
  - peer_id: PEER-0004
    display_name: Independent Reviewer B
    kind: ai_peer
    role: reviewer
    substrate: Claude
open_tensions:
  - edge_structure_vs_predicate_semantics
  - immutable_edges_vs_provisional_predicates
  - predicate_vocabulary_versioning
  - append_only_log_ordering
  - resolution_fold_semantics
---

# R-0007: Claude Review of ADR-0003

| Field | Value |
|---|---|
| **Document** | R-0007 |
| **Title** | Claude Review of ADR-0003 |
| **Status** | Archived Review |
| **Reviewed Document** | ADR-0003: Edge Identity, Immutability, and Addressing |
| **Reviewer** | Claude |
| **Date** | 2026-06-30 |

---

I've read ADR-0003 in full. This is the strongest artifact in the series. It resolves the entire edge-layer issue I raised against v0.3 — cleanly, and in a couple of places more thoroughly than I'd asked. The residual problem is real but it has moved one more layer up, from *storage* to *meaning*, and it's the same pattern that's recurred at every round.

Let me answer your four questions.

**1. Does ADR-0003 resolve the remaining edge-layer issue from v0.3?** Yes (high_confidence). The three v0.3 defects are gone. Immutability is now unambiguous and §4.1 explicitly kills the `status: active`/`retracted` mutation contradiction from the v0.3 example. Edge-as-target is fully specified — §5's EDGE-0021-disputes-EDGE-0007 example completes the reification, and the allowed-target list correctly includes future CLAIM/QUESTION/EVIDENCE so the model extends into the knowledge layer without rework. Version/lineage scope is resolved and actually improved by adding `exact` for edges (§6). Correction-by-new-edge (§4.2) and the no-duplicate-assertion rule with edge-record-is-authoritative (§10.3) close the dual-store ambiguity. The edge *data model* is now complete and internally consistent. So as a freeze of the edge-identity decision, it does its job.

**2. Over-engineered for bootstrap?** Mostly no — and this is worth saying, because the instinct to trim is usually right but here is mostly wrong. Immutability, edge-as-target, and scope are all cheap to specify now and ruinous to retrofit after edges accumulate, so freezing them early is correct, not premature. Lineage propagation (§7) is borderline but I'd keep it for the same reason. The one genuine over-reach is the **predicate vocabulary in §9**: twenty predicates, several near-synonymous (`disputes`/`contradicts`/`qualifies`; `refines`/`narrows`/`broadens`; `resolves`/`nullifies`/`retracts`), shipped with no definitions. That's too much undefined semantic surface for a bootstrap — and as Q4 explains, it's not merely excess, it's actively dangerous given immutability. Trim to a minimal *defined* set. (moderate_confidence.)

**3. Underspecified?** Yes, two concrete gaps plus the predicate one. First, **the resolution/fold semantics are missing**: the ADR defines how edges are *stored* but never how the *current state* of the graph is *computed* from the append-only log. §7.3 quietly assumes a dispute→resolved state machine ("ALS-0002 v2.0 resolves EDGE-0021"), and §7.1 says "graph views should show," but nothing defines the function that answers "is ALS-0002 currently disputed?" from the edge history. Every consumer — the catalog generator, graph views, the future engine — must implement that fold, and if two implement it differently the graph has no well-defined state. Second, and concretely: **`created_at` is optional (§8.2)**, yet any fold over an append-only log depends on deterministic ordering. Optional timestamps mean you cannot reliably replay the log to compute current state. `created_at` (or a monotonic sequence number) must be *required* for an append-only model — small fix, real consequence. (high_confidence.)

(Minor, but verifiable in the same spirit as past rounds: the ADR violates its own §6.4 "scope is required" rule — its header `relations` give `target: {id, version}` with no `scope`, while §10.1's canonical front-matter relation includes `scope: version`. Same self-inconsistency class as the v0.2 header. Worth a one-line cleanup.)

**4. Hardest-to-repair mistake if adopted as-is.** **Freezing the large, explicitly-provisional predicate vocabulary into immutable edges before the predicates' meaning is defined.** (high_confidence.) §9 calls the vocabulary "provisional and may later be formalized in an ALS ontology or epistemology specification" — but §4 makes the predicate field immutable. Those two statements are in tension in the most expensive possible way: every edge written today with `qualifies` or `nullifies` becomes a permanent assertion whose *meaning* is assigned retroactively when the epistemology spec later formalizes that predicate. The edges don't change a byte, yet their meaning silently shifts under them. That is precisely the failure this ADR was built to prevent — "history changing meaning" — reappearing at the semantic layer because immutability was applied to the storage of predicates before the semantics of predicates were stable. You cannot repair it by editing edges (they're immutable); you'd have to issue correction edges across potentially the entire historical corpus, and you can't recover the original author's intent reliably. Immutability is only safe for things whose meaning is already fixed, and the vocabulary's meaning is explicitly not.

The through-line is worth naming, because it's the same lesson three times: at v0.2 the hardest-to-repair thing was *document identity* committed before classification settled; at v0.3 it was *edge identity* committed before edges were treated as nodes; here it's *predicate identity* committed before predicate semantics are defined. Each round, immutability got correctly pushed onto a layer whose meaning wasn't yet stable. The predicate vocabulary is that pattern's final instance — and the last place it can bite before implementation.

The fix is light and mirrors the ADR's own instincts:

- Ship bootstrap with a **minimal, explicitly-defined predicate set** (≈5–6: `based_on`, `reviews`, `supersedes`, `supports`, `disputes`, `resolves`), each with a one-line definition, and forbid the rest until the epistemology ALS lands — **high_confidence**.
- Bind every edge to a **`vocabulary_version`** (or namespace), so a predicate is always interpreted against the vocabulary in force at the edge's creation — versioning the vocabulary exactly as you version artifacts. This is the durable general fix even after the set grows — **moderate-high_confidence**.
- Make **`created_at` (or a sequence number) required** — **high_confidence**.
- Specify the **resolution fold** — even a one-paragraph definition of how current dispute/supersession state is derived from the ordered edge log — before two tools implement it differently — **high_confidence**.
- Fix the header `relations` to carry `scope` per §6.4 — **moderate_confidence**.
- Consider whether strictly binary edges (§3.2) need an n-ary grouping mechanism (one synthesis reconciling several reviews); acceptable to defer, but note it — **speculative**.

Net: ADR-0003 correctly and durably freezes the edge *structure*. Before you adopt it as the implementation baseline, pin the edge *semantics* — minimal defined predicates, required ordering, a stated resolution fold, and vocabulary versioning. Do those four and I'd consider the edge layer genuinely safe to build against; the structural decisions here won't need to be reopened.

If you want, the highest-leverage next artifact is a short **epistemology ALS stub** that defines the minimal predicate set and the resolution fold — that's the missing semantic counterpart to this structural ADR, and it's small. I've drafted nothing per your standing instruction; say the word.
