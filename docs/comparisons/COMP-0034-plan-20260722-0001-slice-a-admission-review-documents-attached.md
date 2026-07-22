# COMP-0034: Provider Comparison — PLAN-20260722-0001 slice A admission review (documents attached)

## Metadata

- comparison_id: `COMP-0034`
- title: `PLAN-20260722-0001 slice A admission review (documents attached)`
- created_at: `2026-07-22T15:55:30.227695+00:00`
- command: `scripts/compare_providers.py --title PLAN-20260722-0001 slice A admission review (documents attached) Review the plan below for admission. The full texts of the plan, its source gap, and the relevant ontology sections are included. Do not rely on repository access; quote only text that appears below. If something you need is not present, say so rather than inferring it.

=== PLAN-20260722-0001 ===
{
  "constraints": [
    "Implementation is authorized only within the scope admitted by the future admission warrant for this plan; any expansion requires a separate proposed and admitted plan.",
    "All relations use the GraphRelation shape of ai_lab/documentation/graph_neighborhood.py; no parallel edge vocabulary (ABS-0004 Section 5 adopted constraint).",
    "Record capture must never alter provider-call semantics beyond the settings-default rider; capture failure is reported as an error, not silently swallowed and not fatal to the underlying call.",
    "Field names and semantics follow ABS-0004 v4 exactly; deviations require an ABS revision first.",
    "The settings rider changes only the AI_LAB_CLAUDE_MAX_TOKENS default; per-call overrides and other defaults are untouched."
  ],
  "created_at": "2026-07-22T00:00:00+00:00",
  "created_from": {
    "repo_commit": "c49dec9de04cf59a330a6c205ebe8624f3e8849d",
    "source_gap_id": "GAP-0005"
  },
  "depends_on_capability_ids": [
    "CAP-0014"
  ],
  "evidence_ids": [
    "docs/self_model/gaps/GAP-0005.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
    "docs/comparisons/COMP-0032-abs-0004-invocation-authorization-ontology-challenge-round.md",
    "docs/self_model/capabilities/CAP-0014.json"
  ],
  "expected_outputs": [
    "ai_lab/providers/invocation_record.py (schema v1, validator, canonical serialization, identity and path rules).",
    "Emission wiring in the compare_providers.py path with produced_by references in comparison artifacts.",
    "docs/self_model/PREDICATE_REGISTRY.md (or equivalent) covering the seven Slice A predicates.",
    "Settings change: AI_LAB_CLAUDE_MAX_TOKENS default 16000.",
    "tests/test_invocation_record.py with schema, rejection, and integration fixtures.",
    "Documentation of the record family, its Slice A field subset, and the deferred fields under docs/self_model/ or docs/architecture/."
  ],
  "mitigation": "Field subset is copied from ABS-0004 v4 verbatim with deferred fields documented rather than invented; canonical serialization reuses the sidecar contract's approach; the validator is the acceptance gate for every emitted record from the first fixture onward; the settings rider is a default only, env-overridable, and its motivation and value are recorded in the plan and captured profiles.",
  "next_action": "Run the admission comparison round (expected COMP-0033) with this plan and GAP-0005 as the subject; on operator adjudication, issue the admission warrant and flip status to admitted.",
  "non_goals": [
    "Routing, escalation, or model selection of any kind.",
    "Catalog objects, catalog verification, or identity resolution (Slice B).",
    "RoleDefinition, RoleQualification, InvocationAuthorization, or consequence classes (Slice C).",
    "Lineage traversal, independence assessment, or evidence-admission enforcement (Slice D).",
    "Capture on any path other than compare_providers.py (ask_provider.py directly, memory pipelines, or future paths).",
    "Any consumer of the captured records, including audit checks; C1 provenance_v1 activation is a later decision.",
    "Retroactive records for past invocations; the pre-provenance boundary of ABS-0004 Section 7 applies."
  ],
  "notes": [],
  "objective": "Make provider invocations on one real path representable exactly as ABS-0004 defines them, so that later slices (catalog resolution, roles and authorization, lineage and admission) attach to captured provenance instead of retrofitting it, and so that execution conditions that shape evidence (such as output-token limits) are recorded rather than reconstructed from incidents.",
  "plan_id": "PLAN-20260722-0001",
  "proposed_change": "After a separate admission checkpoint: add ai_lab/providers/invocation_record.py (schema v1, validator, canonical serialization, identity and path rules), wire emission into the compare_providers.py path, add the predicate-registry artifact for the seven Slice A predicates, raise the AI_LAB_CLAUDE_MAX_TOKENS default to 16000, and add tests and fixtures. No behavior of provider calls changes except the settings default; capture is additive and failure to write a record is reported, never silently swallowed.",
  "rationale": [
    "GAP-0005 records that no invocation, identity, manifest, or profile object exists in the running system, and ABS-0004's enforcement matrix lists representability none for C1/C2/C4/C5/C8; Slice A is the admitted ontology's own proposed first boundary.",
    "The slice is deliberately scoped to one path with no routing and no catalog enforcement, matching the sidecar-contract precedent of contract-plus-validator-first slices that verified cleanly.",
    "The COMP-0032 truncation incident is the concrete exhibit: the evidence record could not explain its own truncation because the output-token cap was captured nowhere; this slice makes that class of execution condition part of the record.",
    "Capturing provenance before building catalog, roles, or routing prevents the retrofit debt GAP-0004 was opened to prevent, now at the provider layer."
  ],
  "repo_commit": "c49dec9de04cf59a330a6c205ebe8624f3e8849d",
  "risk": "Schema decisions made here become load-bearing for Slices B-D; a field misdesign propagates. Digest and serialization choices could diverge from the sidecar contract's canonical-JSON precedent if not aligned. The settings rider changes live provider behavior (longer responses, higher cost ceiling per call).",
  "schema_version": "v1",
  "scope": [
    "An invocation-record module defining schema v1 for InvocationRecord, minimal EffectiveInputManifest, and ExecutionProfile as ABS-0004 Sections 4.8, 4.10, and 4.12 specify for Slice A, with a validate_invocation_record entrypoint, deterministic canonical serialization, and deterministic identity and path rules under docs/invocations/.",
    "Emission wired into the scripts/compare_providers.py call path (including its ask-provider substrate) so each provider call on that path produces one InvocationRecord; the comparison artifact records produced_by references to the emitting invocations.",
    "Session identity capture and session-state mode for that path (expected explicit_replayed_context or stateless; recorded, not assumed).",
    "Rendered prompt digest, instruction digests, tool-schema digest where applicable, prior tool-result references, ContextManifest reference when a context pack is used, and completeness_attestation on the manifest.",
    "ExecutionProfile capture including provider request parameters and output-token limits in effect at call time.",
    "spawned edges for subordinate executions on the path; experimental-versus-governed marker defaulting to experimental until an admission consumer exists.",
    "Predicate-registry entries (GraphRelation shape) for the seven Slice A predicates: produced_by, executed_by, requested_via, used_execution_profile, used_inputs, member_of, spawned.",
    "Governed settings rider: raise the AI_LAB_CLAUDE_MAX_TOKENS default from 4096 to 16000 with the change recorded in this plan's completion evidence and reflected in captured profiles.",
    "Validator fixtures covering valid records, each rejection class, and an integration fixture demonstrating end-to-end capture on the compare_providers.py path without network access."
  ],
  "source_capability_ids": [
    "CAP-0014"
  ],
  "source_gap_id": "GAP-0005",
  "status": "proposed",
  "success_criteria": [
    "A run of scripts/compare_providers.py on the covered path produces one InvocationRecord per provider call, each validating through validate_invocation_record, with the comparison artifact carrying produced_by references.",
    "Captured ExecutionProfiles record the output-token limit in effect, and the new default 16000 appears in profiles captured after the settings change.",
    "EffectiveInputManifests carry the rendered prompt digest and completeness_attestation; a fixture demonstrates that a record with attestation absent fails blind-witness-eligibility checks by construction (field-level, no enforcement logic in this slice).",
    "The seven Slice A predicates have registry entries specifying source type, target type, meaning, cardinality, and temporal semantics; relations serialize in GraphRelation shape.",
    "All new behavior covered by tests; the full suite passes; the repository audit remains ok true verified_current; cross-environment reproduction from the public repository succeeds byte-identically."
  ],
  "summary": "Implement ABS-0004 Slice A as admitted and as recommended by GAP-0005: invocation provenance capture on the scripts/compare_providers.py path only. Provider calls on that path emit atomic InvocationRecords with executor reference and identity-verification status, requested API model name, endpoint surface, session identity, a minimal EffectiveInputManifest (rendered prompt digest, instruction digests, ContextManifest reference, tool-schema digest, prior tool-result references, session-state mode, completeness_attestation), an ExecutionProfile reference including output-token limits, spawned edges where subordinate executions occur, an experimental-versus-governed marker, a produced_by relation from the comparison artifact, and success/failure status. Records are validated by a dedicated validator, serialized deterministically, and covered by fixtures; the seven Slice A predicates receive predicate-registry entries in GraphRelation shape. As a governed rider, the AI_LAB_CLAUDE_MAX_TOKENS default is raised so the first captured ExecutionProfile records the corrected limit (motivated by the COMP-0032 truncation incident). Pure capture: nothing reads these records in this slice.",
  "title": "Invocation provenance capture on the provider-comparison path (ABS-0004 Slice A)"
}

=== GAP-0005 ===
{
  "blocked_by": [],
  "category": "provider_infrastructure",
  "evidence": {
    "files_checked": [
      "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
      "docs/comparisons/COMP-0032-abs-0004-invocation-authorization-ontology-challenge-round.md",
      "docs/abstractions/evidence/ADVISOR-MANIFEST.md",
      "docs/abstractions/evidence/ADVISOR-0000-sol-model-stack-proposal.md",
      "ai_lab/providers/settings.py",
      "ai_lab/providers/claude_provider.py",
      "scripts/ask_provider.py",
      "scripts/compare_providers.py"
    ],
    "reason": "ABS-0004 v4 was admitted at commit 56f18a2 with enforcement-matrix rows C1, C2, C4, C5, and C8 marked proposed with representability none: the admitted ontology itself records that its subject matter cannot yet be represented. ai_lab/providers/settings.py holds model identity as environment-overridable strings and AI_LAB_CLAUDE_MAX_TOKENS with default 4096; no identity, endpoint, catalog, invocation, or manifest object exists anywhere in ai_lab/. COMP-0032's Claude response was truncated by that 4096 cap and the saved artifact could not explain the truncation from its own contents; the incident chain recorded in the artifact's addendum is cited in ABS-0004 Slice A as motivation for ExecutionProfile capture. ADVISOR-0000 consists largely of catalog assertions with verification_outcome unverifiable at capture, and no mechanism exists to verify, date, or supersede such claims. C3, C6, C7, C9, C10, and C11 are adopted-manual; their current enforcement evidence is attestations and disclosure statements in warrants, not structural checks."
  },
  "gap_id": "GAP-0005",
  "last_reviewed_at": "2026-07-20T00:00:00+00:00",
  "name": "Provider invocations lack ontology-mandated representation and governance",
  "notes": [
    "Expressed against admitted ABS-0004 v4 per the agreed sequence (ontology first, challenge round, then the gap). Candidate remediation path is Slices A-D of ABS-0004 Section 10, each a separately governed plan; this gap does not pre-admit any of them.",
    "The deferred provider comparison (third-provider decision per the C5 witness-path framing, per-provider escalation ladders, live catalog verification) is intentionally sequenced after Slice B, because its subject matter is catalog assertions and identities that only Slice B makes representable.",
    "The parked CLAUDE_MAX_TOKENS default change should ride with Slice A as a governed settings change, so the new ExecutionProfile capture records the corrected limit from its first use."
  ],
  "priority": "high",
  "recommended_first_slice": "ABS-0004 Section 10 Slice A exactly as admitted: invocation provenance capture on the scripts/compare_providers.py path only. Atomic InvocationRecord; executor reference with identity-verification status; requested API model name; endpoint surface; session identity; minimal EffectiveInputManifest (rendered prompt digest, instruction digests, ContextManifest reference, tool-schema digest, prior tool-result references, session-state mode, completeness_attestation); ExecutionProfile reference including output-token limits; spawned edges; experimental-versus-governed marker; produced_by relation; status; validator and integration fixture. No routing, no catalog enforcement. Relations in GraphRelation shape with predicate-registry entries for the seven Slice A predicates.",
  "related_capabilities": [],
  "risk": "Without invocation provenance, every governed decision that relies on provider outputs rests on undisclosed execution conditions: truncations, configuration differences, session contamination, and model substitutions are invisible after the fact, as COMP-0032's truncation incident showed. Without catalog verification, unverifiable provider claims (ADVISOR-0000 class) can only be excluded by operator vigilance. Without structural authority separation, the C3/C6/C7 disciplines depend entirely on session practice and degrade silently if practice slips. Deferring representation while building routing or escalation would recreate the retrofit debt GAP-0004 was opened to prevent.",
  "schema_version": "v1",
  "status": "open",
  "summary": "The admitted invocation authorization ontology ABS-0004 v4 (commit 56f18a2) defines the objects, relations, and constraints under which AI-Lab authorizes invocations for roles, but none of it is representable or enforceable in the running system. Concretely: provider calls made through ask_provider.py and compare_providers.py leave no InvocationRecord, no executor identity, no ExecutionProfile, no EffectiveInputManifest, and no session identity; model identity is a settings string with no ModelIdentity, ServiceEndpointIdentity, CatalogSnapshot, or CatalogVerification behind it, so every catalog claim (including the entire ADVISOR-0000 model stack) is unverifiable by construction; roles, qualifications, and InvocationAuthorization have no record forms, so the epistemic-authority separation practiced in sessions is testimonial rather than structural; and lineage, independence assessment, and evidence admission (C3-C5, C9-C11) are enforced only by manual discipline with no ancestry capture. The COMP-0032 round demonstrated the operational cost concretely: a response truncation shaped the evidence record and nothing in the record could explain it, because the output-token limit that caused it was captured nowhere. The deficiency blocks the deferred provider comparison (third-provider decision, escalation ladders, live catalog verification), the sidecar generation slice under GAP-0002 (which needs structured generator provenance), and any future routing or escalation policy."
}

=== ABS-0004 SECTIONS 9-11 ===
## 9. Enforcement Matrix

`[DEF]` Normative state: proposed | adopted-manual | machine-enforced.
Representability: none | partial | full. Manual enforcement counts only
when the check leaves a named artifact; the claim that a check happens is
not evidence. Capability dependencies replace slice numbers until admitted
plans exist.

| Constraint | Normative state | Representability | Current enforcement evidence | Target enforcement | Activation condition | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
| C1 staged provenance | proposed | none | none | validator per profile | profile activation decision after capability ships | invocation records; manifests; profiles |
| C2 catalog admission | proposed | none | none | validator + runtime gate | catalog capability ships | catalog snapshots; identities; qualifications |
| C3 no self-adjudication (executor-generic) | adopted-manual | partial | named attestation in completion warrants (for example WARR-20260719-0002 scope adjudications) | per-kind equivalence check + lineage traversal | already active manually | ancestry capture; executor-equivalence semantics |
| C4 hidden witness reuse | proposed | none | none | context-lineage inspection | lineage capability ships | manifests; ancestry |
| C5 lineage independence | proposed | none | none | categorical assessment with reasons | lineage capability ships | ancestry; claim lineage |
| C6 authority separation | adopted, not currently evidenced | partial | none (no current record names the check) | artifact validator | already practiced; evidence begins with role records | role records |
| C7 implementation separation | adopted-manual | partial | VERIFY records (cross-environment verification) | validator on VERIFY records | already active | none; strengthened later |
| C8 decision traceability | proposed | none | none | RoutingDecision validation | routing capability ships | routing records |
| C9 lineage inheritance | adopted-manual | partial | named disclosure statements in records | inheritance propagation | already active manually | claim lineage (full) |
| C10 validator lineage | adopted-manual | partial | verifier identity in VERIFY command records; independence via cross-environment and operator review | VerificationRun with verifier-ancestry check | already active manually | ancestry capture |
| C11 interim independence disclosure | adopted-manual | partial | disclosure statements in DecisionRecords/warrants | admission validator requiring disclosure + named controls | already active manually | none; retired when claim lineage ships |

## 10. Proposed Implementation Sequence

`[PROPOSAL]` Candidate slices, each subject to GAP definition, plan
admission, and review; not commitments:

- Slice A, invocation provenance capture on exactly one path
  (`scripts/compare_providers.py`): atomic InvocationRecord; executor
  reference with identity-verification status; requested API model name;
  endpoint surface; session identity (not mode alone; shared
  provider-managed state is undetectable from a mode flag); minimal
  EffectiveInputManifest containing rendered prompt digest,
  system/developer instruction digests, ContextManifest reference, exposed
  tool-schema digest, prior tool-result references, session-state mode,
  and completeness_attestation (only fields applicable to this path
  populated); ExecutionProfile reference including output-token limits
  (motivated by the COMP-0032 truncation incident, which the record could
  not explain from its own contents); `spawned` edges for subordinate
  executions; experimental-versus-governed marker; `produced_by`; status;
  validator and integration fixture. No routing, no catalog enforcement.
- Slice B, catalog identity resolution: ModelIdentity,
  ServiceEndpointIdentity, atomic assertions in snapshots, requested-name
  to resolved-identity linkage, freshness/verification validator.
- Slice C, role and authorization: RoleDefinition, execution-scoped
  qualification, InvocationAuthorization, consequence class,
  experimental/governed boundary.
- Slice D, lineage and evidence admission: effective-input ancestry,
  pre-provenance inheritance, EvidenceAdmissionDecision, conservative
  independence statuses.

## 11. Defined but Deferred

Run/ProtocolRound, Claim/EvidenceItem, RoutingPolicy and
AuthorizationPolicy enforcement, RoutingDecision enforcement,
VerificationRun and IndependenceAssessment record implementation,
OutboundInteractionLog (content-addressed declaration of a tool's external
interactions: network targets, external writes, privileged output
consumers; the enforcement object for external-interaction disclosure),
HumanActionRecord (audited human actions that shape effective inputs
without issuing a DecisionRecord; privacy-preserving, principal-referenced;
the partial enforcement object for selection provenance), formal
independence assessment beyond categorical statuses, automatic consequence
assignment, full ancestry enforcement, provider-diversity thresholds,
escalation, third-provider integration, session-mode cataloging per
provider API, endpoint mutable-property assertions.


=== QUESTIONS ===
1. Is the scope a single coherent slice consistent with the ABS-0004 Slice A boundary and with small-observable-testable discipline? Name any scope item that belongs to a later slice.
2. Do the non-goals cleanly fence off Slices B-D and all other call paths? Name any gap in the fence.
3. Are the success criteria verifiable and sufficient? Name any criterion that cannot be mechanically checked, and any missing check.
4. Does the AI_LAB_CLAUDE_MAX_TOKENS rider (4096 to 16000) belong in this plan, or should it be severed into a separate governed change? Argue from the plan text.
5. Which schema decisions in this slice would constrain Slices B-D, and which are reversible?
6. Recommendation: admit as written, admit with named conditions (state them), or revise first.

Do not certify or praise. No provider product recommendations.`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Review the plan below for admission. The full texts of the plan, its source gap, and the relevant ontology sections are included. Do not rely on repository access; quote only text that appears below. If something you need is not present, say so rather than inferring it.

