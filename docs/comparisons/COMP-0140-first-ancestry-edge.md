# COMP-0140: Provider Comparison — First retained ancestry edge

## Metadata

- comparison_id: `COMP-0140`
- title: `First retained ancestry edge`
- context_policy: `latest_context`
- context_require_admission: `true`
- context_max_warning_admissions: `1`
- context_max_warning_admissions_source: `provider_default`
- context_manifest: `docs/comparisons/COMP-0140-first-ancestry-edge.context.886cca23baadb266f8ebefae1f20bc00a5956b62f0c6e410c88f3363c3394522.json`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-8419d4bb8a312acc.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0140", "target_id": "INV-8419d4bb8a312acc"}, {"authoritative": false, "evidence": "docs/invocations/INV-f7249a960a179db3.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0140", "target_id": "INV-f7249a960a179db3"}]`
- created_at: `2026-08-20T10:25:02.621185+00:00`
- command: `scripts/compare_providers.py --latest-context --require-admission --save docs/comparisons/COMP-0140-first-ancestry-edge.md --title First retained ancestry edge What is the single most likely way an artifact-level evidence-ancestry edge could mislead a reader who trusts it?`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

What is the single most likely way an artifact-level evidence-ancestry edge could mislead a reader who trusts it?

## OpenAI Response

- model: `gpt-5.6-terra`

```
It can falsely imply that the whole artifact supports a downstream claim or summary when only a specific passage—or possibly no identifiable passage—does. Without chunk- and span-level provenance, a trusted artifact-level ancestry edge obscures the exact evidence, making unsupported or overgeneralized claims appear properly grounded.
```

## Claude Response

- model: `claude-sonnet-5`

```
Based on the ABS-0003 material, the granularity mismatch between providers' L0 designs is the clearest analog for this failure mode:

**Most likely way an artifact-level evidence-ancestry edge misleads a reader:**

An edge asserted at the **artifact level** implies "this entire artifact supports/derives-from that entire artifact," but the actual evidentiary support may only cover a **small span or chunk** within the source artifact — not the whole thing. The reader trusting the edge will assume the full source artifact backs the full claim, when in reality only a fragment does.

This is exactly the tension the abstraction surfaces between the two designs:

- **OpenAI's approach** ties citations to **chunk-level spans** (`cid@version|span`), so provenance is precise — you know *which part* of the artifact is the actual evidence.
- **Claude's approach** uses an **artifact-level "ArtifactSummary"** with no chunk_id or span information — the ancestry edge points at the whole artifact, with no way to tell what portion actually justifies the claim.

If a reader only sees an artifact-level ancestry edge (Claude-style) but assumes it carries the same precision as a chunk/span-level citation (OpenAI-style), they will over-trust the edge — treating a coarse "this artifact relates to that artifact" link as if it were a validated, span-bounded citation. In practice this means:

- The reader may believe a specific sub-claim is directly evidenced, when actually only *some unspecified part* of a large source artifact loosely relates to it.
- Downstream consumers, updates, or edits to the *unrelated* parts of the source artifact won't trigger any invalidation of the edge (since there's no span-level dependency tracking), so the ancestry edge can silently go stale or misleading as the source evolves — the refresh/staleness triggers described in the abstraction (content/dependency changes, TTL) are far less reliable without span-level granularity to know *what* changed matters.

**In short:** the single most likely failure is **false precision** — the reader infers span-level, validated support from what is actually only a coarse, unverified whole-artifact association, because artifact-level ancestry edges collapse the distinction between "the source loosely touches this topic" and "this exact excerpt is the evidence."
```
