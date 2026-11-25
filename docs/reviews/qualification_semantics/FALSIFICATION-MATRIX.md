# Step 3 falsification matrix — proposed r2

[ALG] **48 planned scenario families; not an executed mutation score.**
F01–F13 preserve the [original preparation matrix](STEP-3-PREPARATION.md).
F14–F31 add the R13/R14 and multi-source cases. Those 31 rows are preserved;
F32–F48 add the r2 review obligations. A family can contain multiple
parameterized tests; the family count is not a pytest count.

The oracle is the [proposed contract](EQUIVALENCE-EVIDENCE-CONTRACT-DRAFT.md),
which requires separate review/admission. Existing-runtime observations are
reported separately in [SOURCE-REVIEW-BASELINE.md](SOURCE-REVIEW-BASELINE.md).
The r2 rules below refine the retained r1 oracles: positive tool/human bindings
are synthetic only; unsupported endpoint aliases remain unresolved; C3/C10 have
no positive value; production Q_identity is always withheld. The preserved
rows do not admit a live profile or override the r2 boundary.

## Original 13 families, retained and made explicit

| ID | Fixture / counterexample | Required future result |
| --- | --- | --- |
| F01 | Two model aliases resolve to one identity, including both-side valid corroboration | equivalent; identity condition blocked; names/endpoints do not create distinction |
| F02 | Distinct model mappings; either side self-asserted/unassessed | Preserve the asserted relation; withhold the corroborated identity condition in both argument orders |
| F03 | Missing, stale, conflicting or inapplicable identity evidence; known omitted potentially relevant source | Explicit non-resolution/exclusion; unresolved source coverage withholds a clean aggregate and identity condition; no current-for-event substitution or label fallback |
| F04 | Same established ToolIdentity + version, including command aliases, platform builds and differing config | equivalent; bytes/config alone do not redefine identity; missing disclosure blocks standing separately |
| F05 | Established distinct tool identity/version; shared source/verifier ancestry | non_equivalent only under the namespace/version rule; no independence inference |
| F06 | Missing version; reused version label with altered artifact; unresolved release/execution alias; hidden model wrapper | Unresolved binding where identity is unestablished; no deterministic-standing or cross-kind shortcut |
| F07 | Same established human principal across accounts/rotated keys/role labels | equivalent; preserve alias and event-actor evidence |
| F08 | Different principal strings without binding; shared account/key; same string in different namespaces; unbound signing key | unresolved; account ownership or a signature alone cannot establish distinct event actors |
| F09 | Three cross-kind pairs, swapped and wrapped | unresolved under current/proposed conservative rule; no distinction from kind tags |
| F10 | Same capture set permuted, agreeing and conflicting | Stable relation, findings and witness sets; no first-match governing outcome |
| F11 | Empty ancestry path with missing input/output/derivation/subordinate/inherited-state coverage | C3/C5 qualification unresolved; known equivalent/direct conflict still refuses |
| F12 | Output producer shares ancestry with verifier code/schema/tests/configuration | Self-authored standing scoped to the run/property; absence of ancestry evidence cannot establish independence |
| F13 | Review covers wrong version/inputs/environment/result or unresolved reviewer dimensions | No review-based lineage promotion or high-consequence clearance |

## R13/R14 and aggregate extensions