=== PLAN-20260722-0001 ===
{
  "constraints": [
    "Implementation is authorized only within the scope admitted by the future admission warrant for this plan; any expansion requires a separate proposed and admitted plan.",
    "All relations use the GraphRelation shape of ai_lab/documentation/graph_neighborhood.py; no parallel edge vocabulary (ABS-0004 Section 5 adopted constraint).",
    "Record capture must never alter provider-call semantics beyond the settings-default rider; capture failure is reported as an error, not silently swallowed and not fatal to the underlying call.",
    "Field names and semantics follow ABS-0004 v4 exactly; deviations require an ABS revision first.",
    "The settings rider changes only the AI_LAB_CLAUDE_MAX_TOKENS default; per-call overrides and other defaults are untouched."
  ],
  "created_at": "2026-07-22T00:00:00+00:00",
  "created_from": {
    "repo_commit": "c49dec9de04cf59a330a6c205ebe8624f3e8849d",
    "source_gap_id": "GAP-0005"
  },
  "depends_on_capability_ids": [
    "CAP-0014"
  ],
  "evidence_ids": [
    "docs/self_model/gaps/GAP-0005.json",
    "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
    "docs/comparisons/COMP-0032-abs-0004-invocation-authorization-ontology-challenge-round.md",
    "docs/self_model/capabilities/CAP-0014.json"
  ],
  "expected_outputs": [
    "ai_lab/providers/invocation_record.py (schema v1, validator, canonical serialization, identity and path rules).",
    "Emission wiring in the compare_providers.py path with produced_by references in comparison artifacts.",
    "docs/self_model/PREDICATE_REGISTRY.md (or equivalent) covering the seven Slice A predicates.",
    "Settings change: AI_LAB_CLAUDE_MAX_TOKENS default 16000.",
    "tests/test_invocation_record.py with schema, rejection, and integration fixtures.",
    "Documentation of the record family, its Slice A field subset, and the deferred fields under docs/self_model/ or docs/architecture/."
  ],
  "mitigation": "Field subset is copied from ABS-0004 v4 verbatim with deferred fields documented rather than invented; canonical serialization reuses the sidecar contract's approach; the validator is the acceptance gate for every emitted record from the first fixture onward; the settings rider is a default only, env-overridable, and its motivation and value are recorded in the plan and captured profiles.",
  "next_action": "Run the admission comparison round (expected COMP-0033) with this plan and GAP-0005 as the subject; on operator adjudication, issue the admission warrant and flip status to admitted.",
  "non_goals": [
    "Routing, escalation, or model selection of any kind.",
    "Catalog objects, catalog verification, or identity resolution (Slice B).",
    "RoleDefinition, RoleQualification, InvocationAuthorization, or consequence classes (Slice C).",
    "Lineage traversal, independence assessment, or evidence-admission enforcement (Slice D).",
    "Capture on any path other than compare_providers.py (ask_provider.py directly, memory pipelines, or future paths).",
    "Any consumer of the captured records, including audit checks; C1 provenance_v1 activation is a later decision.",
    "Retroactive records for past invocations; the pre-provenance boundary of ABS-0004 Section 7 applies."
  ],
  "notes": [],
  "objective": "Make provider invocations on one real path representable exactly as ABS-0004 defines them, so that later slices (catalog resolution, roles and authorization, lineage and admission) attach to captured provenance instead of retrofitting it, and so that execution conditions that shape evidence (such as output-token limits) are recorded rather than reconstructed from incidents.",
  "plan_id": "PLAN-20260722-0001",
  "proposed_change": "After a separate admission checkpoint: add ai_lab/providers/invocation_record.py (schema v1, validator, canonical serialization, identity and path rules), wire emission into the compare_providers.py path, add the predicate-registry artifact for the seven Slice A predicates, raise the AI_LAB_CLAUDE_MAX_TOKENS default to 16000, and add tests and fixtures. No behavior of provider calls changes except the settings default; capture is additive and failure to write a record is reported, never silently swallowed.",
  "rationale": [
    "GAP-0005 records that no invocation, identity, manifest, or profile object exists in the running system, and ABS-0004's enforcement matrix lists representability none for C1/C2/C4/C5/C8; Slice A is the admitted ontology's own proposed first boundary.",
    "The slice is deliberately scoped to one path with no routing and no catalog enforcement, matching the sidecar-contract precedent of contract-plus-validator-first slices that verified cleanly.",
    "The COMP-0032 truncation incident is the concrete exhibit: the evidence record could not explain its own truncation because the output-token cap was captured nowhere; this slice makes that class of execution condition part of the record.",
    "Capturing provenance before building catalog, roles, or routing prevents the retrofit debt GAP-0004 was opened to prevent, now at the provider layer."
  ],
  "repo_commit": "c49dec9de04cf59a330a6c205ebe8624f3e8849d",
  "risk": "Schema decisions made here become load-bearing for Slices B-D; a field misdesign propagates. Digest and serialization choices could diverge from the sidecar contract's canonical-JSON precedent if not aligned. The settings rider changes live provider behavior (longer responses, higher cost ceiling per call).",
  "schema_version": "v1",
  "scope": [
    "An invocation-record module defining schema v1 for InvocationRecord, minimal EffectiveInputManifest, and ExecutionProfile as ABS-0004 Sections 4.8, 4.10, and 4.12 specify for Slice A, with a validate_invocation_record entrypoint, deterministic canonical serialization, and deterministic identity and path rules under docs/invocations/.",
    "Emission wired into the scripts/compare_providers.py call path (including its ask-provider substrate) so each provider call on that path produces one InvocationRecord; the comparison artifact records produced_by references to the emitting invocations.",
    "Session identity capture and session-state mode for that path (expected explicit_replayed_context or stateless; recorded, not assumed).",
    "Rendered prompt digest, instruction digests, tool-schema digest where applicable, prior tool-result references, ContextManifest reference when a context pack is used, and completeness_attestation on the manifest.",
    "ExecutionProfile capture including provider request parameters and output-token limits in effect at call time.",
    "spawned edges for subordinate executions on the path; experimental-versus-governed marker defaulting to experimental until an admission consumer exists.",
    "Predicate-registry entries (GraphRelation shape) for the seven Slice A predicates: produced_by, executed_by, requested_via, used_execution_profile, used_inputs, member_of, spawned.",
    "Governed settings rider: raise the AI_LAB_CLAUDE_MAX_TOKENS default from 4096 to 16000 with the change recorded in this plan's completion evidence and reflected in captured profiles.",
    "Validator fixtures covering valid records, each rejection class, and an integration fixture demonstrating end-to-end capture on the compare_providers.py path without network access."
  ],
  "source_capability_ids": [
    "CAP-0014"
  ],
  "source_gap_id": "GAP-0005",
  "status": "proposed",
  "success_criteria": [
    "A run of scripts/compare_providers.py on the covered path produces one InvocationRecord per provider call, each validating through validate_invocation_record, with the comparison artifact carrying produced_by references.",
    "Captured ExecutionProfiles record the output-token limit in effect, and the new default 16000 appears in profiles captured after the settings change.",
    "EffectiveInputManifests carry the rendered prompt digest and completeness_attestation; a fixture demonstrates that a record with attestation absent fails blind-witness-eligibility checks by construction (field-level, no enforcement logic in this slice).",
    "The seven Slice A predicates have registry entries specifying source type, target type, meaning, cardinality, and temporal semantics; relations serialize in GraphRelation shape.",
    "All new behavior covered by tests; the full suite passes; the repository audit remains ok true verified_current; cross-environment reproduction from the public repository succeeds byte-identically."
  ],
  "summary": "Implement ABS-0004 Slice A as admitted and as recommended by GAP-0005: invocation provenance capture on the scripts/compare_providers.py path only. Provider calls on that path emit atomic InvocationRecords with executor reference and identity-verification status, requested API model name, endpoint surface, session identity, a minimal EffectiveInputManifest (rendered prompt digest, instruction digests, ContextManifest reference, tool-schema digest, prior tool-result references, session-state mode, completeness_attestation), an ExecutionProfile reference including output-token limits, spawned edges where subordinate executions occur, an experimental-versus-governed marker, a produced_by relation from the comparison artifact, and success/failure status. Records are validated by a dedicated validator, serialized deterministically, and covered by fixtures; the seven Slice A predicates receive predicate-registry entries in GraphRelation shape. As a governed rider, the AI_LAB_CLAUDE_MAX_TOKENS default is raised so the first captured ExecutionProfile records the corrected limit (motivated by the COMP-0032 truncation incident). Pure capture: nothing reads these records in this slice.",
  "title": "Invocation provenance capture on the provider-comparison path (ABS-0004 Slice A)"
}

