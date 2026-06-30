from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.citations import CitationError, parse_citation


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an AI-Lab citation in cid@version|span format."
    )
    parser.add_argument(
        "citation",
        help="Citation string, e.g. 3ac9f2b1d0af@a1c2d3e|b:1024-2047",
    )

    args = parser.parse_args()

    try:
        citation = parse_citation(args.citation)
    except CitationError as error:
        print(f"Invalid citation: {error}")
        return 1

    print("Valid citation")
    print(f"cid: {citation.cid}")
    print(f"version: {citation.version}")
    print(f"unit: {citation.span.unit}")
    print(f"start: {citation.span.start}")
    print(f"end: {citation.span.end}")

    if citation.span.tokenizer:
        print(f"tokenizer: {citation.span.tokenizer}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
