#!/usr/bin/env python3
"""Evaluate read-only L0 discovery advisor diagnostics in saved manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.l0_discovery_advisor_evaluation import (
    evaluate_l0_discovery_advisor_manifest_paths,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a diagnostic-only evaluation of manifest-connected L0 discovery "
            "advisor suggestions from saved context-pack manifest JSON files."
        )
    )
    parser.add_argument(
        "--manifest",
        action="append",
        required=True,
        type=Path,
        help="Saved context-pack manifest JSON containing optional advisor diagnostics.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional run ID for the evaluation record.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path. If omitted, JSON is printed to stdout.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    record = evaluate_l0_discovery_advisor_manifest_paths(
        args.manifest,
        run_id=args.run_id,
    )
    payload = json.dumps(record, indent=2, sort_keys=True) + "\n"

    if args.output is None:
        print(payload, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