=== GAP-0005 ===
{
  "blocked_by": [],
  "category": "provider_infrastructure",
  "evidence": {
    "files_checked": [
      "docs/abstractions/ABS-0004-invocation-authorization-ontology.md",
      "docs/comparisons/COMP-0032-abs-0004-invocation-authorization-ontology-challenge-round.md",
      "docs/abstractions/evidence/ADVISOR-MANIFEST.md",
      "docs/abstractions/evidence/ADVISOR-0000-sol-model-stack-proposal.md",
      "ai_lab/providers/settings.py",
      "ai_lab/providers/claude_provider.py",
      "scripts/ask_provider.py",
      "scripts/compare_providers.py"
    ],
    "reason": "ABS-0004 v4 was admitted at commit 56f18a2 with enforcement-matrix rows C1, C2, C4, C5, and C8 marked proposed with representability none: the admitted ontology itself records that its subject matter cannot yet be represented. ai_lab/providers/settings.py holds model identity as environment-overridable strings and AI_LAB_CLAUDE_MAX_TOKENS with default 4096; no identity, endpoint, catalog, invocation, or manifest object exists anywhere in ai_lab/. COMP-0032's Claude response was truncated by that 4096 cap and the saved artifact could not explain the truncation from its own contents; the incident chain recorded in the artifact's addendum is cited in ABS-0004 Slice A as motivation for ExecutionProfile capture. ADVISOR-0000 consists largely of catalog assertions with verification_outcome unverifiable at capture, and no mechanism exists to verify, date, or supersede such claims. C3, C6, C7, C9, C10, and C11 are adopted-manual; their current enforcement evidence is attestations and disclosure statements in warrants, not structural checks."
  },
  "gap_id": "GAP-0005",
  "last_reviewed_at": "2026-07-20T00:00:00+00:00",
  "name": "Provider invocations lack ontology-mandated representation and governance",
  "notes": [
    "Expressed against admitted ABS-0004 v4 per the agreed sequence (ontology first, challenge round, then the gap). Candidate remediation path is Slices A-D of ABS-0004 Section 10, each a separately governed plan; this gap does not pre-admit any of them.",
    "The deferred provider comparison (third-provider decision per the C5 witness-path framing, per-provider escalation ladders, live catalog verification) is intentionally sequenced after Slice B, because its subject matter is catalog assertions and identities that only Slice B makes representable.",
    "The parked CLAUDE_MAX_TOKENS default change should ride with Slice A as a governed settings change, so the new ExecutionProfile capture records the corrected limit from its first use."
  ],
  "priority": "high",
  "recommended_first_slice": "ABS-0004 Section 10 Slice A exactly as admitted: invocation provenance capture on the scripts/compare_providers.py path only. Atomic InvocationRecord; executor reference with identity-verification status; requested API model name; endpoint surface; session identity; minimal EffectiveInputManifest (rendered prompt digest, instruction digests, ContextManifest reference, tool-schema digest, prior tool-result references, session-state mode, completeness_attestation); ExecutionProfile reference including output-token limits; spawned edges; experimental-versus-governed marker; produced_by relation; status; validator and integration fixture. No routing, no catalog enforcement. Relations in GraphRelation shape with predicate-registry entries for the seven Slice A predicates.",
  "related_capabilities": [],
  "risk": "Without invocation provenance, every governed decision that relies on provider outputs rests on undisclosed execution conditions: truncations, configuration differences, session contamination, and model substitutions are invisible after the fact, as COMP-0032's truncation incident showed. Without catalog verification, unverifiable provider claims (ADVISOR-0000 class) can only be excluded by operator vigilance. Without structural authority separation, the C3/C6/C7 disciplines depend entirely on session practice and degrade silently if practice slips. Deferring representation while building routing or escalation would recreate the retrofit debt GAP-0004 was opened to prevent.",
  "schema_version": "v1",
  "status": "open",
  "summary": "The admitted invocation authorization ontology ABS-0004 v4 (commit 56f18a2) defines the objects, relations, and constraints under which AI-Lab authorizes invocations for roles, but none of it is representable or enforceable in the running system. Concretely: provider calls made through ask_provider.py and compare_providers.py leave no InvocationRecord, no executor identity, no ExecutionProfile, no EffectiveInputManifest, and no session identity; model identity is a settings string with no ModelIdentity, ServiceEndpointIdentity, CatalogSnapshot, or CatalogVerification behind it, so every catalog claim (including the entire ADVISOR-0000 model stack) is unverifiable by construction; roles, qualifications, and InvocationAuthorization have no record forms, so the epistemic-authority separation practiced in sessions is testimonial rather than structural; and lineage, independence assessment, and evidence admission (C3-C5, C9-C11) are enforced only by manual discipline with no ancestry capture. The COMP-0032 round demonstrated the operational cost concretely: a response truncation shaped the evidence record and nothing in the record could explain it, because the output-token limit that caused it was captured nowhere. The deficiency blocks the deferred provider comparison (third-provider decision, escalation ladders, live catalog verification), the sidecar generation slice under GAP-0002 (which needs structured generator provenance), and any future routing or escalation policy."
}

