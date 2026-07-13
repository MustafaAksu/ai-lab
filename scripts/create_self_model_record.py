#!/usr/bin/env python3
"""
Create one canonical self-model record from a human-authored JSON payload.

The payload must contain all substantive fields required by the record's
validator. The CLI may fill only the mechanical record ID.

Suggested IDs are local max-suffix suggestions. They are not transactional and
do not protect against concurrent branches or worktrees. If a merge introduces
an ID collision, rebase, request a new suggestion, and recreate the record.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.self_model import (  # noqa: E402
    SELF_MODEL_RECORD_SPECS,
    SelfModelError,
    record_type_spec,
    suggest_next_record_id,
    write_new_self_model_record,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "record_type",
        choices=sorted(
            spec.record_type
            for spec in SELF_MODEL_RECORD_SPECS
        ),
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help=(
            "JSON payload containing all substantive fields. "
            "The type-specific ID field may be omitted."
        ),
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
    )
    parser.add_argument(
        "--record-id",
        help=(
            "Explicit record ID. When omitted, use a local "
            "max-suffix suggestion."
        ),
    )
    parser.add_argument(
        "--date",
        dest="record_date",
        help=(
            "Date for PLAN, VERIFY, WARR, and DECISION IDs. "
            "Use YYYY-MM-DD or YYYYMMDD. Defaults to current UTC date."
        ),
    )

    return parser


def _read_payload(
    parser: argparse.ArgumentParser,
    path: Path,
) -> dict[str, object]:
    try:
        data = json.loads(
            path.read_text(encoding="utf-8")
        )
    except OSError as error:
        parser.error(
            f"could not read input payload: {error}"
        )
    except json.JSONDecodeError as error:
        parser.error(
            f"input payload is invalid JSON: {error}"
        )

    if not isinstance(data, dict):
        parser.error(
            "input payload must be a JSON object"
        )

    return data


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    payload = _read_payload(
        parser,
        args.input,
    )
    spec = record_type_spec(args.record_type)

    payload_identifier = payload.get(spec.id_field)

    if (
        payload_identifier is not None
        and not isinstance(payload_identifier, str)
    ):
        parser.error(
            f"{spec.id_field} must be a string"
        )

    if (
        args.record_id is not None
        and payload_identifier is not None
        and args.record_id != payload_identifier
    ):
        parser.error(
            f"--record-id conflicts with "
            f"payload {spec.id_field}"
        )

    suggested = False

    if args.record_id is not None:
        record_id = args.record_id
    elif isinstance(payload_identifier, str):
        record_id = payload_identifier
    else:
        try:
            record_id = suggest_next_record_id(
                args.record_type,
                repo_root=args.repo_root,
                record_date=args.record_date,
            )
        except SelfModelError as error:
            parser.error(str(error))

        suggested = True

    payload[spec.id_field] = record_id

    try:
        output = write_new_self_model_record(
            args.repo_root,
            args.record_type,
            payload,
        )
    except SelfModelError as error:
        parser.error(str(error))

    relative_output = output.relative_to(
        args.repo_root.resolve()
    )

    print(
        f"Saved self-model record: {relative_output}"
    )
    print(f"record_type: {args.record_type}")
    print(f"record_id: {record_id}")
    print(
        "id_source: "
        + (
            "local_max_suffix_suggestion"
            if suggested
            else "explicit"
        )
    )
    print(
        "ID allocation is local and non-transactional; "
        "rebase and rerun if a merge introduces a collision."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
