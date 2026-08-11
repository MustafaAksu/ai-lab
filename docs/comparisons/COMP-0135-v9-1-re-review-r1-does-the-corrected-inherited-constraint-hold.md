# COMP-0135: Provider Comparison — v9.1 re-review R1 does-the-corrected-inherited-constraint-hold

## Metadata

- comparison_id: `COMP-0135`
- title: `v9.1 re-review R1 does-the-corrected-inherited-constraint-hold`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-5faecb3cd64183ee.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0135", "target_id": "INV-5faecb3cd64183ee"}, {"authoritative": false, "evidence": "docs/invocations/INV-7fbd74693a6c5afd.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0135", "target_id": "INV-7fbd74693a6c5afd"}]`
- created_at: `2026-08-11T14:14:05.265786+00:00`
- command: `scripts/compare_providers.py --title v9.1 re-review R1 does-the-corrected-inherited-constraint-hold You are reviewing a proposed ontology amendment. This is ONE question of five, each asked in a separate call with its own evidence set. Do not attempt to answer the others.

Status: ABS-0004 v9.1 is proposed and not admitted. v4 is the last version with an admission event. v9.1 has no governance force.

Disclosures:

1. v9.1 is the CORRECTED successor to v9. A prior round, COMP-0126 to COMP-0134, found eight defects in v9; all eight were accepted by the operator and answered. You are reviewing the answers, not the original. Do not assume a correction is sound because it was made in response to a finding.

2. THIS IS A RE-RUN. Each of these five questions was asked of v9 and returned an answer qualified by insufficient evidence. The evidence sets were the question author's choices, and they were wrong. If this evidence set is still insufficient, say so and name precisely what is missing; that report is wanted output and the last round's version of it is why this round exists.

3. The executor that drafted v9, the corrections, and the version bump self-reports as gpt-5.6-thinking. One reviewer slot in this round is gpt-5.6-terra. The provider's own catalog asserts these are distinct model identities, and that catalog is a provider self-report. Nothing establishes whether they are the same executor. Under the corrected C3 you are reading, an invocation may not adjudicate a claim whose evidence ancestry contains an executor of unresolved equivalence. Your output is evidence for the accountable principal, not an adjudication.

4. The question author drafted ABS-0004 v5 through v8, all withdrawn or superseded, and drafted none of v9 or v9.1.

Answer in whatever form fits, but include three things: a VERDICT SENTENCE before the reasoning; any evidence you needed and did not have; and anything you found that this question did not ask about.

Quote only text that appears below. Do not certify or praise. No provider product recommendations.

=== QUESTION R1 ===
v9 was found to relocate rather than resolve the defect that withdrew v8. Its tag definition said an inherited constraint's "current governance force derives from v4's admission, not from the proposed v9 document", and reviewers found that this needs a rule — that verbatim reproduction of admitted text inside a non-admitted document carries the original admission's force forward — which the ontology did not state.

v9.1's answer has three parts: the tag definition, a new limitation stating that textual continuity does not establish semantic identity when referents differ, and the retagging of C3 to [PROPOSED_CONSTRAINT] because v4 never admitted it in its current semantic environment.

Does that answer hold? Consider: whether a reader with only this document can now check any inherited claim; whether the limitation does work or restates the problem; and whether the same argument that moved C3 to proposed applies to any constraint still tagged inherited. If it does, name them.

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

=== EVIDENCE Admitted ABS-0004 v4, Section 6, for comparison with the inherited constraints ===
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

`[ADOPTED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
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

`[ADOPTED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another. Assignment independence
is not exercise license: adjudicator-level epistemic authority and
above-read_only action authority may not both be exercised within a single
invocation against the same target unless the adjudication is covered by
an independent verification edge; an invocation that mutates state it also
adjudicates collapses the separation C6 exists to preserve. COMP-0032
produced two constructions satisfying the axis definitions while defeating
separation; this sentence closes both.

`[ADOPTED_CONSTRAINT]` C7 Implementation separation: an executor with
repository or external action authority may implement an admitted plan but
may not be the sole verifier or adjudicator of its own changes.

`[PROPOSED_CONSTRAINT]` C8 Decision traceability: every policy-selected
invocation has a reconstructible RoutingDecision or a governed
manual-override DecisionRecord (accountable principal, reason, scope,
review condition; never a free-text escape hatch).

`[ADOPTED_CONSTRAINT]` C9 Conservative lineage inheritance (from P3): an
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

`[ADOPTED_CONSTRAINT]` C11 Interim independence disclosure: until
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

`[ADOPTED_CONSTRAINT]` C10 Validator lineage independence (property-scoped
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

=== EVIDENCE DECISION-20260727-0005, which adopted the [INHERITED_CONSTRAINT] category ===
{
  "authorized_effects": [
    "Accepting the eight [LIMITATION] statements drafted for V9L-004, V9L-010, V9L-013, V9L-018, V9L-021, V9L-024, V9L-025 and V9L-027 as literal text for ABS-0004 v9, to be applied at assembly.",
    "Adopting [LIMITATION] as a v9 sentence category: a descriptive boundary on what the ontology, its records, or current enforcement establish. It imposes no constraint and claims no adoption.",
    "Adopting [INHERITED_CONSTRAINT] as a v9 sentence category: constraint text carried forward unchanged from the admitted v4 baseline, whose current governance force derives from v4's admission rather than from the proposed v9 document. A substantive change to such text becomes [PROPOSED_CONSTRAINT] until separately admitted.",
    "Accepting that four of the eight statements restate substance already present in admitted v4, on the reasoning that a reader of the section carrying the limitation should not have to reconstruct it from a principle stated elsewhere in the document.",
    "Recording that ABS-0004 v9's Section 3 will be approximately 1.48 times the size of admitted v4's Section 3, and the document approximately 1.06 times, as the accepted consequence of tasks 2 and 3."
  ],
  "blocked_effects": [
    "No assembly of ABS-0004 v9. The accepted text is held with the task 2 text for application at assembly; no ontology file is modified by this decision.",
    "No migration of the sixteen inherited constraints to [INHERITED_CONSTRAINT]. The category is adopted; applying it is an assembly step and is not performed here.",
    "No new constraint, mechanism, or control. Every accepted statement is descriptive. None defines a chain terminus, a standing-authority rule, an ExecutorIdentity inheritance design, a verifier architecture, or an admission control.",
    "No resolution of identity_verification_status, which DECISION-20260727-0004 records as required before assembly and which task 3 deliberately left untouched.",
    "No change to any Section 3 definition or constraint. Section 3 gains three [LIMITATION] statements and nothing else."
  ],
  "created_at": "2026-07-27T00:00:00+00:00",
  "decision": "accept_task3_limitations_and_v9_sentence_categories",
  "decision_id": "DECISION-20260727-0005",
  "evidence_refs": [
    "docs/self_model/v9_reconstruction/V9_TASK3_LIMITATIONS_PROPOSAL.md",
    "docs/self_model/v9_reconstruction/ABS-0004-v9-task3-limitations.patch",
    "docs/self_model/v9_reconstruction/V9_TASK3_SENTENCE_CATEGORY_PROPOSAL.txt",
    "docs/self_model/v9_reconstruction/ABS-0004-v9-task2-proposed-baseline.md",
    "docs/self_model/V9_CHANGE_LEDGER.json",
    "docs/self_model/decisions/DECISION-20260727-0002.json",
    "docs/self_model/decisions/DECISION-20260727-0004.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md"
  ],
  "rationale": [
    "[INHERITED_CONSTRAINT] answers the defect that decided the withdrawal of v8. v8 was marked proposed while carrying twenty-four constraints tagged with a category ABS-0004 defines as 'constraint adopted now', so the governance status of every constraint in the document was undetermined: either proposed text claimed present force, or the tags referred to inherited constraints and the document did not identify which wording had been admitted. [INHERITED_CONSTRAINT] states the answer in the tag itself.",
    "The category is verifiable rather than asserted, and was verified before acceptance. Every one of the sixteen constraints surviving into the task 3 candidate is byte-identical to its admitted v4 text after whitespace normalisation. The single v4 constraint that does not survive is the ModelIdentity constraint that task 2 converted to [PROPOSED_CONSTRAINT], which is the correct treatment for text that changed.",
    "The task 3 chain was verified end to end: five supplied checksums pass; the task 3 baseline is byte-identical to the committed task 2 candidate; the patch applies cleanly to it; the result is byte-identical to the supplied candidate; the ADOPTED_CONSTRAINT count does not change; and no Section 3 definition or constraint is altered.",
    "The size consequence is recorded rather than left to be discovered. Section 3 grows from 1465 to 2173 characters, a factor of 1.48, against the 7.5 by which v8 had grown it across four unadmitted amendments. The document grows by a factor of 1.06.",
    "Three of the accepted statements are added to Section 3, where task 1 found that no textual change is established by the later evidence. These are consistent: task 1 asked whether v4's Section 3 text is wrong or incomplete, and found it is not. The ledger's adjudicated response to three findings bearing on Section 3 is to state a limitation, which adds no definition and no constraint. The operator accepted this explicitly.",
    "One accepted statement expresses the substance of P7, which first appeared in withdrawn v7 and is not present in admitted v4. The wording is the reviewing executor's rather than v7's, and it is tagged [LIMITATION] rather than [PRINCIPLE], so it claims no adoption and imposes no obligation. The underlying finding is established by COMP-0037 and COMP-0039..0046 independently of v7 having stated it.",
    "Four of the eight statements restate substance already in admitted v4, at P2, P3, P5, C3, \u00a74.15 and the C6 enforcement-matrix row. The reviewing executor flagged this rather than including them silently, and asked whether explicit repetition is preferable to the strict smallest-delta discipline. The operator accepted them on the reasoning that a reader of \u00a74.15, \u00a76 or \u00a74.16 should not have to reconstruct the boundary from a principle stated elsewhere."
  ],
  "repo_commit": "7b8b1dc708cacc1012b46ba8d6e5203ad703a765",
  "required_next_governance": [
    "The assembly rule as proposed says to replace the seventeen inherited [ADOPTED_CONSTRAINT] tags. There are seventeen occurrences but sixteen constraints: the seventeenth is the sentence-discipline legend entry that defines what the tag means. At assembly the legend must be replaced by definitions of [INHERITED_CONSTRAINT] and [LIMITATION], not renamed. Applied literally the rule would rewrite the definition of a category the document no longer uses.",
    "identity_verification_status remains unresolved. The accepted task 2 text removes the ontology's only mention of a field that ai_lab/providers/invocation_record.py validates and every captured invocation record carries. Assembly must not proceed until the text names the field or a record states that the ontology deliberately no longer does.",
    "Assembly is the next reconstruction step and has not been authorized by any decision. DECISION-20260727-0002 authorizes constructing v9; what remains unassigned is who performs assembly, and the constraint that whoever drafts v9 does not write the question set that reviews it.",
    "Fifteen ledger entries classified separate gap or policy required have no drafting task and are not addressed by v9. Whether they become gap records, and when, has not been decided."
  ],
  "schema_version": "v1",
  "selection_effect": "The eight [LIMITATION] statements and the two new sentence categories are accepted for ABS-0004 v9. Together with the task 2 text accepted under DECISION-20260727-0004, this completes the drafting inputs for v9 assembly. No ontology file changes as a consequence of this record.",
  "source_capability_ids": [
    "CAP-0015",
    "CAP-0016"
  ],
  "source_gap_id": "GAP-0005",
  "source_plan_id": "PLAN-20260723-0002",
  "status": "recorded",
  "summary": "The eight limitation statements drafted for the ledger's explicit-limitation-sufficient entries are accepted, along with two new v9 sentence categories: [LIMITATION] for descriptive boundaries claiming no adoption, and [INHERITED_CONSTRAINT] for v4 text carried forward whose force derives from v4's admission rather than from proposed v9. The second answers the contradiction that decided v8's withdrawal, and was verified before acceptance: all sixteen surviving constraints are verbatim admitted v4 text.",
  "title": "Accept the task 3 limitation statements and the v9 sentence categories"
}

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

=== QUESTION R1 ===
v9 was found to relocate rather than resolve the defect that withdrew v8. Its tag definition said an inherited constraint's "current governance force derives from v4's admission, not from the proposed v9 document", and reviewers found that this needs a rule — that verbatim reproduction of admitted text inside a non-admitted document carries the original admission's force forward — which the ontology did not state.

v9.1's answer has three parts: the tag definition, a new limitation stating that textual continuity does not establish semantic identity when referents differ, and the retagging of C3 to [PROPOSED_CONSTRAINT] because v4 never admitted it in its current semantic environment.

Does that answer hold? Consider: whether a reader with only this document can now check any inherited claim; whether the limitation does work or restates the problem; and whether the same argument that moved C3 to proposed applies to any constraint still tagged inherited. If it does, name them.

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

=== EVIDENCE Admitted ABS-0004 v4, Section 6, for comparison with the inherited constraints ===
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

`[ADOPTED_CONSTRAINT]` C3 No self-adjudication (executor-generic): an
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

`[ADOPTED_CONSTRAINT]` C6 Authority separation across all three role axes:
epistemic authority, action authority, and accountable authority are
assigned independently and none implies another. Assignment independence
is not exercise license: adjudicator-level epistemic authority and
above-read_only action authority may not both be exercised within a single
invocation against the same target unless the adjudication is covered by
an independent verification edge; an invocation that mutates state it also
adjudicates collapses the separation C6 exists to preserve. COMP-0032
produced two constructions satisfying the axis definitions while defeating
separation; this sentence closes both.

`[ADOPTED_CONSTRAINT]` C7 Implementation separation: an executor with
repository or external action authority may implement an admitted plan but
may not be the sole verifier or adjudicator of its own changes.

`[PROPOSED_CONSTRAINT]` C8 Decision traceability: every policy-selected
invocation has a reconstructible RoutingDecision or a governed
manual-override DecisionRecord (accountable principal, reason, scope,
review condition; never a free-text escape hatch).

`[ADOPTED_CONSTRAINT]` C9 Conservative lineage inheritance (from P3): an
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

`[ADOPTED_CONSTRAINT]` C11 Interim independence disclosure: until
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

`[ADOPTED_CONSTRAINT]` C10 Validator lineage independence (property-scoped
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

=== EVIDENCE DECISION-20260727-0005, which adopted the [INHERITED_CONSTRAINT] category ===
{
  "authorized_effects": [
    "Accepting the eight [LIMITATION] statements drafted for V9L-004, V9L-010, V9L-013, V9L-018, V9L-021, V9L-024, V9L-025 and V9L-027 as literal text for ABS-0004 v9, to be applied at assembly.",
    "Adopting [LIMITATION] as a v9 sentence category: a descriptive boundary on what the ontology, its records, or current enforcement establish. It imposes no constraint and claims no adoption.",
    "Adopting [INHERITED_CONSTRAINT] as a v9 sentence category: constraint text carried forward unchanged from the admitted v4 baseline, whose current governance force derives from v4's admission rather than from the proposed v9 document. A substantive change to such text becomes [PROPOSED_CONSTRAINT] until separately admitted.",
    "Accepting that four of the eight statements restate substance already present in admitted v4, on the reasoning that a reader of the section carrying the limitation should not have to reconstruct it from a principle stated elsewhere in the document.",
    "Recording that ABS-0004 v9's Section 3 will be approximately 1.48 times the size of admitted v4's Section 3, and the document approximately 1.06 times, as the accepted consequence of tasks 2 and 3."
  ],
  "blocked_effects": [
    "No assembly of ABS-0004 v9. The accepted text is held with the task 2 text for application at assembly; no ontology file is modified by this decision.",
    "No migration of the sixteen inherited constraints to [INHERITED_CONSTRAINT]. The category is adopted; applying it is an assembly step and is not performed here.",
    "No new constraint, mechanism, or control. Every accepted statement is descriptive. None defines a chain terminus, a standing-authority rule, an ExecutorIdentity inheritance design, a verifier architecture, or an admission control.",
    "No resolution of identity_verification_status, which DECISION-20260727-0004 records as required before assembly and which task 3 deliberately left untouched.",
    "No change to any Section 3 definition or constraint. Section 3 gains three [LIMITATION] statements and nothing else."
  ],
  "created_at": "2026-07-27T00:00:00+00:00",
  "decision": "accept_task3_limitations_and_v9_sentence_categories",
  "decision_id": "DECISION-20260727-0005",
  "evidence_refs": [
    "docs/self_model/v9_reconstruction/V9_TASK3_LIMITATIONS_PROPOSAL.md",
    "docs/self_model/v9_reconstruction/ABS-0004-v9-task3-limitations.patch",
    "docs/self_model/v9_reconstruction/V9_TASK3_SENTENCE_CATEGORY_PROPOSAL.txt",
    "docs/self_model/v9_reconstruction/ABS-0004-v9-task2-proposed-baseline.md",
    "docs/self_model/V9_CHANGE_LEDGER.json",
    "docs/self_model/decisions/DECISION-20260727-0002.json",
    "docs/self_model/decisions/DECISION-20260727-0004.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md"
  ],
  "rationale": [
    "[INHERITED_CONSTRAINT] answers the defect that decided the withdrawal of v8. v8 was marked proposed while carrying twenty-four constraints tagged with a category ABS-0004 defines as 'constraint adopted now', so the governance status of every constraint in the document was undetermined: either proposed text claimed present force, or the tags referred to inherited constraints and the document did not identify which wording had been admitted. [INHERITED_CONSTRAINT] states the answer in the tag itself.",
    "The category is verifiable rather than asserted, and was verified before acceptance. Every one of the sixteen constraints surviving into the task 3 candidate is byte-identical to its admitted v4 text after whitespace normalisation. The single v4 constraint that does not survive is the ModelIdentity constraint that task 2 converted to [PROPOSED_CONSTRAINT], which is the correct treatment for text that changed.",
    "The task 3 chain was verified end to end: five supplied checksums pass; the task 3 baseline is byte-identical to the committed task 2 candidate; the patch applies cleanly to it; the result is byte-identical to the supplied candidate; the ADOPTED_CONSTRAINT count does not change; and no Section 3 definition or constraint is altered.",
    "The size consequence is recorded rather than left to be discovered. Section 3 grows from 1465 to 2173 characters, a factor of 1.48, against the 7.5 by which v8 had grown it across four unadmitted amendments. The document grows by a factor of 1.06.",
    "Three of the accepted statements are added to Section 3, where task 1 found that no textual change is established by the later evidence. These are consistent: task 1 asked whether v4's Section 3 text is wrong or incomplete, and found it is not. The ledger's adjudicated response to three findings bearing on Section 3 is to state a limitation, which adds no definition and no constraint. The operator accepted this explicitly.",
    "One accepted statement expresses the substance of P7, which first appeared in withdrawn v7 and is not present in admitted v4. The wording is the reviewing executor's rather than v7's, and it is tagged [LIMITATION] rather than [PRINCIPLE], so it claims no adoption and imposes no obligation. The underlying finding is established by COMP-0037 and COMP-0039..0046 independently of v7 having stated it.",
    "Four of the eight statements restate substance already in admitted v4, at P2, P3, P5, C3, \u00a74.15 and the C6 enforcement-matrix row. The reviewing executor flagged this rather than including them silently, and asked whether explicit repetition is preferable to the strict smallest-delta discipline. The operator accepted them on the reasoning that a reader of \u00a74.15, \u00a76 or \u00a74.16 should not have to reconstruct the boundary from a principle stated elsewhere."
  ],
  "repo_commit": "7b8b1dc708cacc1012b46ba8d6e5203ad703a765",
  "required_next_governance": [
    "The assembly rule as proposed says to replace the seventeen inherited [ADOPTED_CONSTRAINT] tags. There are seventeen occurrences but sixteen constraints: the seventeenth is the sentence-discipline legend entry that defines what the tag means. At assembly the legend must be replaced by definitions of [INHERITED_CONSTRAINT] and [LIMITATION], not renamed. Applied literally the rule would rewrite the definition of a category the document no longer uses.",
    "identity_verification_status remains unresolved. The accepted task 2 text removes the ontology's only mention of a field that ai_lab/providers/invocation_record.py validates and every captured invocation record carries. Assembly must not proceed until the text names the field or a record states that the ontology deliberately no longer does.",
    "Assembly is the next reconstruction step and has not been authorized by any decision. DECISION-20260727-0002 authorizes constructing v9; what remains unassigned is who performs assembly, and the constraint that whoever drafts v9 does not write the question set that reviews it.",
    "Fifteen ledger entries classified separate gap or policy required have no drafting task and are not addressed by v9. Whether they become gap records, and when, has not been decided."
  ],
  "schema_version": "v1",
  "selection_effect": "The eight [LIMITATION] statements and the two new sentence categories are accepted for ABS-0004 v9. Together with the task 2 text accepted under DECISION-20260727-0004, this completes the drafting inputs for v9 assembly. No ontology file changes as a consequence of this record.",
  "source_capability_ids": [
    "CAP-0015",
    "CAP-0016"
  ],
  "source_gap_id": "GAP-0005",
  "source_plan_id": "PLAN-20260723-0002",
  "status": "recorded",
  "summary": "The eight limitation statements drafted for the ledger's explicit-limitation-sufficient entries are accepted, along with two new v9 sentence categories: [LIMITATION] for descriptive boundaries claiming no adoption, and [INHERITED_CONSTRAINT] for v4 text carried forward whose force derives from v4's admission rather than from proposed v9. The second answers the contradiction that decided v8's withdrawal, and was verified before acceptance: all sixteen surviving constraints are verbatim admitted v4 text.",
  "title": "Accept the task 3 limitation statements and the v9 sentence categories"
}

--- END OF EVIDENCE ---

Answer only the question above.

## OpenAI Response

- model: `gpt-5.6-terra`

```
**VERDICT: I cannot adjudicate whether the v9.1 answer holds, because the claim under review has evidence ancestry from `gpt-5.6-thinking` while this reviewer slot is `gpt-5.6-terra`, and their equivalence or non-equivalence is unresolved under corrected C3.**

The following are documentary observations, not an adjudication.

1. **The tag definition does not make an inherited claim checkable from v9.1 alone.**  
   It states that an `[INHERITED_CONSTRAINT]` is text “carried forward unchanged from the admitted v4 baseline” and that its force derives from v4. But a reader possessing only v9.1 has neither:
   - the admitted v4 text or a self-contained, authenticated reproduction of it;
   - a per-constraint comparison record establishing unchanged text; nor
   - a mapping from each inherited constraint’s v4 referents to its v9.1 referents.

   The reconstruction-baseline commit identifier is a locator, not evidence available to a reader with only this document. The v9.1 text therefore lets the reader see an assertion of inheritance, but not check that assertion.

2. **The new limitation identifies the semantic-identity problem but does not resolve it.**  
   It says that textual continuity does not establish semantic identity when “definitions, vocabularies, relation rules, or other referents” differ, and that dependencies require re-examination before admission. This is a limitation on what the tag proves. It does not supply:
   - the dependency inventory;
   - the comparison of old and new referents;
   - a finding that each dependency is unchanged or that a difference is non-substantive; or
   - a rule for the interim status of a verbatim constraint whose semantic identity remains unexamined.

   Thus, the limitation prevents a reader from inferring semantic continuity merely from literal continuity, but leaves the claimed carried-forward governance force unsupported in the altered environment.

3. **Retagging C3 recognizes a demonstrated semantic change, but that reasoning requires review of inherited constraints that use C3-dependent concepts.**  
   The displayed v4 C3 permitted an unresolved/resolved endpoint relation to be “treated as distinct until equivalence is affirmatively established,” while also saying that distinctness could not increase independence. The v9.1 C3 instead says that an invocation “may not adjudicate” while equivalence remains unresolved and that the relation is “not treated as distinct.” That is not merely a tag change; it changes the operative treatment of unresolved identity in adjudication and independence.

   On the supplied Section 6 text, the inherited constraints requiring at least re-examination under the stated limitation are:

   - **C6**, because it uses “adjudication” and an “independent verification edge.”
   - **C7**, because it prohibits being the sole “verifier or adjudicator” of one’s own changes.
   - **C10**, because it uses `ModelIdentity`, verifier lineage, independence standing, independently-lineaged verification, and independent review.
   - **C11**, because it governs the satisfaction and disclosure of independence requirements and independent witness paths.

   **C9** also contains `independent_observation: false`, but the supplied excerpts do not establish whether that field’s semantics depend on the changed C3 identity and independence rules. It cannot be cleared from the limitation’s concern without the relevant definitions and relation rules.

   The evidence does not establish that C6, C7, C10, or C11 necessarily changed semantic content. It does establish that their C3-related dependencies were not shown to have been examined. Under v9.1’s own limitation, literal identity alone is insufficient for their inherited-status conclusion in the proposed environment.

### Evidence needed but not provided

To determine this question rather than merely report the above issue, the record would need:

1. The complete admitted v4 ontology and complete v9.1 ontology, including all definitions, vocabulary definitions, relation rules, principles, role rules, and enforcement rules referenced by C6, C7, C9, C10, and C11.
2. A constraint-by-constraint dependency and semantic-continuity analysis for every `[INHERITED_CONSTRAINT]`, identifying each referenced term or relation, its v4 meaning, its v9.1 meaning, and whether any difference is substantive.
3. A self-contained verification mechanism for inherited status: the admitted v4 source or an authenticated immutable copy, normalization rules, and per-constraint comparison results available to the reader rather than asserted in a separate decision.
4. Evidence resolving equivalence or non-equivalence between `gpt-5.6-thinking` and `gpt-5.6-terra`, under the applicable model identity semantics, before this reviewer invocation could adjudicate the claim.

### Other matter found, not asked about

DECISION-20260727-0005 says that no assembly of v9 was authorized and that applying `[INHERITED_CONSTRAINT]` tags was an assembly step not performed by that decision. The supplied v9.1 nevertheless contains those tags. The evidence supplied here does not show the later authorization or verification that would connect the decision’s accepted drafting inputs to their application in the proposed v9.1 document.
```

## Claude Response

- model: `claude-sonnet-5`

```
**VERDICT SENTENCE:** The answer holds only for C3 itself; it does not hold as a general resolution, because the same retagging argument (verbatim text ≠ semantic identity when referents differ) applies with equal logical force to every other constraint still tagged `[INHERITED_CONSTRAINT]` — C6, C7, C9, C10, and C11 — and this evidence set contains nothing that checks, for any of them, whether their referents actually match v4's.

**What I needed and did not have:**
- v4's Section 3 (definitions), §4.15, and §4.16 (the "C6 enforcement-matrix row"), and the corresponding v9.1 text for the same sections, to compare against the C6/C7/C9/C10/C11 text given here. The rationale for DECISION-20260727-0005 explicitly names "P2, P3, P5, C3, §4.15 and the C6 enforcement-matrix row" as places where substance is restated — i.e., places where referent drift is exactly the kind of thing the new v9.1 `[LIMITATION]` warns about — and none of that material is in front of me.
- Any record that "re-examination before admission," which the `[LIMITATION]` itself demands for inherited constraints whose referents differ, was actually performed for C6, C7, C9, C10, or C11. Nothing in the metadata or the decision record shows this was done; DECISION-20260727-0005 checked only byte-identity of text, not identity of referents.
- Confirmation of whether "role," "action authority," "epistemic authority," "witness-path independence," "DecisionRecord," and "verifier_lineage" — the terms C6, C9, C10, C11 depend on — are defined identically in v9.1 as in v4. Byte-identical constraint text can still change meaning if a term it depends on is redefined elsewhere in the same document, and I cannot see the rest of the document.

Given this, and consistent with the prior round's own framing: **this is again insufficient**, but the gap is narrower and nameable — it is specifically the absence of v4-vs-v9.1 Section 3/4.15/4.16 text, not a generic "insufficient evidence."

**Does the answer hold?**

1. *Can a reader with only this document check any inherited claim?* No. The `[LIMITATION]` says referent drift "require[s] re-examination before admission" but does not say where that re-examination occurs, who performs it, or how a reader would find its result. There is no per-constraint disposition (as there was for C3, which got an explicit retagging with a stated reason). A reader has a rule that tells them a problem *might* exist and no mechanism to check whether it does for C6/C7/C9/C10/C11.

2. *Does the limitation do work, or restate the problem?* It restates the problem. The defect reviewers identified was the absence of a rule for when verbatim-carried text keeps its force. The `[LIMITATION]` supplies the negative half only — a rule for when verbatim text does *not* automatically keep its force — without supplying the affirmative rule reviewers asked for, and without resolving which of the sixteen inherited constraints fall on which side. It converts "we don't know the rule" into "we don't know whether the rule's exception applies to each constraint," which is the same unresolved question relocated one level down, exactly the pattern already flagged for v9 relative to v8.

3. *Does the same argument apply to other still-inherited constraints? Name them.* Yes, in form: C3 was retagged because "v4 never admitted it in its current semantic environment" — an assertion about referents, not about the constraint's own wording (C3's wording did in fact change between v4 and v9.1, which independently justifies the retag, but the *stated* justification is the semantic-environment one, and that justification is referent-based and therefore generalizes). The candidates for the same treatment, in descending order of exposure based only on what's visible here:
   - **C6** — explicitly implicated by the decision record's own admission that its "enforcement-matrix row" (§4.16, not in evidence) restates something; if that row changed, C6's semantic environment changed.
   - **C10** and **C9** — depend on "P2" and "P3" respectively, both named in the same rationale list as loci of restated substance; if P2/P3 wording moved between v4 and v9.1, C9/C10's referents moved with them.
   - **C11** — depends on "witness-path independence" and DecisionRecord mechanics defined elsewhere; unverified here.
   - **C7** — shortest and most self-contained, lowest apparent exposure, but not verifiable from this evidence either.

   I cannot say any of these *is* semantically drifted — only that the argument that moved C3 was never applied to them, and nothing here shows it was checked.

