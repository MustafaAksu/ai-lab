# ABS-0004 v9 admission round: consolidated findings

Round COMP-0126..0134, nine questions, eighteen complete responses. The round ran
at repository commit `d5732b6e1290fa1c9933cc8bf98330b8fbfa03f9`; these findings
were re-verified at `7c650a4e18057ddca34d3d9abec4585f8b65c8b3`, which adds
two round-tooling scripts and changes nothing this record cites. For the operator's
adjudication. ABS-0004 v9 is proposed and not admitted.

**The round does not support admitting v9, and it is also not a clean
instrument.** Seven defects are directly verifiable against the repository and
need no further review. An eighth, A8, is a design finding supported by reviewer
construction and requires adjudication rather than verification; it is listed in
Part A because it belongs with the others substantively, not because it shares
their evidentiary status. Seven of the nine questions reported material
evidence insufficiency, so on those surfaces the absence of a finding is not
evidence that the surface passed.

## How to read attributions

- **[VERIFIED]** — checked against the repository by the question author while
  writing this record. The check is stated so it can be repeated.
- **Reviewer finding** — attributed to question and provider. Recording is not
  endorsement.
- **[CORRECTED]** — a claim in the question author's first synthesis that the
  reviewing executor showed to be wrong. The prior claim is stated, not removed.
- **[ADDED]** — found by the reviewing executor reading the raw round artifacts,
  not present in the question author's synthesis.

## Round integrity

Eighteen of eighteen invocations carry an execution outcome and none was
truncated: nine `end_turn` and nine `completed`. This is the first round in this
repository whose completeness is established from `stop_reason` rather than
inferred from response length, under DECISION-20260810-0001.

Reviewer independence is unresolved. The executor that drafted v9 self-reports as
`gpt-5.6-thinking`; one reviewer slot is `gpt-5.6-terra`. The provider's own
catalog asserts these are distinct identities and that catalog is a provider
self-report. Under C3 this round is `independence_unresolved`, as every round in
this repository is. Finding 4 below is what makes that phrase load-bearing rather
than routine.

---

## Part A. Defects verifiable without further review

Each of these can be checked against the repository as it stands. No reviewer
evidence set bears on whether they are real.

### A1. The enforcement matrix uses a normative state it does not define

**[VERIFIED]** Section 9 defines the vocabulary as
`Normative state: proposed | adopted-manual | machine-enforced.`
The C6 row carries `adopted, not currently evidenced`, which is not among them.
Every other row uses one of the three.

Reviewer finding, Q8b, gpt-5.6-terra: the state conflates three distinct
questions — whether the constraint was ever admitted, whether it is presently
operative, and whether there is evidence it was checked.

### A2. Four evidence cells name artifact classes rather than artifacts

**[VERIFIED]** The rule stated immediately above the table reads: *Manual
enforcement counts only when the check leaves a named artifact; the claim that a
check happens is not evidence.* The cells for C7, C9, C10 and C11 name
categories — "VERIFY records", "named disclosure statements in records",
"verifier identity in VERIFY command records", "disclosure statements in
DecisionRecords/warrants" — and no instance.

The matrix therefore fails its own rule in four rows.

### A3. The one named artifact does not evidence the constraint that cites it

**[VERIFIED] [ADDED]** The C3 row is the only one naming a specific artifact:
`WARR-20260719-0002`. That warrant targets `PLAN-20260719-0001`, and contains no
occurrence of C3, equivalence, ancestry, self-adjudication, or any attestation
that such a check occurred.

The question author had reported this artifact as existing and the reviewer's
inability to check it as a scoping fault. It exists; it does not evidence C3.
Taken with A2, no `adopted-manual` row has sufficient evidence as written.

### A4. P5 and Section 4.18 contradict each other

**[VERIFIED] [ADDED]** This is the most serious finding in the round.

P5: *Unknown facts block qualification; they never disappear from the vocabulary.
Uncertainty remains representable, and unknown lineage or identity never
increases independence.*

