from pathlib import Path

from scripts.ask_provider import build_prompt, read_context_pack


def test_build_prompt_without_context_returns_prompt():
    assert build_prompt("Do the task.") == "Do the task."


def test_build_prompt_with_context_pack_wraps_context():
    prompt = build_prompt(
        prompt="Implement the next step.",
        context_pack="# Context Pack\n\nImportant source.",
    )

    assert "BEGIN CONTEXT PACK" in prompt
    assert "# Context Pack" in prompt
    assert "END CONTEXT PACK" in prompt
    assert "User task:" in prompt
    assert prompt.endswith("Implement the next step.")


def test_read_context_pack_reads_markdown(tmp_path):
    path = tmp_path / "context.md"
    path.write_text("# Context Pack", encoding="utf-8")

    assert read_context_pack(Path(path)) == "# Context Pack"
