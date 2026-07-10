from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

from ai_lab.documentation.graph_neighborhood_evaluation import (
    GraphNeighborhoodEvidenceReport,
)


ReadinessDecision = Literal[
    "propose_separate_context_pack_integration_plan",
    "do_not_propose_yet",
]


@dataclass(frozen=True)
class GraphNeighborhoodReadinessFinding:
    """One readiness finding derived from CAP-0006 evidence-only reports."""

    code: str
    passed: bool
    summary: str


@dataclass(frozen=True)
class GraphNeighborhoodIntegrationReadinessReport:
    """Evidence-only decision report for graph-neighborhood integration readiness.

    This report decides only whether a separate context-pack integration plan
    should be proposed. It does not admit or implement integration and has no
    context-selection effect.
    """

    readiness_id: str
    decision: ReadinessDecision
    decision_rationale: str
    selection_effect: str
    preserved_default_context_pack_behavior: bool
    evidence_reports: tuple[GraphNeighborhoodEvidenceReport, ...]
    findings: tuple[GraphNeighborhoodReadinessFinding, ...]
    blocked_integration_behaviors: tuple[str, ...]

    @property
    def evidence_report_ids(self) -> tuple[str, ...]:
        return tuple(report.evaluation_id for report in self.evidence_reports)

    @property
    def passed_findings(self) -> tuple[GraphNeighborhoodReadinessFinding, ...]:
        return tuple(finding for finding in self.findings if finding.passed)

    @property
    def failed_findings(self) -> tuple[GraphNeighborhoodReadinessFinding, ...]:
        return tuple(finding for finding in self.findings if not finding.passed)


def decide_graph_neighborhood_integration_readiness(
    *,
    readiness_id: str,
    evidence_reports: Iterable[GraphNeighborhoodEvidenceReport],
) -> GraphNeighborhoodIntegrationReadinessReport:
    """Decide whether to propose a separate integration plan from CAP-0006 evidence.

    The decision is intentionally narrow: a positive decision means only
    "propose a separate governed plan." It never authorizes integration.
    """

    reports = tuple(evidence_reports)
    findings = _findings_for_reports(reports)
    decision, rationale = _decision_for_findings(findings)

    return GraphNeighborhoodIntegrationReadinessReport(
        readiness_id=readiness_id,
        decision=decision,
        decision_rationale=rationale,
        selection_effect="none",
        preserved_default_context_pack_behavior=True,
        evidence_reports=reports,
        findings=findings,
        blocked_integration_behaviors=(
            "context-pack integration",
            "runtime context selection changes",
            "provider prompt changes",
            "persisted graph node or edge writes",
            "graph database adoption",
            "retrieval calls",
            "embedding calls",
            "reranking calls",
            "production index mutation",
            "memory-store mutation",
            "runtime-manifest mutation",
            "automatic context inclusion",
        ),
    )


def format_graph_neighborhood_readiness_report(
    report: GraphNeighborhoodIntegrationReadinessReport,
) -> str:
    """Format a graph-neighborhood readiness decision report."""

    lines = [
        f"# Graph Neighborhood Readiness Decision: {report.readiness_id}",
        "",
        f"- decision: `{report.decision}`",
        f"- decision_rationale: {report.decision_rationale}",
        f"- selection_effect: `{report.selection_effect}`",
        (
            "- preserved_default_context_pack_behavior: "
            f"`{str(report.preserved_default_context_pack_behavior).lower()}`"
        ),
        f"- evidence_report_ids: `{', '.join(report.evidence_report_ids)}`",
        "",
        "## Findings",
        "",
        "Code | Passed | Summary",
        "--- | --- | ---",
    ]

    for finding in report.findings:
        lines.append(
            f"{finding.code} | {str(finding.passed).lower()} | {finding.summary}"
        )

    lines.extend(
        [
            "",
            "## Evidence Reports",
            "",
            "ID | Target | Recommendation | Failed Findings | Selection Effect",
            "--- | --- | --- | ---: | ---",
        ]
    )

    for evidence_report in report.evidence_reports:
        lines.append(
            " | ".join(
                [
                    evidence_report.evaluation_id,
                    evidence_report.target_id,
                    evidence_report.integration_recommendation,
                    str(len(evidence_report.failed_findings)),
                    evidence_report.selection_effect,
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Blocked Behaviors",
            "",
        ]
    )

    for behavior in report.blocked_integration_behaviors:
        lines.append(f"- {behavior}")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            (
                "This readiness report is evidence-only. A positive decision means only "
                "that a separate context-pack integration plan may be proposed. It does "
                "not implement or admit context-pack integration, context selection, "
                "provider prompt changes, graph persistence, retrieval, embeddings, "
                "reranking, production index mutation, memory-store mutation, "
                "runtime-manifest mutation, or automatic context inclusion."
            ),
        ]
    )

    return "\n".join(lines)


