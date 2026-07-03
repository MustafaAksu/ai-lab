# COMP-0012: Provider Comparison — AI-Lab Provider Warning Cap Default Verification

## Metadata

- comparison_id: `COMP-0012`
- title: `AI-Lab Provider Warning Cap Default Verification`
- context_policy: `latest_context`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0012-ai-lab-provider-warning-cap-default-verification.context.json`
- created_at: `2026-07-03T06:52:32.533772+00:00`
- command: `scripts/compare_providers.py Verify the provider latest-context default warning cap. This run intentionally enables --require-admission but does not pass --max-warning-admissions. Confirm whether the saved context manifest records max_warning_admissions=1, whether explicit override precedence remains the intended behavior, and whether any follow-up implementation is needed. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Provider Warning Cap Default Verification`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Verify the provider latest-context default warning cap. This run intentionally enables --require-admission but does not pass --max-warning-admissions. Confirm whether the saved context manifest records max_warning_admissions=1, whether explicit override precedence remains the intended behavior, and whether any follow-up implementation is needed.

## OpenAI Response

- model: `gpt-5`

```
Here’s the verification against the provided source context:

- Saved manifest default: Yes. With --require-admission enabled and no --max-warning-admissions provided, the resolver defaults the cap to 1 for provider latest-context paths. The context pack’s Admission policy shows require_admission: True and max_warning_admissions: 1, and the admission summary (1 admit_with_warning) aligns with a cap of 1 being applied and recorded.

- Override precedence: Intended behavior remains unchanged. Explicit CLI values take precedence over the default, including the explicit zero override (--max-warning-admissions 0). This is called out in the key decisions and confirmed by tests.

- Follow-up implementation: None required. The resolver is wired into ask_provider.py and compare_providers.py, tests cover defaulting and the zero-cap override, and the manifests record the resolved policy for auditability. Optional niceties (docs/CLI help note) could be added, but no code changes are needed.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Verification Report: Provider Latest-Context Default Warning Cap

## Task Status: ✅ VERIFIED

Based on the context pack analysis, I can confirm the following:

---

## 1. Default Warning Cap Behavior

**Confirmed:** The saved context manifest **will record `max_warning_admissions=1`** when:
- `--require-admission` is enabled
- `--max-warning-admissions` is NOT explicitly passed
- The context is requested via provider latest-context paths

### Evidence
From **L1-20260702-provider-warning-cap-default**:
- `resolve_provider_warning_admission_cap` now returns:
  - **1** when `require_admission=True` and no explicit cap is provided
  - `None` when `require_admission=False` and no cap is provided
  - **Unchanged value** when explicitly set (including 0)

---

## 2. Explicit Override Precedence

**Confirmed:** Explicit override precedence **remains the intended behavior**.

### Key Decision Evidence
From completed work and key decisions:
> "Preserve explicit override precedence, including --max-warning-admissions 0."

This means:
- `--max-warning-admissions 0` will set the cap to 0 (not default to 1)
- Any explicitly passed value takes precedence over the default
- The default only applies when the parameter is omitted entirely

---

## 3. Current Admission Summary Analysis

Your current run shows the default is **working as designed**:

```
Admission policy:
- require_admission: True
- max_warning_admissions: 1  ← Default applied

Admission summary:
- admit: 1
- admit_with_warning: 1       ← Exactly 1, respecting the cap
- excluded_by_policy: 2        ← These were excluded
```

**L1-20260702-provider-warning-cap-default** was admitted cleanly (verdict: `CADM-dc22743bcc4f`, decision: `admit`).

**ABS-0003** was admitted with warning (verdict: `CADM-ea8838115838`, decision: `admit_with_warning`), filling the single warning slot.

Two items (SYNCOMP-0007, COMP-0011) were excluded because the warning cap was reached.

---

## 4. Follow-Up Implementation Needed

### Remaining Action Item
From **next_actions**:
> "Run one admission-gated provider comparison without explicitly passing --max-warning-admissions to verify the default appears in the saved context manifest."

**Status:** ✅ **THIS RUN COMPLETES THAT ACTION**

### Verification Checklist
- [x] Default applies when flag omitted ✅
- [x] `max_warning_admissions=1` in admission policy ✅
- [x] Exactly 1 item admitted with warning ✅
- [x] Explicit override precedence preserved (by design) ✅
- [x] Scoped to provider paths (build_context_pack.py unaffected) ✅

---

## 5. Risks & Auditability

### Acknowledged Risk
From the L1 document:
> "The default now changes provider admission-gated behavior when callers omit the warning cap; manifests make the resolved policy auditable."

**Mitigation:** This context pack manifest itself serves as the audit trail, clearly recording the resolved `max_warning_admissions=1` policy.

---

## Conclusion

✅ **No further implementation needed.** The provider latest-context default warning cap is functioning correctly:

1. Defaults to 1 when omitted with `require_admission=True`
2. Explicit overrides (including 0) are preserved
3. Manifest records the resolved policy for auditability
4. Test coverage includes resolver, provider defaulting, and zero-cap override
5. Full suite passed (191 tests)

The synthesis is complete and working as intended. This verification run confirms the next action from L1-20260702 has been satisfied.
````
