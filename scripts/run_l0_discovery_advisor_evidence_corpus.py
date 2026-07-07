#!/usr/bin/env python3
"""Write deterministic evidence corpus output for L0 discovery advisor evaluation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.l0_discovery_advisor_evidence_corpus import (
    DEFAULT_OUTPUT_ROOT,
    write_l0_discovery_advisor_evidence_corpus,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Write deterministic saved-manifest fixtures and diagnostic-only evidence "
            "for the L0 discovery advisor evaluator."
        )
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory where corpus manifests and evidence.json are written.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional run ID for the evidence and nested evaluation records.",
    )
    parser.add_argument(
        "--created-at",
        default=None,
        help="Optional ISO timestamp for deterministic outputs.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    evidence = write_l0_discovery_advisor_evidence_corpus(
        output_root=args.output_root,
        run_id=args.run_id,
        created_at=args.created_at,
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
