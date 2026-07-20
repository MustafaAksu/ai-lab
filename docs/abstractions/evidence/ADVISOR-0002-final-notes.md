# ADVISOR-0002: Final notes before ABS-0004 drafting (advisor document 2)

Snapshot provenance: attributed advisor artifact received by the operator and
relayed into the ABS-0004 drafting conversation on 2026-07-19/20.
artifact_class: advisor. epistemic_authority: advisor. provenance_status:
pre_provenance. Executor identity: reported claim only (not independently
verified). Invocation details: unrecorded. This snapshot is a normalized
immutable text capture from the drafting conversation record.

---

Yes—start ABS-0004. The six amendments are strong and should be incorporated. I would add the following guardrails before freezing the draft.

## 1. `pre_provenance` must not mean blanket admissibility

Retroactivity needs two separate questions:

* **Historical standing:** Was the artifact validly used under the governance process that existed when it was created?
* **Prospective evidentiary use:** May it be reused as evidence in a new governed decision?

Existing GAP-0003 and GAP-0004 records should retain their historical standing. However, a `pre_provenance` artifact should not automatically qualify as fully independent evidence for a future high-consequence adjudication.

A better rule would be:

> Pre-provenance artifacts retain their historical governance status. When reused in later governed decisions, their missing provenance must be disclosed and may trigger corroboration, reduced independence weight, or exclusion depending on the receiving role and consequence class.

Otherwise the phase-in rule could become a permanent grandfathering loophole.

Possible statuses:

```text
provenance_complete
provenance_partial
pre_provenance
provenance_conflicted
```

These describe provenance condition, not whether the underlying claim is true.

## 2. Separate executor identity from accountable authority

Invocation should not be defined as "an LLM call." It is an event performed by an executor:

```text
Invocation
  executor_identity
  task_function
  epistemic_authority
  inputs
  outputs
  execution_context
  occurred_at
```

Executor identities may include:

* `ModelIdentity`
* `ToolIdentity`
* `HumanIdentity`

But an additional distinction is necessary: **the executor of a decision may not be the accountable authority for that decision**.

For example:

```text
model invocation produced warrant recommendation
human decision invocation admitted warrant
deterministic validator verified schema compliance
```

These should not collapse into one `produced_by` relation.

Useful distinctions would be:

```text
artifact produced_by invocation
decision issued_by invocation
decision approved_by accountable_principal
invocation executed_by executor_identity
invocation verified_by invocation
```

This prevents a model-generated warrant from appearing human-approved merely because a human copied it into the repository. It also prevents a human pressing "run" from appearing to have authored the deterministic test result.

The ABS should therefore leave open whether a generic `ExecutorIdentity` is needed as a superclass, while still defining ModelIdentity, ToolIdentity, and HumanIdentity distinctly enough to preserve their different verification requirements.

## 3. Provider claims are not model qualification evidence

`CatalogAssertion` establishes claims such as:

* an API name exists;
* it resolves to a particular model identity;
* it supports a context length or tool;
* it has particular pricing;
* it was available at an observed time.

It does **not** establish that the model is suitable for an AI-Lab role.

That requires local or independently admitted evaluation evidence.

The ontology should therefore distinguish:

```text
CatalogAssertion:
    What the provider or authoritative catalog claims.

EvaluationOutcome:
    What AI-Lab or an admitted evaluator observed.

RoleQualification:
    The policy conclusion that the identity is eligible for a role.
```

A routing policy may rely on a verified catalog assertion for technical eligibility, but adjudication suitability should require relevant evaluation evidence.

For example:

```text
CatalogAssertion:
    model supports structured output

EvaluationOutcome:
    model produced schema-valid outputs in 99/100 trials

RoleQualification:
    eligible for sidecar generation under policy version P
```

This prevents provider marketing claims from becoming operational authority.

## 4. Refine the Session conclusion

Session belongs in the ontology now, but the ABS should not assert that every multi-turn API mechanism necessarily contains unknowable hidden context. What matters is whether prior state can influence the invocation and whether AI-Lab can reconstruct that state.

I would define Session as:

> A continuity boundary through which one invocation may inherit state that is not represented solely by its immediate explicit prompt.

Useful state modes:

```text
stateless
explicit_replayed_context
provider_managed_state
local_managed_state
hybrid_state
unknown_state
```

An invocation should record, where applicable:

```text
member_of session
continued_from invocation
session_state_mode
session_state_reference
session_state_reconstructibility
```

A provider-managed session may be admissible for ordinary interactive generation but inappropriate for blind witness work if its inherited state cannot be reconstructed or shown independent.

This connects Session directly to the independence rules rather than treating it merely as conversation grouping.

