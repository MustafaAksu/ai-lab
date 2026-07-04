from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai_lab.documentation.self_model import audit_self_model_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit generated SELF_MODEL.json freshness.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--index-path",
        type=Path,
        default=None,
        help="Optional path to SELF_MODEL.json. Defaults under repo root.",
    )
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Return non-zero when warnings are present.",
    )

    args = parser.parse_args()

    result = audit_self_model_index(
        repo_root=args.repo_root,
        index_path=args.index_path,
    )

    print(json.dumps(result, indent=2, sort_keys=True))

    if not result["ok"]:
        return 1

    findings = result.get("findings", [])
    if args.fail_on_warn and any(
        isinstance(finding, dict) and finding.get("severity") == "warn"
        for finding in findings
    ):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
