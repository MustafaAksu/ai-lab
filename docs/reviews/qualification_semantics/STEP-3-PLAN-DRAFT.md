# Step 3 PLAN draft — qualification semantics, r1

[ALG] **PLAN-20261125-0001: proposed. Implementation admission has not been
granted.** This submission follows the user's STEP_2_COMPLETE /
STEP_3_PREPARATION_PASS review. The authorization is to prepare the PLAN and
evidence-contract proposal.

Baseline: **5515f55894b10ad70c321340257f67a960dcc382**. Drafting executor: ChatGPT;
assisting analyses are from the same provider and do not supply independent
adjudication. The [canonical proposed PLAN](../../self_model/plans/PLAN-20261125-0001.json)
is the indexed record; this document is its review map.

## 1. Problem and intended result

Current equivalence support resolves only model/model comparisons and returns
the first successful catalog resolution. It checks endpoint presence without
binding that endpoint to the selected snapshot. Relevant contradicted or
ambiguous evidence can be skipped; evidence order can change both identity and
the helper's Boolean gate. Tool/tool and human/human tests are defined by C3
but lack implemented binding contracts.

The requested next slice makes identity relations evidence-scoped and
order-independent while keeping qualification and authority separate:

    non-equivalence does not entail independence
    independence does not entail authorization

[NUM] The retained [baseline evidence](SOURCE-REVIEW-BASELINE.md) now includes
executed synthetic R13/R14 counterexamples against unchanged baseline code.
These strengthen the source findings; they do not close the defects or prove
the proposed replacement. The model catalog evidence vocabulary remains
model-specific.

## 2. Deliverables and prospective scope

The detailed candidate semantics are in
[EQUIVALENCE-EVIDENCE-CONTRACT-DRAFT.md](EQUIVALENCE-EVIDENCE-CONTRACT-DRAFT.md).
All implementation below is **prospective and requires separate admission**.

| Scope | Planned deliverable after the applicable gate | Boundary |
| --- | --- | --- |
| S1 | Versioned kind-specific evidence/result contracts, references, applicability rules and compatibility strategy | Proposed external annotations; preserve captured InvocationRecord and existing resolution bytes |
| S2 | Tool binding validation and same-kind relation using canonical tool identity + version | Identity binding is distinct from execution disclosure and lineage |
| S3 | Human principal/reference binding, event-actor binding and same-kind relation | Names, accounts, keys and roles are insufficient by themselves |
| S4 | Endpoint binding and model multi-source aggregation; R13/R14 and existing order dependence | All relevant targets/conflicts retained; no ranking, first-success or newest-source rule |
| S5 | Reasoned cross-kind semantic proposal | Recommend unresolved in both orders; no new resolving rule installed |
| S6 | Superclass necessity assessment and explicit deferral | No ExecutorIdentity hierarchy introduced without demonstrated need |
| S7 | Executable C3/C10 input conditions and refusal checks | No ancestry traversal implementation or positive live qualification with GAP-0008 incomplete |
| S8 | Negative/positive controls, permutation tests, falsification, scoped verification and review | Tests establish only their named properties; later completion remains a PI decision |

Likely future implementation surfaces are the catalog resolver, executor
equivalence helper, separate binding/assessment modules and their tests.
The exact record names, public signatures and any compatibility adapter must be
frozen by review. A changed enum, new producer-kind semantics or a normative
ontology amendment cannot enter as an incidental refactor.

### Current submission

This PR contains the proposed PLAN, this review map, the proposed evidence
contract, expanded falsifier matrix, source-baseline artifacts and regenerated
SELF_MODEL. The retained probe script is an offline research reproduction; it
does not install an alternative resolver or enter the runtime/test workflow.

The accepted [STEP-3-PREPARATION.md](STEP-3-PREPARATION.md) remains unchanged as
the prior preparation artifact. Its statement that no canonical PLAN existed
describes that earlier state; this proposed record is the next preparation
revision. Step 2's completed PLAN and warrant remain historical authorities for
their own S1–S9 scope.

## 3. Required design choices

[ALG] The contract's D1–D8 table identifies the choices that require review:

- D1: bind invocation spelling to a retained endpoint identity under event-time
  evidence; do not compare a spelling directly with an EID or infer binding from
  the model originator.
- D2–D3: classify applicability first; require agreement among all applicable
  targets; retain relevant contradictions/ambiguity/unknowns; keep support sets
  and exact corroboration witnesses without an evidence-class ranking.
- D4–D5: define separate tool/version and human/principal/event binding rules,
  namespace/alias/distinctness conditions and limits of any enabled profile.
