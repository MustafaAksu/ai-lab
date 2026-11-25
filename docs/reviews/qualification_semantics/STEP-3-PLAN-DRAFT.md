# Step 3 PLAN draft — qualification semantics, r2

[ALG] **PLAN-20261125-0001 remains proposed; PR #5 remains draft. No implementation admission is granted.** This is the single bounded r2 requested after [review 6064341643](https://github.com/MustafaAksu/ai-lab/pull/5#pullrequestreview-6064341643), whose disposition is `CHANGES_REQUESTED_BEFORE_ADMISSION` and GitHub state is `COMMENTED`.

The [canonical proposed PLAN](../../self_model/plans/PLAN-20261125-0001.json) retains `created_at=2026-11-25T09:20:01+00:00`. Its r2 revision time is the actual clock observation `2026-11-25T20:32:52+00:00`. Original source baseline: `5515f55894b10ad70c321340257f67a960dcc382`; reviewed r1 head/revision base: `8b8e24d133eaa3a585eefa14e76a02a519b73b03`. ChatGPT is the drafting executor. The review and assisting analyses supply no independent C3/C5/C7/C10 adjudication; the GitHub actor account does not establish writer–PI identity separation.

## 1. Bounded r2 artifacts

[ALG] The candidate is specified by these linked proposal documents. None installs a schema, registry, policy, runtime evaluator or live trust rule.

| Artifact | Function in the candidate |
| --- | --- |
| [Evidence contract](EQUIVALENCE-EVIDENCE-CONTRACT-DRAFT.md) | Per-kind semantics and D1–D8 decisions proposed for review |
| [ASSESSMENT-SCHEMA.json](r2/ASSESSMENT-SCHEMA.json) | Closed proposed shapes, exact `ai_lab.qualification.r2/1` version, required fields, nullability and result/error boundaries |
| [SCHEMA-EXAMPLES.json](r2/SCHEMA-EXAMPLES.json) | Synthetic document examples; validating their shape does not establish their claims |
| [DETERMINISTIC-RULES.md](r2/DETERMINISTIC-RULES.md) | Source selection, endpoint/target checks, witness checks, fixed synthetic profiles and reason precedence |
| [CONSUMER-COMPATIBILITY.md](r2/CONSUMER-COMPATIBILITY.md) | All public/legacy entry points, annotation consumers and refusal adapter |
| [Falsification matrix](FALSIFICATION-MATRIX.md) | Positive/negative oracles and targeted broken-variant requirements |
| [R2 review response](r2/R2-REVIEW-RESPONSE.md) | Changes mapped to review 6064341643 |
| [Source-review baseline](SOURCE-REVIEW-BASELINE.md) | Retained r1 source findings and executed diagnostic observations |

The original [preparation artifact](STEP-3-PREPARATION.md), r1 probe script and its two reports, retained pytest output and validation artifact remain historical evidence. r2 does not replace their measurements with expectations for unimplemented behavior. Schema/example checks during preparation establish document consistency only.

## 2. Frozen sequence and S1–S8 mapping

[ALG] Each prospective increment requires its own named review/admission gate. Completing one never admits the next. **3A precedes 3B, which precedes 3C.**

| Increment / decision | Scope IDs | Bounded prospective work | Positive-path boundary |
| --- | --- | --- | --- |
| 3A: D1–D3 | S1, S4, S8 | Endpoint/model binding, source inventory/applicability, conflict-preserving aggregation and exact witness conditions; protect every existing consumer route | No production positive identity/constraint gate; synthetic model-witness conditions only |
| 3B: D4–D5 | S1, S2, S3, S8 | Fixed `SYN-TOOL-1` and `SYN-HUMAN-1` contract evaluation | Synthetic-only; no live issuer, release, principal, actor or enrollment profile |
| 3C: D8 | S1, S7, S8 | Fail-closed C3/C10 evidence checks on top of 3A's protected consumer boundary | No combined positive C3/C10 result in any domain; no ancestry-positive profile |
| D6 | S5 | Separately documented recommendation: cross-kind remains unresolved in both orders | No resolving rule or canonical decision issued |
| D7 | S6 | Separately documented recommendation: superclass deferred | No hierarchy, migration or ontology amendment |