=== ABS-0004 SECTIONS 9-11 ===
## 9. Enforcement Matrix

`[DEF]` Normative state: proposed | adopted-manual | machine-enforced.
Representability: none | partial | full. Manual enforcement counts only
when the check leaves a named artifact; the claim that a check happens is
not evidence. Capability dependencies replace slice numbers until admitted
plans exist.

| Constraint | Normative state | Representability | Current enforcement evidence | Target enforcement | Activation condition | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
| C1 staged provenance | proposed | none | none | validator per profile | profile activation decision after capability ships | invocation records; manifests; profiles |
| C2 catalog admission | proposed | none | none | validator + runtime gate | catalog capability ships | catalog snapshots; identities; qualifications |
| C3 no self-adjudication (executor-generic) | adopted-manual | partial | named attestation in completion warrants (for example WARR-20260719-0002 scope adjudications) | per-kind equivalence check + lineage traversal | already active manually | ancestry capture; executor-equivalence semantics |
| C4 hidden witness reuse | proposed | none | none | context-lineage inspection | lineage capability ships | manifests; ancestry |
| C5 lineage independence | proposed | none | none | categorical assessment with reasons | lineage capability ships | ancestry; claim lineage |
| C6 authority separation | adopted, not currently evidenced | partial | none (no current record names the check) | artifact validator | already practiced; evidence begins with role records | role records |
| C7 implementation separation | adopted-manual | partial | VERIFY records (cross-environment verification) | validator on VERIFY records | already active | none; strengthened later |
| C8 decision traceability | proposed | none | none | RoutingDecision validation | routing capability ships | routing records |
| C9 lineage inheritance | adopted-manual | partial | named disclosure statements in records | inheritance propagation | already active manually | claim lineage (full) |
| C10 validator lineage | adopted-manual | partial | verifier identity in VERIFY command records; independence via cross-environment and operator review | VerificationRun with verifier-ancestry check | already active manually | ancestry capture |
| C11 interim independence disclosure | adopted-manual | partial | disclosure statements in DecisionRecords/warrants | admission validator requiring disclosure + named controls | already active manually | none; retired when claim lineage ships |

