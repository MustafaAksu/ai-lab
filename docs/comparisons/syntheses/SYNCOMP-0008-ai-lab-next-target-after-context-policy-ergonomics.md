# SYNCOMP-0008: Comparison Synthesis — AI-Lab Next Target After Context Policy Ergonomics

## Metadata

- synthesis_id: `SYNCOMP-0008`
- title: `AI-Lab Next Target After Context Policy Ergonomics`
- created_at: `2026-07-03T08:26:49.619663+00:00`
- command: `scripts/synthesize_comparison.py docs/comparisons/COMP-0013-ai-lab-next-target-after-context-policy-ergonomics.md --title AI-Lab Next Target After Context Policy Ergonomics`
- source_comparison: `docs/comparisons/COMP-0013-ai-lab-next-target-after-context-policy-ergonomics.md`
- synthesizer_provider: `OpenAI`
- synthesizer_model: `gpt-5`

## Synthesis

~~~text
1) Shared agreement
- Aim: Deliver the next smallest, testable vertical slice that improves the memory/context workflow and fits a single small commit plus a memory refresh.
- Dry-run and ergonomics first: Both emphasize enhancements that are safe, inspectable, and improve visibility/audit without risking runtime behavior.
- Schema/manifest awareness: Both reference or build toward the reconciled ABS-0003 shape (budgeting defaults, manifest sections, L0/L1 artifacts).
- Testability: Each proposal includes clear unit/integration test hooks and small CLI/help updates.

2) Meaningful differences
- OpenAI focuses on dry-run introspection and output format:
  - Candidate A: Context budget preview in --print-context-summary (percentages and optional absolute tokens).
  - Candidate B: JSON mode for --print-context-summary.
  - Candidate C: Minimal manifest scaffold echo.
  - Explicit recommendation: implement Candidate A now.
- Claude focuses on artifact creation/consumption and validation:
  - Candidate 1: Manual L0 chunk creation helper script and schema.
  - Candidate 2: Read-only inclusion of L0 chunks into the context pack summary/manifest.
  - Candidate 3: Citation validation utility for cid@version|span format.
  - No explicit single recommendation stated in the provided text.

3) Stronger points from OpenAI
- Immediate, low-risk utility: Improves budgeting awareness where users already operate (dry-run summaries), with zero runtime impact.
- Precision and determinism: Concrete percentages (System 15%, Answer 10%, Context 75%; Context split: Explicit 40%, Dependencies 45%, L1 10%, L0 5%) and a deterministic rounding plan (floor, remainder to last leaf).
- Small, testable footprint: One helper, light CLI wiring, 4–6 tests, help updates; clearly gated behind existing flags.

4) Stronger points from Claude
- Moves the system toward end-state capabilities:
  - Establishes L0 artifacts and schema (creation helper).
  - Surfaces L0 in summaries/manifests to prepare for retrieval/ranking.
  - Adds CI-friendly quality guardrails (citation validator).
- Improves auditability and data hygiene, not just presentation.

5) Combined answer
- Recommendation: Implement OpenAI Candidate A now — Dry-run “Context Budget Preview” in --print-context-summary.
  - Why: Fastest path to a tangible improvement in the memory/context workflow, entirely in dry-run space, tightly scoped, and directly connects policy budgeting to day-to-day usage.
  - Scope:
    - Add optional --context-window INT to compute absolute token counts; otherwise show percentages.
    - Compute nested budgets using defaults from ABS-0003 with deterministic rounding (floor; remainder to last leaf per group).
    - Render in the existing --print-context-summary preamble alongside latest_context policy and max_warning_admissions info.
    - Update help text; add unit tests for percentage-only and absolute modes; retain gating behavior.
  - Example outcome (from OpenAI): With --context-window 8000,
    - System: 15% → 1200; Answer: 10% → 800; Context: 75% → 6000
      - Explicit: 40% → 2400; Dependencies: 45% → 2700; L1: 10% → 600; L0: 5% → 300
  - Memory refresh: Add an L1 note recording the new budget preview feature and defaults.

