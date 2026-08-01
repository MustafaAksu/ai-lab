# ABS-0004 v9 reconstruction — Task 1
## Independent re-read of admitted v4 Section 3

- **Record:** `ABS-0004-v9-task1-v4-section3-reread-0001`
- **Repository snapshot:** `bff2a747bc2531089af08c9fe95fd526469e5507`
- **Admitted v4 commit:** `56f18a2ab7b66b1855b631a32d540f654c62b2c2`
- **Baseline surface:** `docs/abstractions/ABS-0004-invocation-authorization-ontology.md`, Section 3, lines 106–133 at the admitted v4 commit
- **Task boundary:** Re-read v4 Section 3 against findings from `COMP-0035`, `COMP-0037`, `COMP-0039..0046`, and `COMP-0118..0125`. No v9 language, schema, control, or implementation remedy is proposed here.

## Repository verification

The supplied ZIP contains a complete Git repository: `.git`, packed objects, refs, index, and working tree. `git fsck --full` completed without findings. A clean clone made from the embedded Git object database resolves `main`, `origin/main`, and `origin/HEAD` to `bff2a747bc2531089af08c9fe95fd526469e5507`.

The self-model audit at that clean checkout reports:

- `ok: true`
- `verification_outcome: verified_current`
- `SELF_MODEL_INDEX_REPO_HEAD_DIFFERS_SOURCE_UNCHANGED` — info
- `SELF_MODEL_INDEX_CONTENT_CURRENT` — info

The working tree stored directly in the ZIP has line-ending conversion across text files and therefore appears globally modified relative to the Git index. It was not used as evidence. All readings were made from Git objects or the clean clone.

## Baseline text under review

V4 Section 3 contains three substantive units:

1. a distinction among invocation authorization, routing selection, and evidence admission;
2. a subordinate-authorization inheritance rule that separately identifies undeclared subordinate execution as a Section 4.7 disclosure violation;
3. one explicit `[OPEN]` for authorization-chain bootstrap.

## Result

**No finding from the four later evidence sets establishes that admitted v4 Section 3 requires a textual change.**

Thirteen admitted ledger entries bear on or are adjacent to Section 3: `V9L-004` through `V9L-015`, plus `V9L-017`. Their response classes remain:

- 4 unresolved;
- 3 explicit limitation sufficient;
- 6 separate gap or policy required;
- 0 v4 change required.

The re-read found no contradiction to that classification.

This is not a finding that the bootstrap problem is solved. It is the narrower finding that the later rounds did not establish a better ontology-level replacement for v4's explicit `[OPEN]`, and that the successful attacks were directed at attempted closures, added status language, missing policy, record attribution, or downstream interpretation.

## Finding-by-finding trace

