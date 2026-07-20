# ADVISOR-0003: v1 adversarial review (advisor document 3, "ChatGPT comments")

Snapshot provenance: attributed advisor artifact, reported by the operator as
ChatGPT-authored, relayed into the ABS-0004 drafting conversation on
2026-07-20. artifact_class: advisor. epistemic_authority: advisor.
provenance_status: pre_provenance. Executor identity: reported claim only
(not independently verified). Invocation details: unrecorded. Consumed the
ABS-0004 v1 draft (information-path dependent on it). This snapshot is a
normalized immutable text capture from the drafting conversation record.

---

## Overall assessment

This is a strong ontology draft and a suitable basis for a challenge round. However, I would **not freeze or admit it yet**. Several internal contradictions affect the central thesis, the first-slice boundary, and the claimed enforceability of the constraints.

The most important issue is this:

> The document says AI-Lab authorizes invocations, but it does not define an authorization object.

It defines routing, qualification, invocation, and eventual output admission concepts, but the actual authorization event remains implicit.

## Blocking issues

### 1. The normative tagging system contradicts itself

The metadata says:

* `[CONSTRAINT]` means an **adopted constraint**.
* `[COMMIT]` means an implementation commitment.

But C1, C2, C4, C5, and C8 are tagged `[CONSTRAINT]` while the enforcement matrix describes them as merely `proposed`. Those cannot both be true.

Section 9 also commits to an implementation slice under a **future GAP-0005**, before that gap, plan, or slice has been admitted. That is premature under AI-Lab's own governance sequence.

I recommend these tags:

```text
[DEF]
[PRINCIPLE]
[PROPOSED_CONSTRAINT]
[ADOPTED_CONSTRAINT]
[COMMIT]
[OPEN]
```

Then change Section 9 from a commitment to something like:

```text
[PROPOSAL] Candidate boundary for the first implementation slice,
subject to GAP definition, plan admission, and slice review.
```

The evidence-document digest commitment can remain `[COMMIT]`, because it concerns preparation of this ABS rather than future runtime implementation.

The anchoring thesis is also not really a definition. It is an architectural principle and should be tagged `[PRINCIPLE]`.

---

### 2. The central ontology lacks `InvocationAuthorization`

`RoutingDecision` explains why an executor was selected. It does not necessarily establish that the invocation was authorized.

`RoleQualification` says an executor is generally eligible. It does not authorize a particular invocation under a particular consequence, context, and independence state.

The ontology needs to distinguish three decisions:

#### Invocation authorization

An ex-ante decision:

```text
May executor E perform invocation I
under role R, consequence C, and conditions K?
```

#### Routing decision

A selection decision:

```text
Why was executor E selected rather than the alternatives?
```

#### Evidence admission

An ex-post decision:

```text
May output O enter governed evidence,
and with what epistemic status?
```

This distinction already exists implicitly in the text: experimental models may run, but their outputs cannot silently enter governed evidence. That means execution authorization and output admission are separate.

Suggested object:

```text
InvocationAuthorization
    authorization_id
    invocation_request
    authorized_executor
    assigned_role
    consequence_class
    applicable_policy
    qualifications_relied_on
    independence_requirements
    conditions
    issued_by
    status
```

Suggested relations:

```text
authorization authorizes invocation
authorization assigns_role role_definition
authorization relied_on role_qualification
authorization issued_by decision_invocation
invocation authorized_by authorization
artifact admitted_by admission_decision
```

Without this object, the anchoring thesis is not yet represented by the ontology.

---

### 3. `Actuator` is not an epistemic authority

The document describes Role as:

```text
task function × epistemic authority
```

But its second axis contains:

* witness;
* advisor;
* adjudicator;
* actuator.

`Actuator` is operational authority, not epistemic authority. This recreates a category error inside the proposed correction.

A better structure is:

```text
task_function
epistemic_authority
action_authority
```

For example:

