#!/usr/bin/env python3
"""Emit read-only L0 discovery advisor suggestions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.l0_discovery_advisor import (
    build_l0_discovery_advisor_record,
    l0_discovery_advisor_manifest_document,
    load_json_object,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build diagnostic-only L0 discovery advisor output."
    )
    parser.add_argument(
        "--selected-context-item",
        action="append",
        default=[],
        help="Selected context item ID available to the advisor as read-only evidence.",
    )
    parser.add_argument(
        "--retrieval-simulator",
        action="append",
        default=[],
        type=Path,
        help="Read-only JSON output from the L0 retrieval simulator.",
    )
    parser.add_argument(
        "--candidate-diagnostics",
        action="append",
        default=[],
        type=Path,
        help="Read-only JSON output from L0 candidate diagnostics.",
    )
    parser.add_argument(
        "--max-suggestions",
        type=int,
        default=None,
        help="Optional maximum number of advisory suggestions.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional run ID for the advisor record.",
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

    retrieval_records = [load_json_object(path) for path in args.retrieval_simulator]
    candidate_records = [load_json_object(path) for path in args.candidate_diagnostics]

    record = build_l0_discovery_advisor_record(
        selected_context_item_ids=args.selected_context_item,
        retrieval_simulator_records=retrieval_records,
        candidate_diagnostics_records=candidate_records,
        retrieval_simulator_paths=[str(path) for path in args.retrieval_simulator],
        candidate_diagnostics_paths=[str(path) for path in args.candidate_diagnostics],
        max_suggestions=args.max_suggestions,
        run_id=args.run_id,
    )
    document = l0_discovery_advisor_manifest_document(record)
    payload = json.dumps(document, indent=2, sort_keys=True) + "\n"

    if args.output is None:
        print(payload, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
