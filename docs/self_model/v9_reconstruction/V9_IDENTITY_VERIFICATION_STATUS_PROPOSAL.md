# ABS-0004 v9 — `identity_verification_status` proposal

## Metadata

- Source repository HEAD independently verified: `c8517902490bd30d91fef562463cb059671a159e`
- Baseline: `docs/self_model/v9_reconstruction/ABS-0004-v9-task3-limitations-candidate.md`
- Scope: draft only the missing ontology text for `identity_verification_status` against the committed task 3 candidate.
- Out of scope: v9 assembly, metadata migration, implementation or schema changes, test changes, review-question authorship, and adjudication.

## Revalidation before drafting

The open item recorded by `DECISION-20260727-0004` and carried forward by `DECISION-20260727-0005` is live:

1. `ai_lab/providers/invocation_record.py` requires `executor.identity_verification_status` on every InvocationRecord.
2. Schema v1 accepts exactly `unresolved` and `verified`.
3. The only admitted capture path hard-codes `unresolved` and performs no identity resolution.
4. All 182 retained InvocationRecords carry `unresolved`; none carries `verified`.
5. `IdentityResolution` is append-only and explicitly does not mutate the InvocationRecord field.
6. Current catalog identity mappings inherit provider-self-report evidence. Authentication can establish who supplied the bytes, not the truth of the mapping.
7. InvocationRecord v1 contains neither a resolved stable identity nor the verifier/evidence reference needed to substantiate `verified`.

Therefore the field must be named, but `verified` cannot be inherited as if it already had a licensed production meaning. The smallest honest treatment is to define its evidentiary meaning and state that no admitted schema-v1 capture path currently meets it.

## Literal proposed text

Insert in Section 4.3 after the definition separating event-time identity resolution from its later assessment and before the existing `[PROPOSED_CONSTRAINT]`:

> `[DEF]` `identity_verification_status` is the immutable capture-time status of
> the executor reference in an InvocationRecord. It is not a later
> IdentityResolution outcome or the current assessment of one. `unresolved` means
> the capture path did not establish an executor-kind-specific stable identity.
> `verified` means an admitted capture path established a unique identity under a
> property-scoped verification rule and durably recorded or referenced the
> identity, supporting evidence, verifier, rule or test version, and verification
> time.
>
> `[LIMITATION]` InvocationRecord schema v1 accepts `verified`, but no admitted
> schema-v1 capture path can presently substantiate it: the current path performs
> no identity resolution, and provider catalog self-report, even over an
> authenticated channel, does not independently establish a model mapping. It
> therefore emits `unresolved`. Later append-only IdentityResolution records do
> not mutate or upgrade this field; validator acceptance of `verified` is
> syntactic compatibility, not a licensed status.

## Why this shape

- The `[DEF]` names the live field and distinguishes capture-time status from both the later resolution annotation and current confidence.
- The definition gives `verified` an evidence-bearing meaning rather than allowing a provider assertion or a validator token to masquerade as verification.
- The `[LIMITATION]` records the present mismatch honestly: the enum contains `verified`, but the admitted v1 record design and capture path cannot substantiate it.
- No new runtime control is claimed. The text does not say that the validator enforces the evidentiary meaning; it states that validator acceptance alone is insufficient.
- No `[ADOPTED_CONSTRAINT]` or `[INHERITED_CONSTRAINT]` is introduced. This is new v9 text, not inherited v4 constraint text.

## Deliberately not decided

- Whether schema v2 should rename the field, remove `verified`, or replace the binary vocabulary.
- Which future evidence mechanism could satisfy the definition in implementation.
- Whether the current validator should reject `verified` until such a mechanism exists.
- Whether any existing or future `IdentityResolution` record should be admitted as independent verification rather than attributed resolution evidence.
- Who assembles v9 or who authors its challenge questions.

## Verification performed

- Embedded Git history and HEAD verified independently.
- `git fsck --full` completed cleanly.
- Self-model audit returned `ok: true` and `verified_current` with the two expected informational findings.
- Baseline is byte-identical to the committed task 3 candidate at HEAD.
- The literal patch applies cleanly and reproduces the supplied candidate byte for byte.
- The patch changes only Section 4.3 and adds one `[DEF]` and one `[LIMITATION]` statement.
- It adds no constraint tag and changes no inherited text.
- Full suite: `713 passed` using import-only local stubs for unavailable `openai` and `anthropic` SDK packages; the stubs were outside the repository and exercised no network behavior.

## Proposed disposition

Accept the literal text for v9 assembly. Keep `verified` as a reserved schema-v1 token with no presently licensed producer. Any implementation change that enables, removes, or renames it requires separate governance.
