# COMP-0136: Provider Comparison — v9.1 re-review R2 do-the-eleven-limitations-do-work

## Metadata

- comparison_id: `COMP-0136`
- title: `v9.1 re-review R2 do-the-eleven-limitations-do-work`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-95bffbc0a863a743.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0136", "target_id": "INV-95bffbc0a863a743"}, {"authoritative": false, "evidence": "docs/invocations/INV-5eeba9dca9477f00.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0136", "target_id": "INV-5eeba9dca9477f00"}]`
- created_at: `2026-08-11T14:15:50.084740+00:00`
- command: `scripts/compare_providers.py --title v9.1 re-review R2 do-the-eleven-limitations-do-work You are reviewing a proposed ontology amendment. This is ONE question of five, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9.1 is proposed and not admitted. v4 is the last version with an admission event. v9.1 has no governance force.

Disclosures:

1. v9.1 is the CORRECTED successor to v9. A prior round, COMP-0126 to COMP-0134, found eight defects in v9; all eight were accepted by the operator and answered. You are reviewing the answers, not the original. Do not assume a correction is sound because it was made in response to a finding.

2. THIS IS A RE-RUN. Each of these five questions was asked of v9 and returned an answer qualified by insufficient evidence. The evidence sets were the question author's choices, and they were wrong. If this evidence set is still insufficient, say so and name precisely what is missing; that report is wanted output and the last round's version of it is why this round exists.

3. The executor that drafted v9, the corrections, and the version bump self-reports as gpt-5.6-thinking. One reviewer slot in this round is gpt-5.6-terra. The provider's own catalog asserts these are distinct model identities, and that catalog is a provider self-report. Nothing establishes whether they are the same executor. Under the corrected C3 you are reading, an invocation may not adjudicate a claim whose evidence ancestry contains an executor of unresolved equivalence. Your output is evidence for the accountable principal, not an adjudication.

4. The question author drafted ABS-0004 v5 through v8, all withdrawn or superseded, and drafted none of v9 or v9.1.

Answer in whatever form fits, but include three things: a VERDICT SENTENCE before the reasoning; any evidence you needed and did not have; and anything you found that this question did not ask about.

Quote only text that appears below. Do not certify or praise. No provider product recommendations.

=== QUESTION R2 ===
The v9 round asked whether the limitation statements do work or wrap failures in accurate disclaimers. Four of nine were supplied and the answer was qualified accordingly. All eleven now in v9.1 are below, with the sections that carry most of them.

A prior synthesis characterised v8's failure mode as: a failed control retained in control-shaped language, wrapped in an accurate disclaimer, and delegated to a future mechanism or a careful reader.

Go statement by statement. For each, say what a reader could do differently because it is present, and what would be lost if it were deleted. Distinguish those that constrain how the ontology may be described from those that merely record an absence. If the set as a whole substitutes disclosure for remedy, say so.

=== EVIDENCE All 11 [LIMITATION] statements in v9.1 ===
`[LIMITATION]` descriptive boundary on what the ontology, its
  records, or current enforcement establish. A

`[LIMITATION]`

`[LIMITATION]` A verification result supports only the property it names. It
does not by itself justify a broader epistemic status or establish truth,
grounding, calibration, privacy, or any other unverified property.

`[LIMITATION]` Distinct identifiers, endpoints, or invocation records do not by themselves
establish distinct executor identities. When executor-kind-specific
equivalence cannot be resolved, independence remains unresolved.

`[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and
authorization records can state and attribute authority claims. Repository
records do not by themselves establish a principal's extra-systemic
entitlement to govern.

`[LIMITATION]` A recorded authorization-chain terminus identifies where the
represented chain stops. It does not by itself establish that the underlying
invocation is substantively authorized.

`[LIMITATION]` Record and relation requirements expose only what was declared,
recorded, linked, traversable, and correctly attributed. They do not establish
that every material invocation, authorization, input, dependency, or external
interaction is present in the record.

`[LIMITATION]` InvocationRecord schema v1 accepts `verified`, but no admitted
schema-v1 capture path can presently substantiate it: the current path performs
no identity resolution, and provider catalog self-report, even over an
authenticated channel, does not independently establish a model mapping. It
therefore emits `unresolved`. Later append-only identity resolution records do
not mutate or upgrade this field; validator acceptance of `verified` is
syntactic compatibility, not a licensed status.

`[LIMITATION]` One artifact may mix original observation, copied finding, new
inference, and paraphrase; artifact-level lineage cannot distinguish them.
Until claim-level derivation exists, the system provides artifact-level
potential-dependence detection, not claim-level independence proof; Section 7
imposes the conservative inheritance this gap requires, and C11 imposes the
interim high-consequence disclosure this gap requires.

`[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does
not establish that a policy was active, applicable, evaluated, or enforced for
a decision. AuthorizationPolicy enforcement remains deferred.

`[LIMITATION]` Role, qualification, and authorization records are inputs to a
C6 evaluation. Their existence does not establish that the C6 exercise
restriction was evaluated or satisfied for a particular invocation.

=== EVIDENCE Section 3, Three Decisions ===
## 3. Three Decisions

`[DEF]` The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

`[DEF]` A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

`[PROPOSED_CONSTRAINT]` Subordinate authorization inheritance: a subordinate
invocation is covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

`[OPEN]` Authorization-chain bootstrap: how an authorization chain terminates
in a standing policy, delegated authority, or AccountablePrincipal authority
scope rather than requiring an infinite sequence of prior authorizations.

`[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and
authorization records can state and attribute authority claims. Repository
records do not by themselves establish a principal's extra-systemic
entitlement to govern.

`[LIMITATION]` A recorded authorization-chain terminus identifies where the
represented chain stops. It does not by itself establish that the underlying
invocation is substantively authorized.

`[LIMITATION]` Record and relation requirements expose only what was declared,
recorded, linked, traversable, and correctly attributed. They do not establish
that every material invocation, authorization, input, dependency, or external
interaction is present in the record.

=== EVIDENCE Section 9, Enforcement Matrix ===
## 9. Enforcement Matrix

`[DEF]` The matrix separates three questions that do not imply one another.
Governance status is `proposed-v9` or `inherited-v4` and records the source of
normative force. Claimed enforcement mode is `none`, `manual`, or `machine` and
records what enforcement mode the document says is presently used. Enforcement
evidence is `none`, a named retained artifact instance, or machine evidence and
records what evidence exists that the applicable check occurred for a named
target. Representability is `none` | `partial` | `full`. A manual enforcement
claim counts as evidenced only when a specific retained artifact attests the
applicable check for a named target. An artifact class, an input record, or the
claim that a check happens is not enforcement evidence.

| Constraint | Governance status | Claimed enforcement mode | Enforcement evidence | Representability | Target enforcement | Activation condition | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 staged provenance | proposed-v9 | none | none | none | validator per profile | profile activation decision after capability ships | invocation records; manifests; profiles |
| C2 catalog admission | proposed-v9 | none | none | none | validator + runtime gate | catalog capability ships | catalog snapshots; identities; qualifications |
| C3 no self-adjudication (executor-generic) | proposed-v9 | manual | none; `WARR-20260719-0002` is not C3 evidence | partial | per-kind equivalence check + lineage traversal | manual use is claimed; evidence begins only with a named C3 attestation for a named adjudication | ancestry capture; executor-equivalence semantics |
| C4 hidden witness reuse | proposed-v9 | none | none | none | context-lineage inspection | lineage capability ships | manifests; ancestry |
| C5 lineage independence | proposed-v9 | none | none | none | categorical assessment with reasons | lineage capability ships | ancestry; claim lineage |
| C6 authority separation | inherited-v4 | manual | none; role records are inputs to C6 evaluation, not evidence that it occurred | partial | artifact validator | manual practice is claimed; evidence begins only with a named C6 evaluation for a named invocation | role records |
| C7 implementation separation | inherited-v4 | manual | none; existing VERIFY records show verification activity but do not attest a C7 implementation-separation check for a named change | partial | validator on VERIFY records | manual practice is claimed; evidence begins only with a named C7 attestation | none; strengthened later |
| C8 decision traceability | proposed-v9 | none | none | none | RoutingDecision validation | routing capability ships | routing records |
| C9 lineage inheritance | inherited-v4 | manual | none; no named artifact instance currently attests a C9 inheritance check for a named target | partial | inheritance propagation | manual practice is claimed; evidence begins only with a named C9 attestation | claim lineage (full) |
| C10 validator lineage | inherited-v4 | manual | none; VERIFY records name verification activity, but no named retained artifact currently establishes the C10 lineage-independence check for a named verification | partial | VerificationRun with verifier-ancestry check | manual practice is claimed; evidence begins only with a named C10 attestation | ancestry capture |
| C11 interim independence disclosure | inherited-v4 | manual | none; no named DecisionRecord or warrant instance currently attests the C11 disclosure check for a named high-consequence decision | partial | admission validator requiring disclosure + named controls | manual practice is claimed; evidence begins only with a named C11 attestation | none; retired when claim lineage ships |

--- END OF EVIDENCE ---

Answer only the question above.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are reviewing a proposed ontology amendment. This is ONE question of five, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9.1 is proposed and not admitted. v4 is the last version with an admission event. v9.1 has no governance force.

Disclosures:

1. v9.1 is the CORRECTED successor to v9. A prior round, COMP-0126 to COMP-0134, found eight defects in v9; all eight were accepted by the operator and answered. You are reviewing the answers, not the original. Do not assume a correction is sound because it was made in response to a finding.

2. THIS IS A RE-RUN. Each of these five questions was asked of v9 and returned an answer qualified by insufficient evidence. The evidence sets were the question author's choices, and they were wrong. If this evidence set is still insufficient, say so and name precisely what is missing; that report is wanted output and the last round's version of it is why this round exists.

3. The executor that drafted v9, the corrections, and the version bump self-reports as gpt-5.6-thinking. One reviewer slot in this round is gpt-5.6-terra. The provider's own catalog asserts these are distinct model identities, and that catalog is a provider self-report. Nothing establishes whether they are the same executor. Under the corrected C3 you are reading, an invocation may not adjudicate a claim whose evidence ancestry contains an executor of unresolved equivalence. Your output is evidence for the accountable principal, not an adjudication.

4. The question author drafted ABS-0004 v5 through v8, all withdrawn or superseded, and drafted none of v9 or v9.1.

Answer in whatever form fits, but include three things: a VERDICT SENTENCE before the reasoning; any evidence you needed and did not have; and anything you found that this question did not ask about.

Quote only text that appears below. Do not certify or praise. No provider product recommendations.

=== QUESTION R2 ===
The v9 round asked whether the limitation statements do work or wrap failures in accurate disclaimers. Four of nine were supplied and the answer was qualified accordingly. All eleven now in v9.1 are below, with the sections that carry most of them.

A prior synthesis characterised v8's failure mode as: a failed control retained in control-shaped language, wrapped in an accurate disclaimer, and delegated to a future mechanism or a careful reader.

Go statement by statement. For each, say what a reader could do differently because it is present, and what would be lost if it were deleted. Distinguish those that constrain how the ontology may be described from those that merely record an absence. If the set as a whole substitutes disclosure for remedy, say so.

=== EVIDENCE All 11 [LIMITATION] statements in v9.1 ===
`[LIMITATION]` descriptive boundary on what the ontology, its
  records, or current enforcement establish. A

`[LIMITATION]`

`[LIMITATION]` A verification result supports only the property it names. It
does not by itself justify a broader epistemic status or establish truth,
grounding, calibration, privacy, or any other unverified property.

`[LIMITATION]` Distinct identifiers, endpoints, or invocation records do not by themselves
establish distinct executor identities. When executor-kind-specific
equivalence cannot be resolved, independence remains unresolved.

`[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and
authorization records can state and attribute authority claims. Repository
records do not by themselves establish a principal's extra-systemic
entitlement to govern.

`[LIMITATION]` A recorded authorization-chain terminus identifies where the
represented chain stops. It does not by itself establish that the underlying
invocation is substantively authorized.

`[LIMITATION]` Record and relation requirements expose only what was declared,
recorded, linked, traversable, and correctly attributed. They do not establish
that every material invocation, authorization, input, dependency, or external
interaction is present in the record.

`[LIMITATION]` InvocationRecord schema v1 accepts `verified`, but no admitted
schema-v1 capture path can presently substantiate it: the current path performs
no identity resolution, and provider catalog self-report, even over an
authenticated channel, does not independently establish a model mapping. It
therefore emits `unresolved`. Later append-only identity resolution records do
not mutate or upgrade this field; validator acceptance of `verified` is
syntactic compatibility, not a licensed status.

`[LIMITATION]` One artifact may mix original observation, copied finding, new
inference, and paraphrase; artifact-level lineage cannot distinguish them.
Until claim-level derivation exists, the system provides artifact-level
potential-dependence detection, not claim-level independence proof; Section 7
imposes the conservative inheritance this gap requires, and C11 imposes the
interim high-consequence disclosure this gap requires.

`[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does
not establish that a policy was active, applicable, evaluated, or enforced for
a decision. AuthorizationPolicy enforcement remains deferred.

`[LIMITATION]` Role, qualification, and authorization records are inputs to a
C6 evaluation. Their existence does not establish that the C6 exercise
restriction was evaluated or satisfied for a particular invocation.

=== EVIDENCE Section 3, Three Decisions ===
## 3. Three Decisions

`[DEF]` The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

`[DEF]` A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

`[PROPOSED_CONSTRAINT]` Subordinate authorization inheritance: a subordinate
invocation is covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

`[OPEN]` Authorization-chain bootstrap: how an authorization chain terminates
in a standing policy, delegated authority, or AccountablePrincipal authority
scope rather than requiring an infinite sequence of prior authorizations.

`[LIMITATION]` AccountablePrincipal, `authority_scope`, delegation, and
authorization records can state and attribute authority claims. Repository
records do not by themselves establish a principal's extra-systemic
entitlement to govern.

`[LIMITATION]` A recorded authorization-chain terminus identifies where the
represented chain stops. It does not by itself establish that the underlying
invocation is substantively authorized.

`[LIMITATION]` Record and relation requirements expose only what was declared,
recorded, linked, traversable, and correctly attributed. They do not establish
that every material invocation, authorization, input, dependency, or external
interaction is present in the record.

=== EVIDENCE Section 9, Enforcement Matrix ===
## 9. Enforcement Matrix

`[DEF]` The matrix separates three questions that do not imply one another.
Governance status is `proposed-v9` or `inherited-v4` and records the source of
normative force. Claimed enforcement mode is `none`, `manual`, or `machine` and
records what enforcement mode the document says is presently used. Enforcement
evidence is `none`, a named retained artifact instance, or machine evidence and
records what evidence exists that the applicable check occurred for a named
target. Representability is `none` | `partial` | `full`. A manual enforcement
claim counts as evidenced only when a specific retained artifact attests the
applicable check for a named target. An artifact class, an input record, or the
claim that a check happens is not enforcement evidence.

| Constraint | Governance status | Claimed enforcement mode | Enforcement evidence | Representability | Target enforcement | Activation condition | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 staged provenance | proposed-v9 | none | none | none | validator per profile | profile activation decision after capability ships | invocation records; manifests; profiles |
| C2 catalog admission | proposed-v9 | none | none | none | validator + runtime gate | catalog capability ships | catalog snapshots; identities; qualifications |
| C3 no self-adjudication (executor-generic) | proposed-v9 | manual | none; `WARR-20260719-0002` is not C3 evidence | partial | per-kind equivalence check + lineage traversal | manual use is claimed; evidence begins only with a named C3 attestation for a named adjudication | ancestry capture; executor-equivalence semantics |
| C4 hidden witness reuse | proposed-v9 | none | none | none | context-lineage inspection | lineage capability ships | manifests; ancestry |
| C5 lineage independence | proposed-v9 | none | none | none | categorical assessment with reasons | lineage capability ships | ancestry; claim lineage |
| C6 authority separation | inherited-v4 | manual | none; role records are inputs to C6 evaluation, not evidence that it occurred | partial | artifact validator | manual practice is claimed; evidence begins only with a named C6 evaluation for a named invocation | role records |
| C7 implementation separation | inherited-v4 | manual | none; existing VERIFY records show verification activity but do not attest a C7 implementation-separation check for a named change | partial | validator on VERIFY records | manual practice is claimed; evidence begins only with a named C7 attestation | none; strengthened later |
| C8 decision traceability | proposed-v9 | none | none | none | RoutingDecision validation | routing capability ships | routing records |
| C9 lineage inheritance | inherited-v4 | manual | none; no named artifact instance currently attests a C9 inheritance check for a named target | partial | inheritance propagation | manual practice is claimed; evidence begins only with a named C9 attestation | claim lineage (full) |
| C10 validator lineage | inherited-v4 | manual | none; VERIFY records name verification activity, but no named retained artifact currently establishes the C10 lineage-independence check for a named verification | partial | VerificationRun with verifier-ancestry check | manual practice is claimed; evidence begins only with a named C10 attestation | ancestry capture |
| C11 interim independence disclosure | inherited-v4 | manual | none; no named DecisionRecord or warrant instance currently attests the C11 disclosure check for a named high-consequence decision | partial | admission validator requiring disclosure + named controls | manual practice is claimed; evidence begins only with a named C11 attestation | none; retired when claim lineage ships |

--- END OF EVIDENCE ---

Answer only the question above.

## OpenAI Response

- model: `gpt-5.6-terra`

```
**VERDICT:** The substantive limitation statements constrain some inferences and descriptions, but they do not remedy the disclosed control gaps; read with the enforcement matrix, the set substantially functions as disclosure of absent or unevidenced enforcement rather than as an operative remedy.

The supplied list contains nine substantive limitation propositions, plus one descriptive preface and one empty `[LIMITATION]` entry. Thus, there are not eleven assessable limitation statements in the text provided.

| Supplied statement | What a reader can do differently because it is present | What deletion would lose | Character |
|---|---|---|---|
| “descriptive boundary on what the ontology, its records, or current enforcement establish.” | Treat the label as a boundary on what claims may be made from ontology records and enforcement descriptions. | The stated interpretive function of `[LIMITATION]` as a category. | Constrains description, but is only a heading fragment, not a complete proposition. |
| Empty `[LIMITATION]` | Nothing. | Nothing textual. | Neither a constraint nor an absence record. |
| “A verification result supports only the property it names.” | Avoid treating a verification result as proof of “truth, grounding, calibration, privacy,” or other unnamed properties. | An explicit prohibition on epistemic overextension from verification. | Constrains how verification may be described and relied upon. It does not cause a verification to test additional properties. |
| “Distinct identifiers, endpoints, or invocation records do not by themselves establish distinct executor identities.” | Avoid inferring independent executors from differing identifiers or records; retain unresolved independence where equivalence cannot be resolved. | The explicit warning that identifier distinction is not identity distinction, and that unresolved equivalence leaves independence unresolved. | Constrains identity and independence claims. It does not resolve equivalence. |
| “AccountablePrincipal, `authority_scope`, delegation, and authorization records can state and attribute authority claims.” | Describe authority records as records of claims and attribution, rather than proof of “extra-systemic entitlement to govern.” | The distinction between represented authority claims and substantive entitlement. | Constrains descriptions of authority. It records a boundary, not a mechanism for establishing entitlement. |
| “A recorded authorization-chain terminus identifies where the represented chain stops.” | Avoid calling a chain terminus proof that an invocation was substantively authorized. | The distinction between a represented stopping point and underlying authorization. | Constrains authorization descriptions. It records that substantive authorization remains unestablished. |
| “Record and relation requirements expose only what was declared, recorded, linked, traversable, and correctly attributed.” | Avoid treating repository completeness or traversability as proof that all material invocations, inputs, dependencies, authorizations, and interactions are recorded. | An explicit completeness limitation on the repository and its relation requirements. | Constrains completeness claims. It does not discover omitted material. |
| “InvocationRecord schema v1 accepts `verified`, but no admitted schema-v1 capture path can presently substantiate it.” | Treat `verified` as syntactically accepted but not presently licensed by the described capture path; expect `unresolved`; do not treat later identity records as upgrades of the original field. | Several specific operational boundaries: no current identity resolution; provider catalog self-report does not independently establish model mapping; later append-only records do not upgrade the field; and validator acceptance is not licensed status. | Both a description constraint and an absence record. It does not supply an identity-resolution path or make `verified` substantively available. |
| “One artifact may mix original observation, copied finding, new inference, and paraphrase; artifact-level lineage cannot distinguish them.” | Do not infer claim-level independence from artifact-level lineage; apply the stated conservative inheritance and high-consequence disclosure pending claim-level derivation. | The reason artifact-level potential-dependence detection is not claim-level independence proof, and the stated interim consequences of that gap. | Constrains lineage and independence claims; also records an absent claim-level derivation capability. It delegates the remedy to a future capability and interim disclosure/inheritance rules. |
| “Defining AuthorizationPolicy and requiring typed references does not establish that a policy was active, applicable, evaluated, or enforced for a decision.” | Avoid treating policy definition or typed references as proof of policy operation or enforcement in a particular decision. | The explicit distinction between policy representation and active, applicable, evaluated, enforced policy. | Both a description constraint and an absence record: “AuthorizationPolicy enforcement remains deferred.” It supplies no current enforcement. |
| “Role, qualification, and authorization records are inputs to a C6 evaluation.” | Avoid treating the existence of role, qualification, or authorization records as evidence that a C6 exercise restriction was evaluated or satisfied for an invocation. | The distinction between inputs to C6 and a completed C6 evaluation for a named invocation. | Both a description constraint and an absence record of evaluation evidence. It does not perform or attest the C6 evaluation. |

The enforcement matrix reinforces the distinction between these limitations and remedies. For the relevant matters, it repeatedly states “none” for enforcement evidence, or says that evidence begins only with a named attestation for a named target. In particular:

- C3 has “manual” claimed enforcement but “none” as enforcement evidence.
- C6 has “manual” claimed enforcement but “none” as enforcement evidence.
- C11 has “manual” claimed enforcement but “none” as enforcement evidence.
- Several proposed controls have no claimed enforcement and no enforcement evidence.

Accordingly, the statements can prevent particular inaccurate descriptions—for example, calling a syntactically accepted field a licensed status, calling records proof of substantive authorization, or calling artifact lineage proof of claim independence. That is real limiting work at the level of permitted inference. But they do not create identity resolution, claim-level derivation, policy enforcement, substantive authorization, C6 evaluation, or named enforcement evidence. Where the corresponding control is not operational or not evidenced, the limitation is disclosure of that failure or absence, not its remedy.

**Evidence needed and not provided:** No additional evidence is needed to identify the textual effects and deletion losses above. However, the supplied text does not establish the factual accuracy of assertions such as “the current path performs no identity resolution,” “no admitted schema-v1 capture path can presently substantiate” `verified`, “AuthorizationPolicy enforcement remains deferred,” or that no named C6/C11 attestations exist. To determine whether those disclosures are accurate, the missing evidence would include the admitted schema-v1 capture-path specification and implementation records, identity-resolution procedure and retained outputs, policy-enforcement implementation and execution evidence, and the repository inventory of relevant named attestations and DecisionRecords.

**Not asked, but found:** The asserted set of eleven includes only nine substantive limitation propositions. One item is a category-description fragment, and one is empty. Repetition of three limitations in Section 3 does not create additional statements. Also, the enforcement matrix labels several rows “proposed-v9,” while the supplied status states that v9.1 is proposed and has no governance force; the matrix therefore does not itself establish operative force for the proposed controls.
```

## Claude Response

- model: `claude-sonnet-5`

```
**VERDICT SENTENCE:** Of the eleven [LIMITATION] statements, two (L1, L2) are textually broken and cannot be assessed at all, one (L8) does genuine constraining work on system behavior, and the remaining eight are accurate disclaimers that record an absence without altering what the ontology permits or does — several of them (most clearly the lineage statement, L9) explicitly delegate the gap to a future mechanism or a control (C11) that the Enforcement Matrix in the same evidence set shows has zero enforcement evidence — so the set as a whole substitutes disclosure for remedy, with L8 as the sole exception.

---

**Statement-by-statement**

L1 — `"descriptive boundary on what the ontology, its records, or current enforcement establish. A"`
Truncated mid-sentence, ends on an orphan "A." Cannot say what a reader could do differently or what would be lost — the content is missing, not present. This is a defect, not a limitation.

L2 — `[LIMITATION]` (no text follows)
Empty. Same conclusion: unassessable. Cannot be counted as doing "work" or "disclaiming" anything because there is nothing there.

L3 — verification result supports only the named property.
Constrains description: forbids inflating a verified-X claim into truth/grounding/calibration/privacy claims. A reader can cite this to reject scope-creep arguments. If deleted: nothing in the ontology would forbid such inflation elsewhere, so the boundary would be lost. This is a real (if narrow) constraint on permissible claims, not merely a record of absence — though it constrains speech about evidence, not the evidence itself.

L4 — distinct identifiers don't establish distinct executor identities; unresolved equivalence stays unresolved.
Records an absence (no resolution mechanism exists) but is invoked by C3's adjudication bar (per Disclosure 3). Reader can use it to block an identity claim resting only on distinct endpoints/IDs. If deleted: the definitional predicate that C3 depends on for "unresolved" would lose its source text, though C3's matrix row already shows enforcement evidence is `none` regardless — so the constraint exists on paper only, per this same evidence set.

L5 — authority/delegation records can state claims but do not establish extra-systemic entitlement to govern.
Pure absence-recording. Nothing a reader can *do* differently operationally; it only tells them not to over-read a repository record as proof of legitimate authority. Deleting it removes a warning, not a mechanism.

L6 — authorization-chain terminus doesn't establish substantive authorization.
Same pattern as L5, and it sits directly beside the still-`[OPEN]` "Authorization-chain bootstrap" item in Section 3 — the underlying problem (how a chain terminates legitimately) is unresolved, not merely disclaimed. Deleting L6 loses the warning; it does not lose a control, because there is no control here to lose.

L7 — record/relation completeness claims don't establish that every material item is present.
Absence-recording. Tells a reader not to treat traceability as completeness. Nothing changes operationally if deleted except the warning disappears.

L8 — InvocationRecord schema forces `unresolved` output, blocks later upgrade to `verified`, denies that validator acceptance is a "licensed status."
This is the one statement that does real constraining work: it specifies an actual required field behavior and forecloses a specific future workaround (mutating the field via later identity-resolution records). A reader/implementer is barred from treating catalog self-report or later append-only records as sufficient to flip the field. If deleted, nothing would stop a future implementation from quietly treating `verified` as meaningful once *any* identity-resolution record appears — a real regression, not just loss of a disclaimer.

L9 — artifact-level lineage cannot separate observation/copy/inference/paraphrase; "Section 7 imposes... C11 imposes..."
This is the clearest instance of the described failure mode: a named gap (no claim-level derivation) is wrapped in accurate language and handed off to (a) a future mechanism ("until claim-level derivation exists") and (b) two control cross-references. But Section 9's own matrix shows C11's enforcement evidence is `none` ("no named DecisionRecord or warrant instance currently attests the C11 disclosure check"). So the delegation is to a control that, per this evidence, is not presently doing anything. Deleting L9 would lose the disclosure of the gap; it would not lose any remedy, because the remedy it names is itself unevidenced.

L10 — defining AuthorizationPolicy and requiring typed references doesn't establish the policy was active/applicable/evaluated/enforced.
Absence-recording, matching the general "enforcement deferred" pattern seen throughout Section 9 (C1, C2, C4, C5, C8 are all `none`/`none`/`none`). Nothing for a reader to do differently; deletion loses only the warning.

L11 — role/qualification records are inputs to C6, not evidence C6 occurred.
This restates, almost verbatim, the C6 row in the Enforcement Matrix ("role records are inputs to C6 evaluation, not evidence that it occurred"). It is disclosure duplicating an already-admitted enforcement gap, not an additional constraint. Deleting it loses nothing that Section 9 doesn't already say.

**Constrain-vs-record split:** L3 and L8 constrain what may be claimed or how the system must behave. L4, L5, L6, L7, L9, L10, L11 merely record an absence of proof, several tracking gaps the document elsewhere admits are unenforced (C6, C9, C10, C11 all show enforcement evidence `none` in Section 9). L1 and L2 are indeterminate.

**Does the set substitute disclosure for remedy?** Yes, overwhelmingly. Nine of eleven statements either record absence with no operative effect or explicitly hand the gap to a not-yet-evidenced control or a future mechanism ("until claim-level derivation exists"). Only L8 forecloses an actual workaround. This matches the named v8 failure pattern — control-shaped language, accurate disclaimer, delegation to a future mechanism — reproduced almost exactly in L9's reference to Section 7/C11.

---

**Evidence needed and not had:** Full text of Section 4.7 (disclosure-violation definition referenced by the subordinate-authorization constraint), Section 7 (the "conservative inheritance" L9 relies on), Section 4.13 (DecisionRecord kinds), the content of `WARR-20260719-0002` (cited in the C3 row as *not* C3 evidence — what it actually is remains unstated), and the COMP-0126–0134 defect/answer texts, which would show whether any of these eleven limitation statements were themselves among the eight "corrected" defects or are unaltered holdovers from v9.

**Found but not asked about:** L1 and L2 are broken (truncated and empty respectively) in the evidence as supplied — a defect in v9.1's limitation section itself, independent of whether the surviving statements do useful work. Also worth noting: this review's own evidence-ancestry question (Disclosure 3, gpt-5.6-thinking vs. gpt-5.6-terra) is a live instance of exactly what L4 and C3 describe — an executor-equivalence question left unresolved — meaning the mechanism L4 disclaims may bear on the standing of this very output, not merely on the ontology's subject matter.
```
