# COMP-0011: Provider Comparison — AI-Lab Warning Admission Cap Default Decision

## Metadata

- comparison_id: `COMP-0011`
- title: `AI-Lab Warning Admission Cap Default Decision`
- context_policy: `latest_context`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0011-ai-lab-warning-admission-cap-default-decision.context.json`
- created_at: `2026-07-03T06:29:37.399961+00:00`
- command: `scripts/compare_providers.py Given the current AI-Lab admission-gated latest-context implementation, should --max-warning-admissions 1 become the default for provider latest-context runs when --require-admission is enabled? Compare keeping it explicit versus making it default. Recommend the next implementation step, tests, non-goals, and risks. --latest-context --scope ai-lab-memory --require-admission --max-warning-admissions 1 --token-budget 8000 --model-target gpt-5 --title AI-Lab Warning Admission Cap Default Decision`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Given the current AI-Lab admission-gated latest-context implementation, should --max-warning-admissions 1 become the default for provider latest-context runs when --require-admission is enabled? Compare keeping it explicit versus making it default. Recommend the next implementation step, tests, non-goals, and risks.

## OpenAI Response

- model: `gpt-5`

```
Short answer
Yes—make max-warning-admissions=1 the default for provider latest-context runs when require-admission is enabled, but roll it out as a guarded default (feature-flagged, with clear precedence for explicit CLI values) and validate with a provider comparison before flipping it on by default.

Why this default is reasonable now
- The manifest already records both the admission policy and the admission summary, so the effective policy is auditable per run.
- Current risk noted: policy is recorded but not used to choose defaults; callers must pick caps. A safe, consistent default reduces footguns while preserving one soft warning.
- The example admission summary (admit_with_warning: 1, excluded_by_policy: 2) shows warning allowances are exercised in practice; allowing exactly one warning balances safety with pragmatism.

Comparison: keep it explicit vs make it default

Keep it explicit (status quo)
- Pros
  - No behavioral surprises; existing jobs are stable.
  - Teams can tune per provider/task without central coupling.
- Cons
  - Easy to forget; uneven safety posture across runs.
  - Reduces comparability across provider runs; manifests vary due to caller choices.
  - Friction for recommended practice (the next action already proposes evaluating “1”).

Make it the default when require-admission is True
- Pros
  - Establishes a consistent safety baseline across providers.
  - Reduces configuration burden; manifests will show a clear, predictable policy.
  - One-warning leniency avoids over-blocking on minor issues.
- Cons/Risks
  - Behavior change may block or trim content in pipelines that relied on more lenient settings.
  - Some providers/tasks might need >1 warning allowance; requires opt-out.
  - If warning detectors are noisy, default could cause flaky exclusions.

Recommendation
Adopt max-warning-admissions=1 as the computed default when:
- Command is a provider latest-context run, and
- require-admission is True, and
- max-warning-admissions is not explicitly set.

Guardrails
- Explicit CLI or config values always take precedence.
- Ship behind a feature flag for one cycle; run the planned provider comparison; then enable by default.
- Emit an info log line and record the computed default in the manifest admission_policy for transparency.

Next implementation step
- Implement default resolution:
  - If require_admission and value is unset, set max_warning_admissions=1.
  - Surface the resolved policy in the manifest admission_policy (already supported) and renderer.
- Add a feature flag and overrides:
  - Env var AL_ADMISSION_DEFAULT_WARNINGS (or config) to globally set/disable the default.
  - Per-provider override in config for edge cases.
- Telemetry:
  - Counters for warnings encountered, warnings admitted, and runs blocked due to cap.
  - Tag with provider/model and policy to compare outcomes.
- Execute the admission-gated provider comparison (the documented next action) with the feature flag on:
  - Compare runs at cap=1 vs current settings across representative providers/tasks.
  - Track exclusion rates, quality impact, and run failures.

Tests
- Unit
  - Default resolution: with require_admission=True and unset cap → resolves to 1.
  - Precedence: explicit CLI cap overrides computed default.
  - No defaulting when require_admission=False.
  - Feature flag off → no computed default applied.
  - Manifest content: admission_policy shows the resolved values; admission_summary unaffected by recording change.
- Integration
  - E2E latest-context build where items trigger warnings:
    - Cap unset + require_admission=True → exactly one warning-admitted, extras excluded by policy.
    - Cap=0 excludes any warning-admitted items.
    - Cap>1 allows multiple.
  - Provider-specific run path respects defaulting logic and records it in rendered context.
- CLI/UX
  - Help text documents the conditional default and precedence.
  - Log line confirms the effective policy when defaulting occurs.
