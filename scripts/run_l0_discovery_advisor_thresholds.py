#!/usr/bin/env python3
"""Write review-only acceptance thresholds for L0 discovery advisor evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.l0_discovery_advisor_thresholds import (
    DEFAULT_EVIDENCE_PATH,
    DEFAULT_OUTPUT_PATH,
    write_l0_discovery_advisor_threshold_review,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read saved L0 discovery advisor evidence and write a review-only "
            "acceptance-threshold decision artifact."
        )
    )
    parser.add_argument(
        "--evidence-path",
        type=Path,
        default=DEFAULT_EVIDENCE_PATH,
        help="Path to evidence.json produced by the evidence corpus.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path where thresholds.json is written.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional run ID for the threshold review.",
    )
    parser.add_argument(
        "--created-at",
        default=None,
        help="Optional ISO timestamp for deterministic output.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    review = write_l0_discovery_advisor_threshold_review(
        evidence_path=args.evidence_path,
        output_path=args.output_path,
        run_id=args.run_id,
        created_at=args.created_at,
    )
    print(json.dumps(review, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
