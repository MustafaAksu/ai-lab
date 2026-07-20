# ADVISOR-0005: v2 final review (advisor document 5)

Snapshot provenance: attributed advisor artifact received by the operator and
relayed into the ABS-0004 drafting conversation on 2026-07-20. Consumed the
ABS-0004 v2 draft (information-path dependent on the full advisory chain).
artifact_class: advisor. epistemic_authority: advisor. provenance_status:
pre_provenance. Executor identity: reported claim only (not independently
verified). Invocation details: unrecorded. This snapshot is a normalized
immutable text capture from the drafting conversation record.

---

## Overall verdict

V2 is substantially stronger than V1. It successfully incorporates nearly all prior blocking corrections: authorization is separated from routing and admission; endpoint identity is separated from model identity; role authority has three axes; claim-lineage limitations are explicit; composite executors are disclosed; and the implementation sequence is now proposed rather than prematurely committed.

I would classify it as:

> **Ready for challenge round after six targeted corrections.**

Two are conceptually important; four are internal consistency fixes. I would not reopen the broader ontology.

---

# Two remaining conceptual issues

## 1. P2 overstates what deterministic verification buys

This is now the most important issue.

P2 says:

> Where an output's correctness is mechanically checkable, executor origin carries no evidential weight and imposes no admission burden beyond recording.

That is too absolute for three reasons.

First, a deterministic check only establishes the property it actually checks. A schema validator can prove schema conformance; it cannot prove factual correctness. Passing tests establishes the tested behavior, not total implementation correctness.

Second, deterministic tools themselves have provenance:

* tool identity and version;
* test or rule version;
* inputs;
* environment;
* configuration;
* execution result;
* whether the verifier was changed by the same actuator.

Third, witness independence is not the only substitute when deterministic verification is unavailable. Other controls include formal proof, empirical replication, source corroboration, human review, and external measurement.

I recommend replacing P2 with:

```text
[PRINCIPLE] P2. Verification is property-scoped. Successful deterministic
verification may reduce or eliminate witness-independence requirements only
for the specific property the verifier establishes. It never eliminates the
need to record the verifier identity and version, verification inputs,
execution environment, rule or test version, and result; nor does it establish
properties outside the verifier's scope.

Where deterministic verification is unavailable, provenance and witness-path
independence are major controls, but not the only admissible controls.
```

The phrase **"Verification before provenance"** could remain as a shorthand title, but verification and provenance are better understood as complementary rather than inversely proportional.

---

## 2. Qualification currently attaches too broadly to an executor

The document correctly adds `ServiceEndpointIdentity` and `ExecutionProfile`, but `RoleQualification` still qualifies an `executor identity`.

That is too broad.

The same model identity may be:

* served through different endpoints;
* subject to different data-handling conditions;
* given different tools;
* run at different reasoning settings;
* used with or without reconstructible state;
* configured with materially different system instructions.

A qualification established for one deployment and configuration should not automatically transfer to all invocations using the same ModelIdentity.

RoleQualification should therefore be scoped to an execution candidate:

```text
executor identity
service endpoint scope
execution-profile constraints
session-state constraints
role definition
policy version
```

You do not necessarily need another object. Section 4.6 could be amended to say:

```text
[DEF] RoleQualification is a reified policy conclusion that qualifies an
executor for a RoleDefinition only within an explicit execution scope:
service endpoint, permitted ExecutionProfile constraints, session-state
constraints, and policy version. A qualification never transfers implicitly
to another endpoint or materially different execution profile.
```

C2 should then refer to an **execution candidate**, rather than saying that a ModelIdentity may "serve a governed role."

---

# Four internal consistency corrections

## 3. The three decisions need a common representation

Section 3 correctly distinguishes:

1. invocation authorization;
2. routing decision;
3. evidence admission.

But the object model defines:

* `DecisionRecord`;
* `InvocationAuthorization`;
* `RoutingDecision`;

and does not explicitly define an evidence-admission record.

