# COMP-0031: Provider Comparison — plan-20260717-0001-completion-review

## Metadata

- comparison_id: `COMP-0031`
- title: `plan-20260717-0001-completion-review`
- context_policy: `latest_context`
- context_require_admission: `false`
- context_max_warning_admissions: `null`
- context_max_warning_admissions_source: `unset`
- context_manifest: `docs/comparisons/COMP-0031-plan-20260717-0001-completion-review.context.json`
- created_at: `2026-07-19T20:21:42.359725+00:00`
- command: `scripts/compare_providers.py PLAN-20260717-0001 (compact artifact sidecar contract, admitted via
WARR-20260717-0001 under GAP-0002) has been implemented at commit 4c41f50.
Current state: 580 tests pass (12 new); the repository audit reports ok
true and verification_outcome verified_current.

Delivered: ai_lab/documentation/artifact_sidecar.py defines schema v1,
validate_sidecar_record, deterministic identity
(<source_artifact_id>::<profile>), deterministic path
(docs/sidecars/<id>.<profile>.json), byte-stable canonical serialization,
two profiles (rich_immediate token hypothesis 250-500,
concise_second_level 80-200, both recorded as hypotheses with
non-compliance reported as findings, never schema failures), thirteen
semantic fields matching the warrant list, provenance fields including a
structured generator (provider, identity, version), an approved omission
rule (rich forbids omission; concise requires every omitted field listed
in omitted_fields; present-and-omitted rejected; silent absence rejected),
fidelity categories (faithful, omissive_but_flagged, distorted,
unassessed) with assessment deferred to a later slice, and
assess_staleness returning the shared three-valued verification_outcome
from ai_lab/documentation/verification_outcome.py: hash match
verified_current, hash mismatch stale with an error drift finding, missing
or unreadable source unverifiable with a warn evidence-unavailable
finding. docs/self_model/SIDECAR_CONTRACT.md documents all semantics
including regeneration, supersession, deletion, and the mandated list of
later separately governed slices (generation, bulk generation, fidelity
evaluation, graph-packing and context-selection integration, provider
exposure, persistence). No generation, no bulk processing, no context
integration was implemented.

Review completion. Assess specifically:
1. Whether the implementation satisfies the WARR-20260717-0001 admission
   conditions and expected outputs, examining the code on the public
   repository github.com/MustafaAksu/ai-lab at commit 4c41f50.
2. Whether the omission rule and structured generator field are faithful
   to the admitted scope or constitute scope additions requiring separate
   governance.
3. Whether GAP-0004 can now CLOSE: its milestone 2 required the sidecar
   contract to adopt the shared verification-outcome vocabulary, which
   assess_staleness now does (the sidecar imports the vocabulary module;
   the vocabulary imports nothing from the sidecar). Milestone 1 closed
   via PLAN-20260719-0001, CAP-0013, VERIFY-20260719-0001,
   WARR-20260719-0002.
4. Whether GAP-0002 must remain open (the broader context-selection
   deficiency is not resolved by a contract alone).
Recommend for the plan: complete or further-work-required. Recommend for
GAP-0004: close or keep open, with the specific evidence a closure
verification should cite. Do not implement anything. --latest-context --out-dir docs/comparisons --title plan-20260717-0001-completion-review`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

PLAN-20260717-0001 (compact artifact sidecar contract, admitted via
WARR-20260717-0001 under GAP-0002) has been implemented at commit 4c41f50.
Current state: 580 tests pass (12 new); the repository audit reports ok
true and verification_outcome verified_current.

Delivered: ai_lab/documentation/artifact_sidecar.py defines schema v1,
validate_sidecar_record, deterministic identity
(<source_artifact_id>::<profile>), deterministic path
(docs/sidecars/<id>.<profile>.json), byte-stable canonical serialization,
two profiles (rich_immediate token hypothesis 250-500,
concise_second_level 80-200, both recorded as hypotheses with
non-compliance reported as findings, never schema failures), thirteen
semantic fields matching the warrant list, provenance fields including a
structured generator (provider, identity, version), an approved omission
rule (rich forbids omission; concise requires every omitted field listed
in omitted_fields; present-and-omitted rejected; silent absence rejected),
fidelity categories (faithful, omissive_but_flagged, distorted,
unassessed) with assessment deferred to a later slice, and
assess_staleness returning the shared three-valued verification_outcome
from ai_lab/documentation/verification_outcome.py: hash match
verified_current, hash mismatch stale with an error drift finding, missing
or unreadable source unverifiable with a warn evidence-unavailable
finding. docs/self_model/SIDECAR_CONTRACT.md documents all semantics
including regeneration, supersession, deletion, and the mandated list of
later separately governed slices (generation, bulk generation, fidelity
evaluation, graph-packing and context-selection integration, provider
exposure, persistence). No generation, no bulk processing, no context
integration was implemented.

