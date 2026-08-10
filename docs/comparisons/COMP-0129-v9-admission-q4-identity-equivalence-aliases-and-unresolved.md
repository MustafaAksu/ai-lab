# COMP-0129: Provider Comparison — v9 admission Q4 identity-equivalence-aliases-and-unresolved

## Metadata

- comparison_id: `COMP-0129`
- title: `v9 admission Q4 identity-equivalence-aliases-and-unresolved`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-8bb8e8326599429f.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0129", "target_id": "INV-8bb8e8326599429f"}, {"authoritative": false, "evidence": "docs/invocations/INV-5d51b22e6fe02a80.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0129", "target_id": "INV-5d51b22e6fe02a80"}]`
- created_at: `2026-08-10T10:27:29.871767+00:00`
- command: `scripts/compare_providers.py --title v9 admission Q4 identity-equivalence-aliases-and-unresolved You are reviewing a proposed ontology amendment. This is ONE question of eight, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

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

=== QUESTION Q4 ===
v9 states that identity_verification_status is the immutable capture-time status of an executor reference, that the value verified means an admitted capture path established a unique identity under a property-scoped verification rule, and that no admitted capture path can presently substantiate it. Every captured record carries unresolved.

Constraint C3 forbids an invocation from adjudicating a claim whose evidence ancestry contains an invocation by an equivalent executor identity.

This is live rather than hypothetical: the executor that drafted v9 self-reports as gpt-5.6-thinking, and one reviewer in this round is gpt-5.6-terra. The provider's catalog asserts they are distinct identities. That catalog is a provider self-report.

Can two executor references be shown NOT equivalent under this ontology? If equivalence can never be established and non-equivalence can never be established either, state what C3 does in practice, and whether independence_unresolved carries any information that distinguishes one pairing from another. If the honest consequence is that C3 cannot be satisfied, say so and say what follows.

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

=== EVIDENCE ABS-0004 v9 constraint C3, no self-adjudication ===
`[INHERITED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
invocation cannot adjudicate a claim whose evidence ancestry contains an
invocation by an equivalent executor identity, with equivalence defined
per executor kind: ModelIdentity resolution equality for models;
tool identity and version equality for tools; principal equality for
humans. Direct lineage conflict: hard prohibition, no exception.
Equivalent-identity conflict: hard prohibition absent a future explicitly
governed exceptional procedure. Unknown or unresolved executor equivalence
cannot establish identity independence; it yields
`independence_unresolved`, never an independent path. An identity
unresolved at one endpoint and resolved at another is treated as distinct
until equivalence is affirmatively established; distinctness never
increases independence (P5).

=== EVIDENCE ABS-0004 v9 constraint C3 and neighbours ===
`[INHERITED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
invocation cannot adjudicate a claim whose evidence ancestry contains an
invocation by an equivalent executor identity, with equivalence defined
per executor kind: ModelIdentity resolution equality for models;
tool identity and version equality for tools; principal equality for
humans. Direct lineage conflict: hard prohibition, no exception.
Equivalent-identity conflict: hard prohibition absent a future explicitly
governed exceptional procedure. Unknown or unresolved executor equivalence
cannot establish identity independence; it yields
`independence_unresolved`, never an independent path. An identity
unresolved at one endpoint and resolved at another is treated as distinct
until equivalence is affirmatively established; distinctness never
increases independence (P5).

`[PROPOSED_CONSTRAINT]` C4 No hidden witness reuse: an invocation that
consumed another witness's output is not an independent confirmation of
that testimony; it may count as synthesis or critique.

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

=== QUESTION Q4 ===
v9 states that identity_verification_status is the immutable capture-time status of an executor reference, that the value verified means an admitted capture path established a unique identity under a property-scoped verification rule, and that no admitted capture path can presently substantiate it. Every captured record carries unresolved.

Constraint C3 forbids an invocation from adjudicating a claim whose evidence ancestry contains an invocation by an equivalent executor identity.

This is live rather than hypothetical: the executor that drafted v9 self-reports as gpt-5.6-thinking, and one reviewer in this round is gpt-5.6-terra. The provider's catalog asserts they are distinct identities. That catalog is a provider self-report.

Can two executor references be shown NOT equivalent under this ontology? If equivalence can never be established and non-equivalence can never be established either, state what C3 does in practice, and whether independence_unresolved carries any information that distinguishes one pairing from another. If the honest consequence is that C3 cannot be satisfied, say so and say what follows.

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

=== EVIDENCE ABS-0004 v9 constraint C3, no self-adjudication ===
`[INHERITED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
invocation cannot adjudicate a claim whose evidence ancestry contains an
invocation by an equivalent executor identity, with equivalence defined
per executor kind: ModelIdentity resolution equality for models;
tool identity and version equality for tools; principal equality for
humans. Direct lineage conflict: hard prohibition, no exception.
Equivalent-identity conflict: hard prohibition absent a future explicitly
governed exceptional procedure. Unknown or unresolved executor equivalence
cannot establish identity independence; it yields
`independence_unresolved`, never an independent path. An identity
unresolved at one endpoint and resolved at another is treated as distinct
until equivalence is affirmatively established; distinctness never
increases independence (P5).

=== EVIDENCE ABS-0004 v9 constraint C3 and neighbours ===
`[INHERITED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
invocation cannot adjudicate a claim whose evidence ancestry contains an
invocation by an equivalent executor identity, with equivalence defined
per executor kind: ModelIdentity resolution equality for models;
tool identity and version equality for tools; principal equality for
humans. Direct lineage conflict: hard prohibition, no exception.
Equivalent-identity conflict: hard prohibition absent a future explicitly
governed exceptional procedure. Unknown or unresolved executor equivalence
cannot establish identity independence; it yields
`independence_unresolved`, never an independent path. An identity
unresolved at one endpoint and resolved at another is treated as distinct
until equivalence is affirmatively established; distinctness never
increases independence (P5).

`[PROPOSED_CONSTRAINT]` C4 No hidden witness reuse: an invocation that
consumed another witness's output is not an independent confirmation of
that testimony; it may count as synthesis or critique.

--- END OF EVIDENCE ---

Answer only the question above. If the evidence set is insufficient, say so and name what is missing.

## OpenAI Response

- model: `gpt-5.6-terra`

```
On the supplied text, these two executor references cannot be shown non-equivalent.

For models, C3 defines equivalence as “ModelIdentity resolution equality.” But the evidence provides no admitted capture-time path that can substantiate `verified`; current records emit `unresolved`. The provider catalog’s assertion that `gpt-5.6-thinking` and `gpt-5.6-terra` are distinct is only an attributed provider self-report and “does not independently establish the truth” of the asserted identity mapping. It therefore cannot establish inequality of their ModelIdentity resolutions.

Nor does the supplied text provide an affirmative procedure or evidentiary rule for establishing *non*-equivalence. “An identity unresolved at one endpoint and resolved at another is treated as distinct until equivalence is affirmatively established” is an operational treatment, not an independently supported finding that the identities are non-equivalent. C3 expressly adds that this distinct treatment “never increases independence.”

Accordingly, for the disclosed pairing, the available result is `independence_unresolved`, not independent and not an established equivalent-identity conflict.

If neither equivalence nor non-equivalence can be established, C3 has these practical effects:

* A direct-lineage conflict remains a hard prohibition and does not depend on executor-identity resolution.
* An affirmatively established equivalent-identity conflict is a hard prohibition.
* An unresolved pairing cannot be used as an independent path. The text does not permit “different requested names,” “different endpoints,” or a provider’s distinctness assertion to cure that problem.
* The supplied C3 text does **not** expressly state that an `independence_unresolved` invocation may not adjudicate at all. It says such a pairing is “never an independent path.” Thus, on this evidence, it can at most support a non-independent synthesis or critique; whether it may perform any adjudication whose acceptance does not require independence is not specified.

`independence_unresolved` carries limited information: it distinguishes an unresolved relationship from an affirmatively established equivalent-identity conflict, and it records that independence has not been established. It does not distinguish one unresolved pairing from another in any independence-relevant way. All such pairings are barred from counting as independent, regardless of whether their names, endpoints, or provider assertions differ.

It would be too strong to say that C3 is wholly impossible to satisfy: it can still apply to direct lineage and to identities whose equivalence is affirmatively established. But if “satisfy C3” means demonstrate that this reviewer is an independent adjudicator of the drafter’s work, then C3 cannot be satisfied for the disclosed pairing using the supplied evidence. The consequence is that this reviewer’s result cannot be treated as an independent review path; calling it independent would contradict C3’s stated rule.

Missing material that would be needed to determine whether non-equivalence can ever be affirmatively established, and what an unresolved adjudication is permitted to do:

* **Section 4.17, VerificationRun** — to determine whether it defines a property-scoped verification rule capable of establishing identity inequality or only particular positive identity claims.
* **The schema and rules for later append-only identity resolution records** — to determine how ModelIdentity resolutions are represented, compared, and evidentially admitted after capture time.
* **P5**, cited by C3 but not supplied — to determine the governing consequence of “distinctness never increases independence.”
* **Any rule defining adjudication acceptance or the required status of an adjudicator** — to determine whether `independence_unresolved` merely prevents an independence claim or bars the adjudication from being accepted at all.
```

## Claude Response

- model: `claude-sonnet-5`

```
**Can non-equivalence be shown?**

No. Equivalence under C3 is defined, for models, as "ModelIdentity resolution equality." Section 4.3 states that `identity_verification_status` is "the immutable capture-time status of the executor reference," that `verified` requires "an admitted capture path" to have "established a unique identity under a property-scoped verification rule," and then states flatly: "no admitted schema-v1 capture path can presently substantiate it: the current path performs no identity resolution, and provider catalog self-report, even over an authenticated channel, does not independently establish a model mapping. It therefore emits `unresolved`." The evidence also states "Every captured record carries unresolved."

The only artifact offered as evidence for the live pairing — the provider's catalog assertion that gpt-5.6-thinking and gpt-5.6-terra are distinct — is exactly the kind of evidence Section 4.4 excludes from probative force: "A provider-controlled catalog response is an attributed provider self-report... [Authentication and integrity] do not independently establish the truth of the asserted model mapping, capability, price, region, or identity." So the catalog assertion cannot establish non-equivalence any more than it could establish equivalence. Neither direction is available under any admitted capture path disclosed here.

**What C3 does in practice**

C3's hard prohibition is worded to trigger on an *established* "equivalent-identity conflict." Since equivalence can never be affirmatively established (no admitted path substantiates `verified` identity resolution), that trigger condition is, in practice, never affirmatively met for model executors. But C3 does not let absence-of-proof-of-equivalence stand in for proof of independence either: "Unknown or unresolved executor equivalence cannot establish identity independence; it yields `independence_unresolved`, never an independent path."

So C3 collapses to a permanent third state for model-executor pairings: not provably equivalent (so the literal hard-prohibition clause doesn't fire), and not provably independent (so no invocation can be certified clear). It cannot be triggered and it cannot be satisfied — it just sits at `independence_unresolved` regardless of what any invocation does downstream. The constraint is evidentially inert for the model-identity case as currently instrumented; the only case where it can actually operate is where equivalence is affirmatively knowable some other way (e.g. the "direct lineage conflict" branch, which is not evidenced here and which I don't have text for beyond the phrase itself — I'd want the fuller lineage-conflict definition, not disclosed in this evidence set, to know what does trigger it).

**Does `independence_unresolved` distinguish pairings?**

No. Because "every captured record carries unresolved," the label attaches identically to the gpt-5.6-thinking/gpt-5.6-terra pairing, to a pairing of two admittedly-identical executor references, and to a pairing of two executors the catalog calls unrelated. The status is a constant produced by the capture path's limitation, not a measurement of the pairing itself. It carries no information that would let this round's two-reviewer-slot design be treated as more independent than a single-reviewer design would have been.

**Honest consequence**

C3 cannot be satisfied — not in the sense of being violated, but in the sense that it can never be *affirmatively discharged*. It can never certify "these two executor references are independent," because the definitional path to that certification (ModelIdentity resolution equality/inequality via an admitted capture path) does not exist for schema-v1 records, and the one substitute evidentiary source available in this round — provider catalog self-report — is explicitly disqualified by 4.4's own definition. The disclosed fact that "nothing establishes that the drafter and this reviewer are different executors, and nothing establishes that they are the same" is therefore not a gap in this particular round's evidence; it is the structurally guaranteed outcome for every round under the current ontology text. `[INHERITED_CONSTRAINT]` C3 renames v8's tag but does not supply the missing capture path; whether v9's tag "works" (per disclosure 2) — it does not, for this purpose, because the underlying evidentiary problem it was meant to answer is untouched.

**Missing evidence I would want:** the full text of Section 4.17 (VerificationRun) to check whether any verification path other than catalog self-report could ever substantiate ModelIdentity resolution equality/inequality; the full text of P5 (cited parenthetically as "distinctness never increases independence (P5)") to see whether it supplies any operative rule beyond the fragment quoted; and the fuller definition distinguishing "direct lineage conflict" from "equivalent-identity conflict," since only the former appears to be a live trigger for C3 and I have only the label, not its criteria.
```
