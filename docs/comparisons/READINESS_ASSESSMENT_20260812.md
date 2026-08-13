# Implementation-readiness assessment: the six manual-mode constraints

Produced by the packaging executor at commit
`d10fd20775e1b83177915055406fdbc74988b403`, after the reviewing executor
rejected the reconciliation's recommendation of C10 as cheapest-first.

**External deliverable for review. No record modified.**

The question: of C3, C6, C7, C9, C10 and C11 — each claiming manual enforcement
with evidence `none` — which is cheapest to turn into an evidenced check, and
what is the minimum honest artifact for each?

## Why the previous recommendation was wrong

The reconciliation proposed C10 on the reasoning that `VERIFY` records exist and
the gap might be one field away. The reviewing executor disagreed, and the
matrix row for C10 states the refutation in its own dependency column:

> `VerificationRun with verifier-ancestry check`

C10 depends on evidence ancestry, which does not exist. Adding a field asserting
the check passed would create the anti-pattern v9.1 removed a week ago in
corrections A2 and A5: a named field asserting a property without the evidence
that establishes it.

The information contradicting the guess was in the row being read.

## The four columns

| constraint | existing inputs | missing evidence | minimum honest artifact |
| --- | --- | --- | --- |
| **C7** implementation separation | **35 of 35 VERIFY records carry `recorded_by.peer_id` and `repo_commit`.** Two distinct verifier identities exist in the record: `claude`, `chatgpt` | the **implementer** identity for the change being verified. `git author` is the operator on every commit and does not name the drafting executor | a `verified_by` / `implemented_by` pair on a VERIFY record, both naming declared executor identities, plus the refusal condition when they match |
| **C11** interim independence disclosure | 3 of 12 DecisionRecords discuss independence in prose; `DRAFTING_EXECUTORS.json` declares three identities | a structured disclosure field on high-consequence decisions naming the witness paths relied on and their shared-source risk | a `witness_independence_disclosure` block on a DecisionRecord that claims a minimum number of independent paths |
| **C6** authority separation | **zero records** carry a typed authority field. `epistemic_authority`, `action_authority`, `accountable_authority` appear in no record | all three role axes, per invocation, plus the target | role assignment records, then a check that adjudicator-level epistemic and above-read-only action authority are not both exercised in one invocation against one target |
| **C9** lineage inheritance | **zero records** carry `claim_lineage_status` or `source_provenance_status` | both fields, on every artifact, plus a propagation rule across transformation | lineage fields on artifacts, then an inheritance check. The claim graph work of July is the nearest existing machinery |
| **C10** validator lineage | VERIFY records name verification activity | verifier executor reference, verifier version, rule/test version, content-addressed inputs, execution environment, `verifier_lineage_status`, **and the evidence ancestry to derive lineage** | a typed `VerificationRun` per §4.17, which requires ancestry capture first |
| **C3** no self-adjudication | `DRAFTING_EXECUTORS.json` declares identities; the corrected C3 states the fail-closed rule | per-kind equivalence resolution **and** lineage traversal over evidence ancestry | ancestry capture plus equivalence resolution. Two mechanisms, neither existing |

## Result

**C7 is the cheapest, and it is cheap for a structural reason rather than by
luck.** It is the only one of the six whose subject is *who did what*, and this
repository already records that on one side. Every VERIFY record names its
verifier. The missing half is the implementer.

It is also the only one where the check is a comparison of two recorded values
rather than a traversal, a propagation, or a resolution. C3, C9 and C10 each
need a mechanism that walks or infers across records. C6 and C9 need fields that
exist nowhere.

**C11 is second**, and is cheaper than it looks: the disclosure it requires is
something the externals already write in prose, in three of twelve decisions.
Structuring it does not require new evidence, only a place to put what is
already being said.

**C3 and C10 share a single blocker.** Both need evidence-ancestry capture. That
is the largest single unlock among the six, but it is a build rather than a
field.

## What this does not establish

- That C7's implementer field is easy to populate. Externals draft in
  conversation and produce no `InvocationRecord`; naming the implementer is a
  declaration, not a capture, and would carry the same unverified status as
  `DRAFTING_EXECUTORS.json`.
- That a C7 check would be meaningful with only two declared verifier
  identities. If `claude` verifies what `chatgpt` implemented and vice versa,
  the check passes trivially until a case arises where they match.
- That any of this is the right next build. It answers which constraint is
  cheapest, not whether cheapest is the right selection criterion.

## The observation worth separating out

Every one of the six is a check that external identities currently perform by
reading records and reasoning about them. None produces an `InvocationRecord`,
and none leaves an artifact the matrix can name.

C7 is the clearest case. The C7 check — did the party that implemented this
change also solely verify it — has in fact been performed continuously
throughout this project, by two external identities alternating drafting and
review. It has never once been recorded. The practice is real and the evidence
is absent, which is precisely what the matrix says.
