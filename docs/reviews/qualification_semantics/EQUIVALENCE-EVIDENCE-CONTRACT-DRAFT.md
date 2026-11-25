# Equivalence evidence contract — proposed r1

[ALG] **Design proposal for PLAN-20261125-0001; not admitted or implemented.**
Baseline: 5515f55894b10ad70c321340257f67a960dcc382. Actual drafting executor:
ChatGPT. This document proposes contracts and explicit choices for review; it
creates no binding assessments, qualified identities or authority.

## 1. Governing separation and compatibility

[THM] Identity non-equivalence does not entail independence; independence does
not entail authorization. A result about one relation cannot settle the others.

[ALG] Bounds come from [ABS-0004 §§4.2–4.7, 4.17–4.19, C3/C5/C10/C12–C14](../../abstractions/ABS-0004-invocation-authorization-ontology.md)
and [DECISION-20260814-0001](../../self_model/decisions/DECISION-20260814-0001.json).
The decision preserves a catalog-asserted relation while withholding the model
identity gate unless both sides have corroborated support. It does not supply
a multi-source rule or a tool/human evidence vocabulary.

The candidate interfaces are pure assessments over retained, declared inputs.
They return three separate products:

| Product | Meaning | Does not establish |
| --- | --- | --- |
| Identity relation | equivalent, non_equivalent or unresolved, under a named per-kind rule | All C5 independence dimensions |
| Qualification-condition findings | Named C3/C10 conditions satisfied, violated or unresolved, with evidence | An authorization decision |
| Authority decision | Outside this PLAN | No implicit grant from either preceding product |

The proposed records below are **external append-only annotations**, not fields
added to InvocationRecord v1. The existing executor mapping is closed to kind,
reference and identity_verification_status. Original InvocationRecords,
IdentityResolutions, VERIFY records and their capture-time statuses stay
unchanged. Later evidence creates a linked assessment rather than overwriting
an earlier one. No record-kind names or new enums in this draft are registered
canonical schemas yet.

## 2. Common assessment envelope

[ALG] Proposed shapes: ModelResolutionAssessment, ToolBindingAssessment,
HumanBindingAssessment and EquivalenceAssessment. Exact names and schema
versions must be frozen in the reviewed implementation scope.

| Required group | Minimum content |
| --- | --- |
| Subject | Exact invocation/reference, complete retained-content digest, executor kind, occurrence time |
| Assessment | Rule identifier/version, assessor reference, assessed_at, mode, evidence knowledge cutoff |
| Mode | event_time or retrospective; the latter links the prior resolution and cannot claim earlier availability |
| Evidence set | Manifest of every supplied item and digest, declared search/source scope, known omissions and coverage finding |
| Proposition | Exact reference-to-identity or event-to-actor claim, canonical target, namespace, scope and validity interval |
| Provenance | Source/issuer, capture method, observed/captured times, relevant assertion or claim span |
| Separate checks | Payload integrity, source authentication, binding establishment, temporal/endpoint applicability |
| Findings | Supporting witnesses, excluded items with reasons, contradictions, unresolved items and candidate targets |
| Result | Relation or per-kind binding outcome; limitations; links to predecessor assessments |

A content hash establishes which bytes are retained. Authentication may
establish who supplied them. Neither by itself establishes the truth of an
identity binding. An input flag saying established or independently_corroborated
is not a substitute for the scoped evidence and verification it names.

Malformed input has an explicit validation result; it is not swallowed in favor
of a later successful candidate. Repeated IDs with different bytes are a
conflict. Exact duplicates do not add evidence weight or change the result.
Canonical output sorts evidence references/reasons for deterministic
serialization. Permutation, duplication and argument-swap invariants are
reviewed separately from adequacy of the underlying evidence.

### Evidence availability and event time

An event-time assessment uses evidence shown to have been available at the
event. Snapshot observation time, capture time and later import/assessment time
are separate. A later import of demonstrably earlier retained evidence does
not change its original availability; a later observation cannot be backdated.
Unavailable or conflicting timing evidence leaves applicability undetermined.

For model/catalog inputs, retain the existing inclusive assertion validity
boundaries and explicit freshness window: valid_from <= event <= valid_until where the upper bound
exists, observed_at <= event, and event - observed_at <= configured window.
The chosen model window and availability rule are versioned inputs. Tool and
human validity/freshness conditions belong to their separately reviewed D4/D5
binding rules; the model window is not transferred to those kinds. Later
corroboration/revocation may inform a **retrospective** assessment with its own
cutoff; it cannot silently become event-time corroboration.

## 3. R13: endpoint binding before model assertion selection

