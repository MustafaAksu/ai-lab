<!-- Admitted as evidence input by DECISION-20260727-0003. Status:
     admitted_as_evidence_input. This file is the Markdown rendering of
     V9_CHANGE_LEDGER.json, which is authoritative. Neither file is read by
     the self-model aggregator and neither appears in SELF_MODEL.json. -->

# ABS-0004 v9 Change Ledger — Draft 0002

**Status:** draft for evidentiary review  
**Purpose:** determine the smallest honest delta from admitted v4.  
**No v9 language, schema, label, or control is proposed here.**

## Method boundary

- Primary evidence: COMP-0032, COMP-0035, COMP-0037, COMP-0039..0046, and COMP-0118..0125.
- v4 is used only as the affected baseline surface.
- v5–v8 are not mined for remedies.
- Initial extraction preceded consultation of `CLAIM_IMPACT.json`.
- Later dispositions are recorded without erasing the initial finding.
- Refuted claims were checked but are not retained as live findings merely to populate an `evidence_strength` class; they appear as corrections in `later_disposition` and the disposition audit.
- The ZIP predates the user-reported checkout at `1914cf5`; later withdrawal facts are supplied context, not independently verified from the archive.
- Prior-exposure caveat: the reviewing executor had inspected v8 before this brief; the ledger mitigates that by using only allowed evidence and proposing no text.
- Draft 0002 preserves every finding and classification; it adds only verified history, a derived Section 3 summary, and evidence conditions for unresolved entries.

## Counts

- Live findings: **29**
- Baseline preservations: **5**
- Unprobed future-review surfaces: **9**

Response classes:
- `v4 change required`: 3
- `separate gap or policy required`: 15
- `explicit limitation sufficient`: 7
- `unresolved`: 4

### Derived Section 3 result

**Thirteen live findings bear on Section 3, and none is classified `v4 change required`.** Their response classes are four `unresolved`, three `explicit limitation sufficient`, and six `separate gap or policy required`. This is a classification result derived from the entries, not a proposed v9 remedy.

## V9L-001 — Provider-returned catalog data establishes an authenticated provider self-report at a time; it does not independently verify the truth of the model identity or capability mapping. Calling that result simply verified creates verification collapse or circular attestation.

**Sources:** COMP-0035  
**v4 surface:** §4.3 ModelIdentity; §4.4 CatalogSnapshot, CatalogAssertion, and CatalogVerification; C2 catalog admission.  
**Evidence strength:** `established`  
**Required response class:** `v4 change required`

**Construction/example:** The system queries a provider-controlled catalog endpoint, stores the returned mapping, then marks the same provider assertion verified without any evidence independent of the asserting provider.

**Reviewer split:** Both reviewers agree on the trust defect. OpenAI permits a scoped verification label that says endpoint-authenticated self-assertion; Claude argues the verification layer should not exist without independent evidence.

**Reason:** v9 starts from v4, whose CatalogVerification vocabulary can overstate what the available evidence establishes. The ledger does not choose replacement language or architecture.

**Later disposition:** Verified against the checkout by the evidentiary reviewer: commit `6d7dfee` (2026-07-22) replaced CatalogVerification with CatalogCapture and introduced P6. Because v5 was not separately admitted and is excluded as a remedy source, that history establishes that a response occurred but does not determine v9’s response. The underlying COMP-0035 finding remains live against a v4 reconstruction.

**Excluded remedies:**
- Do not copy v5 terminology or schema merely because it responded to this finding.
- Do not use a scoped verified label without adjudicating whether its ordinary reading still overclaims.

## V9L-002 — Historical identity resolution and current confidence are different facts. Later staleness or contradiction should not silently rewrite the event-time record, but leaving the original verified status unqualified also misleads.

**Sources:** COMP-0035  
**v4 surface:** §4.3 ModelIdentity verification status; §4.4 time-bounded catalog assertions and invocation-to-snapshot linkage.  
**Evidence strength:** `established`  
**Required response class:** `v4 change required`

**Construction/example:** An invocation was resolved using snapshot C0. Later evidence shows C0 stale or wrong. Recomputing against C1 changes the historical basis; doing nothing preserves an unqualified status now known to be suspect.

**Reviewer split:** Both reviewers favor append-only annotation/current-effective confidence while preserving the original resolution basis. They differ in field and record details, which are remedies and excluded here.

**Reason:** The ontology needs to distinguish what was concluded at execution time from what is currently believed about that conclusion; otherwise status semantics are temporally ambiguous.

**Later disposition:** No later operator disposition for COMP-0035 was found in the attached snapshot.

**Excluded remedies:**
- Do not import the specific resolution_quality enum proposed by a reviewer.
- Do not mutate historical records in place or treat current re-resolution as the original event.

## V9L-003 — Catalog acquisition is network-dependent and mutable, while resolution, freshness evaluation over captured data, and status logic can be deterministic and offline. The governance boundary must not be hidden inside ordinary tests.