There is also some remaining event/artifact conflation. The decision-making action is an Invocation; the resulting authorization is a record produced by that Invocation.

The cleanest structure is:

```text
DecisionRecord
    decision_kind:
        invocation_authorization
        routing_selection
        evidence_admission
        manual_override
```

Then `InvocationAuthorization`, `RoutingDecision`, and `EvidenceAdmissionDecision` can be subtypes or typed profiles of DecisionRecord.

Suggested clarification:

```text
[DEF] A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds, not executor events.
```

### Authorization bootstrap

There is also a small recursion problem:

* an authorization is issued by a decision invocation;
* under P1, that decision invocation itself apparently requires authorization.

The ABS should mark the termination condition:

```text
[OPEN] Authorization-chain bootstrap: how an authorization chain terminates
in a standing policy, delegated authority, or AccountablePrincipal authority
scope rather than requiring an infinite sequence of prior authorizations.
```

This can remain open for the challenge round, but it should be visible.

---

## 4. ExecutionProfile and EffectiveInputManifest overlap

Both currently contain:

* system-instruction digests;
* tool-schema digests;
* execution parameters.

That invites divergent implementations.

I suggest this boundary:

### ExecutionProfile

How the executor was configured:

```text
service endpoint
requested API model name
sampling parameters
reasoning parameters
provider request flags
runtime/library version
tool-execution permissions
```

### EffectiveInputManifest

What information could influence the result:

```text
rendered system/developer/user messages
context manifest
retrieval results
attachments
tool definitions exposed to the model
prior tool outputs
session-state reference
inherited provider-managed state
```

The EffectiveInputManifest may reference the ExecutionProfile, but should not duplicate it.

Correspondingly, Slice A should explicitly create a minimal `EffectiveInputManifest`, not merely record a `ContextManifest` reference. Otherwise the first slice still cannot represent all effective inputs needed for later blindness analysis.

A stronger Slice A wording would be:

```text
Minimal EffectiveInputManifest containing rendered prompt digest,
system/developer instruction digests, ContextManifest reference, exposed
tool-schema digest, prior tool-result references, and session-state mode.
```

Only fields actually applicable to `compare_providers.py` need to be populated.

---

## 5. C9 uses inconsistent status vocabularies

C9 says extracted outputs carry:

```text
source_lineage_status: pre_provenance
```

But Section 7 distinguishes:

* provenance status: `pre_provenance`;
* claim-lineage status: `source_lineage_partial`.

These should not be combined into one field.

Use:

```text
source_provenance_status: pre_provenance
claim_lineage_status: source_lineage_partial
independent_observation: false
```

This is minor textually but important ontologically.

---

## 6. Section 5's "first-slice" predicates do not match Section 10

Section 5 calls ten predicates the candidate first-slice core, including:

```text
invocation resolved_to model_identity
catalog_assertion asserted_by provider_organization
catalog_assertion describes model_identity
```

But Section 10 intentionally defers model resolution and catalog records to Slice B.

Split the predicates by proposed slice.

### Slice A

```text
artifact produced_by invocation
invocation executed_by executor_identity
invocation requested_via service_endpoint
invocation used_execution_profile execution_profile
invocation used_inputs effective_input_manifest
invocation member_of session
invocation spawned invocation
```

### Slice B

```text
invocation resolved_to model_identity
catalog_assertion asserted_by provider_organization
catalog_assertion concerns catalog_subject
```

I would also replace:

```text
catalog_assertion describes model_identity
```

An atomic assertion can concern an API alias, endpoint, price, region, or model identity. It does not always describe a ModelIdentity.

Possible representation:

```text
catalog_assertion concerns catalog_entity
```

or typed fields:

```text
assertion_subject
assertion_predicate
assertion_value_or_target
```

---

# Enforcement-matrix cleanup

The matrix is much better, but it still violates its own column semantics in a few cells.

Examples:

```text
Representability: partial (manual)
Representability: practice
Evidence: current practice
```

