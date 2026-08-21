# COMP-0143: Provider Comparison — Next-slice prioritization advisory after A cost-premise falsification

## Metadata

- comparison_id: `COMP-0143`
- title: `Next-slice prioritization advisory after A cost-premise falsification`
- invocation_produced_by: `[{"authoritative": false, "evidence": "docs/invocations/INV-0f89b52441c4d64f.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0143", "target_id": "INV-0f89b52441c4d64f"}, {"authoritative": false, "evidence": "docs/invocations/INV-e7d23803a1456688.json", "predicate": "produced_by", "relation_source": "future_edge_seed", "scope": "invocation_provenance_slice_a", "source_id": "COMP-0143", "target_id": "INV-e7d23803a1456688"}]`
- created_at: `2026-08-21T12:35:49.836546+00:00`
- command: `scripts/compare_providers.py You are re-evaluating prioritization of the next work slice in a governed AI-research repository after a material premise in a prior advisory was falsified. Adjudication rests with the operator; your role is ranked advisory input with reasons.

Prior advisory COMP-0142 ranked A > B > C. Its prompt stated that candidate A required zero new code. A pre-registered measurement requested by that advisory has now falsified that premise: the retained-manifest path exists only under --latest-context; --context-pack prepends text without creating a retained ContextManifest ancestry edge; and the selection rules actually used by compare_providers.py select L1 episodes and admitted abstractions, not COMP-0141, in either admission mode. The earlier zero-code conclusion came from probing the builder directly with defaults that do not match the script's invocation. Terra's prior drop-condition explicitly said A should drop if the dry run could not produce the retained manifest and bound relation without new implementation work; that condition has fired.

Corrected candidates:

(A) Composable instance. Structural benefit is unchanged: create the first real shared-artifact instance joining the already-implemented produced_by and ContextManifest-consumption edge classes, so C3's ancestry half becomes evaluable for one instance under one selection path. Traversal remains excluded. Cost is no longer zero: it requires a governed explicit-inclusion mechanism, for example --include-artifact PATH, that adds a named artifact such as COMP-0141 to the latest-context manifest as a digest-bound item, plus validation, tests, and falsification of the new inclusion path. Exact engineering cost has not yet been measured and should not be assumed cheaper than B merely from intuition.

(B) Verifier/implementer identity pair on verification records. Requires a schema addition, validator change, tests, and a no-retrofit policy for 38 historical verification records. The operator may pre-decide no retrofit, reducing governance uncertainty, but implementation cost remains real.

(C) Effective-configuration capture. Record what provider calls actually ran with rather than only what was supplied. Cost and feasibility remain unmeasured because provider SDK response surfaces have not yet been characterized. Existing evidence shows output_token_limit 16000 versus null across the invocation corpus, suggesting possible cross-provider asymmetry. A prior advisory stated C should rise if effective configuration is already available authoritatively in discarded SDK response objects at low marginal cost.

Rank A, B, C again using only the corrected premises. For each candidate, distinguish measured fact from estimate. State explicitly whether A still ranks first after its zero-code premise and prior drop-condition failed, and why. Name the strongest argument against your new top choice. Then identify the single cheapest measurement that would most likely change your ranking. Do not treat existence of both ancestry edge classes, or one future composable instance, as C3 solved: the maximum claim available to A is that C3's ancestry half becomes evaluable for one retained instance under one selection path. --title Next-slice prioritization advisory after A cost-premise falsification`
- providers: `OpenAI, Claude`

### Models

- OpenAI: `gpt-5.6-terra`
- Claude: `claude-sonnet-5`

## Prompt

You are re-evaluating prioritization of the next work slice in a governed AI-research repository after a material premise in a prior advisory was falsified. Adjudication rests with the operator; your role is ranked advisory input with reasons.

Prior advisory COMP-0142 ranked A > B > C. Its prompt stated that candidate A required zero new code. A pre-registered measurement requested by that advisory has now falsified that premise: the retained-manifest path exists only under --latest-context; --context-pack prepends text without creating a retained ContextManifest ancestry edge; and the selection rules actually used by compare_providers.py select L1 episodes and admitted abstractions, not COMP-0141, in either admission mode. The earlier zero-code conclusion came from probing the builder directly with defaults that do not match the script's invocation. Terra's prior drop-condition explicitly said A should drop if the dry run could not produce the retained manifest and bound relation without new implementation work; that condition has fired.

Corrected candidates:

(A) Composable instance. Structural benefit is unchanged: create the first real shared-artifact instance joining the already-implemented produced_by and ContextManifest-consumption edge classes, so C3's ancestry half becomes evaluable for one instance under one selection path. Traversal remains excluded. Cost is no longer zero: it requires a governed explicit-inclusion mechanism, for example --include-artifact PATH, that adds a named artifact such as COMP-0141 to the latest-context manifest as a digest-bound item, plus validation, tests, and falsification of the new inclusion path. Exact engineering cost has not yet been measured and should not be assumed cheaper than B merely from intuition.

(B) Verifier/implementer identity pair on verification records. Requires a schema addition, validator change, tests, and a no-retrofit policy for 38 historical verification records. The operator may pre-decide no retrofit, reducing governance uncertainty, but implementation cost remains real.