**Sources:** COMP-0035  
**v4 surface:** §4.4 catalog objects; §9 enforcement matrix; §10 implementation sequence.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** A unit test that calls a live provider catalog becomes nondeterministic, credential-bearing, rate-limited, and time-sensitive; a fixture-only test cannot establish current live catalog truth.

**Reviewer split:** Both reviewers agree on the separation. Their proposed interfaces, annotations, fixture counts, and schedules are implementation preferences.

**Reason:** This is mainly an execution and test-governance requirement rather than a new ontology claim.

**Later disposition:** No later operator disposition for COMP-0035 was found in the attached snapshot.

**Excluded remedies:**
- Do not encode specific test frameworks, schedules, or provider fixture counts in the ontology.

## V9L-004 — Repository records cannot establish the extra-systemic fact that a root principal is genuinely entitled to govern. A record-only chain terminus can state and attribute a claim but cannot make the entitlement true.

**Sources:** COMP-0037, COMP-0040, COMP-0042, COMP-0121  
**v4 surface:** §3 [OPEN] authorization-chain bootstrap; §4.13 AccountablePrincipal and DecisionRecord.  
**Evidence strength:** `established`  
**Required response class:** `explicit limitation sufficient`

**Construction/example:** Two worlds contain byte-identical principal, scope, delegation, and authorization records; in one world the principal is actually accountable, in the other it is not. An internal rule returns the same result in both.

**Reviewer split:** The reviewers converge on the external-entitlement limit. They diverge on whether additional internal acceptance controls are nevertheless useful; that is separated into V9L-005.

**Reason:** v4 already exposes the bootstrap as open rather than pretending to solve it. The rounds support preserving that honesty unless separately governed external evidence semantics exist.

**Later disposition:** CLAIM_IMPACT retained the narrow conclusion that internal records do not establish root authority. Claims that went further and treated every internal control as impossible required correction or re-review.

**Excluded remedies:**
- Do not import v6-v8 standing-authority termination text.
- Do not rename a recorded claim as verified entitlement.

## V9L-005 — The inability to establish real-world root entitlement does not by itself show that internal controls on which records the system accepts are useless. External truth and internal acceptance are distinct objectives.

**Sources:** COMP-0040, COMP-0120  
**v4 surface:** §3 authorization-chain bootstrap open question; P1 authorization framing; P4 anti-laundering principle.  
**Evidence strength:** `disputed`  
**Required response class:** `unresolved`

**Construction/example:** A rule can reject universal or otherwise disallowed scope records without proving that an accepted principal is genuinely entitled in the world. That closes an internal acceptance path but not the external regress.

**Reviewer split:** OpenAI emphasizes that internal bounds cannot solve the extra-systemic regress but may implement a narrower acceptance rule. Claude argues v7 improperly used the regress argument to justify a label-only breadth response.

**Reason:** The rounds establish the conceptual distinction but do not adjudicate which internal acceptance controls, if any, v9 should define.

**Resolution condition:** Resolution requires an operator-adjudicated objective that explicitly distinguishes external entitlement truth from repository-internal record acceptance, together with comparative evidence from concrete constructions showing whether candidate internal acceptance rules close defined paths without being represented as proof of entitlement.

**Later disposition:** CLAIM_IMPACT kept claims that P7 does not entail a label-only scope regime, while several claims about what exact alternative should be adopted were marked needs_re_review.

**Excluded remedies:**
- Do not infer that because a control is incomplete it has no value.
- Do not describe an internal acceptance bound as proof of external entitlement.

## V9L-006 — The scope attacks are not exhausted by breadth. The evidence supports at least an authority-source defect and a target-derived or reverse-fit defect, where scope is selected with knowledge of the act it is intended to authorize.

**Sources:** COMP-0037, COMP-0120  
**v4 surface:** §3 authorization-chain bootstrap open question; §4.13 authority_scope and delegation_reference.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** One construction declares a scope broad enough to cover the intended invocation; another declares a formally narrow scope tailored to authorize exactly itself.

**Reviewer split:** OpenAI names absence of an independent source constraining scope-to-invocation fit. Claude distinguishes origin/self-assertion from reverse-fit correlation. These are compatible rather than identical diagnoses.

**Reason:** The evidence identifies attack classes but does not establish a complete ontology-level rule for scope legitimacy.

**Later disposition:** The operator-approved refutation of CLAIM-7f96b4ee3de269fc confirms that COMP-0037 squarely implicated scope and was not only about self-issuance.

**Excluded remedies:**
- Do not reduce the finding to universal breadth alone.
- Do not treat pre-dating alone, external issuance alone, or parseability alone as a complete solution without separate evidence.

## V9L-007 — A breadth control may close one attack class even if it does not close narrow self-tailoring. Rejecting a partial control solely because it is not a complete solution is not supported by the evidence.

**Sources:** COMP-0037, COMP-0040, COMP-0120  
**v4 surface:** §3 authorization-chain bootstrap open question.  
**Evidence strength:** `disputed`  
**Required response class:** `unresolved`

