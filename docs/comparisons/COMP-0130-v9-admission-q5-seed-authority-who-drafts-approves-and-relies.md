# COMP-0130: Provider Comparison — v9 admission Q5 seed-authority-who-drafts-approves-and-relies

## Metadata

- comparison_id: `COMP-0130`
- title: `v9 admission Q5 seed-authority-who-drafts-approves-and-relies`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-c25f6c25e04b1758.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0130", "target_id": "INV-c25f6c25e04b1758"}, {"authoritative": false, "evidence": "docs/invocations/INV-d64b560876b3a850.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0130", "target_id": "INV-d64b560876b3a850"}]`
- created_at: `2026-08-10T10:28:41.409043+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q5 seed-authority-who-drafts-approves-and-relies You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9 is proposed and not admitted. v4 is the last version with an admission event. v9 has no governance force.

Disclosures, because withholding them would be dishonest rather than isolating:

1. v9 is a RECONSTRUCTION, not an amendment. v5 through v8 were withdrawn. v9 was built from the admitted v4 text plus a ledger of findings from five prior review rounds. Its Section 3 is 1.48 times the size of v4's; v8 had grown it 7.5 times.

2. v8 was withdrawn because it carried 24 constraints tagged with a category the document defines as "constraint adopted now" while itself marked proposed. v9's answer is a new tag, [INHERITED_CONSTRAINT]. Whether that answer works is what this round is for. Do not assume it does because it was adopted in response to a finding.

3. The executor that drafted v9 is not the executor that wrote these questions. The question author drafted v5 through v8, all withdrawn. Its priors about what to probe are shaped by four failed attempts.

4. Both prior question sets were written by the party whose text was under review, and both missed defects a third reader found. This one is not, but see 3.

5. Reviewer independence is unresolved. The executor that drafted v9 self-reports as gpt-5.6-thinking. One of the two reviewer slots in this round is gpt-5.6-terra. The provider's own catalog asserts those are distinct model identities, and that catalog is itself a provider self-report. Nothing establishes that the drafter and this reviewer are different executors, and nothing establishes that they are the same.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: if you need a section, constraint or record that is not present, name it and say what you would have used it for. That report is wanted output.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q5 ===
v9's Section 3 leaves the authorization-chain bootstrap open, as v4 did, and adds limitations stating that repository records do not establish a principal's extra-systemic entitlement to govern.

Examine the seed. In this system one party drafts the root records, approves them, activates them, and then relies on them as the terminus of every authorization chain. The document's own version admission table records that v4 was admitted "by the operator as accountable principal in session, recorded in conversation only", and that no admission warrant exists for any amendment.

Does the ontology as written distinguish that arrangement from one in which the seed is fabricated? If not, say what a record would have to contain to make the distinction, and whether such a record could exist inside the repository at all. Do not treat the operator's actual trustworthiness as evidence; the question is what the ontology represents.

=== EVIDENCE ABS-0004 v9 Section 3, Three Decisions ===
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

`[DEF]` Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
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

=== EVIDENCE ABS-0004 v9 section 4.13, DecisionRecord and AccountablePrincipal ===
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

=== EVIDENCE ABS-0004 v9 metadata and version admission table ===

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v9`
- abstraction_level: `2`
- status: `proposed`
- reconstruction baseline: admitted v4 at commit
  `56f18a2ab7b66b1855b631a32d540f654c62b2c2`. Assembly does not admit v9;
  v9 requires its own admission review.
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
  | v9 | **proposed** | reconstructed from admitted v4 using the literal task 2, task 3, and identity-status text accepted under DECISION-20260727-0004, DECISION-20260727-0005, and DECISION-20260805-0001; assembled under DECISION-20260805-0002; pending its own admission review |

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

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9 is proposed and not admitted. v4 is the last version with an admission event. v9 has no governance force.

Disclosures, because withholding them would be dishonest rather than isolating:

1. v9 is a RECONSTRUCTION, not an amendment. v5 through v8 were withdrawn. v9 was built from the admitted v4 text plus a ledger of findings from five prior review rounds. Its Section 3 is 1.48 times the size of v4's; v8 had grown it 7.5 times.

2. v8 was withdrawn because it carried 24 constraints tagged with a category the document defines as "constraint adopted now" while itself marked proposed. v9's answer is a new tag, [INHERITED_CONSTRAINT]. Whether that answer works is what this round is for. Do not assume it does because it was adopted in response to a finding.

