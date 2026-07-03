#!/usr/bin/env python3
"""Write a manual L0 chunk summary JSON artifact.

This is intentionally manual. It does not call providers, create embeddings,
perform retrieval, validate citations outside the chunk citation itself, or
modify context assembly. It gives AI-Lab a safe bootstrap path for concrete
chunk-level L0 memory artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.chunk_reference import (
    VALID_ARTIFACT_TYPES,
    VALID_REDACTION_LEVELS,
    create_chunk_reference,
)
from ai_lab.documentation.citations import CitationSpan
from ai_lab.documentation.l0_summary import Claim, Entity, L0ChunkSummary, Risk


def _split_prefixed(value: str, field_name: str) -> tuple[str, str]:
    if ":" not in value:
        raise argparse.ArgumentTypeError(f"{field_name} must use prefix:text form.")

    prefix, text = value.split(":", 1)

    if not prefix.strip() or not text.strip():
        raise argparse.ArgumentTypeError(f"{field_name} must use prefix:text form.")

    return prefix.strip(), text.strip()


def _entity(value: str) -> Entity:
    entity_type, name = _split_prefixed(value, "entity")
    return Entity(type=entity_type, name=name)


def _claim(value: str) -> Claim:
    polarity, text = _split_prefixed(value, "claim")
    return Claim(text=text, polarity=polarity)


def _risk(value: str) -> Risk:
    severity, text = _split_prefixed(value, "risk")
    return Risk(text=text, severity=severity)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--artifact-cid", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--span-unit", choices=("b", "c", "t"), required=True)
    parser.add_argument("--span-start", type=int, required=True)
    parser.add_argument("--span-end", type=int, required=True)
    parser.add_argument("--tokenizer")

    parser.add_argument("--path")
    parser.add_argument(
        "--artifact-type",
        choices=sorted(VALID_ARTIFACT_TYPES),
        default="other",
    )
    parser.add_argument("--language")
    parser.add_argument("--embedding-id", action="append", default=[])
    parser.add_argument(
        "--redaction-level",
        choices=sorted(VALID_REDACTION_LEVELS),
        default="none",
    )

    parser.add_argument("--l0-summary", required=True)
    parser.add_argument("--keyphrase", action="append", required=True)
    parser.add_argument(
        "--entity",
        action="append",
        type=_entity,
        default=[],
        help="Entity in type:name form. Repeatable.",
    )
    parser.add_argument(
        "--claim",
        action="append",
        type=_claim,
        default=[],
        help="Claim in polarity:text form. Repeatable.",
    )
    parser.add_argument(
        "--risk",
        action="append",
        type=_risk,
        default=[],
        help="Risk in severity:text form. Repeatable.",
    )

    parser.add_argument("--created-at")
    parser.add_argument("--last-refreshed-at")
    parser.add_argument("--generator-model")
    parser.add_argument("--generator-version")
    parser.add_argument("--pipeline-run-id")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path. Defaults to docs/memory/l0/<chunk_id>.json.",
    )

    return parser


def _summary_from_args(args: argparse.Namespace) -> L0ChunkSummary:
    span = CitationSpan(
        unit=args.span_unit,
        start=args.span_start,
        end=args.span_end,
        tokenizer=args.tokenizer,
    )

    reference = create_chunk_reference(
        artifact_cid=args.artifact_cid,
        version=args.version,
        span=span,
        path=args.path,
        artifact_type=args.artifact_type,
        language=args.language,
        embedding_ids=tuple(args.embedding_id),
        redaction_level=args.redaction_level,
    )

    optional_fields: dict[str, str] = {}

    if args.created_at:
        optional_fields["created_at"] = args.created_at

    if args.last_refreshed_at:
        optional_fields["last_refreshed_at"] = args.last_refreshed_at

    return L0ChunkSummary(
        chunk_reference=reference,
        l0_summary=args.l0_summary,
        keyphrases=tuple(args.keyphrase),
        entities=tuple(args.entity),
        claims=tuple(args.claim),
        risks=tuple(args.risk),
        generator_model=args.generator_model,
        generator_version=args.generator_version,
        pipeline_run_id=args.pipeline_run_id,
        **optional_fields,
    )


def main() -> int:
    args = _build_parser().parse_args()
    summary = _summary_from_args(args)

    output = args.output or Path("docs/memory/l0") / f"{summary.chunk_reference.chunk_id}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(summary.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Saved L0 chunk summary: {output}")
    print(f"chunk_id: {summary.chunk_reference.chunk_id}")
    print(f"citation: {summary.citation}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