```text
task_function:
    extract | classify | retrieve | generate | compare |
    synthesize | evaluate | plan | implement | verify

epistemic_authority:
    none | witness | advisor | adjudicator

action_authority:
    read_only | repository_mutator | external_actuator
```

The accountable authority remains separate again.

This avoids several authority leaks. Under the current design, a role could be:

```text
task_function: implement
epistemic_authority: advisor
may_mutate_repository: true
```

That invocation would mutate the repository without being classified as an actuator. It satisfies the literal structure while defeating its intended separation.

Similarly:

```text
task_function: generate
epistemic_authority: witness
```

could generate an unsupported factual claim and have it treated as witness testimony. Witness authority should require observable or source-grounded evidence, not merely a model-generated candidate finding.

A witness constraint should therefore include something like:

```text
witness outputs must identify their observation source,
source span, measurement, or deterministic derivation.
Unsupported hypotheses are advisor outputs, not witness evidence.
```

---

### 4. C1 is incompatible with human and tool invocations

C1 requires every governed output to link to:

> "a model identity or explicitly unresolved model claim"

But the ontology explicitly says that humans and tools can also execute invocations.

A human-authored decision or deterministic validator output should not require a ModelIdentity.

Rewrite C1 around the generic executor:

```text
A governed output created after activation of the applicable provenance
profile is admissible only if it links to:

- its producing invocation;
- the invocation's executor identity;
- its role or authority assignment;
- its rendered prompt or instruction record, where applicable;
- its effective input manifest;
- its session-state mode;
- its execution environment;
- and its output record.

Model-specific identity and catalog fields are required only when a model
participated as executor or execution resource.
```

There is a second contradiction: C1 requires a role and prompt version, but:

* `assigned_role` is deferred;
* `used_prompt` is deferred;
* RoleDefinition enforcement is deferred;
* neither predicate is in the first-slice minimal core.

Therefore, Slice 1 cannot enforce C1 as written.

There are two clean options:

1. Move complete C1 enforcement to the slice that implements roles and prompts.
2. Define staged provenance profiles:

```text
provenance_v1:
    executor, inputs, session state, output, timestamps

authorization_v1:
    role assignment, qualification, consequence, authorization

lineage_v1:
    claim/input ancestry and independence assessment
```

The staged approach is more honest and more compatible with slice discipline.

---

### 5. Provider, model developer, host, and API surface are conflated

A model may be:

* developed by one organization;
* hosted by another;
* exposed through multiple API surfaces;
* deployed in different regions;
* addressed through mutable aliases.

Examples include a model served directly by its developer versus through a cloud platform or third-party host. These routes can have different identity resolution, jurisdiction, data handling, availability, and catalog properties.

The ontology needs at least a `ServiceEndpointIdentity` or `ProviderSurface`:

```text
ProviderOrganization
ServiceEndpointIdentity
ModelIdentity
CatalogAssertion / DeploymentBinding
```

An invocation would then record:

```text
executed_by model_identity
requested_via service_endpoint
requested_model_name
resolved_model_identity
catalog_snapshot
```

`ModelIdentity.provider_id` should probably become `originator_id` or be removed from the stable identity object. The serving provider belongs to the deployment or endpoint relation.

Likewise, `deprecation_status` should not be a ModelIdentity field. Deprecation is mutable and often endpoint-specific, so it belongs in a catalog assertion.

`governance jurisdiction` also usually belongs partly to the legal provider and partly to the actual processing endpoint or region. Putting it only on Provider is too coarse for the data-governance questions the ABS intends to support.

---

### 6. Catalog assertions need property-level verification

The current CatalogAssertion combines:

* alias resolution;
* modalities;
* tools;
* context limits;
* pricing;
* regional restrictions;
* lifecycle status.

These claims may have different sources, timestamps, and verification outcomes. Pricing may be verified while alias resolution remains unverifiable.

One verification status for the entire object will create false all-or-nothing results.

A cleaner model is:

```text
CatalogSnapshot
    snapshot_id
    provider_surface
    observed_at
    source_set
    assertions[]
```

Each `CatalogAssertion` is atomic:

