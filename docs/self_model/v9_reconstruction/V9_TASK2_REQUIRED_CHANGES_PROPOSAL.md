# ABS-0004 v9 reconstruction — Task 2 proposal
## Revalidation and literal text for the ledger entries classified `v4 change required`

- **Proposal id:** `ABS-0004-v9-task2-required-changes-proposal-0001`
- **Repository snapshot verified:** `99194a29bf639a9ed80c7fe9259c4935252e8530`
- **Admitted baseline:** `56f18a2ab7b66b1855b631a32d540f654c62b2c2`
- **Evidence input:** `docs/self_model/V9_CHANGE_LEDGER.json`, admitted by `DECISION-20260727-0003`
- **Task boundary:** revalidate and draft only V9L-001, V9L-002, and V9L-027. No limitation-sufficient entry, Section 3 text, plan text, schema implementation, or review question is drafted here.
- **Drafting status:** proposal only; no ontology file has been modified.

## Repository verification

The uploaded ZIP contains full Git history. A clean clone from the embedded object database resolves HEAD to `99194a29bf639a9ed80c7fe9259c4935252e8530`; `git fsck --full` is clean; the working tree is clean; and `python scripts/audit_self_model_index.py --repo-root .` reports `ok: true` and `verification_outcome: verified_current` with the two expected informational findings.

## Task 1 verification limits carried forward

The appended verification block in `V9_TASK1_SECTION3_REREAD.md` explicitly did not check:

1. whether each ledger finding was correctly extracted from its source round;
2. whether each ledger classification was correct;
3. whether v4 Section 3 itself was correct.

Task 2 therefore re-read the source evidence for the three entries before drafting. It does not treat the admitted classifications as infallible. `DECISION-20260727-0003` itself says admission does not claim that the classifications are correct.

## Sentence-category boundary

No proposed sentence below uses `[ADOPTED_CONSTRAINT]`. The literal text uses `[DEF]` for ontology meanings and `[PROPOSED_CONSTRAINT]` for behavior that would acquire force only after admission. This preserves the verified Task 1 finding that admitted v4 Section 3 contains zero `[ADOPTED_CONSTRAINT]` tags and does not reproduce v8's proposed/adopted-now contradiction.

## Revalidation result

| Ledger entry | Revalidation | Draft disposition |
| --- | --- | --- |
| `V9L-001` | Confirmed live against v4. Section 4.4 permits a `CatalogVerification` carrying the repository's generic `verified_current` outcome even when the only evidence is the provider's own assertion. COMP-0035 establishes verification collapse/circular attestation. | Drafted. Remove the catalog-specific verification layer from this block; distinguish attributed self-report from property-scoped verification through the already-defined generic `VerificationRun`. |
| `V9L-002` | Confirmed live against v4. Section 4.3 has one identity-verification status and no semantic separation between the event-time resolution and current confidence after later contradiction or staleness. | Drafted. Define the two facts separately and prohibit later evidence from overwriting the historical event-time resolution. |
| `V9L-027` | **Not live against admitted v4 as stated.** COMP-0032 reviewed v3, where only `RoutingPolicy` existed. Commit `56f18a2` added §4.16 `AuthorizationPolicy` as a versioned durable rule and states that all DecisionRecord policy references are typed references, never untyped strings. Section 11 separately marks its enforcement deferred. COMP-0119's inertness attack depends on v8's self-issued-disqualification clause, which v4 does not contain. | **No text drafted.** Drafting another policy definition would duplicate an already-applied COMP-0032 remedy or import the excluded v8 response. The ledger's `later_disposition` is factually wrong when it says v8 defined the object: v4 did. This discrepancy requires operator re-adjudication rather than silent reconciliation. |

## Literal replacement for v4 §§4.3–4.4

The following block replaces v4 from `### 4.3 ModelIdentity` through the final definition in §4.4. It is the complete proposed text for V9L-001 and V9L-002.

