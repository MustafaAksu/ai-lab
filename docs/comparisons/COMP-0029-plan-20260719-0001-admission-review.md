# COMP-0029: Provider Comparison — plan-20260719-0001-admission-review

## Metadata

- comparison_id: `COMP-0029`
- title: `plan-20260719-0001-admission-review`
- context_policy: `latest_context`
- context_require_admission: `false`
- context_max_warning_admissions: `null`
- context_max_warning_admissions_source: `unset`
- context_manifest: `docs/comparisons/COMP-0029-plan-20260719-0001-admission-review.context.json`
- created_at: `2026-07-19T16:29:23.972883+00:00`
- command: `scripts/compare_providers.py PLAN-20260719-0001 is proposed under GAP-0004 and is included below. Review it
for admission. Do not implement anything and do not assume it is admitted.

Assess specifically:
1. Whether the shared vocabulary module (ai_lab/documentation/verification_outcome.py)
   with the constraint that it imports from neither self_model.py nor the sidecar
   implementation is the right dependency direction, or whether the vocabulary
   belongs inside self_model.py or the sidecar contract instead.
2. Whether the deterministic rollup rule (stale beats unverifiable beats
   verified_current) is correct, including the mixed case where both confirmed
   drift and unavailable evidence exist in one audit.
3. Whether splitting content-stale classification by git-evidence availability
   is sufficient, or whether any current finding codes cannot be classified
   deterministically into drift versus evidence_unavailable.
4. Whether the success criteria are testable as written and whether any are
   missing (in particular around the registry audit as opposed to the index audit).
5. Whether the plan scope is genuinely additive and admission-safe, or contains
   hidden behavior changes.
Recommend: admit, admit_with_warning, or revise, with reasons.

PLAN CONTENT:
{
    "constraints": [
        "All schema changes are additive; no existing audit output fields, finding codes, or messages are removed, renamed, or repurposed.",
        "The ok field remains boolean and false unless verification_outcome is verified_current; ok=null is prohibited.",
        "The classification table must be built from the actual finding codes present in ai_lab/documentation/self_model.py, not from provider-suggested codes.",
        "The shared vocabulary module must not import from self_model.py or the sidecar implementation; both import from it.",
        "No CLI flags, provider paths, context selection, prompt rendering, or automatic remediation changes.",
        "Sidecar contract integration is limited to the vocabulary module being importable; this plan does not implement sidecar staleness itself.",
        "GAP-0004 remains open until a completion verification and warrant exist."
    ],
    "created_at": "2026-07-19T00:00:00+00:00",
    "next_action": "Review and, if supported, admit this plan through a separate admission warrant. Do not implement the vocabulary module or modify audit output while the plan remains proposed.",
    "objective": "Make the self-model index and registry audits distinguish confirmed drift from unavailable evidence by adding an additive three-valued verification outcome vocabulary (verified_current, stale, unverifiable), defined in a location the admitted compact artifact sidecar contract (PLAN-20260717-0001) can import, without changing existing finding codes, ok-field semantics, or CLI behavior.",
    "plan_id": "PLAN-20260719-0001",
    "proposed_change": "Add a small shared vocabulary module (ai_lab/documentation/verification_outcome.py) defining the outcome enum, the per-finding evidence classification (drift, evidence_unavailable, other), and the deterministic rollup rule (stale if any confirmed drift; else unverifiable if any evidence unavailable; else verified_current). Extend audit_self_model_index and audit_self_model_registry output additively: top-level verification_outcome field, optional evidence_status cause field (no_git_dir, unreachable_repo_head, other), and per-finding class and verification_outcome fields. Reclassify evidence-unavailable findings from error to warn severity, splitting the content-stale classification by whether git evidence was available when the comparison ran. The ok field remains boolean with unchanged fail-closed computation: false unless verification_outcome is verified_current; null is prohibited. Add focused tests covering the three outcomes using controlled fixtures, including a no-git fixture reproducing the observed zip-export case.",
    "rationale": [
        "COMP-0028 records provider consensus that conflating unverifiable with stale is an epistemic defect: the audit currently verifies git availability, not staleness.",
        "SYNCOMP-0016 resolves naming to verification_outcome and confirms the additive-only, fail-closed-preserving approach.",
        "PLAN-20260717-0001 is admitted and its staleness semantics are about to be implemented; defining the vocabulary in a shared importable module now prevents two incompatible verification vocabularies and a later cross-subsystem retrofit.",
        "The observed zip-export case (SELF_MODEL_INDEX_REPO_HEAD_MISSING plus content-stale errors and 4 test failures despite matching record content) demonstrates the defect concretely."
    ],
    "risk": "Severity downgrades for evidence-unavailable findings could silently relax pipelines that count error findings by code rather than reading the ok field; consumers ignoring the new field will continue failing gates on unverifiable environments, which is intended but may prompt local suppressions. Mitigated by leaving ok semantics unchanged, keeping all existing finding codes and messages intact, documenting the classification table built from the actual auditor codes, and asserting in tests that a genuine-drift fixture still yields error severity and ok false.",
    "schema_version": "v1",
    "source_gap_id": "GAP-0004",
    "status": "proposed",
    "success_criteria": [
        "A no-git fixture audit reports verification_outcome unverifiable, ok false, zero error-severity findings, and at least one warn-severity evidence-unavailable finding.",
        "A genuine-drift fixture audit reports verification_outcome stale, ok false, and at least one error-severity drift finding.",
        "A clean git-backed fixture audit reports verification_outcome verified_current and ok true.",
        "The current repository audit still reports ok true and verification_outcome verified_current.",
        "All existing tests pass unchanged except any that assert specific severities for evidence-unavailable findings, which are updated with justification.",
        "The vocabulary is defined once in a shared module with no imports from audit or sidecar implementations.",
        "Self-model index rebuild, full test suite, and audit pass before completion is claimed."
    ],
    "title": "Introduce shared three-valued verification outcome vocabulary in self-model audits"
} --latest-context --out-dir docs/comparisons --title plan-20260719-0001-admission-review`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

