#!/usr/bin/env python3
"""Check the VERIFY v2 content-addressed store and every v2 record that references it.

PLAN-20261124-0001 S4. Integrity means stored bytes equal the recorded digest. It
does not establish where or whether a run took place.

Checks: every blob in the store hashes to its own name and sits at the path
derived from that name; every canonical VERIFY v2 record validates against its
stored receipt (receipt bytes, referenced blobs, recomputed result, retention and
summary, and the invariants of S1(c)). Exit 0 when nothing is wrong, 1 otherwise.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai_lab.documentation import verification_v2  # noqa: E402


def check(repo_root: Path) -> list[str]:
    problems: list[str] = []
    store = repo_root / verification_v2.STORE_RELATIVE_ROOT
    if store.is_dir():
        for path in sorted(p for p in store.rglob("*") if p.is_file()):
            relative = path.relative_to(store).as_posix()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if relative != verification_v2.store_relative_path(path.name) or path.name != digest:
                problems.append(f"store blob {relative}: content SHA-256 {digest} does not match its address")
    records = repo_root / "docs" / "self_model" / "verifications"
    for path in sorted(records.glob("VERIFY-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("schema_version") != "v2":
            continue
        try:
            verification_v2.validate_against_store(record, repo_root)
        except verification_v2.VerificationV2Error as error:
            problems.append(f"{path.name}: {error}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    problems = check(args.repo_root.resolve())
    for problem in problems:
        print(problem)
    print(json.dumps({"ok": not problems, "problems": len(problems)}, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
