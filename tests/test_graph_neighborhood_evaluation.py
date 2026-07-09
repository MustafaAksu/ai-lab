from pathlib import Path

from ai_lab.documentation.artifact_history import ArtifactRecord, discover_artifacts
from ai_lab.documentation.graph_neighborhood_evaluation import (
    evaluate_graph_neighborhood_advisor,
    format_graph_neighborhood_evidence_report,
)


def write_artifact(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_evidence_report_evaluates_cap_0005_artifact_lineage(tmp_path: Path):
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
        comparison_dir / "COMP-0002-child.md",
        """# COMP-0002

## Metadata

- comparison_id: `COMP-0002`
- title: `Child`
- created_at: `2026-07-01T00:01:00+00:00`
- source_comparison: `docs/comparisons/COMP-0001-root.md`
""",
    )

    records = discover_artifacts(comparison_dir)
    report = evaluate_graph_neighborhood_advisor(
        evaluation_id="GNEVAL-0001",
        target_id="COMP-0002",
        artifact_records=records,
    )

    assert report.selection_effect == "none"
    assert report.target_id == "COMP-0002"
    assert report.integration_recommendation == "plan_separately"
    assert report.failed_findings == ()
    assert report.advisor_report.selected_artifact_ids == ("COMP-0001",)
    assert {finding.code for finding in report.findings} == {
        "RELATION_PATHS_PRESENT",
        "AUTHORITY_LABELS_PRESENT",
        "TOKEN_ESTIMATES_PRESENT",
        "DIAGNOSTIC_RATIONALES_PRESENT",
        "DIAGNOSTIC_DECISIONS_PRESENT",
        "SELECTION_EFFECT_NONE",
    }


def test_evidence_report_marks_empty_neighborhood_not_ready(tmp_path: Path):
    target = tmp_path / "COMP-0001.md"
    target.write_text("target only", encoding="utf-8")

    report = evaluate_graph_neighborhood_advisor(
        evaluation_id="GNEVAL-0002",
        target_id="COMP-0001",
        artifact_records=[
            ArtifactRecord("COMP-0001", "COMP", "Target", target),
        ],
    )

    assert report.selection_effect == "none"
    assert report.integration_recommendation == "not_ready"
    assert report.failed_findings
    assert {
        finding.code
        for finding in report.failed_findings
    } >= {
        "RELATION_PATHS_PRESENT",
        "TOKEN_ESTIMATES_PRESENT",
        "DIAGNOSTIC_RATIONALES_PRESENT",
    }


def test_evidence_report_preserves_non_authoritative_seed_labels(tmp_path: Path):
    a = tmp_path / "COMP-0001.md"
    b = tmp_path / "COMP-0002.md"
    a.write_text("alpha", encoding="utf-8")
    b.write_text("beta", encoding="utf-8")

    report = evaluate_graph_neighborhood_advisor(
        evaluation_id="GNEVAL-0003",
        target_id="COMP-0002",
        artifact_records=[
            ArtifactRecord("COMP-0001", "COMP", "Alpha", a),
            ArtifactRecord("COMP-0002", "COMP", "Beta", b),
        ],
        future_edge_seed_records=[
            {
                "source_id": "COMP-0002",
                "predicate": "derived_from",
                "target_id": "COMP-0001",
            }
        ],
    )

    candidate = report.advisor_report.candidates[0]

    assert report.integration_recommendation == "plan_separately"
    assert candidate.authoritative is False
    assert "non_authoritative" in candidate.relation_path[0]


def test_format_evidence_report_states_boundaries_and_recommendation(tmp_path: Path):
    root = tmp_path / "COMP-0001.md"
    child = tmp_path / "COMP-0002.md"
    root.write_text("root", encoding="utf-8")
    child.write_text("child", encoding="utf-8")

    report = evaluate_graph_neighborhood_advisor(
        evaluation_id="GNEVAL-0004",
        target_id="COMP-0002",
        artifact_records=[
            ArtifactRecord("COMP-0001", "COMP", "Root", root),
            ArtifactRecord("COMP-0002", "COMP", "Child", child),
        ],
        future_edge_seed_records=[
            {
                "source_id": "COMP-0002",
                "predicate": "derived_from",
                "target_id": "COMP-0001",
            }
        ],
    )

    output = format_graph_neighborhood_evidence_report(report)

    assert "# Graph Neighborhood Evidence Report: GNEVAL-0004" in output
    assert "selection_effect: `none`" in output
    assert "integration_recommendation: `plan_separately`" in output
    assert "context selection" in output
    assert "provider prompts" in output
    assert "automatic context inclusion" in output
    assert "COMP-0001" in output