PLAN-20260719-0001 is proposed under GAP-0004 and is included below. Review it
for admission. Do not implement anything and do not assume it is admitted.

Assess specifically:
1. Whether the shared vocabulary module (ai_lab/documentation/verification_outcome.py)
   with the constraint that it imports from neither self_model.py nor the sidecar
   implementation is the right dependency direction, or whether the vocabulary
   belongs inside self_model.py or the sidecar contract instead.
2. Whether the deterministic rollup rule (stale beats unverifiable beats
   verified_current) is correct, including the mixed case where both confirmed
   drift and unavailable evidence exist in one audit.
3. Whether splitting content-stale classification by git-evidence availability
   is sufficient, or whether any current finding codes cannot be classified
   deterministically into drift versus evidence_unavailable.
4. Whether the success criteria are testable as written and whether any are
   missing (in particular around the registry audit as opposed to the index audit).
5. Whether the plan scope is genuinely additive and admission-safe, or contains
   hidden behavior changes.
Recommend: admit, admit_with_warning, or revise, with reasons.

PLAN CONTENT:
{
    "constraints": [
        "All schema changes are additive; no existing audit output fields, finding codes, or messages are removed, renamed, or repurposed.",
        "The ok field remains boolean and false unless verification_outcome is verified_current; ok=null is prohibited.",
        "The classification table must be built from the actual finding codes present in ai_lab/documentation/self_model.py, not from provider-suggested codes.",
        "The shared vocabulary module must not import from self_model.py or the sidecar implementation; both import from it.",
        "No CLI flags, provider paths, context selection, prompt rendering, or automatic remediation changes.",
        "Sidecar contract integration is limited to the vocabulary module being importable; this plan does not implement sidecar staleness itself.",
        "GAP-0004 remains open until a completion verification and warrant exist."
    ],
    "created_at": "2026-07-19T00:00:00+00:00",
    "next_action": "Review and, if supported, admit this plan through a separate admission warrant. Do not implement the vocabulary module or modify audit output while the plan remains proposed.",
    "objective": "Make the self-model index and registry audits distinguish confirmed drift from unavailable evidence by adding an additive three-valued verification outcome vocabulary (verified_current, stale, unverifiable), defined in a location the admitted compact artifact sidecar contract (PLAN-20260717-0001) can import, without changing existing finding codes, ok-field semantics, or CLI behavior.",
    "plan_id": "PLAN-20260719-0001",
    "proposed_change": "Add a small shared vocabulary module (ai_lab/documentation/verification_outcome.py) defining the outcome enum, the per-finding evidence classification (drift, evidence_unavailable, other), and the deterministic rollup rule (stale if any confirmed drift; else unverifiable if any evidence unavailable; else verified_current). Extend audit_self_model_index and audit_self_model_registry output additively: top-level verification_outcome field, optional evidence_status cause field (no_git_dir, unreachable_repo_head, other), and per-finding class and verification_outcome fields. Reclassify evidence-unavailable findings from error to warn severity, splitting the content-stale classification by whether git evidence was available when the comparison ran. The ok field remains boolean with unchanged fail-closed computation: false unless verification_outcome is verified_current; null is prohibited. Add focused tests covering the three outcomes using controlled fixtures, including a no-git fixture reproducing the observed zip-export case.",
    "rationale": [
        "COMP-0028 records provider consensus that conflating unverifiable with stale is an epistemic defect: the audit currently verifies git availability, not staleness.",
        "SYNCOMP-0016 resolves naming to verification_outcome and confirms the additive-only, fail-closed-preserving approach.",
        "PLAN-20260717-0001 is admitted and its staleness semantics are about to be implemented; defining the vocabulary in a shared importable module now prevents two incompatible verification vocabularies and a later cross-subsystem retrofit.",
        "The observed zip-export case (SELF_MODEL_INDEX_REPO_HEAD_MISSING plus content-stale errors and 4 test failures despite matching record content) demonstrates the defect concretely."
    ],
    "risk": "Severity downgrades for evidence-unavailable findings could silently relax pipelines that count error findings by code rather than reading the ok field; consumers ignoring the new field will continue failing gates on unverifiable environments, which is intended but may prompt local suppressions. Mitigated by leaving ok semantics unchanged, keeping all existing finding codes and messages intact, documenting the classification table built from the actual auditor codes, and asserting in tests that a genuine-drift fixture still yields error severity and ok false.",
    "schema_version": "v1",
    "source_gap_id": "GAP-0004",
    "status": "proposed",
    "success_criteria": [
        "A no-git fixture audit reports verification_outcome unverifiable, ok false, zero error-severity findings, and at least one warn-severity evidence-unavailable finding.",
        "A genuine-drift fixture audit reports verification_outcome stale, ok false, and at least one error-severity drift finding.",
        "A clean git-backed fixture audit reports verification_outcome verified_current and ok true.",
        "The current repository audit still reports ok true and verification_outcome verified_current.",
        "All existing tests pass unchanged except any that assert specific severities for evidence-unavailable findings, which are updated with justification.",
        "The vocabulary is defined once in a shared module with no imports from audit or sidecar implementations.",
        "Self-model index rebuild, full test suite, and audit pass before completion is claimed."
    ],
    "title": "Introduce shared three-valued verification outcome vocabulary in self-model audits"
}

