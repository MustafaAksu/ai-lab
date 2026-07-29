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

Limitations 1 and 2 are recorded rather than fixed because fixing them requires
re-running all 64 linking invocations, and a re-link is already required when
ABS-0004 v8 changes block hashes; they should ride with that re-link. Limitation
3 needs an addition to the edge model rather than a re-link. Limitation 4 is
inherent to the calibration method and cannot be fixed, only stated.

1. **One claim links to one block.** Some claims are inherently about several.
   The clearest case is the round's own central finding -- that v7 bundles three
   adopted constraints with different justificatory status -- which concerns
   three blocks and is therefore recorded as null. The null bucket currently
   conflates "about several blocks" with "about nothing identifiable"; these are
   different and should be distinguishable.

2. **The vocabulary omits blocks the reviewers asked for.** 26 nulls name
   Section 4.7, Section 11, COMP-0037, or v6 text. None is in the vocabulary
   because none was in an evidence set for the round. Superseded ontology
   versions and prior comparison records need to be citable evidence units.

   This is not a theoretical gap. COMP-0037 was subsequently read and refuted a
   claim the round had produced; see limitation 3.

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

4. **Calibration is an upper bound on a biased sample**, as above.

## Edge semantics

An edge carries `(block_id, block_content_sha256)`. Block ids are deliberately
NOT stabilised against rewording: an amendment that changes a block's text
changes its hash and breaks every edge citing it.

That breakage is the mechanism, not a defect. A stable identifier would carry a
claim forward onto text that no longer says what the claim responded to, and the
edge would look sound while being false. Re-linking is part of amendment: when a
block changes, each claim citing it is re-adjudicated as still-applies,
superseded, or needs-re-review.

Re-linking triggers on hash mismatch, not on id absence. The slug can survive a
rewording; the hash cannot.

## Record type

These runs are recorded as `COMP-*` comparison artifacts because they go through
`scripts/compare_providers.py`. They are extraction and linking operations, not
review rounds. The comparison record type is being used for an act it was not
designed for. A distinct record type for extraction and linking runs belongs in
the graph ontology and was deliberately not invented ad hoc here.