```text
subject
predicate
value
unit
scope
valid_from
valid_until
source
verification_outcome
verified_at
```

For example:

```text
subject: api-name-X
predicate: resolves_to
value: model-identity-Y
```

and separately:

```text
subject: api-name-X
predicate: context_limit
value: 400000
unit: tokens
```

This also clarifies that `verified_current`, `stale`, and `unverifiable` attach to individual claims rather than to an entire heterogeneous catalog record.

## Missing load-bearing objects

### DecisionRecord

The relation vocabulary uses `decision` repeatedly, but no Decision object is defined.

A decision is more than a generic artifact because it has:

* a target;
* a proposed or effective status;
* an issuer;
* an accountable approver;
* evidence;
* policy authority;
* activation state;
* possible supersession.

Define `DecisionRecord`, or explicitly state that an existing warrant/admission object fulfills this role.

Also distinguish:

```text
recommended_status
effective_status
```

Otherwise a model-issued recommendation could appear to have assigned the final effective status before accountable approval.

### AccountablePrincipal

`accountable_principal` appears in the predicates but is not defined.

It should not necessarily equal HumanIdentity. A principal may be:

* a pseudonymous operator identity;
* a delegated role;
* a governance body;
* an organization.

A privacy-preserving form could be:

```text
principal_id
principal_kind
authority_scope
delegation_reference
```

No personal name or unnecessary identifying data is required.

### EffectiveInputManifest

A ContextManifest may describe the context assembled by AI-Lab, but witness independence depends on **everything capable of influencing the invocation**, including:

* system and developer instructions;
* rendered user prompt;
* tool definitions;
* retrieved documents;
* attachments;
* session state;
* prior tool results;
* local environment;
* provider-managed state.

The ontology needs either an `EffectiveInputManifest` or an `ExecutionEnvelope`.

At minimum it should include:

```text
prompt_template_version
rendered_prompt_digest
system_instruction_digest
tool_schema_digest
context_manifest
retrieval_results
session_state_reference
execution_parameters
```

`used_context` alone cannot prove blindness unless the referenced manifest is explicitly defined as complete for all effective inputs.

### Claim or EvidenceItem

Artifact-level provenance is not sufficient for claim independence.

One artifact may contain:

* an original observation;
* a copied finding code;
* a new inference;
* a paraphrase of another witness;
* an independent measurement.

Assigning one lineage status to the entire artifact loses these distinctions.

The ontology should define a future `Claim` or `EvidenceItem`, anchored to an artifact span:

```text
claim_id
artifact_reference
span
proposition
claim_kind
```

Then relations can include:

```text
claim derived_from claim
claim supported_by evidence_item
decision evaluates claim
invocation consumed claim
```

This can remain deferred, but the ABS should acknowledge that Slice 1 provides **artifact-level potential-dependence detection**, not full claim-level independence proof.

### Run or ProtocolRound

An invocation should be atomic: one executor performing one execution event.

An agent workflow may contain:

* a model invocation;
* several tool invocations;
* retries;
* a second model invocation;
* a validator;
* a human approval.

That needs a parent `Run`, `WorkflowExecution`, or `ProtocolRound`.

Round kinds such as blind witness, comparison, synthesis, and adjudication should be properties of this protocol object—not substitutes for lineage analysis.

## Independence needs refinement

### Blindness is necessary but not sufficient

The statement that only blind witness rounds provide strong independent corroboration is too categorical.

A blind witness may still share:

* the same erroneous source;
* the same leading prompt;
* the same hidden session state;
* a summary derived from the other witness;
* the same unsupported assumption.

Conversely, a witness output generated independently remains independently generated even if it is later placed into a comparison round.

A better constraint is:

> Isolation from other witness outputs is necessary for treating an invocation as an independent confirmation of those outputs, but it is not sufficient for overall witness-path independence. Round labels describe protocol; lineage determines admissibility.

### Avoid a single independence score initially

Independence has several dimensions:

