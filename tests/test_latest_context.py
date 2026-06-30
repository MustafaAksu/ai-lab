from pathlib import Path

from ai_lab.documentation.artifact_history import (
    ArtifactRecord,
    context_level_for_record,
    format_latest_context,
    latest_records_by_context_level,
)


def test_context_level_for_record_uses_abs_level_when_available():
    record = ArtifactRecord(
        artifact_id="ABS-0002",
        kind="ABS",
        title="Memory Pilot",
        path=Path("docs/abstractions/ABS-0002.md"),
        abstraction_level="1",
    )

    assert context_level_for_record(record) == "ABS-L1"


def test_latest_records_by_context_level_keeps_latest_per_level():
    old_comp = ArtifactRecord(
        artifact_id="COMP-0005",
        kind="COMP",
        title="Old",
        path=Path("docs/comparisons/COMP-0005.md"),
        created_at="2026-06-30T10:00:00+00:00",
    )
    new_comp = ArtifactRecord(
        artifact_id="COMP-0006",
        kind="COMP",
        title="New",
        path=Path("docs/comparisons/COMP-0006.md"),
        created_at="2026-06-30T11:00:00+00:00",
    )
    abstraction = ArtifactRecord(
        artifact_id="ABS-0002",
        kind="ABS",
        title="Abstraction",
        path=Path("docs/abstractions/ABS-0002.md"),
        created_at="2026-06-30T12:00:00+00:00",
        abstraction_level="1",
    )

    latest = latest_records_by_context_level([old_comp, new_comp, abstraction])

    assert latest["COMP"].artifact_id == "COMP-0006"
    assert latest["ABS-L1"].artifact_id == "ABS-0002"


def test_format_latest_context_renders_high_to_low_context():
    records = [
        ArtifactRecord(
            artifact_id="COMP-0006",
            kind="COMP",
            title="Implementation",
            path=Path("docs/comparisons/COMP-0006.md"),
            created_at="2026-06-30T11:00:00+00:00",
        ),
        ArtifactRecord(
            artifact_id="SYNCOMP-0002",
            kind="SYNCOMP",
            title="Synthesis",
            path=Path("docs/comparisons/syntheses/SYNCOMP-0002.md"),
            created_at="2026-06-30T10:30:00+00:00",
        ),
        ArtifactRecord(
            artifact_id="ABS-0002",
            kind="ABS",
            title="Memory Pilot",
            path=Path("docs/abstractions/ABS-0002.md"),
            created_at="2026-06-30T12:00:00+00:00",
            abstraction_level="1",
        ),
    ]

    output = format_latest_context(records)

    assert "Level | ID | Kind | Title | Path" in output
    assert output.index("ABS-L1 | ABS-0002") < output.index("SYNCOMP | SYNCOMP-0002")
    assert output.index("SYNCOMP | SYNCOMP-0002") < output.index("COMP | COMP-0006")