(C) Effective-configuration capture. Record what provider calls actually ran with rather than only what was supplied. Cost and feasibility remain unmeasured because provider SDK response surfaces have not yet been characterized. Existing evidence shows output_token_limit 16000 versus null across the invocation corpus, suggesting possible cross-provider asymmetry. A prior advisory stated C should rise if effective configuration is already available authoritatively in discarded SDK response objects at low marginal cost.

Rank A, B, C again using only the corrected premises. For each candidate, distinguish measured fact from estimate. State explicitly whether A still ranks first after its zero-code premise and prior drop-condition failed, and why. Name the strongest argument against your new top choice. Then identify the single cheapest measurement that would most likely change your ranking. Do not treat existence of both ancestry edge classes, or one future composable instance, as C3 solved: the maximum claim available to A is that C3's ancestry half becomes evaluable for one retained instance under one selection path.

## OpenAI Response

- model: `gpt-5.6-terra`
- invocation_id: `INV-0f89b52441c4d64f`

```
## Revised ranking: **B > A > C**

### 1. B — Verifier/implementer identity pair on verification records

**Measured facts**
- B requires a schema addition, validator change, and tests.
- There are 38 historical verification records.
- A no-retrofit policy can be pre-decided by the operator, removing the question of backfilling those 38 records.
- The work is a bounded, legible governance change: new records either carry the identity pair or fail validation.

**Estimates / unresolved points**
- Exact implementation effort has not been measured.
- The governance usefulness of the new fields depends on how often verifier and implementer identities differ or need independent review.
- A no-retrofit decision would leave a known historical discontinuity.

**Why B ranks first**
B is now the most decision-robust slice. It has real implementation cost, but its required changes, policy decision, and resulting evidence are concrete. Unlike A, it does not depend on adding a new artifact-selection capability whose design and interaction with manifest semantics remain unmeasured. Unlike C, it does not depend on uncharacterized provider SDK behavior.

This is not a claim that B is cheaper than A. It is a claim that, on corrected premises, B has the clearest bounded path from implementation to governed evidence.

**Strongest argument against B**
The strongest case against B is that a no-retrofit policy creates a two-tier verification history: 38 existing records remain without verifier/implementer identity evidence, while only future records gain it. If the principal value is historical accountability rather than prospective prevention, B may produce less practical governance value than its clean implementation boundary suggests.

---

### 2. A — Composable retained-artifact instance

**Measured facts**
- The prior zero-new-code premise is falsified.
- The retained-manifest path is available only under `--latest-context`.
- `--context-pack` prepends text but does not create a retained `ContextManifest` ancestry edge.
- The actual `compare_providers.py` selection rules select L1 episodes and admitted abstractions, not COMP-0141, in either admission mode.
- Terra’s pre-stated drop condition has fired: the dry run cannot produce the retained manifest and bound relation without new implementation work.
- A now requires a governed explicit-inclusion mechanism—such as `--include-artifact PATH`—that inserts a named artifact into the latest-context manifest as a digest-bound item, together with validation, tests, and falsification of that path.
- If completed, A can create one real shared-artifact instance joining the already-implemented `produced_by` and `ContextManifest`-consumption edge classes.

**Maximum supported resulting claim**
A would **not** solve C3. At most, it would make **C3’s ancestry half evaluable for one retained instance under one selection path**. Traversal remains excluded, and the existence of both edge classes plus one future composable instance is not evidence that C3 is generally solved.

**Estimates / unresolved points**
- Exact engineering cost is unmeasured.
- It is not established that A is cheaper than B.
- The inclusion mechanism’s interaction with artifact admission, manifest lifecycle, selection semantics, and falsification requirements has not been measured.
- The resulting instance may be narrow in scope even if technically valid.

**Why A no longer ranks first**
**No. A does not still rank first.** Its prior first-place position materially relied on the now-falsified zero-code premise. More importantly, its own stated drop condition was explicit: A should drop if the dry run could not produce the retained manifest and bound relation without implementation work. That condition has fired.

A retains meaningful structural value, but that value is now paired with unmeasured implementation and governance-design work. Since its demonstrated outcome is deliberately narrow—one retained instance, one selection path, ancestry-half evaluability only—it no longer dominates B’s more bounded prospective governance improvement.

A remains ahead of C because A’s target architecture and required work are now known well enough to describe, whereas C’s feasibility still depends on uncharacterized external SDK response surfaces.

---

### 3. C — Effective-configuration capture

**Measured facts**
- Current evidence records what was supplied to provider calls, not necessarily what actually ran.
- Effective configuration availability in provider SDK responses has not been characterized.
- The invocation corpus shows `output_token_limit` values of `16000` versus `null`, indicating possible cross-provider asymmetry.
- That observation does not establish the providers’ effective applied limits, nor that the relevant values are available authoritatively after execution.

**Estimates / unresolved points**
- Cost is unmeasured.
- Feasibility is unmeasured.
- It is unknown whether SDK response objects contain authoritative effective-configuration values, whether those values survive to a usable capture point, and whether they are comparable across providers.
- If authoritative values are already present in discarded response objects, C could be low-marginal-cost and high-value; if not, it may require provider-specific instrumentation or may not be uniformly achievable.

**Why C ranks third**
C has potentially high governance value because it can distinguish requested from effective execution configuration. But it currently has the greatest feasibility uncertainty. The observed `16000`/`null` asymmetry is a reason to investigate, not evidence that capture is available or cheap.

C could move sharply upward, including above B, if authoritative effective configuration is already exposed in response objects with minimal capture work.

---

## Single cheapest measurement most likely to change the ranking

Perform a **small response-surface inspection across the actually used provider SDK paths**:

1. For one representative successful call per provider used by the corpus, retain or serialize the raw SDK response object at the point immediately after invocation.
2. Inspect whether it contains authoritative applied values for output-token limits and other relevant effective parameters.
3. Record, per provider, whether the value is:
   - present,
   - authoritative rather than inferred,
   - normalized or provider-specific,
   - available without changing request execution semantics.

This is likely cheaper than implementing an artifact-inclusion prototype for A or fully estimating B’s schema migration work, and it has the greatest ranking-changing potential. If the needed values are already authoritatively available in discarded response objects, C’s marginal implementation cost could collapse and C could plausibly become the top slice.
```

