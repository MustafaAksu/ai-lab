from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.artifact_history import discover_artifacts
from ai_lab.documentation.context_pack_builder import build_latest_context_manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build an AI-Lab context pack manifest."
    )
    parser.add_argument(
        "task",
        help="Task the context pack is being assembled for.",
    )
    parser.add_argument(
        "--policy",
        choices=["latest_context"],
        default="latest_context",
        help="Context assembly policy.",
    )
    parser.add_argument(
        "--comparison-dir",
        type=Path,
        default=Path("docs/comparisons"),
        help="Directory containing comparison and synthesis artifacts.",
    )
    parser.add_argument(
        "--abstraction-dir",
        type=Path,
        default=Path("docs/abstractions"),
        help="Directory containing abstraction artifacts.",
    )
    parser.add_argument(
        "--token-budget",
        type=int,
        default=None,
        help="Optional token budget for the context pack.",
    )
    parser.add_argument(
        "--model-target",
        default=None,
        help="Optional target model for the context pack.",
    )
    parser.add_argument(
        "--pipeline-run-id",
        default=None,
        help="Optional pipeline run ID.",
    )

    args = parser.parse_args()

    records = discover_artifacts(
        comparison_dir=args.comparison_dir,
        abstraction_dir=args.abstraction_dir,
    )

    if args.policy == "latest_context":
        manifest = build_latest_context_manifest(
            task=args.task,
            records=records,
            token_budget=args.token_budget,
            model_target=args.model_target,
            pipeline_run_id=args.pipeline_run_id,
        )
    else:
        raise ValueError(f"Unsupported policy: {args.policy}")

    print(json.dumps(manifest.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