def _findings_for_reports(
    reports: tuple[GraphNeighborhoodEvidenceReport, ...],
) -> tuple[GraphNeighborhoodReadinessFinding, ...]:
    has_reports = bool(reports)

    all_selection_effect_none = has_reports and all(
        report.selection_effect == "none"
        for report in reports
    )
    all_evidence_passed = has_reports and all(
        not report.failed_findings
        for report in reports
    )
    all_recommend_separate_planning = has_reports and all(
        report.integration_recommendation == "plan_separately"
        for report in reports
    )
    all_have_evidence_ids = has_reports and all(
        bool(report.evaluation_id)
        for report in reports
    )

    return (
        GraphNeighborhoodReadinessFinding(
            code="CAP_0006_EVIDENCE_REPORTS_PRESENT",
            passed=has_reports,
            summary="At least one CAP-0006 evidence-only report is present.",
        ),
        GraphNeighborhoodReadinessFinding(
            code="CAP_0006_EVIDENCE_IDS_PRESENT",
            passed=all_have_evidence_ids,
            summary="Every CAP-0006 evidence report has an evaluation identifier.",
        ),
        GraphNeighborhoodReadinessFinding(
            code="ALL_EVIDENCE_REPORTS_PASSED",
            passed=all_evidence_passed,
            summary="Every CAP-0006 evidence report has no failed findings.",
        ),
        GraphNeighborhoodReadinessFinding(
            code="ALL_EVIDENCE_SELECTION_EFFECT_NONE",
            passed=all_selection_effect_none,
            summary="Every CAP-0006 evidence report preserves selection_effect none.",
        ),
        GraphNeighborhoodReadinessFinding(
            code="ALL_EVIDENCE_RECOMMENDS_SEPARATE_PLANNING",
            passed=all_recommend_separate_planning,
            summary="Every CAP-0006 evidence report recommends separate planning.",
        ),
        GraphNeighborhoodReadinessFinding(
            code="DEFAULT_CONTEXT_PACK_BEHAVIOR_PRESERVED",
            passed=True,
            summary="The readiness report does not change default context-pack behavior.",
        ),
        GraphNeighborhoodReadinessFinding(
            code="NO_RUNTIME_INTEGRATION_AUTHORIZED",
            passed=True,
            summary="The readiness report does not authorize runtime integration.",
        ),
    )


def _decision_for_findings(
    findings: tuple[GraphNeighborhoodReadinessFinding, ...],
) -> tuple[ReadinessDecision, str]:
    failed = tuple(finding for finding in findings if not finding.passed)

    if failed:
        failed_codes = ", ".join(finding.code for finding in failed)
        return (
            "do_not_propose_yet",
            (
                "Do not propose a context-pack integration plan yet; unresolved "
                f"readiness findings remain: {failed_codes}."
            ),
        )

    return (
        "propose_separate_context_pack_integration_plan",
        (
            "CAP-0006 evidence-only reports are adequate to propose a separate "
            "governed context-pack integration plan, but this decision does not "
            "admit or implement integration."
        ),
    )
