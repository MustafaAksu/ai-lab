# COMP-0139: Provider Comparison — v9.1 re-review R5 are-the-inherited-challenge-questions-fit

## Metadata

- comparison_id: `COMP-0139`
- title: `v9.1 re-review R5 are-the-inherited-challenge-questions-fit`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-2964a94f7deeb1c4.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0139", "target_id": "INV-2964a94f7deeb1c4"}, {"authoritative": false, "evidence": "docs/invocations/INV-29b83174d546c0eb.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0139", "target_id": "INV-29b83174d546c0eb"}]`
- created_at: `2026-08-11T14:20:21.268573+00:00`
- command: `scripts/compare_providers.py --title v9.1 re-review R5 are-the-inherited-challenge-questions-fit You are reviewing a proposed ontology amendment. This is ONE question of five, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9.1 is proposed and not admitted. v4 is the last version with an admission event. v9.1 has no governance force.

Disclosures:

1. v9.1 is the CORRECTED successor to v9. A prior round, COMP-0126 to COMP-0134, found eight defects in v9; all eight were accepted by the operator and answered. You are reviewing the answers, not the original. Do not assume a correction is sound because it was made in response to a finding.

2. THIS IS A RE-RUN. Each of these five questions was asked of v9 and returned an answer qualified by insufficient evidence. The evidence sets were the question author's choices, and they were wrong. If this evidence set is still insufficient, say so and name precisely what is missing; that report is wanted output and the last round's version of it is why this round exists.

3. The executor that drafted v9, the corrections, and the version bump self-reports as gpt-5.6-thinking. One reviewer slot in this round is gpt-5.6-terra. The provider's own catalog asserts these are distinct model identities, and that catalog is a provider self-report. Nothing establishes whether they are the same executor. Under the corrected C3 you are reading, an invocation may not adjudicate a claim whose evidence ancestry contains an executor of unresolved equivalence. Your output is evidence for the accountable principal, not an adjudication.

4. The question author drafted ABS-0004 v5 through v8, all withdrawn or superseded, and drafted none of v9 or v9.1.

Answer in whatever form fits, but include three things: a VERDICT SENTENCE before the reasoning; any evidence you needed and did not have; and anything you found that this question did not ask about.

Quote only text that appears below. Do not certify or praise. No provider product recommendations.

=== QUESTION R5 ===
Section 13 lists fourteen challenge-round questions. They were written for the v3 to v4 round and have been carried through v5, v6, v7, v8, v9 and v9.1 unchanged. Nobody has revisited them.

The v9 round asked this and supplied only the question list and the metadata; one reviewer could substantively assess one of the fourteen. The constraints and the enforcement matrix those questions refer to are now attached.

For each of the fourteen: answered, stale, still live, or unassessable on this evidence. At least one is stale on its face, asking whether "candidate Slice A" omits anything when Slice A is implemented and warranted.

Then state what the set does not ask. A question set inherited across six versions encodes the concerns of the version that wrote it; name the concerns of v9.1 it fails to cover, including any raised by the eight corrections just made.

=== DECLARED OMISSIONS ===
- Section 4 object definitions, which several challenge questions reference by number. Attaching Section 4 would put this prompt over the size that has been demonstrated to complete. Where a question cannot be assessed without a definition, say which definition and treat that question as unassessed rather than guessing.

=== EVIDENCE Section 13, Challenge-Round Questions ===
## 13. Challenge-Round Questions

1. Which objects are missing; which defined objects are category errors?
2. Which constraints are unenforceable as stated; what minimal
   representable form makes them enforceable?
3. Construct a concrete invocation satisfying the three-axis Role
   definitions while violating authority separation.
4. Construct a laundering path from a pre-provenance artifact into
   high-consequence independent evidence that survives C9 and C10.
5. Does candidate Slice A omit anything without which the provenance graph
   cannot later answer the witness-independence question?
6. Identify any predicate ambiguous enough to produce divergent
   implementations.
7. Where is invocation authorization represented; how is it distinguished
   from routing and evidence admission; does the distinction hold under
   composition?
8. Can the ontology represent one model served through different
   organizations, endpoints, regions, or mutable aliases without creating
   false model independence?
9. Does provenance as specified apply to claim derivation or only artifact
   production, and where exactly does the artifact-level approximation
   break?
10. What must an effective-input record contain before an invocation may be
    treated as blind?
11. Which constraints apply identically to models, tools, and humans; which
    require executor-specific rules?
12. Under what conditions, if any, can an unresolved model identity qualify
    as an independent witness path? Identify the failure behavior when
    equivalence cannot be resolved.
13. Construct a composite tool that satisfies the disclosure constraints'
    letter (4.7, both) while still exercising undeclared authority.
14. Construct a case where property-scoped verification (P2) plus validator
    lineage marking (C10) still admits a generator-authored blind spot into
    governed evidence.

Do not recommend specific provider products in this round.

=== EVIDENCE Section 6, Epistemic Constraints, carrying every constraint C1 to C11 ===
## 6. Epistemic Constraints

`[PROPOSED_CONSTRAINT]` C1 Staged provenance completeness. Provenance
profiles activate in stages; a governed output created after activation of
the applicable profile is admissible only if it satisfies that profile:
provenance_v1 (producing invocation; executor identity;
EffectiveInputManifest; session-state mode; ExecutionProfile; output
record; timestamps; model-specific identity and catalog fields required
only when a model participated as executor or execution resource);
authorization_v1 (role assignment, qualification, consequence class,
invocation authorization); lineage_v1 (input/claim ancestry and
independence assessment).

`[PROPOSED_CONSTRAINT]` C2 Catalog admission: an execution candidate
(executor within a qualification's execution scope, 4.6) may serve a
governed role only when the role's required catalog claims are satisfied at
the role's freshness requirements. Experimental execution is permitted;
experimental outputs cannot silently enter governed evidence.

`[PROPOSED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
invocation cannot adjudicate a claim whose evidence ancestry contains an
invocation by an equivalent executor identity, with equivalence defined
per executor kind: ModelIdentity resolution equality for models;
tool identity and version equality for tools; principal equality for
humans. Direct lineage conflict: hard prohibition, no exception.
Equivalent-identity conflict: hard prohibition absent a future explicitly
governed exceptional procedure. If equivalence between the adjudicating
executor and an executor in the claim's evidence ancestry is unresolved,
the adjudicating invocation may not adjudicate that claim while the relation
remains unresolved; the independence result is `independence_unresolved`, not
an independent path. An unresolved relation is not treated as distinct for
independence purposes and remains unresolved until equivalence or
non-equivalence is affirmatively established under the applicable
executor-kind identity semantics. A compensating control that leaves the
equivalence fact unresolved cannot license adjudication or increase
independence (P5).

`[PROPOSED_CONSTRAINT]` C4 No hidden witness reuse: an invocation that
consumed another witness's output is not an independent confirmation of
that testimony; it may count as synthesis or critique.

`[PROPOSED_CONSTRAINT]` C5 Lineage-based independence. Isolation from other
witness outputs is necessary for counting an invocation as independent
confirmation of those outputs, but not sufficient for witness-path
independence: shared erroneous sources, common leading prompts, shared
hidden state, and shared unsupported assumptions defeat it. Round labels
describe protocol; lineage determines admissibility. Independence is
assessed per dimension (information path, source, executor identity,
provider/organization correlation, prompt common cause, session-state
confidence, claim-lineage completeness), some of which are hard
disqualifiers. First implementations produce categorical statuses
(`qualified_independent` | `dependent` | `unresolved`) with
dimension-specific reasons; no single numeric score, and no claimed weight
function without evaluation evidence. Provider similarity is recorded as a
correlation factor.

`[INHERITED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another. Assignment independence
is not exercise license: adjudicator-level epistemic authority and
above-read_only action authority may not both be exercised within a single
invocation against the same target unless the adjudication is covered by
an independent verification edge; an invocation that mutates state it also
adjudicates collapses the separation C6 exists to preserve. COMP-0032
produced two constructions satisfying the axis definitions while defeating
separation; this sentence closes both.

`[LIMITATION]` Role, qualification, and authorization records are inputs to a
C6 evaluation. Their existence does not establish that the C6 exercise
restriction was evaluated or satisfied for a particular invocation.

`[INHERITED_CONSTRAINT]` C7 Implementation separation: an executor with
repository or external action authority may implement an admitted plan but
may not be the sole verifier or adjudicator of its own changes.

`[PROPOSED_CONSTRAINT]` C8 Decision traceability: every policy-selected
invocation has a reconstructible RoutingDecision or a governed
manual-override DecisionRecord (accountable principal, reason, scope,
review condition; never a free-text escape hatch).

`[INHERITED_CONSTRAINT]` C9 Conservative lineage inheritance (from P3): an
artifact grounded in pre-provenance or lineage-incomplete material inherits
`claim_lineage_status: source_lineage_partial` while recording
`source_provenance_status` of its sources (for example `pre_provenance`).
Structural transformation, including extraction, cannot improve the
provenance class of the information transformed. Extraction from
pre-provenance sources is permitted; its outputs carry
`source_provenance_status: pre_provenance`, `claim_lineage_status:
source_lineage_partial`, `independent_observation: false`.

Selection provenance (COMP-0032 finding): an invocation's effective inputs
include the selection criteria and priors used to choose its sources.
Undisclosed selection priors derived from pre-provenance or
lineage-incomplete material taint the selection even when every selected
source is independently clean; at high consequence, claims whose source
selection lacks disclosed selection provenance carry `claim_lineage_status:
source_lineage_partial`. Honest limitation: offline human reading is
unobservable, so this rule is only partially enforceable ever;
HumanActionRecord (Section 11) narrows but cannot close the gap, and the
ontology states this rather than pretending otherwise.

`[INHERITED_CONSTRAINT]` C11 Interim independence disclosure: until
claim-level lineage exists, witness-path independence counts are
artifact-level approximations, and both COMP-0032 witnesses independently
identified the resulting silent failure mode (N "independent" paths
satisfied by N copies of one unrecorded shared claim). Therefore any
high-consequence decision relying on a minimum number of independent
witness paths must disclose in its DecisionRecord that independence was
assessed at artifact level only, and must name the compensating controls
relied on (operator adjudication, source disclosure, deterministic
verification of the claims where available). Absent that disclosure, the
independence requirement is unmet, not silently satisfied.

`[INHERITED_CONSTRAINT]` C10 Validator lineage independence (property-scoped
P2 hardening): verifier provenance (identity, version, rule/test version,
inputs, environment, result) is always recorded. When the code, schema,
tests, or configuration driving a verification share evidence ancestry
with the ModelIdentity that produced the output under test, the
verification is marked `verifier_lineage: self_authored` and carries
reduced independence standing; the verified property claim stands only as
far as the verifier's scope and lineage permit. At high consequence,
admission requires either independently-lineaged verification or
independent review of the verifier. Self-authored verification is
governed, not prohibited: AI-Lab's existing compensating controls
(cross-environment reproduction, operator adjudication, provider
completion review) are recognized independent paths.

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

=== QUESTION R5 ===
Section 13 lists fourteen challenge-round questions. They were written for the v3 to v4 round and have been carried through v5, v6, v7, v8, v9 and v9.1 unchanged. Nobody has revisited them.

The v9 round asked this and supplied only the question list and the metadata; one reviewer could substantively assess one of the fourteen. The constraints and the enforcement matrix those questions refer to are now attached.

For each of the fourteen: answered, stale, still live, or unassessable on this evidence. At least one is stale on its face, asking whether "candidate Slice A" omits anything when Slice A is implemented and warranted.

Then state what the set does not ask. A question set inherited across six versions encodes the concerns of the version that wrote it; name the concerns of v9.1 it fails to cover, including any raised by the eight corrections just made.

=== DECLARED OMISSIONS ===
- Section 4 object definitions, which several challenge questions reference by number. Attaching Section 4 would put this prompt over the size that has been demonstrated to complete. Where a question cannot be assessed without a definition, say which definition and treat that question as unassessed rather than guessing.

=== EVIDENCE Section 13, Challenge-Round Questions ===
## 13. Challenge-Round Questions

1. Which objects are missing; which defined objects are category errors?
2. Which constraints are unenforceable as stated; what minimal
   representable form makes them enforceable?
3. Construct a concrete invocation satisfying the three-axis Role
   definitions while violating authority separation.
4. Construct a laundering path from a pre-provenance artifact into
   high-consequence independent evidence that survives C9 and C10.
5. Does candidate Slice A omit anything without which the provenance graph
   cannot later answer the witness-independence question?
6. Identify any predicate ambiguous enough to produce divergent
   implementations.
7. Where is invocation authorization represented; how is it distinguished
   from routing and evidence admission; does the distinction hold under
   composition?
8. Can the ontology represent one model served through different
   organizations, endpoints, regions, or mutable aliases without creating
   false model independence?
9. Does provenance as specified apply to claim derivation or only artifact
   production, and where exactly does the artifact-level approximation
   break?
10. What must an effective-input record contain before an invocation may be
    treated as blind?
11. Which constraints apply identically to models, tools, and humans; which
    require executor-specific rules?
12. Under what conditions, if any, can an unresolved model identity qualify
    as an independent witness path? Identify the failure behavior when
    equivalence cannot be resolved.
13. Construct a composite tool that satisfies the disclosure constraints'
    letter (4.7, both) while still exercising undeclared authority.
14. Construct a case where property-scoped verification (P2) plus validator
    lineage marking (C10) still admits a generator-authored blind spot into
    governed evidence.

Do not recommend specific provider products in this round.

=== EVIDENCE Section 6, Epistemic Constraints, carrying every constraint C1 to C11 ===
## 6. Epistemic Constraints

`[PROPOSED_CONSTRAINT]` C1 Staged provenance completeness. Provenance
profiles activate in stages; a governed output created after activation of
the applicable profile is admissible only if it satisfies that profile:
provenance_v1 (producing invocation; executor identity;
EffectiveInputManifest; session-state mode; ExecutionProfile; output
record; timestamps; model-specific identity and catalog fields required
only when a model participated as executor or execution resource);
authorization_v1 (role assignment, qualification, consequence class,
invocation authorization); lineage_v1 (input/claim ancestry and
independence assessment).

`[PROPOSED_CONSTRAINT]` C2 Catalog admission: an execution candidate
(executor within a qualification's execution scope, 4.6) may serve a
governed role only when the role's required catalog claims are satisfied at
the role's freshness requirements. Experimental execution is permitted;
experimental outputs cannot silently enter governed evidence.

`[PROPOSED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
invocation cannot adjudicate a claim whose evidence ancestry contains an
invocation by an equivalent executor identity, with equivalence defined
per executor kind: ModelIdentity resolution equality for models;
tool identity and version equality for tools; principal equality for
humans. Direct lineage conflict: hard prohibition, no exception.
Equivalent-identity conflict: hard prohibition absent a future explicitly
governed exceptional procedure. If equivalence between the adjudicating
executor and an executor in the claim's evidence ancestry is unresolved,
the adjudicating invocation may not adjudicate that claim while the relation
remains unresolved; the independence result is `independence_unresolved`, not
an independent path. An unresolved relation is not treated as distinct for
independence purposes and remains unresolved until equivalence or
non-equivalence is affirmatively established under the applicable
executor-kind identity semantics. A compensating control that leaves the
equivalence fact unresolved cannot license adjudication or increase
independence (P5).

`[PROPOSED_CONSTRAINT]` C4 No hidden witness reuse: an invocation that
consumed another witness's output is not an independent confirmation of
that testimony; it may count as synthesis or critique.

`[PROPOSED_CONSTRAINT]` C5 Lineage-based independence. Isolation from other
witness outputs is necessary for counting an invocation as independent
confirmation of those outputs, but not sufficient for witness-path
independence: shared erroneous sources, common leading prompts, shared
hidden state, and shared unsupported assumptions defeat it. Round labels
describe protocol; lineage determines admissibility. Independence is
assessed per dimension (information path, source, executor identity,
provider/organization correlation, prompt common cause, session-state
confidence, claim-lineage completeness), some of which are hard
disqualifiers. First implementations produce categorical statuses
(`qualified_independent` | `dependent` | `unresolved`) with
dimension-specific reasons; no single numeric score, and no claimed weight
function without evaluation evidence. Provider similarity is recorded as a
correlation factor.

`[INHERITED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another. Assignment independence
is not exercise license: adjudicator-level epistemic authority and
above-read_only action authority may not both be exercised within a single
invocation against the same target unless the adjudication is covered by
an independent verification edge; an invocation that mutates state it also
adjudicates collapses the separation C6 exists to preserve. COMP-0032
produced two constructions satisfying the axis definitions while defeating
separation; this sentence closes both.

`[LIMITATION]` Role, qualification, and authorization records are inputs to a
C6 evaluation. Their existence does not establish that the C6 exercise
restriction was evaluated or satisfied for a particular invocation.

`[INHERITED_CONSTRAINT]` C7 Implementation separation: an executor with
repository or external action authority may implement an admitted plan but
may not be the sole verifier or adjudicator of its own changes.

`[PROPOSED_CONSTRAINT]` C8 Decision traceability: every policy-selected
invocation has a reconstructible RoutingDecision or a governed
manual-override DecisionRecord (accountable principal, reason, scope,
review condition; never a free-text escape hatch).

`[INHERITED_CONSTRAINT]` C9 Conservative lineage inheritance (from P3): an
artifact grounded in pre-provenance or lineage-incomplete material inherits
`claim_lineage_status: source_lineage_partial` while recording
`source_provenance_status` of its sources (for example `pre_provenance`).
Structural transformation, including extraction, cannot improve the
provenance class of the information transformed. Extraction from
pre-provenance sources is permitted; its outputs carry
`source_provenance_status: pre_provenance`, `claim_lineage_status:
source_lineage_partial`, `independent_observation: false`.

Selection provenance (COMP-0032 finding): an invocation's effective inputs
include the selection criteria and priors used to choose its sources.
Undisclosed selection priors derived from pre-provenance or
lineage-incomplete material taint the selection even when every selected
source is independently clean; at high consequence, claims whose source
selection lacks disclosed selection provenance carry `claim_lineage_status:
source_lineage_partial`. Honest limitation: offline human reading is
unobservable, so this rule is only partially enforceable ever;
HumanActionRecord (Section 11) narrows but cannot close the gap, and the
ontology states this rather than pretending otherwise.

`[INHERITED_CONSTRAINT]` C11 Interim independence disclosure: until
claim-level lineage exists, witness-path independence counts are
artifact-level approximations, and both COMP-0032 witnesses independently
identified the resulting silent failure mode (N "independent" paths
satisfied by N copies of one unrecorded shared claim). Therefore any
high-consequence decision relying on a minimum number of independent
witness paths must disclose in its DecisionRecord that independence was
assessed at artifact level only, and must name the compensating controls
relied on (operator adjudication, source disclosure, deterministic
verification of the claims where available). Absent that disclosure, the
independence requirement is unmet, not silently satisfied.

`[INHERITED_CONSTRAINT]` C10 Validator lineage independence (property-scoped
P2 hardening): verifier provenance (identity, version, rule/test version,
inputs, environment, result) is always recorded. When the code, schema,
tests, or configuration driving a verification share evidence ancestry
with the ModelIdentity that produced the output under test, the
verification is marked `verifier_lineage: self_authored` and carries
reduced independence standing; the verified property claim stands only as
far as the verifier's scope and lineage permit. At high consequence,
admission requires either independently-lineaged verification or
independent review of the verifier. Self-authored verification is
governed, not prohibited: AI-Lab's existing compensating controls
(cross-environment reproduction, operator adjudication, provider
completion review) are recognized independent paths.

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
**VERDICT: On this evidence, Q5 is stale; Q9 and Q12 are answered; Q2, Q4, and Q11 are still live; and Q1, Q3, Q6–Q8, Q10, Q13, and Q14 are unassessable. This is an evidence assessment, not an adjudication of v9.1.**

| # | Classification | Reasoning |
|---|---|---|
| 1 | **Unassessable** | Determining missing objects and category errors requires the Section 4 object definitions. The supplied constraints and matrix do not enumerate the ontology’s objects or their categories. |
| 2 | **Still live** | The matrix identifies many constraints as having `none` representability, and the remainder as `partial`; it also identifies dependencies and proposed target enforcement. But it does not supply the requested minimal representable form for each unenforceable constraint. The question remains materially open. |
| 3 | **Unassessable** | C6 now prohibits the described joint exercise in an invocation, and says a prior construction was closed. But the question requires a construction satisfying the “three-axis Role definitions.” Those definitions are not supplied. Without them, it cannot be determined whether a proposed construction satisfies the definitions while defeating separation. |
| 4 | **Still live** | C9 blocks structural upgrading of pre-provenance information and marks extraction outputs `independent_observation: false`. It also recognizes a residual gap: “offline human reading is unobservable” and the selection-provenance rule is “only partially enforceable ever.” The matrix reports C9 as manual, with no named C9 attestation, and C10 as manual with no named C10 lineage-independence check. The text identifies mitigations and failure statuses, but does not establish that all laundering paths are prevented in practice or semantically excluded from every high-consequence admission path. |
| 5 | **Stale** | It asks whether “candidate Slice A” omits material necessary to answer witness independence, while the question states that Slice A is implemented and warranted. The question is framed as a candidate-completeness challenge for a pre-implementation state, rather than as a review of the implemented and warranted artifact. |
| 6 | **Unassessable** | Identifying ambiguous predicates requires the predicate definitions, relation rules, and controlled vocabularies. Those are not in the evidence. The sentence-discipline metadata also warns that semantic continuity cannot be inferred where definitions or referents differ. |
| 7 | **Unassessable** | C1 names “invocation authorization,” and C8 names `RoutingDecision`, but the record shapes and relations needed to distinguish authorization, routing, and evidence admission—and to test composition—are absent. Section 4 and any composition rules are required. |
| 8 | **Unassessable** | C3 refers to `ModelIdentity` resolution equality, and C5 records provider or organization correlation as a factor. But the evidence does not define ModelIdentity, alias handling, endpoint or regional representation, organizational fields, or the relation rules needed to determine whether these cases create false independence. |
| 9 | **Answered** | C9 expressly governs artifact provenance and lineage inheritance, while C11 expressly states the present boundary: “until claim-level lineage exists, witness-path independence counts are artifact-level approximations.” C11 also identifies the break: “N ‘independent’ paths satisfied by N copies of one unrecorded shared claim.” The supplied text therefore answers both whether provenance is presently artifact-oriented and where the approximation fails. |
| 10 | **Unassessable** | C1 requires an `EffectiveInputManifest` and names session-state mode; C5 also names prompt common cause and session-state confidence. But the required contents of an effective-input record, and the definition or criteria for treating an invocation as blind, are not provided. |
| 11 | **Still live** | The constraints provide partial answers: C3 is executor-generic but supplies kind-specific equivalence semantics for models, tools, and humans; C1 imposes model-specific identity and catalog fields when a model participates; C6 is stated across all three authority axes. But the full cross-kind treatment is not settled by the excerpt. In particular, C10’s stated trigger is ancestry shared with the `ModelIdentity` that produced tested output, while the question asks for the corresponding treatment of tools and humans. The question remains useful for exposing inconsistent executor-kind coverage. |
| 12 | **Answered** | C3 directly answers it. An unresolved relation may not qualify as an independent path; the adjudicating invocation may not adjudicate while the relation remains unresolved; and the result is `independence_unresolved`. A compensating control that leaves equivalence unresolved cannot license adjudication or increase independence. |
| 13 | **Unassessable** | The question expressly depends on “4.7, both.” Section 4.7 and the disclosure-constraint text are absent. Without them, neither literal compliance nor undeclared authority can be evaluated. |
| 14 | **Unassessable** | C10 gives substantial relevant material: self-authored verification is marked `verifier_lineage: self_authored`; at high consequence it requires independently-lineaged verification or independent review of the verifier; and it recognizes several compensating paths. But the question also depends on P2, whose text and property-scoping semantics are not supplied. The admission rules needed to determine whether a blind spot is nevertheless admitted are also absent. |

### What this inherited set does not ask

The fourteen questions do not adequately cover several concerns visible in the supplied v9.1 material:

1. **Whether a proposed constraint has governance force.**  
   C1–C5 and C8 are identified as `proposed-v9`, and v9.1 is proposed and not admitted. The question set does not ask whether an answer relies on a proposed rule rather than an admitted one.

2. **Whether inherited text remains semantically continuous with v4.**  
   The metadata states that textual continuity “does not by itself establish semantic identity” where definitions, vocabularies, relation rules, or other referents differ. No challenge question asks for a dependency-by-dependency semantic-continuity review of inherited C6, C7, C9, C10, and C11 against the v9.1 definitions.

3. **Whether a stated enforcement requirement has evidence of execution.**  
   The matrix repeatedly distinguishes claimed enforcement from enforcement evidence. It reports no named C3, C6, C7, C9, C10, or C11 attestation for a named target, and no enforcement evidence for the proposed constraints. None of the fourteen questions directly asks whether an enforcement claim is supported by a named retained artifact for a named target.

4. **Activation and capability gaps.**  
   C1, C2, C4, C5, and C8 depend on activation decisions or capabilities that have not shipped according to the matrix. The questions ask about ontology design, but not whether the necessary profile, catalog, lineage, routing, or validator capability exists and has been activated.

5. **Selection provenance as a distinct failure mode.**  
   Q4 concerns laundering from a pre-provenance artifact, and Q9 concerns the artifact/claim boundary. Neither specifically asks whether undisclosed selection criteria or priors taint otherwise clean selected sources, despite C9 making that a separate lineage issue.

6. **The expressly admitted observability limitation for human activity.**  
   C9 states that offline human reading is unobservable and that the rule is only partially enforceable. The set does not ask how high-consequence governance treats that irreducible observability boundary, including what evidence is insufficient rather than merely missing.

7. **The relationship between self-authored verification and the asserted compensating paths.**  
   Q14 concerns a blind spot entering governed evidence, but it does not separately ask whether cross-environment reproduction, operator adjudication, or provider completion review are independent under C3 and C5 for the specific claim, executor identity, source, and provider-correlation dimensions.

8. **Whether the eight accepted corrections were actually answered without regression.**  
   The set does not ask for a point-by-point check of A1–A8: the original defect, the correction, the affected normative text, the changed definitions or relations, and any new failure mode introduced by the correction. That omission is particularly material because v9.1 is the corrected successor to v9 and the review is of the answers rather than the original findings.

### Evidence needed but not provided

1. **Section 4 object definitions and relation rules**, including:
   - object categories for Q1;
   - the three-axis Role definitions for Q3;
   - predicates and their formal meanings for Q6;
   - authorization, routing, admission, and composition records or relations for Q7;
   - `ModelIdentity`, organization, endpoint, region, and alias representation for Q8;
   - `EffectiveInputManifest` and the definition of blind treatment for Q10;
   - both parts of 4.7 for Q13.

2. **The text of P2**, including its property-scoped verification semantics, plus the applicable admission rule for governed evidence, for Q14.

3. **The eight findings A1–A8, their recorded answers, and a mapping from each finding to the corrected v9.1 text.**  
   The metadata says that eight findings were accepted and answered, but the evidence does not identify their contents. Consequently, it is not possible to name all correction-raised concerns that the inherited question set fails to cover.

4. **The corrected v9.1 diff or complete corrected text**, sufficient to determine what changed beyond the excerpts and whether the challenge questions still target the actual candidate’s definitions and dependencies.

5. **For any assessment of actual enforcement rather than ontology wording**, named retained attestations or machine evidence for the applicable constraint and named target. The matrix expressly says that artifacts classes, records, and claims that checks occur are not themselves enforcement evidence.

### Additional finding outside the question

The material supports a distinction between a question being textually answered and the underlying control being demonstrated. Several constraints describe prohibitions, statuses, or required records, while the enforcement matrix records `none` enforcement evidence or no named attestation for the relevant checks. The inherited challenge set largely tests conceptual escape paths; it does not test whether the stated controls have been applied, evidenced, or activated for any named invocation, verification, decision, or admission target.
```

## Claude Response

- model: `claude-sonnet-5`

```
**VERDICT SENTENCE:** On the evidence supplied, six of the fourteen challenge-round questions remain unassessable for lack of Section 4 object/predicate definitions, one is stale on its face as specified, three are still live and unresolved by anything in Sections 6/9, and the remainder are answered by C3, C10, and C11 as written — but the set as a whole still does not ask whether the eight corrections it is reviewing actually fixed anything, or whether this review's own executor-identity chain is C3-clean.

---

**Per-question disposition**

1. *Which objects are missing / category errors* — **UNASSESSABLE.** Needs Section 4 object definitions (declared omission).

2. *Which constraints are unenforceable; minimal representable form* — **STILL LIVE.** Section 9's Representability column shows `none` for C1, C2, C4, C5, C8 and `partial` for C3, C6, C7, C9, C10, C11; nothing is `full`. That establishes *unenforceable as stated*, but nothing in evidence supplies "minimal representable form" for any of them.

3. *Concrete invocation satisfying the three-axis Role definitions while violating authority separation* — **UNASSESSABLE.** C6 states "COMP-0032 produced two constructions... this sentence closes both," but the Role three-axis definitions themselves are Section 4 material not supplied; cannot check whether a third construction exists beyond the two closed ones.

4. *Laundering path surviving C9 and C10* — **STILL LIVE.** C9's "structural transformation cannot improve the provenance class" and C10's self-authored-verification demotion narrow this, but Section 9 records enforcement evidence as `none` for both C9 and C10 ("no named artifact instance currently attests a C9 inheritance check"; same for C10). Absence of enforcement evidence means the construction is not foreclosed in practice.

5. *Does candidate Slice A omit anything...* — **STALE ON ITS FACE**, as the question itself flags: it presupposes Slice A "is implemented and warranted," and no such implemented, warranted Slice A appears anywhere in this evidence set (v9.1 "has no governance force"; there is no Slice A artifact in Sections 6, 9, or the metadata).

6. *Predicate ambiguous enough to produce divergent implementations* — **UNASSESSABLE.** Needs Section 4 predicate definitions.

7. *Where invocation authorization is represented; distinguished from routing/admission; holds under composition* — **UNASSESSABLE.** C8 and C2 gesture at the distinction but the object location ("invocation authorization" as a represented entity) is Section 4 material not supplied.

8. *One model served through different orgs/endpoints/aliases without false independence* — **STILL LIVE.** C5 names "provider/organization correlation" as a dimension, but this very round supplies a live, unresolved instance of exactly this problem (Disclosure 3: gpt-5.6-thinking vs. gpt-5.6-terra, "Nothing establishes whether they are the same executor"). Unresolved in fact, not just in principle.

9. *Provenance for claim derivation vs. artifact production; where approximation breaks* — **ANSWERED.** C11: "until claim-level lineage exists, witness-path independence counts are artifact-level approximations," naming the exact failure mode (N "independent" paths = N copies of one unrecorded shared claim).

10. *What an effective-input record must contain before an invocation may be treated as "blind"* — **UNASSESSABLE.** C1 names `EffectiveInputManifest` as a field but does not define "blind" or the manifest's required contents; that is Section 4 material.

11. *Which constraints apply identically across executor kinds; which are executor-specific* — **ANSWERED** (substantively). C3 is explicitly per-kind (ModelIdentity equality / tool identity+version / principal equality); C10 is model-specific (`verifier_lineage: self_authored` keyed to shared ModelIdentity ancestry). The remainder (C4, C5, C6, C7, C8, C9, C11) read as executor-generic on their face.

12. *Conditions for unresolved model identity to qualify as independent witness; failure behavior* — **ANSWERED.** C3, verbatim: unresolved equivalence never qualifies as independent — "the independence result is `independence_unresolved`, not an independent path," remaining unresolved "until equivalence or non-equivalence is affirmatively established." Notably, this is the exact rule Disclosure 3 invokes against this very review.

13. *Composite tool satisfying disclosure constraints' letter (4.7) while exercising undeclared authority* — **UNASSESSABLE.** Section 4.7 (disclosure constraints) is not in evidence.

14. *P2 + C10 still admitting a generator-authored blind spot* — **UNASSESSABLE** on full construction, though partially informed: C10 is fully given ("the verified property claim stands only as far as the verifier's scope and lineage permit," with independent-lineage required only "at high consequence" — implying a live gap below that threshold), but "P2 (property-scoped verification)" itself is referenced, not defined, in this evidence set. Cannot complete the construction without P2's definition.

---

**What I needed and did not have:** Section 4 object/predicate definitions (needed for Q1, Q3, Q6, Q7, Q10, Q13, Q14); Section 4.7 disclosure-constraint text specifically (Q13); the definition of "P2 (property-scoped verification)" referenced but not reproduced in Section 6 (Q14); the actual text of findings A1–A8 and their corrections (referenced by the metadata but not supplied — needed to check whether the "concerns raised by the eight corrections" are covered, beyond inferring from the corrected constraint text itself).

---

**What the set does not ask, and what it fails to cover for v9.1:**

- **Correction soundness.** None of the fourteen ask whether the eight accepted A1–A8 corrections actually cured their findings. Disclosure 1 warns explicitly against assuming soundness from response; the question set, unrevised since v3/v4, has no slot for this at all — it was written before the corrections existed and has not been extended to interrogate them.
- **Self-adjudication within the review itself.** Q3 and Q12 ask about authority separation and unresolved-identity witness paths as abstract constructions, but no question asks whether *this round's own evidence ancestry* — an executor self-reported as gpt-5.6-thinking drafting v9/v9.1, reviewed by a slot self-reported as gpt-5.6-terra — satisfies C3. Disclosure 3 raises exactly this, and the fourteen questions, being about the ontology's objects, never turn the lens on the review process producing the answers.
- **Historical admission traceability.** C8 (decision traceability) is one of the fourteen's referents only obliquely (Q7); no question asks whether v4's own admission — "recorded in conversation only" per the version table — itself satisfies C8's requirement for a "reconstructible RoutingDecision or governed manual-override DecisionRecord." The baseline the whole ontology reconstructs from has a traceability gap the question set never names.
- **Enforcement-evidence uniformity as a structural fact.** Section 9 shows *every single constraint*, proposed or inherited, currently has enforcement evidence of `none` (with C3/C6/C7/C9/C10/C11 marked "manual... none; [specific artifact] is not evidence"). No question asks the aggregate question: should anything be admitted while zero constraints in the entire document have evidenced enforcement.
- **v9.1's own non-substantive claim.** The metadata asserts the version bump "does not itself add a ninth substantive correction." No challenge question tests that assertion.
```