## Claude Response

- model: `claude-sonnet-5`
- invocation_id: `INV-e7d23803a1456688`

```
## Re-ranked: B > A > C

### What changed, and what is measured vs. estimated

**Measured facts (from the pre-registered dry run):**
- The retained-manifest path exists only under `--latest-context`.
- `--context-pack` prepends text but does not create a retained `ContextManifest` ancestry edge.
- `compare_providers.py`'s actual selection rules pick L1 episodes and admitted abstractions — not COMP-0141 — under either admission mode.
- Terra's pre-registered drop condition for A ("A should drop if the dry run could not produce the retained manifest and bound relation without new implementation work") has fired. This is not an interpretation — it is the literal outcome of the measurement Terra specified in advance.
- Corpus evidence shows `output_token_limit` 16000 vs. null across invocations (a real, observed asymmetry, though its cause and significance are not yet characterized).
- B's scope is enumerable now: schema addition, validator change, tests, and a fixed, known population of 38 historical verification records requiring a retrofit-policy decision.

**Estimates / unmeasured quantities:**
- A's actual cost to build a governed `--include-artifact` inclusion mechanism (design, validation, tests, and falsification of the new path itself) — explicitly flagged as unmeasured and not to be assumed cheaper than B.
- B's effort in engineer-time (scope is enumerated, magnitude is not).
- C's feasibility and cost — genuinely unknown, contingent on uncharacterized SDK response surfaces.
- Whether the operator will actually pre-decide "no retrofit" for B, which would shrink but not eliminate B's governance overhead.

### Does A still rank first? No.

A does not retain first rank, and it shouldn't by its own prior logic. Terra's drop condition was written specifically to prevent exactly this situation — a structural argument for A surviving on intuition after its cost premise is falsified. The condition is pre-registered and has fired on measured grounds, not contested ones. Beyond the drop condition itself, A's remaining structural claim is real but narrow: it would make C3's ancestry half evaluable for *one instance under one selection path* — not a general solution, and the advisory is explicit that this shouldn't be inflated. Against that narrow, unquantified benefit, A now carries an *unscoped* cost: a new governed inclusion mechanism, its validation, its tests, and its own falsification pass. That is at least as architecturally involved as B's enumerated scope, and we have no basis — measured or estimated — for calling it cheaper. Ranking A first now would require re-introducing the same unexamined-cost assumption that just failed.

B moves to first because its cost, while real, is *bounded and enumerated* (known artifact classes, known record count, known governance lever — the operator can pre-decide no-retrofit to cut uncertainty), whereas A's cost is presently unbounded/unknown and C's is unknown at the more basic level of feasibility.

### Strongest argument against the new top choice (B)

B does nothing for C3 evaluability — it is orthogonal to the ancestry-edge structural goal that has been the throughline of this prioritization. Even fully executed, B leaves C3 exactly where it was. If C3 evaluability is treated as the program's binding structural objective, promoting B to first sacrifices the only candidate (A) that makes any progress there, in exchange for a schema/validator improvement whose value is narrower and more local (verification-record identity integrity). If the operator weights structural-objective progress heavily, this is the argument for holding B below A despite A's now-real cost — and it should be surfaced explicitly rather than resolved by default.

### Cheapest measurement most likely to change the ranking

Inspect the **already-captured, currently discarded SDK response objects** from existing provider-call logs to check whether effective configuration (e.g., the actual `output_token_limit` used) is present there authoritatively. This requires no new code — it's read-only inspection of data that already exists — and it directly resolves the pre-registered rise-condition for C ("C should rise if effective configuration is already available authoritatively in discarded SDK response objects at low marginal cost"). Because it's pure inspection rather than a design/estimation exercise (unlike costing out A's `--include-artifact` mechanism, which requires nontrivial scoping work just to produce a number), this is the lowest-cost lever available, and a positive result could promote C above A immediately.
```
