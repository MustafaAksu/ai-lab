# COMP-0142: Provider Comparison — Next-slice prioritization advisory

## Metadata

- comparison_id: `COMP-0142`
- title: `Next-slice prioritization advisory`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-4ab872f406e82926.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0142", "target_id": "INV-4ab872f406e82926"}, {"authoritative": false, "evidence": "docs/invocations/INV-66610ffb5b4249e2.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0142", "target_id": "INV-66610ffb5b4249e2"}]`
- created_at: `2026-08-21T12:16:12.069029+00:00`
- command: `scripts/compare_providers.py You are advising prioritization of the next work slice in a governed AI-research repository. Adjudication rests with the operator; your role is ranked advisory input with reasons. Current state: both evidence-ancestry edge classes are implemented (ContextManifest consumption edge; artifact-produced_by-invocation established by output-digest recomputation, 2 established relations on COMP-0141); no artifact instance yet joins the two classes, so no invocation-to-artifact-to-invocation path exists and constraint C3 remains unevaluable. Candidates, with measured cost: (A) Composable instance: one governed run consuming COMP-0141 through a retained ContextManifest; measured as zero new code since the selection rule already picks COMP-0141 and the run path binds per-item digests; directly serves C3; traversal deliberately excluded. (B) Verifier/implementer identity pair on verification records: closes part of an open gap on manual-enforcement evidence; requires a schema addition, validator change, no-retrofit policy for 38 historical records, and tests; touches governance schema. (C) Effective-configuration capture: record what provider calls actually ran with, not what was supplied; cost currently unmeasurable because the provider SDK response surfaces have not been measured; a witness asymmetry (output_token_limit 16000 vs null across all 214 records) suggests cross-provider unevenness. Rank A, B, C with a one-paragraph justification each, name the strongest argument AGAINST your top choice, and state what measurement would change your ranking. --title Next-slice prioritization advisory`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are advising prioritization of the next work slice in a governed AI-research repository. Adjudication rests with the operator; your role is ranked advisory input with reasons. Current state: both evidence-ancestry edge classes are implemented (ContextManifest consumption edge; artifact-produced_by-invocation established by output-digest recomputation, 2 established relations on COMP-0141); no artifact instance yet joins the two classes, so no invocation-to-artifact-to-invocation path exists and constraint C3 remains unevaluable. Candidates, with measured cost: (A) Composable instance: one governed run consuming COMP-0141 through a retained ContextManifest; measured as zero new code since the selection rule already picks COMP-0141 and the run path binds per-item digests; directly serves C3; traversal deliberately excluded. (B) Verifier/implementer identity pair on verification records: closes part of an open gap on manual-enforcement evidence; requires a schema addition, validator change, no-retrofit policy for 38 historical records, and tests; touches governance schema. (C) Effective-configuration capture: record what provider calls actually ran with, not what was supplied; cost currently unmeasurable because the provider SDK response surfaces have not been measured; a witness asymmetry (output_token_limit 16000 vs null across all 214 records) suggests cross-provider unevenness. Rank A, B, C with a one-paragraph justification each, name the strongest argument AGAINST your top choice, and state what measurement would change your ranking.

## OpenAI Response

- model: `gpt-5.6-terra`
- invocation_id: `INV-4ab872f406e82926`

