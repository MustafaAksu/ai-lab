from pathlib import Path

from ai_lab.documentation.comparison_synthesis import (
    auto_synthesis_path,
    build_synthesis_artifact,
    build_synthesis_prompt,
    next_synthesis_id,
    slugify,
    title_from_comparison_path,
)


def test_build_synthesis_prompt_contains_required_sections_and_source():
    prompt = build_synthesis_prompt("# Provider Comparison\n\nContent")

    assert "Shared agreement" in prompt
    assert "Meaningful differences" in prompt
    assert "Suggested re-ask prompt" in prompt
    assert "Use ONLY the comparison artifact below" in prompt
    assert "# Provider Comparison" in prompt


def test_build_synthesis_artifact_records_metadata_and_source():
    artifact = build_synthesis_artifact(
        synthesis_id="SYNCOMP-0001",
        title="Edge Immutability",
        comparison_path=Path("docs/comparisons/COMP-0001-edge.md"),
        comparison_markdown="# Provider Comparison",
        synthesis_response="Combined answer.",
        synthesizer_provider="OpenAI",
        synthesizer_model="gpt-5",
        created_at="2026-06-30T00:00:00Z",
        command="scripts/synthesize_comparison.py docs/comparisons/COMP-0001-edge.md",
    )

    assert "# SYNCOMP-0001: Comparison Synthesis — Edge Immutability" in artifact
    assert "- synthesis_id: `SYNCOMP-0001`" in artifact
    assert "- source_comparison: `docs/comparisons/COMP-0001-edge.md`" in artifact
    assert "- synthesizer_provider: `OpenAI`" in artifact
    assert "- synthesizer_model: `gpt-5`" in artifact
    assert "Combined answer." in artifact
    assert "# Provider Comparison" in artifact


def test_slugify_creates_filesystem_safe_slug():
    assert slugify("Edge Immutability & Provenance!") == "edge-immutability-provenance"


def test_next_synthesis_id_uses_existing_files(tmp_path: Path):
    (tmp_path / "SYNCOMP-0001-first.md").write_text("", encoding="utf-8")
    (tmp_path / "SYNCOMP-0004-fourth.md").write_text("", encoding="utf-8")

    assert next_synthesis_id(tmp_path) == "SYNCOMP-0005"


def test_auto_synthesis_path_uses_next_id_and_slug(tmp_path: Path):
    (tmp_path / "SYNCOMP-0002-existing.md").write_text("", encoding="utf-8")

    path = auto_synthesis_path("Edge Immutability", tmp_path)

    assert path == tmp_path / "SYNCOMP-0003-edge-immutability.md"


def test_title_from_comparison_path_uses_comp_slug():
    path = Path("docs/comparisons/COMP-0003-automatic-comparison-ids.md")

    assert title_from_comparison_path(path) == "Automatic Comparison Ids"
