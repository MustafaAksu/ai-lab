from __future__ import annotations

from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.artifact_history import (
    discover_artifacts,
    format_artifact_history,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Show AI-Lab comparison and synthesis artifact history."
    )
    parser.add_argument(
        "--comparison-dir",
        type=Path,
        default=Path("docs/comparisons"),
        help="Directory containing COMP artifacts.",
    )

    args = parser.parse_args()

    records = discover_artifacts(args.comparison_dir)
    print(format_artifact_history(records))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
