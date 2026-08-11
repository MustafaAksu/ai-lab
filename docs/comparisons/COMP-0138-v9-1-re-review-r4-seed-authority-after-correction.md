# COMP-0138: Provider Comparison — v9.1 re-review R4 seed-authority-after-correction

## Metadata

- comparison_id: `COMP-0138`
- title: `v9.1 re-review R4 seed-authority-after-correction`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-a60e19cf9d822fff.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0138", "target_id": "INV-a60e19cf9d822fff"}, {"authoritative": false, "evidence": "docs/invocations/INV-3b87d93d2283af23.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0138", "target_id": "INV-3b87d93d2283af23"}]`
- created_at: `2026-08-11T14:17:56.239842+00:00`
- command: `scripts/compare_providers.py --title v9.1 re-review R4 seed-authority-after-correction You are reviewing a proposed ontology amendment. This is ONE question of five, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9.1 is proposed and not admitted. v4 is the last version with an admission event. v9.1 has no governance force.

Disclosures:

1. v9.1 is the CORRECTED successor to v9. A prior round, COMP-0126 to COMP-0134, found eight defects in v9; all eight were accepted by the operator and answered. You are reviewing the answers, not the original. Do not assume a correction is sound because it was made in response to a finding.

2. THIS IS A RE-RUN. Each of these five questions was asked of v9 and returned an answer qualified by insufficient evidence. The evidence sets were the question author's choices, and they were wrong. If this evidence set is still insufficient, say so and name precisely what is missing; that report is wanted output and the last round's version of it is why this round exists.

3. The executor that drafted v9, the corrections, and the version bump self-reports as gpt-5.6-thinking. One reviewer slot in this round is gpt-5.6-terra. The provider's own catalog asserts these are distinct model identities, and that catalog is a provider self-report. Nothing establishes whether they are the same executor. Under the corrected C3 you are reading, an invocation may not adjudicate a claim whose evidence ancestry contains an executor of unresolved equivalence. Your output is evidence for the accountable principal, not an adjudication.

4. The question author drafted ABS-0004 v5 through v8, all withdrawn or superseded, and drafted none of v9 or v9.1.

Answer in whatever form fits, but include three things: a VERDICT SENTENCE before the reasoning; any evidence you needed and did not have; and anything you found that this question did not ask about.

Quote only text that appears below. Do not certify or praise. No provider product recommendations.

=== QUESTION R4 ===
One party drafts the root records, approves them, activates them, and relies on them as the terminus of every authorization chain. The version admission table records that v4 was admitted "by the operator as accountable principal in session, recorded in conversation only", and that no admission warrant exists for any amendment.

The v9 round found that the ontology does not distinguish that arrangement from one in which the seed is fabricated, and that AccountablePrincipal permits a pseudonymous identity with no required external anchor. Nothing in the A1 to A8 corrections addressed this.

Say whether that finding still holds against the text below. If it does, state what a record would have to contain to make the distinction, and whether such a record could exist inside the repository at all. Do not treat the operator's actual trustworthiness as evidence; the question is what the ontology represents.

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

=== EVIDENCE Section 4.13, DecisionRecord and AccountablePrincipal ===
### 4.13 DecisionRecord and AccountablePrincipal

`[DEF]` DecisionRecord: `decision_kind` (invocation_authorization |
routing_selection | evidence_admission | manual_override), target,
`recommended_status` and `effective_status` (distinct: a model
recommendation must not appear to have assigned final status before
accountable approval), issuer invocation, accountable approver, evidence,
policy authority, activation state, supersession. `[OPEN]` Whether existing
warrant/admission records are extended to fulfill this or a new record
family is created, and whether kinds are subtypes or one record family.

`[DEF]` InvocationAuthorization (decision_kind invocation_authorization)
additionally carries: invocation request, authorized executor, assigned
role, consequence class, applicable policy, qualifications relied on,
independence requirements, conditions. Without this kind, P1 is not
represented by the ontology.

`[DEF]` RoutingDecision (decision_kind routing_selection) additionally
carries: candidates considered, rejection reasons including lineage
conflicts, selected candidate, policy version, catalog snapshot. Tier
labels are policy-derived under current evidence, never intrinsic
ModelIdentity attributes.

`[DEF]` EvidenceAdmissionDecision (decision_kind evidence_admission)
additionally carries: admitted artifact or claim, admitted epistemic
status, lineage and independence findings relied on, disclosed provenance
limitations, and an enumeration of verified properties against the
receiving role's `required_verified_properties`; admission may not treat a
property as established that no named verification record covers.

`[DEF]` AccountablePrincipal: `principal_id`, `principal_kind` (delegated
role, governance body, pseudonymous operator identity, organization, or
other authorized entity), `authority_scope`, `delegation_reference`. No
personal identifying data required. Cryptographic attestation is a later
implementation mechanism, not an ontology requirement.

=== EVIDENCE ABS-0004 v9.1 metadata and version admission table ===

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v9.1`
- abstraction_level: `2`
- status: `proposed`
- reconstruction baseline: admitted v4 at commit
  `56f18a2ab7b66b1855b631a32d540f654c62b2c2`. Assembly does not admit v9.1;
  v9.1 requires its own admission review.
