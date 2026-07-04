from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.self_model import (
    file_sha256,
    read_json,
    validate_capability_record,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refresh SELF-MODEL CAP file evidence content_hash values."
    )
    parser.add_argument("capability", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Only fill null/missing content_hash values; leave existing hashes unchanged.",
    )

    args = parser.parse_args()

    record = read_json(args.capability)
    validate_capability_record(record)

    evidence = record["evidence"]
    assert isinstance(evidence, dict)

    updated = 0
    for item in evidence.get("files", []):
        if not isinstance(item, dict):
            continue

        item_path = item.get("path")
        if not isinstance(item_path, str) or not item_path:
            continue

        if args.only_missing and item.get("content_hash"):
            continue

        source_path = args.repo_root / item_path
        if not source_path.exists():
            parser.error(f"evidence file does not exist: {item_path}")

        item["content_hash"] = file_sha256(source_path)
        updated += 1

    validate_capability_record(record)
    args.capability.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Refreshed capability hashes: {args.capability}")
    print(f"updated: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
