# Step 3: qualification-semantics preparation

## Status and context

[ALG] **Preparation draft; no canonical PLAN, ontology amendment or admission.**
Prepared by ChatGPT after the PI accepted completion package
`86f08b3f9f3192bfe576d5be207752e446af5941` for PLAN-20261124-0001 and authorized
preparation of the next programme step. That completion concerns observed
execution; it does not activate delegated adjudication. Formal implementation
requires its own plan, review and admission.

[ALG] Completion context: issued
[WARR-20261125-0001](../../self_model/warrants/WARR-20261125-0001.json) and
[PI completion record](../verify_v2/completion/PI-COMPLETION-RECORD.md).
Their preparation permission does not admit this draft's future implementation.

[ALG] Scope follows the three distinct items in
[GAP-0005, recommended_first_slice](../../self_model/gaps/GAP-0005.json).
Plan admission remains **high** under
[ABS-0004 §8](../../abstractions/ABS-0004-invocation-authorization-ontology.md).
No consequence reclassification, authority mechanism, C7 identity binding,
policy activation or lineage-status promotion is proposed here.

## Current software and evidence

| Item | Current support and limitation |
| --- | --- |
| Model/model relation | ModelIdentity resolution equality/inequality is implemented. Distinct catalog-resolved identities can yield `non_equivalent` while adjudication remains blocked. |
| Model permission | `blocks_adjudication=False` requires `non_equivalent` and `independently_corroborated` evidence on **both** sides. The two retained captures are `provider_self_report` / `self_asserted`; neither establishes that permission. |
| Tool/tool; human/human | The ontology defines tool identity-and-version equality and principal equality. The helper implements neither and returns `unresolved`. |
| Different executor kinds | `unresolved`, basis `no_cross_kind_equivalence_test_defined`; different kind tags do not establish non-equivalence. |
| Multiple applicable captures | `_resolve_one` takes the first resolution. A retained test demonstrates order-dependent permission. An aggregation/conflict rule must be governed and falsified before corroborated captures are relied upon. |
| Ancestry | Two directional edge classes exist; GAP-0008 still lacks their governed composable instance and transitive traversal with applicable-edge coverage. Identity resolution alone cannot establish a C3 or C10 qualification. |
| C3/C10 attestation | ABS-0004 §9 records partial support and no named retained C3/C10 attestation. Defining the records or passing helper tests does not supply a check for an actual adjudication or verification run. |

[ALG] Sources: [equivalence implementation](../../../ai_lab/providers/executor_equivalence.py),
[retained falsifier tests](../../../tests/test_executor_equivalence.py),
[DECISION-20260814-0001](../../self_model/decisions/DECISION-20260814-0001.json),
[GAP-0008](../../self_model/gaps/GAP-0008.json). These describe support inspected
at the accepted package revision; no new test run is asserted here.

## Three separate scope items

### A. Same-kind tool and human equivalence

[ALG] Draft an implementation contract for the tests already stated in
[ABS-0004 C3](../../abstractions/ABS-0004-invocation-authorization-ontology.md):
tool identity **and version** equality; human principal equality. Keep relation,
supporting evidence and permission distinct. Unknown identity/version or an
unestablished reference-to-principal binding must remain `unresolved`.

[OPEN] The input records, admissible binding evidence and permission conditions
for these kinds need review before implementation. This draft supplies **no
human-identity binding rule**: a display name, account, Git author, signature
label or `principal_id` string is not made an attested principal by this document.
Likewise, an executable filename or version label alone does not establish a
ToolIdentity/version binding. The model catalog threshold is not silently reused
as a tool/human evidence schema.

[ALG] Preserve §4.7 disclosure requirements: a tool that invokes a model cannot
gain deterministic standing by hiding that subordinate invocation; material
configuration, dependencies and external interactions remain part of the
evidence question. Replacing a model adjudicator with a tool supplies no
permission through an unresolved comparison.

### B. Cross-kind semantics: governed decision

[OPEN] Decide separately whether, and on what evidence, comparisons of
model/tool, model/human and tool/human can resolve. Specify both argument orders,
composition/wrapper cases and missing-evidence outcomes. Until an applicable rule
is admitted, every such comparison stays `unresolved` and blocks adjudication.
An implementation must not infer `non_equivalent` merely from differing kinds.

### C. ExecutorIdentity superclass: separate necessity decision

[OPEN] Assess whether the existing kind-tagged representation can express the
required evidence and dispatch, or whether a superclass is necessary. State its
benefit, compatibility cost and separation of stable identity from invocation,
session and runtime instance. A superclass decision settles representation only;
it does not define cross-kind equivalence or confer authority. This is the
independent open question in [ABS-0004 §4.7](../../abstractions/ABS-0004-invocation-authorization-ontology.md).

## Evidence conditions to make executable

[ALG] **C3: necessary conditions for clearing this constraint**, not a complete
authorization rule:

1. Name the candidate adjudicating invocation, target and relevant evidence
   ancestors; retain identity-resolution evidence and its event-time scope.
2. Establish usable directional ancestry and coverage for every applicable edge
   class. An empty path result with missing/incomplete edges remains unresolved
   under C12–C14; provider, prompt, session or round equality is not a directional
   edge by itself.