| ID | Fixture / counterexample | Required future result | Baseline coverage |
| --- | --- | --- | --- |
| F14 | Same requested name at two endpoints maps to different identities | Other endpoint's snapshot cannot resolve this invocation | R13 executed |
| F15 | Unknown endpoint spelling or missing endpoint definition/binding | unresolved; no nonempty-string fallback | Unknown spelling executed; missing definition is proposed |
| F16 | Two endpoint definitions share a spelling or alias binding conflicts | unresolved until unique event-time binding established | Proposed |
| F17 | Explicit admitted endpoint alias inside/outside validity scope | Match only inside the supported scope; no automatic normalization | Proposed |
| F18 | Otherwise valid relevant sources plus conflicting source from known other endpoint | Exclude wrong endpoint with reason; same result in all orders | Cross-endpoint order sensitivity executed |
| F19 | Contradicted/conflicting source expired, after-event or outside assertion interval | Proven temporal exclusion does not veto valid event-time support | Contradicted variants executed |
| F20 | Observation/freshness/assertion boundary equality, ±1 microsecond and UTC-offset equivalents | Inclusive boundary rule consistent; retain exact policy/window | Proposed |
| F21 | Contradicted capture has no requested-name assertion | No global veto; record inapplicability | Executed |
| F22 | Applicable contradicted capture plus favorable source, same target and alternative target variants | unresolved in every order; capture-wide adverse evidence cannot disappear | Alternative-target variant: six permutations executed; same-target variant proposed |
| F23 | Applicable within-snapshot ambiguity plus clean source | unresolved in every order; preserve competing targets | Six permutations executed |
| F24 | Cross-source disagreement: provider/provider, provider/corroborated, corroborated/corroborated | unresolved without an admitted conflict-resolution rule; no ranking/majority/newest winner | Corroborated-label conflict executed |
| F25 | Same mapping from weak and corroborated sources | Stable asserted identity; preserve class set; identity condition requires an actual scoped corroboration witness | Enum-label order dependence executed; witness verification proposed |
| F26 | Exact evidence duplication and source-list permutations | Idempotent result; no extra independent-source weight | Proposed |
| F27 | Same record ID with different retained bytes | Explicit conflict; ID-only deduplication forbidden | Proposed |
| F28 | Potentially relevant malformed snapshot or capture-linkage mismatch placed before/after success | Stable typed refusal/unresolved; no early success or order-dependent exception; infrastructure error is not a caught mutation | Both variants executed |
| F29 | Unknown scope, uninterpreted superseded_by or conflicting supersession | Cannot be silently excluded or superseded; unresolved if material | Proposed |
| F30 | Later corroboration/revocation assessed against earlier invocation | Append retrospective assessment; preserve event-time inputs/status; do not backdate evidence availability | Proposed |
| F31 | Corroboration enum/channel authentication without actual property evidence | Cannot establish the corroborated identity condition, full C3 clearance or authorization | Baseline uses synthetic enum labels; proposed evidence rule unimplemented |

[ALG] Baseline coverage names actual current-code observations, not successful
future-contract tests. In particular, the synthetic corroborated labels in
F14/F22–F25/F28 exercise the current Boolean helper; they are not independently
corroborated identity evidence.

## r2 additions and refined oracles

[ALG] The exact oracle is [DETERMINISTIC-RULES.md](r2/DETERMINISTIC-RULES.md)
plus the [consumer matrix](r2/CONSUMER-COMPATIBILITY.md). The new executed
baseline is [R2-BASELINE-OBSERVATIONS.md](r2/R2-BASELINE-OBSERVATIONS.md).
Its 189 operation observations are not 189 successful corrected-behavior tests.