- version admission table:

  | version | state | basis |
  | --- | --- | --- |
  | v1, v2 | superseded during drafting | never entered the record |
  | v3 | superseded | entered the record at 6802cf7; underwent the COMP-0032 challenge round |
  | v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only |
  | v5 | amended, not separately admitted | replaced CatalogVerification with CatalogCapture on the COMP-0035 finding, at 6d7dfee |
  | v6 | amended, not separately admitted; superseded | proposed an authorization-chain termination that both COMP-0037 reviewers broke independently, at 8a1399f |
  | v7 | amended, not separately admitted | replaced v6's termination rule, at 00335d6; reviewed by COMP-0039..0046 |
  | v8 | **withdrawn_after_admission_review** | reviewed by COMP-0118..0125 and withdrawn under DECISION-20260727-0002; retained as evidence, not rejected, and not an implementation authority |
  | v9 | reviewed, not admitted; superseded by corrected v9.1 candidate | reconstructed from admitted v4 and assembled under DECISION-20260805-0002; the text reviewed in COMP-0126..0134 had SHA-256 `8f61c283a5d716f6816798a4946824b2d0d633a8be0d154da33cc1ebbe7ab1fa`; eight findings A1-A8 were accepted under DECISION-20260811-0001, so that reviewed text is not the corrected candidate |
  | v9.1 | **proposed** | corrected successor to the reviewed v9. The corrected pre-version-bump text had SHA-256 `c2dadf897441bf842b34e2b71a347a264401bb228168c4b4214d5964c8d218b0`; it differs from the reviewed v9 because the eight accepted findings A1-A8 were answered by recorded corrections. The v9.1 version/history update records that distinction and does not itself add a ninth substantive correction; pending review of the corrected text |

- reconstruction inputs:
  `ABS-0004-v9-task2-required-changes.patch`,
  `ABS-0004-v9-task3-limitations.patch`,
  `ABS-0004-v9-identity-status.patch`, and
  `ASSEMBLY_RULE_CORRECTION.md`, retained under
  `docs/self_model/v9_reconstruction/`.
- authors: operator (adjudicating principal); inherited v4 text drafted by an
  executor self-reported as "Claude"; v9 reconstruction text and assembly by
  the reviewing executor self-reported as `gpt-5.6-thinking`; both executor
  identities are unverified testimony; with attributed advisor contributions
  described in Evidence Inputs.
- sentence discipline: every normative statement is tagged `[DEF]`
  definition; `[PRINCIPLE]` architectural principle;
  `[PROPOSED_CONSTRAINT]` constraint proposed for adoption;
  `[INHERITED_CONSTRAINT]` constraint text carried forward unchanged from the
  admitted v4 baseline. Its current governance force derives from v4's
  admission, not from the proposed v9 document. A substantive change becomes
  `[PROPOSED_CONSTRAINT]` until separately admitted; `[COMMIT]` commitment
  concerning the preparation of this document; `[PROPOSAL]` candidate
  implementation boundary subject to future governance; `[OPEN]` open
  question; or `[LIMITATION]` descriptive boundary on what the ontology, its
  records, or current enforcement establish. A `[DEF]` introduces a term,
  record shape, relation, or descriptive derivation; it does not by itself
  impose an obligation, prohibition, permission, admission condition, or
  status-changing consequence. A limitation imposes no constraint and claims
  no adoption. Untagged prose binds nothing.
- `[LIMITATION]` `[INHERITED_CONSTRAINT]` establishes textual continuity with
  an admitted v4 constraint; it does not by itself establish semantic identity
  when definitions, vocabularies, relation rules, or other referents used by
  that constraint differ in the proposed version. Such dependencies require
  re-examination before admission.

## Evidence Inputs


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

