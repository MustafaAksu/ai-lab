#!/usr/bin/env python3
"""Write a manual ContextAdmissionVerdict JSON artifact.

This script records whether a context item is admissible, warning-only, or
excluded. It does not yet modify context assembly.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.context_admission import (  # noqa: E402
    ContextAdmissionVerdict,
    VALID_ADMISSION_DECISIONS,
    VALID_FRESHNESS_STATES,
    VALID_SUBSTRATES,
    VALID_WARRANT_STATES,
)
from ai_lab.documentation.context_pack import VALID_CONTEXT_ITEM_TYPES  # noqa: E402


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--target-item-id", required=True)
    parser.add_argument("--target-item-type", required=True, choices=sorted(VALID_CONTEXT_ITEM_TYPES))
    parser.add_argument("--decision", required=True, choices=sorted(VALID_ADMISSION_DECISIONS))
    parser.add_argument("--freshness-state", required=True, choices=sorted(VALID_FRESHNESS_STATES))
    parser.add_argument("--warrant-state", required=True, choices=sorted(VALID_WARRANT_STATES))
    parser.add_argument("--author", required=True)
    parser.add_argument("--substrate", required=True, choices=sorted(VALID_SUBSTRATES))
    parser.add_argument("--reason", required=True)
    parser.add_argument("--output", required=True)

    parser.add_argument("--verdict-id")
    parser.add_argument("--created-at")
    parser.add_argument("--evidence-id", action="append")
    parser.add_argument("--evidence-path", action="append")
    parser.add_argument("--citation", action="append")
    parser.add_argument("--expires-at")
    parser.add_argument("--note")

    return parser


def main() -> int:
    args = _build_parser().parse_args()
    created_at = args.created_at or _now_iso()

    if args.verdict_id:
        verdict = ContextAdmissionVerdict(
            verdict_id=args.verdict_id,
            target_item_id=args.target_item_id,
            target_item_type=args.target_item_type,
            decision=args.decision,
            freshness_state=args.freshness_state,
            warrant_state=args.warrant_state,
            author=args.author,
            substrate=args.substrate,
            created_at=created_at,
            reason=args.reason,
            evidence_ids=tuple(args.evidence_id or []),
            evidence_paths=tuple(args.evidence_path or []),
            citations=tuple(args.citation or []),
            expires_at=args.expires_at,
            note=args.note,
        )
    else:
        verdict = ContextAdmissionVerdict.build(
            target_item_id=args.target_item_id,
            target_item_type=args.target_item_type,
            decision=args.decision,
            freshness_state=args.freshness_state,
            warrant_state=args.warrant_state,
            author=args.author,
            substrate=args.substrate,
            created_at=created_at,
            reason=args.reason,
            evidence_ids=tuple(args.evidence_id or []),
            evidence_paths=tuple(args.evidence_path or []),
            citations=tuple(args.citation or []),
            expires_at=args.expires_at,
            note=args.note,
        )

    output = Path(args.output)
    verdict.write_json(output)

    print(f"Saved context admission verdict: {output}")
    print(f"verdict_id: {verdict.verdict_id}")
    print(f"target: {verdict.target_item_id} ({verdict.target_item_type})")
    print(f"decision: {verdict.decision}")
    print(f"freshness_state: {verdict.freshness_state}")
    print(f"warrant_state: {verdict.warrant_state}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
