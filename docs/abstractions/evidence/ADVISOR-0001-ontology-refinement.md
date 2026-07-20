# ADVISOR-0001: Ontology refinement (advisor document 1)

Snapshot provenance: attributed advisor artifact received by the operator and
relayed into the ABS-0004 drafting conversation on 2026-07-19/20.
artifact_class: advisor. epistemic_authority: advisor. provenance_status:
pre_provenance. Executor identity: reported claim only (not independently
verified). Invocation details: unrecorded. This snapshot is a normalized
immutable text capture from the drafting conversation record.

---

I agree with the central argument: **GAP-0005 should not define routing before AI-Lab can represent what is being routed, what produced an artifact, and whether an adjudicator is independent of the evidence.**

I would refine the proposal in four places before drafting ABS-0004.

## 1. Separate model identity from catalog claims

The proposed `Model` object currently mixes two different things:

* the identity of a model;
* the provider's current claim that a particular API name refers to that model and supports particular capabilities.

Those should not be the same object, because catalog information is mutable while provenance must remain stable.

A stronger decomposition would be:

### Provider

The organizational or administrative authority exposing a service.

Examples:

* OpenAI
* Anthropic
* Google

Stable fields might include:

* `provider_id`
* canonical name
* governance jurisdiction
* documentation authority

I would **not** put credentials or current availability into the Provider object. Credentials belong in protected runtime configuration, while availability is observed state.

### Model identity or Model release

The model identity used for provenance.

Possible fields:

* `model_id`
* `provider_id`
* canonical model name
* release/version identity, where verifiable
* identity verification status
* deprecation status

The key requirement is that an invocation must point to the most precise identity AI-Lab could establish at execution time.

### Catalog assertion

A time-bounded claim that an API identifier resolves to a model with certain properties.

For example:

```text
provider OpenAI asserts at time T:
API model name X exists,
maps to identity Y,
supports capabilities C,
and has pricing P.
```

This is where fields such as these belong:

* `api_model_name`
* `observed_at`
* `source`
* `verification_status`
* `valid_from`
* `valid_until` or superseded status
* supported modalities
* supported tools
* context limits
* pricing
* region or endpoint restrictions

This would handle the Sol-document problem correctly. The document did not necessarily describe nonexistent conceptual models; it made **catalog assertions that could not be independently verified**. That status should attach to the assertion, not contaminate the abstract Model object.

It also solves mutable aliases. An invocation that used an alias should preserve both:

```text
requested_model_name
resolved_model_identity
catalog_snapshot
```

when resolution is known.

## 2. Role should probably have two axes

I agree that `Role` is likely the most important discussion point.

The current list mixes operational activities and epistemic authority:

* `extract`
* `generate`
* `compare`
* `synthesize`
* `adjudicate`
* `implement`

These are not all the same kind of thing. `Extract` and `implement` describe work performed; `adjudicate` describes the authority of the result.

I would model Role as a composition of two dimensions.

### Task function

What the invocation does:

* extract
* classify
* retrieve
* generate
* compare
* synthesize
* evaluate
* plan
* implement
* verify

### Epistemic authority

What status its output is permitted to have:

* **witness** — contributes observations or candidate findings;
* **advisor** — interprets evidence or recommends action;
* **adjudicator** — may assign an accepted/rejected/disputed status;
* **actuator** — may change an external or repository state.

This distinction prevents subtle authority leakage.

For example:

| Invocation           | Task function | Authority   |
| -------------------- | ------------- | ----------- |
| Sidecar generator    | generate      | witness     |
| Comparison model     | compare       | advisor     |
| Final warrant review | evaluate      | adjudicator |
| Coding agent         | implement     | actuator    |
| Test runner          | verify        | witness     |

A synthesis model should not become an adjudicator merely because it produced polished prose. Likewise, an implementation model may modify code but should not be allowed to decide that its implementation is epistemically correct.

A Role definition can then carry constraints such as:

```text
allowed_input_classes
allowed_output_classes
required_independence
minimum_catalog_status
maximum_consequence_class
tool_permissions
may_assign_epistemic_status
may_mutate_repository
requires_external_verification
```

This is stronger than assigning a simple label such as `adjudicate`.

## 3. Independence must be lineage-based, not provider-count-based

The most important epistemic refinement is that **provider diversity is only a proxy for independence**.

Two outputs from different providers are not independent when:

* one model was shown the other model's output;
* both were given a synthesis that already incorporated one witness;
* both rely on the same unverified source;
* one invocation's context contains artifacts descended from the other;
* a comparison prompt reveals the expected conclusion;
* both outputs inherit the same mistaken finding code or framing.

Conversely, two models from the same provider may provide some useful diversity, although they should generally receive less independence weight than genuinely isolated witnesses.

I would define several levels.

### Direct lineage conflict

The adjudicating invocation produced the evidence itself, or the evidence descends from one of its earlier outputs.

This should be a **hard prohibition**.

### Model-identity conflict

The adjudicator uses the same model identity as an invocation in the evidence ancestry.

This appears to be the existing rule:

> No model adjudicates a matter where its own prior output is evidence.

Also a hard prohibition, unless AI-Lab later defines an explicit exceptional procedure.

### Provider correlation

The adjudicator and witness use different models from the same provider.

This is not necessarily a prohibition, but should reduce independence weight.

### Information-path dependence

A nominally independent witness consumed another witness's testimony.

This witness must not count as an independent confirmation of that testimony. It may still count as a synthesis or critique.

### Shared-source dependence

Two witnesses rely on the same underlying source set.