| Finding | How it bears on v4 Section 3 | Re-read result |
|---|---|---|
| `V9L-004` | Tests the bootstrap `[OPEN]` against the extra-systemic entitlement limit. | V4 already leaves termination unresolved and makes no claim that repository records establish real-world entitlement. No Section 3 change established. |
| `V9L-005` | Distinguishes external entitlement truth from repository-internal acceptance controls. | The distinction is real, but the rounds do not adjudicate an internal acceptance objective or rule. The evidence remains unresolved rather than a basis for changing Section 3. |
| `V9L-006` | Identifies authority-source and target-derived/reverse-fit scope attacks. | These attacks concern scope legitimacy and policy semantics around `authority_scope`; v4 Section 3 contains no attempted scope-termination solution to correct. Separate gap or policy evidence, not Section 3 text. |
| `V9L-007` | Challenges the rejection of partial breadth controls merely because they do not solve every scope attack. | The defense-in-depth inference remains disputed and no concrete policy was adjudicated. No Section 3 change established. |
| `V9L-008` | Shows that a `self_issued` marker is not an independence control without externally fixed requirements and an evaluator. | V4 Section 3 contains no `self_issued` marker or inert disqualification clause. The finding blocks importing later attempted controls; it does not require changing v4. |
| `V9L-009` | Constructs false decision attribution despite apparently valid chain semantics. | The attack concerns attribution, approval evidence, and record integrity in or around Section 4.13. Section 3 distinguishes decision kinds but does not claim to authenticate the named issuer or approver. No Section 3 change established. |
| `V9L-010` | Rejects complete-visibility claims for undeclared, unlinked, untraversable, or misattributed authorizations. | V4 Section 3 makes no complete-visibility claim. Its subordinate paragraph expressly acknowledges undeclared execution as possible and classifies it as a disclosure violation. Preserve the absence of the later overclaim. |
| `V9L-011` | Challenges a requirement that scope breadth be “legible” without interpretation or rendering semantics. | V4 Section 3 contains no breadth-legibility rule. The disputed later requirement supplies no reason to alter v4. |
| `V9L-012` | Identifies the downstream risk of a control-shaped clause whose separate disclaimer says it is inert. | V4 Section 3 contains no such control-plus-disclaimer construction. The finding is a document-design warning against later remedies, not a defect in v4. |
| `V9L-013` | Distinguishes a recorded chain terminus from substantive authorization and attacks the term `self-standing`. | V4 Section 3 uses neither standing-authority termination nor `self-standing`. Its bootstrap remains open. No Section 3 change established. |
| `V9L-014` | Shows that absence of a separate admission event is not itself an admission status. | This concerns artifact-governance metadata and admission-state representation, not substantive Section 3 semantics. No Section 3 change. |
| `V9L-015` | Shows that a narrow authorization checker can produce labels such as `valid authorization` or `governed` that exceed the properties checked, especially when Section 4.7 disclosure is excluded. | V4's decision-kind separation remains valid. Its subordinate paragraph already separates authorization-scope coverage from an undeclared-execution disclosure violation. The missing validator boundary and consumer-label semantics belong to separate policy/governance work. |
| `V9L-017` | Shows that refusal lists can omit or conflate missing authorization, unmet independence, undeclared subordinate execution, and disclosure failures. | V4 Section 3 defines no refusal enumeration. Its two subordinate cases are already distinct: represented execution outside declared classes versus execution left undeclared. No change established. |

## Round-level cross-check

- **`COMP-0035`:** Its durable findings concern catalog verification, temporal identity status, and network/offline boundaries in Sections 4.3–4.4 and implementation governance. None bears on Section 3.
- **`COMP-0037`:** Establishes attacks on attempted standing-authority closure, scope legitimacy, positive status labels, direct-only independence checks, and refusal completeness. The attacks defeat v6 mechanisms; they do not identify a false statement in v4's open bootstrap.
- **`COMP-0039`:** Concerns direct-only versus deeper lineage/self-adjudication checks. Its primary surface is C3 and claim/evidence ancestry, not Section 3.
- **`COMP-0040..0043`:** Strengthen the extra-systemic entitlement limit, distinguish possible internal acceptance objectives, expose visibility and self-issued-control overclaims, and identify refusal-boundary problems. They support leaving the v4 bootstrap open and preserving the subordinate disclosure distinction.
- **`COMP-0044..0046`:** Concern enforcement evidence, test oracles, schema lock-in, and downstream Slice D constraints. They do not establish a Section 3 textual defect.
- **`COMP-0118..0125`:** Defeat v8's legibility rule, inert disqualification, recorded override, self-standing terminology, admission table, narrowed refusal completeness, checkability claims, and revision-history-heavy document shape. Those are defects introduced after v4; their absence from v4 is evidence for restraint, not a reason to back-port corrective prose.

## Specific checks against the three v4 units

### Decision-kind distinction

The later rounds do not refute the distinction among authorization, routing, and evidence admission. They instead show that a downstream implementation must not let a narrow authorization result imply evidence admission, independence, execution gating, or complete governance. Those are boundary and label problems outside the definition itself.

### Subordinate authorization inheritance

The later rounds repeatedly rely on v4's distinction rather than defeating it:

- a represented subordinate outside declared classes is an authorization-coverage problem;
- an undeclared subordinate is a disclosure violation and is not made implicitly authorized.

