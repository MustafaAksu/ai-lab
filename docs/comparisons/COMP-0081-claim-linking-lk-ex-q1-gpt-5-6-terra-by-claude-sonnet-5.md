# COMP-0081: Provider Comparison — Claim linking LK-EX-Q1-gpt-5-6-terra-by-claude-sonnet-5

## Metadata

- comparison_id: `COMP-0081`
- title: `Claim linking LK-EX-Q1-gpt-5-6-terra-by-claude-sonnet-5`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-7fb65ad9753c23fc.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0081", "target_id": "INV-7fb65ad9753c23fc"}, {"authoritative": false, "evidence": "docs/invocations/INV-b033dd05e4f6521f.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0081", "target_id": "INV-b033dd05e4f6521f"}]`
- created_at: `2026-07-29T06:17:29.313771+00:00`
- command: `scripts/compare_providers.py --title Claim linking LK-EX-Q1-gpt-5-6-terra-by-claude-sonnet-5 You are linking extracted claims to the specific block of source text each claim is about. This is a matching task. Do not evaluate whether any claim is correct.

Below are numbered claims, then a closed list of candidate blocks with their identifiers.

For each claim, give the identifier of the ONE block the claim is about - the specific passage it asserts something concerning.

Rules:

1. Copy the block identifier exactly as written. Do not abbreviate or reformat it.
2. If the claim concerns several blocks, choose the one it is most directly about.
3. If the claim is about something NOT in the candidate list, answer null. This is expected and wanted. Do NOT choose the closest available block. A claim linked to the wrong block is worse than a claim left unlinked, because a wrong link reads as structure and will be trusted. Claims about a missing section, about the answer's own reasoning, or about material outside the list should all be null.
4. When you answer null, give a short reason: what the claim is actually about.
5. Answer for every claim number, once each.

Output STRICT JSON and nothing else. No preamble, no commentary, no markdown fences:

{"links":[{"claim":1,"block":"<identifier or null>","reason_if_null":"..."}]}

=== CLAIMS ===

1. claim: The answer favors reading (a), but only for the specific claim that an internal authorization structure can prevent convenient closure of the extra-systemic authorization regress.
   quote: "I favor **(a)**, but only for the specific claim v6 purported to make"
   extractor called it about: choice between readings (a) and (b)

2. claim: Section 3 states the decisive premise that root authority is extra-systemic.
   quote: "Root authority is extra-systemic."
   extractor called it about: Section 3 premise

3. claim: No internal record arrangement can make or verify the fact of who actually controls the repository and answers for it.
   quote: "no internal record arrangement can make or verify that fact"
   extractor called it about: extra-systemic authority fact

4. claim: A required non-universal scope, a fixed number of delegations, or a prohibition on self-issuance cannot establish that the root claimant has legitimate authority; it can only constrain the shape of records produced by a claimant.
   quote: "On that premise, a required non-universal scope, a fixed number of delegations, or a prohibition on self-issuance cannot establish that the root claimant has legitimate authority. It can only constrain the shape of records produced by a claimant."
   extractor called it about: limits of mechanical scope/delegation rules

5. claim: A rule refusing self-issued authorization cannot eliminate the root's self-standing character; it can only require the root to use another identity or another record path.
   quote: "A rule refusing self-issued authorization cannot eliminate the root’s self-standing character; it can require the root to use another identity or another record path."
   extractor called it about: self-issued authorization rule

6. claim: v7's marking of a self-issued record as disqualified from counting as independent is a substantive limitation on an independence finding, even though it is not a test of root entitlement.
   quote: "That is a substantive limitation on an independence finding, even though it is not a test of root entitlement."
   extractor called it about: v7 self_issued disqualification

7. claim: Permitting a universal authority_scope is not itself the terminus; the terminus is the explicit statement that a universal declaration does not become a real boundary merely because it is represented in a scope field.
   quote: "The terminus is the explicit statement that a universal declaration does not become a real boundary merely because it is represented in a scope field."
   extractor called it about: universal authority_scope and the terminus claim

8. claim: The operative result claimed by v7 is limited to attribution and legibility of the claim, its breadth, and the authorizations resting on it, and does not claim prevention.
   quote: "The operative result claimed by v7 is limited: attribution and legibility of the claim, its breadth, and the authorizations resting on it. It does not claim prevention."
   extractor called it about: scope of v7's claim

9. claim: Reading (b) is not incoherent; it identifies a different objective than (a), namely bounding which records the system accepts rather than establishing root entitlement.
   quote: "That does not make (b) incoherent; it identifies a different objective."
   extractor called it about: reading (b)'s coherence

10. claim: Calling record-acceptance bounding a prevention of the extra-systemic regress would be an error; calling it a restriction on record admissibility or operational participation would be a different, potentially testable claim.
   quote: "Calling that latter effect prevention of the extra-systemic regress would be the error. Calling it a restriction on record admissibility or operational participation would be a different, potentially testable claim."
   extractor called it about: mislabeling risk between prevention and admissibility restriction

11. claim: A paired-world construction with identical repository records but differing real-world accountability can test whether an internal rule reaches the same result in both cases, and if so it cannot verify actual root authority, supporting reading (a).
   quote: "If the internal rule reaches the same result in both cases, it cannot verify or establish the difference in actual root authority. This would support (a) for any claimed internal solution to the regress."
   extractor called it about: paired-world construction for the regress claim

12. claim: An acceptance-language construction defining an enforceable rule rejecting universal-scope chains and testing whether violating records can still produce an effective_status would test reading (b)'s narrower claim about bounding operational acceptance.
   quote: "If they cannot, the system has implemented a genuine internal acceptance bound."
   extractor called it about: acceptance-language construction for reading (b)

13. claim: An external-evidence test construction is needed, specifying the external source, who may assess it, sufficiency of evidence, handling of absent/contested/expired/narrower evidence, and which outputs (visibility, invocation, admission) are affected, to determine whether a scope declaration is non-theatrical.
   quote: "A decision rule would need to specify:"
   extractor called it about: external-evidence test for scope declarations

14. claim: Section 3 itself leaves open what external evidence a scope declaration should carry.
   quote: "Section 3 itself leaves open “what external evidence a scope declaration should carry.”"
   extractor called it about: Section 3 open question on external evidence

15. claim: The evidence set is sufficient to decide the conceptual point that internal records cannot establish the extra-systemic fact described in P7.
   quote: "The evidence set is sufficient to decide the conceptual point that internal records cannot establish the extra-systemic fact described in P7."
   extractor called it about: sufficiency of evidence for the conceptual point

16. claim: The evidence set is insufficient to decide whether v7's visibility-only approach is preferable to an operational scope-bound regime, because materials such as v6's exact enforcement semantics, the two reviewers' constructions in COMP-0037, authority_scope semantics, effectiveness/admission policy rules, the external evidence model, and a threat model/success criterion are absent.
   quote: "It is insufficient to decide whether v7’s visibility-only approach is preferable to an operational scope-bound regime, because the following are absent:"
   extractor called it about: comparison between v7 visibility-only approach and operational scope-bound regime

17. claim: The defensible conclusion is narrow: v7 is correct not to represent its internal records as establishing root authority.
   quote: "the defensible conclusion is narrow: v7 is correct not to represent its internal records as establishing root authority"
   extractor called it about: overall defensible conclusion

18. claim: Whether v7 has abandoned a useful operational control cannot be decided from the supplied text.
   quote: "Whether it has abandoned a useful operational control cannot be decided from the supplied text."
   extractor called it about: limits of the answer's conclusion

=== CANDIDATE BLOCKS ===

--- ABS-0004:v7:S3#def:the-ontology-distinguishes-three-d ---
The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

--- ABS-0004:v7:S3#def:a-decision-making-act-is-an-invoca ---
A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

--- ABS-0004:v7:S3#def:subordinate-authorization-inherita ---
Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

--- ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi ---
P7. Root authority is extra-systemic. An authorization chain
terminates at a standing authority that the system records and does not
establish. Who is accountable for AI-Lab is a fact about the world, about
who controls the repository and answers for it, and no arrangement of
records inside the repository can make that fact true or verify it. Any
design that appears to derive root authority from internal evidence has
merely moved the regress and disguised it.

--- ABS-0004:v7:S3#def:authorization-chain-termination-a ---
Authorization-chain termination. A chain terminates at an
AccountablePrincipal's standing authority within a declared
`authority_scope`. Authorizations the principal issues inside that scope
are self-standing. Every other authorization must chain, through one or
more steps, to such a standing authority. An authorization that chains to
nothing is not thereby permitted: it is unauthorized.

--- ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco ---
A standing-authority claim is recorded, never
verified. AI-Lab does not validate that a declared principal is entitled to
the authority it claims; it has no means to do so, and pretending otherwise
would be the overclaim P6 forbids. What the record provides is visibility:
the claim, its declared scope, and every authorization resting on it are
legible and attributable. Visibility is the whole of what this constraint
achieves, and it is not prevention.

--- ABS-0004:v7:S3#adopted_constraint:scope-breadth-is-visible-not-bound ---
Scope breadth is visible, not bounded by fiat. A
declared `authority_scope` may be arbitrarily wide, including universal. A
wide scope is permitted and must be legible as wide; it may not be
described, in a record or in a summary, as bounded merely because a scope
field was populated. A boundary that no one can fail to satisfy is not a
boundary, and calling it one is the defect this constraint exists to
prevent.

--- ABS-0004:v7:S3#adopted_constraint:self-issued-authorization-is-marke ---
Self-issued authorization is marked, never silently
accepted. Where the issuing principal and the authorized executor are the
same party, or where a principal issues an authorization covering an
invocation it also performs, the authorization records `self_issued: true`.
A self-issued authorization is not refused: at the root of any chain, the
accountable party necessarily authorizes work it is also responsible for.
It is instead disqualified from counting as independent authorization
wherever independence is required, and it is countable as such.

--- ABS-0004:v7:S3#def:standing-authority-is-not-a-capabi ---
Standing authority is not a capability of executors. A model, tool,
or human acting as an executor never holds standing authority by virtue of
executing; it holds it only as an AccountablePrincipal within a declared
scope, which is a separate role under Section 4.13. One party may hold both
roles; the ontology separates the roles, not the parties, and the
`self_issued` marking is how the coincidence is recorded rather than
denied.

--- ABS-0004:v7:S3#open:whether-standing-authority-require ---
Whether standing authority requires periodic re-declaration or
review. COMP-0037 established what v6 got wrong here: both reviewers
independently constructed the same self-authorization path, and v6's claim
to prevent convenient closure of the regress was false. v7 does not close
the question by asserting a stronger internal control; it records that no
internal control can close it, and asks instead what external evidence a
scope declaration should carry.

--- ABS-0004:v7:S4.13#def:decisionrecord-decision-kind-invoc ---
DecisionRecord: `decision_kind` (invocation_authorization |
routing_selection | evidence_admission | manual_override), target,
`recommended_status` and `effective_status` (distinct: a model
recommendation must not appear to have assigned final status before
accountable approval), issuer invocation, accountable approver, evidence,
policy authority, activation state, supersession. `[OPEN]` Whether existing
warrant/admission records are extended to fulfill this or a new record
family is created, and whether kinds are subtypes or one record family.

--- ABS-0004:v7:S4.13#def:invocationauthorization-decision-k ---
InvocationAuthorization (decision_kind invocation_authorization)
additionally carries: invocation request, authorized executor, assigned
role, consequence class, applicable policy, qualifications relied on,
independence requirements, conditions. Without this kind, P1 is not
represented by the ontology.

--- ABS-0004:v7:S4.13#def:routingdecision-decision-kind-rout ---
RoutingDecision (decision_kind routing_selection) additionally
carries: candidates considered, rejection reasons including lineage
conflicts, selected candidate, policy version, catalog snapshot. Tier
labels are policy-derived under current evidence, never intrinsic
ModelIdentity attributes.

--- ABS-0004:v7:S4.13#def:evidenceadmissiondecision-decision ---
EvidenceAdmissionDecision (decision_kind evidence_admission)
additionally carries: admitted artifact or claim, admitted epistemic
status, lineage and independence findings relied on, disclosed provenance
limitations, and an enumeration of verified properties against the
receiving role's `required_verified_properties`; admission may not treat a
property as established that no named verification record covers.

--- ABS-0004:v7:S4.13#def:accountableprincipal-principal-id ---
AccountablePrincipal: `principal_id`, `principal_kind` (delegated
role, governance body, pseudonymous operator identity, organization, or
other authorized entity), `authority_scope`, `delegation_reference`. No
personal identifying data required. Cryptographic attestation is a later
implementation mechanism, not an ontology requirement.

--- END OF CANDIDATES ---

Output the JSON now.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are linking extracted claims to the specific block of source text each claim is about. This is a matching task. Do not evaluate whether any claim is correct.

Below are numbered claims, then a closed list of candidate blocks with their identifiers.

For each claim, give the identifier of the ONE block the claim is about - the specific passage it asserts something concerning.

Rules:

1. Copy the block identifier exactly as written. Do not abbreviate or reformat it.
2. If the claim concerns several blocks, choose the one it is most directly about.
3. If the claim is about something NOT in the candidate list, answer null. This is expected and wanted. Do NOT choose the closest available block. A claim linked to the wrong block is worse than a claim left unlinked, because a wrong link reads as structure and will be trusted. Claims about a missing section, about the answer's own reasoning, or about material outside the list should all be null.
4. When you answer null, give a short reason: what the claim is actually about.
5. Answer for every claim number, once each.

Output STRICT JSON and nothing else. No preamble, no commentary, no markdown fences:

{"links":[{"claim":1,"block":"<identifier or null>","reason_if_null":"..."}]}

=== CLAIMS ===

1. claim: The answer favors reading (a), but only for the specific claim that an internal authorization structure can prevent convenient closure of the extra-systemic authorization regress.
   quote: "I favor **(a)**, but only for the specific claim v6 purported to make"
   extractor called it about: choice between readings (a) and (b)

2. claim: Section 3 states the decisive premise that root authority is extra-systemic.
   quote: "Root authority is extra-systemic."
   extractor called it about: Section 3 premise

3. claim: No internal record arrangement can make or verify the fact of who actually controls the repository and answers for it.
   quote: "no internal record arrangement can make or verify that fact"
   extractor called it about: extra-systemic authority fact

4. claim: A required non-universal scope, a fixed number of delegations, or a prohibition on self-issuance cannot establish that the root claimant has legitimate authority; it can only constrain the shape of records produced by a claimant.
   quote: "On that premise, a required non-universal scope, a fixed number of delegations, or a prohibition on self-issuance cannot establish that the root claimant has legitimate authority. It can only constrain the shape of records produced by a claimant."
   extractor called it about: limits of mechanical scope/delegation rules

5. claim: A rule refusing self-issued authorization cannot eliminate the root's self-standing character; it can only require the root to use another identity or another record path.
   quote: "A rule refusing self-issued authorization cannot eliminate the root’s self-standing character; it can require the root to use another identity or another record path."
   extractor called it about: self-issued authorization rule

6. claim: v7's marking of a self-issued record as disqualified from counting as independent is a substantive limitation on an independence finding, even though it is not a test of root entitlement.
   quote: "That is a substantive limitation on an independence finding, even though it is not a test of root entitlement."
   extractor called it about: v7 self_issued disqualification

7. claim: Permitting a universal authority_scope is not itself the terminus; the terminus is the explicit statement that a universal declaration does not become a real boundary merely because it is represented in a scope field.
   quote: "The terminus is the explicit statement that a universal declaration does not become a real boundary merely because it is represented in a scope field."
   extractor called it about: universal authority_scope and the terminus claim

8. claim: The operative result claimed by v7 is limited to attribution and legibility of the claim, its breadth, and the authorizations resting on it, and does not claim prevention.
   quote: "The operative result claimed by v7 is limited: attribution and legibility of the claim, its breadth, and the authorizations resting on it. It does not claim prevention."
   extractor called it about: scope of v7's claim

9. claim: Reading (b) is not incoherent; it identifies a different objective than (a), namely bounding which records the system accepts rather than establishing root entitlement.
   quote: "That does not make (b) incoherent; it identifies a different objective."
   extractor called it about: reading (b)'s coherence

10. claim: Calling record-acceptance bounding a prevention of the extra-systemic regress would be an error; calling it a restriction on record admissibility or operational participation would be a different, potentially testable claim.
   quote: "Calling that latter effect prevention of the extra-systemic regress would be the error. Calling it a restriction on record admissibility or operational participation would be a different, potentially testable claim."
   extractor called it about: mislabeling risk between prevention and admissibility restriction

11. claim: A paired-world construction with identical repository records but differing real-world accountability can test whether an internal rule reaches the same result in both cases, and if so it cannot verify actual root authority, supporting reading (a).
   quote: "If the internal rule reaches the same result in both cases, it cannot verify or establish the difference in actual root authority. This would support (a) for any claimed internal solution to the regress."
   extractor called it about: paired-world construction for the regress claim

12. claim: An acceptance-language construction defining an enforceable rule rejecting universal-scope chains and testing whether violating records can still produce an effective_status would test reading (b)'s narrower claim about bounding operational acceptance.
   quote: "If they cannot, the system has implemented a genuine internal acceptance bound."
   extractor called it about: acceptance-language construction for reading (b)

13. claim: An external-evidence test construction is needed, specifying the external source, who may assess it, sufficiency of evidence, handling of absent/contested/expired/narrower evidence, and which outputs (visibility, invocation, admission) are affected, to determine whether a scope declaration is non-theatrical.
   quote: "A decision rule would need to specify:"
   extractor called it about: external-evidence test for scope declarations

14. claim: Section 3 itself leaves open what external evidence a scope declaration should carry.
   quote: "Section 3 itself leaves open “what external evidence a scope declaration should carry.”"
   extractor called it about: Section 3 open question on external evidence

15. claim: The evidence set is sufficient to decide the conceptual point that internal records cannot establish the extra-systemic fact described in P7.
   quote: "The evidence set is sufficient to decide the conceptual point that internal records cannot establish the extra-systemic fact described in P7."
   extractor called it about: sufficiency of evidence for the conceptual point

16. claim: The evidence set is insufficient to decide whether v7's visibility-only approach is preferable to an operational scope-bound regime, because materials such as v6's exact enforcement semantics, the two reviewers' constructions in COMP-0037, authority_scope semantics, effectiveness/admission policy rules, the external evidence model, and a threat model/success criterion are absent.
   quote: "It is insufficient to decide whether v7’s visibility-only approach is preferable to an operational scope-bound regime, because the following are absent:"
   extractor called it about: comparison between v7 visibility-only approach and operational scope-bound regime

17. claim: The defensible conclusion is narrow: v7 is correct not to represent its internal records as establishing root authority.
   quote: "the defensible conclusion is narrow: v7 is correct not to represent its internal records as establishing root authority"
   extractor called it about: overall defensible conclusion

18. claim: Whether v7 has abandoned a useful operational control cannot be decided from the supplied text.
   quote: "Whether it has abandoned a useful operational control cannot be decided from the supplied text."
   extractor called it about: limits of the answer's conclusion

=== CANDIDATE BLOCKS ===

--- ABS-0004:v7:S3#def:the-ontology-distinguishes-three-d ---
The ontology distinguishes three decision kinds:

1. Invocation authorization (ex ante): may executor E perform invocation I
   under role R, consequence C, and conditions K?
2. Routing selection: why was executor E selected rather than alternatives?
3. Evidence admission (ex post): may output O enter governed evidence, and
   with what epistemic status?

--- ABS-0004:v7:S3#def:a-decision-making-act-is-an-invoca ---
A decision-making act is an Invocation. Its governed output is a
DecisionRecord. InvocationAuthorization, RoutingDecision, and
EvidenceAdmissionDecision are DecisionRecord kinds (Section 4.13), not
executor events. Execution authorization and output admission are separate:
an experimental executor may be authorized to run while its outputs remain
inadmissible as governed evidence.

--- ABS-0004:v7:S3#def:subordinate-authorization-inherita ---
Subordinate authorization inheritance: a subordinate invocation is
covered by its parent's InvocationAuthorization only when that
authorization's conditions declare the permitted subordinate execution
classes (executor kinds, roles, consequence ceiling). A subordinate
execution outside the declared classes requires its own authorization.
Undeclared subordinate execution is a disclosure violation under 4.7, not
an implicitly authorized act.

--- ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi ---
P7. Root authority is extra-systemic. An authorization chain
terminates at a standing authority that the system records and does not
establish. Who is accountable for AI-Lab is a fact about the world, about
who controls the repository and answers for it, and no arrangement of
records inside the repository can make that fact true or verify it. Any
design that appears to derive root authority from internal evidence has
merely moved the regress and disguised it.

--- ABS-0004:v7:S3#def:authorization-chain-termination-a ---
Authorization-chain termination. A chain terminates at an
AccountablePrincipal's standing authority within a declared
`authority_scope`. Authorizations the principal issues inside that scope
are self-standing. Every other authorization must chain, through one or
more steps, to such a standing authority. An authorization that chains to
nothing is not thereby permitted: it is unauthorized.

--- ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco ---
A standing-authority claim is recorded, never
verified. AI-Lab does not validate that a declared principal is entitled to
the authority it claims; it has no means to do so, and pretending otherwise
would be the overclaim P6 forbids. What the record provides is visibility:
the claim, its declared scope, and every authorization resting on it are
legible and attributable. Visibility is the whole of what this constraint
achieves, and it is not prevention.

--- ABS-0004:v7:S3#adopted_constraint:scope-breadth-is-visible-not-bound ---
Scope breadth is visible, not bounded by fiat. A
declared `authority_scope` may be arbitrarily wide, including universal. A
wide scope is permitted and must be legible as wide; it may not be
described, in a record or in a summary, as bounded merely because a scope
field was populated. A boundary that no one can fail to satisfy is not a
boundary, and calling it one is the defect this constraint exists to
prevent.

--- ABS-0004:v7:S3#adopted_constraint:self-issued-authorization-is-marke ---
Self-issued authorization is marked, never silently
accepted. Where the issuing principal and the authorized executor are the
same party, or where a principal issues an authorization covering an
invocation it also performs, the authorization records `self_issued: true`.
A self-issued authorization is not refused: at the root of any chain, the
accountable party necessarily authorizes work it is also responsible for.
It is instead disqualified from counting as independent authorization
wherever independence is required, and it is countable as such.

--- ABS-0004:v7:S3#def:standing-authority-is-not-a-capabi ---
Standing authority is not a capability of executors. A model, tool,
or human acting as an executor never holds standing authority by virtue of
executing; it holds it only as an AccountablePrincipal within a declared
scope, which is a separate role under Section 4.13. One party may hold both
roles; the ontology separates the roles, not the parties, and the
`self_issued` marking is how the coincidence is recorded rather than
denied.

--- ABS-0004:v7:S3#open:whether-standing-authority-require ---
Whether standing authority requires periodic re-declaration or
review. COMP-0037 established what v6 got wrong here: both reviewers
independently constructed the same self-authorization path, and v6's claim
to prevent convenient closure of the regress was false. v7 does not close
the question by asserting a stronger internal control; it records that no
internal control can close it, and asks instead what external evidence a
scope declaration should carry.

--- ABS-0004:v7:S4.13#def:decisionrecord-decision-kind-invoc ---
DecisionRecord: `decision_kind` (invocation_authorization |
routing_selection | evidence_admission | manual_override), target,
`recommended_status` and `effective_status` (distinct: a model
recommendation must not appear to have assigned final status before
accountable approval), issuer invocation, accountable approver, evidence,
policy authority, activation state, supersession. `[OPEN]` Whether existing
warrant/admission records are extended to fulfill this or a new record
family is created, and whether kinds are subtypes or one record family.

--- ABS-0004:v7:S4.13#def:invocationauthorization-decision-k ---
InvocationAuthorization (decision_kind invocation_authorization)
additionally carries: invocation request, authorized executor, assigned
role, consequence class, applicable policy, qualifications relied on,
independence requirements, conditions. Without this kind, P1 is not
represented by the ontology.

--- ABS-0004:v7:S4.13#def:routingdecision-decision-kind-rout ---
RoutingDecision (decision_kind routing_selection) additionally
carries: candidates considered, rejection reasons including lineage
conflicts, selected candidate, policy version, catalog snapshot. Tier
labels are policy-derived under current evidence, never intrinsic
ModelIdentity attributes.

--- ABS-0004:v7:S4.13#def:evidenceadmissiondecision-decision ---
EvidenceAdmissionDecision (decision_kind evidence_admission)
additionally carries: admitted artifact or claim, admitted epistemic
status, lineage and independence findings relied on, disclosed provenance
limitations, and an enumeration of verified properties against the
receiving role's `required_verified_properties`; admission may not treat a
property as established that no named verification record covers.

--- ABS-0004:v7:S4.13#def:accountableprincipal-principal-id ---
AccountablePrincipal: `principal_id`, `principal_kind` (delegated
role, governance body, pseudonymous operator identity, organization, or
other authorized entity), `authority_scope`, `delegation_reference`. No
personal identifying data required. Cryptographic attestation is a later
implementation mechanism, not an ontology requirement.

--- END OF CANDIDATES ---

Output the JSON now.

## OpenAI Response

- model: `gpt-5.6-terra`

```
{"links":[{"claim":1,"block":null,"reason_if_null":"It concerns the answer's choice between readings (a) and (b), which is not stated in a candidate block."},{"claim":2,"block":"ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi"},{"claim":3,"block":"ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi"},{"claim":4,"block":"ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi"},{"claim":5,"block":"ABS-0004:v7:S3#adopted_constraint:self-issued-authorization-is-marke"},{"claim":6,"block":"ABS-0004:v7:S3#adopted_constraint:self-issued-authorization-is-marke"},{"claim":7,"block":"ABS-0004:v7:S3#adopted_constraint:scope-breadth-is-visible-not-bound"},{"claim":8,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco"},{"claim":9,"block":null,"reason_if_null":"It concerns the coherence of reading (b), a distinction not present in the candidate blocks."},{"claim":10,"block":null,"reason_if_null":"It concerns a distinction between preventing regress and restricting record acceptance, which is not stated in a candidate block."},{"claim":11,"block":null,"reason_if_null":"It concerns a paired-world test construction that is not in the candidate blocks."},{"claim":12,"block":null,"reason_if_null":"It concerns an acceptance-language test construction for reading (b), which is not in the candidate blocks."},{"claim":13,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require"},{"claim":14,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require"},{"claim":15,"block":"ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi"},{"claim":16,"block":null,"reason_if_null":"It concerns the sufficiency of supplied materials for comparing v7 with an operational scope-bound regime, an assessment not contained in a candidate block."},{"claim":17,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco"},{"claim":18,"block":null,"reason_if_null":"It concerns the answer's limit on what can be concluded from the supplied text, not a candidate passage."}]}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"links":[
{"claim":1,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require","reason_if_null":null},
{"claim":2,"block":"ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi","reason_if_null":null},
{"claim":3,"block":"ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi","reason_if_null":null},
{"claim":4,"block":null,"reason_if_null":"This is the answer's synthesized argument drawing on multiple constraints (non-universal scope, delegation limits, self-issuance prohibition) rather than a passage about one specific block."},
{"claim":5,"block":"ABS-0004:v7:S3#adopted_constraint:self-issued-authorization-is-marke","reason_if_null":null},
{"claim":6,"block":"ABS-0004:v7:S3#adopted_constraint:self-issued-authorization-is-marke","reason_if_null":null},
{"claim":7,"block":"ABS-0004:v7:S3#adopted_constraint:scope-breadth-is-visible-not-bound","reason_if_null":null},
{"claim":8,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco","reason_if_null":null},
{"claim":9,"block":null,"reason_if_null":"This is the answer's own interpretive commentary about reading (b) rather than an assertion about a specific source block."},
{"claim":10,"block":null,"reason_if_null":"This is the answer's own cautionary reasoning about mislabeling, not about a specific source block."},
{"claim":11,"block":null,"reason_if_null":"This is the answer's own proposed test construction (paired-world) for reading (a), not a claim about a specific source block."},
{"claim":12,"block":null,"reason_if_null":"This is the answer's own proposed test construction (acceptance-language) for reading (b), not a claim about a specific source block."},
{"claim":13,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require","reason_if_null":null},
{"claim":14,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require","reason_if_null":null},
{"claim":15,"block":"ABS-0004:v7:S3#principle:p7-root-authority-is-extra-systemi","reason_if_null":null},
{"claim":16,"block":null,"reason_if_null":"This is the answer's own assessment of evidentiary sufficiency listing absent materials, not an assertion about a specific source block."},
{"claim":17,"block":null,"reason_if_null":"This is the answer's own overall conclusion, not about a specific source block."},
{"claim":18,"block":null,"reason_if_null":"This is the answer's own statement about limits of its conclusion, not about a specific source block."}
]}
```
