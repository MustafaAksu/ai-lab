# Equivalence evidence contract — proposed r2

[ALG] **PLAN-20261125-0001 remains proposed. This contract is a preparation artifact, not implementation admission.** It revises the proposal reviewed at `8b8e24d133eaa3a585eefa14e76a02a519b73b03` in [review 6064341643](https://github.com/MustafaAksu/ai-lab/pull/5#pullrequestreview-6064341643). Runtime baseline: `5515f55894b10ad70c321340257f67a960dcc382`. Actual drafting executor: ChatGPT, self-declared/unverified; assisting checks are not independent adjudication.

## 1. Contract artifacts and authority

[ALG] The exact candidate version is **ai_lab.qualification.r2/1**. Its closed shapes and evaluation rules are frozen together for review:

| Artifact | Controls |
| --- | --- |
| [ASSESSMENT-SCHEMA.json](r2/ASSESSMENT-SCHEMA.json) | Required fields, types, nullability, closed enums, strict result envelopes and production restrictions |
| [DETERMINISTIC-RULES.md](r2/DETERMINISTIC-RULES.md) | Input integrity, source universe, scope/time, per-kind evaluation, exact witness acceptance and result precedence |
| [CONSUMER-COMPATIBILITY.md](r2/CONSUMER-COMPATIBILITY.md) | Public and legacy paths, annotations, persistence, refusal adapter and safe rollback |
| [SCHEMA-EXAMPLES.json](r2/SCHEMA-EXAMPLES.json) | Positive/negative **shape** examples and strict parsing examples; dummy references do not establish evidence |
| [FALSIFICATION-MATRIX.md](FALSIFICATION-MATRIX.md) | 48 planned behavior families, including the preserved F01–F31; not an executed mutation count |
| [R2-REVIEW-RESPONSE.md](r2/R2-REVIEW-RESPONSE.md) | Review-to-contract traceability and proposal limits |

The schema, rules and consumer matrix are one proposed contract. A contradiction is a review defect, not permission to choose a permissive interpretation. Implementation cannot proceed until the exact revision is separately admitted. Schema conformance alone cannot establish a binding, coverage, witness truth, independence or authority.

[THM] The governing distinction is:

    non-equivalence does not imply independence;
    independence does not imply authorization.

[ALG] [ABS-0004](../../abstractions/ABS-0004-invocation-authorization-ontology.md) and [DECISION-20260814-0001](../../self_model/decisions/DECISION-20260814-0001.json) remain unchanged. r2 proposes stricter aggregation and legacy behavior; it does not silently amend that historical decision. A later governed successor/admission must explicitly authorize any changed semantics. No canonical decision or warrant is issued here.

## 2. Three result axes

| Axis | Values | Candidate meaning |
| --- | --- | --- |
| R_identity | equivalent / non_equivalent / unresolved | Clean relation under the complete consumer-pinned source context and the applicable per-kind rule |
| Q_identity | withheld / conditions_satisfied | Necessary identity-evidence conditions; positive only inside a pinned synthetic fixture, with non-equivalent R_identity and exhausted pinned inventory |
| Q_C3_C10 | violated / unresolved | Combined bounded C3/C10 findings; no positive result in either domain |

C3 and C10 are also retained separately. C3 is violated only under the accepted negative synthetic fixture rule; otherwise unresolved. C10 is always unresolved in r2. **Production Q_identity is always withheld**, and production C3/C10/Q_C3_C10 remain unresolved. A `supplied_relation` diagnostic may describe the supplied assertions without claiming governed coverage; it cannot replace R_identity or a qualification result.

Malformed envelopes return `AssessmentResult.validation_status=invalid`, typed reasons, unresolved relations/constraints and withheld Q_identity. Valid but incomplete evidence returns the appropriate unresolved/withheld findings. Invalid or unknown material cannot be skipped after an early favorable result. No result axis authorizes action.

## 3. D1–D8: frozen choices

| Decision | r2 choice | Deterministic boundary |
| --- | --- | --- |
| D1 endpoint/model validity | Unique exact catalog endpoint mapping; explicit successful capture, valid target dereference, bytes, scope and time checks | No automatic endpoint aliases; no scalar/dangling/wrong-kind target; unknown release cannot clear Q_identity; event availability is a separate evidence obligation |
| D2 complete aggregation | Evaluate every source selected by REPO-CATALOG-ALL-1 and pinned known-source/omission declarations | No first/newest/majority/strongest winner; relevant contradiction, ambiguity, unknown applicability or missing coverage blocks the clean aggregate |
| D3 corroboration | Exact binding/property/evidence/verifier/rule witness under a pinned profile | Model evidence-class labels alone never suffice; full neither/left/right/both matrix; live witness registry empty |
| D4 tool/tool | SYN-TOOL-1 only | Fictional namespace/issuer/release/alias/event-execution chain; no live ToolIdentity binding |
| D5 human/human | SYN-HUMAN-1 only | Bijective fictional person/principal mapping plus separate reference and event-actor binding; no live enrollment |
| D6 cross-kind | unresolved in both orders | Kind inequality is not executor independence; tool adjudication of model/human ancestry cannot clear C3 |
| D7 superclass | deferred | No ExecutorIdentity hierarchy or ontology migration |
| D8 results/compatibility | Separate result axes and protected old entry points | Legacy resolver refuses positive projection, blocks_adjudication always true, no annotation shortcut; rollback preserves refusal |

D6 and D7 are documented semantic proposals, not effective canonical decisions. Their later reconsideration needs separate justification and governance.

## 4. Source universe and time

[ALG] Query does not choose trust roots, freshness, cutoff, profiles or completeness. The consumer independently fixes the Git commit/tree and **REPO-CATALOG-ALL-1**, which inventories every tracked regular file under `docs/catalog/{eid,mid,snap,cap,payloads}/`, plus its pinned known-source and omission declarations. Recompute entries and digests rather than trusting a supplied `complete` field. Known unavailable sources may have an unknown expected ID/digest; that unknown is represented explicitly and cannot be hidden merely because no bytes are available.

Agreement among supplied records does not establish coverage. `pinned_inventory_exhausted` means only that this exact bounded universe was exhausted for the query; it is not knowledge of all possible sources. Missing potentially relevant items remain blocking. Proven out-of-scope or inapplicable items retain reasons without becoming arbitrary vetoes.

The exact temporal checks are in [rules §§4–5](r2/DETERMINISTIC-RULES.md). Validity is inclusive; the consumer fixes a nonnegative freshness window with a 30-day default. Observation, capture, availability and assessment/import timestamps are distinct. Event-time evidence must have become available by the event and knowledge cutoff. Retrospective evidence may be available later, up to its fixed cutoff, but the first slice still requires the catalog observation to precede the original event and satisfy its event-anchored freshness. It does not back-project a newly observed catalog onto an old invocation.

AvailabilityEvidence has its own closed shape. A timestamp claim is not proof: only exact harness-pinned synthetic rows can exercise the availability condition in r2; the production availability profile list is empty. The same separation applies to catalog-declared endpoint mapping versus an established invocation/endpoint binding. Production unknowns remain visible.

## 5. Concrete witness and synthetic binding rules

[ALG] A model witness binds the exact endpoint, name, target MID, event, property, evidence bytes, verifier executor/version, rule version, verification artifact, assessed scope and interval. SYN-MODEL-WITNESS-1 checks a unique exact row in a harness-pinned fictional evidence set. Relevant adverse sources still block despite two valid witnesses. Unknown release, equivalent identity, missing coverage or either missing/mismatched witness withholds Q_identity.

SYN-TOOL-1 uses namespace `fixture:tools`: issuer membership → release/version and artifact mapping → reference alias → exact invocation/artifact/event observation. SYN-HUMAN-1 uses namespace `fixture:human-persons`: one immutable fictional person ↔ one principal → reference alias → exact event actor. Intervals are inclusive except that revocation takes effect at `event >= revoked_at`. Conflicting applicable rows never use a newest-row fallback.

A tool version string, binary digest, human name, account, key, role or `established=true` flag does not complete either chain. Model catalog evidence classes are not applied to tool/human profiles. Production registries for endpoint binding, model witnesses, tool binding, human binding, ancestry and availability are all empty. Entry-point/domain separation prevents a caller from promoting synthetic results into live bindings.

## 6. C3/C10, consumers and persistence

[ALG] C3 checks directional claim/adjudicator evidence and exact ancestor assessments. Only SYN-C3-CONFLICT-1's harness-pinned fictional negative premises can establish a conflict in r2; direct or equivalent conflicts then remain violations despite unrelated missing coverage. Opaque hashed edges, unsupported live evidence and no found conflict over incomplete ancestry remain unresolved. C10 checks the exact verification run/property/version/inputs/environment/result/producer and linked review evidence. Its result stays unresolved: a receiving decision, consequence and attempted reliance are not bound, and no live review acceptance rule exists. Unknown ancestry is neither affirmative independence nor affirmative shared ancestry. No canonical lineage field is written or upgraded.

The bounded slice supplies **no positive ancestry profile**. Even complete synthetic identity evidence cannot produce positive C3, C10 or Q_C3_C10. GAP-0008 remains a structural dependency.

The [consumer matrix](r2/CONSUMER-COMPATIBILITY.md) covers resolve_identity, equivalence, the Boolean adapter, resolution annotations, graph reads and new assessment persistence. Legacy calls cannot bypass strict context checks. Existing records remain historical; a purported newer label cannot overwrite them or become current qualification. New proposed assessments use content-bound, atomic, collision-refusing persistence. General catalog-writer hardening is outside this slice; evaluation reads pinned immutable Git bytes.

Rollback disables the affected route or retains the refusal shim. It must not restore the R13/R14 first-success or unchecked Boolean permitting behavior while any consumer relies on it.

## 7. Delivery and evidence limits

[ALG] Prospective implementation order is **3A D1–D3 → 3B D4–D5 synthetic → 3C D8 bounded checks**, with separate named review/admission gates. Consumer refusal protection is already part of 3A; it cannot wait for 3C. See the [PLAN draft](STEP-3-PLAN-DRAFT.md) and [canonical proposed PLAN](../../self_model/plans/PLAN-20261125-0001.json).

[NUM] [r1 observations](SOURCE-REVIEW-BASELINE.md) and [r2 observations](r2/R2-BASELINE-OBSERVATIONS.md) concern the unchanged baseline implementation. Schema-example validation concerns document shapes. Existing-suite success concerns unchanged runtime plus proposal/index compatibility. None demonstrates the prospective corrections or a completed mutation campaign.

The r1 probe reports, test output and validation report are preserved byte-for-byte at their historical scope; their embedded contract hashes refer to r1, not this revision. New validation is recorded separately. Historical INV/catalog/VERIFY/CAS/PLAN completion/warrant records remain unchanged.

[OPEN] PLAN remains proposed; PR remains draft/open; GAP-0005/0008/0010 remain open; writer–PI separation remains unresolved; origin remains unverified; verifier lineage remains self_authored_unreviewed; autonomy is not enabled. **Step 5 is not ready**, including after a future successful bounded Step 3 implementation.