**Construction/example:** A maximum-breadth rule blocks a universal-scope construction but not a scope tailored to one invocation. That makes it partial, not necessarily valueless.

**Reviewer split:** OpenAI and Claude both distinguish external entitlement from internal acceptance, but neither round adjudicates a concrete breadth policy. The stronger defense-in-depth conclusion is an inference from their split, not reviewer consensus.

**Reason:** The operator must decide whether partial internal controls belong in the ontology, in policy, or nowhere.

**Resolution condition:** Resolution requires evaluation of at least one precisely bounded partial-control hypothesis against an enumerated set of scope-attack families, with the paths closed and left open recorded separately, followed by operator adjudication of whether such defense-in-depth evidence belongs in ontology, policy, or neither.

**Later disposition:** CLAIM_IMPACT refuted claims that COMP-0037 was about self-issuance rather than breadth. It did not admit a breadth rule; alternative-control claims remained for re-review.

**Excluded remedies:**
- Do not treat any specific breadth threshold or co-approval scheme proposed in a review as established.

## V9L-008 — A self_issued marker is descriptive, not an independence control, unless an external policy fixes when independence is required outside the issuing principal’s discretion and a consumer or validator applies the consequence.

**Sources:** COMP-0041, COMP-0042, COMP-0119, COMP-0121  
**v4 surface:** §3 authorization-chain bootstrap; §4.13 InvocationAuthorization independence requirements; deferred AuthorizationPolicy concept.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** The same party declares no independence requirement on its own authorization, records self_issued:true, and the conditional disqualification never fires.

**Reviewer split:** Reviewers disagree whether to retain future conditional semantics or delete control-shaped disqualification language. They agree the current marker does no operative work by itself.

**Reason:** The missing operative semantics belong to independently governed policy and enforcement, not to a self-declared field on one authorization.

**Later disposition:** CLAIM_IMPACT operator-refuted CLAIM-4ffd64de25ee0f86, CLAIM-6e4dce3e8bc65018, and CLAIM-ef4e55078f3fc39a, all of which treated the current marking as a real downstream consequence.

**Excluded remedies:**
- Do not describe self_issued as an active control absent the external requirement and evaluator.
- Do not copy either reviewer’s keep/delete wording into v9 before adjudication.

## V9L-009 — Section-level authorization semantics do not establish that the principal named as issuer actually made or approved the recorded decision. False decision attribution is a distinct attack from false root entitlement.

**Sources:** COMP-0121  
**v4 surface:** §3 decision-kind distinction; §4.13 DecisionRecord issuer invocation, accountable approver, and principal attribution.  
**Evidence strength:** `plausible`  
**Required response class:** `separate gap or policy required`

**Construction/example:** Executor E creates an InvocationAuthorization record attributing issuance to principal P, with E and P distinct so self_issued does not trigger. The chain appears to terminate at P although P never made the decision.

**Reviewer split:** OpenAI constructs the attribution attack. Claude instead reconstructs the self-appointed-root path and does not address false attribution. The supplied Q4 evidence omitted the full DecisionRecord and authentication rules.

**Reason:** Attribution integrity, approval evidence, signatures or equivalent controls, and repository write authority require their own governed semantics.

**Later disposition:** No later operator disposition for COMP-0121 was found in the attached snapshot.

**Excluded remedies:**
- Do not assume record authorship, issuer invocation, accountable approval, and principal identity are interchangeable.
- Do not infer cryptographic design from the finding.

## V9L-010 — Recording a claim and links does not establish complete visibility of every authorization resting on it. Visibility is bounded by what was declared, recorded, linked, traversable, and correctly attributed.

**Sources:** COMP-0041, COMP-0118, COMP-0125  
**v4 surface:** §3 decision records and bootstrap open question; §4.7 subordinate execution; §5 canonical relations.  
**Evidence strength:** `established`  
**Required response class:** `explicit limitation sufficient`

**Construction/example:** An undeclared subordinate invocation or an unlinked authorization exists outside the recorded chain; no field in the visible record enumerates the missing object.

**Reviewer split:** Both reviewers reject present-tense claims of complete visibility. They differ only in the exact honest wording, which is excluded as drafting.

**Reason:** The v4 open question does not need to become a visibility guarantee. A limitation can state the boundary without pretending completeness.

**Later disposition:** CLAIM_IMPACT marked the v7 complete-visibility claims corrected and retained the narrower finding that only correctly declared and linked records can be visible.

**Excluded remedies:**
- Do not say every authorization is visible unless completeness and traversal are established.

## V9L-011 — A requirement that scope be legible as wide is not mechanically usable without a scope grammar, interpretation rule, rendering rule, or adjudication procedure. Whether it remains a manual norm or should be withdrawn is disputed.

**Sources:** COMP-0041, COMP-0118, COMP-0125  
**v4 surface:** §3 authorization-chain bootstrap open question; §4.13 authority_scope.  
**Evidence strength:** `disputed`  
**Required response class:** `unresolved`