```
**1. A — Composable instance.** This is the highest-value next slice because it converts two already-established edge classes into the first actual invocation-to-artifact-to-invocation witness, making C3 evaluable rather than merely structurally anticipated. Its measured incremental implementation cost is zero: the selection rule already chooses COMP-0141, and the governed-run path already binds per-item digests. It is also narrowly scoped, preserves the existing governance model, and produces a concrete evidence object whose validity can be independently checked through the retained `ContextManifest` and output-digest recomputation. Deliberately excluding traversal is appropriate for this slice: establish the composable witness first, then decide whether traversal deserves separate work.

**2. B — Verifier/implementer identity pair on verification records.** This addresses a real and meaningful governance gap: manual-enforcement evidence is weaker when the actor who implemented a change and the actor who verified it cannot be distinguished. It is second because it requires a schema change, validator changes, tests, and an explicit no-retrofit treatment for 38 historical records, all of which create compatibility and policy surface beyond the immediate evidence gain. Still, the work is bounded and measurable, and it improves accountability in a way that is likely durable across future records. The no-retrofit policy should be recorded explicitly so that the historical omission is itself governed rather than silently normalized.

**3. C — Effective-configuration capture.** This may ultimately be highly important, especially given the observed `output_token_limit` asymmetry—`16000` versus `null` across all 214 records—which is evidence that supplied configuration is not necessarily the effective configuration under all providers. However, it should rank third now because its cost, feasibility, and even the available authoritative data surfaces remain unmeasured. Recording an inferred or partially surfaced “effective” configuration before establishing what each provider SDK actually returns risks creating misleading provenance. The appropriate immediate posture is investigation and measurement, not committing it as the next implementation slice.

**Strongest argument against A:** A may produce only a minimal, potentially non-representative witness: it demonstrates that one selected artifact can bridge the two edge classes, but it does not validate traversal behavior, broader selection behavior, or whether such paths remain stable under ordinary repository use. If C3’s practical value depends on general graph-query capability rather than merely the existence of one composable path, A could be criticized as proving only a narrow construction while deferring the operationally harder part.

**Measurement that would change the ranking:** The most consequential measurement is a provider-by-provider, SDK-version-specific experiment showing whether effective runtime configuration is available authoritatively, at what granularity, and with what implementation and retention cost. If that experiment shows that effective parameters—including token limits, model/provider-resolved values, and defaults—are reliably obtainable for the materially used providers with a small bounded change, C could move ahead of B and potentially A, particularly if the 214-record asymmetry is shown to affect reproducibility or policy compliance. Conversely, if an A dry run fails to produce a retained manifest, a correctly bound digest, and a verifiable output-produced-by relation without new implementation work, A should drop. B would rise if an audit shows that missing verifier/implementer separation presently blocks a required approval, segregation-of-duties control, or investigation workflow.
```

## Claude Response

- model: `claude-sonnet-5`
- invocation_id: `INV-66610ffb5b4249e2`

```
# Ranking: A > B > C

## A — Composable instance (Top choice)

This closes the single largest gap in the evidence-ancestry graph at the lowest possible cost: zero new code. Both edge classes already exist independently; what's missing is an actual instance that joins them, which is the precondition for C3 evaluability at all. Right now C3 is not "failing" — it's *unevaluable*, meaning the repository cannot make any claim about invocation-to-artifact-to-invocation integrity. A single governed run through a retained ContextManifest converts C3 from an open question into a testable one. The explicit exclusion of traversal is a scope discipline worth preserving for this slice — it isolates "does the joined instance exist" from "does multi-hop traversal work," which is a separate and larger claim. Given the cost is measured at zero, the only argument for not doing this would be that something else is more urgent — and nothing here dominates closing a load-bearing structural gap for free.

## B — Verifier/implementer identity pair

This is legitimate governance debt but is costed, not free: schema addition, validator change, a no-retrofit policy decision affecting 38 historical records, and new tests. The no-retrofit policy is itself a governance decision that needs deliberate framing (silently grandfathering 38 records into an exempt class is a real precedent, not a detail). This work should happen, but it's addressing a *known, bounded* gap in manual-enforcement evidence rather than an *unevaluable constraint* blocking downstream reasoning. It's well-specified enough to schedule confidently, which makes it a reasonable second slice once A is banked.

## C — Effective-configuration capture

The witness asymmetry (16000 vs null across all 214 records) is a real signal worth flagging, but the cost is explicitly unmeasured because the provider SDK response surfaces haven't been characterized yet. Prioritizing unmeasured work ahead of measured, zero-cost work that closes a structural gap is backwards. This candidate needs a scoping/measurement pass before it can even be ranked against B, let alone A.

---

## Strongest argument against A

**A only produces a single instance, not a validated path.** Because traversal is deliberately excluded, completing A tells you an artifact *can* join the two edge classes, but not that the join is well-formed under composition (e.g., digest binding stays consistent across multiple hops, or that the selection rule generalizes beyond COMP-0141's convenient default). There's a risk that A gets treated as "C3 solved" when it has only made C3 *evaluable for one instance under one selection path*. The one-paragraph justification above should be read with this caveat attached to any downstream claim.

## What measurement would change the ranking

If someone measured the provider SDK response surfaces for C and found that effective-configuration capture is **also near-zero marginal cost** (e.g., the data is already in a response object being discarded, not requiring new API calls or schema), then C would jump ahead of B — a live, silent cross-provider correctness risk (16000 vs null) outranks a documentation/attribution gap on historical records. Separately, if the no-retrofit policy for B were pre-decided by the operator (removing that as an open governance question), B's true engineering cost would drop and it might tie with A on cost — at which point the tiebreaker would be "unevaluable constraint" (A) vs. "known gap with bounded blast radius" (B), and A would still win, but by a thinner margin.
```
