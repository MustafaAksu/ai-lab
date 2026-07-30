# Claim graph over COMP-0039..0046

What this is, what it measures, and what it cannot do. Written at the close of
the build so the limits are recorded with the capability rather than after it.

## What it is

The eight-question atomic round produced sixteen review answers, roughly 96,000
characters. Reading them is how the round's findings were originally found. This
pipeline turns those answers into addressable claim nodes and links each to the
specific block of source text it concerns, so that a finding spanning several
answers can be retrieved rather than remembered.

Pipeline, all through `scripts/compare_providers.py` unchanged:

| stage | runs | invocations | output |
| --- | --- | --- | --- |
| extraction pass one | COMP-0047..0062 | 32 | 1379 claims, 77 quarantined |
| extraction pass two | COMP-0063..0078 | 32 | 530 claims, 14 quarantined |
| linking | COMP-0079..0110 | 64 | 1060 edges over 101 blocks |

Pass one is retained. It is not superseded work to be tidied away: it is the
evidence that established the granularity and fidelity problems pass two was
built to fix, and the comparison between the two is the measurement.

## Measured properties

**Granularity is normative, not natural.** Pass one asked for "one assertion per
claim" and got 970 claims from one extractor and 409 from the other, from the
same sixteen answers: a median ratio of 1.80. A claim is not a natural kind. Pass
two defined a claim by function -- an assertion a reader could accept, reject or
act on, excluding reasoning steps and restatements -- and the ratio fell to 0.91
(gpt 258, claude 272). Had extraction been single rather than dual, whichever
extractor was chosen would have silently become the definition.

**Quote fidelity, measured.** Every claim must carry a verbatim span from its
source answer, checked mechanically. Pass one: 23 elided quotes (ellipsis
bridging omitted material, which reads as verbatim while having removed the
qualifier that sat in the gap) and 36 reshaped. Pass two, with the quote rules
made strict: 0 elided, 14 reshaped, a fidelity failure rate of 2.57%. Without the
check those 14 would have entered the graph looking verbatim.

**Linker accuracy, upper bound 0.885.** 52 claims can be linked deterministically
because their quote matches exactly one block verbatim. Scored against that held
out set: claude-sonnet-5 49/52, gpt-5.6-terra 43/52. The set is NOT randomly
sampled -- it consists precisely of claims that quote source text, which are
plausibly the easiest to link -- so this bounds accuracy rather than estimating
it.

**Vocabulary completeness: 21% unlinked.** 219 of 1060 edges are null. Declining
was made a first-class answer because a wrong edge reads as structure and will be
trusted, while a missing one does not. The null rate therefore measures the
vocabulary, not the linker.

**Linker disagreement: 108 of 530 dual-linked claims.** Of these, 55 are one
linker declining while the other links, 24 are the same evidence unit at a
different block, and 21 are different units. Most disagreement is a decline
threshold difference rather than a dispute about the target.

## Known limitations

Status after the v7 to v8 re-link, which exercised the graph rather than
inspecting it. Each item below is annotated with what actually happened, because
in two cases the limitation as originally written was wrong.

Limitation 1 is CLOSED. Limitation 2 was WRONG as written and is corrected in
place. Limitation 3 is partially addressed. Limitation 4 cannot be fixed, only
stated. Limitations 5 and 6 were found by using the graph and are new.

1. **One claim links to one block.** Some claims are inherently about several.
   The clearest case is the round's own central finding -- that v7 bundles three
   adopted constraints with different justificatory status -- which concerns
   three blocks and is therefore recorded as null. The null bucket currently
   conflates "about several blocks" with "about nothing identifiable"; these are
   different and should be distinguishable.

   **CLOSED** in the v8 re-link, which permits up to three targets per claim,
   each a separate (block_id, content_sha256) pair breaking independently. This
   was not a marginal case: of 104 placements by the two linkers, 63 used one
   block, 38 used two, and 3 used three. The single-target restriction had been
   discarding 39% of the structure the linkers could see.

2. **The vocabulary omits blocks the reviewers asked for.** 26 nulls name
   Section 4.7, Section 11, COMP-0037, or v6 text. None is in the vocabulary
   because none was in an evidence set for the round. Superseded ontology
   versions and prior comparison records need to be citable evidence units.

   **CORRECTED.** The second sentence above is right and the first is wrong, and
   they were run together. Superseded ontology versions and prior comparison
   records do need to be citable, as evidence a future question can be given:
   COMP-0037 was subsequently read and refuted a claim the round had produced,
   which is limitation 3's worked example. But they are NOT the missing targets
   for those 26 nulls. All 26 are evidence_gap claims, and an evidence_gap claim
   is not about the named material's content; it is about what its question was
   given. Adding COMP-0037 to the vocabulary would invite the linker to place a
   claim about an absence onto the material that was absent. That is a wrong
   edge, not a recovered one, and both linkers had already declined for exactly
   that reason -- "it concerns the absence of v6 rule text", "the claim concerns
   the underlying COMP-0037 source material itself". The null-is-first-class
   design was protecting against the fix this limitation proposed.

   Section 11 WAS added in the re-link, on the opposite reasoning: claims about
   deferred enforcement objects are about its content.

