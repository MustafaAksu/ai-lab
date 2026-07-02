import json
import subprocess
import sys

from ai_lab.documentation.interaction_log import InteractionLogEvent


def test_write_interaction_event_script_creates_json(tmp_path):
    output = tmp_path / "event.json"
    request_file = tmp_path / "request.txt"
    request_file.write_text("raw user request")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/write_interaction_event.py",
            "--episode-id",
            "EP-CLI-0002",
            "--turn-id",
            "2",
            "--event-type",
            "user_message",
            "--role",
            "user",
            "--actor",
            "mustafa",
            "--summary",
            "Asked to continue implementing interaction memory.",
            "--request-file",
            str(request_file),
            "--artifact-id",
            "0fe0d75",
            "--topic",
            "memory",
            "--topic",
            "interaction-log",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.exists()
    assert "Saved interaction event" in result.stdout
    assert "request_text_hash" in result.stdout

    payload = json.loads(output.read_text())
    assert payload["event_id"].startswith("EVT-")
    assert payload["request_text_hash"] is not None
    assert payload["response_text_hash"] is None

    loaded = InteractionLogEvent.read_json(output)
    assert loaded.episode_id == "EP-CLI-0002"
    assert loaded.turn_id == 2
    assert loaded.artifact_ids == ("0fe0d75",)
    assert loaded.topics == ("memory", "interaction-log")


def test_write_interaction_event_script_rejects_text_and_file_together(tmp_path):
    output = tmp_path / "event.json"
    request_file = tmp_path / "request.txt"
    request_file.write_text("raw user request")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/write_interaction_event.py",
            "--episode-id",
            "EP-CLI-0002",
            "--turn-id",
            "2",
            "--event-type",
            "user_message",
            "--role",
            "user",
            "--actor",
            "mustafa",
            "--summary",
            "This should fail.",
            "--request-text",
            "inline",
            "--request-file",
            str(request_file),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert not output.exists()
    assert "Use either direct text or file input" in result.stderr