**Found but not asked about:**
- Under the `[PROPOSED_CONSTRAINT]` C3 text I am evaluating, an invocation may not adjudicate a claim whose evidence ancestry contains an executor of unresolved equivalence to the adjudicator. Disclosure 3 states the relation between the drafting executor (`gpt-5.6-thinking`) and a reviewer identity (`gpt-5.6-terra`) is unresolved. If my own invocation is or resembles that reviewer identity, C3 as written would forbid this invocation from adjudicating the very claim about C3's correctness. Consistent with the instructions, I am treating this output as evidence for the accountable principal, not as an adjudication of C3's soundness — but this is a live instance of the exact defect class the question is about, and it is not otherwise flagged in the evidence.
- `required_next_governance` in DECISION-20260727-0005 states `identity_verification_status remains unresolved` and that assembly must not proceed until the ontology either names that field or records that it deliberately no longer tracks it. Nothing in the v9.1 metadata shown here indicates this was resolved before v9.1 was proposed.
- The same decision record notes the assembly rule as literally proposed would have overwritten the *legend definition* of the old `[ADOPTED_CONSTRAINT]` tag rather than replacing it with definitions of `[INHERITED_CONSTRAINT]`/`[LIMITATION]` — flagged as a required correction. Whether that correction was actually applied in v9.1 (versus only in the reconstruction task text) is not shown by the metadata provided.
```