## 10. Proposed Implementation Sequence

`[PROPOSAL]` Candidate slices, each subject to GAP definition, plan
admission, and review; not commitments:

- Slice A, invocation provenance capture on exactly one path
  (`scripts/compare_providers.py`): atomic InvocationRecord; executor
  reference with identity-verification status; requested API model name;
  endpoint surface; session identity (not mode alone; shared
  provider-managed state is undetectable from a mode flag); minimal
  EffectiveInputManifest containing rendered prompt digest,
  system/developer instruction digests, ContextManifest reference, exposed
  tool-schema digest, prior tool-result references, session-state mode,
  and completeness_attestation (only fields applicable to this path
  populated); ExecutionProfile reference including output-token limits
  (motivated by the COMP-0032 truncation incident, which the record could
  not explain from its own contents); `spawned` edges for subordinate
  executions; experimental-versus-governed marker; `produced_by`; status;
  validator and integration fixture. No routing, no catalog enforcement.
- Slice B, catalog identity resolution: ModelIdentity,
  ServiceEndpointIdentity, atomic assertions in snapshots, requested-name
  to resolved-identity linkage, freshness/verification validator.
- Slice C, role and authorization: RoleDefinition, execution-scoped
  qualification, InvocationAuthorization, consequence class,
  experimental/governed boundary.
