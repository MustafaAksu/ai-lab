from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "create_l0_chunk.py"


def run_create_l0_chunk(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd or PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def base_args(output: Path | None = None) -> list[str]:
    args = [
        "--artifact-cid",
        "3ac9f2b1d0af",
        "--version",
        "a1c2d3e",
        "--span-unit",
        "b",
        "--span-start",
        "100",
        "--span-end",
        "200",
        "--path",
        "docs/example.md",
        "--artifact-type",
        "doc",
        "--language",
        "markdown",
        "--embedding-id",
        "emb_001",
        "--l0-summary",
        "Defines citation format and validation rules.",
        "--keyphrase",
        "citation",
        "--keyphrase",
        "span",
        "--keyphrase",
        "validation",
        "--entity",
        "schema:Citation",
        "--claim",
        "pro:Citations use cid@version|span.",
        "--risk",
        "med:Token spans require tokenizer versioning.",
        "--created-at",
        "2026-06-30T00:00:00+00:00",
        "--last-refreshed-at",
        "2026-06-30T00:00:00+00:00",
        "--generator-model",
        "gpt-5",
        "--generator-version",
        "v1",
        "--pipeline-run-id",
        "run_001",
    ]

    if output is not None:
        args.extend(["--output", str(output)])

    return args


def test_create_l0_chunk_script_writes_valid_summary(tmp_path: Path):
    output = tmp_path / "l0.json"

    result = run_create_l0_chunk(*base_args(output))

    assert result.returncode == 0, result.stderr
    assert "Saved L0 chunk summary:" in result.stdout
    assert "chunk_id:" in result.stdout
    assert "citation: 3ac9f2b1d0af@a1c2d3e|b:100-200" in result.stdout

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["citation"] == "3ac9f2b1d0af@a1c2d3e|b:100-200"
    assert data["l0_summary"] == "Defines citation format and validation rules."
    assert data["keyphrases"] == ["citation", "span", "validation"]
    assert data["entities"] == [{"name": "Citation", "type": "schema"}]
    assert data["claims"] == [
        {
            "polarity": "pro",
            "text": "Citations use cid@version|span.",
        }
    ]
    assert data["risks"] == [
        {
            "severity": "med",
            "text": "Token spans require tokenizer versioning.",
        }
    ]
    assert data["chunk_reference"]["artifact_cid"] == "3ac9f2b1d0af"
    assert data["chunk_reference"]["artifact_type"] == "doc"
    assert data["chunk_reference"]["embedding_ids"] == ["emb_001"]
    assert data["chunk_reference"]["language"] == "markdown"
    assert data["chunk_reference"]["path"] == "docs/example.md"
    assert data["chunk_reference"]["span"] == {
        "end": 200,
        "start": 100,
        "unit": "b",
    }
    assert data["generator"] == {
        "model": "gpt-5",
        "version": "v1",
    }
    assert data["provenance"] == {
        "pipeline_run_id": "run_001",
    }


def test_create_l0_chunk_script_defaults_output_to_l0_memory_dir(tmp_path: Path):
    result = run_create_l0_chunk(*base_args(), cwd=tmp_path)

    assert result.returncode == 0, result.stderr

    outputs = sorted((tmp_path / "docs" / "memory" / "l0").glob("*.json"))
    assert len(outputs) == 1

    data = json.loads(outputs[0].read_text(encoding="utf-8"))
    assert data["citation"] == "3ac9f2b1d0af@a1c2d3e|b:100-200"
    assert outputs[0].stem == data["chunk_reference"]["chunk_id"]


def test_create_l0_chunk_script_validates_l0_schema(tmp_path: Path):
    output = tmp_path / "l0.json"
    args = [
        "--artifact-cid",
        "3ac9f2b1d0af",
        "--version",
        "a1c2d3e",
        "--span-unit",
        "b",
        "--span-start",
        "100",
        "--span-end",
        "200",
        "--l0-summary",
        "Too few keyphrases.",
        "--keyphrase",
        "only-one",
        "--output",
        str(output),
    ]

    result = run_create_l0_chunk(*args)

    assert result.returncode != 0
    assert not output.exists()
    assert "keyphrases must contain between 3 and 10 items" in result.stderr