Agreement is still meaningful, but it is evidence of consistent interpretation rather than independent factual corroboration.

Therefore, the third-provider rule should not be:

```text
adjudication requires three providers
```

It should look more like:

```text
high-consequence adjudication requires a minimum number
of qualifying witness paths whose provenance is sufficiently independent.
```

Provider diversity would contribute to the independence score, but would not define it.

This also means the system should distinguish:

* **blind witness rounds**, where witnesses do not see one another's outputs;
* **comparison rounds**, where differences are intentionally exposed;
* **synthesis rounds**, where prior testimony is intentionally combined;
* **adjudication rounds**, where only admissible evidence is evaluated.

Only the first category provides strong independent corroboration.

## 4. Escalation policy and routing decision should be separate

An escalation policy is a durable rule. The actual choice made for a particular invocation is an event.

I would therefore define:

### Routing or escalation policy

A versioned policy artifact specifying:

* eligible roles;
* candidate qualification requirements;
* escalation triggers;
* independence requirements;
* cost or latency boundaries;
* fallback behavior;
* consequence classes;
* catalog freshness requirements.

### Routing decision

The event-level record explaining why a particular model was selected.

For example:

```text
requested_role: adjudicator
consequence_class: high
initial_candidate: model-A
candidate_rejected_because:
  - prior output present in evidence ancestry
selected_candidate: model-C
policy_version: POLICY-...
catalog_snapshot: CATALOG-...
```

Without this object, AI-Lab can know which model ran but not whether the routing policy was correctly applied.

I would also avoid making "tier" an intrinsic property of a model. `frontier`, `balanced`, and `cheap` are local, time-sensitive classifications. They should be policy-defined qualification labels derived from current evidence, not permanent model attributes.

## Suggested minimum ontology

To avoid excessive expansion, I would propose these seven core concepts:

1. **Provider**
2. **ModelIdentity**
3. **CatalogAssertion**
4. **RoleDefinition**
5. **Invocation**
6. **RoutingPolicy**
7. **RoutingDecision**

Existing artifacts can continue to represent:

* prompts;
* context manifests;
* outputs;
* comparisons;
* warrants;
* evaluations;
* capability records.

A separate `Session` object should be added only if sessions have semantics beyond grouping invocations—for example persistent provider state, accumulated hidden context, or replay boundaries. If provider-side session state can influence output, then Session becomes provenance-critical and should be included now rather than deferred.

## Relation vocabulary

Reusing `GraphRelation` is correct, but I would use predicates with narrow semantics:

```text
artifact produced_by invocation
invocation executed_with model_identity
invocation requested_catalog_entry catalog_assertion
invocation assigned_role role_definition
invocation used_context context_manifest
invocation used_prompt prompt_artifact
invocation member_of session
invocation derived_from invocation
routing_decision applied_policy routing_policy
routing_decision selected_model model_identity
routing_decision governed invocation
decision_artifact evaluates claim_or_artifact
decision_artifact issued_by invocation
catalog_assertion asserted_by provider
catalog_assertion describes model_identity
```

I would reconsider:

```text
invocation adjudicated warrant
```

because it conflates the process with the resulting judgment. A better chain is:

```text
decision artifact issued_by invocation
decision artifact evaluates warrant
decision artifact assigns_status accepted/rejected/disputed
```

That makes the adjudication itself inspectable and versionable.

## Core constraints for ABS-0004

I would put these near the center of the design note.

### Provenance completeness

No governed output is admissible unless it links to an invocation, model identity or unresolved model claim, role, prompt version, and context manifest.

### Catalog admission

A model may be used in a governed role only when its required catalog claims satisfy the role's verification and freshness requirements.

Unverified models may still be used experimentally, but their outputs cannot silently enter governed evidence.

### No self-adjudication

An invocation cannot adjudicate a claim when the evidence ancestry contains an invocation executed with the same model identity.

### No hidden witness reuse

An invocation that consumed another witness's output cannot be counted as an independent confirmation of that witness.

### Authority separation

Generation, synthesis, implementation, and adjudication authority are distinct. Producing an artifact does not grant authority to accept it.

### Decision traceability

Every policy-selected invocation must have a reconstructible routing decision or a documented manual override.

### Implementation separation

An actuator may implement an admitted plan but may not be the sole verifier or adjudicator of its own changes.

## Revised sequence

Your proposed sequence is right. I would slightly sharpen the deliverables:

1. **ABS-0004 ontology note**

   * object definitions;
   * distinction between model identity and catalog assertion;
   * two-axis role model;
   * canonical predicates;
   * provenance and independence constraints;
   * open questions explicitly marked.

2. **Ontology challenge round**

   * ask providers to identify missing objects, category errors, and unenforceable constraints;
   * do not yet ask them to recommend their own model products.

3. **GAP-0005**

   * express the operational deficiency against the accepted ontology;
   * define what cannot currently be represented or enforced.

4. **Provider comparison**

   * live catalog evidence is admitted separately from architectural reasoning;
   * blind witness responses first;
   * synthesis only after witnesses are frozen;
   * adjudicator selected through lineage checks.

5. **Implementation slices**

   * catalog assertion and invocation provenance;
   * roles and authority constraints;
   * routing decisions;
   * escalation;
   * session semantics, if required.

The strongest conceptual change I would make is this:

> **AI-Lab should not primarily route prompts to models. It should authorize invocations for roles under evidence, provenance, independence, and consequence constraints.**

Routing then becomes a consequence of the ontology and epistemic policy rather than the organizing abstraction itself.