**Construction/example:** Two readers can disagree whether free-text scope is broad or bounded, and the ontology supplies no criterion deciding the dispute.

**Reviewer split:** OpenAI treats the prohibition on falsely describing breadth as a legitimate unenforced manual constraint. Claude treats an uninterpretable must as an aspiration dressed as an obligation.

**Reason:** The round establishes missing semantics but not whether a manual anti-misrepresentation norm belongs in the ontology.

**Resolution condition:** Resolution requires ambiguous scope examples to be assessed under a declared interpretation, rendering, or human-adjudication procedure. The evidence must show either reproducible judgments or an explicit operator acceptance of a deliberately non-mechanical norm and its evidentiary limits; reviewer preference alone is insufficient.

**Later disposition:** CLAIM_IMPACT retained the missing-grammar and overclaim findings against v8; no operator adjudication between the keep/delete positions was found.

**Excluded remedies:**
- Do not import v8’s legibility text.
- Do not assume that manual readability is either sufficient or invalid without adjudication.

## V9L-012 — A control-shaped clause followed by a disclaimer that it is inert can remain independently citable and may function as a decoy even when the disclaimer is accurate.

**Sources:** COMP-0119, COMP-0125  
**v4 surface:** §3 authorization-chain bootstrap; sentence-discipline and normative-status semantics if retained in v9.  
**Evidence strength:** `disputed`  
**Required response class:** `unresolved`

**Construction/example:** A downstream plan cites “does not count as independent” but omits the separate passage stating that no policy triggers the rule and nothing is disqualified.

**Reviewer split:** OpenAI argues the future conditional fact is worth retaining with explicit inertness. Claude argues deletion is safer because the caveat is severable from the control-shaped sentence. Both agree the current clause is not a control.

**Reason:** This is a document-design and downstream-consumer risk requiring operator choice, not an established wording solution.

**Resolution condition:** Resolution requires downstream-consumer evidence: either a concrete repository instance of the control-shaped clause being cited without its inertness caveat, or a controlled interpretation comparison showing whether the clause-plus-disclaimer materially invites unsupported control inferences, followed by operator adjudication of the resulting risk.

**Later disposition:** The later v8 round did not adjudicate the reviewer split.

**Excluded remedies:**
- Do not treat accurate disclaimer text as structural enforcement.
- Do not copy either side’s proposed replacement sentence.

## V9L-013 — Calling an authorization self-standing can conflate a recorded chain-termination convention with substantive authorization, even when the root claim is explicitly unverified.

**Sources:** COMP-0121, COMP-0125  
**v4 surface:** §3 authorization-chain bootstrap open question.  
**Evidence strength:** `plausible`  
**Required response class:** `explicit limitation sufficient`

**Construction/example:** A declared principal issues within self-declared scope; the record is called self-standing although the ontology says entitlement was never established.

**Reviewer split:** OpenAI explicitly flags the ambiguity in Q8. Claude’s attack demonstrates the practical path but treats it as compliant disclosure rather than a terminology analysis.

**Reason:** The distinction between “the recorded chain stops here” and “the act is substantively authorized” must remain visible if any chain-termination concept is introduced.

**Later disposition:** No later operator disposition for this Q8 finding was found in the attached snapshot.

**Excluded remedies:**
- Do not import self-standing as a positive status from v7 or v8.

## V9L-014 — The absence of a separate admission event is not itself an admission status. A single current status field, or a row reading amended, not separately admitted, cannot determine whether an amendment inherited, lost, or never acquired governance force.

**Sources:** COMP-0122  
**v4 surface:** Artifact metadata and governance representation rather than substantive §3 text; DecisionRecord/admission-record open choice in §4.13.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** v4 is recorded as admitted in conversation; v5-v7 are amendments with no separate warrants. The table reports the missing event but no rule says what that absence means.

**Reviewer split:** Both reviewers agree the table fixes the narrow v7 metadata conflation but relocates the larger status ambiguity. Claude additionally questions whether the v4 admission row visually overstates conversation-only evidence.

**Reason:** Version-governance state needs an admitted schema and transition rule; ontology prose should not invent status consequences from missing records.

**Later disposition:** The user reports that a later withdrawal decision deliberately exposed the same status-only consumer failure for a withdrawn plan. That current checkout is not present in the attached ZIP and is treated as supplied context, not independently verified here.

**Excluded remedies:**
- Do not copy v8’s table as the solution.
- Do not infer inheritance or invalidation of admission from amendment without an explicit rule.

## V9L-015 — A Slice-C-local authorization result can be complete only for its self-defined checks while remaining incomplete under the ontology’s broader disclosure constraints. Labels such as valid authorization or governed can exceed the checked property set.

**Sources:** COMP-0037, COMP-0043, COMP-0123  
**v4 surface:** §3 distinction between authorization and evidence admission; §4.7 disclosure constraints; §4.13 InvocationAuthorization; C1/C8; consequence/status vocabulary.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** An invocation with an undisclosed subordinate execution, missing effective-input disclosure, or absent outbound-interaction evidence passes every enumerated authorization check and is classified governed.

