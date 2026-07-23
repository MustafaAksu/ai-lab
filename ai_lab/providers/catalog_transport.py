"""Transport for live catalog capture (ABS-0004 v5 Slice B).

Completes the live-fetch scope item of PLAN-20260723-0001: the capture
mechanism in ``catalog_capture`` takes an injected fetcher, and this module
supplies real ones. Recorded as a correction, not a quiet patch: the
original completion verification claimed the fetch path was delivered when
only the mechanism existed. See VERIFY-20260723-0002.

Nothing here runs unless ``AI_LAB_ENABLE_LIVE_CATALOG=1``; the guard lives
in ``catalog_capture.capture_live`` and is checked again here before any
client is constructed, so a disabled run never touches credentials.

The payload is retained verbatim alongside the derived records (a
WARR-20260723-0002 condition): a capture whose evidence cannot be
re-examined is a claim about a fetch, not a record of one.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from ai_lab.providers.catalog_capture import (
    LIVE_CAPTURE_ENV,
    CatalogCaptureError,
    capture_live,
    live_capture_enabled,
    write_catalog_records,
)


PAYLOAD_DIR = "docs/catalog/payloads"

SURFACES = {
    "openai": {
        "operating_organization": "openai",
        "endpoint_identifier": "openai.responses",
    },
    "anthropic": {
        "operating_organization": "anthropic",
        "endpoint_identifier": "anthropic.messages",
    },
}


def _entry_to_dict(entry: Any) -> dict[str, Any]:
    """Normalize one SDK model entry to the payload shape.

    Unknown attributes are ignored rather than guessed: a field absent from
    a provider's response is absent from the record, not defaulted.
    """

    if isinstance(entry, Mapping):
        source = dict(entry)
    else:
        source = {
            key: getattr(entry, key)
            for key in ("id", "owned_by", "display_name", "created_at", "type")
            if getattr(entry, key, None) is not None
        }

    normalized: dict[str, Any] = {}
    identifier = source.get("id")
    if identifier is not None:
        normalized["id"] = str(identifier)
    owner = source.get("owned_by")
    if owner is not None:
        normalized["owned_by"] = str(owner)
    for optional in ("display_name", "type"):
        if source.get(optional) is not None:
            normalized[optional] = str(source[optional])
    created = source.get("created_at")
    if created is not None:
        normalized["created_at"] = str(created)
    return normalized


def openai_models_fetcher() -> Callable[[], dict[str, Any]]:
    """Fetcher for the OpenAI models list. Constructs no client until called."""

    def fetch() -> dict[str, Any]:
        from openai import OpenAI

        from ai_lab.config import read_api_key

        client = OpenAI(api_key=read_api_key())
        listing = client.models.list()
        return {"data": [_entry_to_dict(entry) for entry in listing.data]}

    return fetch


def anthropic_models_fetcher() -> Callable[[], dict[str, Any]]:
    """Fetcher for the Anthropic models list. Constructs no client until called."""

    def fetch() -> dict[str, Any]:
        from anthropic import Anthropic

        from ai_lab.config import read_claude_api_key

        client = Anthropic(api_key=read_claude_api_key())
        listing = client.models.list()
        return {"data": [_entry_to_dict(entry) for entry in listing.data]}

    return fetch


FETCHERS = {
    "openai": openai_models_fetcher,
    "anthropic": anthropic_models_fetcher,
}


def retain_payload(
    *, payload: Mapping[str, Any], surface: str, captured_at: str, repo_root: Path | str
) -> Path:
    """Write the retrieved payload verbatim beside the derived records."""

    stamp = captured_at.replace(":", "").replace("-", "").split(".")[0]
    target = Path(repo_root) / PAYLOAD_DIR / f"{surface}-{stamp}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "surface": surface,
        "captured_at": captured_at,
        "provenance": (
            "Verbatim provider models-list response retrieved by "
            "ai_lab.providers.catalog_transport under "
            "AI_LAB_ENABLE_LIVE_CATALOG. Provider self-report: the provider "
            "describing its own catalog. Not independently corroborated."
        ),
        "payload": dict(payload),
    }
    target.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def run_live_capture(
    *,
    surface: str,
    repo_root: Path | str,
    fetcher: Callable[[], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Capture one provider catalog, retain the payload, write the records.

    Returns a summary. Raises CatalogCaptureError if live capture is
    disabled or the surface is unknown; constructs no client in that case.
    """

    if surface not in SURFACES:
        raise CatalogCaptureError(
            f"unknown surface {surface!r}; known: {sorted(SURFACES)}"
        )
    if not live_capture_enabled():
        raise CatalogCaptureError(
            f"live catalog capture is disabled; set {LIVE_CAPTURE_ENV}=1 to enable it"
        )

    config = SURFACES[surface]
    fetch = fetcher or FETCHERS[surface]()

    retained: dict[str, Any] = {}

    def recording_fetch() -> dict[str, Any]:
        payload = fetch()
        retained["payload"] = payload
        return payload

    endpoint, snapshot, capture, identities = capture_live(
        fetcher=recording_fetch,
        operating_organization=config["operating_organization"],
        endpoint_identifier=config["endpoint_identifier"],
        capturing_executor="tool:catalog_transport",
    )

    payload_path = retain_payload(
        payload=retained.get("payload", {}),
        surface=surface,
        captured_at=capture["captured_at"],
        repo_root=repo_root,
    )
    written = write_catalog_records([endpoint, snapshot, capture, *identities], repo_root)

    return {
        "surface": surface,
        "endpoint_id": endpoint["record_id"],
        "snapshot_id": snapshot["record_id"],
        "capture_id": capture["record_id"],
        "identity_count": len(identities),
        "assertion_count": len(snapshot["assertions"]),
        "payload_path": str(payload_path),
        "record_paths": [str(path) for path in written],
        "captured_at": capture["captured_at"],
        "content_evidence_status": capture["content_evidence_status"],
        "channel_authentication_status": capture["channel_authentication_status"],
    }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
