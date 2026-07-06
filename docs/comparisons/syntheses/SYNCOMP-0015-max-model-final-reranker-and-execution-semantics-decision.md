# SYNCOMP-0015: Comparison Synthesis — Max Model Final Reranker And Execution Semantics Decision

## Metadata

- synthesis_id: `SYNCOMP-0015`
- title: `Max Model Final Reranker And Execution Semantics Decision`
- created_at: `2026-07-06T08:49:22.686865+00:00`
- command: `scripts/synthesize_comparison.py --provider openai docs/comparisons/COMP-0024-max-model-final-reranker-and-execution-semantics-decision.md`
- source_comparison: `docs/comparisons/COMP-0024-max-model-final-reranker-and-execution-semantics-decision.md`
- synthesizer_provider: `OpenAI`
- synthesizer_model: `gpt-5`

## Synthesis

~~~text
1) Shared agreement
- Reranker field decision: ACCEPT AS CONSTRAINED.
- Execution semantics decision: CONFIRM NO LIVE PRODUCTION RETRIEVAL.
- Omitted reranker field is interpreted as "none".
- No reranking behavior, scoring, telemetry, or selection change admitted.
- Inputs limited to simulated/external/read-only snapshots; no external embedding API calls; no index mutation; no production writes.
- BM25/dense outputs are diagnostic-only from fixtures/mocks/read-only snapshots.

2) Meaningful differences
- Omission equivalence:
  - OpenAI: States omission ⇒ "none".
  - Claude: Strengthens with “consumers SHALL NOT distinguish omitted vs explicit 'none'.”
- Reranker schema stance:
  - OpenAI: Non-"none" or telemetry requires new PLAN/WARRANT (implies future extension path).
  - Claude: Any non-"none" value is schema-invalid under this warrant (current strictness explicit).
- Execution prohibitions specificity:
  - OpenAI: Explicitly forbids changing context selection and provider prompts; mentions reranker provider/model attribution logging prohibition; notes compatibility alias inherits constraints.
  - Claude: Ties outputs to selection_effect: "none"; does not explicitly mention alias inheritance or provider/model attribution.
- PLAN wording delta posture:
  - OpenAI: No delta.
  - Claude: No delta, but highlights a clarifying clause about omission equivalence embedded in the warrant snippet.

3) Stronger points from OpenAI
- Explicit prohibition list for reranker field: no triggering, implying, or recording of reranking steps, scoring, provider/model attribution, selection reordering, or selection change.
- Execution constraints explicitly include: no change to context selection or provider prompts.
- Compatibility alias inheritance called out (context_pack.selection_diagnostics.retrieval_candidates is read-only/deprecated and inherits constraints).

4) Stronger points from Claude
- Normative clarity: consumers SHALL NOT distinguish omitted vs explicit "none".
- Schema strictness: any non-"none" reranker value is schema-invalid under this warrant.
- Explicit linkage that diagnostic outputs have selection_effect: "none".
- Clear binding constraints summary for reranker acceptance (optional, enum ["none"], omitted ⇒ "none", future changes require new PLAN/WARRANT).

5) Combined answer
- A. Reranker field decision: ACCEPT AS CONSTRAINED.
- B. Execution semantics decision: CONFIRM NO LIVE PRODUCTION RETRIEVAL.
- C. Exact warrant text snippets:
  - Reranker field:
    The simulator header MAY include an optional reranker field constrained to the enum ["none"]. An omitted reranker field SHALL be interpreted as "none", and consumers SHALL NOT distinguish the omitted case from the explicit "none" case. This field is declarative compatibility metadata only and MUST NOT trigger, imply, or record any reranking step, reranker scoring, reranker provider/model attribution, selection reordering, selection change, or reranker telemetry of any kind beyond the literal or implicit value "none". Any non-"none" value is schema-invalid under this warrant; admission of any other value or any reranker telemetry requires a separate PLAN and WARRANT.
  - Execution semantics:
    The L0 retrieval simulator at manifest.diagnostics.l0_retrieval_simulator is diagnostic-only and SHALL NOT perform live retrieval against production indices. All simulator inputs MUST be simulated, externally provided as inert diagnostic data, or read from explicitly read-only snapshots. The simulator MUST NOT call external embedding APIs, create production embeddings, mutate any vector or document index, change context selection, change provider prompts, or perform production writes. BM25 and dense scores emitted by the simulator are diagnostic outputs derived exclusively from fixtures, mocks, or read-only snapshots, have no selection effect (selection_effect: "none"), and any compatibility alias, including context_pack.selection_diagnostics.retrieval_candidates, is read-only/deprecated and inherits these execution constraints.