- Near-term follow-ups (sequenced, optional):
  - OpenAI Candidate B (JSON output for summaries) to enable CI/tooling.
  - Claude Candidate 3 (Citation validation) to strengthen documentation and artifact quality.
  - Claude Candidate 1 or 2 (L0 helper and/or read-only inclusion) once budgets and summary outputs are stabilized.

6) Risks or missing assumptions
- Budget defaults stability: Relies on ABS-0003 percentages remaining stable; changes would require updates and could churn tests/docs.
- Gating assumptions: Assumes existing gating for --print-context-summary with --latest-context and --print-prompt is intact.
- Output coupling: Downstream scripts that scrape text summaries could be sensitive to new preamble lines; they should avoid parsing the human-readable summary or wait for JSON mode.
- Manifest evolution: OpenAI’s Candidate C and Claude’s L0 inclusion both risk premature schema lock-in if ABS-0003 evolves.
- Scope clarity: Claude mentions “206 passing tests” and existing files/scripts not shown here; the synthesis treats these as provider-stated context but does not verify them.

7) Suggested re-ask prompt
Propose and implement a minimal dry-run Context Budget Preview for ai-lab-memory:
- Use the admitted ai-lab-memory context and the latest-context policy.
- In --print-context-summary, show per-section percentages using ABS-0003 defaults and, if --context-window INT is provided, compute absolute token counts with deterministic rounding (floor; remainder to the last leaf).
- Keep behavior gated behind existing --latest-context and --print-prompt requirements.
- Provide a concise implementation plan, exact CLI flag semantics, sample output for --context-window 8000, and 4–6 deterministic tests.
- Include help text updates and a brief memory refresh entry describing the new preview and default percentages.
- Do not change runtime request/packing behavior; this is dry-run only.
~~~

## Source Comparison

~~~markdown
# COMP-0013: Provider Comparison — AI-Lab Next Target After Context Policy Ergonomics

## Metadata

- comparison_id: `COMP-0013`
- title: `AI-Lab Next Target After Context Policy Ergonomics`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- token_budget: `8000`
- model_target: `gpt-5`
- context_manifest: `docs/comparisons/COMP-0013-ai-lab-next-target-after-context-policy-ergonomics.context.json`
- created_at: `2026-07-03T08:19:21.276621+00:00`
- command: `scripts/compare_providers.py AI-Lab has closed the provider latest-context warning-cap and context-policy ergonomics chain through CLI help, policy audit output, comparison metadata, metadata centralization, and dry-run context summaries. Using the admitted ai-lab-memory context, recommend the next smallest implementation target. Prefer a vertical slice that is testable, improves the memory/context workflow, and can be completed in one small commit plus memory refresh. Compare at least three candidate targets and choose one. --latest-context --scope ai-lab-memory --require-admission --token-budget 8000 --model-target gpt-5 --title AI-Lab Next Target After Context Policy Ergonomics`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5`
- Claude: `claude-sonnet-4-5`

## Prompt

AI-Lab has closed the provider latest-context warning-cap and context-policy ergonomics chain through CLI help, policy audit output, comparison metadata, metadata centralization, and dry-run context summaries. Using the admitted ai-lab-memory context, recommend the next smallest implementation target. Prefer a vertical slice that is testable, improves the memory/context workflow, and can be completed in one small commit plus memory refresh. Compare at least three candidate targets and choose one.

## OpenAI Response

- model: `gpt-5`

```
Here are three small, testable vertical-slice targets that build directly on the admitted ai-lab-memory context and the newly added dry-run summary flow.

Candidate A: Dry-run “Context Budget Preview” in --print-context-summary
- What it is
  - When --latest-context, --print-prompt, and --print-context-summary are used, print a per-section token budget preview based on the reconciled default percentages from ABS-0003:
    - System: 15%
    - Answer: 10%
    - Context: 75%, split into Explicit 40%, Dependencies 45%, L1 10%, L0 5%
  - Add an optional --context-window <int> flag to compute absolute token counts; without it, show percentages only.
