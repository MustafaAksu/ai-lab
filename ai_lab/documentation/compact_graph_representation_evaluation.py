from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from statistics import median
from typing import Iterable, Literal

from ai_lab.documentation.artifact_history import ArtifactRecord
from ai_lab.documentation.graph_neighborhood import graph_neighborhood_advisor
from ai_lab.documentation.reask import (
    ReaskPromptError,
    extract_section,
    strip_markdown_fence,
)


TOKEN_ESTIMATOR_ID = "whitespace_word_count_v1"
SELECTION_EFFECT = "none"
DEFAULT_BUDGETS = (500, 1000, 1500, 2000, 3000)

ScenarioName = Literal[
    "whole_artifact_baseline",
    "distance_aware_existing_compact",
    "distance_aware_metadata_lower_bound",
]
Recommendation = Literal[
    "reuse_existing_representations",
    "propose_separate_compact_representation_contract",
    "reject_distance_aware_approach",
]


@dataclass(frozen=True)
class ArtifactRepresentationProfile:
    """Read-only compact-representation inventory for one graph artifact."""

    artifact_id: str
    artifact_kind: str
    title: str
    path: str
    full_token_estimate: int
    semantic_compact_source: str | None
    semantic_compact_token_estimate: int | None
    metadata_lower_bound_token_estimate: int
    semantic_compact_available: bool
    metadata_lower_bound_semantically_sufficient: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryRepresentationInventory:
    """Repository-level inventory for existing compact representations."""

    token_estimator_id: str
    artifact_count: int
    artifact_kind_counts: tuple[tuple[str, int], ...]
    semantic_compact_artifact_count: int
    semantic_compact_kind_counts: tuple[tuple[str, int], ...]
    l0_record_count: int
    l1_record_count: int
    l1_record_count_with_citations: int
    l1_record_count_with_canonical_artifact_links: int
    artifact_summary_record_count: int
    profiles: tuple[ArtifactRepresentationProfile, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "token_estimator_id": self.token_estimator_id,
            "artifact_count": self.artifact_count,
            "artifact_kind_counts": dict(self.artifact_kind_counts),
            "semantic_compact_artifact_count": self.semantic_compact_artifact_count,
            "semantic_compact_kind_counts": dict(
                self.semantic_compact_kind_counts
            ),
            "l0_record_count": self.l0_record_count,
            "l1_record_count": self.l1_record_count,
            "l1_record_count_with_citations": (
                self.l1_record_count_with_citations
            ),
            "l1_record_count_with_canonical_artifact_links": (
                self.l1_record_count_with_canonical_artifact_links
            ),
            "artifact_summary_record_count": self.artifact_summary_record_count,
            "profiles": [profile.to_dict() for profile in self.profiles],
        }


@dataclass(frozen=True)
class PackingBudgetResult:
    """One deterministic what-if packing result."""

    target_id: str
    scenario: ScenarioName
    token_budget: int
    included_artifact_ids: tuple[str, ...]
    excluded_artifact_ids: tuple[str, ...]
    used_token_estimate: int

    @property
    def included_neighbor_count(self) -> int:
        return len(self.included_artifact_ids)

    def to_dict(self) -> dict[str, object]:
        return {
            "target_id": self.target_id,
            "scenario": self.scenario,
            "token_budget": self.token_budget,
            "included_artifact_ids": list(
                self.included_artifact_ids
            ),
            "excluded_artifact_ids": list(
                self.excluded_artifact_ids
            ),
            "used_token_estimate": self.used_token_estimate,
            "included_neighbor_count": (
                self.included_neighbor_count
            ),
        }


@dataclass(frozen=True)
class TargetRepresentationEvaluation:
    """Distance-aware evidence for one target artifact."""

    target_id: str
    isolated: bool
    candidate_count: int
    results: tuple[PackingBudgetResult, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "target_id": self.target_id,
            "isolated": self.isolated,
            "candidate_count": self.candidate_count,
            "results": [result.to_dict() for result in self.results],
        }