- D. PLAN wording delta: None required beyond incorporating the above warrant snippets.

6) Risks or missing assumptions
- Enforcement locus risk: Validation MUST reject any non-"none" reranker value at schema/ingest time; otherwise runtime paths could diverge. (Inference)
- Omission-equivalence drift: All consumers and serializers must treat omitted and "none" identically; the explicit “SHALL NOT distinguish” clause mitigates but requires conformance testing.
- Telemetry leakage: Logging/metrics systems might accidentally capture reranker-related telemetry or provider/model attribution; warrants forbid this, but instrumentation audits are needed. (Inference)
- Alias path conformance: Ensure all readers of context_pack.selection_diagnostics.retrieval_candidates actually treat it as read-only and inherit constraints.
- Selection side-effects: OpenAI explicitly forbids any selection change; implementations relying only on selection_effect: "none" must also avoid implicit reordering or prompt mutations.
- Snapshot integrity: Read-only snapshots must be provenance-verified and access-controlled to avoid accidental live reads or writes. (Inference)

7) Suggested re-ask prompt
Resolve final warrant text freeze for PLAN-20260706-0002. All prior boundaries remain fixed. Decide only confirmation and exact text approval.

Decisions (must answer exactly as instructed):
1) Reranker field decision:
- Respond exactly one: ACCEPT AS CONSTRAINED or REJECT FIELD ENTIRELY
2) Execution semantics decision:
- Respond exactly one: CONFIRM NO LIVE PRODUCTION RETRIEVAL or ADJUST

If adjusting or rejecting, provide only the exact schema or permissible-operations delta.

Approve or redline the exact warrant text below:
Warrant — Reranker field:
"The simulator header MAY include an optional reranker field constrained to the enum ['none']. An omitted reranker field SHALL be interpreted as 'none', and consumers SHALL NOT distinguish the omitted case from the explicit 'none' case. This field is declarative compatibility metadata only and MUST NOT trigger, imply, or record any reranking step, reranker scoring, reranker provider/model attribution, selection reordering, selection change, or reranker telemetry of any kind beyond the literal or implicit value 'none'. Any non-'none' value is schema-invalid under this warrant; admission of any other value or any reranker telemetry requires a separate PLAN and WARRANT."

Warrant — Execution semantics:
"The L0 retrieval simulator at manifest.diagnostics.l0_retrieval_simulator is diagnostic-only and SHALL NOT perform live retrieval against production indices. All simulator inputs MUST be simulated, externally provided as inert diagnostic data, or read from explicitly read-only snapshots. The simulator MUST NOT call external embedding APIs, create production embeddings, mutate any vector or document index, change context selection, change provider prompts, or perform production writes. BM25 and dense scores emitted by the simulator are diagnostic outputs derived exclusively from fixtures, mocks, or read-only snapshots, have no selection effect (selection_effect: 'none'), and any compatibility alias, including context_pack.selection_diagnostics.retrieval_candidates, is read-only/deprecated and inherits these execution constraints."

Output format:
A. Reranker field decision
B. Execution semantics decision
C. APPROVE WARRANT TEXT or REDLINE WITH EXACT TEXT
D. Exact PLAN wording delta, only if needed
~~~

## Source Comparison

~~~markdown
# COMP-0024: Provider Comparison — Max-model final reranker and execution semantics decision

## Metadata