## Consequence classes

I agree with your concern but would not derive consequence exclusively from target type. Target type is a good default, yet consequence can also depend on authority, reversibility, and external effect.

For example, "comparison" is usually medium consequence, but a comparison that automatically selects and deploys code becomes high consequence.

The first version can remain simple:

```text
default_consequence = consequence_by_target_type
effective_consequence = default_consequence + explicit modifiers
```

Possible modifiers:

* repository mutation;
* external side effect;
* irreversible or difficult-to-reverse action;
* gap closure or plan admission;
* capability or warrant status change;
* security, privacy, legal, or financial impact.

Every override should require a recorded reason. The detailed scoring function can remain an open question.

## Enforcement matrix

Your enforcement-locus amendment should become a mandatory table for every normative constraint:

| Constraint              | Representable now | Enforceable now | Enforcement mechanism         | Failure behavior                    | Required slice |
| ----------------------- | ----------------- | --------------- | ----------------------------- | ----------------------------------- | -------------- |
| Catalog admission       | No                | No              | Future validator/runtime gate | Warn until slice; reject afterward  | Slice 1        |
| No self-adjudication    | Partially         | No              | Lineage traversal             | Manual review                       | Slice 2        |
| Authority separation    | Partially         | Partially       | Artifact validator            | Reject invalid authority assignment | Slice 2        |
| No hidden witness reuse | No                | No              | Context-lineage inspection    | Mark independence unresolved        | Slice 3        |

I would add two columns:

* **Normative status:** proposed, adopted-but-manual, machine-enforced.
* **Enforcement evidence:** test, audit output, validator result, or human attestation.

This prevents "implemented in prose" from being mistaken for "operationally enforced."

## Minimal core versus complete ontology

Your scope boundary is right.

### Defined and implemented first

* `ModelIdentity`
* `CatalogAssertion`
* `Invocation`
* `Session`, at least enough to identify state continuity
* executor identity reference
* minimal provenance predicates

Minimal relations:

```text
artifact produced_by invocation
invocation executed_by executor_identity
invocation executed_with model_identity
invocation member_of session
catalog_assertion asserted_by provider
catalog_assertion describes model_identity
invocation relied_on catalog_assertion
```

I would include `used_context` if ContextManifest already exists operationally. Without it, the first provenance slice cannot later answer whether one witness saw another witness's output.

### Defined but deferred

* `RoleDefinition`
* `RoutingPolicy`
* `RoutingDecision`
* formal independence scoring
* automatic consequence assignment
* full ancestry enforcement
* provider-diversity thresholds

Role should still be fully designed in ABS-0004 even if enforcement comes later, because Invocation needs a stable place to attach future role assignments.

## Treatment of the advisor document

It should enter as attributed evidence, but the ontology should be applied honestly rather than retroactively fabricating unavailable fields.

Record what is actually known:

```text
artifact_class: advisor
task_function: evaluate / propose
epistemic_authority: advisor
provenance_status: partial or pre_provenance
provider/model identity: only if independently established
invocation details: unknown where not recorded
```

A digest or immutable transcript excerpt should accompany the summary so later synthesis cannot silently alter what the advisor actually proposed.

## Recommended ABS-0004 structure

1. **Anchoring thesis**

   > AI-Lab does not primarily route prompts to models. It authorizes invocations for roles under evidence, provenance, independence, consequence, and execution constraints.

2. **Scope and non-goals**

   Ontology and governance semantics now; provider selection and routing implementation later.

3. **Object definitions**

   Provider, ModelIdentity, CatalogAssertion, executor identities, RoleDefinition, Invocation, Session, RoutingPolicy, RoutingDecision.

4. **Canonical relations**

   All represented through `GraphRelation`; no parallel edge vocabulary.

5. **Epistemic constraints**

   Provenance completeness, catalog admission, self-adjudication prohibition, information-path dependence, authority separation, implementation separation, and decision traceability.

6. **Legacy and phase-in rules**

   Historical standing versus prospective evidentiary admissibility.

7. **Enforcement matrix**

   Representation, current enforcement, future enforcement, failure behavior, and evidence.

8. **Minimal enforceable core**

   Explicit first-slice boundary.

9. **Defined-but-deferred objects and behavior**

10. **Open questions**

Consequence classification, independence weighting, qualifying witness-path thresholds, Session state semantics, human accountability representation, and local model qualification.

11. **Challenge-round questions**

The draft should proceed now. The key drafting discipline is to make every sentence visibly one of four things: **definition, adopted constraint, implementation commitment, or open question**. That will prevent ontology decisions from being confused with capabilities AI-Lab does not yet possess.