[NUM] Current invocation spellings include openai.responses and
anthropic.messages. The corresponding ServiceEndpointIdentity records contain
operating_organization and endpoint_identifier; snapshots reference their EID
record IDs. Comparing an invocation spelling directly with an EID would reject
valid current representations. The current resolver merely checks that the
spelling is present; [the baseline probes](SOURCE-REVIEW-BASELINE.md) reproduce
cross-endpoint resolution.

[ALG] Proposed endpoint path:

1. Bind the invocation's retained service_endpoint spelling and event context
   to one established ServiceEndpointIdentity. Retain the EID record/digest and
   the rule/evidence that establishes this binding.
2. Exact endpoint_identifier agreement is a necessary syntactic match for the
   default path, not sufficient proof where organization or alias binding is
   ambiguous. Do not infer the operating organization from requested model
   name or the model's originator.
3. An alias needs explicit, event-applicable alias evidence under a reviewed
   rule. There is no automatic hostname, case, provider, proxy or region
   normalization. An unresolved collision or missing binding remains unresolved.
4. Require the snapshot's service_endpoint_id to reference that same established
   endpoint. A different established endpoint is inapplicable, even if the
   requested model name matches.
5. Select only resolves_to assertions for the exact requested name and applicable
   event interval. Retain target ModelIdentity records and their digests.

Endpoint evidence belongs in the assessment inputs/annotation; it does not
rewrite historical invocation strings. Equality of endpoints does not establish
model identity or provider independence. A proxy/originator relationship does
not substitute for an endpoint binding.

## 4. R14: applicability, then complete aggregation

### 4.1 Three applicability outcomes

[ALG] Classify each supplied source relative to the named invocation,
endpoint, requested name, property, event time and declared evidence scope:

| Outcome | Examples | Aggregate treatment |
| --- | --- | --- |
| applicable | Established matching endpoint; matching assertion/property; valid event interval and availability | Evaluate all its relevant targets and adverse findings |
| inapplicable | Established different endpoint; absent requested-name assertion; proven expired/future-only source for event-time mode | Exclude with the precise reason; no veto or positive support |
| undetermined | Missing endpoint binding, uncertain time/scope, potentially relevant malformed input | Preserve as unresolved; cannot be silently excluded |

A structurally invalid record may be rejected at input validation before
applicability is knowable. Proven inapplicability requires enough trustworthy
structure to establish the exclusion. Do not discard arbitrary malformed input
merely by reading one convenient field.

A capture-wide contradicted status blocks every applicable identity assertion
from that capture. The current schema supplies no property-specific contradiction
scope. Narrowing it requires a separate supported assessment; this draft does
not infer narrower scope from unrelated metadata. Conversely, a contradicted
capture proven irrelevant to this invocation does not veto its resolution.

### 4.2 Candidate model aggregation rule

[ALG] **Proposed choice for admission review: agreement over all applicable
targets, with relevant adverse evidence preserved.** This is a new proposed
aggregation rule, not a rule already granted by DECISION-20260814-0001.

For each invocation:

1. Validate the complete input manifest and classify all supplied sources.
2. Collect every applicable target and the complete source/assertion/capture
   references supporting or contesting it.
3. If applicability remains undetermined for a potentially relevant item, return
   unresolved with those items named.
4. If any applicable capture is contradicted, any applicable snapshot contains
   ambiguous targets, or applicable sources disagree on the target, return
   unresolved. Preserve candidate identities and all adverse reasons.
5. With no applicable target, return unresolved with non-resolution reasons.
6. With exactly one target and no blocking finding, report the catalog-asserted
   identity and its full support set. Do not choose the first, newest, majority
   or strongest-label source.

The declared source scope is bounded, not a claim of knowledge of every possible
source. A known omitted or unavailable potentially relevant item within that
scope is an undetermined input for step 3, even though its bytes are not supplied.
Agreement among the supplied sources may be retained as a bounded observation,
but it cannot yield a clean aggregate or clear the identity condition while that
coverage question remains unresolved. Exclusion needs an evidenced applicability
reason under the reviewed scope rule; a complete=true flag does not supply it.

A positive result must therefore be unchanged for every permutation of the same
evidence set. Invalid/unknown sources cannot disappear because an earlier item
happened to resolve.

Supersession is event-sensitive and evidence-backed. A newer timestamp or a
superseded_by string alone cannot erase a conflicting source. The first slice
has no source-priority, majority-vote or automatic supersession policy: unresolved
supersession stays visible and blocks wherever it could affect the result.

### 4.3 Evidence support without an ordinal ranking

For the unique agreed identity, retain the **set** of observed evidence classes
and the exact witnesses for each class. Do not synthesize one strongest or
weakest class, and do not relabel a provider self-report because another source
corroborates the same mapping.

