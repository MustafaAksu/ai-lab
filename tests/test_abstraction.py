from pathlib import Path

from ai_lab.documentation.abstraction import (
    abstraction_id_from_path,
    auto_abstraction_path,
    build_abstraction_artifact,
    build_abstraction_prompt,
    compact_artifact_markdown,
    next_abstraction_id,
    slugify,
)


def test_next_abstraction_id_uses_existing_files(tmp_path: Path):
    (tmp_path / "ABS-0001-first.md").write_text("", encoding="utf-8")
    (tmp_path / "ABS-0007-seventh.md").write_text("", encoding="utf-8")

    assert next_abstraction_id(tmp_path) == "ABS-0008"


def test_auto_abstraction_path_uses_next_id_and_slug(tmp_path: Path):
    (tmp_path / "ABS-0002-existing.md").write_text("", encoding="utf-8")

    path = auto_abstraction_path("Artifact Discipline Loop", tmp_path)

    assert path == tmp_path / "ABS-0003-artifact-discipline-loop.md"


def test_slugify_creates_filesystem_safe_slug():
    assert slugify("Artifact Discipline & Memory!") == "artifact-discipline-memory"


def test_abstraction_id_from_path_extracts_abs_id():
    assert abstraction_id_from_path(Path("ABS-0004-history-compression.md")) == "ABS-0004"


def test_build_abstraction_prompt_records_level_sources_and_rules():
    prompt = build_abstraction_prompt(
        title="Artifact Discipline Loop",
        abstraction_level=1,
        source_artifacts=[
            (
                Path("docs/comparisons/COMP-0003-example.md"),
                "# COMP-0003\n\nProvider response.",
            ),
            (
                Path("docs/comparisons/syntheses/SYNCOMP-0001-example.md"),
                "# SYNCOMP-0001\n\nSynthesis response.",
            ),
        ],
    )

    assert "Title: Artifact Discipline Loop" in prompt
    assert "Abstraction level: 1" in prompt
    assert "Stable claims" in prompt
    assert "Unsupported strengthenings or risks" in prompt
    assert "Use numeric abstraction level only" in prompt
    assert "SOURCE ARTIFACT: docs/comparisons/COMP-0003-example.md" in prompt
    assert "# SYNCOMP-0001" in prompt


def test_build_abstraction_artifact_records_metadata_sources_and_response():
    artifact = build_abstraction_artifact(
        abstraction_id="ABS-0001",
        title="Artifact Discipline Loop",
        abstraction_level=1,
        source_paths=[
            Path("docs/comparisons/COMP-0003-example.md"),
            Path("docs/comparisons/syntheses/SYNCOMP-0001-example.md"),
        ],
        abstraction_response="Stable claims go here.",
        abstracter_provider="OpenAI",
        abstracter_model="gpt-5",
        created_at="2026-06-30T00:00:00+00:00",
        command="scripts/create_abstraction.py ...",
    )

    assert "# ABS-0001: Abstraction — Artifact Discipline Loop" in artifact
    assert "- abstraction_id: `ABS-0001`" in artifact
    assert "- abstraction_level: `1`" in artifact
    assert "- abstracter_provider: `OpenAI`" in artifact
    assert "- abstracter_model: `gpt-5`" in artifact
    assert "- `docs/comparisons/COMP-0003-example.md`" in artifact
    assert "Stable claims go here." in artifact

def test_compact_artifact_markdown_removes_embedded_source_sections():
    markdown = """# SYNCOMP-0001

## Metadata

- synthesis_id: `SYNCOMP-0001`

## Synthesis

Useful synthesis.

## Source Comparison

Large embedded comparison should not be included.
"""

    compact = compact_artifact_markdown(markdown)

    assert "Useful synthesis." in compact
    assert "Source Comparison" not in compact
    assert "Large embedded comparison" not in compact