- Why it helps
  - Operationalizes the reconciled budgeting defaults from ABS-0003 in a zero-risk dry-run, giving contributors a concrete view of packing targets before any retrieval/packing logic lands.
  - Tight feedback loop for sizing prompts and catching budget drift early, improving the memory/context workflow ergonomics immediately.
- Scope/effort
  - One helper to compute nested budgets with deterministic rounding.
  - CLI wiring in ask_provider.py and compare_providers.py.
  - Help text and a few unit tests for both CLIs.
- Testability
  - Deterministic math; verify both percentage-only and absolute token rendering (e.g., with --context-window 8000).
- Risks
  - None to runtime behavior; gated behind the existing --print-context-summary dry-run flags.

Candidate B: JSON mode for --print-context-summary
- What it is
  - Add --summary-format json to output a machine-readable summary payload (policy name, resolved max_warning_admissions and source, optional budget preview as structured data).
- Why it helps
  - Unblocks downstream tooling and CI to parse summaries; reduces fragility of text parsing.
- Scope/effort
  - Small: a serialization gate around an existing data object and tests for both CLIs.
- Testability
  - Golden-file or schema-like structural assertions.
- Risks
  - Minor: requires aligning field names with future manifest/telemetry to avoid churn.

Candidate C: Minimal “Manifest Skeleton” echo in dry-run
- What it is
  - Print a minimal, empty Context Pack Manifest scaffold in the summary (policy, budgeting section, empty inclusions with inclusion_reason fields present).
- Why it helps
  - Socializes the reconciled manifest shape early and creates a clear landing zone for future selection/ranking integration.
- Scope/effort
  - Slightly larger than A/B due to schema definition and tests asserting structure.
- Testability
  - Straightforward structural tests.
- Risks
  - Premature schema lock-in; future manifest details from ABS-0003 may still evolve.

Recommendation: Implement Candidate A (Context Budget Preview) now
- Rationale
  - Highest immediate utility for the memory/context workflow with the smallest surface area and zero runtime impact.
  - Directly applies reconciled budgeting defaults from ABS-0003, closing the loop between policy and packing ergonomics in dry-run.
  - Clean, testable vertical slice that fits “one small commit plus memory refresh.”

Implementation sketch
- Flags and gating
  - Reuse existing gating: --print-context-summary requires --latest-context and --print-prompt.
  - New optional flag: --context-window INT for absolute token calculations.
- Logic
  - Define default percentages:
    - system=15, answer=10, context=75
    - context splits: explicit=40, dependencies=45, l1=10, l0=5
  - If --context-window set:
    - Compute absolute tokens with deterministic rounding:
      - Use floor for each segment; assign remainder to the last leaf of each group to ensure totals match the window.
    - Print both percentages and absolute counts.
  - Else:
    - Print percentages only.
- Output example (dry-run preamble only; illustrative numbers)
  - Latest-context policy: latest_context
  - Resolved max_warning_admissions: 1 (source: policy)
  - Budget preview (context window: 8000)
    - System: 15% → 1200
    - Answer: 10% → 800
    - Context: 75% → 6000
      - Explicit: 40% → 2400
      - Dependencies: 45% → 2700
      - L1: 10% → 600
      - L0: 5% → 300
- Tests
  - ask_provider.py and compare_providers.py:
    - With --latest-context --print-prompt --print-context-summary --context-window 8000, assert the numbers above.
    - Without --context-window, assert percentage-only rendering.
    - Gating errors: using --print-context-summary without required flags should fail (retain existing behavior).
- Docs/help
  - Update CLI help for --print-context-summary to mention budget preview and --context-window.

Expected commit footprint
- ~1 helper function + small CLI integration in two scripts
- 4–6 tests total across both CLIs
- Help text updates