Proposed model identity-gate condition: the relation must be **non_equivalent**,
declared-source coverage must have no unresolved potentially relevant omission,
and each side needs at least one applicable,
positively corroborating witness for that exact endpoint/name/identity/event
binding, and neither side may retain a blocking conflict. The witness must name
the property-specific verification/assessment, its scope and supporting evidence;
a third_party_record label or channel-authentication status alone is insufficient.
Agreement with an attributed self-report does not negate valid corroboration;
contradiction with it cannot be ignored by ranking the corroborated source higher.

Equivalent and unresolved relations always block this identity condition,
including when both sides have valid corroboration for the same identity.

This is an existential witness condition after conflict exclusion, **not** a
total order on evidence classes. The existing both-side corroboration threshold
remains necessary. Clearing this identity subcondition still does not clear
ancestry, C5, C10 or authorization.

The legacy blocks_adjudication property is model-specific and incomplete as an
overall gate. A future compatibility adapter must preserve that limited meaning,
retain per-side evidence, and prevent consumers from treating False as a full
permission. Tool/human results must not be fed fabricated model evidence classes
to make that property return False.

## 5. Tool/tool binding contract

[ALG] Proposed binding identity is the pair:

    T(invocation) = (canonical ToolIdentity, canonical release/version identity)

| Required evidence | What must be established |
| --- | --- |
| Namespace rule | Naming authority, identity/version semantics, aliases, uniqueness and scope |
| Release binding | Exact retained release manifest connects identity/version to executable or package artifacts |
| Issuer binding | Source is established as the issuer of that release-binding assertion under the named rule |
| Event execution binding | Retained observation connects the named invocation to the artifacts actually executed |
| Artifact references | Digests and roles of entry point, executable/package, interpreter/build components as applicable |
| Version/alias findings | Canonical version identity; no unresolved renamed command, package alias, collision or release alias |
| Assessment | Property-specific checker/witness, rule version, exact inputs, result and limitations |

A concrete candidate path is an attributable release manifest plus an
event-specific artifact-execution observation, assessed under a named
ToolBinding rule. A signature is one possible authentication mechanism; no
cryptographic mechanism or issuer is silently designated trusted here. Raw
version strings, filenames, binary digests and the existing VERIFY writer's
self-description do not automatically meet this contract.

If both bindings are established and their canonical pairs agree, relation =
equivalent. If both are established and canonical inequality is established
under the namespace/alias rules, relation = non_equivalent. Otherwise relation =
unresolved. Distinct namespaces alone do not establish distinct tools.

Identity/version equality is not byte equality: platform builds may have
different bytes for one release; identical bytes may be named by different
unestablished identities. Configuration differences do not manufacture distinct
tool identities.

Full execution disclosure is assessed separately: material configuration,
environment, dependencies, subordinate invocations and external interactions
remain governed by §4.7. Missing configuration can defeat deterministic or
qualification standing while an otherwise established identity/version relation
remains equivalent. If missing evidence prevents knowing which tool/version
actually ran, the binding itself is unresolved. A version change can establish
non-equivalence while preserving shared code/verifier ancestry.

## 6. Human/human principal binding contract

[ALG] Proposed principal binding has two independent obligations:
**reference-to-principal binding** and **principal-to-event-actor binding**.

| Required evidence | What must be established |
| --- | --- |
| Principal semantics | Versioned namespace rule defining what the principal denotes |
| Canonical reference | Stable principal reference and non-reassignment/continuity semantics |
| Reference binding | Attributable enrollment/witness finding connecting the declared reference to that principal |
| Alias/distinctness | Name/account/key changes, alias deduplication and the basis for canonical equality or distinctness |
| Event actor binding | Evidence that this principal acted in the exact invocation/event |
| Temporal validity | Applicable time, revocation, reassignment, compromise and shared/delegated-control findings |
| Assessment | Named rule, source/witness identity, exact evidence, outcome and unresolved limitations |

A candidate path combines a retained, attributable enrollment finding under a
named HumanBinding rule with event-specific actor evidence. Account ownership
and credential possession alone do not establish who performed an event.
A signed action can involve a shared key, delegated automation or compromised
credential; unresolved actor binding remains unresolved.

Same established canonical principal, including established aliases, yields
equivalent. Established distinct principals under the applicable namespace
uniqueness/alias rule or a named pairwise finding yield non_equivalent.
Different names, IDs, accounts, email addresses, keys or Git authors alone do
not yield distinct principals; identical strings in unrelated namespaces do
not establish equality.

The namespace must specify whether it denotes a pseudonymous human actor,
another recognized principal kind, or an organizational role. A human executor
must not become a different human merely by changing roles or delegating an
account. This draft does not choose account equality, legal-person equality or
a new identity registry as C3 semantics. Stable pseudonymous references and
rule-scoped evidence are possible; extra-systemic entitlement and action
authority are separate questions.

