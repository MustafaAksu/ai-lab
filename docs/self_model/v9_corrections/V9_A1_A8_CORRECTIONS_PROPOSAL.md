# ABS-0004 v9 — A1–A8 correction proposal

## Status

Drafting proposal only. This artifact does not adjudicate or apply any correction.
It is based on repository HEAD `4c29406bcf54f48510a8cec8ffeeb2beaa774535`
and `DECISION-20260811-0001`.

The proposed ontology keeps `version: v9` and `status: proposed`. The decision on
whether the corrected candidate is called v9 or v10 remains deliberately
unmade, as required by `DECISION-20260811-0001`.

## Role and transport choices

- Correction drafter: the executor self-reporting as `gpt-5.6-thinking` (Sol).
- The correction drafter must not review these corrections.
- Review-question authorship should remain with a different executor. Because
  the preceding question set under-supplied evidence in seven of nine questions,
  the next question-authoring step should require a per-question evidence
  manifest and a preflight that proves every cited artifact is actually
  attached before any provider call is made.
- Transport recommendation: stop using base64-in-shell-script transport for
  ontology text. Retain literal proposal/patch files in the laptop Git clone,
  commit them through the normal Git workflow, and let the server pull. A shell
  runner may verify hashes and apply an already-retained patch if needed, but it
  should not be the primary carrier of authored text.

## Correction design

### A1–A3 — enforcement matrix

**Drafted response:** replace the single `Normative state` axis with three
separate facts:

1. `Governance status`: `proposed-v9` or `inherited-v4`.
2. `Claimed enforcement mode`: `none`, `manual`, or `machine`.
3. `Enforcement evidence`: `none`, a named retained artifact instance, or
   machine evidence.

This is a deliberate combined answer to A1–A3. It avoids falsely demoting an
admitted/inherited constraint merely because no current enforcement artifact
exists. It also makes a manual-practice claim explicitly different from evidence
that the check occurred.

The corrected matrix therefore:

- removes the undefined `adopted, not currently evidenced` state;
- removes `WARR-20260719-0002` as C3 evidence and states why it is not evidence;
- records C3, C6, C7, C9, C10 and C11 enforcement evidence as `none` rather than
  using artifact classes or unrelated records as evidence;
- retains current manual-practice claims as claims, not as evidence;
- requires a named artifact instance attesting the applicable check for a named
  target before manual enforcement becomes evidenced.

This differs from the literal A2 fallback "move the rows to proposed" because,
after A1 separates governance from enforcement, that fallback would falsely
state the governance status of C6/C7/C9/C10/C11. The proposal records the
alternative explicitly rather than taking it silently.

### A4 — P5 versus IndependenceAssessment

**Drafted response:** remove the compensating-control fall-through.

Any `unresolved` dimension yields overall `unresolved`. A compensating control
may be recorded as mitigation or may supply evidence used to reassess a
dimension, but its name or existence cannot upgrade independence. Qualification
may increase only after the governing rule for that dimension records evidence
that resolves the unknown to a non-`unresolved` result, after which the overall
status is derived again.

This chooses the strict branch of the authorized remedy. A control that merely
bounds risk while leaving the fact unknown does not convert the epistemic state.

### A5 — VerificationRun review conversion

**Drafted response:** split the record definition from the admission/status
consequence and make the latter a `[PROPOSED_CONSTRAINT]`.

A review artifact changes `verifier_lineage_status` to
`self_authored_with_review` only when it is linked to the exact VerificationRun
and establishes, for the reviewed property:

- reviewer invocation and executor identity;
- reviewer independence relative to the verifier and output under review, with
  no unresolved or disqualified independence dimension;
- coverage of verifier version, rule/test version, content-addressed inputs,
  execution environment and result;
- a positive review outcome.

Merely naming or linking an artifact performs no conversion.

### A6 — `[DEF]` carrying consequences

**Drafted response:** both prevention and repair.

1. The sentence-discipline legend now states that `[DEF]` may describe terms,
   shapes, relations or descriptive derivations, but may not itself impose an
   obligation, prohibition, permission, admission condition or status-changing
   consequence.
2. The Section 3 subordinate-authorization paragraph is retagged
   `[PROPOSED_CONSTRAINT]`.
3. Section 4.17 is split: the VerificationRun shape remains `[DEF]`; the
   admission/status consequence becomes `[PROPOSED_CONSTRAINT]` and is
   substantively corrected under A5.

The Section 3 paragraph is deliberately **not** retagged
`[INHERITED_CONSTRAINT]`. A6 itself establishes that its category in admitted v4
was wrong. Calling the newly classified occurrence inherited would use the
inheritance mechanism to settle the very classification question now under
correction. Admitted v4 is not edited; its historical text remains intact.

### A7 — byte identity versus semantic identity

**Drafted response:** two parts.

1. Add a `[LIMITATION]` stating that `[INHERITED_CONSTRAINT]` establishes
   textual continuity only; it does not establish semantic identity where
   definitions, vocabularies, relation rules or other referents changed.
2. Re-examine C3 in this correction. Because A8 changes C3 substantively, its
   v9 occurrence is retagged `[PROPOSED_CONSTRAINT]`; it is no longer presented
   as an inherited constraint.

This means the corrected candidate does not ask byte identity to carry a C3
semantic-equivalence claim it cannot support.

### A8 — unresolved executor equivalence

**Drafted response:** fail closed for adjudication.

When equivalence between the adjudicating executor and an executor in the
claim's evidence ancestry is unresolved:

- the invocation may not adjudicate that claim while the relation remains
  unresolved;
- the independence result remains `independence_unresolved`;
- unresolved is not treated as distinct for independence purposes;
- equivalence or non-equivalence must be affirmatively established under the
  applicable executor-kind identity semantics;
- a compensating control that leaves equivalence unresolved cannot license
  adjudication or increase independence.

This is the operational consequence adjudicated by A8 and is consistent with
the A4 rule that an unknown cannot be upgraded merely by naming mitigation.

## Intentionally not changed

- admitted v4;
- the v9/v10 version-number decision;
- C10's inherited normative sentence about existing compensating controls,
  because DECISION-20260811-0001 did not authorize a substantive C10 rewrite;
- the fifteen `gap or policy` ledger entries;
- the evidence-starved challenge questions themselves;
- GAP-0006 execution-profile limitations.

Those surfaces can be reviewed or governed separately; this proposal does not
silently absorb them into A1–A8.

## Verification performed on the proposal

- source repository HEAD independently verified as
  `4c29406bcf54f48510a8cec8ffeeb2beaa774535`;
- patch applies in a second clean checkout;
- `git diff --check` passes;
- `tests/test_abstraction.py`: 7 passed;
- full suite with import-only OpenAI/Anthropic SDK stubs outside the repository:
  726 passed;
- `scripts/audit_self_model_index.py`: `ok: true`,
  `verification_outcome: verified_current`;
- only `docs/abstractions/ABS-0004-invocation-authorization-ontology.md` is
  modified in the candidate checkout.

## Required next governance

The operator or packaging executor should verify this literal proposal against
`DECISION-20260811-0001` before any repository application. Each A1–A8 response
should be accepted, rejected, or replaced explicitly. The correction drafter
must not author the substantive review of the accepted corrected candidate.