Memory refresh
- New L1 entry noting the addition of budget preview to dry-run summaries and the default reconciled percentages from ABS-0003, with risks note that scripts parsing --print-prompt should avoid enabling the summary preamble.
```

## Claude Response

- model: `claude-sonnet-4-5`

```
# Next Implementation Target Recommendation

## Analysis Context

Based on the admitted context, AI-Lab has completed:
- CLI ergonomics for context policy (`--print-context-summary`)
- Warning-cap and admission gating infrastructure
- Dry-run flows for policy audit
- 206 passing tests

The reconciled memory implementation loop (ABS-0003) describes a full system with L0/L1 summaries, embeddings, retrieval, and write-back. The task is to find the **smallest testable vertical slice** that advances toward this vision.

---

## Candidate Target Comparison

### Candidate 1: **L0 Chunk Creation Helper (Manual Mode)**

**Scope:**  
A CLI script `scripts/create_l0_chunk.py` that accepts a source file path, chunk text/span, and outputs a minimal L0 JSON record conforming to the reconciled `ChunkReference` schema (chunk_id, source_path, span_start/end, content_hash, summary_text, created_at).

**Why small:**
- No retrieval, no embeddings, no auto-summary generation—just manual structured data entry
- Schema validation only (JSON schema or pydantic model)
- Minimal dependencies: file I/O, hash generation, timestamp

**Testability:**
- Unit test: create a chunk, validate schema fields
- Integration test: round-trip write + read from `docs/memory/l0/`
- Negative test: invalid span, missing required fields

**Workflow improvement:**
- Enables **writing L0 records** to feed future retrieval
- Establishes the L0 artifact pattern alongside existing L1 episodes
- Unlocks L0-to-L1 linkage experiments

**Commit size:**
- ~150–200 lines: script, schema definition, tests, one example chunk
- Memory refresh: one L1 episode summarizing the new capability

**Risks:**
- Does not yet integrate with retrieval or prompt assembly (deferred complexity)
- Manual mode may feel incomplete without auto-chunking (but that's a larger slice)

---

### Candidate 2: **Context Pack L0 Inclusion (Read-Only)**

**Scope:**  
Extend `build_context_pack.py` (or the provider assembly code) to **discover and include** existing L0 chunks from `docs/memory/l0/` in the context pack manifest, alongside the current L1 episodes. Display L0 items in `--print-context-summary` output.

**Why small:**
- Leverages existing L1 discovery logic; add parallel glob/JSON load for L0
- No write-back, no embeddings—just read and pack
- Manifest schema already exists (per ABS-0003); add L0 section

**Testability:**
- Unit test: given L0 fixtures, assert they appear in manifest
- Integration test: `--print-context-summary` shows L0 count and token estimate
- Negative test: malformed L0 JSON is skipped with warning

**Workflow improvement:**
- **Closes the loop** from L0 creation (future) to L0 consumption (now)
- Makes L0 chunks **visible and auditable** in dry-run flows
- Prepares manifest structure for retrieval/ranking (next phase)

**Commit size:**
- ~100–150 lines: L0 discovery function, manifest schema update, tests, one example L0 fixture
- Memory refresh: one L1 episode

**Risks:**
- Without retrieval scoring, all L0s are included or arbitrarily limited (naive truncation)
- Token budget may be exceeded if many L0s exist (mitigated by warning or skip logic)

---

### Candidate 3: **Citation Validation Utility**

**Scope:**  
A standalone validator script `scripts/validate_citations.py` that parses a text file (e.g., comparison or L1 summary) and checks citations against the reconciled `cid@version|span` format. Reports malformed citations and optionally verifies that `cid` resolves to an existing L0/L1 artifact.

**Why small:**
- Pure text parsing and pattern matching (regex + file lookups)
- No LLM, no embeddings, no prompt assembly
- Reusable: can be called in CI or manually

**Testability:**
- Unit test: valid/invalid citation strings, span unit rules
- Integration
```

~~~
