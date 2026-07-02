# COMP-0010: Provider Comparison — AI-Lab Admission-Gated Context Next Step

## Metadata

- comparison_id: `COMP-0010`
- title: `AI-Lab Admission-Gated Context Next Step`
- context_policy: `latest_context`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0010-ai-lab-admission-gated-context-next-step.context.json`
- created_at: `2026-07-02T15:57:44.574642+00:00`
- command: `scripts/compare_providers.py Given the current AI-Lab memory/context implementation, choose the next safest implementation step. Options: (A) topic-aware routing inside scope, (B) manifest task_label/full_prompt_hash metadata, (C) admission-verdict ergonomics for older seeds, (D) topological context packing. Use the current scoped admission-gated context and justify ordering, tests, non-goals, and risks. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Admission-Gated Context Next Step`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

Given the current AI-Lab memory/context implementation, choose the next safest implementation step. Options: (A) topic-aware routing inside scope, (B) manifest task_label/full_prompt_hash metadata, (C) admission-verdict ergonomics for older seeds, (D) topological context packing. Use the current scoped admission-gated context and justify ordering, tests, non-goals, and risks.

## OpenAI Response

- model: `gpt-5`

```
Decision: (C) admission-verdict ergonomics for older seeds

Why this ordering
- Immediate risk reduction: The current L1 admission note explicitly flags that warning-admitted older artifacts can still influence models unless their warning metadata is clearly interpreted. Tightening ergonomics around admission decisions directly addresses this near-term safety risk without introducing new complexity.
- Minimal surface-area change: We build on the existing scoped, admission-gated context and manifest assembly described in the reconciled plan (ABS-0003). No new retrieval algorithms, schemas, or graph/topology are required.
- Defers known dependencies: Topological context packing (D) should not come first (per SYNCOMP-0005). Topic-aware routing inside scope (A) will be safer and easier once admission semantics are reliably surfaced and enforced. Manifest task_label/full_prompt_hash (B) is valuable for reproducibility, but it doesn’t mitigate the immediate risk of misusing older seeds; it can land right after C.

Proposed ordering
1) C admission-verdict ergonomics for older seeds
2) B manifest task_label and full_prompt_hash metadata (reproducibility and evaluation)
3) A topic-aware routing inside scope (uses safe, well-labeled inputs)
4) D topological context packing (gated on stable semantics and labels)

Scope for (C)
Goal: Make admission status first-class in selection and manifest ergonomics so warning-admitted items are safely downranked, capped, and transparently reported, while preserving usefulness when needed.

Implementation plan

1) Manifest ergonomics
- Add to each manifest item:
  - admission_decision: {admit, admit_with_warning, deny, unknown}
  - admission_verdict_id: stable id (e.g., CADM-…)
  - freshness_state: {fresh, stale, unknown}
  - warrant_state: {supported, unsupported, unknown}
  - included_with_warning: boolean derived from admission_decision != admit
  - inclusion_reason: keep existing values (explicit_ref, dependency, episode_l1, retrieved, system_rule), ensure present
- Telemetry fields at manifest level:
  - counts and token_budget_by_admission_decision
  - warn_budget_pct_applied and any demotion_reason flags

2) Selection policy updates (no retrieval changes)
- Hard filters:
  - require_admission=true excludes items with decision not in {admit, admit_with_warning}.
  - strict_mode=false (default): allow admit_with_warning; strict_mode=true excludes admit_with_warning unless item is explicit_ref.
- Soft penalties and caps:
  - Apply rank penalty to admit_with_warning (configurable, e.g., -0.3 score or one priority tier demotion).
  - Cap warn-admitted items to a warn_budget_pct (default 10% of context tokens) with a hard upper bound of N items (default 3).
  - Freshness modifiers: unknown freshness additional small penalty; stale larger penalty. Explicit refs bypass penalties but still count toward caps.
- Inclusion precedence:
  - explicit_ref > dependency > episode_l1 > retrieved, within each admission tier.