Section 4.18 derivation rule: *any dimension `disqualified` yields overall status
`dependent`; any dimension `unresolved` without a named compensating control
yields overall `unresolved`; otherwise `qualified_independent` with degradations
listed.*

An `unresolved` dimension accompanied by a named compensating control falls
through to `otherwise` and yields `qualified_independent`. Nothing requires the
compensating control to resolve the unknown. An unknown fact therefore stops
blocking qualification without being resolved, which is what P5 forbids three
sections earlier.

This is live rather than theoretical. Executor identity between
`gpt-5.6-thinking` and `gpt-5.6-terra` is unresolved. Under 4.18 as written,
naming a compensating control would yield `qualified_independent` for exactly the
pairing the ontology cannot resolve.

### A5. Section 4.17 converts a verification status by naming an artifact

**[VERIFIED] [ADDED]** *Self-authored-unreviewed verification cannot satisfy
admission for high-consequence outputs; the named independent review artifact
converts the status to `self_authored_with_review`.*

Naming an artifact performs the conversion. Nothing requires that the artifact
establish that the reviewer was independent, that reviewer identity was resolved,
that the review covered the relevant verifier version, inputs or tests, or that
it passed.

### A6. `[DEF]` carries normative content, and it does so in admitted v4

**[VERIFIED]** Reviewer finding, Q8a, claude-sonnet-5: the Section 3 subordinate
inheritance paragraph is tagged `[DEF]` while stating that a subordinate
execution outside the declared classes *requires its own authorization* and that
undeclared subordinate execution *is a disclosure violation*. Those determine
permitted behaviour and consequences.

**[CORRECTED]** The question author's first synthesis treated this as a v9
defect. The reviewing executor established that the paragraph is present in
admitted v4 unchanged. It is therefore a previously undiscovered weakness in v4's
sentence discipline, not a reconstruction failure. Section 4.17 carries a second
instance.

The consequence matters for v9's central innovation: retagging
`[ADOPTED_CONSTRAINT]` to `[INHERITED_CONSTRAINT]` guards one entry path into
normative text. `[DEF]` is another and is unguarded.

### A7. Byte identity is not semantic identity

**[VERIFIED] [ADDED]** C3 is byte-identical to its admitted v4 text. Sections 4.3
and 4.4, which define the `ModelIdentity` resolution that C3's equivalence test
turns on, grew from 1589 to 3506 characters in v9.

An inherited constraint whose referents changed is not necessarily the same
constraint. The verification performed before adopting `[INHERITED_CONSTRAINT]`
checked byte identity of the constraint and not stability of what it refers to,
so it could not have detected this.

### A8. C3 does not bar adjudication when equivalence is unresolved

**Not repository-verifiable.** This is a finding that a consequence is *absent*,
which no check over the current text can establish as a defect rather than a
choice. It rests on reviewer construction and needs adjudication.

Reviewer finding, Q4 and Q8b, both providers. C3's hard prohibition applies when
an equivalent executor identity is established. Where equivalence is unresolved,
the ontology yields `independence_unresolved` and "never an independent path".

Those are not the same as *this invocation may not adjudicate this claim*. A
possible same-executor relation can therefore avoid the prohibition by being
unresolvable rather than by being resolved. P5 reads as though it should supply
fail-closed behaviour; no rule connects it to that consequence.

**Requires adjudication rather than verification**: the finding is that a
consequence is absent, and its absence is a design question.

---

## Part B. Corrections to the question author's first synthesis

Recorded rather than removed. Each was found by the reviewing executor reading
the raw artifacts, which is the correction the arrangement exists to supply.

### B1. The COMP-0032 confabulation was isolated, and the record says how

**[CORRECTED]** The question author reported that nothing addresses how the
confabulated continuation was isolated from the twelve findings adopted into v4.
COMP-0032 states of continuation attempt 1: *Discarded; retained here as a live
specimen of coherent model failure on missing input*, and records attempt 2 as
discarded for truncation before attempt 3 was used.

