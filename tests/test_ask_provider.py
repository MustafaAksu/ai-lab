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


def test_main_print_prompt_does_not_call_provider(tmp_path, monkeypatch, capsys):
    from scripts.ask_provider import main

    context_path = tmp_path / "context.md"
    context_path.write_text("# Context Pack\n\nImportant context.", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "the",
            "next",
            "step.",
            "--context-pack",
            str(context_path),
            "--print-prompt",
        ],
    )

    assert main() == 0

    output = capsys.readouterr().out

    assert "BEGIN CONTEXT PACK" in output
    assert "# Context Pack" in output
    assert "END CONTEXT PACK" in output
    assert "User task:" in output
    assert output.rstrip().endswith("Do the next step.")