- Budgeting integration:
  - Enforce warn_budget_pct within the reconciled budgeting slices (ABS-0003). Do not steal from system/answer budgets; cap applies only to the context slice.

3) Prompt assembly behavior
- Do not inject warning text into the model-visible prompt. Keep admission metadata in the manifest only to avoid contaminating reasoning.
- Optional debug mode: add a non-user-visible header (comment/metadata) for offline audits.

4) CLI/API ergonomics
- New flags:
  - --require-admission (default true)
  - --allow-warning (default true unless --strict-mode)
  - --warn-budget-pct (default 10)
  - --warn-max-items (default 3)
  - --strict-mode (default false)
  - --admission-telemetry (emit per-request counters)
- Dry-run display clearly groups items by admission_decision with penalties/caps shown.

5) Validators and guards
- Admission validator: All selected items must have an admission_decision when --require-admission=true.
- Namespace/ACL guard: Maintain deny-by-default and prevent redacted/full mixing (per ABS-0003).
- Budget guard: Fail fast if warn items exceed configured caps due to mis-scoring.
- Idempotency: Manifests with identical candidate sets and configs yield identical admission annotations and ordering.

6) Observability
- Log distribution of decisions included/excluded, tokens by decision, and cases where caps eject warning-admitted candidates.
- Track answer quality/regression vs. warn_budget_pct changes.

Acceptance tests

Unit tests
- Manifest fields:
  - Items missing admission_decision are rejected when require_admission=true.
  - included_with_warning boolean is correct for admit_with_warning.
- Ranking and caps:
  - admit_with_warning receives score demotion; explicit_ref lifts above demotion.
  - warn_budget_pct and warn_max_items strictly enforced.
- Freshness penalties:
  - unknown and stale adjust scores as configured.
- Guards:
  - strict_mode excludes admit_with_warning unless explicit_ref.
  - Budget guard triggers when limits exceeded and proposes minimal ejection set.

Integration tests
- Mixed-corpus episode:
  - Candidates: fresh admit, unknown admit_with_warning, stale admit_with_warning, deny, unknown decision.
  - With defaults: deny/unknown excluded, warning-admitted downranked and capped; manifest telemetry correct.
  - With strict_mode: only fresh admit (plus any explicit_ref with warning) included.
- Explicit reference override:
  - User cites a warning-admitted seed; selection includes it despite strict_mode; still counted toward warning cap.
- Budget interplay:
  - Ensure warn_budget_pct does not consume system/answer slices; enforce within context slice only.
- ACL/redaction:
  - Verify no cross-namespace leakage and no mixing of redacted/full text in a single prompt.

Negative tests
- Forcing include of a deny item raises explicit error.
- Misreported admission_decision corrected or request fails with validator message.
- Exceeding warn caps without eligible fresh alternatives yields graceful degradation (include fewer items, not fail the whole request).

Non-goals for this increment
- No new retrieval algorithms or topic-aware routing (A).
- No changes to L0/L1 schemas beyond manifest annotations.
- No predicate vocabulary or edge graph; no topological packing (D).
- No UI dashboards beyond basic counters/logs.

Key risks and mitigations
- Context becomes too sparse if warnings are over-capped:
  - Mitigate with conservative defaults (10% cap, allow_warning=true), explicit_ref bypass, and clear telemetry to tune.
- Misinterpretation of admission semantics by downstream tools:
  - Keep semantics in manifest only; stable field names; add CI checks against schema drift.
- Operational complexity from new flags:
  - Reasonable defaults; inherit from environment config; emit config snapshot in telemetry for reproducibility.
- Silent regression in relevance due to penalties:
  - A/B evaluate warn_budget_pct and penalty values; monitor answer quality and citation integrity.

Follow-on step (next after C)
- (B) manifest task_label and full_prompt_hash metadata:
  - Add task_label to manifest and to EpisodeL1 provenance; add full_prompt_hash of the assembled system+user+tool prompt; persist in InteractionLog. This improves reproducibility, facilitates analysis of admission impacts, and prepares for future routing (A) and packing (D) without changing selection behavior.