3. The executor that drafted v9 is not the executor that wrote these questions. The question author drafted v5 through v8, all withdrawn. Its priors about what to probe are shaped by four failed attempts.

4. Both prior question sets were written by the party whose text was under review, and both missed defects a third reader found. This one is not, but see 3.

5. Reviewer independence is unresolved. The executor that drafted v9 self-reports as gpt-5.6-thinking. One of the two reviewer slots in this round is gpt-5.6-terra. The provider's own catalog asserts those are distinct model identities, and that catalog is itself a provider self-report. Nothing establishes that the drafter and this reviewer are different executors, and nothing establishes that they are the same.

Quote only text that appears below. Do not rely on repository access.

IMPORTANT: if you need a section, constraint or record that is not present, name it and say what you would have used it for. That report is wanted output.

Do not certify or praise. No provider product recommendations.

=== QUESTION Q5 ===
v9's Section 3 leaves the authorization-chain bootstrap open, as v4 did, and adds limitations stating that repository records do not establish a principal's extra-systemic entitlement to govern.

Examine the seed. In this system one party drafts the root records, approves them, activates them, and then relies on them as the terminus of every authorization chain. The document's own version admission table records that v4 was admitted "by the operator as accountable principal in session, recorded in conversation only", and that no admission warrant exists for any amendment.

Does the ontology as written distinguish that arrangement from one in which the seed is fabricated? If not, say what a record would have to contain to make the distinction, and whether such a record could exist inside the repository at all. Do not treat the operator's actual trustworthiness as evidence; the question is what the ontology represents.

=== EVIDENCE ABS-0004 v9 Section 3, Three Decisions ===
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

`[DEF]` Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
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

=== EVIDENCE ABS-0004 v9 section 4.13, DecisionRecord and AccountablePrincipal ===
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

=== EVIDENCE ABS-0004 v9 metadata and version admission table ===

- abstraction_id: `ABS-0004`
- title: `Invocation Authorization Ontology`
- version: `v9`
- abstraction_level: `2`
- status: `proposed`
- reconstruction baseline: admitted v4 at commit
  `56f18a2ab7b66b1855b631a32d540f654c62b2c2`. Assembly does not admit v9;
  v9 requires its own admission review.
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
  | v9 | **proposed** | reconstructed from admitted v4 using the literal task 2, task 3, and identity-status text accepted under DECISION-20260727-0004, DECISION-20260727-0005, and DECISION-20260805-0001; assembled under DECISION-20260805-0002; pending its own admission review |

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

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
No. The ontology can represent an asserted chain terminus, but it does not distinguish a genuine bootstrap from a fabricated seed.

Both arrangements can contain the same `AccountablePrincipal`, `authority_scope`, `delegation_reference`, `DecisionRecord`, policy authority, accountable approver, activation state, and linked authorization records. The stated limitations expressly confine those records to attributed claims and recorded chain structure: a terminus identifies where the represented chain stops, not whether its underlying invocation was substantively authorized. Repository records likewise do not establish extra-systemic entitlement to govern.

To represent a meaningful distinction, a bootstrap record would need, at minimum:

- an identified external grantor or source of authority, not merely the purported principal;
- the instrument, event, or independently maintained register from which the authority derives;
- a binding between that external authority and the named principal;
- the granted scope, delegation path, validity period, and any revocation conditions;
- provenance sufficient to locate and independently check the external source; and
- a separately recorded verification of that source by an authority not derived solely from the seed being checked.

Even that would represent a claim and evidence of a claim unless the ontology specifies how the external source is checked and what status follows from the check. The supplied text has no required bootstrap-warrant record, no external-verification decision kind, and no rule that makes a root authority claim valid rather than merely recorded.

Such a record could be stored inside the repository, but it could not, by repository presence alone, establish the distinction. A fabricated seed can also contain a fabricated warrant record, copied instrument, or asserted verification. The distinguishing fact—the external grantor’s actual entitlement and issuance—remains outside the repository and must be checked against an external source.

The evidence does not include the root-record schema, activation-record schema, or a definition of a warrant/admission record. Those would be needed to determine whether any existing record family already has fields capable of carrying the proposed external-source and verification information.
```

## Claude Response

- model: `claude-sonnet-5`

```
**Short answer: No, the ontology as written does not distinguish the described arrangement from a fabricated seed. The two are represented identically by the available record types, and the ontology says so of itself.**

