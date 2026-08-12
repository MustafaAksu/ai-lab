# ABS-0004 v9.1 — C10 Section 9 governance alignment

## Base

- Repository HEAD: `7b386b8b7e265509785736f78295dc5d7937a7e8`
- Baseline ontology SHA-256: `6dbd6d87f41bae1a9510c43c55d8a3f1a843f6022978bf77710f8fc77753aaaf`

## Finding

C10 was retagged in the normative body from `[INHERITED_CONSTRAINT]` to
`[PROPOSED_CONSTRAINT]` after material referent drift was established, but its
Section 9 governance-status cell remained `inherited-v4`.

A complete C1–C11 cross-check found no other sentence-tag / matrix-governance
mismatch. C10 was the sole mismatch.

## Correction

Change only C10's Section 9 governance status:

- `inherited-v4` -> `proposed-v9`

No other C10 matrix cell changes.

## Non-governance-cell verification

- Claimed enforcement mode remains `manual`. The ontology still claims current
  manual practice; this field records the claim, not evidence that it occurred.
- Enforcement evidence remains `none; ...`: repository search found verification
  activity records but no named retained artifact attesting a C10
  lineage-independence check for a named verification.
- No C10/verifier-ancestry machine enforcement exists in `ai_lab/`, `scripts/`,
  or `tests/` in this checkout.
- Representability, target enforcement, activation condition, and dependency
  cells are unchanged by the governance-source retag.

## Scope

This proposal changes one table cell only. It does not change C10 wording,
Section 4.17, implementation code, or any other constraint's governance status.