This increment tightens safety around admitted-with-warning seeds, keeps context quality high, and preserves room to layer in reproducibility (B), routing (A), and topology (D) later with lower risk.
```

## Claude Response

- model: `claude-sonnet-4-5`

````
# Implementation Decision: Option B – Manifest task_label/full_prompt_hash Metadata

## Decision Rationale

**Choose (B) manifest task_label/full_prompt_hash metadata** as the next safest step.

### Why B Now

1. **Foundation for observability**: The current context shows we have:
   - Scoped admission-gated context working (L1-20260702 evidence)
   - Context packing with manifests (COMP-0009 context.json referenced)
   - But no way to track *what tasks* drive context selection or correlate manifest outcomes

2. **Low risk, high leverage**: 
   - Pure metadata addition to existing manifest structure
   - No changes to selection logic, ACL, or admission verdicts
   - Enables immediate wins: task-based metrics, prompt reproducibility, A/B testing

3. **Unblocks future capabilities safely**:
   - **(A) topic-aware routing** needs task labels to route effectively ("which tasks benefit from topic X?")
   - **(D) topological packing** needs reproducible manifest hashes to validate that topology changes don't break known-good contexts
   - **(C) admission ergonomics** will benefit from task-specific admission patterns ("older seeds work fine for summarization tasks")

### Why Not A, C, or D Yet

- **(A) topic-aware routing**: Requires task classification to be meaningful; without task_label we can't measure routing quality or avoid over-fitting topics to unknown workloads
- **(C) admission ergonomics**: Risks easing constraints before we can measure impact per task type; B gives us that measurement layer
- **(D) topological packing**: Per SYNCOMP-0005/ABS-0003, depends on stable provenance and clear selection semantics; adding topology before we can fingerprint and compare manifests risks invisible regressions

---

## Implementation Plan

### P0: Schema and Write Path

**Extend ContextPackManifest**:
```python
@dataclass
class ContextPackManifest:
    # Existing fields...
    manifest_id: str
    created_at: str
    token_budget: int
    assembly_policy: str
    inclusions: List[ManifestItem]
    
    # NEW fields
    task_label: Optional[str]        # e.g., "next-step-decision", "synthesis", "comparison"
    full_prompt_hash: str            # SHA-256 of complete assembled prompt text
    prompt_structure_hash: str       # Hash of template/structure (excludes variable content)
    
    # Provenance
    user_request_hash: Optional[str] # Hash of original user query
    parent_manifest_id: Optional[str] # For multi-turn tracking
```

**Metadata Capture Points**:
1. **At manifest creation** (in `scripts/compare_providers.py`, `scripts/synthesize_comparison.py`, etc.):
   - Derive `task_label` from command/context (e.g., `--title` → label, or explicit `--task-label` flag)
   - Compute `full_prompt_hash` after final assembly, before sending to model
   - Compute `prompt_structure_hash` from template with placeholders for variable content

2. **Storage**:
   - Write manifests to `docs/comparisons/*.context.json` and `docs/syntheses/*.context.json` (already done)
   - Add manifest index: `docs/manifests/index.json` mapping `(task_label, date) → manifest_id` for queries

### P1: Validators and Integrity

**Validators** (enforce at CI and runtime):
```python
def validate_manifest_metadata(manifest: ContextPackManifest) -> List[str]:
    errors = []
    
    # Hash integrity
    if not manifest.full_prompt_hash or len(manifest.full_prompt_hash) != 64:
        errors.append("full_prompt_hash must be 64-char SHA-256")
    
    # Task label format
    if manifest.task_label:
        if not re.match(r'^[a-z0-9-]+$', manifest.task_label):
            errors.append("task_label must be lowercase kebab-case")
    
    # Prompt structure vs full hash
    # Structure hash should be stable across similar tasks
    # (
````
