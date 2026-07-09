from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

from ai_lab.documentation.artifact_history import ArtifactRecord
from ai_lab.documentation.graph_neighborhood import (
    GraphNeighborhoodReport,
    graph_neighborhood_advisor,
)


IntegrationRecommendation = Literal["plan_separately", "not_ready"]


@dataclass(frozen=True)
class GraphNeighborhoodEvidenceFinding:
    """One evidence finding from a graph-neighborhood diagnostic report."""

    code: str
    passed: bool
    summary: str


@dataclass(frozen=True)
class GraphNeighborhoodEvidenceReport:
    """Evidence-only evaluation report for CAP-0005.

    This report is deliberately diagnostic-only. It has no selection effect and
    does not modify context manifests, provider prompts, graph records, indexes,
    memory stores, retrieval, embeddings, reranking, or automatic inclusion.
    """

    evaluation_id: str
    target_id: str
    selection_effect: str
    advisor_report: GraphNeighborhoodReport
    findings: tuple[GraphNeighborhoodEvidenceFinding, ...]
    integration_recommendation: IntegrationRecommendation
    recommendation_rationale: str

    @property
    def passed_findings(self) -> tuple[GraphNeighborhoodEvidenceFinding, ...]:
        return tuple(finding for finding in self.findings if finding.passed)

    @property
    def failed_findings(self) -> tuple[GraphNeighborhoodEvidenceFinding, ...]:
        return tuple(finding for finding in self.findings if not finding.passed)


def evaluate_graph_neighborhood_advisor(
    *,
    evaluation_id: str,
    target_id: str,
    artifact_records: Iterable[ArtifactRecord],
    edge_records: Iterable[dict[str, object]] = (),
    future_edge_seed_records: Iterable[dict[str, str]] = (),
    max_depth: int = 2,
    token_budget: int | None = None,
) -> GraphNeighborhoodEvidenceReport:
    """Evaluate CAP-0005 output as evidence only."""

    advisor_report = graph_neighborhood_advisor(
        target_id=target_id,
        artifact_records=artifact_records,
        edge_records=edge_records,
        future_edge_seed_records=future_edge_seed_records,
        max_depth=max_depth,
        token_budget=token_budget,
    )

    findings = _findings_for_report(advisor_report)
    recommendation, rationale = _recommendation_for_findings(findings)

    return GraphNeighborhoodEvidenceReport(
        evaluation_id=evaluation_id,
        target_id=target_id,
        selection_effect="none",
        advisor_report=advisor_report,
        findings=findings,
        integration_recommendation=recommendation,
        recommendation_rationale=rationale,
    )


def format_graph_neighborhood_evidence_report(
    report: GraphNeighborhoodEvidenceReport,
) -> str:
    """Format an evidence-only graph-neighborhood evaluation report."""

    lines = [
        f"# Graph Neighborhood Evidence Report: {report.evaluation_id}",
        "",
        f"- target_id: `{report.target_id}`",
        f"- selection_effect: `{report.selection_effect}`",
        f"- integration_recommendation: `{report.integration_recommendation}`",
        f"- recommendation_rationale: {report.recommendation_rationale}",
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
            "## Candidate Evidence",
            "",
            "ID | Decision | Distance | Authority | Tokens | Path",
            "--- | --- | ---: | --- | ---: | ---",
        ]
    )

    for candidate in report.advisor_report.candidates:
        authority = "authoritative" if candidate.authoritative else "non_authoritative"
        path = " ; ".join(candidate.relation_path)
        lines.append(
            " | ".join(
                [
                    candidate.artifact_id,
                    candidate.decision,
                    str(candidate.distance),
                    authority,
                    str(candidate.token_estimate),
                    path,
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            (
                "This report is evidence-only. It does not modify context selection, "
                "provider prompts, graph persistence, retrieval, embeddings, reranking, "
                "production indexes, memory stores, runtime manifests, or automatic "
                "context inclusion."
            ),
        ]
    )

    return "\n".join(lines)


def _findings_for_report(
    report: GraphNeighborhoodReport,
) -> tuple[GraphNeighborhoodEvidenceFinding, ...]:
    candidates = report.candidates

    has_relation_paths = bool(candidates) and all(
        bool(candidate.relation_path)
        for candidate in candidates
    )
    has_authority_labels = bool(candidates) and all(
        isinstance(candidate.authoritative, bool)
        for candidate in candidates
    )
    has_token_estimates = bool(candidates) and all(
        candidate.token_estimate > 0
        for candidate in candidates
    )
    has_rationales = bool(candidates) and all(
        bool(candidate.rationale.strip())
        for candidate in candidates
    )
    has_diagnostic_decisions = bool(candidates) and all(
        candidate.decision in {"included", "excluded"}
        for candidate in candidates
    )
    no_selection_effect = True

    return (
        GraphNeighborhoodEvidenceFinding(
            code="RELATION_PATHS_PRESENT",
            passed=has_relation_paths,
            summary="Every candidate exposes at least one relation-path explanation.",
        ),
        GraphNeighborhoodEvidenceFinding(
            code="AUTHORITY_LABELS_PRESENT",
            passed=has_authority_labels,
            summary="Every candidate exposes an authoritative or non-authoritative label.",
        ),
        GraphNeighborhoodEvidenceFinding(
            code="TOKEN_ESTIMATES_PRESENT",
            passed=has_token_estimates,
            summary="Every candidate exposes a positive token estimate.",
        ),
        GraphNeighborhoodEvidenceFinding(
            code="DIAGNOSTIC_RATIONALES_PRESENT",
            passed=has_rationales,
            summary="Every candidate exposes diagnostic inclusion/exclusion rationale.",
        ),
        GraphNeighborhoodEvidenceFinding(
            code="DIAGNOSTIC_DECISIONS_PRESENT",
            passed=has_diagnostic_decisions,
            summary="Every candidate exposes a diagnostic included/excluded decision.",
        ),
        GraphNeighborhoodEvidenceFinding(
            code="SELECTION_EFFECT_NONE",
            passed=no_selection_effect,
            summary="The evaluation report has no context-selection effect.",
        ),
    )


def _recommendation_for_findings(
    findings: tuple[GraphNeighborhoodEvidenceFinding, ...],
) -> tuple[IntegrationRecommendation, str]:
    failed = tuple(finding for finding in findings if not finding.passed)

    if failed:
        failed_codes = ", ".join(finding.code for finding in failed)
        return (
            "not_ready",
            (
                "Do not plan context-pack integration yet; unresolved evidence "
                f"findings remain: {failed_codes}."
            ),
        )

    return (
        "plan_separately",
        (
            "CAP-0005 evidence is structurally usable for a future context-pack "
            "integration discussion, but integration must be planned separately."
        ),
    )
