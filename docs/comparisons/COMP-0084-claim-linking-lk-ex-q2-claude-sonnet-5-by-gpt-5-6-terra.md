# COMP-0084: Provider Comparison — Claim linking LK-EX-Q2-claude-sonnet-5-by-gpt-5-6-terra

## Metadata

- comparison_id: `COMP-0084`
- title: `Claim linking LK-EX-Q2-claude-sonnet-5-by-gpt-5-6-terra`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-4872ef2c66a94892.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0084", "target_id": "INV-4872ef2c66a94892"}, {"authoritative": false, "evidence": "docs/invocations/INV-1f8b1d5e0793915e.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0084", "target_id": "INV-1f8b1d5e0793915e"}]`
- created_at: `2026-07-29T06:19:04.340635+00:00`
- command: `scripts/compare_providers.py --title Claim linking LK-EX-Q2-claude-sonnet-5-by-gpt-5-6-terra You are linking extracted claims to the specific block of source text each claim is about. This is a matching task. Do not evaluate whether any claim is correct.

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

1. claim: The standing-authority constraint's visibility claim overclaims completeness.
   quote: "every authorization resting on it are legible and attributable."
   extractor called it about: v7 standing-authority constraint visibility claim

2. claim: The described mechanism only supports visibility for authorizations that are correctly declared and not defeated by omission.
   quote: "authorizations that are correctly declared and not defeated by omission are legible."
   extractor called it about: v7 standing-authority constraint visibility mechanism

3. claim: The honest visibility claim should be limited to authorizations that are declared and correctly chained.
   quote: "visibility for authorizations that are declared and correctly chained"
   extractor called it about: v7 standing-authority constraint visibility wording

4. claim: The honest visibility claim should state that undeclared or non-conforming authorizations are not made visible by the constraint.
   quote: "Undeclared or non-conforming authorizations are not made visible by this constraint;"
   extractor called it about: v7 standing-authority constraint visibility wording

5. claim: The retraction overclaims a general impossibility from a single defeated instance.
   quote: "The retraction itself overclaims a general impossibility from a single defeated instance."
   extractor called it about: v7 retraction of the internal-control claim

6. claim: The honest retraction should state that whether another internal control could close the regress is unresolved.
   quote: "Whether some other internal control could close the regress is unresolved;"
   extractor called it about: v7 retraction wording on internal controls

7. claim: P6's actual text is needed to determine whether v7 accurately characterizes P6.
   quote: "I can't check whether this characterization of P6 is itself accurate without P6."
   extractor called it about: P6

8. claim: Section 4.7 is needed to determine whether undeclared subordinate execution is actually detected or surfaced.
   quote: "needed to know whether undeclared subordinate execution is actually detected/surfaced"
   extractor called it about: Section 4.7 disclosure violations

9. claim: COMP-0037 itself is needed to determine whether its evidence supports only the failure of one rule or a broader claim.
   quote: "to check whether "two reviewers independently defeated it" supports only "this rule failed" or something closer to the broader claim"
   extractor called it about: COMP-0037

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

1. claim: The standing-authority constraint's visibility claim overclaims completeness.
   quote: "every authorization resting on it are legible and attributable."
   extractor called it about: v7 standing-authority constraint visibility claim

2. claim: The described mechanism only supports visibility for authorizations that are correctly declared and not defeated by omission.
   quote: "authorizations that are correctly declared and not defeated by omission are legible."
   extractor called it about: v7 standing-authority constraint visibility mechanism

3. claim: The honest visibility claim should be limited to authorizations that are declared and correctly chained.
   quote: "visibility for authorizations that are declared and correctly chained"
   extractor called it about: v7 standing-authority constraint visibility wording

4. claim: The honest visibility claim should state that undeclared or non-conforming authorizations are not made visible by the constraint.
   quote: "Undeclared or non-conforming authorizations are not made visible by this constraint;"
   extractor called it about: v7 standing-authority constraint visibility wording

5. claim: The retraction overclaims a general impossibility from a single defeated instance.
   quote: "The retraction itself overclaims a general impossibility from a single defeated instance."
   extractor called it about: v7 retraction of the internal-control claim

6. claim: The honest retraction should state that whether another internal control could close the regress is unresolved.
   quote: "Whether some other internal control could close the regress is unresolved;"
   extractor called it about: v7 retraction wording on internal controls

7. claim: P6's actual text is needed to determine whether v7 accurately characterizes P6.
   quote: "I can't check whether this characterization of P6 is itself accurate without P6."
   extractor called it about: P6

8. claim: Section 4.7 is needed to determine whether undeclared subordinate execution is actually detected or surfaced.
   quote: "needed to know whether undeclared subordinate execution is actually detected/surfaced"
   extractor called it about: Section 4.7 disclosure violations

9. claim: COMP-0037 itself is needed to determine whether its evidence supports only the failure of one rule or a broader claim.
   quote: "to check whether "two reviewers independently defeated it" supports only "this rule failed" or something closer to the broader claim"
   extractor called it about: COMP-0037

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
{"links":[{"claim":1,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco"},{"claim":2,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco"},{"claim":3,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco"},{"claim":4,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco"},{"claim":5,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require"},{"claim":6,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require"},{"claim":7,"block":null,"reason_if_null":"The claim is about the missing text of P6."},{"claim":8,"block":null,"reason_if_null":"The claim is about the missing Section 4.7 disclosure-violation provisions."},{"claim":9,"block":null,"reason_if_null":"The claim is about the missing COMP-0037 evidence itself."}]}
```

## Claude Response

- model: `claude-sonnet-5`

```
{"links":[
{"claim":1,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco","reason_if_null":null},
{"claim":2,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco","reason_if_null":null},
{"claim":3,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco","reason_if_null":null},
{"claim":4,"block":"ABS-0004:v7:S3#adopted_constraint:a-standing-authority-claim-is-reco","reason_if_null":null},
{"claim":5,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require","reason_if_null":null},
{"claim":6,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require","reason_if_null":null},
{"claim":7,"block":null,"reason_if_null":"Claim is about P6's own text, which is not present among the candidate blocks (only P7 appears)."},
{"claim":8,"block":"ABS-0004:v7:S3#def:subordinate-authorization-inherita","reason_if_null":null},
{"claim":9,"block":"ABS-0004:v7:S3#open:whether-standing-authority-require","reason_if_null":null}
]}
```