## OpenAI Response

- model: `gpt-5`

```
Verdict: admit_with_warning

Summary
The plan aligns with the synthesized provider consensus in SYNCOMP-0016 and COMP-0028: introduce a shared, tri-valued verification outcome; preserve ok semantics; add per-finding classification; and adopt a deterministic rollup where stale dominates unverifiable, which dominates verified_current. The proposed dependency direction for a neutral, shared vocabulary module is appropriate. However, two issues warrant warnings or minor adjustments before or during admission: (a) the plan downgrades severities for evidence_unavailable, which is an intentional behavior change that can silently relax pipelines keyed on error counts, and (b) success criteria omit explicit registry-audit coverage and a mixed-case rollup test. Governance umbrella alignment should also be double-checked.

Detailed assessment

1) Shared vocabulary module dependency direction
- Assessment: Correct. Defining the vocabulary in a neutral, shared module that imports from neither self_model.py nor the sidecar implementation is the right direction. It avoids circular dependencies, prevents duplicated enums, and enables both subsystems to share the same contract.
- Minor suggestion: The chosen package path ai_lab/documentation/verification_outcome.py is acceptable if that namespace is the home for importable contracts. If “documentation” is primarily prose/ADR, consider a neutral code-oriented namespace (e.g., ai_lab/contracts or ai_lab/shared) to better signal stability and avoid conflation with docs. This is a naming/placement nit, not a blocker.
- Scope guard: Keep the module to pure types/constants and the generic rollup function. Do not embed any classification table that depends on concrete auditor finding codes there; that mapping should live in the auditor code to satisfy the constraint that the shared module does not import self_model.py.

2) Deterministic rollup rule
- Assessment: Correct as written and consistent with SYNCOMP-0016.
  - Rule: stale if any confirmed drift; else unverifiable if any evidence_unavailable; else verified_current.
  - Mixed case: When both confirmed drift and unavailable evidence exist in one audit, stale must dominate. This preserves the semantics that positive evidence of drift cannot be masked by missing evidence elsewhere.
- Recommendation: Add an explicit mixed-case test to success criteria to lock this in.

3) Splitting content-stale classification by git-evidence availability
- Assessment: Sufficient, with care. The synthesized guidance explicitly calls out CONTENT_STALE as the one code that spans two realities:
  - With evidence (e.g., reachable repo_head, or hash mismatch with available provenance): class=drift, severity=error.
  - Without evidence (e.g., no .git, shallow history, unreachable commit): class=evidence_unavailable, severity=warn.
- Determinism caveat: Ensure the classification table is built against the actual set of finding codes (as the plan states) and that any codes which bundle multiple causes are disambiguated via the new per-finding fields (class and, if needed, an evidence_cause/evidence_status). If you cannot deterministically tell which branch applies for a specific finding code without additional context, either:
  - Split the emission site into two codes, or
  - Always attach the disambiguating per-finding attributes and key classification on those, not just the code.
- Likely straightforward mappings (based on SYNCOMP-0016/COMP-0028 examples):
  - SELF_MODEL_INDEX_REPO_HEAD_MISSING → evidence_unavailable (warn)
  - SELF_MODEL_INDEX_SHALLOW_HISTORY → evidence_unavailable (warn)
  - SELF_MODEL_INDEX_CONTENT_HASH_MISMATCH → drift (error)
  - SELF_MODEL_INDEX_CONTENT_STALE → drift (error) when evidence available; evidence_unavailable (warn) when not.
- For registry audit, make a parallel table for any REGISTRY_* codes; if any are ambiguous, apply the same approach.

4) Success criteria: testability and gaps
- Generally testable:
  - The three fixture-driven cases (no-git/unverifiable, genuine-drift/stale, clean/verified_current) are clear and actionable for the index audit.
  - Ensuring ok semantics and shared vocabulary placement are verifiable.
- Missing/should add:
  - Explicit registry audit coverage: add parallel fixtures and assertions for audit_self_model_registry producing the same three outcomes.
  - Mixed-case rollup: a fixture where both a confirmed drift and an evidence_unavailable condition co-occur, asserting the rollup yields stale.
  - Evidence status enumeration: tests that specific causes (e.g., no_git_dir vs unreachable_repo_head) map to evidence_status consistently.
  - Backward-compat invariants: a snapshot/diff asserting that, aside from the new additive fields and the expected severity downgrade for evidence_unavailable, no finding codes/messages are changed or suppressed; ok remains computed identically.
  - Import direction: a simple import test in the sidecar package that imports the shared module (without implementing sidecar staleness) to prove the module is truly dependency-neutral.

5) Additivity vs. hidden behavior changes
- Schema: Additive, as required. No renames or removals proposed.
- Behavior: There is a deliberate change: reclassifying evidence-unavailable findings from error to warn. This is a behavior change and can relax pipelines that key on error counts, exactly as your risk section notes. SYNCOMP-0016 flags this as a known risk and suggests considering a transitional configuration. Your constraints prohibit new CLI flags; even so, a transitional config toggle (e.g., env var or policy file) is not mentioned.
- Guidance:
  - If your governance requires minimizing breakage for consumers who count errors, consider adding a documented, temporary config (not necessarily a CLI flag) in a follow-on slice to optionally keep evidence_unavailable as error during migration. Given your stated constraint, this does not block admission, but it does warrant a clear operator communication plan.
  - Ensure you do not silently suppress findings in unverifiable contexts; only reclassify severity and add the disambiguating fields. Suppression would constitute an additional behavior change.

Additional note: governance umbrella
- SYNCOMP-0016 frames this slice under existing audit/canonical-records governance (it references GAP-0003). This plan is proposed under GAP-0004. Before finalizing admission, confirm that GAP-0004 is indeed the intended umbrella for audit vocabulary harmonization across the self-model and sidecar surfaces; otherwise, retarget to the appropriate GAP. This is an administrative alignment, not a technical blocker.

Recommendation rationale
- Strong alignment with synthesized guidance: shared enum, additive fields, unchanged ok semantics, deterministic rollup, per-finding classification, and severity policy match SYNCOMP-0016.
- Warnings are limited to:
  - The intentional severity downgrade’s impact on consumers that count error findings (mitigate via comms or transitional config).
  - Expanding success criteria to include registry audit coverage and a mixed-case rollup test.
  - Optional relocation of the shared module to a more semantically neutral namespace and confirmation of governance umbrella.

Decision: admit_with_warning
- Proceed, provided you:
  - Add registry-audit success criteria and a mixed-case rollup test.
  - Document the severity change prominently and plan for consumer migration; consider a transitional configuration in a subsequent, narrowly scoped slice if needed.
  - Confirm GAP umbrella alignment (GAP-0004 vs GAP-0003) before issuance of the admission warrant.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# Admission Review: PLAN-20260719-0001

## Overall Recommendation: **ADMIT_WITH_WARNING**

This plan addresses a genuine epistemic defect with a sound technical approach and is admission-safe, but carries operational risks that require explicit acknowledgment and mitigation commitments.

---

## Assessment by Question

### 1. Shared vocabulary module dependency direction

**Assessment: Correct as specified.**

**Rationale:**
- The constraint that `ai_lab/documentation/verification_outcome.py` imports from neither `self_model.py` nor the sidecar implementation is the right dependency direction.
- Both the self-model auditor and the admitted sidecar contract (PLAN-20260717-0001) need a shared verification vocabulary; placing it in a standalone module prevents circular imports and subsystem coupling.
- The vocabulary is semantically independent: it defines outcome states, classification categories, and rollup logic—none of which depend on audit implementation details or sidecar persistence.
- Importing the vocabulary into both consumers ensures single-source-of-truth semantics and avoids the divergent-vocabulary risk SYNCOMP-0016 warns against.

**Alternative considered and rejected:**
- Placing the vocabulary inside `self_model.py` would force the sidecar to import from the self-model module, creating a layering violation (the sidecar contract should not depend on audit internals).
- Placing it in the sidecar contract would force the auditor to import from a persistence layer, which is architecturally backward.

**Verdict:** No change needed; the plan is correct.

---

### 2. Deterministic rollup rule

**Assessment: Correct, including mixed cases.**

**Rationale:**
- The rollup rule `stale > unverifiable > verified_current` is semantically sound:
  - **Stale beats unverifiable:** If any drift is confirmed, the audit has found a defect; missing evidence for *other* records does not negate the confirmed drift. The top-level status should reflect the worst verified state.
  - **Unverifiable beats verified_current:** If some evidence is missing, the audit cannot claim full verification, even if available evidence shows no drift.
- **Mixed case (both confirmed drift and unavailable evidence):** The plan correctly resolves this to `stale` at the top level. Example: records A and B verify clean, record C has confirmed content drift (stale), record D has no git evidence (unverifiable) → audit reports `verification_outcome: stale` because at least one drift was confirmed.
- The `ok` field correctly computes as `false` in both `stale` and `unverifiable` cases, preserving fail-closed semantics.

**Edge case confirmation:**
- All findings are `evidence_unavailable` → `unverifiable`, `ok: false`.
- At least one `drift` finding exists → `stale`, `ok: false`, regardless of concurrent unverifiable findings.
- Zero findings → `verified_current`, `ok: true`.

**Verdict:** No change needed; the rollup is deterministic and correct.

---

### 3. Content-stale classification determinism

**Assessment: Sufficient with one clarification required.**

**Current plan:** "Split content-stale classification by whether git evidence was available when the comparison ran."

**Analysis:**
- The existing `SELF_MODEL_INDEX_CONTENT_STALE` code must be disambiguated:
  - **Git available, content hash mismatch** → `class: drift`, `severity: error`, `verification_outcome: stale`.
  - **Git unavailable, cannot verify content** → `class: evidence_unavailable`, `severity: warn`, `verification_outcome: unverifiable`.
- This split is deterministic if the auditor can reliably detect git-evidence availability *at the point of issuing the finding*.

**Risk identified:**
- If the auditor emits `CONTENT_STALE` **before** checking git availability (e.g., triggers on a missing cached comparison, then later discovers no git), the finding code alone cannot deterministically classify.
- **Mitigation required:** The classification table must specify that `CONTENT_STALE` classification depends on **context captured when the finding is emitted** (e.g., a `has_git_evidence` boolean in the finding's internal state or a code split: `CONTENT_STALE_VERIFIED` vs. `CONTENT_STALE_UNVERIFIABLE`).

**Other codes from context:**
- `SELF_MODEL_INDEX_REPO_HEAD_MISSING`: Always `evidence_unavailable` (git unavailable).
- `SELF_MODEL_INDEX_SHALLOW_HISTORY`: Always `evidence_unavailable` (git incomplete).
- Any `CONTENT_HASH_MISMATCH` with git evidence: Always `drift`.

**Verdict:** The split is conceptually sufficient but requires a clarification constraint:

> **Add constraint:** "The classification of CONTENT_STALE findings into drift versus evidence_unavailable must be deterministic from the finding's emitted context (e.g., a git-evidence-available flag or distinct code variants). Findings emitted before git availability is checked are prohibited."

---

### 4. Success criteria testability and coverage

**Assessment: Testable but incomplete for registry audits.**

**Testable criteria:**
- ✅ No-git fixture, genuine-drift fixture, clean-git fixture outcomes are testable with controlled fixtures.
- ✅ Current repository audit assertion is testable (regression gate).
- ✅ Existing test pass rate is measurable.
- ✅ Shared vocabulary module structure is verifiable (import test).
- ✅ Rebuild/suite/audit pass is standard completion gate.

**Missing coverage:**
- **Registry audit (`audit_self_model_registry`):** The plan mentions extending both index and registry audits but success criteria only specify index-audit fixtures.
  - Registry audits face the same unverifiable scenarios (e.g., registry entries referencing artifacts in a no-git environment).
  - Without explicit registry success criteria, the slice could ship with index-only coverage and defer registry integration, creating the divergence risk SYNCOMP-0016 warns against.

**Verdict:** Add registry-specific success criteria:

> **Add success criterion:** "The registry audit (audit_self_model_registry) emits verification_outcome for rollup across registry entries and per-entry verification_status where applicable, using the same vocabulary module and classification table as the index audit."

> **Add success criterion:** "A fixture registry audit with at least one registry entry referencing an artifact in a no-git environment reports verification_outcome unverifiable and zero error-severity findings for evidence-unavailable causes."

---

### 5. Additive scope and hidden behavior changes

**Assessment: Genuinely additive with one operational behavior change that is acceptable.**

**Additive guarantees upheld:**
- ✅ No fields removed, renamed, or repurposed.
- ✅ `ok` field remains boolean with unchanged computation.
- ✅ Finding codes and messages unchanged.
- ✅ No CLI, provider, selection, or prompt changes.
- ✅ Sidecar integration limited to vocabulary import (sidecar staleness deferred).

**Operational behavior change (severity downgrade):**
- **Current behavior:** Evidence-unavailable findings (e.g., `REPO_HEAD_MISSING`) emit `severity: error`.
- **New behavior:** Evidence-unavailable findings emit `severity: warn`.
- **Is this a hidden change?** No—it is explicitly called out in the plan and risk section.
- **Is it admission-safe?** Yes, because:
  - The `ok` field still returns `false` for unverifiable, preserving fail-closed gates.
  - Pipelines keying on `ok` see no change.
  - Pipelines counting errors by code **will** see a change, but this is the intended epistemic correction (the audit should not report errors when it cannot verify).
  - The risk acknowledges this and proposes documentation and test guardrails.

**Hidden change risk audit:**
- Could test expectations silently change? **Mitigated:** The success criteria require justification for any severity assertion updates.
- Could pipelines silently relax? **Mitigated:** The `ok` field computation is unchanged; genuine drift still yields `ok: false` and error severity.
- Could the rollup introduce a state machines don't expect? **Mitigated:** The `verification_outcome` field is new (additive); old consumers ignore it.

**Verdict:** The scope is genuinely additive. The severity downgrade is an intentional, documented, and operationally sound correction of the epistemic defect.

---

## Warnings and Conditions

### Warning 1: Operational monitoring adjustment required
**Severity: Medium**

Pipelines, dashboards, or CI gates that count audit errors **by finding code** rather than the `ok` field will see reduced error counts in no-git environments after this change ships. While this is the intended correction, operators must be notified.

**Mitigation required:**
- Add a success criterion: "Documentation or operator guidance is provided explaining the severity reclassification and advising consumers to gate on the `ok` field or the new `verification_outcome` field rather than error counts by code."
- Consider a transition log message (warn-level) the first time an audit emits `verification_outcome: unverifiable` in a session, explaining the semantic change.

### Warning 2: CONTENT_STALE classification requires implementation care
**Severity: Medium**

The plan relies on deterministic classification of `CONTENT_STALE` by git-evidence availability, but the current auditor implementation may not capture this context atomically when findings are emitted.

**Mitigation required (already recommended in §3):**
- Add the constraint clarifying that git-evidence availability must be known *when the finding is emitted*, not retroactively inferred.
- During implementation, if the auditor cannot deterministically split `CONTENT_STALE`, consider introducing two codes: `CONTENT_STALE_VERIFIED_DRIFT` and `CONTENT_STALE_UNVERIFIABLE`.

### Warning 3: Registry audit coverage must be confirmed
**Severity: Low**

The plan mentions registry audits but success criteria omit registry-specific tests.

**Mitigation required (already recommended in §4):**
- Add the registry success criteria specified above.

---

## Missing Elements (Non-Blocking)

1. **No explicit governance milestone update:** The plan proposes a GAP-0004 slice but does not specify whether GAP-0004's description or milestones need amendment to reflect this vocabulary work. **Recommendation:** Confirm GAP-0004 scope covers verification vocabulary; if not, add a milestone or cross-reference.

2. **No L1 update plan:** Introducing a new shared module and changing audit output schema may warrant L1 episode generation or self-model index rebuild. The success criteria include "self-model index rebuild" but do not specify whether new L1 records are expected. **Recommendation:** Clarify whether `ai_lab/documentation/verification_outcome.py` should appear in the self-model index and, if so, whether this plan includes its L1 generation.

3. **No provider comparison or warrant source:** The plan rationale cites COMP-0028 and SYNCOMP-0016 but does not specify whether a warrant should be generated from those sources before implementation. **Recommendation:** Consider generating a warrant (e.g., WARR-20260719-000X) summarizing the provider consensus before marking the plan admitted.

---

## Final Recommendation: **ADMIT_WITH_WARNING**

**Admit because:**
- The plan addresses a genuine epistemic defect identified by provider consensus (COMP-0028, SYNCOMP-0016).
- The shared vocabulary module dependency direction is correct.
- The rollup rule is deterministic and semantically sound.
- The scope is genuinely additive with no hidden breaking changes.
- The success criteria are testable (with additions recommended).

**Warnings and required additions:**
1. Add constraint clarifying `CONTENT_STALE` classification determinism (§3).
2. Add registry audit success criteria (§4).
3. Add operator guidance/documentation success criterion (Warning 1).
4. Confirm GAP-0004 scope or add milestone (Missing Element 1).
5. Clarify L1 generation expectations for the new module (Missing Element 2, optional).
6. Consider generating a warrant from COMP-0028/SYNCOMP-0016 before implementation (Missing Element 3, optional).

**Conditions for admission:**
- The plan author acknowledges that severity downgrades will affect error-count-based monitoring.
- The implementation must deterministically classify `CONTENT_STALE` per the added constraint.
- Registry audit coverage must be tested per the added success criteria.

**If these conditions are met:** The plan is admission-safe and should proceed to implementation under GAP-0004.
```
