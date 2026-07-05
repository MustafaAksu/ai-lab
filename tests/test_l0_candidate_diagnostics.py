from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from ai_lab.documentation.l0_candidate_diagnostics import l0_candidate_diagnostics


def _write_l0_record(path: Path, summary_text: str = "short summary") -> None:
    helper_path = Path("tests/test_context_pack_builder.py")
    spec = importlib.util.spec_from_file_location(
        "context_pack_builder_test_helper",
        helper_path,
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.write_l0_record(path, summary_text=summary_text)


def test_l0_candidate_diagnostics_reports_valid_record_without_selection_effect(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    _write_l0_record(l0_store / "chunk-a.json")

    result = l0_candidate_diagnostics(
        l0_store=l0_store,
        context_item_ids=("chunk-a", "chunk-b"),
    )

    assert result["schema_version"] == "v1"
    assert result["diagnostic_type"] == "l0_candidate_sources"
    assert result["selection_effect"] == "none"
    assert result["store_status"] == "ok"
    assert result["dropped"] == []

    assert len(result["candidates"]) == 1

    candidate = result["candidates"][0]
    assert candidate["cid"] == "chunk-a"
    assert candidate["path"] == str(l0_store / "chunk-a.json")
    assert candidate["candidate_reason"] == "valid_l0_summary_record"
    assert candidate["selection_effect"] == "none"
    assert candidate["context_match"] is True
    assert candidate["token_cost"] > 0

    if "citation" in candidate:
        assert isinstance(candidate["citation"], str)
        assert candidate["citation"]


def test_l0_candidate_diagnostics_marks_non_matching_context_id(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    _write_l0_record(l0_store / "chunk-a.json")

    result = l0_candidate_diagnostics(
        l0_store=l0_store,
        context_item_ids=("other-item",),
    )

    assert result["candidates"][0]["cid"] == "chunk-a"
    assert result["candidates"][0]["context_match"] is False
    assert result["candidates"][0]["selection_effect"] == "none"


def test_l0_candidate_diagnostics_reports_invalid_records_as_dropped(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    (l0_store / "bad.json").write_text("{}", encoding="utf-8")

    result = l0_candidate_diagnostics(l0_store=l0_store)

    assert result["candidates"] == []
    assert result["dropped"][0]["path"] == str(l0_store / "bad.json")
    assert result["dropped"][0]["dropped_reason"] == "invalid_record"
    assert result["dropped"][0]["diagnostics"]


def test_l0_candidate_diagnostics_missing_store_is_nonfatal(tmp_path):
    result = l0_candidate_diagnostics(l0_store=tmp_path / "missing")

    assert result["store_status"] == "missing"
    assert result["selection_effect"] == "none"
    assert result["candidates"] == []
    assert result["dropped"] == []


def test_diagnose_l0_candidates_script_outputs_json(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    _write_l0_record(l0_store / "chunk-a.json")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/diagnose_l0_candidates.py",
            "--l0-store",
            str(l0_store),
            "--context-item-id",
            "chunk-a",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    data = json.loads(result.stdout)
    assert data["selection_effect"] == "none"
    assert data["candidates"][0]["cid"] == "chunk-a"
    assert data["candidates"][0]["context_match"] is True


def test_diagnose_l0_candidates_script_can_write_output(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    _write_l0_record(l0_store / "chunk-a.json")
    output = tmp_path / "diagnostics.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/diagnose_l0_candidates.py",
            "--l0-store",
            str(l0_store),
            "--output",
            str(output),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["candidates"][0]["cid"] == "chunk-a"
    assert data["candidates"][0]["selection_effect"] == "none"
