# ABS-0004 v9 assembly record

## Identity and scope

- Assembly executor self-report recorded by `DECISION-20260805-0002`:
  `gpt-5.6-thinking`, unverified.
- Repository HEAD used for this rebased assembly verification:
  `d07ece3c9e8025556d04970c8fde4143aac9b119`.
- Original assembly was produced against `944c3e6d92e75453f3f82bd42512a3a9cabada44`.
- Authority: `DECISION-20260805-0002`.
- Baseline authority: `DECISION-20260727-0002`.
- Scope: mechanical assembly only. No accepted ontology sentence was revised,
  no review question was drafted, and assembly does not admit v9.

## Updated-repository recheck

The repository advanced from `944c3e6` to `d07ece3` before the assembly was
applied. The intervening commits are:

- `6c615d4` — provider SDK requirement pins refreshed.
- `d07ece3` — `DECISION-20260810-0001`, GAP-0006 first slice: additive
  execution-outcome capture for the governed comparison path, plus its
  verification and self-model updates.

The ontology file and every accepted v9 reconstruction input are byte-identical
between `944c3e6` and `d07ece3`:

- `ABS-0004-v9-task2-required-changes.patch`
- `ABS-0004-v9-task3-limitations.patch`
- `ABS-0004-v9-identity-status.patch`
- `ASSEMBLY_RULE_CORRECTION.md`

The previously generated repository assembly patch applies cleanly to
`d07ece3`, and produces the same assembled ontology hash recorded below.

`DECISION-20260810-0001` adds an optional InvocationRecord `outcome` block
(`stop_reason`, its source field, token counts, content-block types and text
length) without changing stored record identities or the two-value invocation
status vocabulary. Rechecking the accepted v9 inputs found no accepted sentence
claiming that execution outcome or stop reason is absent from InvocationRecord.
Accordingly this repository update does not contradict an accepted v9 sentence
and supplies no authority to revise the accepted assembly text. Any broader
question about whether inherited implementation-sequence prose should be
refreshed belongs to review/adjudication, not mechanical assembly.

## Input chain

The admitted baseline was read from commit
`56f18a2ab7b66b1855b631a32d540f654c62b2c2`.

1. `ABS-0004-v9-task2-required-changes.patch` was applied to admitted v4.
   Its output was byte-identical to the committed task 2 candidate:
   `cda99362776f3e33026958319a84613cc094a4b8f111c267d0b95ef419da2061`.
2. `ABS-0004-v9-task3-limitations.patch` was applied to that output.
   Its output was byte-identical to the committed task 3 candidate:
   `67be6f2a8b55c57304e8498acd537ab5ebbb85ea3fd82e38c54c6bf52825af06`.
3. `ABS-0004-v9-identity-status.patch` was applied to that output.
   Its output was byte-identical to the accepted, lowercased identity-status
   candidate:
   `b74be817d6cdeb48db2bf05b20b719a157e7f3149c2d5f92a33ba5012be02948`.
4. `ASSEMBLY_RULE_CORRECTION.md` was applied: the sixteen surviving v4
   constraint occurrences were relabelled `[INHERITED_CONSTRAINT]`; the
   legend entry was replaced rather than renamed; `[LIMITATION]` was retained;
   `[PROPOSED_CONSTRAINT]` was not migrated.
5. Version metadata was assembled under `DECISION-20260805-0002`: v9 is
   `proposed`, v8 remains `withdrawn_after_admission_review`, v4 remains the
   last admitted version, the accepted input files are named, and the
   unverified drafting/assembly attribution is stated.

## Output

The assembled ontology is stored at:

`docs/abstractions/ABS-0004-invocation-authorization-ontology.md`

An exact retained copy is stored at:

`docs/self_model/v9_reconstruction/ABS-0004-v9-assembled.md`

The repository-level application patch is delivered outside the repository. A
unified-diff artifact contains required single-space context markers, which Git
reports as trailing whitespace when the patch itself is added as a tracked text
file. Keeping it external preserves `git diff --check` for the repository
change.

SHA-256 of both files:

`8f61c283a5d716f6816798a4946824b2d0d633a8be0d154da33cc1ebbe7ab1fa`

## Mechanical verification

- The ontology body after `## Evidence Inputs` is byte-identical to the
  accepted identity-status candidate after only the authorized tag migration.
- The original v4 Section 3 is an exact byte-for-byte prefix of v9 Section 3.
  Its SHA-256 is
  `66deb2d14f4790118da780571ed5c0a566d0d730738173ebdd15088618a055e4`.
- Three accepted Task 3 limitations follow that unchanged Section 3 core.
  No original Section 3 sentence was edited.
- Sixteen inherited constraint blocks occur exactly in admitted v4.
- `[ADOPTED_CONSTRAINT]`: zero occurrences.
- `[INHERITED_CONSTRAINT]`: seventeen occurrences, comprising one legend
  definition and sixteen constraints.
- `[PROPOSED_CONSTRAINT]`: ten occurrences, comprising one legend definition
  and nine constraints.
- `[LIMITATION]`: ten occurrences, comprising one legend definition and nine
  limitation statements.
- The ontology metadata states `version: v9` and `status: proposed`.
- The version table states v8 is withdrawn and v9 is proposed.

## Repository verification at d07ece3

- `git fsck --full`: clean before assembly.
- `python scripts/audit_self_model_index.py --repo-root .`: `ok: true`,
  `verification_outcome: verified_current`, with two informational findings.
- The sandbox does not contain the pinned OpenAI and Anthropic SDKs, so direct
  pytest collection stops at four import errors. With import-only SDK stubs
  outside the repository, the complete updated suite passes: `726 passed`.
  The stubs make no provider calls and modify no repository file.
- `git diff --check`: passed.
- The final repository patch was applied to a second clean clone of `d07ece3`;
  it reproduced the assembled ontology byte-for-byte and passed the same audit,
  test and diff checks.

## Not checked by assembly

- Assembly does not re-adjudicate the accepted Task 2, Task 3, or
  identity-status text.
- Assembly does not establish that v9 is correct, complete, or admissible.
- Assembly does not address the fifteen ledger entries classified as
  `separate gap or policy required`.
- Assembly does not resolve the four disputed bootstrap findings.
- Assembly does not update the inherited Section 13 challenge questions;
  review-question authorship belongs to the packaging executor under
  `DECISION-20260805-0002`.
- Assembly does not establish reviewer independence. The relation between
  `gpt-5.6-thinking` and the `gpt-5.6-terra` reviewer slot remains unresolved.
- Assembly does not adjudicate how GAP-0006's newly captured stop reasons should
  affect completeness assessment in the upcoming review round;
  `DECISION-20260810-0001` explicitly leaves that question open.
