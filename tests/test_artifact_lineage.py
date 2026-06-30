from pathlib import Path

import pytest

from ai_lab.documentation.artifact_history import (
    ArtifactHistoryError,
    discover_artifacts,
    format_artifact_lineage,
    lineage_for_artifact,
)


def write_artifact(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_lineage_for_artifact_returns_source_to_target_chain(tmp_path: Path):
    comparison_dir = tmp_path / "docs" / "comparisons"

    write_artifact(
        comparison_dir / "COMP-0003-automatic-comparison-ids.md",
        """# COMP-0003

## Metadata

- comparison_id: `COMP-0003`
- title: `Automatic Comparison IDs`
- created_at: `2026-06-30T00:00:00+00:00`
""",
    )

    write_artifact(
        comparison_dir / "syntheses" / "SYNCOMP-0001-automatic-comparison-ids.md",
        """# SYNCOMP-0001

## Metadata

- synthesis_id: `SYNCOMP-0001`
- title: `Automatic Comparison IDs`
- created_at: `2026-06-30T00:01:00+00:00`
- source_comparison: `docs/comparisons/COMP-0003-automatic-comparison-ids.md`
""",
    )

    write_artifact(
        comparison_dir / "COMP-0004-re-ask-automatic-comparison-ids.md",
        """# COMP-0004

## Metadata

- comparison_id: `COMP-0004`
- title: `Re-Ask Automatic Comparison IDs`
- created_at: `2026-06-30T00:02:00+00:00`
- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0001-automatic-comparison-ids.md`
""",
    )

    records = discover_artifacts(comparison_dir)
    chain = lineage_for_artifact(records, "COMP-0004")

    assert [record.artifact_id for record in chain] == [
        "COMP-0003",
        "SYNCOMP-0001",
        "COMP-0004",
    ]


def test_format_artifact_lineage_renders_relations(tmp_path: Path):
    comparison_dir = tmp_path / "docs" / "comparisons"

    write_artifact(
        comparison_dir / "COMP-0003-root.md",
        """# COMP-0003

## Metadata

- comparison_id: `COMP-0003`
- title: `Root`
""",
    )

    write_artifact(
        comparison_dir / "syntheses" / "SYNCOMP-0001-synthesis.md",
        """# SYNCOMP-0001

## Metadata

- synthesis_id: `SYNCOMP-0001`
- title: `Synthesis`
- source_comparison: `docs/comparisons/COMP-0003-root.md`
""",
    )

    write_artifact(
        comparison_dir / "COMP-0004-reask.md",
        """# COMP-0004

## Metadata

- comparison_id: `COMP-0004`
- title: `Reask`
- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0001-synthesis.md`
""",
    )

    records = discover_artifacts(comparison_dir)
    output = format_artifact_lineage(records, "COMP-0004")

    assert "COMP-0003 [COMP] Root" in output
    assert "↓ synthesized into" in output
    assert "SYNCOMP-0001 [SYNCOMP] Synthesis" in output
    assert "↓ re-asked into" in output
    assert "COMP-0004 [COMP] Reask" in output


def test_lineage_for_artifact_raises_for_unknown_artifact():
    with pytest.raises(ArtifactHistoryError):
        lineage_for_artifact([], "COMP-9999")
