from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_lab.documentation.self_model import validate_capability_record


def _split_pair(value: str, label: str) -> tuple[str, str]:
    if ":" not in value:
        raise argparse.ArgumentTypeError(f"{label} must use VALUE:ROLE format")
    left, right = value.split(":", 1)
    if not left or not right:
        raise argparse.ArgumentTypeError(f"{label} must use VALUE:ROLE format")
    return left, right


def _split_triple(value: str, label: str) -> tuple[str, str, str]:
    parts = value.split(":", 2)
    if len(parts) != 3 or not all(parts):
        raise argparse.ArgumentTypeError(f"{label} must use ID:PATH:ROLE format")
    return parts[0], parts[1], parts[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a SELF-MODEL CAP record.")
    parser.add_argument("--capability-id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--status", default="implemented")
    parser.add_argument("--category", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--interface", action="append", default=[])
    parser.add_argument("--commit", action="append", default=[], help="FULL_HASH:ROLE")
    parser.add_argument("--file", action="append", default=[], help="PATH:ROLE")
    parser.add_argument("--memory-record", action="append", default=[], help="ID:PATH:ROLE")
    parser.add_argument("--admission", action="append", default=[], help="ID:PATH:ROLE")
    parser.add_argument("--limit", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--recommended-next-action", action="append", default=[])
    parser.add_argument("--last-verified-commit", required=True)
    parser.add_argument("--verification-artifact", required=True)
    parser.add_argument("--verified-at", required=True)
    parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()

    commits = [
        {"commit": commit, "role": role}
        for commit, role in (_split_pair(value, "--commit") for value in args.commit)
    ]
    files = [
        {"path": path, "role": role, "content_hash": None}
        for path, role in (_split_pair(value, "--file") for value in args.file)
    ]
    memory_records = [
        {"id": record_id, "path": path, "role": role}
        for record_id, path, role in (
            _split_triple(value, "--memory-record") for value in args.memory_record
        )
    ]
    admissions = [
        {"id": record_id, "path": path, "role": role}
        for record_id, path, role in (
            _split_triple(value, "--admission") for value in args.admission
        )
    ]

    record = {
        "schema_version": "v1",
        "capability_id": args.capability_id,
        "name": args.name,
        "status": args.status,
        "category": args.category,
        "summary": args.summary,
        "interfaces": args.interface,
        "evidence": {
            "commits": commits,
            "files": files,
            "memory_records": memory_records,
            "admissions": admissions,
        },
        "limits": args.limit,
        "risks": args.risk,
        "recommended_next_actions": args.recommended_next_action,
        "last_verified": {
            "repo_commit": args.last_verified_commit,
            "verification_artifact": args.verification_artifact,
            "verified_at": args.verified_at,
        },
    }

    validate_capability_record(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Saved capability record: {args.output}")
    print(f"capability_id: {args.capability_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
