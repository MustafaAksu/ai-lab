# COMP-0028: Provider Comparison — audit-verification-outcome-vocabulary

## Metadata

- comparison_id: `COMP-0028`
- title: `audit-verification-outcome-vocabulary`
- context_policy: `latest_context`
- context_require_admission: `false`
- context_max_warning_admissions: `null`
- context_max_warning_admissions_source: `unset`
- context_manifest: `docs/comparisons/COMP-0028-audit-verification-outcome-vocabulary.context.json`
- created_at: `2026-07-19T14:58:30.728826+00:00`
- command: `scripts/compare_providers.py AI-Lab's self-model index audit (audit_self_model_index) currently reports
error-severity findings when git evidence cannot be resolved, for example when
.git is absent, history is shallow, or a stored repo_head commit is missing
from the local history. This makes an environment where verification is
IMPOSSIBLE indistinguishable from a repository where verification SUCCEEDED
and found genuine drift or staleness. A concrete observed case: a zip export
of the repository without .git produced SELF_MODEL_INDEX_REPO_HEAD_MISSING and
SELF_MODEL_INDEX_CONTENT_STALE errors and 4 test failures, although record
content was identical to a normalized rebuild except for repo_head and
generated_at.

Evaluate whether AI-Lab should introduce an explicit three-valued verification
outcome vocabulary in the self-model index and registry audits:

- verified_current: evidence available, no drift
- stale: evidence available, drift confirmed
- unverifiable: required evidence unavailable (no git, shallow history,
  unreachable commit), no claim about drift is made

Specifically assess:

1. Whether conflating unverifiable with stale is a genuine epistemic defect in
   the audit ontology, or acceptable conservative behavior (fail-closed).
2. Whether unverifiable findings should carry a distinct severity (e.g. warn)
   rather than error, and whether the audit's top-level "ok" field should
   remain false, become true, or be replaced by a three-valued status when
   only unverifiable findings exist.
3. Whether the same vocabulary should be adopted now by the admitted compact
   artifact sidecar contract (PLAN-20260717-0001), whose staleness semantics
   are about to be implemented, so both subsystems share one verification
   vocabulary instead of retrofitting later.
4. Whether this is a small governed slice under an existing gap or requires a
   new GAP record.
5. What the safest first slice is, preserving the current audit JSON schema
   where possible (additive fields preferred over changed meanings).

Constraints: do not implement anything; do not assume any new GAP or PLAN is
admitted; canonical records and existing audit finding codes must remain
readable by current tooling. --latest-context --out-dir docs/comparisons --title audit-verification-outcome-vocabulary`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab's self-model index audit (audit_self_model_index) currently reports
error-severity findings when git evidence cannot be resolved, for example when
.git is absent, history is shallow, or a stored repo_head commit is missing
from the local history. This makes an environment where verification is
IMPOSSIBLE indistinguishable from a repository where verification SUCCEEDED
and found genuine drift or staleness. A concrete observed case: a zip export
of the repository without .git produced SELF_MODEL_INDEX_REPO_HEAD_MISSING and
SELF_MODEL_INDEX_CONTENT_STALE errors and 4 test failures, although record
content was identical to a normalized rebuild except for repo_head and
generated_at.

Evaluate whether AI-Lab should introduce an explicit three-valued verification
outcome vocabulary in the self-model index and registry audits:

- verified_current: evidence available, no drift
- stale: evidence available, drift confirmed
- unverifiable: required evidence unavailable (no git, shallow history,
  unreachable commit), no claim about drift is made

Specifically assess:

1. Whether conflating unverifiable with stale is a genuine epistemic defect in
   the audit ontology, or acceptable conservative behavior (fail-closed).
2. Whether unverifiable findings should carry a distinct severity (e.g. warn)
   rather than error, and whether the audit's top-level "ok" field should
   remain false, become true, or be replaced by a three-valued status when
   only unverifiable findings exist.
3. Whether the same vocabulary should be adopted now by the admitted compact
   artifact sidecar contract (PLAN-20260717-0001), whose staleness semantics
   are about to be implemented, so both subsystems share one verification
   vocabulary instead of retrofitting later.
4. Whether this is a small governed slice under an existing gap or requires a
   new GAP record.
5. What the safest first slice is, preserving the current audit JSON schema
   where possible (additive fields preferred over changed meanings).