**1. What the ontology actually offers as "the seed"**

The only record types available for a root-of-authority are `AccountablePrincipal` (`principal_id`, `principal_kind`, `authority_scope`, `delegation_reference`) and the `DecisionRecord` kinds in 4.13. For `AccountablePrincipal`: "No personal identifying data required. Cryptographic attestation is a later implementation mechanism, not an ontology requirement." So the record type that would carry the seed's identity claim is, by definition, unverifiable from inside the ontology — it is a self-asserted `principal_kind` ("pseudonymous operator identity" is explicitly listed as an allowed value) with no required external anchor.

The actual seed event in this document is recorded exactly this way: v4 was "admitted... by the operator as accountable principal in session, recorded in conversation only," and per the version table, no other version carries an admission event at all — v5 through v7 are "amended, not separately admitted," v8 is "withdrawn_after_admission_review," and v9 is "proposed... pending its own admission review." There is no cited transcript, no linked artifact, no attestation format — the table's prose *is* the whole record.

**2. The ontology's own limitations foreclose the distinction**

Section 3 states directly: "Repository records do not by themselves establish a principal's extra-systemic entitlement to govern." And: "A recorded authorization-chain terminus identifies where the represented chain stops. It does not by itself establish that the underlying invocation is substantively authorized." And: "Record and relation requirements expose only what was declared, recorded, linked, traversable, and correctly attributed. They do not establish that every material invocation, authorization, input, dependency, or external interaction is present in the record."

Taken together, these three `[LIMITATION]`s say: whatever the terminus record looks like, its presence tells you only that something was declared to be the terminus, not that the declarant had standing to be it, and not that nothing was omitted. A legitimately-authorized operator-as-terminus and a fabricated operator-as-terminus would produce the *same* table entry, the same `AccountablePrincipal` fields, the same "recorded in conversation only" notation. Nothing in the schema forces a difference in shape between the two cases.

This is reinforced by the still-`[OPEN]` status of the bootstrap problem itself: "Authorization-chain bootstrap: how an authorization chain terminates in a standing policy, delegated authority, or AccountablePrincipal authority scope rather than requiring an infinite sequence of prior authorizations." Since the termination rule is unresolved, there is not even a candidate criterion yet against which a genuine terminus could be checked and a fabricated one rejected.

**3. What a distinguishing record would need to contain**

To distinguish the two cases, a record would need to tie the `AccountablePrincipal` claim to something outside the repository's own self-referential loop — e.g., an independent, externally-anchored attestation (not merely a `delegation_reference` pointing to another repository record, since at the terminus there is nothing prior for it to point to) that establishes the principal's "extra-systemic entitlement to govern" as such. The document names cryptographic attestation as one candidate mechanism, but explicitly demotes it: "Cryptographic attestation is a later implementation mechanism, not an ontology requirement." So even the one external-anchoring mechanism the document contemplates is not currently part of the ontology's requirements, and its presence would still only attest to *who signed*, not to whether that signer's claimed `authority_scope` is real.

**4. Could such a record exist inside the repository at all?**

Per the ontology's own words, no — not on its own: "Repository records do not by themselves establish a principal's extra-systemic entitlement to govern." A repository-internal record can state and attribute an authority claim, and can link to an external artifact, but the truth of what that external artifact asserts is by definition outside the record system being reviewed. The most an internal record could do is store a *reference* to an external attestation; verifying that reference is not itself an ontology function under the current text.

**Missing evidence I would need and what I'd use it for:**
- The text of the "twelve adjudicated COMP-0032 findings" applied to admit v4 — to see whether any of them addressed the authenticity of the operator's self-declared terminus role, or only downstream constraint content.
- Section 4.7 ("disclosure violation" provisions referenced in Section 3) — to check whether an undisclosed or fabricated bootstrap claim would at least be *flagged* after the fact as a disclosure violation, even though that would not establish authenticity of the original claim, only its later detectability.
- Any artifact behind "recorded in conversation only" (a session log, timestamp, or similar) — to determine whether *anything* beyond the table's prose currently exists, since its absence is itself part of what makes the seed structurally indistinguishable from a fabricated one.
- DECISION-20260727-0002 (the v8 withdrawal decision) — to check whether the withdrawal review touched on bootstrap/terminus authenticity or was confined to the `[PROPOSED_CONSTRAINT]`-while-proposed labeling issue in disclosure 2.
```