- Slice D, lineage and evidence admission: effective-input ancestry,
  pre-provenance inheritance, EvidenceAdmissionDecision, conservative
  independence statuses.

## 11. Defined but Deferred

Run/ProtocolRound, Claim/EvidenceItem, RoutingPolicy and
AuthorizationPolicy enforcement, RoutingDecision enforcement,
VerificationRun and IndependenceAssessment record implementation,
OutboundInteractionLog (content-addressed declaration of a tool's external
interactions: network targets, external writes, privileged output
consumers; the enforcement object for external-interaction disclosure),
HumanActionRecord (audited human actions that shape effective inputs
without issuing a DecisionRecord; privacy-preserving, principal-referenced;
the partial enforcement object for selection provenance), formal
independence assessment beyond categorical statuses, automatic consequence
assignment, full ancestry enforcement, provider-diversity thresholds,
escalation, third-provider integration, session-mode cataloging per
provider API, endpoint mutable-property assertions.


=== QUESTIONS ===
1. Is the scope a single coherent slice consistent with the ABS-0004 Slice A boundary and with small-observable-testable discipline? Name any scope item that belongs to a later slice.
2. Do the non-goals cleanly fence off Slices B-D and all other call paths? Name any gap in the fence.
3. Are the success criteria verifiable and sufficient? Name any criterion that cannot be mechanically checked, and any missing check.
4. Does the AI_LAB_CLAUDE_MAX_TOKENS rider (4096 to 16000) belong in this plan, or should it be severed into a separate governed change? Argue from the plan text.
5. Which schema decisions in this slice would constrain Slices B-D, and which are reversible?
6. Recommendation: admit as written, admit with named conditions (state them), or revise first.

Do not certify or praise. No provider product recommendations.

## OpenAI Response

- model: `gpt-5`

