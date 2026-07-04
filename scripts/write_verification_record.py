from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from ai_lab.documentation.self_model import validate_verification_record


def _repo_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a SELF-MODEL VERIFY record.")
    parser.add_argument("--verification-id", required=True)
    parser.add_argument("--repo-commit", default=None)
    parser.add_argument("--command", action="append", required=True)
    parser.add_argument("--exit-code", action="append", type=int, required=True)
    parser.add_argument("--summary", action="append", required=True)
    parser.add_argument("--recorded-by-peer-id", default="chatgpt")
    parser.add_argument("--recorded-by-substrate", default="conversation")
    parser.add_argument("--recorded-by-role", default="assistant")
    parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()

    if not (len(args.command) == len(args.exit_code) == len(args.summary)):
        parser.error("--command, --exit-code, and --summary must have matching counts.")

    record = {
        "schema_version": "v1",
        "verification_id": args.verification_id,
        "repo_commit": args.repo_commit or _repo_head(),
        "recorded_by": {
            "peer_id": args.recorded_by_peer_id,
            "substrate": args.recorded_by_substrate,
            "role": args.recorded_by_role,
        },
        "commands": [
            {
                "command": command,
                "exit_code": exit_code,
                "summary": summary,
            }
            for command, exit_code, summary in zip(
                args.command,
                args.exit_code,
                args.summary,
                strict=True,
            )
        ],
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }

    validate_verification_record(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Saved verification record: {args.output}")
    print(f"verification_id: {args.verification_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
