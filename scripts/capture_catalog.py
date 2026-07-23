#!/usr/bin/env python3
"""Run one governed live catalog capture.

Requires AI_LAB_ENABLE_LIVE_CATALOG=1. Retains the provider payload
verbatim and writes the derived catalog records, then prints a summary
for the governance record.

    AI_LAB_ENABLE_LIVE_CATALOG=1 python scripts/capture_catalog.py anthropic

Every capture is provider self-report: the provider describing its own
catalog. Content evidence is self_asserted and channel authentication is
unverifiable, because this slice inspects no certificate chain.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.providers.catalog_capture import (  # noqa: E402
    LIVE_CAPTURE_ENV,
    CatalogCaptureError,
    live_capture_enabled,
)
from ai_lab.providers.catalog_transport import SURFACES, run_live_capture  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("surface", choices=sorted(SURFACES))
    parser.add_argument(
        "--repo-root", default=str(PROJECT_ROOT), help="repository root for writes"
    )
    args = parser.parse_args()

    if not live_capture_enabled():
        print(
            f"Live catalog capture is disabled. Set {LIVE_CAPTURE_ENV}=1 to enable it.",
            file=sys.stderr,
        )
        return 2

    try:
        summary = run_live_capture(surface=args.surface, repo_root=Path(args.repo_root))
    except CatalogCaptureError as error:
        print(f"Capture failed: {error}", file=sys.stderr)
        return 1

    print(json.dumps(summary, indent=2, sort_keys=True))
    print(
        "\nProvider self-report: content evidence is "
        f"{summary['content_evidence_status']}, channel authentication is "
        f"{summary['channel_authentication_status']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