@dataclass(frozen=True)
class ScenarioAggregate:
    """Aggregate evidence for one scenario and budget."""

    scenario: ScenarioName
    token_budget: int
    connected_target_count: int
    targets_with_at_least_one_neighbor: int
    total_included_neighbors: int
    median_included_neighbors: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class CompactGraphRepresentationEvaluationReport:
    """Evidence-only report for PLAN-20260716-0002.

    This report has no context-selection effect and does not modify manifests,
    provider prompts, CLI behavior, graph persistence, retrieval, embeddings,
    reranking, indexes, memory stores, or runtime manifests.
    """

    evaluation_id: str
    selection_effect: str
    token_estimator_id: str
    budgets: tuple[int, ...]
    excluded_artifact_ids: tuple[str, ...]
    inventory: RepositoryRepresentationInventory
    target_evaluations: tuple[TargetRepresentationEvaluation, ...]
    aggregates: tuple[ScenarioAggregate, ...]
    connected_target_count: int
    isolated_target_ids: tuple[str, ...]
    recommendation: Recommendation
    recommendation_rationale: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": "v1",
            "evaluation_id": self.evaluation_id,
            "selection_effect": self.selection_effect,
            "token_estimator_id": self.token_estimator_id,
            "budgets": list(self.budgets),
            "excluded_artifact_ids": list(self.excluded_artifact_ids),
            "inventory": self.inventory.to_dict(),
            "target_evaluations": [
                evaluation.to_dict()
                for evaluation in self.target_evaluations
            ],
            "aggregates": [
                aggregate.to_dict()
                for aggregate in self.aggregates
            ],
            "connected_target_count": self.connected_target_count,
            "isolated_target_ids": list(self.isolated_target_ids),
            "recommendation": self.recommendation,
            "recommendation_rationale": self.recommendation_rationale,
            "boundary": (
                "Evidence-only. No context-selection, manifest, provider, "
                "prompt, CLI, persistence, retrieval, embedding, reranking, "
                "index, memory-store, or runtime-manifest changes."
            ),
        }


def estimate_text_tokens(text: str) -> int:
    """Match CAP-0005's deterministic whitespace token estimator."""

    return max(1, len(text.split()))


def inventory_repository_representations(
    *,
    artifact_records: Iterable[ArtifactRecord],
    l0_dir: Path = Path("docs/memory/l0"),
    l1_dir: Path = Path("docs/memory/l1"),
    docs_root: Path = Path("docs"),
) -> RepositoryRepresentationInventory:
    """Inventory existing compact representations without creating new ones."""

    records = tuple(artifact_records)
    artifact_ids = {record.artifact_id for record in records}
    profiles = tuple(
        _representation_profile(record)
        for record in sorted(records, key=lambda item: item.artifact_id)
    )

    kind_counts = _count_values(profile.artifact_kind for profile in profiles)
    semantic_kind_counts = _count_values(
        profile.artifact_kind
        for profile in profiles
        if profile.semantic_compact_available
    )

    l0_records = _json_records(l0_dir)
    l1_records = _json_records(l1_dir)
    artifact_summary_records = tuple(
        record
        for record in _json_records(docs_root)
        if _looks_like_artifact_summary(record)
    )

    l1_with_citations = sum(
        1
        for record in l1_records
        if isinstance(record.get("citations"), list)
        and bool(record["citations"])
    )
    l1_with_links = sum(
        1
        for record in l1_records
        if _l1_has_canonical_artifact_link(record, artifact_ids)
    )

    return RepositoryRepresentationInventory(
        token_estimator_id=TOKEN_ESTIMATOR_ID,
        artifact_count=len(profiles),
        artifact_kind_counts=kind_counts,
        semantic_compact_artifact_count=sum(
            1 for profile in profiles if profile.semantic_compact_available
        ),
        semantic_compact_kind_counts=semantic_kind_counts,
        l0_record_count=len(l0_records),
        l1_record_count=len(l1_records),
        l1_record_count_with_citations=l1_with_citations,
        l1_record_count_with_canonical_artifact_links=l1_with_links,
        artifact_summary_record_count=len(artifact_summary_records),
        profiles=profiles,
    )