3. Reject direct lineage conflict. Reject equivalent-identity conflict under the
   present rule. Any unresolved relevant comparison blocks. Every claimed
   non-equivalence must be affirmatively established under its admitted kind rule.
4. For models, preserve both-side corroboration and settle the recorded
   multi-capture order/conflict blocker before reliance. No ordinal ranking of
   evidence classes is introduced.

[ALG] **C10: per verification run and named property.** Bind verifier identity
and version, rule/test version, content-addressed inputs, environment and result.
Evaluate the ancestry of the verifier's code, schema, tests and configuration
relative to the producer of the output under test. Established shared ancestry
receives self-authored standing; absent ancestry evidence cannot establish
independent standing. C10 currently names the producing **ModelIdentity**;
generalizing its producer semantics to other kinds would require explicit
governance rather than a silent implementation extension.

[ALG] At high consequence, independently-lineaged verification or qualifying
independent review of the verifier is required. A review-based transition to
`self_authored_with_review` must satisfy **all** §4.17 conditions for the exact
run/property: identified reviewer invocation/executor, no unresolved or
disqualified independence dimension, exact verifier/rule/input/environment/result
coverage, and positive outcome. A linked review, reproduction, PI completion
decision or passing test result alone does not supply these findings. Existing
VERIFY v2 records retain their current statuses; unresolved assessment evidence
does not create a new canonical lineage enum.

[ALG] Sources: [ABS-0004 P2/P5, §§4.14–4.19, C3/C5/C10/C12–C14](../../abstractions/ABS-0004-invocation-authorization-ontology.md),
[GAP-0008 dependency note](../../self_model/gaps/GAP-0008.json).
Provider/name/endpoint/session separation is not independence; a resolved
identity distinction also does not establish independence in the other C5
dimensions. Step-3 preparation can proceed while GAP-0008 is open; a positive
qualification requiring its missing ancestry evidence cannot.

## Falsifier matrix for the future admitted slice

[ALG] These are required cases to review, **not newly executed tests**.

| Case | Required result / refusal boundary |
| --- | --- |
| Two model aliases resolve to one identity | `equivalent`; blocks despite distinct names/endpoints. |
| Distinct resolved models; either side self-asserted/unassessed | Preserve supported relation; permission withheld in both argument orders. |
| Missing, stale, conflicting or inapplicable identity evidence | No silent current-for-event substitution; unresolved or explicit refusal under the governing rule. |
| Same established ToolIdentity and same established version | `equivalent`; no self-adjudication permission. |
| Tool identity or version differs with adequate admitted binding evidence | Apply the identity-and-version relation; do not infer independence or role qualification from inequality. |
| Tool version absent, alias unresolved or version label unbound | `unresolved`; no permission. |
| Same established human principal, including aliases | `equivalent`; different labels do not separate the principal. |
| Claimed distinct humans without admitted binding evidence | `unresolved`; no inference from names, accounts or signatures. |
| All three cross-kind pairs, swapped and wrapped | `unresolved` under current semantics; any later resolving outcome needs the separately admitted rule. |
| Identical capture set in every order; agreeing and contradictory mappings | Order-invariant result under the future governed rule; unresolved conflict cannot clear permission. Current first-match behavior is a blocker, not an accepted target. |
| Negative traversal with a missing applicable edge or hidden session state | Ancestry/independence unresolved; no C3/C10 clearance. |
| C10 producer shares ancestry with verifier code/tests/configuration | Self-authored standing; evaluate the exact run and property, not the verifier author's name alone. |
| Review names the wrong verifier/test version, inputs or run; reviewer identity/lineage unresolved | No review-based lineage upgrade or high-consequence admission. |

[ALG] Retain the existing alias, unknown-name, absent-catalog, asymmetric
corroboration and cross-kind falsifiers. Replace the test pinning first-match
order dependence only after an aggregation rule is admitted; retain the prior
defect as historical evidence. Construct and record counterexamples before
reliance on each new guard.

## Minimum questions for the next review

[OPEN] Review must resolve or explicitly retain these unknowns before a formal
scope is admitted:

1. Which retained evidence and binding rule establish tool identity/version and
   human principal identity, and which per-kind evidence conditions distinguish
   a relation from permission? What remains unresolvable with current evidence?
2. Does each cross-kind pair remain unresolved, or is a specific resolving rule
   proposed with falsifiers? Is any extension of C10's producer semantics needed?
3. Is a superclass necessary independently of question 2, and what fails without it?
4. What order-independent rule handles agreeing, conflicting, superseded and
   event-time catalog assertions without inventing an evidence-class ranking?
5. What exact C3/C10 targets and evidence fields can the first implementation
   evaluate now, and which must explicitly wait for GAP-0008 composition/coverage?

[ALG] The subsequent submission should contain a proposed contract, evidence
inventory, unresolved cases and this falsifier matrix before seeking separate
PLAN admission. The C7 implementer/verifier pair on observed VERIFY records and
writer–PI identity separation remain explicit GAP-0005 work; this preparation
neither completes nor discards them.