S1 is the common schema/result/context contract. S8 supplies verification for each admitted increment. The immediate next possible implementation decision concerns bounded **3A**, after review and a separate explicit PI admission of the exact revision. This document does not make that decision.

## 3. Three result axes and typed errors

[ALG] `supplied_relation` may report agreement among the supplied assertions. It is a diagnostic, not a fourth clearance axis. Where authoritative context or governed inventory coverage is absent, `R_identity` remains unresolved even if that diagnostic shows agreement.

| Axis | r2 values | Meaning and boundary |
| --- | --- | --- |
| `R_identity` | `equivalent`, `non_equivalent`, `unresolved` | Clean governed relation after the required context, source, applicability and binding checks; not independence |
| `Q_identity` | `withheld`, `conditions_satisfied` | Necessary identity-evidence condition only; always withheld in production; positive only within the three pinned synthetic profiles |
| `Q_C3_C10` | `violated`, `unresolved` | Bounded constraint findings, with separate C3 and C10 diagnostics; C10 always unresolved; production combined result unresolved; no positive value |

Malformed inputs use the closed `AssessmentResult` invalid form: `validation_status=invalid`, nonempty typed `validation_reasons`, unresolved relation/constraint findings and withheld identity condition. That form cannot be consumed as a valid assessment or ignored in favor of later success. A valid but unknown/insufficient evidence condition retains its specified unresolved/withheld reason. No axis, diagnostic, schema-valid object or Boolean adapter issues authority.

An accepted synthetic direct or equivalent-identity C3 conflict remains blocking even if other ancestry coverage is incomplete. SYN-C3-CONFLICT-1 fixes fictional directional-edge and ancestor-assessment premises under the harness anchor; opaque edge digests are insufficient. Production C3 remains unresolved because no live directional-evidence rule is enabled. Absence of a found conflict over incomplete coverage remains unresolved. Unknown ancestry is also not affirmative shared ancestry; it cannot manufacture a self-authored or independent lineage finding.

`Q_identity=conditions_satisfied` is available only through isolated evaluations under `SYN-TOOL-1`, `SYN-HUMAN-1` or `SYN-MODEL-WITNESS-1`. The positive synthetic identity condition additionally requires valid input, governed `R_identity=non_equivalent`, `coverage=pinned_inventory_exhausted` and the exact profile evidence checks. A caller's `established`, `synthetic` or `test_mode` value cannot select that trusted evaluation domain or turn a fixture result into production evidence. There is no synthetic ancestry-positive profile. A future full positive C3/C10 evaluator requires a later admitted scope and applicable GAP-0008 evidence.

## 4. 3A: endpoint, source and witness contract

### D1: endpoint and model evidence

[ALG] The r2 rules distinguish a catalog-declared endpoint/name mapping from an affirmatively established invocation/endpoint binding. Invocation spellings such as `openai.responses` are linked through the retained endpoint identity by exact unique spelling; no endpoint alias rule is supported; a spelling is not compared directly with an EID, and a model originator does not define the serving endpoint.

The rules fix the current configurable **30-day default** freshness window and inclusive validity boundaries. Source observation, successful capture, demonstrable event-time availability, import time and retrospective knowledge cutoff are separate. Later observation/corroboration is not backdated. The candidate distinguishes null assertion scope from unsupported non-null scope and defines outcomes for invalid intervals and unknown aliases.

Snapshot/capture ID linkage is checked separately from complete retained-byte digests. Capture success and a dereferenced valid ModelIdentity target are required where the identity gate relies on them. Unsuccessful capture, a scalar/dangling/wrong-kind target, conflicting bytes for one target ID or unresolved release identity cannot clear that gate. A narrower catalog assertion may remain reportable as such; valid-looking IDs and labels do not establish the stronger binding.

