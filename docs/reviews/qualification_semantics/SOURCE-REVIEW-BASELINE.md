# Step 3 source review and executed baseline

[NUM] Baseline source commit: **5515f55894b10ad70c321340257f67a960dcc382**.
Observation date: 2026-11-25. This file separates current-code observations from
the unimplemented [proposed contract](EQUIVALENCE-EVIDENCE-CONTRACT-DRAFT.md).

[ALG] R13 and R14 arrived as source-review findings. They are now reproduced
with isolated synthetic fixtures. Both defects remain open: this preparation
changes no production resolver, equivalence helper, schema or existing test.

## Method and retained artifacts

The [probe](probes/probe_r13_r14.py) verifies the exact baseline HEAD and compares
11 inspected source files with their committed bytes before importing them.
It disables bytecode writes, performs no provider call, and requires its output
to be outside the inspected repository. Complete fixtures, input ordering,
returned results, exceptions and source hashes are retained.

| Observation | Python | Result |
| --- | --- | --- |
| [Baseline](probes/r13_r14_baseline.json) | 3.13.5 | 88 observations; 15 schema-valid synthetic snapshot/capture pairs plus two explicitly invalid pairs |
| [Reproduction](probes/r13_r14_reproduction.json) | 3.12.14 | Same 88 observations, fixtures and source hashes |

Parsed JSON differs **only** in python_version. This is same-provider
implementation-team reproduction; it establishes no independent adjudication,
authenticated CI origin or C10 lineage qualification.

| Artifact | SHA-256 |
| --- | --- |
| probe_r13_r14.py | 5c1be890715584481898bd4df7cecb33c50b193da4b0c1da9398caa769e11bf7 |
| r13_r14_baseline.json | 7f8640d7fa4ccf27865d667a7c7c292aec0b8c341f02193f91fb3f92c7c9a6e1 |
| r13_r14_reproduction.json | 3e05154e11e5b08280aa8ff2af7869ce2a17472fc7812c917b982797f6d399b7 |

The fixtures' independently_corroborated values are **synthetic enum inputs**,
not actual corroboration. A reported blocks_adjudication=False is only the
current helper's Boolean output. It supplies neither the missing ancestry nor
actual adjudication authorization. The 88 observations are not 88 mutations or
a claim that a future guard passed.

## Observed results

| Case | Actual unchanged-baseline behavior |
| --- | --- |
| Exact matching endpoint control | Resolves to the expected synthetic identity |
| R13: another known endpoint or an unbound endpoint | Resolves using the original endpoint's snapshot |
| R13 with synthetic corroborated labels on both sides | non_equivalent; helper Boolean false |
| Relevant contradicted capture alone | unresolved / contradicted_evidence |
| Relevant ambiguous snapshot alone | unresolved / ambiguous_assertions |
| R14: either adverse source combined with favorable sources | In 6/6 permutations for each case, non_equivalent and helper Boolean false; the adverse source is skipped |
| Applicable corroborated-label sources disagree on identity | 3/6 orders yield equivalent/block; 3/6 yield non_equivalent/Boolean false |
| Agreeing self-asserted and corroborated-label sources | Same identity; 3/6 orders block and 3/6 return Boolean false |
| Conflicting source from another endpoint | Relation changes with source order, 3/6 versus 3/6 |
| Contradicted source expired, after-event, wrong-endpoint, wrong-name or outside assertion interval | Each single-source call reports contradicted_evidence before establishing relevance; aggregation skips it in all six orders per variant |
| Capture/snapshot linkage mismatch | Single-source ResolutionError; aggregation skips it in 6/6 orders |
| Malformed snapshot | CatalogRecordError in 4/6 orders, early successful Boolean false in 2/6 |

The relevant-adverse cases require preservation. The irrelevant-adverse cases
are negative controls: simply propagating every current contradicted_evidence
reason as a global veto would introduce a different defect.

## Source interpretation

R13: [catalog_resolution.py](../../../ai_lab/providers/catalog_resolution.py)
requires a nonempty invocation endpoint but does not bind it to the snapshot's
service_endpoint_id when selecting assertions. Retained invocation spellings are
openai.responses and anthropic.messages; endpoint records resolve those
spellings through EID-4f3c9d6be930ec02 and EID-beff998d7cb8945f respectively.
The required check is a justified binding, not direct spelling-to-EID equality.

R14: [executor_equivalence.py](../../../ai_lab/providers/executor_equivalence.py)
returns the first successful resolution, skips ResolutionError and retains only
a last non-resolution reason. The underlying resolver's contradicted check
precedes time and assertion filtering. The proposed replacement therefore
requires applicability classification before complete conflict-preserving
aggregation.

The [existing decision](../../self_model/decisions/DECISION-20260814-0001.json)
already records first-match order dependence and requires governed multi-capture
semantics before corroborating sources are relied upon. This baseline adds
endpoint substitution, skipped adverse evidence and validation-order behavior
without claiming that a new semantic rule is already admitted.

## Repository inventory at the baseline

[NUM] Direct file reads found:

| Item | Count / state |
| --- | --- |
| InvocationRecords | 218; all kind=model and capture identity state=unresolved |
| Invocation endpoints | 109 openai.responses; 109 anthropic.messages |
| Retained catalog captures | 2; both provider_self_report / self_asserted |
| Tool/human invocations | 0 |
| Existing PLAN records | 26 completed + 1 withdrawn; no open PLAN before this draft |
| Existing VERIFY records | 47 |
| GAP-0005 / GAP-0008 / GAP-0010 | open |

Tool/human examples in the proposal are therefore synthetic contracts, not
newly discovered live binding evidence. The proposed PLAN adds one open
proposed record; it does not change the 27 historical PLAN records.

## Reproduction

From a checkout containing this draft, create a separate detached baseline
worktree, then run the retained script against that exact source revision.
The output path must be outside that baseline checkout:

    git worktree add --detach /tmp/ai-lab-r13-r14-baseline 5515f55894b10ad70c321340257f67a960dcc382
    python -B docs/reviews/qualification_semantics/probes/probe_r13_r14.py --repo /tmp/ai-lab-r13-r14-baseline --output /tmp/ai-lab-r13-r14-result.json

The report records the interpreter version used. Compare fixtures, source hashes
and observations; a different interpreter version intentionally changes the
report's metadata.

Preparation-record validation is retained in
[PREPARATION-VALIDATION.json](PREPARATION-VALIDATION.json), with
[the existing-suite output](step3_preparation_pytest.txt). Those checks validate
this preparation workspace and unchanged existing implementation; the 31 future
scenario families in [FALSIFICATION-MATRIX.md](FALSIFICATION-MATRIX.md) remain
prospective. No new canonical VERIFY or lineage assertion is issued here.
