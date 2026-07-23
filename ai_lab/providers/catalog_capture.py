"""Catalog capture: live fetch (opt-in) and fixture replay (default).

Admitted by WARR-20260723-0001 as part of PLAN-20260723-0001.

Live network access is opt-in and disabled by default. No test may require
it. The default path builds snapshots from recorded fixtures under
``tests/fixtures/catalog/``, which carry their own capture dates so that
the freshness validator reports currency against the recording rather than
assuming it.

What live capture can and cannot establish
------------------------------------------
Fetching a provider's own catalog establishes what the provider says about
itself at a moment in time. It does not establish that the claim is true.
Every capture produced here therefore carries
``source_type: provider_self_report`` and
``content_evidence_status: self_asserted``, and the schema forbids
anything stronger (ABS-0004 v5).

``channel_authentication_status`` is currently recorded as
``unverifiable``: this slice does not inspect certificate chains or key
digests, so nothing has been independently established about the channel.
Recording ``verified_current`` here without performing that check would be
exactly the overclaim P6 forbids. Channel authentication is representable
now and performed later.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from ai_lab.documentation.verification_outcome import UNVERIFIABLE
from ai_lab.providers.catalog import (
    EVIDENCE_SELF_ASSERTED,
    SOURCE_PROVIDER_SELF_REPORT,
    build_assertion,
    build_capture,
    build_endpoint_identity,
    build_model_identity,
    build_snapshot,
    canonical_catalog_json,
    catalog_relative_path,
    validate_catalog_record,
)


LIVE_CAPTURE_ENV = "AI_LAB_ENABLE_LIVE_CATALOG"
FIXTURE_DIR = "tests/fixtures/catalog"


class CatalogCaptureError(RuntimeError):
    """Raised when live capture is attempted while disabled, or fails."""


def live_capture_enabled() -> bool:
    """True only when explicitly enabled. Default is off."""

    return os.getenv(LIVE_CAPTURE_ENV, "").strip().lower() in {"1", "true", "yes"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def snapshot_from_payload(
    *,
    payload: Mapping[str, Any],
    operating_organization: str,
    endpoint_identifier: str,
    observed_at: str,
    source_set: str,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    """Build endpoint identity, snapshot, and model identities from a payload.

    Pure: takes an already-retrieved payload, performs no I/O. The same
    function serves live capture and fixture replay, so the offline tests
    exercise the identical parsing path.
    """

    entries = payload.get("data")
    if not isinstance(entries, list) or not entries:
        raise CatalogCaptureError("payload has no model entries")

    endpoint = build_endpoint_identity(
        operating_organization=operating_organization,
        endpoint_identifier=endpoint_identifier,
    )

    identities: list[dict[str, Any]] = []
    assertions: list[dict[str, Any]] = []
    for entry in entries:
        api_name = entry.get("id")
        if not isinstance(api_name, str) or not api_name.strip():
            raise CatalogCaptureError("payload entry lacks an id")

        identity = build_model_identity(
            originator_id=str(entry.get("owned_by") or operating_organization),
            canonical_name=api_name,
            release_identity=str(entry.get("release") or "unknown"),
        )
        identities.append(identity)
        assertions.append(
            build_assertion(
                assertion_subject=api_name,
                assertion_predicate="resolves_to",
                assertion_value_or_target=identity["record_id"],
                valid_from=observed_at,
                source=source_set,
            )
        )
        # No context_limit assertion is emitted. The first live capture
        # (2026-07-23) confirmed that neither provider's models-list response
        # carries a context window, so a branch keyed on one would be
        # unreachable from live capture and reachable only from a fixture that
        # invented the field. Context limits are a real catalog claim, but they
        # require a source that actually publishes them; until such a source is
        # admitted, AI-Lab records no claim about them rather than a claim it
        # cannot obtain.

    snapshot = build_snapshot(
        service_endpoint_id=endpoint["record_id"],
        observed_at=observed_at,
        assertions=assertions,
        source_set=source_set,
    )
    return endpoint, snapshot, identities


def capture_from_payload(
    *,
    payload: Mapping[str, Any],
    raw_text: str,
    snapshot: Mapping[str, Any],
    capture_method: str,
    captured_at: str,
    capturing_executor: str,
) -> dict[str, Any]:
    """Build the capture record for a retrieved payload.

    The evidence class is fixed by what this path can establish: the
    provider's own report, self-asserted, over a channel nothing has yet
    authenticated.
    """

    return build_capture(
        snapshot_id=snapshot["record_id"],
        capture_method=capture_method,
        source_type=SOURCE_PROVIDER_SELF_REPORT,
        captured_at=captured_at,
        capture_success=True,
        capturing_executor=capturing_executor,
        payload=raw_text,
        channel_authentication_status=UNVERIFIABLE,
        content_evidence_status=EVIDENCE_SELF_ASSERTED,
    )


def load_fixture(name: str, repo_root: Path | str = ".") -> dict[str, Any]:
    """Load a recorded catalog payload with its capture metadata."""

    path = Path(repo_root) / FIXTURE_DIR / f"{name}.json"
    if not path.exists():
        raise CatalogCaptureError(f"no recorded fixture named {name!r}")
    fixture = json.loads(path.read_text(encoding="utf-8"))
    for field in ("recorded_at", "operating_organization", "endpoint_identifier", "payload"):
        if field not in fixture:
            raise CatalogCaptureError(f"fixture {name!r} lacks {field}")
    return fixture


def capture_from_fixture(
    name: str, repo_root: Path | str = "."
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    """Replay a recorded catalog payload. No network access.

    Returns (endpoint, snapshot, capture, identities). The snapshot's
    observed_at is the fixture's recording date, never the current time,
    so freshness is assessed against when the payload was actually seen.
    """

    fixture = load_fixture(name, repo_root)
    raw_text = json.dumps(fixture["payload"], sort_keys=True)
    endpoint, snapshot, identities = snapshot_from_payload(
        payload=fixture["payload"],
        operating_organization=fixture["operating_organization"],
        endpoint_identifier=fixture["endpoint_identifier"],
        observed_at=fixture["recorded_at"],
        source_set=f"recorded fixture {name}",
    )
    capture = capture_from_payload(
        payload=fixture["payload"],
        raw_text=raw_text,
        snapshot=snapshot,
        capture_method=f"fixture_replay:{name}",
        captured_at=fixture["recorded_at"],
        capturing_executor="tool:capture_from_fixture",
    )
    return endpoint, snapshot, capture, identities


def capture_live(
    *,
    fetcher,
    operating_organization: str,
    endpoint_identifier: str,
    capturing_executor: str = "tool:capture_live",
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    """Capture a provider catalog over the network. Opt-in only.

    ``fetcher`` is a zero-argument callable returning the decoded payload;
    injecting it keeps this function testable without network access and
    keeps transport concerns out of the catalog module.
    """

    if not live_capture_enabled():
        raise CatalogCaptureError(
            f"live catalog capture is disabled; set {LIVE_CAPTURE_ENV}=1 to enable it"
        )

    observed_at = _now_iso()
    payload = fetcher()
    raw_text = json.dumps(payload, sort_keys=True)
    endpoint, snapshot, identities = snapshot_from_payload(
        payload=payload,
        operating_organization=operating_organization,
        endpoint_identifier=endpoint_identifier,
        observed_at=observed_at,
        source_set=f"live fetch {endpoint_identifier}",
    )
    capture = capture_from_payload(
        payload=payload,
        raw_text=raw_text,
        snapshot=snapshot,
        capture_method="live_fetch",
        captured_at=observed_at,
        capturing_executor=capturing_executor,
    )
    return endpoint, snapshot, capture, identities


def write_catalog_records(
    records: Sequence[Mapping[str, Any]], repo_root: Path | str
) -> list[Path]:
    """Validate and write catalog records to their deterministic paths."""

    written: list[Path] = []
    for record in records:
        validate_catalog_record(record)
        target = Path(repo_root) / catalog_relative_path(record["record_id"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(canonical_catalog_json(record), encoding="utf-8")
        written.append(target)
    return written
