import json
import subprocess
import sys

from ai_lab.documentation.context_admission import ContextAdmissionVerdict


def test_write_context_admission_script_creates_json(tmp_path):
    output = tmp_path / "verdict.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/write_context_admission.py",
            "--target-item-id",
            "L1-20260702-memory-refresh",
            "--target-item-type",
            "episode_l1",
            "--decision",
            "admit",
            "--freshness-state",
            "fresh",
            "--warrant-state",
            "supported",
            "--author",
            "mustafa",
            "--substrate",
            "human",
            "--reason",
            "Manual L1 memory refresh was inspected and committed.",
            "--evidence-id",
            "ef71fce",
            "--evidence-path",
            "docs/memory/l1/L1-20260702-memory-refresh.json",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.exists()
    assert "Saved context admission verdict" in result.stdout

    payload = json.loads(output.read_text())
    assert payload["verdict_id"].startswith("CADM-")
    assert payload["target_item_id"] == "L1-20260702-memory-refresh"
    assert payload["decision"] == "admit"

    loaded = ContextAdmissionVerdict.read_json(output)
    assert loaded.target_item_type == "episode_l1"
    assert loaded.evidence_ids == ("ef71fce",)
    assert loaded.evidence_paths == ("docs/memory/l1/L1-20260702-memory-refresh.json",)


def test_write_context_admission_script_rejects_stale_admit(tmp_path):
    output = tmp_path / "bad-verdict.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/write_context_admission.py",
            "--target-item-id",
            "ABS-0003",
            "--target-item-type",
            "abstraction",
            "--decision",
            "admit",
            "--freshness-state",
            "stale",
            "--warrant-state",
            "supported",
            "--author",
            "ai-lab",
            "--substrate",
            "process",
            "--reason",
            "Stale direct admission should fail.",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert not output.exists()
    assert "stale items" in result.stderr