=== QUESTION R4 ===
One party drafts the root records, approves them, activates them, and relies on them as the terminus of every authorization chain. The version admission table records that v4 was admitted "by the operator as accountable principal in session, recorded in conversation only", and that no admission warrant exists for any amendment.

The v9 round found that the ontology does not distinguish that arrangement from one in which the seed is fabricated, and that AccountablePrincipal permits a pseudonymous identity with no required external anchor. Nothing in the A1 to A8 corrections addressed this.

Say whether that finding still holds against the text below. If it does, state what a record would have to contain to make the distinction, and whether such a record could exist inside the repository at all. Do not treat the operator's actual trustworthiness as evidence; the question is what the ontology represents.

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

=== EVIDENCE Section 4.13, DecisionRecord and AccountablePrincipal ===
### 4.13 DecisionRecord and AccountablePrincipal

`[DEF]` DecisionRecord: `decision_kind` (invocation_authorization |
routing_selection | evidence_admission | manual_override), target,
`recommended_status` and `effective_status` (distinct: a model
recommendation must not appear to have assigned final status before
accountable approval), issuer invocation, accountable approver, evidence,
policy authority, activation state, supersession. `[OPEN]` Whether existing
warrant/admission records are extended to fulfill this or a new record
family is created, and whether kinds are subtypes or one record family.

`[DEF]` InvocationAuthorization (decision_kind invocation_authorization)
additionally carries: invocation request, authorized executor, assigned
role, consequence class, applicable policy, qualifications relied on,
independence requirements, conditions. Without this kind, P1 is not
represented by the ontology.

`[DEF]` RoutingDecision (decision_kind routing_selection) additionally
carries: candidates considered, rejection reasons including lineage
conflicts, selected candidate, policy version, catalog snapshot. Tier
labels are policy-derived under current evidence, never intrinsic
ModelIdentity attributes.

`[DEF]` EvidenceAdmissionDecision (decision_kind evidence_admission)
additionally carries: admitted artifact or claim, admitted epistemic
status, lineage and independence findings relied on, disclosed provenance
limitations, and an enumeration of verified properties against the
receiving role's `required_verified_properties`; admission may not treat a
property as established that no named verification record covers.

`[DEF]` AccountablePrincipal: `principal_id`, `principal_kind` (delegated
role, governance body, pseudonymous operator identity, organization, or
other authorized entity), `authority_scope`, `delegation_reference`. No
personal identifying data required. Cryptographic attestation is a later
implementation mechanism, not an ontology requirement.