- Regression
  - Backward compatibility when admission_policy is absent in older manifests (optional field remains optional).
  - Ensure excluded_by_policy counts remain correct under the new default.

Non-goals
- Changing the definition or severity of “warning” admissions.
- Altering admission criteria or detectors.
- Applying this default to non-provider or non-latest-context commands.
- Retrofitting older manifests or rewriting past summaries.

Risks and mitigations
- Silent behavior change breaks pipelines
  - Mitigate with feature-flagged rollout, clear logs, explicit override path, and release notes.
- Provider/task variance needs >1 warning
  - Allow per-provider overrides; document tuning guidance.
- Detector noise causes flaky exclusions
  - Use the comparison run to assess noise; consider provider-specific thresholds if needed.
- Configuration drift between CLI and programmatic calls
  - Centralize default resolution in one shared helper, covered by tests; always record resolved policy in manifest.

Decision checkpoint
- Ship the feature-flagged default, run the provider comparison, and, if exclusion/quality metrics are acceptable, flip the default on by default in the next release while preserving easy opt-out.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Analysis: Default --max-warning-admissions for Admission-Gated Latest-Context

## Current State

Based on L1-20260702-admission-policy-manifest, the implementation has:
- ✅ Admission policy recording in manifests (`require_admission`, `max_warning_admissions`)
- ✅ Schema validation and serialization
- ✅ Rendering in context-pack Markdown
- ✅ Full test coverage (186 tests passed)
- ⚠️ **Open question**: Should `--max-warning-admissions 1` become the default?

This pack itself demonstrates the policy in action:
- 2 items excluded by policy (SYNCOMP-0006, COMP-0010)
- 1 admitted with warning (ABS-0003)
- 1 admitted cleanly (L1-20260702)

## Comparison: Explicit vs. Default

### Option A: Keep Explicit (Current)
**Pros:**
- Maximum transparency—users must consciously choose to allow warnings
- Fail-safe default (zero warnings = stricter quality gate)
- Clear signal when context quality degrades
- Forces deliberate policy decisions per command

**Cons:**
- Repetitive flag usage for provider comparisons
- Friction in iterative workflows where warnings are acceptable
- May discourage exploration of borderline-relevant context
- Current manifest shows `max_warning_admissions: 1` was already chosen explicitly—suggesting it's a common need

### Option B: Default to 1 When --require-admission Enabled
**Pros:**
- Matches demonstrated usage pattern (this pack uses it)
- Balances quality (rejects unknowns/unsupported) with pragmatism (allows borderline-fresh)
- Reduces boilerplate in provider comparison workflows
- Still auditable via manifest recording
- Can be overridden to 0 for strict gates or higher for permissive runs

**Cons:**
- Hides a quality trade-off behind implicit behavior
- Warning items (like ABS-0003: freshness unknown) auto-admitted without explicit acknowledgment
- May mask context degradation if users don't inspect manifests

## Recommendation: **Make it Default with Clear Escape Hatches**

### Rationale
1. **Empirical evidence**: The L1 next-action explicitly requests testing with `--max-warning-admissions 1`, and this context pack itself uses that value—indicating it's the **intended baseline** for admission-gated workflows.

2. **Workflow fit**: Provider comparisons (the primary use case per L1) benefit from including "admit_with_warning" items like borderline-fresh abstractions or unsupported warrants, which often provide valuable historical context even if not perfectly fresh.

3. **Auditability preserved**: Manifests already record both `admission_policy` and `admission_summary`, so the trade-off remains visible.

4. **Failure modes**: Defaulting to 0 (reject all warnings) creates false negatives; defaulting to unlimited creates unbounded quality drift. **1 is a reasonable Schelling point**: allow one borderline item while still signaling degradation.

---

## Implementation Plan

### Next Step
**Implement default policy logic in provider latest-context commands:**

```python
# In scripts/provider_comparison.py or equivalent
def build_latest_context_args(require_admission: bool, max_warning_admissions: Optional[int]) -> dict:
    """
    Construct context-pack arguments with admission-gating defaults.
    
    When require_admission is True:
    - Default max_warning_admissions to 1 if not explicitly set
    - Allow override to 0 (strict) or higher (permissive)
    """
    if require_admission and max_warning_admissions is None:
        max_warning_admissions = 1  # Default Schelling point
    
    return {
        "require_admission": require_admission,
        "max_warning_admissions": max_warning_admissions if require_admission else None,
    }
```

**CLI change:**
```bash
# Old (explicit required)
scripts/provider_comparison.py --assembly latest-context --require-admission --max-warning-admissions 1

# New (default applied)
scripts/provider_comparison.py --assembly latest-context --require-admission

# Override to strict
scripts/provider_comparison.py
````