### D2: noncaller bounded source universe

[ALG] `REPO-CATALOG-ALL-1` selects all retained entries recursively under `docs/catalog/{eid,mid,snap,cap,payloads}/` from the anchored Git tree, together with pinned known-source/omission declarations. The consumer loads the policy/context anchor independently of query input. The caller cannot choose a smaller universe, substitute a favorable anchor, omit a known relevant capture or assert `complete=true` to obtain clearance.

The manifest is checked against the fixed inventory, event/knowledge cutoff and coverage evidence. The result over supplied assertions remains distinguishable from a clean governed aggregate. Evidence outside the bounded scope is not disproved by agreement inside it.

Within that universe, applicability is relevant, proven irrelevant or undetermined. Wrong-endpoint/expired/absent-name sources can be excluded only with the specified evidence and reason. Possibly relevant malformed evidence, unknown endpoint bindings and applicable adverse findings cannot disappear. All relevant targets must agree; relevant contradiction or ambiguity blocks the clean aggregate in every order. Duplicate sources add no weight, and repeated IDs with conflicting bytes are diagnosed.

### D3: exact corroboration witness

[ALG] The rule binds the endpoint, requested name, target identity/release scope, event/property, evidence digest, verifier/rule version and assessed scope. The full neither/left/right/both-side matrix is required, including every mismatch and conflict case. A `third_party_record` or `independently_corroborated` label is not proof, and there is no strongest/weakest evidence-class ranking.

`SYN-MODEL-WITNESS-1` exercises those necessary conditions only in the pinned fixture domain. No admitted live witness rule is enabled, so production `Q_identity` remains withheld. [DECISION-20260814-0001](../../self_model/decisions/DECISION-20260814-0001.json) remains unchanged historical authority: changed aggregation/gating semantics require an explicit governed successor/admission, not a silent rewrite of that decision.

## 5. 3B: fixed synthetic tool and human profiles

[ALG] The exact deterministic rules and record fields are in the r2 rules/schema/examples. These profiles do not enroll real tools or people.

| Profile | Frozen fixture chain | Refusals and identity boundary |
| --- | --- | --- |
| `SYN-TOOL-1` | Pinned namespace/issuer → tool/release identity → complete artifact mapping → event execution binding, with explicit aliases, validity and revocation | Equal bytes do not establish equal ToolIdentity; different builds/configuration do not establish identity inequality. Missing execution disclosure can block standing without erasing an otherwise established identity relation. |
| `SYN-HUMAN-1` | Pinned fictional-principal namespace and uniqueness/alias rules → reference/account/key binding → separate event-to-acting-principal binding, with validity and revocation | A principal represents the fixture individual, not a role/account label. Shared accounts, reassignment, conflicting aliases or missing actor linkage cannot be resolved by a flag. Delegation does not rename the acting principal. |

Issuer/witness admissibility and event-time/revocation behavior are computed from the anchored fixture evidence under the named rule. A payload saying `established` is not evidence. Model catalog evidence classes are not copied into either profile. Production tool/human registries remain empty; no credentials, identity documents, new enrollment registry or writer–PI separation is supplied.

## 6. 3C, consumer compatibility and rollback

[ALG] The [consumer matrix](r2/CONSUMER-COMPATIBILITY.md) freezes the integration boundary before implementation. 3A already protects resolver/equivalence routes; 3C cannot postpone that protection while an old entry point continues permitting.

- Existing `resolve_identity` and `equivalence` calls without the required shared context refuse through the specified typed path.
- Full-context calls delegate to the complete governed pipeline; none may skip endpoint, source or witness validation.
- Historical IdentityResolution annotations remain history-only. Reading one does not create current qualification.
- `blocks_adjudication` is **true unconditionally in r2**, including synthetic evaluations. Direct construction with apparent model evidence labels cannot bypass that rule.
- Synthetic identity-condition results cannot be passed to a legacy consumer as live permission.

