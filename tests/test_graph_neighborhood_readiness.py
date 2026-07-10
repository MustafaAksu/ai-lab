from pathlib import Path

from ai_lab.documentation.artifact_history import ArtifactRecord
from ai_lab.documentation.graph_neighborhood_evaluation import (
    evaluate_graph_neighborhood_advisor,
)
from ai_lab.documentation.graph_neighborhood_readiness import (
    decide_graph_neighborhood_integration_readiness,
    format_graph_neighborhood_readiness_report,
)


def passing_evidence_report(tmp_path: Path, evaluation_id: str = "GNEVAL-READY"):
    root = tmp_path / f"{evaluation_id}-root.md"
    child = tmp_path / f"{evaluation_id}-child.md"
    root.write_text("root", encoding="utf-8")
    child.write_text("child", encoding="utf-8")

    return evaluate_graph_neighborhood_advisor(
        evaluation_id=evaluation_id,
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


def not_ready_evidence_report(tmp_path: Path, evaluation_id: str = "GNEVAL-NOT-READY"):
    target = tmp_path / f"{evaluation_id}-target.md"
    target.write_text("target only", encoding="utf-8")

    return evaluate_graph_neighborhood_advisor(
        evaluation_id=evaluation_id,
        target_id="COMP-0001",
        artifact_records=[
            ArtifactRecord("COMP-0001", "COMP", "Target", target),
        ],
    )


def test_readiness_decision_proposes_separate_plan_when_cap_0006_evidence_passes(tmp_path: Path):
    evidence = passing_evidence_report(tmp_path)

    report = decide_graph_neighborhood_integration_readiness(
        readiness_id="GNREADY-0001",
        evidence_reports=[evidence],
    )

    assert report.decision == "propose_separate_context_pack_integration_plan"
    assert report.selection_effect == "none"
    assert report.preserved_default_context_pack_behavior is True
    assert report.evidence_report_ids == ("GNEVAL-READY",)
    assert report.failed_findings == ()
    assert "context-pack integration" in report.blocked_integration_behaviors
    assert "automatic context inclusion" in report.blocked_integration_behaviors


def test_readiness_decision_does_not_propose_when_cap_0006_evidence_fails(tmp_path: Path):
    evidence = not_ready_evidence_report(tmp_path)

    report = decide_graph_neighborhood_integration_readiness(
        readiness_id="GNREADY-0002",
        evidence_reports=[evidence],
    )

    assert evidence.integration_recommendation == "not_ready"
    assert report.decision == "do_not_propose_yet"
    assert report.selection_effect == "none"
    assert report.failed_findings
    assert {
        finding.code
        for finding in report.failed_findings
    } >= {
        "ALL_EVIDENCE_REPORTS_PASSED",
        "ALL_EVIDENCE_RECOMMENDS_SEPARATE_PLANNING",
    }


def test_readiness_decision_requires_cap_0006_evidence_reports():
    report = decide_graph_neighborhood_integration_readiness(
        readiness_id="GNREADY-0003",
        evidence_reports=[],
    )

    assert report.decision == "do_not_propose_yet"
    assert report.evidence_report_ids == ()
    assert "CAP_0006_EVIDENCE_REPORTS_PRESENT" in {
        finding.code
        for finding in report.failed_findings
    }


def test_format_readiness_report_states_no_integration_boundary(tmp_path: Path):
    evidence = passing_evidence_report(tmp_path, evaluation_id="GNEVAL-FORMAT")

    report = decide_graph_neighborhood_integration_readiness(
        readiness_id="GNREADY-0004",
        evidence_reports=[evidence],
    )

    output = format_graph_neighborhood_readiness_report(report)

    assert "# Graph Neighborhood Readiness Decision: GNREADY-0004" in output
    assert "decision: `propose_separate_context_pack_integration_plan`" in output
    assert "selection_effect: `none`" in output
    assert "preserved_default_context_pack_behavior: `true`" in output
    assert "GNEVAL-FORMAT" in output
    assert "separate context-pack integration plan may be proposed" in output
    assert "does not implement or admit context-pack integration" in output
    assert "provider prompt changes" in output
    assert "automatic context inclusion" in output
