from pathlib import Path

from scripts.compare_providers import (
    auto_comparison_path,
    build_markdown_artifact,
    next_comparison_id,
    slugify,
)


def test_build_markdown_artifact_records_metadata_models_and_responses():
    artifact = build_markdown_artifact(
        prompt="Explain provenance.",
        responses={
            "OpenAI": {
                "model": "gpt-5",
                "response": "OpenAI answer.",
            },
            "Claude": {
                "model": "claude-sonnet-4-5",
                "response": "Claude answer.",
            },
        },
        created_at="2026-06-30T00:00:00Z",
        command="scripts/compare_providers.py Explain provenance.",
        comparison_id="COMP-0003",
        title="Provenance",
    )

    assert "# COMP-0003: Provider Comparison — Provenance" in artifact
    assert "- comparison_id: `COMP-0003`" in artifact
    assert "- title: `Provenance`" in artifact
    assert "- created_at: `2026-06-30T00:00:00Z`" in artifact
    assert "- providers: `OpenAI, Claude`" in artifact
    assert "- OpenAI: `gpt-5`" in artifact
    assert "- Claude: `claude-sonnet-4-5`" in artifact
    assert "## Prompt" in artifact
    assert "Explain provenance." in artifact
    assert "## OpenAI Response" in artifact
    assert "OpenAI answer." in artifact
    assert "## Claude Response" in artifact
    assert "Claude answer." in artifact


def test_build_markdown_artifact_uses_longer_fence_when_response_contains_backticks():
    artifact = build_markdown_artifact(
        prompt="Return code.",
        responses={
            "OpenAI": {
                "model": "gpt-5",
                "response": "```python\nprint('hello')\n```",
            },
        },
        created_at="2026-06-30T00:00:00Z",
        command="scripts/compare_providers.py Return code.",
    )

    assert "````" in artifact


def test_slugify_creates_filesystem_safe_slug():
    assert slugify("Model Metadata & Provenance!") == "model-metadata-provenance"


def test_next_comparison_id_uses_existing_files(tmp_path: Path):
    (tmp_path / "COMP-0001-first.md").write_text("", encoding="utf-8")
    (tmp_path / "COMP-0007-seventh.md").write_text("", encoding="utf-8")
    (tmp_path / "NOT-A-COMP.md").write_text("", encoding="utf-8")

    assert next_comparison_id(tmp_path) == "COMP-0008"


def test_auto_comparison_path_uses_next_id_and_slug(tmp_path: Path):
    (tmp_path / "COMP-0002-existing.md").write_text("", encoding="utf-8")

    path = auto_comparison_path("Edge Immutability", tmp_path)

    assert path == tmp_path / "COMP-0003-edge-immutability.md"
