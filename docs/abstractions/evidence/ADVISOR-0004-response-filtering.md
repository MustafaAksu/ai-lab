# ADVISOR-0004: Response filtering of a third-model reply (advisor document 4)

Snapshot provenance: attributed advisor artifact received by the operator and
relayed into the ABS-0004 drafting conversation on 2026-07-20. It evaluates a
third model's response (that response itself is not separately preserved;
its adopted content is quoted within this document). artifact_class: advisor.
epistemic_authority: advisor. provenance_status: pre_provenance. Executor
identity: reported claim only (not independently verified). Invocation
details: unrecorded. Information-path dependent on the v1 draft, the v1
adversarial review, and the third-model response it filters. This snapshot is
a normalized immutable text capture from the drafting conversation record.

---

Yes. It contains **two genuinely valuable new points**, one useful refinement, and several repetitions or technically incorrect claims.

## Genuinely new contributions

### 1. Hidden sub-invocations inside tools

The strongest new point is the possibility that a `ToolIdentity` classified as deterministic or operational may internally call an LLM and thereby exercise undeclared epistemic authority.

Example:

```text
test-runner invocation
    └── hidden LLM call judging "logical correctness"
```

The existing ABS distinguishes models, tools, and humans, but it does not yet require a composite tool to disclose subordinate executions. This is a real provenance loophole.

However, the proposed fix—requiring every actuator tool to be fully deterministic—is too restrictive. Nondeterministic actuators can be legitimate. The proper constraint is recursive disclosure:

> Every epistemically or operationally material subordinate execution must be represented as an Invocation and linked to its parent invocation. A tool that invokes a model cannot be represented as a purely deterministic ToolIdentity.

Suggested additions:

```text
invocation spawned invocation
invocation called invocation
tool_identity uses_executor executor_identity
```

And:

```text
[CONSTRAINT] An Invocation may not acquire authority by encapsulating
an undisclosed subordinate executor. Any subordinate model, tool, or
human execution capable of influencing the output or external effect
must be represented in the invocation graph.
```

This should be added to the ABS challenge findings.

---

### 2. Runtime configuration as a provenance dimension

The response correctly observes that model identity alone does not fully describe execution behavior. Parameters such as these matter:

* temperature;
* `top_p`;
* reasoning effort;
* seed, where supported;
* system and developer instructions;
* tool definitions;
* endpoint configuration;
* provider-side feature flags.

That is valuable, but creating an `InvocationRuntimeInstance` would probably duplicate the existing `Invocation` object. An Invocation is already the concrete execution event.

A cleaner addition would be an `ExecutionProfile` or `ExecutionEnvelope` referenced by the Invocation:

```text
Invocation
    executed_by ModelIdentity
    used_execution_profile ExecutionProfile
```

```text
ExecutionProfile
    service_endpoint
    sampling_parameters
    reasoning_parameters
    system_instruction_digest
    developer_instruction_digest
    tool_schema_digest
    provider_request_parameters
    runtime_version_information
```

This reinforces the `EffectiveInputManifest` issue identified in the earlier review.

The response's statement that changing temperature creates a different "executor" is too strong. It changes the execution configuration, not the executor identity.

---

## Useful but only partially new

### Provider-managed state as an independence hazard

The response adds useful emphasis to the Session problem, but the underlying concern was already present in:

* the ABS's restriction on unreconstructible provider-managed sessions;
* the earlier recommendation for an `EffectiveInputManifest`;
* the finding that shared session state can invalidate blindness.

Its specific treatment of prompt caching and KV caches is technically imprecise.

**Prompt caching does not necessarily introduce hidden semantic state.** In many implementations it is only an optimization for processing an explicitly supplied token prefix. The logical model input remains the same.

This must be distinguished from:

* provider-managed conversation threads;
* hidden conversation summaries;
* server-side memory;
* assistant state not fully returned to the caller;
* provider-controlled context truncation or rewriting.

The correct distinction is not "cached versus uncached." It is:

```text
Does unrecorded inherited state influence the logical execution input?
```

A better constraint would be:

> An invocation cannot qualify as a blind witness when provider-managed or hybrid state may contain unrecorded information relevant to the matter under review. Reconstructible provider-side state remains eligible when its effective contents and lineage can be demonstrated.

The demand for a "bit-level raw token history" is unnecessarily absolute. What AI-Lab needs is a sufficiently complete and canonical representation of effective inputs. Exact internal KV-cache values are implementation details and are neither available nor required for semantic provenance.

Also, `unknown_state` should **not** be removed. Ontologies must represent uncertainty honestly. Instead:

```text
unknown_state
    → independence_status: unresolved
    → blind_witness_eligible: false
```

Unknown facts should block qualification, not disappear from the vocabulary.

## Points already covered in the earlier review

### `AccountablePrincipal`

This is not new. The earlier critique already identified `AccountablePrincipal` as an undefined load-bearing object and proposed a privacy-preserving representation.

The new response adds cryptographic keys and multisignature governance, but those are implementation choices rather than ontology requirements.

This proposed definition is too narrow:

```text
substrate_type:
    human_operator | governance_multisig
```

An accountable principal might also be:

* a delegated organizational role;
* a governance committee;
* a pseudonymous operator identity;
* a service owner;
* another authorized legal or operational entity.

A better minimal definition remains:

```text
principal_id
principal_kind
authority_scope
delegation_reference
```

Cryptographic signing can be a later qualification or implementation mechanism.

