from __future__ import annotations

from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.artifact_history import (
    ArtifactHistoryError,
    discover_artifacts,
    format_artifact_history,
    format_artifact_lineage,
    format_artifact_source_tree,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Show AI-Lab comparison, synthesis, and abstraction artifact history."
    )
    parser.add_argument(
        "--comparison-dir",
        type=Path,
        default=Path("docs/comparisons"),
        help="Directory containing COMP artifacts.",
    )
    parser.add_argument(
        "--abstraction-dir",
        type=Path,
        default=Path("docs/abstractions"),
        help="Directory containing ABS artifacts.",
    )
    parser.add_argument(
        "--lineage",
        help="Show single-chain lineage for a specific artifact ID.",
    )
    parser.add_argument(
        "--source-tree",
        help="Show recursive source tree for a specific artifact ID.",
    )

    args = parser.parse_args()

    records = discover_artifacts(args.comparison_dir, args.abstraction_dir)

    if args.lineage:
        try:
            print(format_artifact_lineage(records, args.lineage))
        except ArtifactHistoryError as error:
            print(f"Could not show lineage: {error}")
            return 1

        return 0

    if args.source_tree:
        try:
            print(format_artifact_source_tree(records, args.source_tree))
        except ArtifactHistoryError as error:
            print(f"Could not show source tree: {error}")
            return 1

        return 0

    print(format_artifact_history(records))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
