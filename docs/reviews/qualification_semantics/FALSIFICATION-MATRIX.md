# Step 3 falsification matrix — proposed r1

[ALG] **31 planned scenario families; not an executed mutation score.**
F01–F13 preserve the [original preparation matrix](STEP-3-PREPARATION.md).
F14–F31 add the R13/R14 and multi-source cases. A family can contain multiple
parameterized tests; the family count is not a pytest count.

The oracle is the [proposed contract](EQUIVALENCE-EVIDENCE-CONTRACT-DRAFT.md),
which requires separate review/admission. Existing-runtime observations are
reported separately in [SOURCE-REVIEW-BASELINE.md](SOURCE-REVIEW-BASELINE.md).

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

## Common execution requirements for the future admitted slice

- Inspect every selected test's successful unmodified baseline before mutation.
- Keep exact test/node identifiers, assertion phase, stdout/stderr and result.
- Permute the complete evidence sets and swap left/right arguments; compare
  normalized reasons and provenance, not only the relation string.
- Include positive controls: exact matching endpoint; clean applicable mapping;
  established same/different tool bindings; established same/distinct principal
  actors; valid alias interval. A universal-refusal implementation fails.
- Do not count collection/selection/usage/internal errors, process launch
  failures or timeout as successful falsification.
- Preserve synthetic fixture labels. Actual independence/authorization claims
  need separate retained evidence and their own governing decision.