```text
information_path_independence
source_independence
executor_identity_independence
provider_or_organization_correlation
prompt_common_cause
session_state_confidence
claim_lineage_completeness
```

Some are hard disqualifiers; others are weaker correlation indicators. Combining them immediately into one numeric score risks laundering a hard dependency through several positive factors.

The first implementation should probably produce:

```text
qualified_independent
dependent
unresolved
```

alongside dimension-specific reasons.

Provider similarity should be recorded as a correlation factor, but the ABS should not yet claim a mathematically defined "weight reduction" without evaluation evidence.

### Unknown identity must not pass as independent

C3 can be evaded if two invocations use unresolved aliases and the system cannot establish whether they resolved to the same model.

Add:

> Unknown or unresolved model equivalence cannot establish model-identity independence. It yields `independence_unresolved`, not an independent path.

## A concrete pre-provenance laundering path

The current legacy rule can be exploited as follows:

1. A pre-provenance artifact `P` contains an unsupported claim.
2. A human creates a new artifact `S` summarizing `P`.
3. The production of `S` has complete modern provenance, but `S` does not record claim derivation from `P`.
4. A blind model receives `S`, not `P`, and repeats the claim.
5. An adjudicator sees `P` and the model result as two apparently separate witness paths.
6. The inherited claim has now acquired a modern, apparently independent confirmation.

The key rule needed is:

> Complete production provenance does not imply complete claim provenance.

A newly created artifact must not erase the provenance limitations of the claims it carries.

Until claim-level derivation exists, any new artifact grounded in pre-provenance material should conservatively inherit a lineage limitation such as:

```text
source_lineage_partial
```

Unknown lineage should never increase independence.

## Predicate problems

The predicate list needs a registry with:

* source type;
* target type;
* exact meaning;
* cardinality;
* inverse;
* temporal semantics;
* whether transitive;
* evidence requirements;
* authoritative-default behavior.

Several predicates are currently ambiguous:

| Predicate                       | Problem                                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------------------ |
| `executed_by` / `executed_with` | Both appear to identify the executor for model calls.                                      |
| `relied_on`                     | Does this mean identity resolution, authorization evidence, or actual decision rationale?  |
| `describes`                     | Too broad for alias-to-model resolution.                                                   |
| `derived_from`                  | Could mean textual copying, causal ancestry, conceptual influence, or workflow succession. |
| `continued_from`                | Session chronology or semantic dependency?                                                 |
| `verified_by`                   | Schema validation, factual verification, test execution, or approval?                      |
| `approved_by`                   | Approval of content, execution, admission, or activation?                                  |
| `qualifies`                     | RoleQualification is ternary: executor, role, and policy.                                  |
| `used_context`                  | Whole manifest, one item, or all effective inputs?                                         |

Specific recommendations:

```text
invocation executed_by executor_identity
invocation requested_via service_endpoint
invocation resolved_to model_identity
```

Drop `executed_with` unless it has a meaning distinct from executor identity.

Move catalog reliance to the selection or authorization event:

```text
routing_decision relied_on catalog_snapshot
authorization relied_on role_qualification
```

A RoleQualification should be reified with at least:

```text
role_qualification qualifies_executor executor_identity
role_qualification qualifies_for role_definition
role_qualification issued_under policy
role_qualification based_on evaluation_outcome
```

`decision assigns_status accepted` does not naturally fit `GraphRelation`, because `target_id` expects a node, not a literal. Either make status a field on DecisionRecord or define a reified StatusAssignment.

## Consequence calculation should be monotonic

This expression is too loose:

```text
effective_consequence = default_consequence + modifiers
```

Low, medium, and high are ordinal classes, not numbers.

Use:

```text
effective_consequence =
    maximum(default_consequence, applicable_modifier_levels)
```

Modifiers should only raise consequence automatically.

A downward override should be a separate governed exception requiring:

* reason;
* accountable principal;
* scope;
* evidence;
* expiry or review condition.

It should not be capable of overriding hard prohibitions such as disqualifying lineage conflicts.

