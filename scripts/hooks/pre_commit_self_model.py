#!/usr/bin/env python3
"""Refuse a commit whose self-model records disagree with the committed index.

Four index-lag incidents occurred on 2026-08-12, with four different causes: the
index was built before `git add`, built on a stale checkout, built against the
wrong parent after a failed rebase, and built on one side of a divergence. In
each case the repository landed in a state that failed its own audit, and each
was found by running the suite afterwards rather than by anything refusing.

WHAT THIS CHECKS, AND WHAT IT DOES NOT.

It compares the record-derived content of the staged SELF_MODEL.json against a
rebuild from the staged record files. It deliberately EXCLUDES two fields:

  repo_head    During a pre-commit hook, `git rev-parse HEAD` names the PARENT
               of the commit being made, so a rebuild here can never produce the
               repo_head the commit will have. The one-commit lag is a designed
               condition that the audit reports as an info finding, not an
               error, and this hook must not attempt to enforce against it.

  generated_at A timestamp, different on every run by construction.

  audit_summary It embeds the audit result, which is derived from repo_head. With
               repo_head necessarily naming the parent here, the audit reports
               stale and this field differs even when the index and records agree
               exactly. Excluding it was not foreseen: the first version of this
               hook refused a correct commit in test, which is a worse failure
               than not checking at all.

So this hook establishes that the committed index describes the committed
records. It does NOT establish that repo_head is current, that the audit will
report verified_current after the commit, or that any record is correct.

It also reads the STAGED content rather than the working tree, so a commit made
with `git add -p` or with unstaged edits present is checked against what is
actually being committed.

Install:  ln -sf ../../scripts/hooks/pre_commit_self_model.py .git/hooks/pre-commit
Bypass:   git commit --no-verify   (recorded here as available, deliberately)
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

INDEX = "docs/self_model/SELF_MODEL.json"
RECORD_DIRS = ("capabilities", "gaps", "verifications", "plans", "warrants", "decisions")
EXCLUDED = ("repo_head", "generated_at", "audit_summary")


def git(*args: str, **kw) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, **kw).stdout


def staged_paths() -> list[str]:
    out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return [l for l in out.splitlines() if l.strip()]


def touches_self_model(paths: list[str]) -> bool:
    return any(p.startswith("docs/self_model/") and p.endswith(".json") for p in paths)


def main() -> int:
    paths = staged_paths()
    if not touches_self_model(paths):
        return 0

    repo = Path(git("rev-parse", "--show-toplevel").strip())

    # Build from what is STAGED, not from the working tree. `git stash` would be
    # destructive in a hook; a temporary checkout of the index is not.
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "checkout-index", "-a", "-f", f"--prefix={td}/"],
                       cwd=repo, check=True, capture_output=True)
        work = Path(td)
        staged_index_path = work / INDEX
        if not staged_index_path.exists():
            print("pre-commit: SELF_MODEL.json is absent from the staged tree; "
                  "not checking.", file=sys.stderr)
            return 0
        staged_index = json.loads(staged_index_path.read_text())

        r = subprocess.run(
            [sys.executable, str(repo / "scripts" / "build_self_model.py"),
             "--repo-root", str(work), "--output", str(work / "REBUILT.json"),
             "--generated-at", "1970-01-01T00:00:00+00:00"],
            capture_output=True, text=True, cwd=repo)
        if r.returncode != 0:
            print("pre-commit: the self-model build FAILED against the staged tree.",
                  file=sys.stderr)
            print(r.stderr.strip()[:800], file=sys.stderr)
            return 1
        rebuilt = json.loads((work / "REBUILT.json").read_text())

    a = {k: v for k, v in staged_index.items() if k not in EXCLUDED}
    b = {k: v for k, v in rebuilt.items() if k not in EXCLUDED}
    if a == b:
        return 0

    differing = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    print("\npre-commit REFUSED: the staged self-model index does not describe the "
          "staged records.", file=sys.stderr)
    print(f"  differing keys: {differing}", file=sys.stderr)
    for k in differing:
        if isinstance(a.get(k), list) and isinstance(b.get(k), list):
            only_a = [x for x in a[k] if x not in b[k]]
            only_b = [x for x in b[k] if x not in a[k]]
            if only_a:
                print(f"  {k}: in the index but not derivable from the records: "
                      f"{str(only_a)[:200]}", file=sys.stderr)
            if only_b:
                print(f"  {k}: derivable from the records but missing from the index: "
                      f"{str(only_b)[:200]}", file=sys.stderr)
    print("\n  Fix:  python scripts/build_self_model.py && "
          "git add docs/self_model/SELF_MODEL.json", file=sys.stderr)
    print("  This hook compares record content only. It does not check repo_head, "
          "which necessarily lags by one commit here.\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
