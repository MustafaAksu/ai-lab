# Falsification record: the self-model pre-commit hook

Recorded under DECISION-20260812-0002, which requires that before a check is
relied upon for a governance claim, the input that should make it fail and the
observed result of supplying it are recorded.

Six cases were constructed and run against a clone with the hook installed.

| | constructed input | required behaviour | observed |
| --- | --- | --- | --- |
| 1 | a gap record changed, index not rebuilt — the four real incidents | refuse | **refused**, naming `gaps`, `open_gaps`, `gap_counts`, `recommended_next_targets` as differing |
| 2 | the same change with the index rebuilt and staged | permit | **permitted** |
| 3 | index rebuilt but not `git add`ed — the "built too early" incident | refuse | **refused** |
| 4 | a commit touching no self-model file | not run at all | **not run**, commit permitted |
| 5 | a malformed record, so the build fails | refuse | **refused**, reporting the build failure |
| 6 | unstaged edits present while the staged content is correct | permit | **permitted** |
| 7 | a self-model record **deleted** without rebuilding the index | refuse | **refused** (after correction; see below) |
| 8 | the same deletion with the index rebuilt and staged | permit | **permitted** |
| 9 | the index itself deleted while records change | refuse | **refused** |

## The deletion blind spot, found after shipping

Cases 7 to 9 were added on 2026-08-12 after the reviewing executor found a real
defect in the shipped hook.

`staged_paths()` used `git diff --cached --name-only --diff-filter=ACMR`. `D` is
absent from that filter, so a staged **deletion** of a self-model record returned
no paths, `touches_self_model()` was false, and the hook exited 0. A record could
be removed with no index rebuild and the commit would be permitted, while the
hook's docstring claimed it established that the index describes the staged
records.

The six original cases were all additions and modifications. **No deletion was
ever constructed**, so the falsification practice adopted the same day caught
nothing here: the practice requires that a falsifying case be constructed, and a
case not thought of is not constructed. The reviewing executor found it by
reading the filter rather than by running the suite.

The filter is removed; every staged path now counts. Deleting the index while
records change is refused rather than skipped.

This is the limitation `DECISION-20260812-0002` states in its blocked effects:
the practice does not prevent the defect it addresses, because a constructed
case can be chosen from the same mistaken understanding that produced the check.

## What the falsification found

Case 2 **failed on the first version of the hook**. It refused a correct commit,
because `audit_summary` embeds the audit result, which derives from `repo_head`,
which during a pre-commit hook names the parent of the commit being made. The
audit therefore reports `stale` and the field differs even when index and records
agree exactly.

A hook that refuses correct commits is worse than no hook. `audit_summary` was
added to the excluded set for the same reason `repo_head` already was, and the
reason is recorded in the hook's own docstring.

This is the case the practice exists for: the hook would have been shipped
believing it worked, and its first real use would have blocked a valid commit.

## What this check does not establish

- That `repo_head` is current. It cannot be checked here by construction.
- That the audit will report `verified_current` after the commit. It will not,
  until the next commit, which is the designed one-commit lag the audit reports
  as an info finding.
- That any record is correct. Only that the index describes the records.