def evaluate_compact_graph_representations(
    *,
    evaluation_id: str,
    artifact_records: Iterable[ArtifactRecord],
    budgets: Iterable[int] = DEFAULT_BUDGETS,
    max_depth: int = 2,
    excluded_artifact_ids: Iterable[str] = (),
    l0_dir: Path = Path("docs/memory/l0"),
    l1_dir: Path = Path("docs/memory/l1"),
    docs_root: Path = Path("docs"),
) -> CompactGraphRepresentationEvaluationReport:
    """Evaluate existing and lower-bound compact views as evidence only."""

    normalized_budgets = tuple(sorted(set(int(value) for value in budgets)))
    if not normalized_budgets or any(value < 1 for value in normalized_budgets):
        raise ValueError("budgets must contain positive integers.")

    excluded = tuple(sorted(set(excluded_artifact_ids)))
    excluded_set = set(excluded)
    records = tuple(
        record
        for record in artifact_records
        if record.artifact_id not in excluded_set
    )
    if not records:
        raise ValueError("artifact_records must contain at least one artifact.")

    inventory = inventory_repository_representations(
        artifact_records=records,
        l0_dir=l0_dir,
        l1_dir=l1_dir,
        docs_root=docs_root,
    )
    profile_index = {
        profile.artifact_id: profile
        for profile in inventory.profiles
    }

    target_evaluations: list[TargetRepresentationEvaluation] = []
    isolated_target_ids: list[str] = []

    for record in sorted(records, key=lambda item: item.artifact_id):
        advisor_report = graph_neighborhood_advisor(
            target_id=record.artifact_id,
            artifact_records=records,
            max_depth=max_depth,
            token_budget=None,
        )
        candidates = advisor_report.candidates

        if not candidates:
            isolated_target_ids.append(record.artifact_id)

        results: list[PackingBudgetResult] = []
        for budget in normalized_budgets:
            for scenario in (
                "whole_artifact_baseline",
                "distance_aware_existing_compact",
                "distance_aware_metadata_lower_bound",
            ):
                results.append(
                    _pack_candidates(
                        target_id=record.artifact_id,
                        candidates=candidates,
                        profile_index=profile_index,
                        scenario=scenario,
                        token_budget=budget,
                    )
                )

        target_evaluations.append(
            TargetRepresentationEvaluation(
                target_id=record.artifact_id,
                isolated=not candidates,
                candidate_count=len(candidates),
                results=tuple(results),
            )
        )

    aggregates = _aggregate_results(
        target_evaluations=tuple(target_evaluations),
        budgets=normalized_budgets,
    )
    recommendation, rationale = _recommendation(
        inventory=inventory,
        aggregates=aggregates,
    )

    return CompactGraphRepresentationEvaluationReport(
        evaluation_id=evaluation_id,
        selection_effect=SELECTION_EFFECT,
        token_estimator_id=TOKEN_ESTIMATOR_ID,
        budgets=normalized_budgets,
        excluded_artifact_ids=excluded,
        inventory=inventory,
        target_evaluations=tuple(target_evaluations),
        aggregates=aggregates,
        connected_target_count=(
            len(target_evaluations) - len(isolated_target_ids)
        ),
        isolated_target_ids=tuple(isolated_target_ids),
        recommendation=recommendation,
        recommendation_rationale=rationale,
    )


def format_compact_graph_representation_report(
    report: CompactGraphRepresentationEvaluationReport,
) -> str:
    """Format the evidence-only evaluation as Markdown."""

    inventory = report.inventory
    lines = [
        f"# Compact Graph Representation Evaluation: {report.evaluation_id}",
        "",
        f"- selection_effect: `{report.selection_effect}`",
        f"- token_estimator_id: `{report.token_estimator_id}`",
        f"- artifact_count: `{inventory.artifact_count}`",
        f"- connected_target_count: `{report.connected_target_count}`",
        f"- isolated_target_count: `{len(report.isolated_target_ids)}`",
        f"- excluded_artifact_ids: `{', '.join(report.excluded_artifact_ids)}`",
        f"- recommendation: `{report.recommendation}`",
        f"- recommendation_rationale: {report.recommendation_rationale}",
        "",
        "## Representation Inventory",
        "",
        f"- artifact_kind_counts: `{dict(inventory.artifact_kind_counts)}`",
        (
            "- semantic_compact_artifact_count: "
            f"`{inventory.semantic_compact_artifact_count}`"
        ),
        (
            "- semantic_compact_kind_counts: "
            f"`{dict(inventory.semantic_compact_kind_counts)}`"
        ),
        f"- l0_record_count: `{inventory.l0_record_count}`",
        f"- l1_record_count: `{inventory.l1_record_count}`",
        (
            "- l1_record_count_with_citations: "
            f"`{inventory.l1_record_count_with_citations}`"
        ),
        (
            "- l1_record_count_with_canonical_artifact_links: "
            f"`{inventory.l1_record_count_with_canonical_artifact_links}`"
        ),
        (
            "- artifact_summary_record_count: "
            f"`{inventory.artifact_summary_record_count}`"
        ),
        "",
        "## Aggregate Packing Evidence",
        "",
        (
            "Scenario | Budget | Connected Targets | Targets With Neighbor | "
            "Total Included | Median Included"
        ),
        "--- | ---: | ---: | ---: | ---: | ---:",
    ]

    for aggregate in report.aggregates:
        lines.append(
            " | ".join(
                [
                    aggregate.scenario,
                    str(aggregate.token_budget),
                    str(aggregate.connected_target_count),
                    str(aggregate.targets_with_at_least_one_neighbor),
                    str(aggregate.total_included_neighbors),
                    str(aggregate.median_included_neighbors),
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Isolated Targets",
            "",
        ]
    )
    if report.isolated_target_ids:
        lines.extend(f"- {artifact_id}" for artifact_id in report.isolated_target_ids)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            (
                "Existing semantic sections and metadata-only lower bounds are "
                "diagnostic representations, not implemented context-pack "
                "content. Metadata-only representations are explicitly marked "
                "semantically insufficient."
            ),
            "",
            "## Operational Boundary",
            "",
            (
                "This report is evidence-only. It does not modify "
                "ContextPackManifest.items, context selection, provider prompts, "
                "CLI behavior, graph persistence, retrieval, embeddings, "
                "reranking, production indexes, memory stores, or runtime "
                "manifests."
            ),
        ]
    )

    return "\n".join(lines)