=== EVIDENCE ABS-0004 v9.1 metadata and version admission table ===

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v9.1`
- abstraction_level: `2`
- status: `proposed`
- reconstruction baseline: admitted v4 at commit
  `56f18a2ab7b66b1855b631a32d540f654c62b2c2`. Assembly does not admit v9.1;
  v9.1 requires its own admission review.
- version admission table:

  | version | state | basis |
  | --- | --- | --- |
  | v1, v2 | superseded during drafting | never entered the record |
  | v3 | superseded | entered the record at 6802cf7; underwent the COMP-0032 challenge round |
  | v4 | **admitted** 2026-07-20 | twelve adjudicated COMP-0032 findings applied; admitted at 56f18a2 by the operator as accountable principal in session, recorded in conversation only |
  | v5 | amended, not separately admitted | replaced CatalogVerification with CatalogCapture on the COMP-0035 finding, at 6d7dfee |
  | v6 | amended, not separately admitted; superseded | proposed an authorization-chain termination that both COMP-0037 reviewers broke independently, at 8a1399f |
  | v7 | amended, not separately admitted | replaced v6's termination rule, at 00335d6; reviewed by COMP-0039..0046 |
  | v8 | **withdrawn_after_admission_review** | reviewed by COMP-0118..0125 and withdrawn under DECISION-20260727-0002; retained as evidence, not rejected, and not an implementation authority |
  | v9 | reviewed, not admitted; superseded by corrected v9.1 candidate | reconstructed from admitted v4 and assembled under DECISION-20260805-0002; the text reviewed in COMP-0126..0134 had SHA-256 `8f61c283a5d716f6816798a4946824b2d0d633a8be0d154da33cc1ebbe7ab1fa`; eight findings A1-A8 were accepted under DECISION-20260811-0001, so that reviewed text is not the corrected candidate |
  | v9.1 | **proposed** | corrected successor to the reviewed v9. The corrected pre-version-bump text had SHA-256 `c2dadf897441bf842b34e2b71a347a264401bb228168c4b4214d5964c8d218b0`; it differs from the reviewed v9 because the eight accepted findings A1-A8 were answered by recorded corrections. The v9.1 version/history update records that distinction and does not itself add a ninth substantive correction; pending review of the corrected text |

- reconstruction inputs:
  `ABS-0004-v9-task2-required-changes.patch`,
  `ABS-0004-v9-task3-limitations.patch`,
  `ABS-0004-v9-identity-status.patch`, and
  `ASSEMBLY_RULE_CORRECTION.md`, retained under
  `docs/self_model/v9_reconstruction/`.
- authors: operator (adjudicating principal); inherited v4 text drafted by an
  executor self-reported as "Claude"; v9 reconstruction text and assembly by
  the reviewing executor self-reported as `gpt-5.6-thinking`; both executor
  identities are unverified testimony; with attributed advisor contributions
  described in Evidence Inputs.
- sentence discipline: every normative statement is tagged `[DEF]`
  definition; `[PRINCIPLE]` architectural principle;
  `[PROPOSED_CONSTRAINT]` constraint proposed for adoption;
  `[INHERITED_CONSTRAINT]` constraint text carried forward unchanged from the
  admitted v4 baseline. Its current governance force derives from v4's
  admission, not from the proposed v9 document. A substantive change becomes
  `[PROPOSED_CONSTRAINT]` until separately admitted; `[COMMIT]` commitment
  concerning the preparation of this document; `[PROPOSAL]` candidate
  implementation boundary subject to future governance; `[OPEN]` open
  question; or `[LIMITATION]` descriptive boundary on what the ontology, its
  records, or current enforcement establish. A `[DEF]` introduces a term,
  record shape, relation, or descriptive derivation; it does not by itself
  impose an obligation, prohibition, permission, admission condition, or
  status-changing consequence. A limitation imposes no constraint and claims
  no adoption. Untagged prose binds nothing.
- `[LIMITATION]` `[INHERITED_CONSTRAINT]` establishes textual continuity with
  an admitted v4 constraint; it does not by itself establish semantic identity
  when definitions, vocabularies, relation rules, or other referents used by
  that constraint differ in the proposed version. Such dependencies require
  re-examination before admission.

## Evidence Inputs


--- END OF EVIDENCE ---

Answer only the question above.

## OpenAI Response

- model: `gpt-5.6-terra`

```
**VERDICT: I cannot issue a binding adjudication because the evidence ancestry includes an executor whose equivalence remains unresolved under the described corrected C3 rule; analytically, the prior finding still holds against the supplied text.**

The text permits an authorization-chain terminus to be attributed to an `AccountablePrincipal`, including a `pseudonymous operator identity`, without requiring an external identity anchor, an external entitlement source, or verification of either. The listed fields are `principal_id`, `principal_kind`, `authority_scope`, and `delegation_reference`; none requires a binding from the asserted principal to an independently identifiable or externally authorized entity.

The limitations make the gap express:

- Records can state and attribute authority claims but do not establish extra-systemic entitlement to govern.
- A recorded terminus identifies where the represented chain stops but does not establish substantive authorization.
- Repository records establish only what was declared, recorded, linked, traversable, and correctly attributed.

Accordingly, the ontology can represent both a genuinely authorized root arrangement and a fabricated seed arrangement as records with the same relevant internal shape: an asserted `AccountablePrincipal`, an asserted `authority_scope`, and a chain ending at that assertion. Nothing in the supplied definitions requires a represented difference between them.

To represent the distinction, a root-authority record would need, at minimum:

1. an asserted external anchor for the `AccountablePrincipal`, such as an identified organization, office, delegated authority, or other extra-repository authority source;
2. a time-bounded binding between that anchor and the asserted `principal_id`;
3. evidence that the anchor actually conferred or possessed the stated `authority_scope`;
4. provenance for that evidence, including the external issuer or source and the method by which the binding and authority were checked;
5. a verification record identifying who performed the verification, what was verified, and the limits or status of that verification; and
6. a relation linking the root authorization, approval, activation, and chain terminus to that verified authority basis.

A record containing assertions, references, or copies of such material could exist inside the repository. But a repository-only record could not itself establish the external anchor, the authenticity of the binding, or the principal’s extra-systemic entitlement. It could represent that an external basis was claimed or was checked by a named verifier; it could not turn the external fact into an internally established fact merely by being stored or linked there.

**Evidence needed and not provided**