Constraints: do not implement anything; do not assume any new GAP or PLAN is
admitted; canonical records and existing audit finding codes must remain
readable by current tooling.

## OpenAI Response

- model: `gpt-5`

```
Short answer
- Yes, add a three‑valued verification outcome: verified_current | stale | unverifiable.
- Treat “unverifiable” as a distinct epistemic state. Keep fail‑closed at the top level for backward compatibility, but make the distinction explicit.
- Adopt the same vocabulary now for the compact artifact sidecar to avoid later retrofit.
- This can ship as a small governed slice (diagnostic-only), no new GAP required.
- Prefer additive fields; do not change finding codes or their meanings.

Details

1) Ontology: conflating unverifiable with stale
- Assessment: It is an epistemic defect. “Unverifiable” = lack of evidence; “stale” = positive evidence of drift. Collapsing these obscures what the audit actually knows.
- Conservatism: You can still fail-closed operationally (e.g., keep ok=false), while recording “unverifiable” distinctly so consumers and tests don’t infer drift where none is proven.

2) Severity and top-level ok when only “unverifiable” exists
- Findings severity:
  - Recommendation: classify these findings as evidence_unavailable and default their severity to warn (not error). They are not proof of defect, only missing evidence.
- Top-level ok:
  - Backward-compatibility: keep ok and keep its current meaning.
  - Policy: when only unverifiable exists, ok should remain false (conservative, unchanged behavior) but a new explicit outcome should carry the semantic truth.
- Additive status:
  - Add a top-level verification_outcome enum with values:
    - verified_current: evidence available, no drift
    - stale: evidence available, drift confirmed
    - unverifiable: required evidence unavailable; no claim about drift
  - Optional additive detail: evidence_status (e.g., none, shallow_history, unreachable_commit) to explain why it’s unverifiable.

This preserves existing tooling (still sees ok=false) while allowing upgraded tooling/tests to distinguish unverifiable from stale. If teams later want pipelines to pass on “unverifiable,” they can pivot to the new field without reinterpreting ok.

3) Consistency with compact artifact sidecar (PLAN-20260717-0001)
- Recommendation: adopt the same tri‑valued vocabulary now in the sidecar staleness semantics. One shared verification vocabulary reduces future migration risk and keeps diagnostics coherent across subsystems.

4) Governance routing
- Scope: diagnostic-only, no selection or prompt/path changes, no persistence or provider behavior changes, purely audit semantics.
- Recommendation: treat this as a small governed slice under existing audit/verification governance (no new GAP). If an umbrella GAP for verification/staleness already exists (e.g., the open governance thread that keeps “not_ready” explicit), anchor the PLAN to it; otherwise proceed as a maintenance/evidence slice within the audit subsystem.

5) Safest first slice (additive, schema-stable)
Do not remove or rename anything; do not change meanings of existing fields or finding codes.

- Additive top-level fields
  - verification_outcome: enum ["verified_current", "stale", "unverifiable"].
  - evidence_status (optional): enum ["ok", "no_git_dir", "shallow_history", "unreachable_repo_head", "other"].
  - counters (optional): { verified_current: n, stale: n, unverifiable: n } for quick summaries.

- Additive per-finding fields
  - class: enum ["drift", "evidence_unavailable", "other"].
  - evidence_cause (optional): mirrors evidence_status where applicable.

- Severity policy
  - Set severity for class="evidence_unavailable" to warn by default.
  - Keep ok computation unchanged (ok=false unless fully verified_current).
  - This combination preserves fail-closed behavior (pipelines keying on ok remain conservative) while eliminating the stale/unverifiable ambiguity for upgraded consumers.

- Backward compatibility guardrails
  - Keep all existing finding codes (e.g., SELF_MODEL_INDEX_REPO_HEAD_MISSING, SELF_MODEL_INDEX_CONTENT_STALE) and messages as-is.
  - Do not repurpose codes; rely on the new class and verification_outcome to express the distinction.
  - Tests that currently assert “no errors” can continue to use ok, while new tests can assert verification_outcome == "unverifiable" for zip-without-.git scenarios.

- Example mapping of the observed case (zip export without .git)
  - verification_outcome: "unverifiable"
  - evidence_status: "no_git_dir"
  - findings:
    - SELF_MODEL_INDEX_REPO_HEAD_MISSING: class="evidence_unavailable", severity="warn"
    - Any drift-only findings should not be emitted unless content comparison demonstrates drift; if emitted solely due to missing git, they should be reclassified to evidence_unavailable.
  - ok: false (unchanged)

Summary of decisions
- 1) Conflation is an epistemic defect; differentiate “unverifiable.”
- 2) Use warn severity for unverifiable findings; keep ok=false when only unverifiable exists; add a tri‑valued verification_outcome for clarity.
- 3) Adopt the same vocabulary now in the compact sidecar contract.
- 4) Ship as a small governed slice under existing governance; no new GAP required.
- 5) First slice is additive-only: new outcome and classification fields; unchanged finding codes; unchanged ok semantics.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Evaluation: Three-Valued Verification Outcome Vocabulary for AI-Lab Self-Model Audits

## 1. Epistemic Defect vs. Conservative Fail-Closed

**This is a genuine epistemic defect, not acceptable conservative behavior.**

**Analysis:**

The current conflation creates **three distinct harms**:

1. **False signal**: A zip-exported repository (common in CI artifacts, deployment packages, hermetic builds) reports the same error severity as a repository with confirmed content drift. Operators cannot distinguish "we don't know" from "we know it's wrong."

2. **Unusable error budgets**: Error-severity findings that may represent zero actual problems pollute monitoring, break test gates in legitimate environments, and force operators to either ignore all self-model errors (unsafe) or maintain complex environment-specific suppression rules (brittle).

3. **Violated audit semantics**: An audit that reports `"ok": false` and error-severity findings when **no verification was attempted** has failed at its definitional purpose. The audit did not verify staleness; it verified git availability. These are orthogonal properties.

**Conservative fail-closed would be appropriate if:**
- Unavailable evidence *could* hide drift, AND
- The operator can reasonably provide evidence, AND  
- Failing closed creates back-pressure toward providing evidence.

**None of these hold here:**
- A `.git`-less zip export *cannot* hide drift in the exported snapshot—the content is what it is.
- Many deployment/hermetic-build scenarios *cannot* provide git history (by design).
- Failing closed creates back-pressure to suppress or ignore the audit, not to improve evidence.

**Correct conservative behavior**: Report `unverifiable`, explain why evidence is missing, allow the operator to decide whether that matters in their environment. A CI pipeline verifying against a known-good snapshot may tolerate `unverifiable`; a production registry sync must not.

---

## 2. Severity, Top-Level Status, and Three-Valued Outcomes

### Recommended severity for unverifiable findings:

**`warn` (or a new `info`-level class), not `error`.**

**Rationale:**
- `error` implies "this is wrong and must be fixed." `unverifiable` means "we cannot tell; context determines whether this matters."
- `warn` signals "operator attention recommended" without forcing remediation in environments where git history is intentionally absent.
- Allows error-budget policies to remain strict (zero errors) while tolerating expected unverifiable states.

### Top-level `"ok"` field semantics:

**Replace boolean `"ok"` with three-valued `"status"`** (or keep `"ok"` and add `"status"` additively):

```json
{
  "ok": true,          // DEPRECATED: backward compat; true iff status == "verified_current"
  "status": "unverifiable",  // enum: ["verified_current", "stale", "unverifiable"]
  "findings": [ ... ]
}
```

**Three-valued status semantics:**

| Status | Meaning | `ok` (compat) | Error findings? | Warn findings? |
|--------|---------|---------------|-----------------|----------------|
| `verified_current` | Evidence available, no drift | `true` | No | No |
| `stale` | Evidence available, drift confirmed | `false` | Yes | Maybe |
| `unverifiable` | Required evidence unavailable | `false` (conservative) or `null` | No | Yes (unverifiable findings) |

**Recommendation for `unverifiable`:**
- Set `"ok": null` (or omit) to force callers to check `status` explicitly, OR
- Set `"ok": false` conservatively but document that `status == "unverifiable"` with zero error findings is not a remediation-required state.

**Safest transition path:**
- Add `"status"` field; keep `"ok"` as `not (status == "verified_current")` for backward compatibility.
- Emit deprecation notice if `"ok"` is read and `"status"` is available.
- Future slice can remove `"ok"` once consumers migrate.

---

## 3. Shared Vocabulary with Compact Artifact Sidecar (PLAN-20260717-0001)

**Yes—adopt the same three-valued vocabulary now.**

**Rationale:**

1. **Prevent divergence**: PLAN-20260717-0001's staleness semantics are about to be implemented. If the sidecar contract uses a different verification vocabulary (e.g., boolean `is_stale` or two-valued `fresh`/`stale`), AI-Lab will have two incompatible verification models—one for self-model index/registry audits, one for compact artifact sidecars.

2. **Shared epistemic stance**: Compact artifact sidecars face identical unverifiable scenarios:
   - Sidecar present, canonical artifact missing → unverifiable (cannot confirm drift).
   - Sidecar content_hash mismatches canonical, but canonical is itself unverifiable → cannot determine sidecar staleness.
   - Git evidence for sidecar `generated_at` / `repo_head` missing → unverifiable provenance.

3. **Unified audit surface**: If both subsystems report `verified_current` / `stale` / `unverifiable`, operators can apply uniform policies (e.g., "deployment gates require `verified_current`; CI allows `unverifiable` for zip exports").

4. **Implementation efficiency**: PLAN-20260717-0001 has not yet shipped sidecar staleness checking. Introducing the three-valued vocabulary now avoids a later retrofit of sidecar validation, sidecar schema, and all consumers.

**Concrete integration:**

Compact artifact sidecar schema should include:

```json
{
  "verification_status": "verified_current",  // enum: same as audit status
  "verification_findings": [
    // same finding structure as audit findings, scoped to this sidecar
  ]
}
```

Self-model index records should include the same `verification_status` field (per-record) and audits should roll up per-record statuses into the top-level audit status.

---

## 4. GAP Record: New or Existing?

**Small governed slice under existing GAP-0003 (canonical records and lineage), NOT a new GAP.**

**Rationale:**

- **Scope alignment**: GAP-0003 covers "Canonical record and lineage management," including self-model index, registry, and compact artifact sidecars. Verification outcome vocabulary is a refinement of how staleness/drift is represented in these records—it does not introduce new capabilities or cross-cut unrelated domains.

- **Bounded change**: This slice affects:
  - Self-model index audit output schema (additive `status` field, finding severity changes).
  - Registry audit output schema (same).
  - Compact artifact sidecar schema (additive `verification_status` field, per PLAN-20260717-0001 scope).
  - Audit implementation (`unverifiable` classification logic; no new evidence sources or verification algorithms).

- **No new integration surface**: Does not touch context selection, retrieval, provider paths, CLI exposure beyond existing audit commands, or cross-domain coordination.

- **Precedent**: L1-20260707 and COMP-0027 show that evidence-gathering and representation-refinement slices (e.g., L0 discovery advisor thresholds, graph-local diagnostics) proceed under existing GAPs when they clarify or instrument existing scope rather than expand it.

**GAP-0003 amendment:**
- Add a sub-goal or milestone: "Verification outcome vocabulary and unverifiable-state diagnostics for self-model audits and sidecar staleness."
- No new GAP record required.

---

## 5. Safest First Slice (Schema-Preserving, Additive)

### Slice goal:
Introduce three-valued verification vocabulary to self-model index and registry audits, preserving backward compatibility with existing JSON schema and tooling.

### Deliverables:

1. **Schema changes (additive only):**

   **Before (current audit output):**
   ```json
   {
     "ok": false,
     "findings": [
       {
         "code": "SELF_MODEL_INDEX_REPO_HEAD_MISSING",
         "severity": "error",
         "message": "...",
         "record_id": "..."
       }
     ]
   }
   ```

   **After (additive fields):**
   ```json
   {
     "ok": false,  // DEPRECATED; computed as (status == "verified_current")
     "status": "unverifiable",  // NEW: enum ["verified_current", "stale", "unverifiable"]
     "findings": [
       {
         "code": "SELF_MODEL_INDEX_REPO_HEAD_MISSING",
         "severity": "warn",  // CHANGED: error → warn for unverifiable findings
         "verification_outcome": "unverifiable",  // NEW: per-finding outcome
         "message": "...",
         "record_id": "..."
       }
     ]
   }
   ```

   **Per-record changes (self-model index JSON):**
   ```json
   {
     "record_id": "...",
     "repo_head": "abc123",
     "verification_status": "unverifiable",  // NEW: per-record status
     // existing fields unchanged
   }
   ```

2. **Finding code classification:**

   Create a **deterministic mapping** from existing finding codes to verification outcomes:

   | Finding Code | Old Severity | New Severity | Verification Outcome |
   |--------------|--------------|--------------|----------------------|
   | `SELF_MODEL_INDEX_REPO_HEAD_MISSING` | error | **warn** | `unverifiable` |
   | `SELF_MODEL_INDEX_SHALLOW_HISTORY` | error | **warn** | `unverifiable` |
   | `SELF_MODEL_INDEX_CONTENT_STALE` (git unavailable) | error | **warn** | `unverifiable` |
   | `SELF_MODEL_INDEX_CONTENT_STALE` (git available, hash mismatch) | error | error | `stale` |
   | `SELF_MODEL_INDEX_CONTENT_HASH_MISMATCH` | error | error | `stale` |
   | (no findings, verification succeeded) | — | — | `verified_current` |

   **Implementation note**: Distinguish `CONTENT_STALE` with git evidence from `CONTENT_STALE` without git evidence (e.g., split into two codes: `CONTENT_STALE_VERIFIED` and `CONTENT_STALE_UNVERIFIABLE`, or use a `verification_outcome` field).

3. **Audit top-level status rollup:**

   ```python
   if any(f.verification_outcome == "stale" for f in findings):
       status = "stale"
   elif any(f.verification_outcome == "unverifiable" for f in findings):
       status = "unverifiable"
   else:
       status = "verified_current"
   
   ok = (status == "verified_current")  # backward compat
   ```

4. **Compact artifact sidecar schema (PLAN-20260717-0001 integration):**

   Add to sidecar schema:
   ```json
   {
     "verification_status": "verified_current",  // same enum
     "verification_message": "Content hash matches canonical L1-... record."
   }
   ```

   Sidecar validation emits findings with same structure as audit findings.

5. **Documentation and migration guide:**

   - Explain `status` vs. `ok` semantics.
   - Provide operator guidance: when to tolerate `unverifiable`, when to require `verified_current`.
   - CLI flag to suppress unverifiable findings for environments where git history is intentionally absent (e.g., `--allow-unverifiable`).

### Guardrails (mandatory non-goals for this slice):

- **No schema breakage**: Existing `"ok"` field remains; existing finding codes remain valid (severity changes only for unverifiable cases).
- **No new verification algorithms**: Classification logic only; no new git queries, no new hash computations.
- **No automatic remediation**: Slice adds diagnostics; does not auto-rebuild, auto-fetch git history, or suppress findings.
- **No selection_effect changes**: Audit output changes only; no impact on context selection, manifests, or provider paths.

### Success criteria:

- Zip-exported repository reports `status: "unverifiable"`, `ok: false`, zero error findings, 1+ warn findings, zero test failures.
- Git-backed repository with no drift reports `status: "verified_current"`, `ok: true`, zero findings.
- Git-backed repository with drift reports `status: "stale"`, `ok: false`, 1+ error findings.
- Compact artifact sidecar validation uses same `verification_status` enum.
- Existing tooling (scripts that check `"ok"`) continues to work; new tooling can check `"status"` for finer granularity.

---

## Summary Recommendations

1. **Epistemic defect**: Yes—conflating unverifiable with stale is a category error. The audit claims to verify staleness but actually verifies git availability.

2. **Severity and status**:
   - Unverifiable findings: `warn` (or `info`), not `error`.
   - Add three-valued `"status"` field: `verified_current` / `stale` / `unverifiable`.
   - Keep `"ok"` as `status == "verified_current"` for backward compatibility; deprecate over time.

3. **Shared vocabulary**: Yes—adopt the same three-valued vocabulary in compact artifact sidecars (PLAN-20260717-0001) now to prevent divergence.

4. **GAP record**: Small governed slice under **GAP-0003** (canonical records and lineage); no new GAP required.

5. **Safest first slice**:
   - Additive schema changes only (`status`, `verification_outcome`, per-record `verification_status`).
   - Reclassify unverifiable findings as `warn`; preserve existing finding codes.
   - Deterministic status rollup; backward-compatible `"ok"` field.
   - Integrate with PLAN-20260717-0001 sidecar schema before sidecar staleness ships.
   - No new verification algorithms, no schema breakage, no automatic remediation.

**Next step**: Draft a small PLAN under GAP-0003 with the above schema changes, finding classification table, and sidecar integration points. Reserve implementation for a subsequent slice pending admission.
````