```markdown
### 4.3 ModelIdentity

`[DEF]` The stable identity of a model release used for provenance:
`model_id`, `originator_id` (developing organization), canonical name,
release/version identity where establishable. Deprecation is mutable and
endpoint-specific; it lives in catalog assertions.

`[DEF]` An invocation's event-time identity resolution and the current
assessment of that resolution are distinct facts. The event-time resolution is
bound to the evidence available when the invocation occurred. A later
assessment is recorded separately and linked to that historical resolution.

`[PROPOSED_CONSTRAINT]` An invocation records the most precise ModelIdentity
resolution establishable from evidence available at execution time; an
unresolved requested name is recorded as unresolved and is never silently
substituted. Later evidence that a relied-on catalog assertion was stale,
contradicted, or wrong does not overwrite the event-time resolution.

### 4.4 CatalogSnapshot and CatalogAssertion

`[DEF]` CatalogSnapshot: `snapshot_id`, provider surface, `observed_at`,
source set, assertions[]. Each CatalogAssertion is atomic and records only
the claim: `assertion_subject`, `assertion_predicate`,
`assertion_value_or_target`, unit, scope, `valid_from`,
`valid_until`/superseded, source. An assertion may concern an API alias, an
endpoint, a price, a region, or a model identity. Example atomic assertions:
(api-name-X, resolves_to, model-identity-Y); (api-name-X, context_limit,
400000, tokens).

`[DEF]` A CatalogAssertion records what its named source asserted at the
snapshot's observed time. A provider-controlled catalog response is an
attributed provider self-report. Authentication of the endpoint and integrity
of the captured payload may establish who supplied which bytes at a time; they
do not independently establish the truth of the asserted model mapping,
capability, price, region, or identity.

`[DEF]` Verification of a property concerning a CatalogAssertion is represented
by a VerificationRun (Section 4.17), separate from the assertion. The
VerificationRun identifies the property assessed, the evidence used, and the
result.

`[PROPOSED_CONSTRAINT]` A provider assertion alone never supports an
unqualified `verified` status. Any verification claim concerning a
CatalogAssertion is limited to the named property its evidence establishes.

`[DEF]` Catalog assertions record what a provider claims; they never record
suitability for an AI-Lab role.
```

## Property established and not established

### V9L-001

The proposed text establishes only that:

- provider-returned catalog content is attributed self-report;
- endpoint authentication and payload integrity establish those named properties, not catalog truth;
- catalog-related verification is property-scoped and separate from the assertion;
- provider self-report alone cannot yield an unqualified verified status.

It does **not** establish that a model mapping or capability is true, that a provider catalog is complete, or that a `VerificationRun` implementation exists.

### V9L-002

The proposed text establishes only that:

- the resolution made from execution-time evidence is a historical fact distinct from current confidence;
- later evidence is linked separately rather than overwriting that historical result;
- unresolved requested names remain unresolved rather than being silently substituted.

It does **not** choose a status enum, a record-family implementation, a freshness window, or an automatic re-resolution policy.

## V9L-027 discrepancy

The admitted ledger says:

> AuthorizationPolicy is a load-bearing missing object ... Untyped strings ... cannot support replayable external constraints.

That statement accurately describes the v3 surface reviewed by COMP-0032, but not admitted v4. The v4 commit message explicitly lists `AuthorizationPolicy ... defined`, and §4.16 states:

> All policy references in DecisionRecords ... are typed references to a versioned policy object, never untyped strings.

The remaining fact is narrower: enforcement is deferred. V4 says so in the §4.16 heading and Section 11. Deferral can make a later control inoperative, but v4 contains no self-issued control whose operation depends on the deferred policy. No V9L-027 text can therefore be drafted honestly without first changing the admitted classification or supplying a different defect construction against v4.

## Files supplied

- `ABS-0004-v9-task2-required-changes.patch` — unified diff against the exact v4 commit, containing only the V9L-001/V9L-002 textual delta.
- `ABS-0004-v9-task2-proposed-baseline.md` — v4 with that delta applied for inspection; not a complete v9 draft.
- This proposal record — preserved literal text and the V9L-027 discrepancy.

## Disposition

- V9L-001: literal text proposed.
- V9L-002: literal text proposed.
- V9L-027: no text proposed; operator re-adjudication required.
- Section 3: untouched.
- `[ADOPTED_CONSTRAINT]` introduced by this task: zero.
- Repository ontology modified: no.