What is genuinely absent is narrower: no claim-level lineage establishes that
each of the twelve accepted findings derives only from valid evidence. The v4
commit message enumerates the twelve, so there is traceability but not
finding-level provenance. That is a provenance weakness, not contamination.

### B2. v4's admission not being a DecisionRecord is disclosed, not hidden

**[CORRECTED]** The question author reported this as an internal inconsistency.
v4's own metadata states that structural DecisionRecord representation awaits
Slice C. It is a disclosed bootstrap limitation. It remains relevant because
`[INHERITED_CONSTRAINT]` depends on that admission, but the admission is not
invalid merely because a schema defined in the same evolving ontology was not yet
implemented.

### B3. A governance rule for inherited force does exist

**[CORRECTED]** The question author reported, following Q1, that no rule
establishes that verbatim reproduction of admitted text carries the original
admission's force forward. DECISION-20260727-0005 adopts exactly that category
and rule. The reviewers were not given it.

What survives is narrower and is Q1's real result: a reader of v9 alone cannot
check the claim, and the ontology does not carry the rule internally. The
reviewing executor also offers a reading that avoids the transfer problem
entirely — that the v4 occurrence remains operative because v4 remains admitted,
while the reproduced sentence inside proposed v9 is informational until v9 is
itself admitted. That reading is not the one v9's tag definition states.

**Q1 should be re-run with complete evidence before its conclusion is
adjudicated.**

---

## Part C. The pattern

Findings A2, A3, A4, A5 and the C6 activation condition in A1 are instances of
one architectural failure, identified by the reviewing executor:

> the existence of a record is substituted for evidence that the property the
> record represents actually holds.

It appears as role records standing in for a C6 evaluation, verifier identity
standing in for C10 independence, a named review artifact converting a
verification status, a named compensating control converting an independence
assessment, and evidence cells naming categories of record.

This is the same failure the withdrawn PLAN-20260723-0002 committed with
`check_depth`, where a field recording that a check ran was presented as
preventing a misreading. It warrants one consolidated correction rather than five
separate patches.

---

## Part D. The round's own limitations

**Seven of nine questions reported material evidence insufficiency**: Q1, Q2, Q4,
Q5, Q7, Q8a and Q8b, with narrower qualifications on Q3 and Q6.

The worst is Q7, which asked reviewers to assess fourteen inherited challenge
questions while supplying the question list and metadata only. One reviewer could
substantively evaluate one of the fourteen. Q1 asked whether sixteen inherited
constraints carry admitted status without supplying v4 or the decision that
created the category.

The question set was written by the question author, who drafted v5 through v8.
Its evidence sets were also its author's choices. This is the fourth consecutive
round in which prompts cited material that was not attached.

**Consequence for adjudication: this round is good evidence for the constructions
reviewers managed to build, and poor evidence for exoneration.** No surface
should be treated as having passed because no finding was reported against it.

---

## Part E. Recommended sequence

From the reviewing executor, endorsed by the question author.

1. Adjudicate Part A. Seven of the eight are directly repository-verifiable;
   A8 is the adjudication-dependent one.
2. Correct what is accepted under a new explicit governance decision. Do not
   patch v9 silently.
3. Re-run only the questions whose evidence sets prevented reliable judgment,
   Q1 above all, supplying the prerequisite artifacts: admitted v4,
   DECISION-20260727-0005, the assembly record, the constraint comparison, and
   the definitions on which inherited constraints depend.
4. Close with one unframed full-document question against the corrected
   candidate, asking for the most serious remaining admission defect not already
   named, and requiring an internal contradiction to be distinguished from a
   declared limitation.

Step 4 preserves what has repeatedly been the highest-value part of these rounds:
allowing a reviewer to leave the question author's frame. Every round so far has
produced its sharpest finding that way.

## Standing

ABS-0004 v9 is proposed and not admitted. v4 remains the last version with an
admission event. This record does not adjudicate; it assembles what the round
found, and what the round could not reach, for the accountable principal.