- comparison_id: `COMP-0024`
- title: `Max-model final reranker and execution semantics decision`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- context_manifest: `docs/comparisons/COMP-0024-max-model-final-reranker-and-execution-semantics-decision.context.json`
- created_at: `2026-07-06T08:44:40.654729+00:00`
- command: `scripts/compare_providers.py --latest-context --require-admission --title Max-model final reranker and execution semantics decision Resolve the final two decisions before creating PLAN-20260706-0002.

All prior boundaries are fixed:
- No automatic L0 retrieval.
- No context selection changes.
- No provider prompt changes.
- No production embedding creation.
- No vector/index mutation.
- No reranking unless explicitly admitted later.
- No token budget telemetry.
- No selection adapter integration.
- No persistent write-back.
- Canonical path: manifest.diagnostics.l0_retrieval_simulator.
- Compatibility alias: context_pack.selection_diagnostics.retrieval_candidates, read-only/deprecated.
- selection_effect enum: ["none"] only.
- combine_policy and normalization require explicit config; no defaults.

Prior artifacts:
- COMP-0021 / SYNCOMP-0012
- COMP-0022 / SYNCOMP-0013
- COMP-0023 / SYNCOMP-0014

Decide only these two items:

1. Header reranker field:
   Proposed resolution:
   - Keep header.reranker as an optional field.
   - Allowed values: ["none"] only.
   - If omitted, treat as "none".
   - Warrant still says no reranking and no reranker telemetry beyond "none".

   Answer exactly one:
   - ACCEPT AS CONSTRAINED
   - REJECT FIELD ENTIRELY

   If rejecting, provide the exact schema delta only.

2. Execution semantics:
   Proposed resolution:
   - Simulator SHALL NOT perform live retrieval against production indices.
   - Inputs MUST be simulated, externally provided, or read from explicitly read-only snapshots.
   - No external embedding API calls.
   - No vector/document index mutation.
   - No production writes.
   - BM25/dense scores are diagnostic outputs from fixtures, mocks, or read-only snapshots only.

   Answer exactly one:
   - CONFIRM NO LIVE PRODUCTION RETRIEVAL
   - ADJUST

   If adjusting, provide exact permissible operations only.

Output format:
A. Reranker field decision
B. Execution semantics decision
C. Exact warrant text snippets for both decisions
D. Exact PLAN wording delta, only if needed`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.5-pro`
- Claude: `claude-fable-5`

## Prompt

Resolve the final two decisions before creating PLAN-20260706-0002.

All prior boundaries are fixed:
- No automatic L0 retrieval.
- No context selection changes.
- No provider prompt changes.
- No production embedding creation.
- No vector/index mutation.
- No reranking unless explicitly admitted later.
- No token budget telemetry.
- No selection adapter integration.
- No persistent write-back.
- Canonical path: manifest.diagnostics.l0_retrieval_simulator.
- Compatibility alias: context_pack.selection_diagnostics.retrieval_candidates, read-only/deprecated.
- selection_effect enum: ["none"] only.
- combine_policy and normalization require explicit config; no defaults.

Prior artifacts:
- COMP-0021 / SYNCOMP-0012
- COMP-0022 / SYNCOMP-0013
- COMP-0023 / SYNCOMP-0014

Decide only these two items:

1. Header reranker field:
   Proposed resolution:
   - Keep header.reranker as an optional field.
   - Allowed values: ["none"] only.
   - If omitted, treat as "none".
   - Warrant still says no reranking and no reranker telemetry beyond "none".

   Answer exactly one:
   - ACCEPT AS CONSTRAINED
   - REJECT FIELD ENTIRELY

   If rejecting, provide the exact schema delta only.

2. Execution semantics:
   Proposed resolution:
   - Simulator SHALL NOT perform live retrieval against production indices.
   - Inputs MUST be simulated, externally provided, or read from explicitly read-only snapshots.
   - No external embedding API calls.
   - No vector/document index mutation.
   - No production writes.
   - BM25/dense scores are diagnostic outputs from fixtures, mocks, or read-only snapshots only.

   Answer exactly one:
   - CONFIRM NO LIVE PRODUCTION RETRIEVAL
   - ADJUST

   If adjusting, provide exact permissible operations only.

Output format:
A. Reranker field decision
B. Execution semantics decision
C. Exact warrant text snippets for both decisions
D. Exact PLAN wording delta, only if needed

## OpenAI Response

- model: `gpt-5.5-pro`

````
A. Reranker field decision

ACCEPT AS CONSTRAINED

B. Execution semantics decision

CONFIRM NO LIVE PRODUCTION RETRIEVAL

C. Exact warrant text snippets for both decisions

```text
Reranker field constraint: header.reranker is optional and has the only admitted value "none". If omitted, it is interpreted as "none". This warrant admits no reranking behavior and no reranker telemetry beyond the literal or implicit value "none". The field is declarative compatibility metadata only and MUST NOT trigger, imply, or record any reranking step, reranker scoring, reranker provider/model attribution, selection reordering, or selection change. Any non-"none" value or reranker telemetry requires a separate admitted PLAN and WARRANT.
```

```text
Execution constraint: manifest.diagnostics.l0_retrieval_simulator is diagnostic-only and SHALL NOT perform live retrieval against production indices. Simulator inputs MUST be simulated, externally provided as inert diagnostic data, or read from explicitly read-only snapshots. The simulator MUST NOT call external embedding APIs, create production embeddings, mutate vector/document indices, change context selection, change provider prompts, or perform production writes. BM25/dense scores are diagnostic outputs from fixtures, mocks, or explicitly read-only snapshots only. Any compatibility alias, including context_pack.selection_diagnostics.retrieval_candidates, is read-only/deprecated and inherits these execution constraints.
```

D. Exact PLAN wording delta, only if needed

None.
````

## Claude Response

- model: `claude-fable-5`

```
# Decision Resolution for PLAN-20260706-0002

