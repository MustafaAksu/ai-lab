from pathlib import Path

import pytest

from ai_lab.documentation.artifact_history import ArtifactRecord, discover_artifacts
from ai_lab.documentation.graph_neighborhood import (
    GraphNeighborhoodError,
    edge_record_relations,
    format_graph_neighborhood_report,
    future_edge_seed_relations,
    graph_neighborhood_advisor,
)


def write_artifact(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_graph_neighborhood_reports_artifact_lineage_candidates(tmp_path: Path):
    comparison_dir = tmp_path / "docs" / "comparisons"

    write_artifact(
        comparison_dir / "COMP-0001-root.md",
        """# COMP-0001

## Metadata

- comparison_id: `COMP-0001`
- title: `Root`
- created_at: `2026-07-01T00:00:00+00:00`
""",
    )
    write_artifact(
        comparison_dir / "syntheses" / "SYNCOMP-0001-root-synthesis.md",
        """# SYNCOMP-0001

## Metadata

- synthesis_id: `SYNCOMP-0001`
- title: `Root Synthesis`
- created_at: `2026-07-01T00:01:00+00:00`
- source_comparison: `docs/comparisons/COMP-0001-root.md`
""",
    )
    write_artifact(
        comparison_dir / "COMP-0002-reask.md",
        """# COMP-0002

## Metadata

- comparison_id: `COMP-0002`
- title: `Reask`
- created_at: `2026-07-01T00:02:00+00:00`
- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0001-root-synthesis.md`
""",
    )

    records = discover_artifacts(comparison_dir)
    report = graph_neighborhood_advisor(
        target_id="COMP-0002",
        artifact_records=records,
        max_depth=2,
    )

    assert report.selected_artifact_ids == ("SYNCOMP-0001", "COMP-0001")
    assert report.excluded_artifact_ids == ()
    assert report.selected_token_estimate > 0

    first = report.candidates[0]
    assert first.artifact_id == "SYNCOMP-0001"
    assert first.distance == 1
    assert first.authoritative is True
    assert first.relation_sources == ("artifact_lineage",)
    assert "re_asked_into" in first.relation_path[0]
    assert first.decision == "included"


def test_graph_neighborhood_applies_diagnostic_budget_without_selection_effect(tmp_path: Path):
    root = tmp_path / "docs" / "comparisons"

    root.mkdir(parents=True)
    (root / "COMP-0001-root.md").write_text(
        "# COMP-0001\n\n## Metadata\n\n- comparison_id: `COMP-0001`\n- title: `Root`\n",
        encoding="utf-8",
    )
    (root / "COMP-0002-child.md").write_text(
        "# COMP-0002\n\n## Metadata\n\n- comparison_id: `COMP-0002`\n- title: `Child`\n- source_comparison: `docs/comparisons/COMP-0001-root.md`\n",
        encoding="utf-8",
    )

    records = discover_artifacts(root)
    report = graph_neighborhood_advisor(
        target_id="COMP-0002",
        artifact_records=records,
        token_budget=1,
    )

    assert report.candidates[0].decision == "excluded"
    assert report.selected_artifact_ids == ()
    assert "selection_effect: `none`" in format_graph_neighborhood_report(report)


def test_graph_neighborhood_uses_validated_edge_records(tmp_path: Path):
    comp_a = tmp_path / "COMP-0001.md"
    comp_b = tmp_path / "COMP-0002.md"
    comp_a.write_text("alpha", encoding="utf-8")
    comp_b.write_text("beta", encoding="utf-8")

    records = [
        ArtifactRecord("COMP-0001", "COMP", "Alpha", comp_a),
        ArtifactRecord("COMP-0002", "COMP", "Beta", comp_b),
    ]

    edge = {
        "id": "EDGE-0001",
        "origin_type": "relation_record",
        "current_type": "relation_record",
        "title": "COMP-0002 supports COMP-0001",
        "created_at": "2026-07-09T00:00:00Z",
        "subject": {"id": "COMP-0002", "scope": "exact"},
        "predicate": {
            "id": "supports",
            "vocabulary": "bootstrap_predicates",
            "version": "0.1",
        },
        "object": {"id": "COMP-0001", "scope": "exact"},
        "warrant": {"summary": "Synthetic edge for test."},
        "contributors": [
            {
                "peer_id": "PEER-0002",
                "role": "relation_author",
                "substrate": "GPT-5.5 Thinking",
            }
        ],
    }

    report = graph_neighborhood_advisor(
        target_id="COMP-0002",
        artifact_records=records,
        edge_records=[edge],
    )

    assert report.selected_artifact_ids == ("COMP-0001",)
    assert report.candidates[0].relation_sources == ("edge_record",)
    assert "supports" in report.candidates[0].relation_path[0]
    assert "scope=exact" in report.candidates[0].relation_path[0]


def test_graph_neighborhood_rejects_invalid_edge_records(tmp_path: Path):
    records = [
        ArtifactRecord(
            "COMP-0001",
            "COMP",
            "Alpha",
            tmp_path / "COMP-0001.md",
        )
    ]

    with pytest.raises(GraphNeighborhoodError, match="Invalid EDGE record"):
        graph_neighborhood_advisor(
            target_id="COMP-0001",
            artifact_records=records,
            edge_records=[
                {
                    "id": "EDGE-0001",
                    "origin_type": "relation_record",
                    "current_type": "relation_record",
                }
            ],
        )


def test_future_edge_seed_relations_are_non_authoritative(tmp_path: Path):
    comp_a = tmp_path / "COMP-0001.md"
    comp_b = tmp_path / "COMP-0002.md"
    comp_a.write_text("alpha", encoding="utf-8")
    comp_b.write_text("beta", encoding="utf-8")

    records = [
        ArtifactRecord("COMP-0001", "COMP", "Alpha", comp_a),
        ArtifactRecord("COMP-0002", "COMP", "Beta", comp_b),
    ]

    report = graph_neighborhood_advisor(
        target_id="COMP-0002",
        artifact_records=records,
        future_edge_seed_records=[
            {
                "source_id": "COMP-0002",
                "predicate": "derived_from",
                "target_id": "COMP-0001",
            }
        ],
    )

    assert report.selected_artifact_ids == ("COMP-0001",)
    assert report.candidates[0].authoritative is False
    assert report.candidates[0].relation_sources == ("future_edge_seed",)
    assert "non_authoritative" in report.candidates[0].relation_path[0]


def test_relation_helpers_are_deterministic_and_validate_seed_shape():
    seeds = future_edge_seed_relations(
        [
            {
                "source_id": "L1-0001",
                "predicate": "derived_from",
                "target_id": "EVT-0001",
            }
        ]
    )

    assert seeds[0].source_id == "L1-0001"
    assert seeds[0].authoritative is False

    with pytest.raises(GraphNeighborhoodError, match="missing required field"):
        future_edge_seed_relations([{"source_id": "L1-0001"}])


def test_edge_record_relations_exposes_authoritative_scope():
    edge = {
        "id": "EDGE-0001",
        "origin_type": "relation_record",
        "current_type": "relation_record",
        "title": "A supports B",
        "created_at": "2026-07-09T00:00:00Z",
        "subject": {"id": "A", "scope": "exact"},
        "predicate": {
            "id": "supports",
            "vocabulary": "bootstrap_predicates",
            "version": "0.1",
        },
        "object": {"id": "B", "scope": "lineage"},
        "warrant": {"summary": "Synthetic edge for test."},
        "contributors": [
            {
                "peer_id": "PEER-0002",
                "role": "relation_author",
                "substrate": "GPT-5.5 Thinking",
            }
        ],
    }

    relation = edge_record_relations([edge])[0]

    assert relation.source_id == "A"
    assert relation.target_id == "B"
    assert relation.predicate == "supports"
    assert relation.relation_source == "edge_record"
    assert relation.authoritative is True
    assert relation.scope == "lineage"
