from pathlib import Path

import pytest

from ai_lab.documentation.artifact_history import (
    ArtifactHistoryError,
    discover_artifacts,
    format_artifact_source_tree,
)


def write_artifact(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_format_artifact_source_tree_handles_abstraction_sources(tmp_path: Path):
    comparison_dir = tmp_path / "docs" / "comparisons"
    abstraction_dir = tmp_path / "docs" / "abstractions"

    write_artifact(
        comparison_dir / "COMP-0003-root.md",
        """# COMP-0003

## Metadata

- comparison_id: `COMP-0003`
- title: `Root Comparison`
- created_at: `2026-06-30T00:00:00+00:00`
""",
    )

    write_artifact(
        comparison_dir / "syntheses" / "SYNCOMP-0001-synthesis.md",
        """# SYNCOMP-0001

## Metadata

- synthesis_id: `SYNCOMP-0001`
- title: `Root Synthesis`
- created_at: `2026-06-30T00:01:00+00:00`
- source_comparison: `docs/comparisons/COMP-0003-root.md`
""",
    )

    write_artifact(
        comparison_dir / "COMP-0004-reask.md",
        """# COMP-0004

## Metadata

- comparison_id: `COMP-0004`
- title: `Reask Comparison`
- created_at: `2026-06-30T00:02:00+00:00`
- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0001-synthesis.md`
""",
    )

    write_artifact(
        abstraction_dir / "ABS-0001-loop.md",
        """# ABS-0001

## Metadata

- abstraction_id: `ABS-0001`
- title: `Loop Abstraction`
- abstraction_level: `1`
- created_at: `2026-06-30T00:03:00+00:00`
- source_artifacts: `docs/comparisons/COMP-0003-root.md, docs/comparisons/syntheses/SYNCOMP-0001-synthesis.md, docs/comparisons/COMP-0004-reask.md`
""",
    )

    records = discover_artifacts(comparison_dir, abstraction_dir)
    output = format_artifact_source_tree(records, "ABS-0001")

    assert "ABS-0001 [ABS] Loop Abstraction" in output
    assert "↑ source for abstracted into" in output
    assert "COMP-0003 [COMP] Root Comparison" in output
    assert "SYNCOMP-0001 [SYNCOMP] Root Synthesis" in output
    assert "COMP-0004 [COMP] Reask Comparison" in output


def test_format_artifact_source_tree_raises_for_unknown_artifact():
    with pytest.raises(ArtifactHistoryError):
        format_artifact_source_tree([], "ABS-9999")