```
Here is a focused review tied only to the texts provided.

1) Scope coherence vs ABS-0004 Slice A; items that look like later-slice material
- Coherence: The plan’s scope matches the Slice A boundary quoted in ABS-0004 Section 10: “invocation provenance capture on exactly one path (scripts/compare_providers.py): atomic InvocationRecord; executor reference…; session identity…; minimal EffectiveInputManifest…; ExecutionProfile reference including output-token limits…; spawned edges…; experimental-versus-governed marker; produced_by; status; validator and integration fixture. No routing, no catalog enforcement.” The plan’s scope elements (InvocationRecord, EffectiveInputManifest with rendered prompt digest and completeness_attestation, ExecutionProfile with token limits, spawned edges, experimental/governed marker, produced_by relation, validator, single path only) are all consistent with that boundary.
- Small-observable-testable: The plan confines changes to one script path, introduces a validator, canonical serialization, fixtures, and an integration test. That is compatible with the discipline.
- Possible overreach items:
  - Predicates beyond what is explicitly named in the excerpted Slice A bullet. The plan registers seven predicates: produced_by, executed_by, requested_via, used_execution_profile, used_inputs, member_of, spawned. In the ABS-0004 text we have, produced_by and spawned are explicit; the others are not explicitly enumerated in the provided Slice A paragraph. Because we do not have the predicate list elsewhere in the ontology text here, it is not verifiable from the provided material that all seven belong to Slice A. If any of executed_by, requested_via, used_execution_profile, used_inputs, member_of are not in Slice A, those would belong later.
  - Deterministic identity and path rules: While reasonable and likely needed, Section 10’s Slice A paragraph does not call these out. They may still be fine to include, but they will become load-bearing for later slices.

2) Non-goals: fence quality and any gap
- The non-goals cleanly fence off:
  - Slice B (“Catalog objects, catalog verification, or identity resolution (Slice B).”)
  - Slice C (“RoleDefinition, RoleQualification, InvocationAuthorization, or consequence classes (Slice C).”)
  - Slice D (“Lineage traversal, independence assessment, or evidence-admission enforcement (Slice D).”)
  - Routing/model selection; consumers of the records; retroactive backfill; and all other paths.
- Fence gap to call out:
  - Leakage risk onto ask_provider.py. Scope says “Emission wired into the scripts/compare_providers.py call path (including its ask-provider substrate)…” while non-goals say “Capture on any path other than compare_providers.py (ask_provider.py directly, …).” If wiring occurs in a shared substrate, capture could unintentionally activate on ask_provider.py unless there is an explicit gate. That gating requirement is not spelled out in success criteria. This is a real fence gap to close with a hard path-scoping check and a test that ask_provider.py does not emit.

3) Success criteria: verifiability, sufficiency, and gaps
- Mechanically checkable as written:
  - “One InvocationRecord per provider call,” “validating through validate_invocation_record,” and “comparison artifact carrying produced_by references” are verifiable.
  - “ExecutionProfiles record the output-token limit… new default 16000 appears…” is verifiable by inspecting captured profiles.
  - “EffectiveInputManifests carry the rendered prompt digest and completeness_attestation; a fixture demonstrates that a record with attestation absent fails…” is verifiable if the validator enforces presence.
  - “The seven Slice A predicates have registry entries… relations serialize in GraphRelation shape” is partially verifiable (presence/shape).
  - “All new behavior covered by tests; full suite passes; repository audit ok true verified_current; cross-environment reproduction… byte-identically” are verifiable process outcomes (assuming existing audit and VERIFY flows).
- Elements that cannot be mechanically checked for semantic truth from the provided criteria:
  - The “meaning, cardinality, and temporal semantics” in the predicate registry can be checked for presence but not for correctness of semantics by a generic test.
- Missing or underspecified checks relative to the plan’s own constraints and scope:
  - Canonical serialization and identity determinism: add a cross-environment, byte-identical round-trip test that canonical serialization and identity/path rules produce stable digests/IDs.
  - Relation-shape exclusivity: add tests that non-GraphRelation shapes (or parallel edge vocabularies) are rejected, per the constraint “All relations use the GraphRelation shape…; no parallel edge vocabulary.”
  - Emission scoping: add an integration test that scripts/ask_provider.py produces no InvocationRecord, proving the path gate works.
  - Capture failure handling: add a test demonstrating that a simulated write failure surfaces an error while the underlying provider call still returns (per “capture failure is reported as an error, not silently swallowed and not fatal to the underlying call”).
  - Settings rider discipline: add tests that environment overrides and per-call overrides still take precedence and that only the default changes.
  - Experimental-versus-governed default: add a test that the marker defaults to experimental as stated in scope.
  - Session identity capture: add a check that session identity is present and non-empty per Slice A’s emphasis that “session identity (not mode alone…)” be recorded.
  - Validator rejection coverage: the scope promises “fixtures covering … each rejection class,” but the success criteria do not require that granularity. Make it explicit that each rejection class has a fixture.

4) AI_LAB_CLAUDE_MAX_TOKENS rider: in-scope or separate
- It belongs in this plan. GAP-0005 explicitly recommends: “The parked CLAUDE_MAX_TOKENS default change should ride with Slice A as a governed settings change, so the new ExecutionProfile capture records the corrected limit from its first use.” The plan’s rationale ties this to the COMP-0032 truncation incident and the ExecutionProfile capture. The constraints also bound the rider narrowly: “The settings rider changes only the AI_LAB_CLAUDE_MAX_TOKENS default; per-call overrides and other defaults are untouched.”

5) Schema decisions that will constrain Slices B–D vs reversible decisions
- Constraining (load-bearing for later slices):
  - InvocationRecord v1 field names and semantics (“Field names and semantics follow ABS-0004 v4 exactly; deviations require an ABS revision first.”). These anchor lineage and admission later.
  - Deterministic canonical serialization and identity/path rules: choice of digest/normalization becomes a foundation for cross-slice linkage and verification.
  - EffectiveInputManifest content choices: rendered prompt digest algorithm, instruction digesting, tool-schema digest, prior result references, completeness_attestation field semantics. These directly affect Slice D (lineage, admission) and any independence analyses.
  - ExecutionProfile schema, including where and how output-token limits and request parameters are represented; later routing/admission logic will depend on these semantics.
  - Relation vocabulary and GraphRelation shape for the “seven Slice A predicates.” Predicate names and cardinality/temporal semantics will be reused by lineage and routing.
  - Session identity representation: later role/authorization and lineage logic will bind to this identity form.
  - Experimental-versus-governed marker semantics.
- More reversible or low-risk decisions:
  - The default value change to AI_LAB_CLAUDE_MAX_TOKENS (governed setting) can be changed later without schema break.
  - The set of deferred fields being “documented rather than invented” allows additive evolution later.
  - Emission wiring limited to compare_providers.py is an integration choice, not a schema decision; it can be extended later.
  - File locations for predicate registry/docs can change (“or equivalent”) without affecting record schema.
  - Produced_by references added to comparison artifacts are additive; as long as GraphRelation is stable, adding or adjusting where the relation attaches is manageable.

6) Recommendation
- Admit with named conditions:
  - Add an explicit emission gate that ensures capture activates only when invoked via scripts/compare_providers.py, and a test proving scripts/ask_provider.py does not emit any InvocationRecord.
  - Add success criteria and tests for canonical serialization and identity/path rules determinism across environments (byte-identical round-trip and stable IDs).
  - Add tests for capture failure handling: record-write failure surfaces a reported error while the provider call result is still returned.
  - Add tests proving the settings rider is default-only: environment overrides and per-call overrides remain honored.
  - Add a test that the experimental-versus-governed marker defaults to experimental.
  - Add a success criterion that session identity is present (not just mode) in each record, reflecting ABS-0004 Section 10’s requirement.
  - Add tests that only GraphRelation-shaped relations are emitted and that any alternative/parallel edge vocabulary is rejected.
  - Clarify predicate scope: confirm that executed_by, requested_via, used_execution_profile, used_inputs, and member_of are indeed Slice A predicates per ABS-0004; if any are not in Slice A, defer them to the appropriate later slice or label them “defined but inactive” until the corresponding slice is admitted.
  - Make explicit in success criteria that each validator rejection class has a dedicated fixture (the scope promises this; the criteria should require it).

If these conditions are incorporated, the plan remains a single, testable Slice A implementation aligned with the provided ABS-0004 Section 10 framing and GAP-0005’s recommendation, while closing the identified fence and verification gaps.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# Admission Review: PLAN-20260722-0001

## 1. Scope Coherence Against ABS-0004 Slice A

The scope is **consistent with the admitted Slice A boundary** as quoted in ABS-0004 Section 10. Cross-checking each scope item against the Section 10 text:

- ✓ InvocationRecord, EffectiveInputManifest, ExecutionProfile (Sections 4.8, 4.10, 4.12)
- ✓ Executor reference with identity-verification status
- ✓ Requested API model name, endpoint surface, session identity
- ✓ Rendered prompt digest, instruction digests, ContextManifest reference, tool-schema digest, prior tool-result references, session-state mode, completeness_attestation
- ✓ ExecutionProfile including output-token limits
- ✓ Spawned edges, experimental-versus-governed marker, produced_by, status
- ✓ Validator and integration fixture
- ✓ "No routing, no catalog enforcement"
- ✓ Single path restriction (`compare_providers.py`)

**One item requires clarification**: "Predicate-registry entries (GraphRelation shape) for the seven Slice A predicates" is explicitly scoped, but the Section 10 text does not mention a predicate registry. However, the plan constraints reference "ABS-0004 Section 5 adopted constraint" regarding GraphRelation shape. Without Section 5 text provided, I cannot verify whether the registry itself is Slice A work or infrastructure that should precede it.

**No scope item clearly belongs to a later slice** based on the Section 10 boundary.

## 2. Non-Goals Fence Completeness

The non-goals list explicitly excludes:

- ✓ Slices B, C, D by their defining subjects (catalog objects/verification, roles/authorization, lineage enforcement)
- ✓ Other call paths (`ask_provider.py` directly, memory pipelines, future paths)
- ✓ Consumers of records, including audit checks and C1 enforcement
- ✓ Retroactive records (Section 7 pre-provenance boundary)

**Gap identified**: The non-goals fence does not explicitly exclude **Run/ProtocolRound objects** listed in Section 11 as "Defined but Deferred." The scope mentions "Session identity capture" and "session-state mode" but does not clarify whether these are lightweight fields on InvocationRecord or whether they imply Run/ProtocolRound objects. The GAP-0005 text states "session identity (not mode alone; shared provider-managed state is undetectable from a mode flag)" but does not specify the record structure.

**Recommendation**: Add Run/ProtocolRound to non-goals, or clarify that "session identity" is a simple field, not a structured object.

## 3. Success Criteria Verification

Reviewing each criterion:

1. **"A run of scripts/compare_providers.py [...] produces one InvocationRecord per provider call, each validating"** — Mechanically checkable via test fixture and validator.

2. **"Captured ExecutionProfiles record the output-token limit [...] and the new default 16000 appears"** — Mechanically checkable by inspecting serialized profile after settings change.

3. **"EffectiveInputManifests carry [...] completeness_attestation; a fixture demonstrates that a record with attestation absent fails blind-witness-eligibility checks by construction (field-level, no enforcement logic)"** — **Ambiguity**: "fails blind-witness-eligibility checks by construction (field-level)" is vague. Does this mean the validator rejects records missing the field, or that a separate eligibility function returns false? The parenthetical "no enforcement logic in this slice" suggests the latter, but the criterion does not name the check location or mechanism.

4. **"The seven Slice A predicates have registry entries specifying source type, target type, meaning, cardinality, and temporal semantics"** — Mechanically checkable if the registry format is specified (not quoted here).

5. **"All new behavior covered by tests; the full suite passes"** — Mechanically checkable.

6. **"Repository audit remains ok true verified_current"** — Mechanically checkable via existing VERIFY tooling.

7. **"Cross-environment reproduction from the public repository succeeds byte-identically"** — Mechanically checkable via existing VERIFY tooling.

**Missing checks**:
- No criterion verifies that **capture failure is reported as an error** (per constraints) rather than silently swallowed or fatal. This is a behavioral requirement without a named test.
- No criterion verifies **deterministic canonical serialization** beyond validator acceptance; byte-identical serialization of semantically identical records is not explicitly checked.
- No criterion verifies **identity and path rules** are deterministic and collision-resistant (mentioned in scope and expected outputs but not success criteria).

## 4. AI_LAB_CLAUDE_MAX_TOKENS Rider Placement

**Argument from plan text for inclusion**:

1. **Rationale[2]**: "The COMP-0032 truncation incident is the concrete exhibit: the evidence record could not explain its own truncation because the output-token cap was captured nowhere; this slice makes that class of execution condition part of the record."

2. **Scope**: "ExecutionProfile capture including provider request parameters and output-token limits in effect at call time."

3. **Success criteria[1]**: "Captured ExecutionProfiles record the output-token limit in effect, and the new default 16000 appears in profiles captured after the settings change."

4. **GAP-0005 notes[2]**: "The parked CLAUDE_MAX_TOKENS default change should ride with Slice A as a governed settings change, so the new ExecutionProfile capture records the corrected limit from its first use."

5. **Constraints[4]**: "The settings rider changes only the AI_LAB_CLAUDE_MAX_TOKENS default; per-call overrides and other defaults are untouched."

**The rider belongs in this plan**. The plan's motivation is to capture execution conditions that shaped past evidence but were unrecorded; changing the default while introducing the capture mechanism ensures the first captured profiles reflect the intended operating condition. Severing the rider would create a disjunction: either implement capture with the known-wrong default, then change it later (requiring two sets of fixtures and explanations), or delay capture until the settings change (contradicting the "parked" framing in GAP-0005). The plan treats it correctly as a governed rider with recorded motivation.

## 5. Schema Decisions: Constraining vs. Reversible

**Constraining decisions for Slices B-D**:

1. **Canonical serialization format**: If Slice A adopts JSON-based deterministic serialization (implied by "reuses the sidecar contract's approach"), all later slices must use the same format for digest stability. The plan acknowledges this risk: "Digest and serialization choices could diverge from the sidecar contract's canonical-JSON precedent if not aligned."

2. **Identity and path rules**: If InvocationRecord identity incorporates a digest of its contents, and Slices B-D add fields, the identity calculation must either exclude those fields or version the schema. The plan states "identity and path rules under docs/invocations/" but does not specify versioning strategy.

3. **GraphRelation shape**: Constraint[1] adopts this "for all relations," binding Slices B-D. The constraint references Section 5 (not provided), so I cannot assess implications.

4. **Field names from ABS-0004 v4**: Constraint[3] states "Field names and semantics follow ABS-0004 v4 exactly; deviations require an ABS revision first." This binds all future slices to the v4 ontology unless the abstraction itself is revised.

5. **Executor reference structure**: If Slice A defines executor identity as a string or simple reference, Slice C's RoleDefinition and qualification logic must accommodate that structure.

**Reversible decisions** (additive, no breakage):

1. **Deferred fields**: The plan explicitly documents Slice B/C/D fields as deferred, not omitted. Adding them later extends the schema without breaking Slice A records.

2. **Validator strictness**: The validator can be tightened (reject more) without invalidating existing records, only loosened (accept more) with risk.

3. **Path expansion**: Limiting capture to `compare_providers.py` in Slice A does not prevent wiring other paths later; it's purely scope control.

**Ambiguous** (depends on unquoted details):

1. **Session identity representation**: If Slice A captures session identity as an opaque string, Slice C's session-mode cataloging (Section 11 deferred) may need to parse or supersede it.

## 6. Recommendation

**Admit with the following conditions**:

### Condition 1: Clarify Session Identity Structure
Add to non-goals or scope: confirm that "session identity" is a simple field (string/reference) on InvocationRecord, not a Run or ProtocolRound object. If it is a reference to a separate object, that object's schema must be scoped here or the reference must be deferred to Slice D.

### Condition 2: Success Criterion for Capture Failure Reporting
Add success criterion: "A fixture demonstrates that invocation-record emission failure on the compare_providers.py path is reported as an error (logged/raised) without silently swallowing the failure or terminating the provider call."

### Condition 3: Deterministic Serialization and Identity Verification
Add success criterion: "A fixture demonstrates that two InvocationRecords with identical semantic content serialize to identical byte sequences, and that their computed identities are collision-resistant (different records produce different identities)."

### Condition 4: Schema Versioning Strategy
Add to expected outputs or documentation requirement: the identity and path rules must specify how schema version changes (Slices B-D field additions) affect record identity and digest stability. If identities are version-scoped, state it. If they're content-digest-based and must remain stable, document the exclusion mechanism for future fields.

---

**Justification**: The plan is well-scoped, traceable to the admitted ontology, and correctly treats the settings rider as integral. The four conditions address mechanical verifiability gaps and schema-evolution risks the plan itself identifies but does not fully resolve. None require scope changes, only clarifications and additional test coverage.
```