- A resolution of whether `gpt-5.6-thinking` and `gpt-5.6-terra` are equivalent executors, or other evidence sufficient under corrected C3 to remove the stated adjudication bar.
- The text of corrected C3 itself, including its defined terms and any exception or procedure for handling unresolved executor equivalence.
- If the question were instead about the actual root arrangement rather than the ontology’s representational capacity: the actual root records and any external-anchor, delegation, entitlement, and verification materials. Those are not needed for the textual conclusion above.

**Other finding not asked about**

The supplied text leaves authorization-chain bootstrap marked `[OPEN]`. Thus, apart from the missing external-anchor distinction, the proposed text does not yet define how a chain is to terminate in a standing policy, delegated authority, or `AccountablePrincipal` authority scope.
```

## Claude Response

- model: `claude-sonnet-5`

```
**VERDICT:** The finding still holds — nothing in the evidence given distinguishes a genuinely-authorized seed from a fabricated one, and the gap is structural, not merely uncorrected by A1–A8.

**Reasoning**

Section 4.13's `AccountablePrincipal` definition is unchanged in the relevant respect: `principal_kind` includes "pseudonymous operator identity," "No personal identifying data required," and "Cryptographic attestation is a later implementation mechanism, not an ontology requirement." `authority_scope` and `delegation_reference` are self-declared fields on the same record the principal itself (or an executor acting for it) can author. Nothing requires that `delegation_reference` resolve to anything outside the repository.

Section 3's limitations state this plainly:

- "Repository records do not by themselves establish a principal's extra-systemic entitlement to govern."
- "A recorded authorization-chain terminus identifies where the represented chain stops. It does not by itself establish that the underlying invocation is substantively authorized."
- "[OPEN] Authorization-chain bootstrap: how an authorization chain terminates in a standing policy, delegated authority, or AccountablePrincipal authority scope rather than requiring an infinite sequence of prior authorizations" — still open.

A genuine root principal and a fabricated one would produce *identical* record shapes under these definitions: same `principal_id`, `principal_kind`, `authority_scope`, `delegation_reference` fields, none externally checked. The ontology has no field or record type that forces an external anchor. The v4 admission itself — "by the operator as accountable principal in session, recorded in conversation only" — is a live instance of exactly this unanchored pattern sitting at the terminus every later authorization chain relies on.

**What a distinguishing record would need**

1. A `delegation_reference` (or new field) that resolves to an *externally checkable* instrument — a signed appointment, a registry-verifiable credential, a witnessed act — not a self-declared string.
2. A named verification act covering that anchor, admitted the way 4.13 requires for any property: "admission may not treat a property as established that no named verification record covers." I.e., an `EvidenceAdmissionDecision` listing "principal anchor verified" as a `required_verified_property`, with the verifying party and method disclosed (lineage/independence findings, per 4.13's `EvidenceAdmissionDecision` fields).
3. That verification record's own provenance would need to be outside the principal's unilateral control, or the same problem recurses one level up.

**Whether such a record could exist inside the repository at all**

Only as a *representation* that an external check occurred — not as the check itself. The repository can hold "verification record V asserts anchor A was checked by method M on date D," which is a legitimate `DecisionRecord`/`EvidenceAdmissionDecision` shape. But per the LIMITATION language, such a record still "does not by itself establish a principal's extra-systemic entitlement to govern." The ontology can represent the *presence or absence* of an anchoring/verification act; it cannot, from inside the repository, certify the external fact the anchor points to. That gap is declared, not merely unaddressed by A1–A8.

**Evidence needed and not had:** The actual text of corrections A1–A8 (only the metadata summary — "answered by recorded corrections" — was supplied). I cannot confirm from what's given whether any of A1–A8 touched Section 3 or 4.13 language beyond what's quoted here; I'm relying on the disclosure's own characterization that "Nothing in the A1 to A8 corrections addressed this," which the supplied section text is at least consistent with (it contains no anchor requirement).

**Found but not asked about:**

- The v4 admission record — the terminus of every authorization chain per the question's own framing — is itself "recorded in conversation only," with no admission warrant. This is not a hypothetical risk; it is the actual root record exhibiting the unanchored pattern the finding describes.
- Disclosure 3's C3 constraint ("an invocation may not adjudicate a claim whose evidence ancestry contains an executor of unresolved equivalence") applies reflexively to this very output: the metadata names "the reviewing executor self-reported as `gpt-5.6-thinking`" as author of the v9 reconstruction under review, and states "both executor identities are unverified testimony." Any invocation reviewing this text — including this one — carries that same unresolved-equivalence ancestry. Consistent with Disclosure 3, this response is offered as evidence for the accountable principal, not as an adjudication of the claim.
```