| ID | Fixture / counterexample | Required future result | Current-baseline coverage |
| --- | --- | --- | --- |
| F32 | capture_success=false; string false; unsuccessful source with favorable payload; unsuccessful source proven irrelevant | False supplies no positive mapping/name-absence evidence; potentially relevant failure remains unresolved. Wrong type is invalid. Proven irrelevant failure has a named exclusion. | Failed capture acceptance and wrong-type rejection executed |
| F33 | resolves_to targets true, false, 1, 0, 7, 1.5, empty string, arbitrary string, null, list; true/1 collision and mixed int/string ambiguity | Type/domain checks precede equality, sets and sorting; no truthiness/coercion; invalid target cannot resolve, annotate, clear an adapter or raise an uncontrolled exception | Scalar propagation, truthiness differences and mixed-type exception executed |
| F34 | Valid MID; dangling MID; existing wrong-kind EID; ID-preserving differing full bytes; identity-field change with stale ID | Recompute named schema ID, check kind, dereference pinned target and hash full bytes. Missing target refuses; wrong kind/invalid ID/byte conflict has its precise typed reason. Exact duplicate bytes are a control. | Target-domain failures executed; direct MID-schema controls executed; old resolver has no target-registry input |
| F35 | MID release_identity=unknown versus supported nonempty release with exact witness | Unknown release may preserve a clean catalog-record relation but never Q_identity; stronger release finding requires its scoped witness | Unknown release accepted by baseline; 132/132 retained MID records use unknown |
| F36 | scope=null; unsupported non-null string; object scope; expired unsupported scope | Null has the frozen snapshot/name/property/interval meaning; unsupported string cannot act as wildcard. Wrong shape is invalid; proven time exclusion is distinct from unknown scope. | Null/string/object behaviors executed |
| F37 | Reversed interval; zero-length interval; missing/invalid timestamp; equal UTC instants at distinct offsets | Reversed interval is invalid; valid equal bounds are inclusive; malformed/naive times rejected; normalized instant comparison deterministic | Reversed/zero-length/malformed controls executed |
| F38 | Capture after event, capture before observation, availability after cutoff, later import of earlier available bytes, absent availability evidence, changed fixture availability row | Chronology error is invalid; valid but after-bound evidence is excluded; unproved availability unresolved. Retrospective cutoff does not back-project a later observation. Production availability profile remains absent. | Baseline capture/event chronology gaps and future-observation control executed; new availability rule not implemented |
| F39 | Run identical R13/R14/failed-capture/witness fixtures through every public resolver, equivalence, annotation, graph read and direct Boolean constructor | Same context checks on all paths; old no-context path refuses; legacy resolver never positively projects in r2; blocks_adjudication always true; historical annotations do not establish qualification | Annotation and direct-constructor acceptance/bypass surfaces executed |
| F40 | Same assessment ID with different bytes; changed reason/outcome under same legacy RES ID; interrupted write; identical replay | New content-bound assessment storage refuses different bytes and writes atomically; identical replay idempotent. Old annotations retained as history; no silent overwrite or promotion. General catalog-writer redesign is outside this slice. | Legacy RES/CAP overwrite and reason-ID collision executed |
| F41 | Disable new resolver/profile; revert body while consumer remains active; unsupported schema/context; exception path | Refusal shim or disabled consumer remains active. No rollback may reinstate first-success R13/R14 or unchecked Boolean permission. | Proposed |
| F42 | Remove a relevant source, root, known omission or unavailable unknown-digest declaration; replace pinned commit/tree/selector/cutoff; forge complete=true; genuine out-of-scope control | Consumer anchor and deterministic enumeration reject narrowing. Unknown bytes remain explicit omissions. Supplied agreement cannot become clean R_identity; genuine exclusion carries its reason. | Proposed |
| F43 | All 3×3 valid/missing/mismatched witness pairs; every endpoint/name/target/event/property/evidence/verifier/rule/verification/scope mismatch; all 4×4 legacy evidence-class pairs | Only two exact accepted synthetic witnesses plus clean non-equivalent R and coverage can satisfy synthetic Q_identity; any relevant conflict, unknown release or mismatch withholds it. Labels alone never substitute. | Baseline label-only path executed; new witness contract not implemented |
| F44 | Perfect asserted model mapping or fabricated live endpoint/availability/witness/tool/human/ancestry profile | All six production profile registries remain empty and production Q_identity withheld; caller profile registration rejected | Proposed |
| F45 | Tool issuer/release/alias/execution mismatch; human person/principal non-bijection, role/account/key alias, missing actor; revocation at event; forged test_mode or synthetic result replay | Exact harness-pinned fixture chain and revocation rules; no caller-selected trust anchor, namespace or domain. Synthetic success cannot create real binding. Valid same/distinct fixtures remain controls. | Proposed |
| F46 | Valid pinned synthetic direct/equivalent C3 conflict plus incomplete unrelated ancestry; opaque/unbound edge references; ancestor proof depends on current fixture/context or forms a reference cycle; no conflict with incomplete coverage | Accepted negative-conflict fixture yields violated despite other unknowns; a digest alone never establishes direction. Cyclic/current-anchor proof dependencies are invalid. Prior assessment context is provenance only; recompute the exact pair under current context. Unsupported/production edge evidence and absent conflict remain unresolved; no positive C3 output. | Proposed |
| F47 | Exact C10 run versus wrong run/property/verifier/version/input/environment/result/producer/review; known shared ancestry versus merely unknown ancestry; no receiving-decision consequence context | Retain exact mismatch/shared/unknown diagnostics; no lineage upgrade. C10 stays unresolved in r2 because high-consequence reliance and accepted live review conditions are outside its input/accepted-rule scope. | Proposed |
| F48 | Tool adjudicator with model/human ancestor, model wrapper, swapped cross-kind pairs; attempt Step 5 activation from synthetic Q_identity | Cross-kind unresolved; material influence cannot be erased by wrapper/kind. Q_C3_C10 cannot become positive; Step 5 readiness is not established. | Proposed |

[ALG] F12/F13's retained r1 wording does not authorize an affirmative lineage
classification from unknown ancestry. F17's hypothetical admitted alias is
outside r2, whose alias registry is empty. F32–F48 specify the narrower r2
oracles. The schema corpus checks **syntax**, not any of these behavior families.

## Common execution requirements for the future admitted slice

- Inspect every selected test's successful unmodified baseline before mutation.
- Keep exact test/node identifiers, assertion phase, stdout/stderr and result.
- Permute the complete evidence sets and swap left/right arguments; compare
  normalized reasons and provenance, not only the relation string.
- Include positive controls: exact matching endpoint; clean applicable mapping;
  synthetic same/different tool bindings; synthetic same/distinct principal
  actors; valid fixture alias interval. A universal-refusal implementation fails
  these synthetic relation/identity controls; the deliberate production gate
  refusal and non-positive C3/C10 boundary are required outcomes.
- Do not count collection/selection/usage/internal errors, process launch
  failures or timeout as successful falsification.
- Preserve synthetic fixture labels. Actual independence/authorization claims
  need separate retained evidence and their own governing decision.
