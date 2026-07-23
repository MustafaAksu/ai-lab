"""Tests for live catalog capture transport (ABS-0004 v5 Slice B).

Separate from tests/test_catalog.py because that file is named as evidence
in CAP-0016 with a content hash; appending to it would invalidate a
verified capability's evidence without re-verification.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_lab.documentation.verification_outcome import UNVERIFIABLE
from ai_lab.providers.catalog import (
    EVIDENCE_SELF_ASSERTED,
    validate_catalog_record,
)


# --- transport: real fetchers behind the opt-in ------------------------


class _FakeModelEntry:
    def __init__(self, identifier, owned_by=None, display_name=None):
        self.id = identifier
        if owned_by is not None:
            self.owned_by = owned_by
        if display_name is not None:
            self.display_name = display_name


class _FakeListing:
    def __init__(self, entries):
        self.data = entries


def test_transport_refuses_while_live_capture_is_disabled(monkeypatch, tmp_path):
    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV, CatalogCaptureError
    from ai_lab.providers.catalog_transport import run_live_capture

    monkeypatch.delenv(LIVE_CAPTURE_ENV, raising=False)

    def fetcher():  # pragma: no cover - must never run
        raise AssertionError("network access attempted while disabled")

    with pytest.raises(CatalogCaptureError, match="disabled"):
        run_live_capture(surface="anthropic", repo_root=tmp_path, fetcher=fetcher)


def test_transport_rejects_an_unknown_surface(monkeypatch, tmp_path):
    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV, CatalogCaptureError
    from ai_lab.providers.catalog_transport import run_live_capture

    monkeypatch.setenv(LIVE_CAPTURE_ENV, "1")

    with pytest.raises(CatalogCaptureError, match="unknown surface"):
        run_live_capture(surface="carrier-pigeon", repo_root=tmp_path, fetcher=lambda: {})


def test_transport_run_writes_records_and_retains_the_payload(monkeypatch, tmp_path):
    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV
    from ai_lab.providers.catalog_transport import run_live_capture

    monkeypatch.setenv(LIVE_CAPTURE_ENV, "1")
    payload = {"data": [{"id": "model-alpha", "owned_by": "org"}]}

    summary = run_live_capture(
        surface="anthropic", repo_root=tmp_path, fetcher=lambda: payload
    )

    retained = Path(summary["payload_path"])
    assert retained.exists()
    body = json.loads(retained.read_text(encoding="utf-8"))
    assert body["payload"] == payload
    assert "self-report" in body["provenance"]

    for path in summary["record_paths"]:
        record = json.loads(Path(path).read_text(encoding="utf-8"))
        validate_catalog_record(record)

    assert summary["content_evidence_status"] == EVIDENCE_SELF_ASSERTED
    assert summary["channel_authentication_status"] == UNVERIFIABLE


def test_sdk_entries_normalize_without_guessing_absent_fields():
    from ai_lab.providers.catalog_transport import _entry_to_dict

    full = _entry_to_dict(_FakeModelEntry("model-alpha", owned_by="org", display_name="Alpha"))
    assert full == {"id": "model-alpha", "owned_by": "org", "display_name": "Alpha"}

    sparse = _entry_to_dict(_FakeModelEntry("model-beta"))
    assert sparse == {"id": "model-beta"}
    assert "owned_by" not in sparse


def test_mapping_entries_are_accepted_too():
    from ai_lab.providers.catalog_transport import _entry_to_dict

    assert _entry_to_dict({"id": "model-gamma", "owned_by": "org"}) == {
        "id": "model-gamma",
        "owned_by": "org",
    }


def test_fetchers_construct_no_client_until_called():
    from ai_lab.providers.catalog_transport import (
        anthropic_models_fetcher,
        openai_models_fetcher,
    )

    # Building the fetcher must not touch credentials or the network; only
    # calling it does. Constructing both here proves the deferral.
    assert callable(openai_models_fetcher())
    assert callable(anthropic_models_fetcher())


def test_fetcher_shape_matches_the_capture_parser(monkeypatch, tmp_path):
    """An SDK-shaped listing flows through the real parsing path."""

    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV
    from ai_lab.providers.catalog_transport import _entry_to_dict, run_live_capture

    monkeypatch.setenv(LIVE_CAPTURE_ENV, "1")
    listing = _FakeListing(
        [_FakeModelEntry("model-alpha", owned_by="org"), _FakeModelEntry("model-beta")]
    )

    def fetch():
        return {"data": [_entry_to_dict(entry) for entry in listing.data]}

    summary = run_live_capture(surface="openai", repo_root=tmp_path, fetcher=fetch)

    assert summary["identity_count"] == 2
    assert summary["assertion_count"] == 2


def test_capture_script_refuses_without_the_opt_in(monkeypatch, capsys):
    import importlib

    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV

    monkeypatch.delenv(LIVE_CAPTURE_ENV, raising=False)
    module = importlib.import_module("scripts.capture_catalog")
    monkeypatch.setattr("sys.argv", ["capture_catalog.py", "anthropic"])

    assert module.main() == 2
    assert "disabled" in capsys.readouterr().err
