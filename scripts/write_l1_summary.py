#!/usr/bin/env python3
"""Write a manual EpisodeL1Summary JSON artifact.

This is intentionally manual. It does not call providers, generate summaries,
persist graph edges, or modify context assembly. It gives AI-Lab a safe
write-back path for fresh L1 memory artifacts.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.interaction_log import EpisodeL1Summary


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _tuple(values: list[str] | None) -> tuple[str, ...]:
    return tuple(values or [])


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--episode-id", required=True)
    parser.add_argument("--summary-text", required=True)
    parser.add_argument("--source-event-id", action="append", required=True)
    parser.add_argument("--output", required=True)

    parser.add_argument("--l1-id")
    parser.add_argument("--created-at", default=_now_iso())
    parser.add_argument("--summary-version", default="v1")
    parser.add_argument("--citation", action="append", default=[])
    parser.add_argument("--key-decision", action="append")
    parser.add_argument("--completed-work", action="append")
    parser.add_argument("--open-question", action="append")
    parser.add_argument("--risk", action="append")
    parser.add_argument("--next-action", action="append")
    parser.add_argument("--topic", action="append")
    parser.add_argument("--scope", default="default")
    parser.add_argument("--generation-model")
    parser.add_argument("--generation-prompt-id")
    parser.add_argument("--coverage-score", type=float, default=0.0)
    parser.add_argument(
        "--freshness-state",
        choices=("fresh", "stale", "unknown"),
        default="unknown",
    )
    parser.add_argument("--ttl-until")
    parser.add_argument("--namespace", default="public")
    parser.add_argument(
        "--access-level",
        choices=("public", "internal", "private"),
        default="public",
    )
    parser.add_argument(
        "--redaction-level",
        choices=("none", "partial", "full"),
        default="none",
    )
    parser.add_argument(
        "--print-edge-seeds",
        action="store_true",
        help="Print future graph-edge seed records after writing.",
    )

    return parser


def main() -> int:
    args = _build_parser().parse_args()

    provisional_id = args.l1_id or "L1-PENDING"

    summary = EpisodeL1Summary(
        l1_id=provisional_id,
        episode_id=args.episode_id,
        created_at=args.created_at,
        summary_version=args.summary_version,
        summary_text=args.summary_text,
        source_event_ids=tuple(args.source_event_id),
        citations=tuple(args.citation),
        key_decisions=_tuple(args.key_decision),
        completed_work=_tuple(args.completed_work),
        open_questions=_tuple(args.open_question),
        risks=_tuple(args.risk),
        next_actions=_tuple(args.next_action),
        topics=_tuple(args.topic),
        scope=args.scope,
        generation_model=args.generation_model,
        generation_prompt_id=args.generation_prompt_id,
        coverage_score=args.coverage_score,
        freshness_state=args.freshness_state,
        ttl_until=args.ttl_until,
        namespace=args.namespace,
        access_level=args.access_level,
        redaction_level=args.redaction_level,
    )

    if args.l1_id is None:
        summary = EpisodeL1Summary(
            **{
                **summary.to_dict(),
                "l1_id": f"L1-{summary.stable_content_hash()[:12]}",
                "content_hash": summary.stable_content_hash(),
            }
        )
    elif summary.content_hash is None:
        summary = EpisodeL1Summary(
            **{
                **summary.to_dict(),
                "content_hash": summary.stable_content_hash(),
            }
        )

    output = Path(args.output)
    summary.write_json(output)

    print(f"Saved L1 summary: {output}")
    print(f"l1_id: {summary.l1_id}")
    print(f"content_hash: {summary.content_hash}")

    if args.print_edge_seeds:
        print("future_edge_seed_records:")
        for seed in summary.future_edge_seed_records():
            print(f"- {seed['source_id']} {seed['predicate']} {seed['target_id']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