3C checks exact VerificationRun/property/version/input/environment/result linkage and substantiated conflict/coverage findings. It neither implements full traversal nor trusts a caller's ancestry-complete flag. Current C10 producer semantics remain ModelIdentity; extending them is a separate normative question. C10 remains unresolved in both domains: receiving-decision consequence and attempted reliance are not bound, and no live review-acceptance rule exists. Exact-run/property mismatches and shared-ancestry claims are diagnostics, not proof of a C10 violation. `Q_C3_C10` remains violated or unresolved; no canonical lineage enum or lineage upgrade is introduced.

**Safe rollback disables the affected route and retains a refusal shim.** It never restores the previous R13/R14 permitting behavior, first-success resolver or unchecked adapter. A reviewable revert is allowed only while that refusal boundary remains intact. Retain faulty results, adverse evidence, corrections and reviews; never delete or reclassify historical evidence to obtain a passing result.

## 7. Falsification and review gates

[ALG] Extend the existing [falsification families](FALSIFICATION-MATRIX.md), with explicit positive and negative oracles. All 31 existing rows remain verbatim, with 17 additions for 48 planned families. Family counts are not a success metric. r1 executed probes remain unchanged and do not demonstrate the proposed corrections.

Before relying on an admitted increment, its checks must cover:

1. Endpoint/capture/digest/target/release failures and valid controls; null/unsupported scope, invalid intervals, configured freshness and event/retrospective timing.
2. Source omission, caller scope narrowing, changed anchors and forged completeness; valid inapplicable-source controls and order/duplicate/argument-swap invariants.
3. The complete both-side witness matrix and exact-binding mismatches, with relevant conflicts retained despite apparently corroborating labels.
4. Synthetic namespace/issuer/release and principal/actor/time/revocation cases, and attempts to promote fixture output into production.
5. Every public/legacy consumer, direct Boolean-adapter construction, typed error handling and safe rollback.
6. Direct/equivalent C3 conflict precedence, incomplete ancestry, exact C10 run/property mismatch and the absence of any positive combined constraint path.
7. Historical byte preservation and scoped integration/index verification.

For each relied-on guard: retain a passing baseline and then the intended assertion failure under its deliberate broken variant. Collection/import/setup/teardown/runtime/environment errors and timeouts are not caught mutations. Schema conformance and synthetic success do not establish real identity, completeness or independence.

The implementer must not be the sole verifier/adjudicator. Technical review and an explicit PI admission remain separate. A successful implementation review later requires its own completion decision; this r2 review is not that decision.

## 8. D6/D7 and readiness consequences

[OPEN] D6's separate documented proposal is **cross-kind unresolved in both orders**. A tool proposed as adjudicator with model or human evidence ancestry cannot clear those comparisons just because its kind differs. A wrapper cannot remove a material subordinate executor or shared evidence ancestry.

[OPEN] D7's separate documented proposal is **superclass deferred**. Existing kind-tagged contracts do not demonstrate a need for a new identity hierarchy. Any resolving cross-kind rule or superclass requires a later explicit normative decision; this PR issues none.

GAP-0008 composition/traversal/coverage, later live evidence rules and later cross-kind semantics remain dependencies for positive qualification. GAP-0005, GAP-0008 and GAP-0010 remain open; writer–PI identity separation remains unresolved. Completion of 3A, 3B or 3C does not establish Step 4/5 readiness. **Step 5 is not ready.**

Current state: Step 1 scope records complete; Step 2 observed-execution slice complete; Step 3 r2 proposed/preparation only; authority mechanism not activated; bootstrap not ready. Next action: review this exact r2, then consider a separately recorded bounded 3A admission. No implementation begins in this revision.
