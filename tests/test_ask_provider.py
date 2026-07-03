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


def test_main_latest_context_print_prompt_uses_generated_context(monkeypatch, capsys):
    from scripts import ask_provider

    def fake_build_latest_context_pack_text(task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None):
        assert task == "Do the next step."
        assert token_budget == 8000
        assert model_target == "gpt-5"
        return "# Generated Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "the",
            "next",
            "step.",
            "--latest-context",
            "--token-budget",
            "8000",
            "--model-target",
            "gpt-5",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out

    assert "BEGIN CONTEXT PACK" in output
    assert "# Generated Context Pack" in output
    assert "END CONTEXT PACK" in output
    assert output.rstrip().endswith("Do the next step.")


def test_main_latest_context_uses_short_task_label_but_keeps_full_prompt(monkeypatch, capsys):
    from scripts import ask_provider

    long_prompt = "x" * 600

    def fake_build_latest_context_pack_text(task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None):
        assert len(task) == 500
        assert task.endswith("...")
        return "# Generated Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            long_prompt,
            "--latest-context",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    assert long_prompt in output
    assert "# Generated Context Pack" in output


def test_main_latest_context_passes_require_admission(monkeypatch, capsys):
    from scripts import ask_provider

    def fake_build_latest_context_pack_text(
        task,
        token_budget=None,
        model_target=None,
        scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None, max_warning_admissions=None
    ):
        assert task == "Do the admitted step."
        assert token_budget == 8000
        assert model_target == "gpt-5"
        assert scope == "ai-lab-memory"
        assert require_admission is True
        return "# Admitted Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "the",
            "admitted",
            "step.",
            "--latest-context",
            "--scope",
            "ai-lab-memory",
            "--require-admission",
            "--token-budget",
            "8000",
            "--model-target",
            "gpt-5",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    assert "# Admitted Context Pack" in output
    assert "Do the admitted step." in output
