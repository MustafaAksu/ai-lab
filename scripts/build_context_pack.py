from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.artifact_history import discover_artifacts
from ai_lab.documentation.context_pack_builder import build_latest_context_manifest
from ai_lab.documentation.context_pack_renderer import render_context_pack_markdown


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
        "--scope",
        default=None,
        help="Optional L1 memory scope/stream to select from.",
    )
    parser.add_argument(
        "--require-admission",
        action="store_true",
        help="Require selected context items to have an admitting admission verdict.",
    )
    parser.add_argument(
        "--max-warning-admissions",
        type=int,
        default=None,
        help=(
            "Optional cap for admit_with_warning items when using latest-context "
            "assembly. Defaults to no cap."
        ),
    )
    parser.add_argument(
        "--pipeline-run-id",
        default=None,
        help="Optional pipeline run ID.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output file. Prints to stdout when omitted.",
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=None,
        help="Optional JSON manifest output file.",
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
            l1_scope=args.scope,
            require_admission=args.require_admission,
            max_warning_admissions=args.max_warning_admissions,
        )
    else:
        raise ValueError(f"Unsupported policy: {args.policy}")

    manifest_json = json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n"

    if args.format == "markdown":
        output = render_context_pack_markdown(manifest)
    else:
        output = manifest_json

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    if args.manifest_output:
        args.manifest_output.parent.mkdir(parents=True, exist_ok=True)
        args.manifest_output.write_text(manifest_json, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
