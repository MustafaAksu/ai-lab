from pathlib import Path

from ai_lab.documentation.artifact_history import ArtifactRecord
from ai_lab.documentation.context_pack_builder import (
    build_latest_context_manifest,
    context_item_from_record,
    item_type_for_record,
)


def make_record(
    artifact_id,
    kind,
    title,
    path,
    created_at,
    abstraction_level=None,
):
    return ArtifactRecord(
        artifact_id=artifact_id,
        kind=kind,
        title=title,
        path=Path(path),
        created_at=created_at,
        source_comparison=None,
        source_synthesis=None,
        source_artifacts=(),
        abstraction_level=abstraction_level,
    )


def test_item_type_for_record_maps_history_kinds():
    assert item_type_for_record(
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            "docs/abstractions/ABS-0003.md",
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        )
    ) == "abstraction"

    assert item_type_for_record(
        make_record(
            "SYNCOMP-0003",
            "SYNCOMP",
            "Memory Synthesis",
            "docs/comparisons/syntheses/SYNCOMP-0003.md",
            "2026-06-30T00:00:00+00:00",
        )
    ) == "synthesis"

    assert item_type_for_record(
        make_record(
            "COMP-0007",
            "COMP",
            "Memory Comparison",
            "docs/comparisons/COMP-0007.md",
            "2026-06-30T00:00:00+00:00",
        )
    ) == "comparison"


def test_context_item_from_record_preserves_identity_and_path():
    record = make_record(
        "ABS-0003",
        "ABS",
        "AI-Lab Reconciled Memory Implementation Loop",
        "docs/abstractions/ABS-0003.md",
        "2026-06-30T00:00:00+00:00",
        abstraction_level=1,
    )

    item = context_item_from_record(
        record=record,
        relevance_score=0.9,
        token_estimate=1200,
    )

    assert item.item_type == "abstraction"
    assert item.item_id == "ABS-0003"
    assert item.relevance_score == 0.9
    assert item.token_estimate == 1200
    assert item.source_path == "docs/abstractions/ABS-0003.md"
    assert "ABS-L1 context seed" in item.reason


def test_build_latest_context_manifest_selects_latest_per_context_level():
    records = (
        make_record(
            "ABS-0002",
            "ABS",
            "Old Memory Loop",
            "docs/abstractions/ABS-0002.md",
            "2026-06-29T00:00:00+00:00",
            abstraction_level=1,
        ),
        make_record(
            "ABS-0003",
            "ABS",
            "New Memory Loop",
            "docs/abstractions/ABS-0003.md",
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
        make_record(
            "SYNCOMP-0003",
            "SYNCOMP",
            "Memory Synthesis",
            "docs/comparisons/syntheses/SYNCOMP-0003.md",
            "2026-06-30T00:00:00+00:00",
        ),
        make_record(
            "COMP-0007",
            "COMP",
            "Memory Comparison",
            "docs/comparisons/COMP-0007.md",
            "2026-06-30T00:00:00+00:00",
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare implementation context.",
        records=records,
        token_budget=8000,
        model_target="gpt-5",
        pipeline_run_id="run_001",
    )

    assert manifest.assembly_policy == "latest_context"
    assert manifest.token_budget == 8000
    assert manifest.model_target == "gpt-5"
    assert tuple(item.item_id for item in manifest.items) == (
        "ABS-0003",
        "SYNCOMP-0003",
        "COMP-0007",
    )
