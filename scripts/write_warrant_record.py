from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.self_model import validate_warrant_record


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a self-model WARRANT record.")
    parser.add_argument("--warrant-id", required=True)
    parser.add_argument("--target-item-id", required=True)
    parser.add_argument("--target-item-type", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--warrant-state", required=True)
    parser.add_argument("--created-at", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--substrate", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--evidence-id", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()

    record = {
        "schema_version": "v1",
        "warrant_id": args.warrant_id,
        "target_item_id": args.target_item_id,
        "target_item_type": args.target_item_type,
        "decision": args.decision,
        "warrant_state": args.warrant_state,
        "created_at": args.created_at,
        "author": args.author,
        "substrate": args.substrate,
        "reason": args.reason,
        "scope": args.scope,
        "evidence_ids": args.evidence_id,
    }

    validate_warrant_record(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Saved WARRANT record: {args.output}")
    print(f"warrant_id: {args.warrant_id}")
    print(f"target: {args.target_item_id} ({args.target_item_type})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