**Reviewer split:** Reviewers differ on whether disclosure constraints should be checked inside authorize() or explicitly excluded. They agree an unqualified positive label must not imply those checks occurred.

**Reason:** The checked-property boundary and consumer-visible status semantics must be governed together.

**Later disposition:** COMP-0123 confirms that fourteen can be complete by definition for the narrow slice but not for full ABS-0004 compliance.

**Excluded remedies:**
- Do not retain positive labels solely because a disclaimer exists at one definition site.
- Do not force Section 4.7 into authorize() without adjudicating the functional boundary.

## V9L-016 — A direct-only check_depth field reports the inspection bound; it neither detects deeper collisions nor prevents consumers from treating a permitted result as a general independence finding.

**Sources:** COMP-0039, COMP-0037, COMP-0125  
**v4 surface:** C3 no self-adjudication; §4.15 claim/evidence ancestry; future authorization outcome schema.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** Executor A produces X; executor B transforms X into Y; A adjudicates Y. The direct producer is B, so the one-hop check permits, while A remains in evidence ancestry.

**Reviewer split:** Both reviewers agree on the two-hop miss and on the field’s disclosure-only nature. Claude further distinguishes disclosure of the gap’s shape from disclosure that this artifact actually contains a deeper collision.

**Reason:** A partial check can exist, but its result cannot be used as a full ancestry or independence conclusion.

**Later disposition:** The v8 round retained this limitation; Q8 found that even claims about check_depth accurately disclosing the check require schema and production integrity not supplied in evidence.

**Excluded remedies:**
- Do not claim the field prevents misuse.
- Do not treat direct-only permission as evidence of independence.

## V9L-017 — Refusal enumerations omitted materially distinct cases, including absence of matching authorization, unmet independence requirements, undisclosed subordinate execution, and disclosure failures; broad catch-all reasons can conceal different diagnoses.

**Sources:** COMP-0037, COMP-0043, COMP-0123  
**v4 surface:** §3 subordinate authorization distinction if introduced; §4.7 disclosure constraints; §4.13 authorization conditions and status.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** A subordinate invocation is never represented at all. A reason for represented-but-out-of-class subordinate execution does not describe the missing-record disclosure failure.

**Reviewer split:** OpenAI favored checking the disclosure constraints in authorization; Claude favored explicit exclusion for the scoped slice. Both reject silent conflation.

**Reason:** The operator must define the validator boundary and diagnostic vocabulary before completeness can be claimed.

**Later disposition:** COMP-0123 shows the later plan made the exclusion explicit, but retained labels whose portability remained in dispute.

**Excluded remedies:**
- Do not use malformed or conditions unmet as an unstated catch-all for every omitted validity dimension.

## V9L-018 — Role and authorization records are inputs to an authority-separation check, not evidence that the C6 exercise restriction was actually evaluated. Enforcement evidence requires a named artifact recording the check and result.

**Sources:** COMP-0044  
**v4 surface:** C6 authority separation; §9 enforcement matrix.  
**Evidence strength:** `established`  
**Required response class:** `explicit limitation sufficient`

**Construction/example:** A RoleDefinition records adjudicator epistemic authority and repository-mutator action authority, but no artifact evaluates whether both were exercised against the same target without independent verification.

**Reviewer split:** Both reviewers agree Slice C would at most supply prerequisite role records, not the target enforcement evidence.

**Reason:** The enforcement matrix should distinguish dependency artifacts from performed-check evidence.

**Later disposition:** No later contrary disposition was found in the attached snapshot.

**Excluded remedies:**
- Do not cite existence of role records as proof that C6 was enforced.

## V9L-019 — A bound makes a success criterion mechanically checkable only when it replaces the broad property with a finite specified oracle. Naming a limitation without naming fixtures, predicates, commands, manifests, and expected outputs does not create a test.

**Sources:** COMP-0037, COMP-0045, COMP-0124  
**v4 surface:** §8 consequence classes; §9 enforcement matrix; §10 implementation sequence; plan-governance layer.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** A test hand-assigns consequence modifiers and verifies max; it does not establish that the correct modifiers were applicable to the real invocation.

**Reviewer split:** Claude accepts several fixture-bounded criteria as checkable; OpenAI requires a stricter distinction between testing chosen fixtures and establishing the property named. Both agree missing ontology semantics cannot be repaired by test wording.

**Reason:** Exact success oracles belong in implementation governance. Missing ontology semantics must be resolved or the corresponding conformity claim removed.

**Later disposition:** COMP-0124 explicitly preserves the distinction between bounded fixture tests and general semantic claims.

**Excluded remedies:**
- Do not treat example-based passing tests as proof of universal monotonicity, unchanged behavior, or general scope matching.
- Do not require reviewers to author full test suites as part of independent review.

## V9L-020 — Persisting record families, role vocabularies, identity-equality assumptions, scope semantics, and capture omissions before open choices are resolved creates migration costs; omitted historical provenance may be irrecoverable.