def _representation_profile(
    record: ArtifactRecord,
) -> ArtifactRepresentationProfile:
    try:
        markdown = record.path.read_text(encoding="utf-8")
    except OSError:
        markdown = ""

    compact_source: str | None = None
    compact_text: str | None = None

    if record.kind == "SYNCOMP":
        compact_source = "markdown_section:Synthesis"
        compact_text = _optional_section(markdown, "Synthesis")
    elif record.kind == "ABS":
        compact_source = "markdown_section:Abstraction"
        compact_text = _optional_section(markdown, "Abstraction")

    metadata_text = "\n".join(
        value
        for value in (
            record.artifact_id,
            record.kind,
            record.title,
            record.source_comparison,
            record.source_synthesis,
            record.source_artifacts,
            record.abstraction_level,
        )
        if value
    )

    return ArtifactRepresentationProfile(
        artifact_id=record.artifact_id,
        artifact_kind=record.kind,
        title=record.title,
        path=record.path.as_posix(),
        full_token_estimate=estimate_text_tokens(markdown),
        semantic_compact_source=(compact_source if compact_text else None),
        semantic_compact_token_estimate=(
            estimate_text_tokens(compact_text)
            if compact_text
            else None
        ),
        metadata_lower_bound_token_estimate=estimate_text_tokens(
            metadata_text
        ),
        semantic_compact_available=bool(compact_text),
        metadata_lower_bound_semantically_sufficient=False,
    )


def _optional_section(markdown: str, heading: str) -> str | None:
    try:
        value = extract_section(markdown, heading)
    except ReaskPromptError:
        return None

    stripped = strip_markdown_fence(value).strip()
    return stripped or None


def _count_values(values: Iterable[str]) -> tuple[tuple[str, int], ...]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return tuple(sorted(counts.items()))


def _json_records(root: Path) -> tuple[dict[str, object], ...]:
    if not root.is_dir():
        return ()

    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            records.append(value)
    return tuple(records)


def _looks_like_artifact_summary(record: dict[str, object]) -> bool:
    required = {
        "artifact_cid",
        "version",
        "path",
        "artifact_type",
        "language",
        "size_bytes",
        "complexity_score",
    }
    return required.issubset(record)


def _l1_has_canonical_artifact_link(
    record: dict[str, object],
    artifact_ids: set[str],
) -> bool:
    citations = record.get("citations")
    if not isinstance(citations, list):
        return False

    for citation in citations:
        if isinstance(citation, str):
            if any(artifact_id in citation for artifact_id in artifact_ids):
                return True
            continue
        if not isinstance(citation, dict):
            continue
        values = " ".join(str(value) for value in citation.values())
        if any(artifact_id in values for artifact_id in artifact_ids):
            return True
    return False


