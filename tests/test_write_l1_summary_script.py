import json
import subprocess
import sys

from ai_lab.documentation.interaction_log import EpisodeL1Summary


def test_write_l1_summary_script_creates_json(tmp_path):
    output = tmp_path / "l1.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/write_l1_summary.py",
            "--episode-id",
            "EP-CLI-0001",
            "--summary-text",
            "Manual L1 write-back records the current implementation state.",
            "--source-event-id",
            "EVT-CLI-0001",
            "--source-event-id",
            "EVT-CLI-0002",
            "--citation",
            "3ac9f2b1d0af@a1c2d3e|b:1024-2047",
            "--key-decision",
            "Use manual L1 summaries before automatic generation.",
            "--completed-work",
            "Added JSON serialization.",
            "--risk",
            "Unvalidated summaries can become stale context.",
            "--next-action",
            "Integrate manual L1 artifacts into context selection later.",
            "--topic",
            "memory",
            "--coverage-score",
            "0.75",
            "--freshness-state",
            "fresh",
            "--output",
            str(output),
            "--print-edge-seeds",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.exists()
    assert "Saved L1 summary" in result.stdout
    assert "future_edge_seed_records" in result.stdout

    payload = json.loads(output.read_text())
    assert payload["l1_id"].startswith("L1-")
    assert len(payload["content_hash"]) == 64
    assert payload["freshness_state"] == "fresh"

    loaded = EpisodeL1Summary.read_json(output)
    assert loaded.episode_id == "EP-CLI-0001"
    assert loaded.source_event_ids == ("EVT-CLI-0001", "EVT-CLI-0002")
    assert loaded.topics == ("memory",)


def test_write_l1_summary_script_rejects_bad_citation(tmp_path):
    output = tmp_path / "bad-l1.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/write_l1_summary.py",
            "--episode-id",
            "EP-CLI-0001",
            "--summary-text",
            "Bad citation should fail.",
            "--source-event-id",
            "EVT-CLI-0001",
            "--citation",
            "not-a-citation",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert not output.exists()
    assert "Invalid citation" in result.stderr
