# ABS-0004 v9 reconstruction — Task 3 limitation proposal

## Snapshot and task boundary

- Source snapshot HEAD independently verified as `7b8b1dc708cacc1012b46ba8d6e5203ad703a765`.
- Git object verification completed without error in a clean clone.
- Self-model audit result: `ok: true`, `verification_outcome: verified_current`, with the two expected informational findings.
- Baseline for this proposal: the accepted Task 2 candidate at `docs/self_model/v9_reconstruction/ABS-0004-v9-task2-proposed-baseline.md`.
- Scope: revalidate and draft limitation statements only for V9L-004, V9L-010, V9L-013, V9L-018, V9L-021, V9L-024, V9L-025, and V9L-027; state a sentence-category proposal. No v9 assembly, ontology-file modification, schema implementation, review-question drafting, or resolution of `identity_verification_status` occurs here.
- V5-v8 text was not used as a remedy source. Later-round text was used only as evidence of the relevant finding and failed constructions.

## Revalidation result

All eight entries survive revalidation, but they do not all require new semantic content. Four are already stated substantively in admitted v4; Task 3 makes their boundary explicit or separates it under a limitation category rather than adding a new control.

| Entry | Revalidation against admitted v4 | Drafting consequence |
|---|---|---|
| `V9L-004` | **Established residual limitation.** V4 leaves bootstrap open and defines `AccountablePrincipal`, `authority_scope`, and delegation records, but does not state that repository records cannot establish extra-systemic entitlement. The later rounds establish that record-equivalent worlds can differ in actual entitlement. | Add an explicit limitation after the bootstrap `[OPEN]`; do not define a chain terminus or import v5-v8 standing-authority text. |
| `V9L-010` | **Established residual limitation.** V4 requires disclosure and graph representation but does not claim detection or completeness. Later complete-visibility claims failed because absent, unlinked, untraversable, or misattributed objects cannot be enumerated from the record. | Add an explicit record-completeness limitation; do not weaken the disclosure requirements themselves. |
| `V9L-013` | **Plausible but live only as a boundary.** V4 does not use `self-standing` and does not define a positive chain-termination status. The later terminology defect therefore does not reach v4 directly. The durable distinction is between where a represented chain stops and whether the act is substantively authorized. | State that distinction without introducing `self-standing` or any new termination mechanism. |
| `V9L-018` | **Established and already disclosed in v4.** The C6 enforcement-matrix row says `adopted, not currently evidenced` and names no current check artifact. COMP-0044 confirms that role and authorization records are dependency artifacts, not evidence that C6 was evaluated. | Add a nearby limitation sentence only to make the matrix distinction explicit at C6; no enforcement claim is added. |
| `V9L-021` | **Established and already stated in v4 §4.15.** V4 already says artifact-level lineage cannot distinguish mixed claim origins and supplies potential-dependence detection, not claim-level independence proof. | Preserve the wording and separate it under `[LIMITATION]`; no new semantic claim. |
| `V9L-024` | **Established and already stated across P2 and §4.13.** V4 confines verification to named properties and forbids admission from treating uncovered properties as established. The remaining risk is the consumer inferring a broader epistemic status from a narrow result. | Add a concise limitation summary; do not add a new verifier architecture or admission control. |
| `V9L-025` | **Established and already stated across P5 and C3.** V4 defines executor-kind-specific equivalence and says unresolved equivalence cannot increase independence. | Add a concise limitation summary; do not select an `ExecutorIdentity` inheritance design. |
| `V9L-027` | **Established only after the DECISION-20260727-0004 correction.** V4 defines `AuthorizationPolicy` and typed policy references. What remains is that definition and reference typing do not evidence activation, evaluation, or enforcement. | Add an explicit limitation after §4.16; do not duplicate the policy definition or import v8's self-issued clause. |

## Literal limitation text

The supplied patch adds exactly these eight statements to the accepted Task 2 candidate.

### V9L-004

