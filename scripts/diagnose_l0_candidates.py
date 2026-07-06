from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.l0_candidate_diagnostics import (
    context_item_ids_from_manifest_path,
    l0_candidate_diagnostics,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report read-only candidate L0 summary sources."
    )
    parser.add_argument(
        "--l0-store",
        type=Path,
        default=Path("docs/memory/l0"),
        help="Directory containing L0 summary JSON records.",
    )
    parser.add_argument(
        "--context-item-id",
        action="append",
        default=[],
        help="Optional context item ID to mark against candidate L0 chunk IDs.",
    )
    parser.add_argument(
        "--context-manifest",
        type=Path,
        default=None,
        help=(
            "Optional saved context-pack JSON manifest. Its selected item_id "
            "values are used only for read-only candidate matching."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output JSON path. Defaults to stdout.",
    )

    args = parser.parse_args()

    context_item_ids = tuple(args.context_item_id)
    manifest_details: dict[str, object] = {}

    if args.context_manifest is not None:
        manifest_item_ids, manifest_details = context_item_ids_from_manifest_path(
            args.context_manifest
        )
        context_item_ids = (*manifest_item_ids, *context_item_ids)

    result = l0_candidate_diagnostics(
        l0_store=args.l0_store,
        context_item_ids=context_item_ids,
    )
    result.update(manifest_details)

    output = json.dumps(result, indent=2, sort_keys=True) + "\n"

    if args.output is None:
        print(output, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"Saved L0 candidate diagnostics: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
