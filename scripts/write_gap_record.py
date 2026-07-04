from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_lab.documentation.self_model import validate_gap_record


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a SELF-MODEL GAP record.")
    parser.add_argument("--gap-id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--status", default="open")
    parser.add_argument("--category", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--related-capability", action="append", default=[])
    parser.add_argument("--evidence-reason", required=True)
    parser.add_argument("--file-checked", action="append", default=[])
    parser.add_argument("--risk", required=True)
    parser.add_argument("--recommended-first-slice", required=True)
    parser.add_argument("--blocked-by", action="append", default=[])
    parser.add_argument("--priority", default="medium")
    parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()

    record = {
        "schema_version": "v1",
        "gap_id": args.gap_id,
        "name": args.name,
        "status": args.status,
        "category": args.category,
        "summary": args.summary,
        "related_capabilities": args.related_capability,
        "evidence": {
            "reason": args.evidence_reason,
            "files_checked": args.file_checked,
        },
        "risk": args.risk,
        "recommended_first_slice": args.recommended_first_slice,
        "blocked_by": args.blocked_by,
        "priority": args.priority,
    }

    validate_gap_record(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Saved gap record: {args.output}")
    print(f"gap_id: {args.gap_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