> `[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and authorization records can state and attribute authority claims. Repository records do not by themselves establish a principal's extra-systemic entitlement to govern.

### V9L-010

> `[LIMITATION]` Record and relation requirements expose only what was declared, recorded, linked, traversable, and correctly attributed. They do not establish that every material invocation, authorization, input, dependency, or external interaction is present in the record.

### V9L-013

> `[LIMITATION]` A recorded authorization-chain terminus identifies where the represented chain stops. It does not by itself establish that the underlying invocation is substantively authorized.

### V9L-018

> `[LIMITATION]` Role, qualification, and authorization records are inputs to a C6 evaluation. Their existence does not establish that the C6 exercise restriction was evaluated or satisfied for a particular invocation.

### V9L-021

> `[LIMITATION]` One artifact may mix original observation, copied finding, new inference, and paraphrase; artifact-level lineage cannot distinguish them. Until claim-level derivation exists, the system provides artifact-level potential-dependence detection, not claim-level independence proof; Section 7 imposes the conservative inheritance this gap requires, and C11 imposes the interim high-consequence disclosure this gap requires.

This is admitted v4 text separated from the preceding `[DEF]`; the proposal changes its category, not its substance.

### V9L-024

> `[LIMITATION]` A verification result supports only the property it names. It does not by itself justify a broader epistemic status or establish truth, grounding, calibration, privacy, or any other unverified property.

### V9L-025

> `[LIMITATION]` Distinct identifiers, endpoints, or invocation records do not by themselves establish distinct executor identities. When executor-kind-specific equivalence cannot be resolved, independence remains unresolved.

### V9L-027

> `[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does not establish that a policy was active, applicable, evaluated, or enforced for a decision. AuthorizationPolicy enforcement remains deferred.

## Sentence-category proposal

### Proposed categories for a proposed v9

1. Introduce `[LIMITATION]`:

   > `[LIMITATION]` descriptive boundary on what the ontology, its records, or current enforcement establish. A limitation imposes no new constraint and claims no adoption.

2. Replace the seventeen inherited `[ADOPTED_CONSTRAINT]` tags at v9 assembly with `[INHERITED_CONSTRAINT]`, defined as:

   > `[INHERITED_CONSTRAINT]` constraint text carried forward unchanged from the admitted v4 baseline. Its current governance force derives from v4's admission, not from the proposed v9 document. A substantive change is tagged `[PROPOSED_CONSTRAINT]` until separately admitted.

### Reason

A proposed document cannot truthfully label its own statements “adopted now.” At the same time, simply relabeling unchanged v4 constraints as proposed would falsely erase their existing v4 admission history. `[INHERITED_CONSTRAINT]` preserves both facts: the constraint is already admitted through v4, while v9 itself remains proposed. `[LIMITATION]` is neither a constraint nor an adoption event; it records the boundary of what the ontology or its current implementation establishes.

The attached limitation candidate does **not** perform the seventeen-tag migration. It remains a Task 2-derived v4-form baseline used only to show the exact limitation insertions. The operator must adjudicate the category proposal before v9 assembly.

## Diff accounting

Against the accepted Task 2 candidate:

- new limitation statements: 8;
- `[LIMITATION]` occurrences: 9, including the sentence-discipline definition;
- `[ADOPTED_CONSTRAINT]` count: unchanged at 17;
- `[PROPOSED_CONSTRAINT]` count: unchanged at 9;
- Section 3 constraints or definitions changed: 0;
- Section 3 `[ADOPTED_CONSTRAINT]` count: remains 0;
- Section 3 limitation statements added: 3;
- ontology repository file modified: no.

## Not checked

- This task does not establish that adding all eight explicit statements is preferable to relying on v4's existing language for V9L-018, V9L-021, V9L-024, and V9L-025. It supplies literal text for operator adjudication; four are clarifying restatements rather than new findings.
- This task does not re-adjudicate the remaining twenty-one ledger entries or establish that the ledger is globally correct.
- This task does not resolve the accepted Task 2 text's omission of `identity_verification_status` or decide the implementation consequence recorded in DECISION-20260727-0004.
- This task does not decide whether inherited v4 constraints remain operative during the interval between v9 proposal and v9 admission; it only proposes a tag that reports their source of governance force.
- This task does not define, implement, or validate authorization-chain termination, entitlement verification, complete-record detection, C6 enforcement, claim-level lineage, evidence-admission enforcement, executor equivalence resolution, or AuthorizationPolicy enforcement.
- This task does not establish that v4 or the resulting candidate is correct. It states bounded limitations supported by the cited rounds and admitted baseline.

## Supplied artifacts

- `ABS-0004-v9-task3-baseline.md` — byte copy of the accepted Task 2 candidate.
- `ABS-0004-v9-task3-limitations-candidate.md` — baseline with the eight literal limitation statements and `[LIMITATION]` category definition.
- `ABS-0004-v9-task3-limitations.patch` — exact unified diff from the Task 2 candidate.
- `V9_TASK3_LIMITATIONS_PROPOSAL.md` — this revalidation and drafting record.
- `SHA256SUMS.txt` — content hashes for all supplied artifacts.
