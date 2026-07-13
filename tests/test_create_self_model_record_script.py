from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from ai_lab.documentation.self_model import (
    suggest_next_record_id,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    PROJECT_ROOT
    / "scripts"
    / "create_self_model_record.py"
)


def _gap_payload(
    *,
    gap_id: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": "v1",
        "name": "Fixture gap",
        "status": "open",
        "priority": "medium",
        "category": "fixture",
        "summary": "Fixture gap summary.",
        "related_capabilities": [],
        "evidence": {
            "reason": "Fixture evidence.",
            "files_checked": [],
        },
        "risk": "Fixture risk.",
        "recommended_first_slice": (
            "Create the first governed fixture slice."
        ),
        "blocked_by": [],
    }

    if gap_id is not None:
        payload["gap_id"] = gap_id

    return payload


def _plan_payload(
    plan_id: str,
) -> dict[str, object]:
    return {
        "schema_version": "v1",
        "plan_id": plan_id,
        "title": "Fixture plan",
        "status": "proposed",
        "created_at": "2026-07-13T00:00:00+00:00",
        "source_gap_id": "GAP-9999",
        "objective": "Exercise date-scoped ID discovery.",
        "proposed_change": "Add a fixture plan.",
        "rationale": ["Fixture rationale."],
        "constraints": ["Fixture constraint."],
        "success_criteria": ["Fixture success criterion."],
        "risk": "Fixture risk.",
        "next_action": "Review the fixture.",
    }


def _write_record(
    repo_root: Path,
    directory: str,
    filename: str,
    payload: dict[str, object],
) -> None:
    path = (
        repo_root
        / "docs"
        / "self_model"
        / directory
        / filename
    )
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _run(
    *args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            *args,
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_suggest_next_record_id_uses_namespace_maximum(
    tmp_path,
):
    _write_record(
        tmp_path,
        "gaps",
        "GAP-0001.json",
        _gap_payload(gap_id="GAP-0001"),
    )
    _write_record(
        tmp_path,
        "gaps",
        "GAP-0003.json",
        _gap_payload(gap_id="GAP-0003"),
    )

    _write_record(
        tmp_path,
        "plans",
        "PLAN-20260712-0099.json",
        _plan_payload("PLAN-20260712-0099"),
    )
    _write_record(
        tmp_path,
        "plans",
        "PLAN-20260713-0002.json",
        _plan_payload("PLAN-20260713-0002"),
    )

    assert suggest_next_record_id(
        "gap",
        repo_root=tmp_path,
    ) == "GAP-0004"

    assert suggest_next_record_id(
        "plan",
        repo_root=tmp_path,
        record_date="2026-07-13",
    ) == "PLAN-20260713-0003"

    assert suggest_next_record_id(
        "plan",
        repo_root=tmp_path,
        record_date="2026-07-14",
    ) == "PLAN-20260714-0001"

    assert suggest_next_record_id(
        "decision",
        repo_root=tmp_path,
        record_date="2026-07-13",
    ) == "DECISION-20260713-0001"


def test_create_self_model_record_writes_valid_gap(
    tmp_path,
):
    payload_path = tmp_path / "gap-payload.json"
    payload_path.write_text(
        json.dumps(_gap_payload()),
        encoding="utf-8",
    )

    result = _run(
        "gap",
        "--input",
        str(payload_path),
        "--repo-root",
        str(tmp_path),
    )

    assert result.returncode == 0, result.stderr
    assert "record_id: GAP-0001" in result.stdout
    assert "local and non-transactional" in result.stdout

    output = (
        tmp_path
        / "docs"
        / "self_model"
        / "gaps"
        / "GAP-0001.json"
    )
    assert output.exists()

    record = json.loads(
        output.read_text(encoding="utf-8")
    )
    assert record["gap_id"] == "GAP-0001"


def test_create_self_model_record_refuses_collision(
    tmp_path,
):
    _write_record(
        tmp_path,
        "gaps",
        "GAP-0001.json",
        _gap_payload(gap_id="GAP-0001"),
    )

    payload_path = tmp_path / "gap-payload.json"
    payload_path.write_text(
        json.dumps(_gap_payload()),
        encoding="utf-8",
    )

    result = _run(
        "gap",
        "--input",
        str(payload_path),
        "--repo-root",
        str(tmp_path),
        "--record-id",
        "GAP-0001",
    )

    assert result.returncode != 0
    assert "already exists" in result.stderr


def test_create_self_model_record_validates_before_write(
    tmp_path,
):
    payload = _gap_payload()
    del payload["risk"]

    payload_path = tmp_path / "invalid-gap.json"
    payload_path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    result = _run(
        "gap",
        "--input",
        str(payload_path),
        "--repo-root",
        str(tmp_path),
        "--record-id",
        "GAP-0001",
    )

    assert result.returncode != 0
    assert "$.risk" in result.stderr
    assert not (
        tmp_path
        / "docs"
        / "self_model"
        / "gaps"
        / "GAP-0001.json"
    ).exists()


def test_create_self_model_record_help_documents_id_limit():
    result = _run("--help")

    assert result.returncode == 0
    assert "not transactional" in result.stdout
    assert "rebase" in result.stdout
    assert "merge" in result.stdout
