from pathlib import Path

from ai_lab.documentation.prompt_context import build_prompt, read_context_pack


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


def test_build_latest_context_pack_text_uses_manifest_helper(monkeypatch):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from ai_lab.documentation import prompt_context

    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction.",
        relevance_score=0.9,
        token_estimate=100,
    )
    manifest = ContextPackManifest(
        task="Prepare context.",
        assembly_policy="latest_context",
        items=(item,),
    )

    monkeypatch.setattr(
        prompt_context,
        "build_latest_context_pack_manifest",
        lambda task, token_budget=None, model_target=None: manifest,
    )
    monkeypatch.setattr(
        prompt_context,
        "render_context_pack_markdown",
        lambda manifest: "# Rendered Context",
    )

    assert (
        prompt_context.build_latest_context_pack_text(
            task="Prepare context.",
            token_budget=8000,
            model_target="gpt-5",
        )
        == "# Rendered Context"
    )