### Pre-provenance laundering

The laundering path is essentially the same as the one already identified:

1. A legacy claim is summarized.
2. The summary has fresh production provenance.
3. Another model evaluates the summary.
4. The inherited claim appears newly corroborated.

The earlier critique expressed the core rule:

> Complete production provenance does not imply complete claim provenance.

The new response is corroborating that finding rather than adding a distinct one.

### `derived_from` ambiguity

The earlier review already identified `derived_from` as ambiguous.

The suggestion to rename it `transformed_from` is useful for one specific relation:

```text
output structurally transformed_from input
```

But it does not replace all the semantics currently being overloaded. AI-Lab will likely need separate predicates:

```text
transformed_from       # mechanical or structural transformation
claim_derived_from     # epistemic or inferential dependence
continued_from         # execution/session continuity
copied_from            # direct content inheritance
summarized_from        # lossy representational transformation
```

The response also criticizes overlap between `derived_from` and `based_on`, but **`based_on` does not appear in the submitted ABS predicate vocabulary**. That part of the critique appears to address an invented predicate.

## Incorrect or dangerous recommendations

### "All actuator tools must be deterministic"

This is unnecessarily restrictive and does not solve the real problem.

A deployment controller, network client, optimizer, or distributed test harness may have nondeterministic behavior without exercising epistemic authority.

The relevant questions are:

* Did it make an epistemic judgment?
* Did it assign governed status?
* Did it call another executor?
* Are subordinate executions recorded?
* Are external effects traceable?

The constraint should target **undeclared authority and hidden composition**, not nondeterminism itself.

---

### "Higher than witness" session restriction

The proposed rule prohibits provider-managed state only for authorities higher than witness. That is backwards in one important respect.

Blind witnesses are precisely where hidden prior state most directly compromises claims of independent corroboration. Witness invocations require at least as much state isolation as adjudicators.

The restriction should depend on protocol and independence requirements:

```text
blind witness:
    must have reconstructible, isolated effective inputs

adjudicator:
    must have reconstructible evidence ancestry and no prohibited lineage

advisor:
    may use broader state, but inherited context must be disclosed

actuator:
    state constraints depend on operational authorization and auditability
```

There is no reliable linear authority ordering in which witness is simply "below" advisor and adjudicator for every constraint.

---

### The proposed pre-provenance exception for extraction

The response suggests rejecting pre-provenance inputs unless the task is `extract`.

That exception is dangerous because extraction is exactly the first step in the laundering path it identifies.

Extraction should be allowed, but the output must inherit the source limitation:

```text
extracted claim
    source_lineage_status: pre_provenance
    independent_observation: false
```

A structural transformation cannot improve the provenance class of the information transformed.

---

### `relied_on` and `used_context` as additions

This is not new. Both already appear among the eight minimal predicates in Section 4, and Section 9 explicitly explains why `used_context` belongs in the first candidate slice.

More importantly, merely adding these relations does not prevent laundering unless:

* their target manifests are complete;
* inherited claim ancestry is preserved;
* unknown lineage propagates conservatively.

---

### "Sentence discipline is flawless"

This misses one of the draft's clearest contradictions.

The ABS defines `[CONSTRAINT]` as adopted, while the enforcement matrix classifies several `[CONSTRAINT]` statements as merely `proposed`. It also uses `[COMMIT]` for a future implementation slice before GAP and plan admission.

Therefore, the sentence discipline is valuable but not flawless. The vocabulary needs at least:

```text
[PRINCIPLE]
[PROPOSED_CONSTRAINT]
[ADOPTED_CONSTRAINT]
[COMMIT]
```

## What should be carried into the ABS review

I would retain these two findings from this response:

### New finding A — Composite-executor disclosure

> Tools and agents may encapsulate subordinate model, tool, or human executions. Every material subordinate execution must be represented recursively as an Invocation; authority cannot be acquired through an opaque wrapper.

### New finding B — Execution configuration provenance

> ModelIdentity does not fully characterize an execution. Invocation provenance must include or reference an ExecutionProfile covering endpoint, parameters, instruction envelopes, tools, and runtime configuration.

And refine the Session contribution as:

### Refined finding C — Logical-state reconstructibility

> Caching alone is not evidence of hidden semantic state. Independence eligibility depends on whether all logically influential inherited state is represented, reconstructible, and lineage-accounted.

## Net assessment

The response contains **two meaningful additions**, but it should not be accepted wholesale:

| Point                                  | Assessment                                    |
| -------------------------------------- | --------------------------------------------- |
| Hidden sub-invocations inside tools    | **New and important**                         |
| Runtime parameters/configuration       | **New framing; useful**                       |
| Provider-managed session contamination | Partly new emphasis; technically overstated   |
| AccountablePrincipal                   | Already identified                            |
| Pre-provenance laundering              | Already identified                            |
| `derived_from` ambiguity               | Already identified                            |
| `based_on` overlap                     | Based on a predicate absent from the ABS      |
| Deterministic-actuator requirement     | Too broad                                     |
| Remove `unknown_state`                 | Wrong; uncertainty must remain representable  |
| Extraction exception                   | Creates the laundering route it warns against |
| Add `relied_on`/`used_context`         | Already present                               |
| "Sentence discipline flawless"         | Incorrect                                     |

The next review revision should add **composite invocation provenance** and an **ExecutionProfile**, but should reject the response's blanket determinism rule, its prompt-cache claim, and its extraction exception.