## Enforcement matrix corrections

The matrix is valuable, but several columns mix distinct concepts:

* "Partially (manual)" is not a representation status.
* "Yes (practice)" is not a data representation.
* A manually enforced rule should not say `Enforceable now: No`.
* Current mechanisms and future mechanisms are mixed.
* "Slice 2" and "Slice 3" are referenced before those slices are defined.
* "Warn until slice, reject after" lacks an explicit activation condition.

I recommend these columns:

```text
Constraint
Normative state
Representability
Current enforcement
Target enforcement
Current failure behavior
Activation condition
Enforcement evidence
Dependencies
```

Use capability dependencies instead of unnamed slice numbers until an admitted plan exists.

Also, manual overrides under C8 must themselves be governed records. Otherwise "documented manual override" becomes a universal escape hatch.

## The proposed first slice is both too broad and incomplete

It includes:

* ModelIdentity;
* CatalogAssertion;
* Invocation;
* Session;
* executor references;
* eight predicates;
* validators;
* fixtures.

That is several ontology families, not one small vertical slice.

At the same time it omits:

* `used_prompt`;
* role assignment;
* complete effective inputs;
* service endpoint;
* authorization;
* output-admission status.

A safer sequence would be:

### Slice A — Invocation provenance capture

For one existing provider-comparison path only:

* atomic InvocationRecord;
* executor reference;
* requested API model name;
* endpoint/provider surface;
* rendered prompt digest;
* ContextManifest reference;
* explicit session-state mode;
* output artifact `produced_by` relation;
* success/failure status;
* validator and integration fixture.

No routing or catalog enforcement.

### Slice B — Catalog identity resolution

* ModelIdentity;
* ServiceEndpointIdentity;
* atomic CatalogAssertions grouped into CatalogSnapshot;
* requested-name to resolved-identity linkage;
* freshness and verification validator.

### Slice C — Role and authorization

* RoleDefinition;
* executor qualification;
* InvocationAuthorization;
* consequence class;
* experimental versus governed execution boundary.

### Slice D — Lineage and evidence admission

* effective-input ancestry;
* pre-provenance inheritance;
* admission decisions;
* conservative independence statuses.

This sequence is more consistent with AI-Lab's small, observable, testable slice discipline.

## Evidence-input concern

An immutable digest proves that a retained document has not changed. It does not preserve the document or make it auditable.

For advisor evidence used by the ABS, retain:

* a normalized immutable text snapshot, or an admissible excerpt;
* its digest;
* capture timestamp;
* source label;
* provenance limitations.

A digest alone is an integrity anchor, not an evidence artifact.

The authorship metadata should also avoid presenting `Claude` as a verified ModelIdentity if the Evidence Inputs simultaneously say that the model identity was not independently established. Use an attributed executor label or explicitly mark it as a reported identity claim.

## Recommended challenge-round additions

Add these questions:

7. Where is invocation authorization represented, and how is it distinguished from routing and evidence admission?

8. Can the ontology represent the same model served through different organizations, endpoints, regions, or mutable aliases without creating false model independence?

9. Does provenance apply only to artifact production, or also to the derivation of individual claims?

10. What information must an effective-input record contain before an invocation may be treated as blind?

11. Which constraints apply identically to models, tools, and humans, and which require executor-specific conflict rules?

12. Can an unresolved model identity ever qualify as an independent witness path? The expected safe answer should be no.

## Final recommendation

The ABS is close, but I would make five corrections **before** sending it to providers:

1. Repair normative tagging and remove the premature implementation commitment.
2. Add InvocationAuthorization and distinguish it from RoutingDecision and evidence admission.
3. Split epistemic authority from action authority.
4. Fix C1 and the first-slice contradiction, including human/tool executors.
5. Add ServiceEndpoint and EffectiveInputManifest to the core ontology.

The challenge round should then focus on the genuinely open issues—claim-level lineage, independence qualification, consequence rules, and provider/path diversity—instead of spending its effort detecting avoidable internal inconsistencies.
