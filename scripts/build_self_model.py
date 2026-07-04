from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.self_model import build_self_model_index


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build aggregation-only SELF_MODEL.json."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/self_model/SELF_MODEL.json"),
    )
    parser.add_argument(
        "--generated-at",
        default=None,
        help="Optional fixed generated_at timestamp for deterministic tests.",
    )

    args = parser.parse_args()

    index = build_self_model_index(
        repo_root=args.repo_root,
        generated_at=args.generated_at,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Saved self-model index: {args.output}")
    print(f"repo_head: {index['repo_head']}")
    print(f"capabilities: {len(index['capabilities'])}")
    print(f"open_gaps: {len(index['open_gaps'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
