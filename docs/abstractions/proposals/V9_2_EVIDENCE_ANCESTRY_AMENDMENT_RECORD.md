# ABS-0004 v9.2 evidence-ancestry amendment record

Base repository commit: `64bcc2bfafa9bc8695c5f3e95cd890aa57d1f7af`

This is a drafting/packaging record, not the operator's decision record.

## Placement judgment

The admitted proposal is appended as `§4.19 Artifact-Level Evidence Ancestry`,
without the `(defined, deferred)` marker.

Reason: appending as §4.19 preserves all existing subsection numbers and keeps
§4.15–§4.18 as the existing deferred typed-object cluster. The evidence-ancestry
term and its derivation semantics become usable ontology definitions immediately
on admission. What is deferred is capture/evaluation capability, which is already
stated explicitly by the new limitations and proposal. Marking the subsection
itself `(defined, deferred)` would therefore blur definition availability with
implementation availability.

## Incorporated proposal

The content is the text committed at:
`docs/abstractions/proposals/PROP-GAP0008-evidence-ancestry-definition.md`.

The five `[DEF]`, two `[LIMITATION]`, and one `[PROPOSAL]` blocks are carried into
§4.19. The three `[PROPOSED_CONSTRAINT]` blocks preserve the proposal wording and
receive only identifiers `C12.`, `C13.`, and `C14.` so they can be referenced by
the enforcement matrix.

## Enforcement matrix judgments

All three new constraints use governance status `proposed-v9`, claimed
enforcement mode `none`, and an enforcement-evidence cell beginning `none;` with
a named reason. No manual practice is claimed.

- C12 representability: `partial`. `spawned` exists as a record field/relation,
  but no retained directional influence linkage is populated.
- C13 representability: `partial`. co-input/session facts are represented, but
  no directional influence relation and no reconstructible inherited-session
  lineage are available to establish the required ancestry distinction.
- C14 representability: `none`. no ancestry traversal/coverage result record
  exists today, so the fail-closed coverage rule is not presently representable
  as a retained check result.

The matrix therefore moves from 11 to 14 constraints and remains at zero named
enforcement-evidence artifacts for the new rows.

## Admission-hash convention

The repository's v9.1 convention is preserved:

1. The adjudicated v9.2 text is hashed immediately before admission bookkeeping.
2. Admission bookkeeping changes the document bytes (`status`, history/admission
   metadata), so the resulting admitted document has a second hash.
3. The v9.2 admission row records the adjudicated pre-bookkeeping hash and says
   explicitly that the current file has a different post-recording hash. The
   post-recording hash is supplied externally in this record and `SHA256SUMS.txt`
   rather than embedded into the ontology, avoiding a self-referential hash.

The patch reserves `DECISION-20260817-0001` for the operator's forthcoming
admission decision record. No decision record is created by this package. If the
operator uses a different decision id or admission date, the admission-bookkeeping
bytes and post-recording hash must be regenerated before application.

## Verification

- clean checkout at `64bcc2bfafa9bc8695c5f3e95cd890aa57d1f7af`
- `git apply --check`: pass
- `git diff --check`: pass
- §4.19 tag counts: 5 `[DEF]`, 3 `[PROPOSED_CONSTRAINT]`, 2 `[LIMITATION]`, 1 `[PROPOSAL]`
- C12–C14 each have exactly one matrix row; each row is `proposed-v9 / none / none; reason`
- `tests/test_abstraction.py`: 7 passed
- full suite: 743 passed using temporary import-only `openai` and `anthropic` stubs outside the repository because those SDKs are absent from the sandbox
- second checkout reproduces the post-recording ontology SHA-256 exactly