[OPEN] No admitted tool/human binding path or live tool/human invocation evidence
is available in the inspected repository. The first implementation may validate
synthetic fixtures and return unresolved for unsupported live inputs. Enabling
a real binding profile requires review of its specific rule, namespace, issuer/
witness evidence and limitations; a caller-supplied established flag is not a
profile. Model catalog evidence classes are not imported into these kinds.

## 7. Cross-kind choice and superclass deferral

[ALG] Proposed semantic recommendation: keep model/tool, model/human and
tool/human comparisons unresolved in both orders until a separate applicable
cross-kind rule is justified and admitted. Preserve the current enumerated
no-cross-kind-rule reason.

| Alternative | Assessment |
| --- | --- |
| Different kind implies non-equivalent | Unsupported: tags are representation, and wrappers can hide the same influencing executor |
| Flatten every composite to its leaf executor | Unsupported: an invocation can involve several material executors and external action surfaces |
| Keep unresolved, disclose composition, require directional evidence | Recommended conservative boundary; does not assert that the kinds are equal |

A tool invoking a model must disclose the subordinate invocation. That disclosure
does not itself establish an ancestry edge: C12 requires directional influence.
A human instructing a tool is likewise not reduced to a kind-tag comparison.

Defer ExecutorIdentity superclass introduction. The current kind-tagged
representation can express a proposed dispatch contract without deciding a new
inheritance hierarchy. A future proposal must demonstrate an unrepresentable
requirement or concrete failure, compatibility impact and falsifiers; identity
must remain distinct from invocation/runtime instance.

## 8. Executable C3/C10 evidence conditions — specification only

[ALG] These are proposed input/output contracts for future condition evaluators,
not implemented enforcement or a new IndependenceAssessment.

**C3 input:** named adjudicating invocation and target/claim; applicable evidence
manifest; directional ancestry paths plus coverage by every applicable edge
class; per-ancestor executor relation/binding assessments; rule versions and
remaining uncertainty.

**C3 result:** a direct lineage conflict is a hard refusal. An equivalent
ancestor identity refuses under the present rule. Any unresolved relevant
relation, hidden inherited state or incomplete/non-connectable applicable edge
coverage produces unresolved qualification and blocks adjudication. Only a
complete, positively supported assessment can report the named C3 conditions
satisfied; it cannot output an authorization grant. An empty path list alone
is insufficient.

**C10 input:** exact VerificationRun and reviewed property; verifier
identity/version, rule/test version, content-addressed inputs, environment and
result; producer ModelIdentity; ancestry/coverage for verifier code, schema,
tests and configuration; any review artifact with exact-run coverage.

**C10 result:** established shared ancestry retains self-authored standing.
Incomplete ancestry cannot produce independent standing. A review-based
self_authored_with_review finding requires every §4.17 condition, including
identified reviewer, no unresolved/disqualified independence dimension, exact
coverage and positive outcome. Present C10 producer semantics name ModelIdentity;
extension to another producer kind is a separate normative decision.

[GAP-0008](../../self_model/gaps/GAP-0008.json) remains the structural dependency
for positive qualification needing missing composition/traversal/coverage.
C5's information path, source, executor identity, provider/organization
correlation, prompt common cause, session-state confidence and claim-lineage
completeness remain separate. No enum upgrade, capability promotion or
retrospective qualification follows from this contract or its future unit tests.

## 9. Decisions required before implementation admission

[OPEN] The subsequent review must freeze these choices against the exact
candidate revision:

| ID | Proposed choice / unresolved admission item |
| --- | --- |
| D1 | Endpoint binding path, alias policy and event-time availability/freshness rules |
| D2 | All-applicable-target agreement; relevant conflict/ambiguity/undetermined applicability blocks; proven irrelevant sources do not veto |
| D3 | Per-side support sets and scoped corroboration witnesses, without ranking or rewriting evidence classes |
| D4 | Tool identity/version namespace, release/execution binding rule and enabled-profile limits |
| D5 | Human principal semantics, reference/event-actor binding rule, alias/distinctness and enabled-profile limits |
| D6 | Cross-kind unresolved recommendation; separate later rule required for any resolving alternative |
| D7 | No superclass now; concrete necessity evidence required to revisit |
| D8 | Condition-result/legacy-adapter boundary, invalid-input behavior, ancestry dependency and append-only migration |

Validation scenarios are specified in [FALSIFICATION-MATRIX.md](FALSIFICATION-MATRIX.md).
The [PLAN draft](STEP-3-PLAN-DRAFT.md) separates this proposal, later admission,
implementation and subsequent verification/completion.