## A. Reranker field decision

**ACCEPT AS CONSTRAINED**

Rationale (brief): The constrained form is structurally identical to the already-fixed `selection_effect` enum `["none"]` boundary — a single-value enum whose only function is to make the *absence* of behavior explicit and machine-checkable. It creates no reranking capability, no telemetry beyond the literal `"none"`, and the omitted-defaults-to-`"none"` rule keeps the alias path (`context_pack.selection_diagnostics.retrieval_candidates`) readable without schema divergence. Rejecting the field would remove an explicit negative assertion without reducing any actual capability surface.

Binding constraints on acceptance:
- `header.reranker` is optional.
- Enum: `["none"]`. No other value is schema-valid.
- Omitted ⇒ interpreted as `"none"`. Readers MUST NOT distinguish omitted from `"none"`.
- Any future non-`"none"` value requires a new PLAN, new WARRANT, and new admission verdict (consistent with the fixed boundary: no reranking unless explicitly admitted later).

## B. Execution semantics decision

**CONFIRM NO LIVE PRODUCTION RETRIEVAL**

The proposed resolution is confirmed verbatim, with no adjustments. It is fully consistent with every fixed boundary: no production embedding creation, no vector/index mutation, no persistent write-back, no selection adapter integration, and diagnostic-only scoring. No permissible-operations list is provided because none is needed — the proposal as written is the complete permitted surface.

## C. Exact warrant text snippets

**WARR snippet — reranker field:**

> The simulator header MAY include an optional `reranker` field constrained to the enum `["none"]`. An omitted `reranker` field SHALL be interpreted as `"none"`, and consumers SHALL NOT distinguish the omitted case from the explicit `"none"` case. This warrant does NOT admit reranking behavior, reranker configuration, reranker scoring, or reranker telemetry of any kind beyond the literal value `"none"`. Any non-`"none"` value is schema-invalid under this warrant. Admission of any reranking behavior requires a separate PLAN, a separate WARRANT, and a new admission verdict.

**WARR snippet — execution semantics:**

> The L0 retrieval simulator at `manifest.diagnostics.l0_retrieval_simulator` SHALL NOT perform live retrieval against production indices. All simulator inputs MUST be simulated, externally provided, or read from explicitly read-only snapshots. The simulator SHALL NOT make external embedding API calls, SHALL NOT create production embeddings, SHALL NOT mutate any vector or document index, and SHALL NOT perform production writes. BM25 and dense scores emitted by the simulator are diagnostic outputs derived exclusively from fixtures, mocks, or read-only snapshots, and SHALL have no selection effect (`selection_effect: "none"`).

## D. PLAN wording delta

No delta required. Both proposed resolutions are adopted verbatim; PLAN-20260706-0002 SHALL incorporate the two warrant snippets in section C without modification. The only normative addition beyond the proposals as written is the single clarifying clause already embedded in the reranker snippet:

> "consumers SHALL NOT distinguish the omitted case from the explicit `\"none\"` case"

This clause closes the only ambiguity in the original proposal (whether omission is semantically distinct from an explicit `"none"`), and requires no other PLAN wording changes.

---

*Note on sources: SYNCOMP-0014 and COMP-0023 were excluded from the context pack by admission policy and were not relied upon. These decisions rest on the fixed boundaries stated in the task and the completed-slice constraints recorded in L1-20260706-context-manifest-l0-diagnostics-completion (diagnostic-only, no automatic retrieval, no selection changes).*
```

~~~