**Sources:** COMP-0046  
**v4 surface:** §4.7 executor identities and disclosure; §4.9 roles; §4.13 DecisionRecord open family choice; §5 relations; §10 implementation sequence.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** If subordinate invocations or outbound interactions were not captured at execution time, a later multi-hop validator cannot reconstruct them. If self_issued used exact identifier equality, later equivalence rules may invalidate stored results.

**Reviewer split:** Both reviewers agree capture-time omissions are most expensive; they differ on whether some later changes are schema migration or validation-only depending on final representation.

**Reason:** Migration/versioning policy and admission sequencing should be governed before load-bearing persisted records are seeded.

**Later disposition:** No later operator disposition for COMP-0046 was found in the attached snapshot.

**Excluded remedies:**
- Do not treat every later validator improvement as retroactively repairing missing evidence.

## V9L-021 — Artifact-level production provenance cannot prove claim-level independence when one artifact mixes copied claims, observations, inferences, and paraphrases.

**Sources:** COMP-0032  
**v4 surface:** P3; §4.15 Claim/EvidenceItem; C4, C5, C9.  
**Evidence strength:** `established`  
**Required response class:** `explicit limitation sufficient`

**Construction/example:** Multiple independently produced artifacts repeat the same pre-provenance claim or select evidence using an unrecorded prior, while artifact-level produced_by edges appear independent.

**Reviewer split:** Both reviewers ranked the claim-level lineage limitation among the most severe findings. One response sharpened the laundering path toward selection/copying where derivation cannot be represented.

**Reason:** v4 already states that artifact-level lineage provides potential-dependence detection, not claim-level independence proof. That limitation should remain rather than be converted into a control claim.

**Later disposition:** The metadata says COMP-0032 findings were applied before v4 admission; no contrary later disposition was found.

**Excluded remedies:**
- Do not claim N artifact paths equal N independent claim paths.

## V9L-022 — EffectiveInputManifest completeness and blind-witness status depend on every material information channel, including prompts, retrievals, attachments, tool outputs, session state, subordinate execution, and tool configuration. A self-asserted manifest cannot by itself prove completeness.

**Sources:** COMP-0032  
**v4 surface:** §4.7 executor disclosure; §4.12 EffectiveInputManifest; §4.14 Session; C4 and C5.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** A prior artifact influences search terms offline or provider-managed state contains relevant history not represented in the manifest; the invocation is labeled blind despite the hidden channel.

**Reviewer split:** Both reviewers agree unknown or unreconstructed state defeats blind status. Proposed attestation and instrumentation mechanisms are remedies, not established findings.

**Reason:** The ontology can state the limitation and safe failure; detection and completeness evidence require capture and validation mechanisms.

**Later disposition:** The metadata says COMP-0032 findings were applied before v4 admission; the current implementation status is outside this ledger.

**Excluded remedies:**
- Do not treat a completeness_attestation field as proof of completeness without evidence about the capture mechanism.

## V9L-023 — Composite-executor and external-interaction declarations cannot guarantee that all material calls or ambient effects were disclosed. A deterministic-looking tool can exercise undeclared authority through hardcoded network behavior or privileged downstream consumers.

**Sources:** COMP-0032, COMP-0043, COMP-0046  
**v4 surface:** P4; §4.7 composite-executor, tool-configuration, and external-interaction disclosure; §4.12 EffectiveInputManifest.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** A tool emits a URL that a privileged renderer fetches, triggering a merge; or it makes a hardcoded external call not represented as a subordinate executor or configuration input.

**Reviewer split:** Both COMP-0032 reviewers identify the escape hatch. Later reviewers disagree whether authorization should check these constraints or explicitly exclude them, not whether the underlying disclosure gap exists.

**Reason:** Declarations classify discovered violations but do not detect omitted behavior. Capture/enforcement objects and consumer consequences require separate governance.

**Later disposition:** No later refutation was found; the v8 plan explicitly acknowledged that undisclosed execution could pass its slice checks.

**Excluded remedies:**
- Do not claim disclosure constraints surface, catch, or prevent undeclared interactions.
- Do not limit authority analysis to returned output bytes.

## V9L-024 — Property-scoped verification can be correct yet insufficient for the epistemic status granted. Admission must not infer unverified grounding, truth, calibration, privacy, or other properties from a narrower validator result.

**Sources:** COMP-0032  
**v4 surface:** P2; §4.9 RoleDefinition required_verified_properties; §4.13 EvidenceAdmissionDecision; C10.  
**Evidence strength:** `established`  
**Required response class:** `explicit limitation sufficient`

**Construction/example:** An independent validator proves JSON schema compliance; the artifact is admitted as witness evidence even though source grounding and factual accuracy were never checked.

**Reviewer split:** Both reviewers identify the scope-sufficiency gap. Specific multi-verifier or schema proposals are remedies and excluded.

**Reason:** The admitted baseline should preserve the property-to-status boundary; implementation of admission remains separate.

