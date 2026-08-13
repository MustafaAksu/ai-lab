# ABS-0004 v9.1 Admission Bookkeeping Record

## Base

- Repository HEAD: `0c14652249b0ed946657e88f9f549d5ddbf09272`
- Adjudicated pre-admission ontology SHA-256: `36e4ef61d2007d18ac5cd5d6dd014dcd4266d67438f13d29743bc74969b675ae`
- Admission decision identifier supplied by the operator: `DECISION-20260812-0001`
- Admission date: `2026-08-12`
- Admitting principal: operator as accountable principal

The attached repository snapshot does not itself contain `DECISION-20260812-0001`; its identifier and admission facts are therefore treated here as operator-supplied governance input, not independently re-read from a committed decision file.

## Bookkeeping edits only

1. `status: proposed` -> `status: admitted`.
2. The v9.1 admission-table row records admission date, admitting principal, `DECISION-20260812-0001`, and the pre-admission adjudicated-text hash.
3. The v4 row records supersession by v9.1 while preserving v4 as the admitted reconstruction baseline and historical predecessor.
4. Reconstruction/admission-history wording no longer describes v9.1 as a candidate awaiting review. The v9 row is correspondingly updated from “corrected v9.1 candidate” to “v9.1”.

No normative ontology section was edited.

## Hash distinction

The adjudication was performed over the ontology text whose SHA-256 is:

`36e4ef61d2007d18ac5cd5d6dd014dcd4266d67438f13d29743bc74969b675ae`

Recording that admission changes the document bytes. The post-recording admitted ontology therefore has SHA-256:

`bb9ea9c57250a7b14031554f6111e9b71843cda67a4e5a6c6eec58d78110ec8b`

The first hash identifies the text adjudicated for admission. The second identifies the same ontology after its admission metadata/history was recorded. This is intentional, not a hash inconsistency.

The admission row explicitly preserves the enforcement boundary: admission establishes what the ontology says; it does not establish that constraints are machine-enforced or evidenced as enforced.

## Verification

- `git apply --check`: passed against clean `0c146522...` checkout.
- `git diff --check`: passed.
- `tests/test_abstraction.py`: 7 passed.
- Patch applied in a second clean checkout and reproduced post-recording ontology hash exactly.
- Diff hunks are confined to metadata/admission-table lines at the top of ABS-0004.
