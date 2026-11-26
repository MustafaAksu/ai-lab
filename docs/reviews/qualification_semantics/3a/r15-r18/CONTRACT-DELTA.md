# Step 3A corrections R15–R18

[ALG] Scope: [review 6070899882](https://github.com/MustafaAksu/ai-lab/pull/5#pullrequestreview-6070899882)
on `877b94922fc9acf882930cd275d2889038cada33`, under the existing
[WARR-20261126-0001](../../../../self_model/warrants/WARR-20261126-0001.json)
A1–A4. These are implementation corrections within admitted 3A. No new PLAN,
admission warrant, trust profile or completion decision is introduced.

The prior [implementation contract](../IMPLEMENTATION.md),
[review package](../REVIEW-PACKAGE.md) and reports retain their original
subjects. This document specifies the corrections; it does not retrospectively
upgrade the prior implementation or its test coverage. The frozen r2 schema is
unchanged.

## R15 — Raw Git object pinning

[ALG] Every Git invocation in `qualification_records.load_git_catalog()` now
uses `git --no-replace-objects`. Commit, tree enumeration and batch object reads
therefore refer to the raw requested objects even when local commit, tree or
blob replacement refs exist. Neither a returned commit spelling nor valid
replacement blob hashes are accepted as a substitute for that binding.

The loader also checks decoded object identities, tree-entry structure and
batch framing. Missing/malformed headers, non-decimal or invalid lengths,
truncated bodies, missing delimiters, wrong IDs/kinds, hash mismatch and trailing
bytes produce `QualificationError` rather than uncontrolled parsing exceptions.

Tests in [test_qualification_r15_r17.py](../../../../../tests/test_qualification_r15_r17.py)
use a real repository: original A contains an adverse source; replacement B
removes it. A's true inventory retains the adverse source under replacement;
B's narrowed inventory claiming A is refused. Separate controls cover tree and
blob replacement. Git process failure and malformed batch output are also
exercised. These checks apply to the qualification loader; the historical VERIFY
writer and its documented observation limits are not changed by this correction.

## R16 — Witness evidence must predate assessment

[ALG] For the exact same source chain accepted by a witness, the evaluator now
requires an accepted pinned availability proof satisfying:

\[
t_{capture}\le t_{source\ available}\le t_{assessed}
\le t_{witness\ available}\le t_{bound}.
\]

The source availability proof still binds that source's exact capture, snapshot
and payload. The witness still binds the applicable capture–snapshot–payload–MID
chain, property, verification premise, verifier/rule and scope. An early proof
for another source with the same MID cannot qualify a later witnessed chain.
Both the assessment-time source check and the event/knowledge-bound checks must
pass. Equality is allowed; timestamps are compared as UTC instants.

Failure withholds `Q_identity`; a valid catalog-record `R_identity` diagnostic
may remain. The accepted source and witness availability evidence, the five
times and the exact payload/verification digests are retained in existing
schema-compatible reasons. Choice among multiple already acceptable proofs is
deterministic: earliest accepted time, then canonical reference bytes. This is
a diagnostic selection among valid proofs, not an evidence-strength ranking.

[test_qualification_r16.py](../../../../../tests/test_qualification_r16.py)
tests assessment before capture, assessment before source availability,
same-MID alternative-source borrowing, inclusive boundaries, equivalent offset
instants, retrospective bounds, retained proof references and permutation.

## R17 — Both publication destinations are contained

[ALG] `write_assessment()` validates both CAS and `by-id` paths before reading
an existing display entry or publishing either object. Their real parent paths
must remain under the resolved designated store and outside the production
checkout. Every descendant path component is checked for symlinks, including
final-file links; even a link whose current target is inside the store is
refused. A resolution failure or loop also refuses.

The tests invoke the complete writer with an actual valid synthetic assessment.
They cover redirected `synthetic`, CAS root, hash shard, `by-id`, and both leaf
paths, with targets inside an isolated checkout, outside the store, and inside
the store. Rejected cases must leave the observed checkout/store/destination
path states unchanged. Real-directory controls preserve idempotent replay,
collision refusal and atomic complete-file publication.

[OPEN] This is containment validation in a stable filesystem namespace. It is
not a namespace sandbox against a malicious concurrent OS actor replacing path
components between checks and publication, nor against arbitrary in-process
Python. Those stronger guarantees were not requested or added. Existing
multi-object publication semantics remain: an unrelated later I/O failure can
leave a complete unindexed CAS object, never an accepted partial assessment.

## R18 — Explicit schema-bootstrap exception contract

[ALG] Both public evaluator entry points require the pinned schema before
processing Query. A schema bootstrap failure produces **no AssessmentResult**.
It raises `qualification_records.QualificationBootstrapError(RuntimeError)`,
separate from `QualificationError`, with bounded `code` and `detail` attributes.
Constructing or formatting this exception performs no schema validation.

| Bootstrap code | Trigger |
| --- | --- |
| `QUALIFICATION_SCHEMA_UNAVAILABLE` | Schema bytes cannot be read |
| `QUALIFICATION_SCHEMA_DIGEST_MISMATCH` | Retained bytes differ from the frozen SHA-256 |
| `QUALIFICATION_SCHEMA_INVALID` | Decoding or metaschema validation cannot establish the schema |

These codes are not new r2 `Reason` values or historical v1 RES vocabulary.
They cannot be persisted as an accepted assessment. Ordinary invalid input,
after successful bootstrap, retains the existing typed invalid-result contract.
Legacy adapters catch the bootstrap exception and remain blocking without a
positive projection or assessment reference.

```python
try:
    result = evaluate_synthetic_r2(query, anchor=anchor)
except QualificationBootstrapError as failure:
    # No assessment exists. Record a bootstrap diagnostic if desired;
    # do not synthesize a passing or schema-valid assessment.
    handle_bootstrap_failure(failure.code, failure.detail)
```

A successfully verified schema is cached as the process's pinned in-memory
snapshot. Removing or changing its file afterwards does not silently replace
that snapshot. A new process or cleared cache must bootstrap again; failed
loads are not cached. This contract concerns schema loading after module import,
not arbitrary missing Python dependencies or hostile interpreter mutation.

[test_qualification_r18.py](../../../../../tests/test_qualification_r18.py)
tests missing/changed schema on both entry points, malformed Query precedence,
single-load error construction, decoding/metaschema failures, legacy refusal,
load-once behavior and the normal invalid-result control. Faults are confined to
temporary schema paths; the frozen repository schema is not edited.

## Evidence and standing

[ALG] The new
[falsify_qualification_3a_review.py](../../../../../scripts/falsify_qualification_3a_review.py)
imports the historical 20-guard manifest without modifying it and adds eight
R15–R18 guard mutations. The existing strict classifier is unchanged: passing
baseline, identical selected test IDs and ordinary call-phase assertion failure
are required. It retains both groups separately. Runtime exceptions, collection,
setup, environment failures and timeout do not count as catches. Exact-source
execution totals belong to the new validation report, not this contract.

[OPEN] Production acceptance remains unavailable; `blocks_adjudication=True`.
`C3=C10=Q_C3_C10=unresolved` in every domain. 3B/3C remain NOT_ADMITTED;
PLAN completion and PR merge remain pending. Origin stays `unverified`, lineage
`self_authored_unreviewed`; same-provider internal checks do not establish
independent adjudication or writer–PI separation. No GAP or capability standing
is promoted.