3. **A claim node cannot carry what later happened to it.** Edges record what a
   claim is about. Nothing records that a claim was checked and found false,
   superseded, or confirmed. The graph represents claims about blocks, not the
   status of claims.

   The worked example is in this round. `CLAIM-7f96b4ee3de269fc` (Q1,
   claude-sonnet-5) asserts that v7's `[OPEN]` paragraph grounds its
   scope-breadth retreat in COMP-0037, "which is a fact about self-issuance, not
   about scope breadth." Reading COMP-0037 refutes this: Claude's own review
   there found that nothing constrained "the content or breadth of what may be
   declared as `authority_scope`", and gpt-5.6-terra recommended rejecting
   universal scopes outright. Scope was squarely implicated.

   Two properties of this case make it the right example. First, the same Q1
   answer also produced `CLAIM-c80738608c9c0608` (extracted by the other
   extractor), which states that COMP-0037 is needed to decide precisely this
   question -- so the graph already contains both the claim and the condition
   for checking it. Second, the record needed was committed in this repository
   throughout.

   Until a claim-status edge exists, a reader assembling ABS-0004 v8 from these
   nodes will read the refuted premise with nothing attached to it. The
   refutation is recorded in prose in the consolidated Slice C findings record;
   it is not reachable from the claim.

   Note what must NOT be done: COMP-0040 records what the reviewer answered and
   is correct as a record of that. Amending the artifact to fix the reviewer's
   premise would falsify it.

   **PARTIALLY ADDRESSED.** The disposition vocabulary now carries 'refuted', and
   six claims hold it, recorded in CLAIM_IMPACT.json with the reasoning. A
   disposition is not an edge: it exists only for claims whose edges an amendment
   broke, so a claim refuted without any amendment having touched its block still
   has nowhere to record that.

4. **Calibration is an upper bound on a biased sample**, as above.

5. **Three claim categories the block vocabulary cannot hold.** Found one at a
   time, by using the graph, and they are a pattern rather than three
   coincidences: the vocabulary holds claims **about source text** and has no
   node for claims about anything else.

   - **Evidence-gap claims**, about what a question was given rather than about
     any block's content. 26 instances; see limitation 2.
   - **Refuted claims**, about another claim's truth. 6 instances; see
     limitation 3.
   - **Verdict claims**, about the answer's own position rather than about the
     source. Found by the re-link cross-check, which reports claims
     dispositioned still_applies that neither linker could place. It found
     exactly one, and the disposition was right while the placement was
     impossible: "The answer favors reading (a), but only for the specific claim
     that an internal authorization structure can prevent convenient closure of
     the extra-systemic authorization regress." That position does still hold. It
     is not about a passage.

   The three share a shape. A claim's target may be a block, a question's
   evidence set, another claim, or the answer itself, and only the first exists.

6. **The edge set is not self-describing about validity.** linking/EDGES.json
   holds all 841 pass-one edges, including the 213 the v8 amendment broke, with
   their pre-amendment hashes. relink/EDGES_V8.json holds the 148 replacements. A
   reader needs three files -- EDGES.json, CLAIM_IMPACT.json and EDGES_V8.json --
   to determine which edges are live, and nothing in EDGES.json says so. An edge
   whose cited content_sha256 no longer matches its block is detectable, which is
   the mechanism working; but detecting it is left to the reader rather than
   recorded.

## Edge semantics

An edge carries `(block_id, block_content_sha256)`. Block ids are deliberately
NOT stabilised against rewording: an amendment that changes a block's text
changes its hash and breaks every edge citing it.

That breakage is the mechanism, not a defect. A stable identifier would carry a
claim forward onto text that no longer says what the claim responded to, and the
edge would look sound while being false. Re-linking is part of amendment: when a
block changes, each claim citing it is re-adjudicated. The v7 to v8
amendment exercised this: 213 of 841 edges broke and 118 claims were
dispositioned. The vocabulary needed five values, not the three named
here when this was written -- adopted, corrected, still_applies, refuted,
needs_re_review -- because 'superseded' conflated a recommendation being
taken with a criticised sentence being deleted, and because six claims
asserted something the record shows false, which an amendment contradicts
rather than responds to. See CLAIM_IMPACT.json.

Re-linking triggers on hash mismatch, not on id absence. The slug can survive a
rewording; the hash cannot.

## Record type

These runs are recorded as `COMP-*` comparison artifacts because they go through
`scripts/compare_providers.py`. They are extraction and linking operations, not
review rounds. The comparison record type is being used for an act it was not
designed for. A distinct record type for extraction and linking runs belongs in
the graph ontology and was deliberately not invented ad hoc here.
