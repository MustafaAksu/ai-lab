from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.self_model import validate_plan_record


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a self-model PLAN record.")
    parser.add_argument("--plan-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--created-at", required=True)
    parser.add_argument("--source-gap-id", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--proposed-change", required=True)
    parser.add_argument("--rationale", action="append", required=True)
    parser.add_argument("--constraint", action="append", required=True)
    parser.add_argument("--success-criterion", action="append", required=True)
    parser.add_argument("--risk", required=True)
    parser.add_argument("--next-action", required=True)
    parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()

    record = {
        "schema_version": "v1",
        "plan_id": args.plan_id,
        "title": args.title,
        "status": args.status,
        "created_at": args.created_at,
        "source_gap_id": args.source_gap_id,
        "objective": args.objective,
        "proposed_change": args.proposed_change,
        "rationale": args.rationale,
        "constraints": args.constraint,
        "success_criteria": args.success_criterion,
        "risk": args.risk,
        "next_action": args.next_action,
    }

    validate_plan_record(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Saved PLAN record: {args.output}")
    print(f"plan_id: {args.plan_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