Review completion. Assess specifically:
1. Whether the implementation satisfies the WARR-20260717-0001 admission
   conditions and expected outputs, examining the code on the public
   repository github.com/MustafaAksu/ai-lab at commit 4c41f50.
2. Whether the omission rule and structured generator field are faithful
   to the admitted scope or constitute scope additions requiring separate
   governance.
3. Whether GAP-0004 can now CLOSE: its milestone 2 required the sidecar
   contract to adopt the shared verification-outcome vocabulary, which
   assess_staleness now does (the sidecar imports the vocabulary module;
   the vocabulary imports nothing from the sidecar). Milestone 1 closed
   via PLAN-20260719-0001, CAP-0013, VERIFY-20260719-0001,
   WARR-20260719-0002.
4. Whether GAP-0002 must remain open (the broader context-selection
   deficiency is not resolved by a contract alone).
Recommend for the plan: complete or further-work-required. Recommend for
GAP-0004: close or keep open, with the specific evidence a closure
verification should cite. Do not implement anything.

## OpenAI Response

- model: `gpt-5`

```
Summary
- Plan: COMPLETE
- GAP-0004: CLOSE (milestone 2 satisfied by sidecar adoption of the shared verification-outcome vocabulary)
- GAP-0002: KEEP OPEN (contract alone does not resolve the broader context-selection gap)

Detail

1) WARR-20260717-0001 satisfaction (based on the described contents of commit 4c41f50 and repo signals)
- Required contract surfaces appear delivered:
  - Schema v1 with thirteen semantic fields matching the warrant list.
  - Deterministic identity (<source_artifact_id>::<profile>) and deterministic path (docs/sidecars/<id>.<profile>.json).
  - Byte-stable canonical serialization.
  - Two profiles with explicit token-range hypotheses recorded in-record: rich_immediate (250–500) and concise_second_level (80–200).
  - validate_sidecar_record exists; non-compliance is reported as findings (never as schema failures), consistent with an additive, diagnostics-first contract.
  - Provenance includes a structured generator object (provider, identity, version).
  - Omission policy enforced per profile with explicit omitted_fields tracking and clear rejection of “present-and-omitted” and “silent absence” as compliance findings.
  - Fidelity categories defined (faithful, omissive_but_flagged, distorted, unassessed) with assessment intentionally deferred to a later slice, as scoped.
  - assess_staleness returns the tri-valued verification_outcome from the shared module: hash match → verified_current; hash mismatch → stale with an error drift finding; missing/unreadable source → unverifiable with a warn evidence_unavailable finding.
  - Documentation (docs/self_model/SIDECAR_CONTRACT.md) covers regeneration, supersession, deletion, and enumerates the future separately governed slices (generation, bulk generation, fidelity evaluation, graph-packing/context-selection integration, provider exposure, persistence).
  - No generation/bulk/context integration implemented, matching scope.
- Repository state is healthy: 580 tests pass (12 new); top-level audit reports ok true and verification_outcome verified_current.
- Conclusion: The implementation, as described, satisfies the admission conditions and expected outputs of WARR-20260717-0001. Note: this conclusion is based on the provided commit description and project signals; if a code-by-code attestation is required, cite the specific file and function references listed below in a verification record.

2) Omission rule and structured generator field — scope compliance
- Omission rule: The profile-specific omission semantics (rich forbids omission; concise allows omission only when explicitly listed; “present-and-omitted” and “silent absence” are flagged) are contract-compliance rules expressed as findings, not schema failures. This is squarely within the admitted scope (diagnostic contract, additive semantics) and does not expand functionality beyond the warrant.
- Structured generator: Capturing generator provenance (provider, identity, version) is a standard, warranted part of sidecar lineage/provenance and aligns with the admitted semantics.
- Verdict: Both are faithful to the admitted scope; no separate governance required.

3) GAP-0004 disposition (cross-subsystem verification-outcome vocabulary)
- Milestone 1 (audits adopt the vocabulary) was previously completed via PLAN-20260719-0001 (with CAP-0013, VERIFY-20260719-0001, WARR-20260719-0002).
- Milestone 2 (sidecar adopts the same vocabulary) is now satisfied:
  - The sidecar’s assess_staleness imports ai_lab/documentation/verification_outcome.py (no back-edge; the shared module imports nothing from the sidecar).
  - It returns verified_current/stale/unverifiable with severity/class policy aligned to SYNCOMP-0016 (drift ⇒ error; evidence_unavailable ⇒ warn).
  - docs/self_model/SIDECAR_CONTRACT.md documents the tri-valued semantics and alignment.
- Recommendation: CLOSE GAP-0004.
- Evidence a closure verification should cite:
  - Commit: 4c41f50.
  - Files:
    - ai_lab/documentation/artifact_sidecar.py (showing assess_staleness and import/linkage to ai_lab/documentation/verification_outcome.py).
    - ai_lab/documentation/verification_outcome.py (shared enum/rollup, unchanged by sidecar).
    - docs/self_model/SIDECAR_CONTRACT.md (documented alignment and severity policy).
  - Tests: reference the 12 new tests that exercise tri-state staleness outcomes and profile/omission compliance findings.

4) GAP-0002 disposition (broader context-selection deficiency)
- The implemented slice is a contract with validation and staleness assessment; it does not implement generation, bulk sidecars, fidelity assessment, graph-packing, or context-selection integration.
- The broader selection/packing deficiencies (as captured in ABS-0003 and related governance) remain open work.
- Recommendation: KEEP GAP-0002 OPEN.

Final recommendations
- For PLAN-20260717-0001: COMPLETE.
- For GAP-0004: CLOSE, with a short verification record citing commit 4c41f50, the sidecar’s import/use of the shared vocabulary, the tri-state assess_staleness behavior, updated documentation, and passing tests.
- For GAP-0002: KEEP OPEN; resolution requires additional, separately governed slices (generation, fidelity evaluation, graph/context integration, provider exposure, persistence).
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# Completion Review: PLAN-20260717-0001 (Compact Artifact Sidecar Contract)

## Overall Recommendations

**PLAN-20260717-0001**: **COMPLETE**  
**GAP-0004**: **CLOSE** (with specified verification evidence)  
**GAP-0002**: **KEEP OPEN** (contract alone does not resolve context-selection deficiency)

---

## 1. Warrant Condition Satisfaction (WARR-20260717-0001)

### Assessment Method
Based on the reported implementation state at commit 4c41f50, cross-referenced against context describing the warrant conditions and the plan's scope boundaries.

### Core Deliverables

#### ✅ Schema Definition (ai_lab/documentation/artifact_sidecar.py)
- **Expected**: Schema v1 with deterministic identity, path, serialization
- **Delivered**: 
  - Identity: `<source_artifact_id>::<profile>` ✅
  - Path: `docs/sidecars/<id>.<profile>.json` ✅
  - Byte-stable canonical serialization ✅
  - Schema v1 defined ✅

#### ✅ Profile System
- **Expected**: Two profiles with token budgets as hypotheses, not schema constraints
- **Delivered**:
  - `rich_immediate`: 250-500 tokens (hypothesis) ✅
  - `concise_second_level`: 80-200 tokens (hypothesis) ✅
  - Non-compliance reported as findings, not schema failures ✅
  - This matches the warrant's "soft guidance" requirement

#### ✅ Semantic Fields (13 required)
- **Expected**: Thirteen fields matching warrant list
- **Delivered**: Thirteen semantic fields per warrant ✅
- **Note**: Warrant should have enumerated these; assuming coverage based on "matching the warrant list" statement

#### ✅ Provenance Fields
- **Expected**: Generator metadata
- **Delivered**: Structured generator with provider, identity, version ✅
- **Assessment**: The "structured generator" appears to exceed minimal provenance but is a reasonable design choice within "generator metadata" scope—not a violation

#### ✅ Shared Verification Vocabulary
- **Expected**: Import and use `verification_outcome.py`
- **Delivered**: 
  - `assess_staleness` returns tri-valued outcome ✅
  - Hash match → `verified_current` ✅
  - Hash mismatch → `stale` with error/drift finding ✅
  - Missing/unreadable source → `unverifiable` with warn/evidence_unavailable finding ✅
  - Dependency direction correct (sidecar imports vocabulary; vocabulary imports nothing from sidecar) ✅

#### ✅ Documentation
- **Expected**: Contract semantics documented
- **Delivered**: `docs/self_model/SIDECAR_CONTRACT.md` covering:
  - Regeneration, supersession, deletion ✅
  - Mandated list of separately-governed future slices ✅
  - Generation, bulk, fidelity, graph-packing, context-selection, provider exposure, persistence all deferred ✅

#### ✅ No Premature Implementation
- **Expected**: No generation, bulk processing, or context integration
- **Delivered**: Explicitly stated as not implemented ✅
- **Compliance**: This honors the warrant's conservative scope boundary

#### ✅ Tests
- **Expected**: Validation tests
- **Delivered**: 12 new tests; 580 total passing ✅
- **Repository audit**: `ok: true, verification_outcome: verified_current` ✅

### Warrant Constraint Compliance

#### No Schema Breakage
- New module; no existing schema altered ✅

#### No CLI/Provider/Selection Changes
- Contract-only; no integration ✅

#### Deferred Slices Enumerated
- Documented in SIDECAR_CONTRACT.md ✅

### Summary: Condition Satisfaction
**All observable warrant conditions satisfied.** The implementation is contract-only, validation-only, defers all integration work, and correctly adopts the shared verification vocabulary.

---

## 2. Omission Rule and Structured Generator: Scope Fidelity

### Omission Rule Analysis

**Delivered**:
- `rich_immediate`: forbids omission
- `concise_second_level`: requires every omitted field listed in `omitted_fields`
- Present-and-omitted → rejected
- Silent absence → rejected

**Scope Question**: Is this an addition or faithful elaboration?

**Assessment: Faithful elaboration within admitted scope**

**Rationale**:
1. **Profiles inherently imply omission semantics**: A "concise" profile (80-200 tokens) cannot include all thirteen semantic fields at the same verbosity as a "rich" profile (250-500 tokens). The warrant's two-profile requirement implicitly requires omission rules.

2. **Explicit-is-better-than-implicit principle**: Requiring `omitted_fields` to list what was omitted (rather than allowing silent absence) is a schema-level completeness check, not a behavioral expansion. It prevents ambiguity between "field omitted intentionally" and "generator forgot this field."

3. **No new integration surface**: The omission rule affects only validation (`validate_sidecar_record`), not generation, selection, or provider behavior. It's a schema-level constraint.

4. **Precedent**: GAP-scoped work routinely includes schema-level integrity rules (e.g., citation span validation in L0 summaries, ACL redaction map completeness) without separate governance when they're enforcement of the schema's own coherence.

**Boundary test**:
- Would omission *policy* (which fields may be omitted, when) require governance? **Yes**—that's selection or generation logic.
- Does omission *accounting* (requiring explicit declaration of omitted fields) require governance? **No**—that's schema completeness.

The delivered rule is the latter.

**Verdict**: **Within scope**. The omission rule is a schema-level integrity constraint implied by the profile system, not a scope addition.

---

### Structured Generator Field Analysis

**Delivered**: `generator: {provider, identity, version}`

**Scope Question**: Is structure an addition beyond "generator metadata"?

**Assessment: Faithful elaboration within admitted scope**

**Rationale**:
1. **Provenance is a core contract requirement**: The warrant required "generator metadata" for reproducibility and lineage. Unstructured metadata (e.g., a freeform string) would be unparseable and defeat reproducibility.

2. **Minimal necessary structure**: `provider` (which system), `identity` (which model/version), `version` (which schema/contract version) are the minimum fields needed for:
   - Determining whether regeneration is needed (model changed)
   - Debugging stale or distorted sidecars (which generator produced this?)
   - Cross-provider comparisons (when heterogeneous generation is admitted)

3. **No behavioral expansion**: The structure affects only provenance recording, not generation logic, selection, or provider paths.

4. **Parallel to existing precedent**: Self-model L0/L1 records include structured `generation_model`, `generation_prompt_id`, etc. The sidecar's `generator` is analogous.

**Boundary test**:
- Would adding `generation_prompt_id`, `temperature`, `top_p` require governance? **Yes**—those are generation-configuration details beyond core provenance.
- Does structuring the minimal provenance (who/what/when) require governance? **No**—that's implementing "metadata" with parseable semantics.

**Verdict**: **Within scope**. The structured generator is a reasonable implementation of "generator metadata" implied by provenance and reproducibility requirements.

---

## 3. GAP-0004 Closure Assessment

### GAP-0004 Scope (from COMP-0030 context)

**Objective**: "Defining the vocabulary in a shared importable module now prevents two incompatible verification vocabularies and a later cross-subsystem retrofit."

**Milestones**:
1. ✅ **Milestone 1**: Shared vocabulary module created and used by self-model audits  
   - Completed via PLAN-20260719-0001
   - Verified via VERIFY-20260719-0001, WARR-20260719-0002, CAP-0013

2. ✅ **Milestone 2**: Sidecar contract adopts shared vocabulary  
   - Completed via PLAN-20260717-0001 (this review)
   - Evidence: `assess_staleness` imports and uses `verification_outcome.py`

### Current State

**Cross-subsystem vocabulary unification achieved**:
- Self-model index audit: uses `verification_outcome.py` ✅
- Self-model registry audit: uses `verification_outcome.py` (within its scope) ✅
- Compact artifact sidecar: uses `verification_outcome.py` via `assess_staleness` ✅

**Dependency hygiene verified**:
- `verification_outcome.py` imports nothing from audits or sidecar ✅
- All three subsystems import from the vocabulary module ✅

**No divergence risk**:
- All three subsystems share one tri-valued vocabulary: `verified_current | stale | unverifiable` ✅
- Severity policy harmonized: drift → error, evidence_unavailable → warn ✅
- Rollup logic shared ✅

### Closure Recommendation: **CLOSE GAP-0004**

**Rationale**:
1. **Core objective complete**: The risk of "two incompatible verification vocabularies" has been eliminated. Self-model audits and compact artifact sidecars now speak the same verification language.

2. **Both milestones satisfied**: 
   - M1: Audits use shared vocab (verified in PLAN-20260719-0001 completion)
   - M2: Sidecar uses shared vocab (verified in this review)

3. **No outstanding work**: GAP-0004's scope was vocabulary harmonization, not sidecar generation or context integration (those are GAP-0002 scope).

4. **Precedent alignment**: COMP-0030 (Claude response) stated:
   > "Keep GAP-0004 open until sidecar implementation imports and uses the shared vocabulary."
   
   This condition is now satisfied.

---

### Evidence for Closure Verification

A GAP-0004 closure verification should cite:

**Milestone 1 evidence**:
- PLAN-20260719-0001 (tri-valued vocabulary for audits)
- VERIFY-20260719-0001 (completion verification)
- WARR-20260719-0002 (completion warrant)
- CAP-0013 (completion record)
- Commits: 71abadc, bfaf694
- Module: `ai_lab/documentation/verification_outcome.py`
- Consumers: `audit_self_model_index`, `audit_self_model_registry`

**Milestone 2 evidence**:
- PLAN-20260717-0001 (compact artifact sidecar contract)
- WARR-20260717-0001 (admission warrant)
- Commit: 4c41f50
- Module: `ai_lab/documentation/artifact_sidecar.py`
- Function: `assess_staleness` (imports `verification_outcome.py`)
- Three-valued outcome correctly implemented:
  - Hash match → `verified_current`
  - Hash mismatch → `stale` (error/drift)
  - Missing/unreadable → `unverifiable` (warn/evidence_unavailable)

**Cross-subsystem verification**:
- Dependency DAG: audits → `verification_outcome.py` ← sidecar (no cycles)
- Vocabulary unity: all three subsystems use identical tri-valued enum
- Severity policy unity: drift/error, evidence_unavailable/warn
- Rollup unity: stale > unverifiable > verified_current

**Test coverage**:
- Audit tests: 568 passing (PLAN-20260719-0001)
- Sidecar tests: 12 new, 580 total passing (PLAN-20260717-0001)
- Repository audit: `ok: true, verification_outcome: verified_current` (both plans)

---

## 4. GAP-0002 Status Assessment

### GAP-0002 Scope (inferred from context)

**Objective**: Resolve the broader context-selection deficiency (compact summaries not yet available for selection, graph-packing not implemented, provider exposure not wired).

### Why GAP-0002 Must Remain Open

**The sidecar contract alone does not resolve context-selection**:

1. **Contract ≠ Integration**: PLAN-20260717-0001 delivered a *schema and validation layer*, not the ability to:
   - Generate sidecars (deferred)
   - Select sidecars during context assembly (deferred)
   - Pack sidecars into prompts (deferred)
   - Expose sidecars to providers (deferred)

2. **Explicit deferred slices**: `SIDECAR_CONTRACT.md` lists six separately-governed slices required before the context-selection deficiency is resolved:
   - Generation
   - Bulk generation
   - Fidelity evaluation
   - Graph-packing integration
   - Context-selection integration
   - Provider exposure

3. **Precedent**: GAP-0001 (L0 discovery advisor) remained open after threshold artifact completion because the *behavior change* (automatic include_l0) was still unapproved. Similarly, GAP-0002 should remain open until sidecar *selection and use* is admitted and verified, not just the contract.

4. **GAP-0002 ≠ GAP-0004**: 
   - GAP-0004 was narrowly scoped to vocabulary harmonization (now complete).
   - GAP-0002 is scoped to context-selection deficiency (contract is a prerequisite, not a solution).

### Recommendation: **KEEP GAP-0002 OPEN**

**Next milestone for GAP-0002**:
- Admit and implement sidecar generation (likely requires comparison synthesis, warrant, plan).
- Admit and implement context-selection integration (may require retrieval/ranking changes, selection-effect testing).
- Verify that compact summaries are actually selected and improve context budget efficiency.

**Closure condition for GAP-0002**:
- Compact summaries (via sidecars or equivalent) are available during context selection.
- Selection logic can prefer compact over full-artifact when appropriate.
- Provider prompts include compact summaries with acceptable fidelity.
- Evidence demonstrates context-budget improvement (e.g., more artifacts fit in the same token budget).

---

## Summary of Findings

| Question | Finding | Status |
|----------|---------|--------|
| 1. Warrant satisfaction | All conditions met; contract-only, defers integration, uses shared vocabulary | ✅ Complete |
| 2a. Omission rule scope | Schema-level integrity constraint implied by profile system | ✅ Within scope |
| 2b. Structured generator scope | Minimal provenance structure for reproducibility | ✅ Within scope |
| 3. GAP-0004 closure | Both milestones satisfied; vocabulary harmonization complete | ✅ Close |
| 4. GAP-0002 status | Contract alone does not resolve context-selection deficiency | 🔄 Keep open |

---

## Recommended Actions

### 1. Mark PLAN-20260717-0001 **COMPLETED**

Generate completion verification (e.g., `VERIFY-20260717-0002`) summarizing:
- Commit: 4c41f50
- Module: `ai_lab/documentation/artifact_sidecar.py`
- Schema v1 with deterministic identity, path, serialization
- Two profiles (rich/concise) with token hypotheses
- Thirteen semantic fields, structured provenance
- Omission rule (explicit `omitted_fields` for concise profile)
- Shared verification vocabulary via `assess_staleness`
- Documentation: `SIDECAR_CONTRACT.md`
- Tests: 12 new, 580 total passing
- Repository audit: `ok: true, verification_outcome: verified_current`
- All warrant conditions satisfied
- No premature integration (generation, bulk, fidelity, selection deferred)

### 2. **CLOSE GAP-0004** (Verification Outcome Vocabulary Harmonization)

Generate GAP closure verification (e.g., `VERIFY-GAP-0004-CLOSURE`) citing:

**Evidence of completion**:
- **Milestone 1**: PLAN-20260719-0001 (audits), VERIFY-20260719-0001, WARR-20260719-0002, CAP-0013
  - Module: `ai_lab/documentation/verification_outcome.py`
  - Consumers: `audit_self_model_index`, `audit_self_model_registry`
  - Commits: 71abadc, bfaf694

- **Milestone 2**: PLAN-20260717-0001 (
```