**Later disposition:** The metadata says COMP-0032 findings were applied before v4 admission.

**Excluded remedies:**
- Do not let a generic verified flag travel without the property scope it establishes.

## V9L-025 — Self-adjudication and independence rules require executor-kind-specific equivalence semantics across models, tools, and humans; unresolved equivalence must never increase independence.

**Sources:** COMP-0032, COMP-0046  
**v4 surface:** P5; §4.3 ModelIdentity; §4.7 executor identities; C3 and C5.  
**Evidence strength:** `established`  
**Required response class:** `explicit limitation sufficient`

**Construction/example:** The same model appears under different endpoint aliases, or one human/tool appears under distinct identifiers. Exact identifier inequality yields a false independent result.

**Reviewer split:** COMP-0032 found the original model-only C3 scope incomplete. COMP-0046 notes that later broader sameness can require re-evaluation of stored results. The exact superclass design remains a preference/open choice.

**Reason:** The baseline must preserve safe unresolved behavior and generic applicability without committing to one inheritance architecture.

**Later disposition:** The current v8 text appears to carry executor-generic equivalence, but v8 is excluded as a remedy source and not the basis of this classification.

**Excluded remedies:**
- Do not equate endpoint or identifier diversity with executor independence.
- Do not require an ExecutorIdentity superclass solely from this finding.

## V9L-026 — DecisionRecord semantics risk dual sources of truth and premature schema lock-in: issuer invocation, issuing principal, accountable approver, status fields, graph relations, activation, supersession, and record-family inheritance were not fully reconciled.

**Sources:** COMP-0032, COMP-0037, COMP-0046  
**v4 surface:** §4.13 DecisionRecord and AccountablePrincipal; §5 canonical relations; open choice between extending existing records and creating a new family.  
**Evidence strength:** `plausible`  
**Required response class:** `separate gap or policy required`

**Construction/example:** The plan stores issuing principal while the ontology also requires issuer invocation and accountable approver; a graph approved_by edge and a field can disagree, with no precedence rule.

**Reviewer split:** OpenAI identified representation inconsistency in COMP-0032 and unreconciled fields in COMP-0037. Claude emphasizes migration cost if records are persisted before the family choice is resolved.

**Reason:** The ontology may identify the decision kinds while leaving concrete record-family resolution to separately governed schema work.

**Later disposition:** No later operator disposition resolving the record-family choice was found in the attached snapshot.

**Excluded remedies:**
- Do not infer that a new record family, subtypes, or field-only representation is already selected.

## V9L-027 — AuthorizationPolicy is a load-bearing missing object when authorization, qualifications, or independence requirements cite policy. Untyped strings or issuer-populated requirements cannot support replayable external constraints.

**Sources:** COMP-0032, COMP-0119  
**v4 surface:** §4.13 InvocationAuthorization policy and independence fields; RoutingPolicy/deferred policy area; C2/C8.  
**Evidence strength:** `established`  
**Required response class:** `v4 change required`

**Construction/example:** An InvocationAuthorization names an applicable policy as text and the issuing principal chooses its own independence requirements; no versioned external rule can be replayed or checked.

**Reviewer split:** COMP-0032 identifies the missing typed policy object. COMP-0119 confirms that without externally fixed policy the self-issued rule remains inert.

**Reason:** v9 reconstruction from v4 must decide whether to define the object, remove dependent claims, or leave an explicit gap; an untyped load-bearing reference is not sufficient.

**Later disposition:** v8 reportedly defined AuthorizationPolicy but deferred it; that unadmitted response is excluded as a remedy source.

**Excluded remedies:**
- Do not copy v8’s AuthorizationPolicy definition.
- Do not claim a defined-but-deferred object makes current controls operative.

## V9L-028 — Consequence combination can be tested over supplied levels, but the correctness of consequence assignment remains undefined when modifier identity, applicability, evidence, and exception semantics are open.

**Sources:** COMP-0032, COMP-0045, COMP-0124  
**v4 surface:** §8 Consequence Classes and applicable modifiers; §9 enforcement matrix.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** A fixture passes max(default, modifiers) after the test author selects modifier levels; nothing establishes that those modifiers should apply to the real target.

**Reviewer split:** Reviewers agree formula consistency is narrower than classifier correctness. They differ on how much fixture-level checkability is enough for a success criterion.

**Reason:** A consequence policy and exact evidence semantics are needed before the result can carry substantive governance meaning.

**Later disposition:** COMP-0124 preserves the distinction; no contrary adjudication was found.

**Excluded remedies:**
- Do not treat ordinal max tests as a complete consequence classifier.

## V9L-029 — A plan must not cite a proposed ontology revision as settled authority for condemning or validating its own behavior. Proposed text and admitted governance rules are different evidentiary states.

**Sources:** COMP-0125  
**v4 surface:** Artifact-governance metadata; relation between ontology status and implementation-plan constraints.  
**Evidence strength:** `established`  
**Required response class:** `separate gap or policy required`