The later failed plans blurred these cases in refusal labels. V4 does not.

### Bootstrap `[OPEN]`

The later rounds establish that internal records cannot prove extra-systemic entitlement and that attempted standing-authority closures introduced new attacks. They do not establish a replacement termination rule. Four unresolved ledger entries cluster here and remain disputed. The evidence therefore supports retaining the question as open rather than converting it into normative closure text.

## Task 1 disposition

- **Section 3 textual delta required by later evidence:** none established.
- **Section 3 concepts requiring later non-text resolution:** bootstrap objective and evidence, internal acceptance-policy scope, scope-attack policy, independence policy, attribution integrity, and consumer-label semantics.
- **Drafting performed:** none.
- **Repository files modified:** none.

---

# Verification block

Appended by the drafting executor of v5 through v8, acting here as verifier
only. This block is not part of the re-read and did not influence it: the
re-read was completed and checksummed before this executor saw it. Everything
below was checked against the repository at `bff2a747bc2531089af08c9fe95fd526469e5507`.

## Integrity

- SHA-256 of the re-read record matches the supplied checksum:
  `90e374082c9a73047d5c749422480a32662531e48cbdefdac7e17c65a571ef7d`.
- The reported snapshot commit equals this checkout's HEAD.
- `56f18a2ab7b66b1855b631a32d540f654c62b2c2` resolves, dated 2026-07-21,
  subject "Admit ABS-0004 v4: invocation authorization ontology".

## Baseline surface

Lines 106-133 at the admitted v4 commit are exactly Section 3: 1,463 characters
across 28 lines. (An earlier figure of 1,464 recorded in this repository
measured from the `## 3.` heading to the `## 4.` heading and includes the
trailing blank line.)

Tag census of that range:

| tag | count |
| --- | --- |
| `[DEF]` | 3 |
| `[OPEN]` | 1 |
| `[ADOPTED_CONSTRAINT]` | 0 |
| `[PRINCIPLE]` | 0 |

The zero is worth stating because it was not in the re-read and bears on the
withdrawal. `[ADOPTED_CONSTRAINT]` is the tag ABS-0004 defines as "constraint
adopted now", and the contradiction between 24 of them and `status: proposed`
is what decided DECISION-20260727-0002. Admitted v4 Section 3 carries none. The
tag entered with the amendments.

## Substantive claims

The re-read asserts that v4 Section 3 contains none of the constructions the
later rounds attacked. Each was checked by search over the exact line range:

| asserted absent | result |
| --- | --- |
| `self_issued` marker | absent |
| `self-standing` terminology | absent |
| breadth-legibility rule ("legible") | absent |
| standing-authority termination | absent |
| refusal enumeration | absent |
| complete-visibility claim ("every authorization") | absent |

And the three units it asserts are present — the decision-kind distinction, the
subordinate-inheritance rule naming a Section 4.7 disclosure violation, and the
single bootstrap `[OPEN]` — are all present.

## Trace completeness

The ledger records thirteen Section 3 bearing entries. The re-read traces
thirteen: none omitted, none added. Their response classes as stored in
`V9_CHANGE_LEDGER.json` are 4 unresolved, 3 explicit limitation sufficient,
6 separate gap or policy required, 0 v4 change required, which is what the
re-read reports.

## Not checked

- Whether each ledger finding is correctly extracted from the round it cites.
  That would require re-reading roughly 844KB of comparison artifacts, and this
  executor is the party whose text those rounds reviewed.
- Whether the ledger's classification of any entry is correct. Those
  classifications were adjudicated by the operator under DECISION-20260727-0003
  and are not re-derived here.
- Whether v4 Section 3 is correct. The re-read establishes that the later
  rounds do not show it false, which is a different and narrower claim.

## Disposition

Task 1 of DECISION-20260727-0002 is complete. Its requirement was that the
re-read be recorded before v9 drafting begins, and that a null result be
recorded as a result rather than treated as a failure to find something. The
result is null and is recorded as such.

No repository file was modified by the re-read or by this verification.
