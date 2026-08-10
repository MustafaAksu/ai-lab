# COMP-0128: Provider Comparison — v9 admission Q3 authorization-graph-cycles-expiry-retroactivity

## Metadata

- comparison_id: `COMP-0128`
- title: `v9 admission Q3 authorization-graph-cycles-expiry-retroactivity`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-083ca93dc5494ad8.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0128", "target_id": "INV-083ca93dc5494ad8"}, {"authoritative": false, "evidence": "docs/invocations/INV-3de932a5f9a5877b.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0128", "target_id": "INV-3de932a5f9a5877b"}]`
- created_at: `2026-08-10T10:25:58.149760+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q3 authorization-graph-cycles-expiry-retroactivity You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

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

=== QUESTION Q3 ===
Five review rounds have not probed the temporal and structural behaviour of the authorization graph. Construct concrete failures for each of the following, or state that the ontology as written prevents it and identify the sentence that does:

(a) a cycle in the authorization chain, where A's authority derives from B's and B's from A's;
(b) two authorization records that both cover an invocation and contradict each other;
(c) an authorization relied upon after the standing authority behind it was superseded or withdrawn;
(d) an authorization issued after the invocation it covers, and a record that cannot distinguish this from one issued before.

For each, say whether the defect is in the ontology's definitions, in the absence of a rule, or outside the ontology's scope.

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

=== EVIDENCE ABS-0004 v9 section 4.16, RoutingPolicy and AuthorizationPolicy ===
### 4.16 RoutingPolicy and AuthorizationPolicy (defined, deferred)

`[DEF]` RoutingPolicy: a versioned durable rule specifying eligible roles,
qualification requirements, escalation triggers, independence requirements,
cost and latency boundaries, fallback behavior, consequence classes,
catalog freshness requirements.

`[DEF]` AuthorizationPolicy: a versioned durable rule governing invocation
authorization: role eligibility conditions, consequence ceilings,
subordinate-execution classes permitted for inheritance (Section 3),
required qualifications and independence, exception procedures. All policy
references in DecisionRecords (`applicable policy`, `issued_under`,
`policy authority`) are typed references to a versioned policy object,
never untyped strings.

`[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does
not establish that a policy was active, applicable, evaluated, or enforced for
a decision. AuthorizationPolicy enforcement remains deferred.

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

=== QUESTION Q3 ===
Five review rounds have not probed the temporal and structural behaviour of the authorization graph. Construct concrete failures for each of the following, or state that the ontology as written prevents it and identify the sentence that does:

(a) a cycle in the authorization chain, where A's authority derives from B's and B's from A's;
(b) two authorization records that both cover an invocation and contradict each other;
(c) an authorization relied upon after the standing authority behind it was superseded or withdrawn;
(d) an authorization issued after the invocation it covers, and a record that cannot distinguish this from one issued before.

For each, say whether the defect is in the ontology's definitions, in the absence of a rule, or outside the ontology's scope.

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

=== EVIDENCE ABS-0004 v9 section 4.16, RoutingPolicy and AuthorizationPolicy ===
### 4.16 RoutingPolicy and AuthorizationPolicy (defined, deferred)

`[DEF]` RoutingPolicy: a versioned durable rule specifying eligible roles,
qualification requirements, escalation triggers, independence requirements,
cost and latency boundaries, fallback behavior, consequence classes,
catalog freshness requirements.

`[DEF]` AuthorizationPolicy: a versioned durable rule governing invocation
authorization: role eligibility conditions, consequence ceilings,
subordinate-execution classes permitted for inheritance (Section 3),
required qualifications and independence, exception procedures. All policy
references in DecisionRecords (`applicable policy`, `issued_under`,
`policy authority`) are typed references to a versioned policy object,
never untyped strings.

`[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does
not establish that a policy was active, applicable, evaluated, or enforced for
a decision. AuthorizationPolicy enforcement remains deferred.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
**Scope note.** The supplied text does not provide a formal authorization-chain relation, temporal fields or semantics, conflict-resolution rules, or definitions of `activation state` and `supersession`. Thus it does not establish that another unstated constraint prevents any of the following.

### (a) Circular authorization chain

**Concrete failure:** Record IA-A authorizes A for an invocation, with B asserted as the authority from which that authorization derives. Record IA-B authorizes B for its invocation, with A asserted as the authority from which that authorization derives. Traversal is A → B → A and never reaches standing policy, delegated authority, or an AccountablePrincipal authority scope.

The ontology cannot reliably represent or detect that cycle from the listed InvocationAuthorization fields. Those fields include an issuer invocation, accountable approver, evidence, policy authority, and supersession, but do not define an authorization-parent or authority-derivation edge. An issuer invocation is not defined as the authorization on which the issuer relied.

No supplied sentence prevents the cycle. The closest text leaves termination unresolved:

> `[OPEN]` Authorization-chain bootstrap: how an authorization chain terminates in a standing policy, delegated authority, or AccountablePrincipal authority scope rather than requiring an infinite sequence of prior authorizations.

That open issue concerns termination, but supplies neither an acyclicity condition nor a traversal rule.

**Defect location:** Both a **definition defect**—the chain edge is not defined—and an **absence of a rule**—no rule requires a terminating, acyclic chain. The question of whether the final external authority is substantively entitled is additionally outside the ontology’s established power:

> `[LIMITATION]` Repository records do not by themselves establish a principal's extra-systemic entitlement to govern.

### (b) Two contradictory authorizations covering one invocation

**Concrete failure:** Two InvocationAuthorization records name the same invocation request, authorized executor, assigned role, and consequence class. One record has an effective status and conditions that permit the invocation; the other has an effective status or conditions that prohibit it. Both records remain in an activation state represented as usable, and neither identifies the other through supersession.

Nothing defines when an authorization covers an invocation, how multiple records applicable to the same invocation are compared, which has priority, or whether contradictory effective statuses or conditions are invalid. The ontology requires that an InvocationAuthorization carry an invocation request and conditions, but does not supply matching, exclusivity, precedence, or conflict-resolution semantics.

No supplied sentence prevents this. In particular, this merely lists record content:

> `[DEF]` DecisionRecord: `decision_kind` (invocation_authorization | routing_selection | evidence_admission | manual_override), target, `recommended_status` and `effective_status` (distinct: a model recommendation must not appear to have assigned final status before accountable approval), issuer invocation, accountable approver, evidence, policy authority, activation state, supersession.

It does not define a single controlling record or the effect of competing records.

**Defect location:** Primarily an **absence of a rule**, with supporting **definition gaps** for coverage, status meaning, condition semantics, activation state, and supersession.

### (c) Reliance after underlying standing authority was superseded or withdrawn

**Concrete failure:** An InvocationAuthorization cites an AuthorizationPolicy version as its applicable policy and policy authority. That policy version, or the delegation or AccountablePrincipal authority scope behind it, is later superseded or withdrawn. A subsequent invocation relies on the earlier authorization. The record can still contain its typed policy reference and can still be presented as authorization because no stated rule requires revalidation of the standing authority at invocation time or invalidates dependent authorizations upon supersession or withdrawal.

The text expressly says that typed policy references do not establish activity, applicability, evaluation, or enforcement:

> `[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does not establish that a policy was active, applicable, evaluated, or enforced for a decision. AuthorizationPolicy enforcement remains deferred.

Although `activation state` and `supersession` are listed as DecisionRecord content, no supplied definition says what either means, whether it applies to the authority behind an authorization, or how a later invocation must treat a superseded record.

No supplied sentence prevents the failure.

**Defect location:** For the represented authorization graph, this is an **absence of a rule** concerning validity periods, withdrawal, supersession propagation, and revalidation. For whether the external standing authority was actually valid, it is also partly **outside the ontology’s scope**, because:

> `[LIMITATION]` A recorded authorization-chain terminus identifies where the represented chain stops. It does not by itself establish that the underlying invocation is substantively authorized.

### (d) Authorization created after the invocation it covers

**Concrete failure:** Invocation I occurs. Later, an InvocationAuthorization is created that names I as its invocation request and records the executor, role, consequence class, policy, qualifications, independence requirements, and conditions. The record contains no authorization issuance time, no invocation time, no effective-from or expiry time, and no rule comparing those times. Therefore the resulting record cannot distinguish this retrospective authorization from one created before I.

The intended characterization is ex ante:

> 1. Invocation authorization (ex ante): may executor E perform invocation I  
>    under role R, consequence C, and conditions K?

But no supplied definition makes ex ante ordering a required temporal predicate or requires records to contain the dates needed to test it. The InvocationAuthorization field list likewise contains no timestamp or validity interval.

**Defect location:** A **definition defect**—required temporal properties and their meanings are absent—and an **absence of a rule** requiring issuance and validity before the covered invocation. It is not outside the ontology’s stated subject matter, because invocation authorization is expressly described as ex ante.

### Missing material needed to determine whether another provision cures these failures

The evidence set lacks:

1. A formal definition of authorization-chain derivation or a record relation identifying the authorization, delegation, policy, or authority scope on which a record depends.
2. Definitions and permitted values for `activation state`, `supersession`, `recommended_status`, and `effective_status`.
3. A rule for authorization applicability, overlap, priority, conflict resolution, revocation, withdrawal, and supersession effects.
4. Temporal fields and rules for invocation occurrence, authorization issuance, effective time, expiry, and retrospective authorization.
5. Any constraints from the referenced Section 4.7 that might bear on undeclared subordinate execution, though that reference does not by itself address cycles, contradictory records, revocation, or temporal ordering.
```

## Claude Response

- model: `claude-sonnet-5`

```
# Q3 Response: Authorization Graph — Temporal and Structural Failures

Evidence available is limited to Section 3, 4.13, and 4.16. I note gaps as they arise.

## (a) Cycle: A's authority derives from B's, B's from A's

**Concrete failure:** AccountablePrincipal A carries `delegation_reference` pointing to B's authority_scope; AccountablePrincipal B carries `delegation_reference` pointing to A's authority_scope. Each InvocationAuthorization's `policy authority` / `qualifications relied on` traces back along this loop. Nothing in the record schema breaks the cycle, and the record and relation requirements only test that references are "declared, recorded, linked, traversable, and correctly attributed" — a cycle satisfies all four while establishing no terminal authority.

**Classification: absence of a rule**, and the ontology says so itself. Section 3 flags this class of problem as unresolved:

> `[OPEN]` Authorization-chain bootstrap: how an authorization chain terminates in a standing policy, delegated authority, or AccountablePrincipal authority scope rather than requiring an infinite sequence of prior authorizations.

An infinite sequence and a finite cycle are both non-terminating in the relevant sense (no ground truth is ever reached), and this OPEN item does not exclude cyclic "termination." v9 does not close this; it remains an admitted gap.

**Missing evidence:** any acyclicity constraint on `delegation_reference` or on authorization-chain traversal, if one exists elsewhere in the document, is not in this evidence set. I would need it to check whether the OPEN item was resolved outside Section 3.

## (b) Two contradictory authorization records both covering an invocation

**Concrete failure:** InvocationAuthorization R1 targets invocation I, authorizing executor E under consequence ceiling C1, `effective_status` = approved, `activation state` = active. InvocationAuthorization R2, created independently, also targets I, authorizing E under a broader consequence ceiling C2, also `effective_status` = approved, `activation state` = active, with `supersession` unpopulated on both. Nothing in 4.13 specifies that only one InvocationAuthorization may be effective per invocation, nor what "activation state" or "supersession" mean operationally, nor a precedence rule when two records conflict.

**Classification: absence of a rule**, compounded by a definitional gap. The field exists —

> `[DEF]` DecisionRecord: ... issuer invocation, accountable approver, evidence, policy authority, activation state, supersession.

— but its semantics are never defined here (no statement of what makes a record superseded, or of uniqueness/precedence among concurrent records for the same target). Naming a field without defining its governing rule is itself a definitional deficiency, and there is no separate conflict-resolution rule to fall back on.

**Missing evidence:** a definition of `supersession` and `activation state`, and any conflict-resolution or uniqueness constraint over DecisionRecords sharing a target — not present in this evidence set. I would use it to determine whether contradiction detection is even representable, let alone resolved.

## (c) Authorization relied upon after standing authority was superseded or withdrawn

**Concrete failure:** InvocationAuthorization cites `applicable policy` = AuthorizationPolicy v2, which at issuance validly granted the relevant role eligibility/consequence ceiling. AuthorizationPolicy v2 is later superseded by v3, narrowing or revoking that eligibility. The InvocationAuthorization record retains its typed reference to v2 and is never re-evaluated; a later invocation is executed relying on it as if still live.

**Classification: outside the ontology's current scope, and disclosed as such.**

> `[LIMITATION]` Defining AuthorizationPolicy and requiring typed references does not establish that a policy was active, applicable, evaluated, or enforced for a decision. AuthorizationPolicy enforcement remains deferred.

This is not a silent absence — v9 states plainly that liveness/enforcement checking is deferred. The failure mode in (c) is exactly what "enforcement remains deferred" leaves open: the ontology can record *that* a policy was cited, not *that it was still in force* at the moment relied upon.

**Missing evidence:** any mechanism, elsewhere in the document, for propagating policy supersession to already-issued authorizations, or a validity-window field on InvocationAuthorization. Not present here.

## (d) Authorization issued after the invocation it covers, indistinguishable from one issued before

**Concrete failure:** Executor E performs invocation I at T0 with no authorization on record. At T1 > T0, an InvocationAuthorization record is created with `decision_kind` = invocation_authorization, target = I, `effective_status` = approved. The InvocationAuthorization field list —

> invocation request, authorized executor, assigned role, consequence class, applicable policy, qualifications relied on, independence requirements, conditions

— contains no issuance timestamp and no field recording the invocation's execution time for comparison. The general DecisionRecord fields likewise contain none. A record built this way is structurally identical to one legitimately issued at T-minus-something before I occurred.

**Classification: absence of a rule**, resting on a definition that asserts but does not enforce the property. The decision kind is *labeled* ex ante —

> 1. Invocation authorization (ex ante): may executor E perform invocation I under role R, consequence C, and conditions K?

— but "ex ante" here is a definitional characterization of the decision's intended function, not a structural constraint the record format can verify. No field ties authorization-issuance time to invocation-occurrence time, so nothing in the schema can detect, or even represent, the violation of ex-ante-ness. This compounds with the adjacent general limitation:

> `[LIMITATION]` Record and relation requirements expose only what was declared, recorded, linked, traversable, and correctly attributed. They do not establish that every material invocation, authorization, input, dependency, or external interaction is present in the record.

That limitation covers *presence*, not *ordering*, so it does not by itself resolve (d); it only reinforces that the ontology does not claim completeness checks that could catch a missing prior authorization.

**Missing evidence:** a temporal field pair (authorization issuance timestamp vs. invocation timestamp) or an ordering rule requiring the former to precede the latter for `decision_kind = invocation_authorization`. Not present in this evidence set; without it, (d)'s failure is not merely possible but unfalsifiable from the record alone.

## Summary table

| Part | Failure constructible? | Classification |
|---|---|---|
| (a) cycle | Yes | Absence of a rule (ontology's own `[OPEN]` bootstrap item, unresolved) |
| (b) contradiction | Yes | Absence of a rule (undefined `supersession`/`activation state`, no precedence rule) |
| (c) stale reliance | Yes | Outside current scope, explicitly disclosed (`[LIMITATION]`: "AuthorizationPolicy enforcement remains deferred") |
| (d) post-hoc issuance | Yes | Absence of a rule (label "ex ante" not backed by an enforceable/verifiable temporal field) |

None of the four is prevented by a stated sentence; in each case either no governing rule exists, or the ontology explicitly defers the relevant enforcement.
```
