# COMP-0127: Provider Comparison — v9 admission Q2 do-limitations-do-work-or-wrap-failures

## Metadata

- comparison_id: `COMP-0127`
- title: `v9 admission Q2 do-limitations-do-work-or-wrap-failures`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-a45245d3f5a61eef.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0127", "target_id": "INV-a45245d3f5a61eef"}, {"authoritative": false, "evidence": "docs/invocations/INV-bd7369efbf3ef2e9.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0127", "target_id": "INV-bd7369efbf3ef2e9"}]`
- created_at: `2026-08-10T10:24:17.933583+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q2 do-limitations-do-work-or-wrap-failures You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

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

=== QUESTION Q2 ===
v9 adds nine [LIMITATION] statements, a category defined as "a descriptive boundary on what the ontology, its records, or current enforcement establish. A limitation imposes no constraint and claims no adoption."

A prior synthesis characterised v8's failure mode as: a failed control retained in control-shaped language, wrapped in an accurate disclaimer, and delegated to a future mechanism or a careful reader.

Are these limitations that same pattern under a different tag? Go statement by statement for those below. For each, say what a reader could do differently because it is present, and what would be lost if it were deleted. Where a limitation only restates what the surrounding text already implies, say so. If some earn their place and others do not, distinguish them.

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

=== EVIDENCE ABS-0004 v9 sections 4.3 and 4.4 ===
### 4.3 ModelIdentity

`[DEF]` The stable identity of a model release used for provenance:
`model_id`, `originator_id` (developing organization), canonical name,
release/version identity where establishable. Deprecation is mutable and
endpoint-specific; it lives in catalog assertions.

`[DEF]` An invocation's event-time identity resolution and the current
assessment of that resolution are distinct facts. The event-time resolution is
bound to the evidence available when the invocation occurred. A later
assessment is recorded separately and linked to that historical resolution.

`[DEF]` `identity_verification_status` is the immutable capture-time status of
the executor reference in an InvocationRecord. It is not a later identity
resolution outcome or the current assessment of one. `unresolved` means
the capture path did not establish an executor-kind-specific stable identity.
`verified` means an admitted capture path established a unique identity under a
property-scoped verification rule and durably recorded or referenced the
identity, supporting evidence, verifier, rule or test version, and verification
time.

`[LIMITATION]` InvocationRecord schema v1 accepts `verified`, but no admitted
schema-v1 capture path can presently substantiate it: the current path performs
no identity resolution, and provider catalog self-report, even over an
authenticated channel, does not independently establish a model mapping. It
therefore emits `unresolved`. Later append-only identity resolution records do
not mutate or upgrade this field; validator acceptance of `verified` is
syntactic compatibility, not a licensed status.

`[PROPOSED_CONSTRAINT]` An invocation records the most precise ModelIdentity
resolution establishable from evidence available at execution time; an
unresolved requested name is recorded as unresolved and is never silently
substituted. Later evidence that a relied-on catalog assertion was stale,
contradicted, or wrong does not overwrite the event-time resolution.

### 4.4 CatalogSnapshot and CatalogAssertion

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic and records only
the claim: `assertion_subject`, `assertion_predicate`,
`assertion_value_or_target`, unit, scope, `valid_from`,
`valid_until`/superseded, source. An assertion may concern an API alias, an
endpoint, a price, a region, or a model identity. Example atomic assertions:
(api-name-X, resolves_to, model-identity-Y); (api-name-X, context_limit,
400000, tokens).

`[DEF]` A CatalogAssertion records what its named source asserted at the
snapshot's observed time. A provider-controlled catalog response is an
attributed provider self-report. Authentication of the endpoint and integrity
of the captured payload may establish who supplied which bytes at a time; they
do not independently establish the truth of the asserted model mapping,
capability, price, region, or identity.

`[DEF]` Verification of a property concerning a CatalogAssertion is represented
by a VerificationRun (Section 4.17), separate from the assertion. The
VerificationRun identifies the property assessed, the evidence used, and the
result.

`[PROPOSED_CONSTRAINT]` A provider assertion alone never supports an
unqualified `verified` status. Any verification claim concerning a
CatalogAssertion is limited to the named property its evidence establishes.

`[DEF]` Catalog assertions record what a provider claims; they never record
suitability for an AI-Lab role.

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

=== QUESTION Q2 ===
v9 adds nine [LIMITATION] statements, a category defined as "a descriptive boundary on what the ontology, its records, or current enforcement establish. A limitation imposes no constraint and claims no adoption."

A prior synthesis characterised v8's failure mode as: a failed control retained in control-shaped language, wrapped in an accurate disclaimer, and delegated to a future mechanism or a careful reader.

Are these limitations that same pattern under a different tag? Go statement by statement for those below. For each, say what a reader could do differently because it is present, and what would be lost if it were deleted. Where a limitation only restates what the surrounding text already implies, say so. If some earn their place and others do not, distinguish them.

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

=== EVIDENCE ABS-0004 v9 sections 4.3 and 4.4 ===
### 4.3 ModelIdentity

`[DEF]` The stable identity of a model release used for provenance:
`model_id`, `originator_id` (developing organization), canonical name,
release/version identity where establishable. Deprecation is mutable and
endpoint-specific; it lives in catalog assertions.

`[DEF]` An invocation's event-time identity resolution and the current
assessment of that resolution are distinct facts. The event-time resolution is
bound to the evidence available when the invocation occurred. A later
assessment is recorded separately and linked to that historical resolution.

`[DEF]` `identity_verification_status` is the immutable capture-time status of
the executor reference in an InvocationRecord. It is not a later identity
resolution outcome or the current assessment of one. `unresolved` means
the capture path did not establish an executor-kind-specific stable identity.
`verified` means an admitted capture path established a unique identity under a
property-scoped verification rule and durably recorded or referenced the
identity, supporting evidence, verifier, rule or test version, and verification
time.

`[LIMITATION]` InvocationRecord schema v1 accepts `verified`, but no admitted
schema-v1 capture path can presently substantiate it: the current path performs
no identity resolution, and provider catalog self-report, even over an
authenticated channel, does not independently establish a model mapping. It
therefore emits `unresolved`. Later append-only identity resolution records do
not mutate or upgrade this field; validator acceptance of `verified` is
syntactic compatibility, not a licensed status.

`[PROPOSED_CONSTRAINT]` An invocation records the most precise ModelIdentity
resolution establishable from evidence available at execution time; an
unresolved requested name is recorded as unresolved and is never silently
substituted. Later evidence that a relied-on catalog assertion was stale,
contradicted, or wrong does not overwrite the event-time resolution.

### 4.4 CatalogSnapshot and CatalogAssertion

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic and records only
the claim: `assertion_subject`, `assertion_predicate`,
`assertion_value_or_target`, unit, scope, `valid_from`,
`valid_until`/superseded, source. An assertion may concern an API alias, an
endpoint, a price, a region, or a model identity. Example atomic assertions:
(api-name-X, resolves_to, model-identity-Y); (api-name-X, context_limit,
400000, tokens).

`[DEF]` A CatalogAssertion records what its named source asserted at the
snapshot's observed time. A provider-controlled catalog response is an
attributed provider self-report. Authentication of the endpoint and integrity
of the captured payload may establish who supplied which bytes at a time; they
do not independently establish the truth of the asserted model mapping,
capability, price, region, or identity.

`[DEF]` Verification of a property concerning a CatalogAssertion is represented
by a VerificationRun (Section 4.17), separate from the assertion. The
VerificationRun identifies the property assessed, the evidence used, and the
result.

`[PROPOSED_CONSTRAINT]` A provider assertion alone never supports an
unqualified `verified` status. Any verification claim concerning a
CatalogAssertion is limited to the named property its evidence establishes.

`[DEF]` Catalog assertions record what a provider claims; they never record
suitability for an AI-Lab role.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
Only four of the nine `[LIMITATION]` statements are in the evidence. The other five cannot be assessed without their text.

Because v9 is proposed and not admitted, none of these statements has governance force. Even if retained, they can inform interpretation but cannot themselves require conduct or prevent a contrary record.

| Limitation | What a reader can do differently | What deletion loses / overlap | Same failed-control pattern? |
|---|---|---|---|
| Authority claims and records do not themselves establish a principal’s extra-systemic entitlement to govern. | Do not treat an `AccountablePrincipal`, an `authority_scope`, delegation, or a complete-looking authorization record as proof that the purported principal actually has authority outside the repository. Seek the relevant external source of authority before drawing that conclusion. | The surrounding material distinguishes authorization records and identifies an unresolved authorization-chain bootstrap question, but it does not otherwise expressly separate recorded authority claims from the real-world entitlement claimed. Deletion would leave a substantial inferential gap. | No, not primarily. It does not prescribe a control, imply that a control exists, or defer enforcement. It marks a boundary between attribution in records and external legitimacy. It earns its place as an epistemic boundary, though it supplies no mechanism for obtaining or evaluating extra-systemic authority. |
| A recorded authorization-chain terminus identifies where the represented chain stops, not whether the invocation is substantively authorized. | Treat a chain endpoint as provenance information about the representation, rather than proof that the chain is valid, complete, or grounded in valid authority. Examine the substantive basis separately. | This substantially overlaps the preceding limitation: both reject an inference from a record to actual authority. It also follows from the `[OPEN]` bootstrap issue. Still, it addresses a narrower but plausible erroneous inference: that finding an endpoint resolves authorization. Deletion would lose that targeted clarification, but not the general principle. | Not a failed control in the stated sense. It does not simulate enforcement. It is somewhat repetitive of the first limitation and the `[OPEN]` item, but its specificity can help prevent endpoint-equals-validity reasoning. |
| Record and relation requirements expose only what was declared, recorded, linked, traversable, and correctly attributed; they do not establish completeness of material invocations, inputs, dependencies, or external interactions. | Avoid treating the absence of a node, relation, authorization, input, or dependency in a repository graph as evidence that it did not exist. Seek corroboration, compare against external traces where available, and qualify negative conclusions. | The supplied text says undeclared subordinate execution is a disclosure violation, but that does not establish that all such executions will be declared or discovered. Nor do the record definitions establish completeness. Deletion would remove the clearest warning against completeness and absence inferences. | No. This is a genuine scope limitation of record-based evidence. It is not a substitute for a completeness control, and it does not pretend to provide one. It earns its place, while leaving the underlying completeness problem unresolved. |
| Schema v1 accepts `verified`, but no admitted schema-v1 capture path presently substantiates it; the current path emits `unresolved`; later resolution does not mutate the field; validator acceptance is syntactic rather than a licensed status. | A reader should not infer that a syntactically accepted `verified` value is evidentially valid. For records produced by the described current path, treat the capture-time status as `unresolved`; treat later identity work as separate append-only resolution evidence rather than an upgrade of the historical capture field. | Parts restate surrounding definitions: the field is immutable capture-time status, `verified` has stated evidentiary prerequisites, and later assessment is distinct. But the limitation adds material current-state facts not supplied elsewhere: no admitted schema-v1 path presently supports `verified`, the current path emits `unresolved`, and validator acceptance does not establish entitlement to the status. Deletion would therefore lose operationally important information. | This is the closest to the prior failure pattern. “Validator acceptance” combined with “not a licensed status” identifies a system that accepts the value while relying on readers to distinguish syntax from evidentiary validity. The limitation accurately discloses that gap, but—being non-constraint text—does not stop a record from carrying `verified` or establish an admission check that rejects it. Thus it earns a place as disclosure, but it cannot be treated as the control that the wording may lead a careful reader to wish existed. |

Overall: the first three are principally descriptive limits on what repository records can establish. They do not appear to retain a failed control under a new tag; they instead prevent overclaiming from records and chains. The fourth is also descriptively useful, but it exposes rather than resolves a control gap: syntactic acceptance remains distinct from substantiated status, and the limitation itself cannot bridge that gap.
```