Representation should be something like:

```text
none | partial | full
```

"Manual" belongs under enforcement, and "practice" is not enforcement evidence.

In particular, C6 says manual enforcement only counts when it leaves an artifact, but its evidence cell says:

```text
current practice; future validator tests
```

If no current artifact records the authority-separation check, C6 should either be:

```text
Normative state: adopted, not currently evidenced
```

or its current evidence should name an actual record type.

Suggested normalization:

| Constraint | Representability                    | Current enforcement evidence                      |
| ---------- | ----------------------------------- | ------------------------------------------------- |
| C3         | partial                             | named warrant attestation                         |
| C6         | partial                             | named review or decision artifact; otherwise none |
| C7         | full/partial through VERIFY records | VERIFY record                                     |
| C9         | partial                             | named disclosure field or record                  |

This is not a design blocker, but the final document should not use "current practice" as proof after explicitly rejecting that standard.

---

# Challenge-round blindness

The challenge-round setup is strong, but Question 12 says:

> The expected safe answer is no.

That is deliberately leading and conflicts with the stated maximum-blindness objective. It tells every provider what conclusion will be rewarded.

Change it to:

```text
12. Under what conditions, if any, can an unresolved model identity qualify
as an independent witness path? Identify the failure behavior when equivalence
cannot be resolved.
```

The adopted constraint already states AI-Lab's current answer. The challenge round should still be allowed to attack it without being told the expected result.

I would also change "maximum blindness" in Evidence Inputs to **"maximum practical isolation"**, since the document itself is the product of a braided advisory chain. The provider is blind to the review history, not to the resulting concepts.

---

# One optional ontology refinement

`ServiceEndpointIdentity` currently includes region, data-handling characteristics, and processing jurisdiction as identity properties.

Those facts can change over time, just like pricing and deprecation. To apply the same discipline used for ModelIdentity:

* keep stable endpoint identifiers and operating organization on the identity;
* represent region, processing jurisdiction, retention behavior, and data handling as time-bounded endpoint assertions.

This is not necessary before the challenge round, but providers may otherwise identify it as the next identity/assertion conflation.

---

# Assessment of the three flagged drafting decisions

## C9 as a named constraint

**Correct decision.**

It is the actual anti-laundering rule. Keeping it visible in the matrix is much better than hiding it in phase-in prose.

Only the status-field inconsistency needs correction.

## P1–P5 as anchoring principles

**Correct structurally, with P2 rewritten.**

P3, P4, and P5 are especially strong and concise. P2 is valuable in intent but currently overclaims the sufficiency of deterministic verification.

## Question 13

**Keep it.**

It is an excellent adversarial question. Composite disclosure itself can be gamed through:

* false claims of immateriality;
* a generic wrapper invocation hiding executor changes;
* subordinate calls summarized rather than individually recorded;
* dynamic plugin loading;
* remote services misrepresented as deterministic tools.

That question should produce useful pressure on the definition of "material subordinate execution."

---

# Final recommendation

After these changes, I would approve it for the challenge round.

### Must fix before distribution

1. Rewrite P2 as property-scoped verification.
2. Scope RoleQualification to endpoint and execution-profile conditions.
3. Clarify DecisionRecord kinds and add evidence admission explicitly.
4. Remove ExecutionProfile/EffectiveInputManifest duplication.
5. Correct C9's status fields.
6. Align Section 5 predicates with Slices A and B.
7. Remove the expected answer from Question 12.
8. Correct enforcement-matrix cells that treat practice as evidence.

### Appropriate to leave open

* authorization bootstrap;
* exact AccountablePrincipal implementation;
* whether decision kinds are subtypes or one record family;
* endpoint mutable-property representation;
* claim-level lineage mechanics;
* consequence thresholds;
* third-provider requirements.

With those edits, V2 will be internally coherent enough that the challenge round can attack the ontology's true unknowns rather than rediscovering document-level contradictions.
