# COMP-0131: Provider Comparison — v9 admission Q6 what-the-labels-mean-to-a-reader

## Metadata

- comparison_id: `COMP-0131`
- title: `v9 admission Q6 what-the-labels-mean-to-a-reader`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-4e11c2979837afaf.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0131", "target_id": "INV-4e11c2979837afaf"}, {"authoritative": false, "evidence": "docs/invocations/INV-64b5780486dac688.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0131", "target_id": "INV-64b5780486dac688"}]`
- created_at: `2026-08-10T10:30:19.473185+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q6 what-the-labels-mean-to-a-reader You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

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

=== QUESTION Q6 ===
Read as an ordinary reader who sees a record and not the ontology.

The system emits and uses the terms governed, permitted, valid authorization, self-standing, and verified. A prior round established that an invocation with undisclosed subordinate execution can be classified governed.

For each term as it appears below, state what an ordinary reader would take it to mean, what it actually means under this ontology, and the gap. Then answer the question no round has adjudicated: is a system that only classifies, and never refuses, performing authorization at all? If it is better described as authorization assessment or record-coverage classification, say which and say what would have to change in the text.

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

=== EVIDENCE ABS-0004 v9 Section 8, Consequence Classes ===
## 8. Consequence Classes

`[DEF]` Ordinal classes (low | medium | high), not numbers.
`default_consequence` derives from target type (gap closure, plan
admission: high; comparison/synthesis: medium; extraction/classification:
low). `effective_consequence = max(default_consequence,
applicable_modifier_levels)`; modifiers (repository mutation, external side
effect, irreversibility, warrant/capability status change,
security/privacy/legal/financial impact) only raise. `[INHERITED_CONSTRAINT]`
Downward adjustment is a separate governed exception (reason, accountable
principal, scope, evidence, expiry/review) and can never override hard
prohibitions such as disqualifying lineage conflicts. `[OPEN]` Detailed
classification function.

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

=== QUESTION Q6 ===
Read as an ordinary reader who sees a record and not the ontology.

The system emits and uses the terms governed, permitted, valid authorization, self-standing, and verified. A prior round established that an invocation with undisclosed subordinate execution can be classified governed.

For each term as it appears below, state what an ordinary reader would take it to mean, what it actually means under this ontology, and the gap. Then answer the question no round has adjudicated: is a system that only classifies, and never refuses, performing authorization at all? If it is better described as authorization assessment or record-coverage classification, say which and say what would have to change in the text.

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

=== EVIDENCE ABS-0004 v9 Section 8, Consequence Classes ===
## 8. Consequence Classes

`[DEF]` Ordinal classes (low | medium | high), not numbers.
`default_consequence` derives from target type (gap closure, plan
admission: high; comparison/synthesis: medium; extraction/classification:
low). `effective_consequence = max(default_consequence,
applicable_modifier_levels)`; modifiers (repository mutation, external side
effect, irreversibility, warrant/capability status change,
security/privacy/legal/financial impact) only raise. `[INHERITED_CONSTRAINT]`
Downward adjustment is a separate governed exception (reason, accountable
principal, scope, evidence, expiry/review) and can never override hard
prohibitions such as disqualifying lineage conflicts. `[OPEN]` Detailed
classification function.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
### governed

- **Ordinary-reader meaning:** Subject to the system’s rules and oversight; not merely recorded, but actually controlled or properly conducted under governance.
- **Meaning in the supplied ontology text:** The text calls a DecisionRecord an Invocation’s “governed output” and asks whether output may enter “governed evidence.” But it does not define the criteria by which an invocation, output, or evidence becomes governed. The record requirements reach what was “declared, recorded, linked, traversable, and correctly attributed,” while expressly not establishing that every material invocation or interaction is present.
- **Gap:** “Governed” ordinarily implies substantive control and adequate oversight of the underlying activity. Here it can at most denote a status supported by the disclosed record. That leaves room for an invocation with undisclosed subordinate execution to be classified governed despite the ordinary implication that undisclosed material execution defeats meaningful governance.

### permitted

- **Ordinary-reader meaning:** Allowed to occur; authorized rather than prohibited.
- **Meaning in the supplied ontology text:** “Permitted” occurs in the rule that a parent authorization must declare the “permitted subordinate execution classes.” A subordinate invocation is covered only if its executor kind, role, and consequence ceiling fall within those declared classes. An undeclared subordinate execution is a disclosure violation and is not implicitly authorized.
- **Gap:** Ordinary permission is commonly understood as a real authorization to act. The ontology establishes only record-based coverage by a parent authorization’s declared conditions. It does not establish that the declared permission was substantively valid, nor that all subordinate execution was disclosed.

### valid authorization

- **Ordinary-reader meaning:** An authorization that is legally, procedurally, and substantively effective—issued by someone with actual authority, applicable to the act, and still in force.
- **Meaning in the supplied ontology text:** No definition of “valid authorization” appears in the evidence. The nearest construct is InvocationAuthorization, which carries an invocation request, authorized executor, role, consequence class, policy, qualifications, independence requirements, and conditions. The text also states that recorded authority claims and an authorization-chain terminus do not establish extra-systemic entitlement or substantive authorization.
- **Gap:** The ordinary phrase joins record validity with actual authority and effectiveness. The supplied text deliberately declines to establish the latter. An InvocationAuthorization record may therefore represent an authorization claim or documented decision without demonstrating a valid authorization in the ordinary sense.

### self-standing

- **Ordinary-reader meaning:** Independent; able to stand on its own without needing unstated external support, authority, or context.
- **Meaning in the supplied ontology text:** “Self-standing” does not appear in the evidence, and no equivalent defined term is supplied. The closest relevant statements are that authorization-chain bootstrap is open and that a recorded terminus does not establish substantive authorization.
- **Gap:** An ordinary reader could infer that a DecisionRecord or authorization is self-standing because it has an issuer, approver, policy authority, and activation state. The text does not support that inference: its authority chain may terminate only in a represented claim, and the basis for the terminus remains unresolved.

### verified

- **Ordinary-reader meaning:** Checked and established as true, accurate, or compliant.
- **Meaning in the supplied ontology text:** For evidence admission, verified properties must be enumerated against the receiving role’s required properties, and a property may not be treated as established unless a named verification record covers it. The supplied evidence does not define what a verification record must contain, what methods qualify, or what degree of assurance “covers” requires.
- **Gap:** Ordinary “verified” suggests that the property itself has been established. Here it means, at most, that there is a named record covering the property for admission purposes. The text does not establish the adequacy, independence, correctness, or completeness of that verification.

## Is a system that only classifies, and never refuses, performing authorization?

Not in the operative ordinary sense of authorization.

The text frames invocation authorization as an ex-ante question: “may executor E perform invocation I.” But the supplied provisions require DecisionRecords and specify what an InvocationAuthorization carries; they do not require a system to block, refuse, suspend, or otherwise prevent an invocation lacking an effective authorization. Nor do they define the consequences of an unfavorable `effective_status`, an inactive authorization, unmet conditions, or an undisclosed subordinate invocation.

On this evidence, the better description is **record-coverage classification**, rather than authorization assessment alone. It classifies whether disclosed records represent authorization and whether a subordinate invocation falls within declared classes. The limitations make clear that this classification does not establish that all material activity was recorded or that represented authority was substantively valid. “Authorization assessment” would be a closer label than “authorization” if the system made reasoned determinations about authorization claims, but the disclosed-record limitation makes record-coverage classification the more precise description of what is established here.

To make the text support a claim that the system performs authorization, it would need provisions stating, at minimum, that:

1. a currently active, effective InvocationAuthorization is a precondition to performing the invocation;
2. an invocation outside its authorization, conditions, consequence ceiling, or permitted subordinate classes must be refused or halted;
3. `recommended_status`, `effective_status`, activation state, and accountable approval have defined authorization effects;
4. undeclared subordinate execution prevents, rather than merely qualifies, the invocation’s governed status until resolved; and
5. the scope of any residual uncertainty is explicit, since the current limitation says the record cannot establish that every material interaction is present.

If the intended function is only assessment, the text should instead rename or distinguish InvocationAuthorization from an authorization-assessment record, and define “governed” as a record-status claim rather than a claim of substantive control or permission.

Missing material that would be needed to reach a firmer conclusion includes: the definition of `effective_status` and activation state; any enforcement, refusal, or execution-gating rule; the definition and required contents of a verification record; the rule defining when something is “governed”; and the referenced disclosure requirements in section 4.7.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Governed

**Ordinary reading:** "governed" implies something has been brought under proper oversight — checked, approved, under rules that actually constrain it.

**Ontological meaning:** The text uses "governed" as a status label attached to output/evidence via a specific DecisionRecord kind: "may output O enter governed evidence, and with what epistemic status?" and "Its governed output is a DecisionRecord." Governed is thus a classification result of an EvidenceAdmissionDecision, not a statement that the underlying invocation was substantively sound.

**Gap:** An ordinary reader hears "governed" as "vetted." The ontology's own limitation undercuts that: "Record and relation requirements expose only what was declared, recorded, linked, traversable, and correctly attributed. They do not establish that every material invocation, authorization, input, dependency, or external interaction is present in the record." A prior round's finding — that an invocation with undisclosed subordinate execution can still be classified governed — is consistent with this limitation as written, and shows "governed" tolerates undisclosed material facts. The word carries more assurance to a lay reader than the definition delivers.

## Permitted

**Ordinary reading:** allowed, sanctioned, cleared to happen.

**Ontological meaning:** "permitted" appears only as part of a narrow, declared enumeration: "a subordinate invocation is covered by its parent's InvocationAuthorization only when that authorization's conditions declare the permitted subordinate execution classes (executor kinds, roles, consequence ceiling)." Anything not on that declared list is not permitted by default — it is a violation: "Undeclared subordinate execution is a disclosure violation under 4.7, not an implicitly authorized act."

**Gap:** Ordinary use treats "permitted" as the default absent a prohibition. Here it is the opposite: permission exists only for what is explicitly enumerated in the parent authorization's conditions; everything else is a disclosure failure, not a lesser-but-still-real permission.

## Valid authorization

This exact term does **not appear** in the evidence provided. The evidence uses "InvocationAuthorization," "authorized executor," "applicable policy," and discusses a "recorded authorization-chain terminus," but never the phrase "valid authorization." I cannot state what an ordinary reader vs. the ontology would mean by it without inventing text.

**What I would need:** a definition (likely in Section 4.7, not in this evidence set) that specifies what makes an authorization "valid" — record completeness, policy conformance, or something about the underlying entitlement. This matters because the evidence already draws a sharp line the missing definition would need to respect: "A recorded authorization-chain terminus identifies where the represented chain stops. It does not by itself establish that the underlying invocation is substantively authorized." Without the missing definition I cannot say whether "valid" in this ontology means "record-valid" or "substantively authorized" — and the evidence suggests those are not the same thing, which is exactly the ambiguity an ordinary reader would miss.

## Self-standing

This term also does **not appear** in the evidence provided.

**What I would need:** the section (not furnished here) that defines "self-standing," presumably in contrast to "subordinate" invocation, to determine whether it means "not covered by inheritance from a parent authorization" or something about independence of the executor/evidence. Without it, I cannot compare ordinary and technical meaning, and I flag its absence rather than guess.

## Verified

**Ordinary reading:** checked and confirmed true, typically by someone independent of the claim.

**Ontological meaning:** "verified" is defined by reference to a named record's existence, not to independent confirmation of fact: EvidenceAdmissionDecision requires "an enumeration of verified properties against the receiving role's `required_verified_properties`; admission may not treat a property as established that no named verification record covers."

**Gap:** The rule as written is negative and record-bound — it forbids treating an unverified property as established, by requiring a named verification record to exist. It does not require that the verification record's content be independently checked for accuracy. Combined with the limitation that record requirements "expose only what was declared, recorded, linked, traversable, and correctly attributed" and "do not establish that every material invocation, authorization, input, dependency, or external interaction is present in the record," "verified" here means "a verification record is present and attributed," not "independently confirmed true." An ordinary reader would assume the stronger sense.

## Is a classify-only, never-refuse system performing authorization?

Under this ontology's own terms, no — not in the sense Decision 1 defines. Section 3 frames invocation authorization as an answer to "may executor E perform invocation I under role R, consequence C, and conditions K?" — a binding may/may-not determination. Section 4.13 then splits DecisionRecord into `recommended_status` and `effective_status`, explicitly "distinct: a model recommendation must not appear to have assigned final status before accountable approval." That clause exists precisely to prevent a classifying act from being mistaken for an authorizing act. A system that only classifies and never refuses produces, at most, a `recommended_status` — it never reaches `effective_status`, and the text treats that gap as load-bearing, not incidental. It also treats InvocationAuthorization, RoutingDecision, and EvidenceAdmissionDecision as "DecisionRecord kinds… not executor events," meaning the record itself is not the act of authorizing; something (the "accountable approver" field) has to act on it.

Given what the evidence actually supplies — enumeration of verified properties against a required list, admission of evidence into "governed" status, declared/undeclared subordinate classes — the classify-only system as described is closer to **record-coverage classification**: it checks whether declared conditions, verification records, and disclosure requirements are present and attributed, per the limitation that such requirements "expose only what was declared, recorded, linked, traversable, and correctly attributed" without establishing that "every material invocation… is present in the record." It falls short of even "authorization assessment" because assessment implies a substantive may/may-not judgment against role, consequence, and conditions (Decision 1's language), whereas a system that never refuses never renders that judgment — it only tags.

**What would have to change in the text:**
- A defined, binding refusal or block act tied to `effective_status` (currently the field exists but no enumerated values or enforcement consequence are shown in this evidence), so "authorization" names an act with teeth, not just a labeled record.
- Closure of the `[OPEN]` item on whether recommended/effective status live in one record family or separate ones, since that bears directly on whether classification and authorization are even the same kind of act.
- A definition for "valid authorization" and "self-standing" (absent from this evidence) so the gap between record-validity and substantive authorization — already flagged in the `[LIMITATION]` on authorization-chain termini — is closed rather than left implicit.
- Some reconciliation of the disclosed prior finding that undisclosed subordinate execution can still be classified governed, since that finding is direct evidence that the current classification apparatus does not track the "may/may not" question Section 3 says authorization is supposed to answer.
```