def _candidate_cost(
    *,
    artifact_id: str,
    distance: int,
    profile_index: dict[str, ArtifactRepresentationProfile],
    scenario: ScenarioName,
) -> int:
    profile = profile_index[artifact_id]

    if scenario == "whole_artifact_baseline" or distance <= 1:
        return profile.full_token_estimate

    if scenario == "distance_aware_existing_compact":
        return (
            profile.semantic_compact_token_estimate
            if profile.semantic_compact_token_estimate is not None
            else profile.full_token_estimate
        )

    return profile.metadata_lower_bound_token_estimate


def _pack_candidates(
    *,
    target_id: str,
    candidates,
    profile_index: dict[str, ArtifactRepresentationProfile],
    scenario: ScenarioName,
    token_budget: int,
) -> PackingBudgetResult:
    included: list[str] = []
    excluded: list[str] = []
    used = 0

    for candidate in candidates:
        cost = _candidate_cost(
            artifact_id=candidate.artifact_id,
            distance=candidate.distance,
            profile_index=profile_index,
            scenario=scenario,
        )
        if used + cost <= token_budget:
            included.append(candidate.artifact_id)
            used += cost
        else:
            excluded.append(candidate.artifact_id)

    return PackingBudgetResult(
        target_id=target_id,
        scenario=scenario,
        token_budget=token_budget,
        included_artifact_ids=tuple(included),
        excluded_artifact_ids=tuple(excluded),
        used_token_estimate=used,
    )


def _aggregate_results(
    *,
    target_evaluations: tuple[TargetRepresentationEvaluation, ...],
    budgets: tuple[int, ...],
) -> tuple[ScenarioAggregate, ...]:
    connected = tuple(
        evaluation
        for evaluation in target_evaluations
        if not evaluation.isolated
    )
    aggregates: list[ScenarioAggregate] = []

    for scenario in (
        "whole_artifact_baseline",
        "distance_aware_existing_compact",
        "distance_aware_metadata_lower_bound",
    ):
        for budget in budgets:
            matching = [
                result
                for evaluation in connected
                for result in evaluation.results
                if result.scenario == scenario
                and result.token_budget == budget
            ]
            counts = [result.included_neighbor_count for result in matching]
            aggregates.append(
                ScenarioAggregate(
                    scenario=scenario,
                    token_budget=budget,
                    connected_target_count=len(connected),
                    targets_with_at_least_one_neighbor=sum(
                        1 for count in counts if count > 0
                    ),
                    total_included_neighbors=sum(counts),
                    median_included_neighbors=(
                        float(median(counts)) if counts else 0.0
                    ),
                )
            )

    return tuple(aggregates)


def _recommendation(
    *,
    inventory: RepositoryRepresentationInventory,
    aggregates: tuple[ScenarioAggregate, ...],
) -> tuple[Recommendation, str]:
    index = {
        (aggregate.scenario, aggregate.token_budget): aggregate
        for aggregate in aggregates
    }
    low_budgets = tuple(
        budget
        for budget in DEFAULT_BUDGETS
        if budget <= 1500
        and ("whole_artifact_baseline", budget) in index
    )
    existing_gain = sum(
        index[("distance_aware_existing_compact", budget)].total_included_neighbors
        - index[("whole_artifact_baseline", budget)].total_included_neighbors
        for budget in low_budgets
    )
    lower_bound_gain = sum(
        index[("distance_aware_metadata_lower_bound", budget)].total_included_neighbors
        - index[("whole_artifact_baseline", budget)].total_included_neighbors
        for budget in low_budgets
    )
    semantic_gap_count = (
        inventory.artifact_count - inventory.semantic_compact_artifact_count
    )

    if existing_gain > 0 and semantic_gap_count == 0:
        return (
            "reuse_existing_representations",
            (
                "Existing semantic compact representations improve low-budget "
                "neighbor retention and cover the evaluated artifact corpus."
            ),
        )

    if semantic_gap_count > 0 or lower_bound_gain > existing_gain:
        return (
            "propose_separate_compact_representation_contract",
            (
                "Existing semantic compact coverage is incomplete or fails to "
                "capture the improvement suggested by the metadata-only lower "
                "bound. A separately governed AI-optimized compact "
                "representation contract should be considered before runtime "
                "graph-local context implementation."
            ),
        )

    return (
        "reject_distance_aware_approach",
        (
            "Neither existing compact representations nor the metadata-only "
            "lower bound improve low-budget graph-neighbor retention."
        ),
    )
