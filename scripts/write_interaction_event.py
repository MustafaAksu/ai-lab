#!/usr/bin/env python3
"""Write a manual InteractionLogEvent JSON artifact.

This script records one raw interaction/process event as structured memory.
It hashes optional raw request/response text instead of storing it.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_lab.documentation.interaction_log import (  # noqa: E402
    InteractionLogEvent,
    VALID_ACCESS_LEVELS,
    VALID_EVENT_TYPES,
    VALID_REDACTION_LEVELS,
    VALID_ROLES,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_optional_text(value: str | None, file_path: str | None) -> str | None:
    if value is not None and file_path is not None:
        raise SystemExit("Use either direct text or file input, not both.")
    if file_path is not None:
        return Path(file_path).read_text()
    return value


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--episode-id", required=True)
    parser.add_argument("--turn-id", required=True, type=int)
    parser.add_argument("--event-type", required=True, choices=sorted(VALID_EVENT_TYPES))
    parser.add_argument("--role", required=True, choices=sorted(VALID_ROLES))
    parser.add_argument("--actor", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--output", required=True)

    parser.add_argument("--event-id")
    parser.add_argument("--created-at", default=_now_iso())
    parser.add_argument("--request-text")
    parser.add_argument("--request-file")
    parser.add_argument("--response-text")
    parser.add_argument("--response-file")
    parser.add_argument("--prompt-manifest-id")
    parser.add_argument("--selected-context-manifest-id")
    parser.add_argument("--artifact-id", action="append")
    parser.add_argument("--commit-hash")
    parser.add_argument("--topic", action="append")
    parser.add_argument("--scope", default="default")
    parser.add_argument("--namespace", default="public")
    parser.add_argument("--access-level", choices=sorted(VALID_ACCESS_LEVELS), default="public")
    parser.add_argument(
        "--redaction-level",
        choices=sorted(VALID_REDACTION_LEVELS),
        default="none",
    )
    parser.add_argument("--model-used")
    parser.add_argument("--model-version")
    parser.add_argument("--tokens-prompt", type=int)
    parser.add_argument("--tokens-completion", type=int)
    parser.add_argument("--duration-ms", type=int)
    parser.add_argument("--outcome-code")
    parser.add_argument("--error-code")
    parser.add_argument("--error-message")

    return parser


def main() -> int:
    args = _build_parser().parse_args()

    request_text = _read_optional_text(args.request_text, args.request_file)
    response_text = _read_optional_text(args.response_text, args.response_file)

    provisional_id = args.event_id or "EVT-PENDING"

    event = InteractionLogEvent.from_text(
        event_id=provisional_id,
        episode_id=args.episode_id,
        turn_id=args.turn_id,
        created_at=args.created_at,
        event_type=args.event_type,
        role=args.role,
        actor=args.actor,
        summary=args.summary,
        request_text=request_text,
        response_text=response_text,
        prompt_manifest_id=args.prompt_manifest_id,
        selected_context_manifest_id=args.selected_context_manifest_id,
        artifact_ids=tuple(args.artifact_id or []),
        commit_hash=args.commit_hash,
        topics=tuple(args.topic or []),
        scope=args.scope,
        namespace=args.namespace,
        access_level=args.access_level,
        redaction_level=args.redaction_level,
        model_used=args.model_used,
        model_version=args.model_version,
        tokens_prompt=args.tokens_prompt,
        tokens_completion=args.tokens_completion,
        duration_ms=args.duration_ms,
        outcome_code=args.outcome_code,
        error_code=args.error_code,
        error_message=args.error_message,
    )

    if args.event_id is None:
        seed = "|".join(
            [
                event.episode_id,
                str(event.turn_id),
                event.created_at,
                event.event_type,
                event.role,
                event.actor,
                event.summary,
                event.request_text_hash or "",
                event.response_text_hash or "",
            ]
        )
        import hashlib

        event = InteractionLogEvent(
            **{
                **event.to_dict(),
                "event_id": f"EVT-{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:12]}",
            }
        )

    output = Path(args.output)
    event.write_json(output)

    print(f"Saved interaction event: {output}")
    print(f"event_id: {event.event_id}")
    if event.request_text_hash:
        print(f"request_text_hash: {event.request_text_hash}")
    if event.response_text_hash:
        print(f"response_text_hash: {event.response_text_hash}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