- D6–D7: retain unresolved cross-kind relations and defer the superclass, with
  the alternatives and their rejected assumptions documented.
- D8: specify typed invalid-input outcomes, append-only compatibility and the
  narrow identity-gate adapter; keep C3/C10 condition results separate from
  independence and authorization.

The inspected repository retains **218 model invocations and no tool/human
invocations**. An implementation can be evaluated with synthetic tool/human
fixtures without claiming real-world bindings. Live positive support remains
unavailable until the particular binding path and its evidence are admitted;
record validation alone cannot provide it.

## 4. Structural dependencies and exclusions

| Dependency | What this slice can prepare/implement after admission | What remains unavailable |
| --- | --- | --- |
| GAP-0005 | Kind-specific identity relation and evidence contracts | Complete implementer/verifier identity separation, writer–PI resolution and authority activation |
| GAP-0008 | Explicit ancestry/coverage inputs and refusal on missing evidence | Composable live ancestry and positive qualification depending on absent coverage |
| GAP-0010 | Reuse property-scoped observed-execution evidence | Required exact-candidate merge enforcement |
| ABS-0004 C5 | Preserve per-dimension findings as separate requirements | Deriving overall independence from identity inequality |
| ABS-0004 C10 | Exact-run/property and lineage/refusal conditions | Automatic lineage promotion; a silent expansion of producer semantics beyond ModelIdentity |

Excluded: principal enrollment or a new identity registry; acquiring new live
third-party corroboration; changing current captures' evidence classes;
IdentityVerificationStatus upgrades; ontology or consequence reclassification;
authority-policy machinery; branch protections; autonomous warrants, merge,
adjudication or bootstrap activation. The current review does not close any GAP.

Full tool configuration/subordinate/external-interaction disclosure remains
necessary where §4.7 applies. Its absence blocks the appropriate standing
claim; it does not manufacture a new identity or necessarily erase an otherwise
established identity/version relation.

## 5. Verification plan and success criteria

The [matrix](FALSIFICATION-MATRIX.md) preserves the original 13 scenario families
and adds 18 families covering endpoint binding, relevant conflict handling,
timing, malformed inputs, duplicates and assessment history: **31 planned
families**, not 31 completed tests.

For a future admitted implementation:

1. Freeze the selected D1–D8 semantics, exact record shapes and fixture oracles.
2. Preserve the existing defect demonstrations. For each changed guard, retain
   its baseline counterexample and expected corrected result.
3. Verify argument symmetry, evidence permutation invariance, duplicate
   idempotence and stable reason/provenance output.
4. Include both relevant-adverse cases and proven-irrelevant negative controls.
   A solution that blocks every source is insufficient.
5. Verify tool/version and principal/event binding separately from disclosure,
   independence and authority; reject any model-class shortcut for tool/human.
6. Check capture/resolution/VERIFY immutability and compatibility with existing
   catalog records and append-only consumers.
7. Run targeted and integration tests with exact subject and output retention.
   Any mutation score must first establish a passing baseline and then identify
   the intended test's actual assertion failure; collection, usage, internal
   errors and timeout do not count as caught.
8. Obtain the separately required technical review and PI decision for the
   implemented revision. Preserve actual executor/lineage limits.

Passing these checks is evidence about the implementation's named contracts.
It does not by itself admit a plan, close GAP-0008 or establish a live
C3/C5/C10 qualification.

## 6. Sequencing, stopping conditions and rollback

[ALG] Proposed sequence:

1. Review this exact proposal and resolve or explicitly bound D1–D8.
2. If the PI later admits an implementation slice, record its exact revision,
   scope, conditions and time in a separate warrant.
3. Implement only that admitted scope; collect baseline and corrected evidence.
4. Review the resulting implementation and request its separate completion
   decision with preserved limitations.

Stop implementation admission if principal semantics, endpoint applicability,
conflict treatment or the result/permission boundary remains insufficiently
specified. A narrowed fixture-only profile can be proposed explicitly; lack of
live evidence must remain visible rather than replaced by assumed truth.

If a future implementation increases standing on unresolved evidence or loses
relevant adverse input, stop reliance and restore the previous runtime behavior
through a reviewable revert. Preserve the faulty result, correction and review
history; do not delete evidence or retroactively relabel earlier runs.

[OPEN] Current program: scope records COMPLETE; observed execution COMPLETE;
qualification semantics PREPARATION/proposed PLAN; authority mechanism PENDING;
bootstrap activation PENDING. The next decision is review of this proposal,
**not implementation admission already granted**.