## Claude Response

- model: `claude-sonnet-5`

```
## Preliminary: evidence gap

v9 is said to add nine `[LIMITATION]` statements. Only four appear in the evidence supplied:

- Section 3: the AccountablePrincipal/authority_scope limitation
- Section 3: the authorization-chain terminus limitation
- Section 3: the record/relation completeness limitation
- Section 4.3: the `identity_verification_status`/`verified` limitation

I cannot go "statement by statement" for the other five — I don't have them. Naming what's missing: the remaining five `[LIMITATION]` statements themselves, and also the full `[DEF]` text for `AccountablePrincipal` and `authority_scope` (only referenced, not quoted here) and the definition of "record and relation requirements" that Limitation 3 characterizes. Without those DEFs I can't fully judge whether some limitations merely restate what their own surrounding definitions already scope. I'll flag that at each relevant point below.

## Statement by statement

**1. "Repository records do not by themselves establish a principal's extra-systemic entitlement to govern."**

What a reader can do differently: treat a recorded `authority_scope` or delegation chain as a claim, not as proof — and go looking for something outside the repository (a charter, a signed grant, an external role assignment) before relying on it to authorize anything consequential.

What is lost if deleted: nothing textually stops a reader from equating "recorded as AccountablePrincipal" with "actually entitled." The limitation blocks that specific inference.

Restates the surrounding text? The `AccountablePrincipal`/`authority_scope` `[DEF]` is not in evidence, so I can't confirm whether this is new information or just a paraphrase of a scope already stated there. Missing: that DEF text.

Pattern check: no formal apparatus is retained here that pretends to do more than it does — it's a plain boundary statement, not a disguised control. Does not obviously match the v8 pattern.

**2. "A recorded authorization-chain terminus identifies where the represented chain stops. It does not by itself establish that the underlying invocation is substantively authorized."**

What a reader can do differently: not treat reaching a terminus (standing policy, delegated authority, AccountablePrincipal scope) as closing the authorization question, even once the `[OPEN]` bootstrap problem above it is eventually resolved.

What is lost if deleted: a reader could conflate "the chain has a recorded stopping point" with "the invocation was properly authorized."

Restates the surrounding text? This is very close to being a direct corollary of the `[OPEN]` item immediately above it ("Authorization-chain bootstrap: how an authorization chain terminates … rather than requiring an infinite sequence of prior authorizations"). If the bootstrap mechanism is openly unresolved, it already follows that a terminus can't establish substantive authorization. This limitation adds little beyond what the adjacent `[OPEN]` tag already signals — it should be flagged as largely restating what the surrounding text implies, unless the intent is specifically to cover the case *after* bootstrap is eventually resolved, which the text doesn't say.

**3. "Record and relation requirements expose only what was declared, recorded, linked, traversable, and correctly attributed. They do not establish that every material invocation, authorization, input, dependency, or external interaction is present in the record."**

What a reader can do differently: stop treating traceability/linkage completeness (the thing the "record and relation requirements" apparently check) as evidence of factual completeness — i.e., know that absence of a record is not evidence of absence of the event.

What is lost if deleted: a reader relying on the graph of records could mistake "everything links up" for "everything that happened is here."

Restates the surrounding text? I don't have the definition of "record and relation requirements" this refers to, so I can't say whether it already states this scope. Missing: the section defining those requirements.

Pattern check: like #1, this is a plain closed-world disclaimer, not a retained mechanism dressed as something it isn't. It doesn't delegate a fix to "a future mechanism" — it states a permanent boundary and stops there. This is the shape of a limitation that does real, if generic, work: it forecloses a specific and plausible misreading (linkage = completeness).

**4. The `identity_verification_status`/`verified` limitation**

Text: schema v1 still syntactically accepts a `verified` value; no admitted capture path can currently substantiate it; it therefore emits `unresolved`; later identity-resolution records don't upgrade the field; "validator acceptance of `verified` is syntactic compatibility, not a licensed status."

What a reader can do differently: know that if a record ever shows `identity_verification_status: verified`, that fact alone is not evidence of anything — it must be checked against whether an admitted capture path existed, because the schema will accept the value regardless.

What is lost if deleted: without this limitation, nothing else in the quoted text says that `verified` passing validation is meaningless under the current schema. A reader would have no warning that the schema's own vocabulary outruns what any current process can actually establish.

Is this the same pattern as v8, under a different tag? This is the one that fits the described failure mode most closely:

- The failed control: the schema still defines and accepts a `verified` status — a formal apparatus that reads as though it certifies something (it lists what `verified` is supposed to mean: "an admitted capture path established a unique identity … and durably recorded … the identity, supporting evidence, verifier, rule or test version, and verification time"). That apparatus is *retained*, not removed, even though the text itself says no path can currently earn it.
- Control-shaped language: yes — an enumerated status field with defined semantics functions exactly like a constraint field, even while carrying a `[LIMITATION]` tag that "imposes no constraint."
- Wrapped in an accurate disclaimer: yes, this passage is accurate and says so plainly.
- Delegated to a future mechanism or a careful reader: both. It's delegated to "a careful reader" (must remember `verified` is currently unearnable and validator acceptance is "syntactic" only), and implicitly to a future mechanism (an admitted capture path that doesn't yet exist). Nothing in the quoted text — no `[PROPOSED_CONSTRAINT]`, no schema change — actually prevents a `verified` value from being written by some path other than the described one (manual entry, migration, a future capture path nobody has vetted) and passing validation regardless. The limitation describes the gap; it doesn't close it.

So of the four available, this is the strongest candidate for "same pattern, different tag": a status value that looks like it certifies something, is kept live in the schema, and is defused only by prose that a reader has to carry forward, rather than by a constraint that would make the schema itself refuse an unsupportable `verified` entry.

## Summary

- Limitation 4 (`verified`/`identity_verification_status`) most closely reproduces the v8 pattern: a schema-level apparatus with control-shaped semantics is retained, accurately disclaimed, and left to reader vigilance rather than closed off.
- Limitation 2 (chain terminus) is largely redundant with the adjacent `[OPEN]` item and adds little independent content.
- Limitations 1 and 3 are plain, non-control-shaped epistemic boundaries that block specific plausible misreadings (recorded authority ≠ real entitlement; linkage completeness ≠ factual completeness); I can't fully judge their redundancy without the `AccountablePrincipal`/`authority_scope` DEF and the "record and relation requirements" definition, which are not in evidence.
- Five of the nine `[LIMITATION]` statements are not in the evidence set at all and cannot be assessed here; they would be needed to say whether the pattern holds across the full set or only for a subset.
```
