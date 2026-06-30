from pathlib import Path

from ai_lab.documentation.artifact_history import (
    artifact_id_from_path,
    artifact_kind_from_path,
    artifact_record_from_file,
    discover_artifacts,
    format_artifact_history,
    parse_metadata,
    title_from_path,
)


def test_artifact_kind_from_path_detects_comp_and_syncomp():
    assert artifact_kind_from_path(Path("COMP-0001-example.md")) == "COMP"
    assert artifact_kind_from_path(Path("SYNCOMP-0001-example.md")) == "SYNCOMP"
    assert artifact_kind_from_path(Path("notes.md")) == "UNKNOWN"


def test_artifact_id_from_path_extracts_known_ids():
    assert artifact_id_from_path(Path("COMP-0004-re-ask.md")) == "COMP-0004"
    assert artifact_id_from_path(Path("SYNCOMP-0002-synthesis.md")) == "SYNCOMP-0002"


def test_parse_metadata_extracts_backticked_values():
    markdown = """# COMP-0001

## Metadata

- comparison_id: `COMP-0001`
- title: `Example`
- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0001-example.md`

## Prompt

ignored
"""

    metadata = parse_metadata(markdown)

    assert metadata["comparison_id"] == "COMP-0001"
    assert metadata["title"] == "Example"
    assert metadata["source_synthesis"] == "docs/comparisons/syntheses/SYNCOMP-0001-example.md"


def test_artifact_record_from_file_uses_metadata(tmp_path: Path):
    path = tmp_path / "COMP-0004-re-ask.md"
    path.write_text(
        """# COMP-0004

## Metadata

- comparison_id: `COMP-0004`
- title: `Re-Ask`
- created_at: `2026-06-30T00:00:00+00:00`
- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0001-example.md`
""",
        encoding="utf-8",
    )

    record = artifact_record_from_file(path)

    assert record.artifact_id == "COMP-0004"
    assert record.kind == "COMP"
    assert record.title == "Re-Ask"
    assert record.source_synthesis == "docs/comparisons/syntheses/SYNCOMP-0001-example.md"


def test_discover_artifacts_finds_comparisons_and_syntheses(tmp_path: Path):
    comparison_dir = tmp_path / "docs" / "comparisons"
    synthesis_dir = comparison_dir / "syntheses"
    synthesis_dir.mkdir(parents=True)

    (comparison_dir / "COMP-0001-example.md").write_text(
        """# COMP-0001

## Metadata

- comparison_id: `COMP-0001`
- title: `Example Comparison`
- created_at: `2026-06-30T00:00:00+00:00`
""",
        encoding="utf-8",
    )

    (synthesis_dir / "SYNCOMP-0001-example.md").write_text(
        """# SYNCOMP-0001

## Metadata

- synthesis_id: `SYNCOMP-0001`
- title: `Example Synthesis`
- created_at: `2026-06-30T00:01:00+00:00`
- source_comparison: `docs/comparisons/COMP-0001-example.md`
""",
        encoding="utf-8",
    )

    records = discover_artifacts(comparison_dir)

    assert [record.artifact_id for record in records] == ["COMP-0001", "SYNCOMP-0001"]


def test_format_artifact_history_renders_table():
    comparison_dir = Path("docs/comparisons")
    record = artifact_record_from_file(
        comparison_dir / "COMP-0004-re-ask-automatic-comparison-ids.md"
    )

    output = format_artifact_history([record])

    assert "ID | Kind | Title | Source" in output
    assert "COMP-0004 | COMP | Re-Ask Automatic Comparison IDs" in output
    assert "SYNCOMP-0001-automatic-comparison-ids.md" in output

def test_title_from_path_strips_artifact_prefix():
    assert title_from_path(Path("COMP-0001-provider-comparison-artifact.md")) == "Provider Comparison Artifact"
    assert title_from_path(Path("SYNCOMP-0001-automatic-comparison-ids.md")) == "Automatic Comparison Ids"