**Construction/example:** The plan says earlier wording contradicted ABS-0004 P6 while the reviewed ABS-0004 v8, including P6, is itself proposed and unadmitted.

**Reviewer split:** Claude identifies the defect directly. OpenAI’s Q8 response criticizes unsupported plan assertions but does not frame this exact governance-state issue.

**Reason:** Dependencies must reference the admitted version and exact admitted rule, or explicitly state that a proposed text is only advisory.

**Later disposition:** The user reports a later decision withdrew v8 and the plan, consistent with this concern; the updated checkout is not present in the ZIP.

**Excluded remedies:**
- Do not use v8 content as v9 authority merely because it was reviewed.

# Baseline properties to preserve

## V9B-001 — Keep authorization, routing selection, and evidence admission distinct; selection is not permission and permission is not admission.
**Sources:** COMP-0032  
**v4 surface:** §3 Three Decisions.  
This is already a v4 baseline property, not a requested delta.

## V9B-002 — Endpoint, provider organization, mutable alias, and model release identity are separate; endpoint diversity never establishes model independence.
**Sources:** COMP-0032  
**v4 surface:** §4.1–§4.4.  
Preserve safe identity separation and unresolved failure behavior.

## V9B-003 — Unknown identity, state, or lineage blocks qualification or yields unresolved; it never increases independence.
**Sources:** COMP-0032  
**v4 surface:** P5, §4.14, C3/C5.  
Preserve as a baseline invariant.

## V9B-004 — Producing an artifact does not grant authority to accept it; role-axis assignment alone does not enforce exercise separation.
**Sources:** COMP-0032  
**v4 surface:** §4.9 and C6/C7.  
Preserve the distinction; enforcement evidence is addressed separately in V9L-018.

## V9B-005 — Decision and verification outputs must carry property scope, provenance, and accountable status distinctions rather than a generic verified label.
**Sources:** COMP-0032  
**v4 surface:** P2, §4.13, C10.  
Preserve; concrete record schemas remain separately governed.

# Unprobed surfaces for a later review round

## UP-001 — Proposed status versus any sentence tag defined as adopted now.
**Status:** independently confirmed in prior full-document review; not asked by the five rounds  
**Handling:** Do not treat as round-established; carry into the next review/adjudication input.

## UP-002 — Plan propagation failure retaining the word necessarily after the ontology itself says the claim is false.
**Status:** independently confirmed in prior full-document review; not asked by the five rounds  
**Handling:** Treat as evidence of propagation risk, not as candidate v9 language.

## UP-003 — A next_action that collapses adjudication into approval.
**Status:** independently confirmed in prior full-document review; not asked by the five rounds  
**Handling:** Governance-process finding for future plan review.

## UP-004 — Executor identity equivalence under aliases, unresolved identities, and cross-kind identity collisions.
**Status:** partly covered by COMP-0032 and COMP-0046 but not directly stress-tested in the two authored question sets  
**Handling:** Retained in V9L-025 and should receive an unframed future attack.

## UP-005 — Authorization graph cycles, conflicting records, expiry, retroactivity, and post-invocation authorization.
**Status:** not directly probed by the selected rounds  
**Handling:** Second-round review surface; no finding asserted yet.

## UP-006 — Seed-authority bootstrap and provenance of who drafts, approves, activates, and then relies on root records.
**Status:** partly adjacent to bootstrap attacks but not fully probed  
**Handling:** Second-round review surface; no remedy inferred.

## UP-007 — Ordinary-language implications of governed, valid authorization, permitted, and self-standing when detached from disclaimers.
**Status:** partly covered by COMP-0037, COMP-0123, and COMP-0125  
**Handling:** Captured in V9L-013 and V9L-015; consumer-only review still warranted.

## UP-008 — Whether a classification-only system is authorization, authorization assessment, or record-coverage classification.
**Status:** partly covered by COMP-0037 but not adjudicated  
**Handling:** Captured in V9L-015; terminology remains unresolved.

## UP-009 — Question-author capture: the same executor wrote both reviewed text and the question set, narrowing what was probed.
**Status:** disclosed by the user; supported by round metadata and process history  
**Handling:** Methodological constraint on the next review, not ontology text.

# Later-disposition audit

`CLAIM_IMPACT.json` records 118 claims: 58 still applies, 35 corrected, 15 adopted, 6 refuted, and 4 needs re-review.

Important corrections carried into this ledger:

- `CLAIM-7f96b4ee3de269fc` — Refutes the assertion that COMP-0037 concerned self-issuance rather than scope breadth.
- `CLAIM-4ffd64de25ee0f86` — Refutes the assertion that self-issued disqualification already had a real downstream consequence.
- `CLAIM-6e4dce3e8bc65018` — Near-duplicate refutation of the same claimed consequence.
- `CLAIM-ef4e55078f3fc39a` — Refutes calling the marking a substantive limitation when nothing requires an independence finding.

Dispositions were proposed by the drafting executor and operator-approved. They are recorded as later governance evidence, not allowed to erase the initial extraction.
