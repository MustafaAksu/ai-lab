from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

from ai_lab.documentation.artifact_history import (
    ArtifactRecord,
    artifact_id_from_path,
    relation_label_for_child,
    source_paths_for_record,
)
from ai_lab.documentation.edge_validation import validate_edge_record


RelationSource = Literal["artifact_lineage", "edge_record", "future_edge_seed"]
Decision = Literal["included", "excluded"]


class GraphNeighborhoodError(ValueError):
    """Raised when graph-neighborhood diagnostics cannot be computed."""


@dataclass(frozen=True)
class GraphRelation:
    """A read-only graph relation used for diagnostic neighborhood advice."""

    source_id: str
    predicate: str
    target_id: str
    relation_source: RelationSource
    authoritative: bool
    scope: str | None = None
    evidence: str | None = None


@dataclass(frozen=True)
class GraphNeighborCandidate:
    """One graph-local candidate and its explanation."""

    artifact_id: str
    title: str
    kind: str
    distance: int
    relation_path: tuple[str, ...]
    relation_sources: tuple[RelationSource, ...]
    authoritative: bool
    token_estimate: int
    decision: Decision
    rationale: str


@dataclass(frozen=True)
class GraphNeighborhoodReport:
    """Read-only diagnostic report for graph-local scoped memory."""

    target_id: str
    max_depth: int
    token_budget: int | None
    candidates: tuple[GraphNeighborCandidate, ...]

    @property
    def selected_artifact_ids(self) -> tuple[str, ...]:
        return tuple(
            candidate.artifact_id
            for candidate in self.candidates
            if candidate.decision == "included"
        )

    @property
    def excluded_artifact_ids(self) -> tuple[str, ...]:
        return tuple(
            candidate.artifact_id
            for candidate in self.candidates
            if candidate.decision == "excluded"
        )

    @property
    def selected_token_estimate(self) -> int:
        return sum(
            candidate.token_estimate
            for candidate in self.candidates
            if candidate.decision == "included"
        )


def artifact_lineage_relations(records: Iterable[ArtifactRecord]) -> tuple[GraphRelation, ...]:
    """Return graph relations derived from artifact source metadata."""

    relations: list[GraphRelation] = []

    for record in records:
        predicate = _predicate_for_artifact_child(record)

        for source_path in source_paths_for_record(record):
            source_id = artifact_id_from_path(Path(source_path))
            relations.append(
                GraphRelation(
                    source_id=source_id,
                    predicate=predicate,
                    target_id=record.artifact_id,
                    relation_source="artifact_lineage",
                    authoritative=True,
                    evidence=str(record.path),
                )
            )

    return tuple(relations)


def edge_record_relations(edge_records: Iterable[dict[str, Any]]) -> tuple[GraphRelation, ...]:
    """Return graph relations derived from validated EDGE records."""

    relations: list[GraphRelation] = []

    for edge in edge_records:
        errors = validate_edge_record(edge)
        if errors:
            edge_id = edge.get("id", "<unknown>")
            raise GraphNeighborhoodError(
                f"Invalid EDGE record {edge_id}: {'; '.join(errors)}"
            )

        subject = _mapping(edge["subject"], "subject")
        predicate = _mapping(edge["predicate"], "predicate")
        obj = _mapping(edge["object"], "object")

        relations.append(
            GraphRelation(
                source_id=str(subject["id"]),
                predicate=str(predicate["id"]),
                target_id=str(obj["id"]),
                relation_source="edge_record",
                authoritative=True,
                scope=str(obj.get("scope")) if obj.get("scope") is not None else None,
                evidence=str(edge["id"]),
            )
        )

    return tuple(relations)


def future_edge_seed_relations(
    seed_records: Iterable[dict[str, str]],
) -> tuple[GraphRelation, ...]:
    """Return non-authoritative relations from future edge seed records."""

    relations: list[GraphRelation] = []

    for seed in seed_records:
        try:
            source_id = seed["source_id"]
            predicate = seed["predicate"]
            target_id = seed["target_id"]
        except KeyError as exc:
            raise GraphNeighborhoodError(
                f"Future edge seed is missing required field: {exc.args[0]}"
            ) from exc

        relations.append(
            GraphRelation(
                source_id=str(source_id),
                predicate=str(predicate),
                target_id=str(target_id),
                relation_source="future_edge_seed",
                authoritative=False,
                evidence="future_edge_seed",
            )
        )

    return tuple(relations)


def graph_neighborhood_advisor(
    *,
    target_id: str,
    artifact_records: Iterable[ArtifactRecord],
    edge_records: Iterable[dict[str, Any]] = (),
    future_edge_seed_records: Iterable[dict[str, str]] = (),
    max_depth: int = 2,
    token_budget: int | None = None,
) -> GraphNeighborhoodReport:
    """
    Return a read-only graph-local neighborhood diagnostic report.

    This advisor does not modify context selection, provider prompts, manifests,
    persisted graph artifacts, retrieval, embeddings, indexes, or memory stores.
    """

    if max_depth < 1:
        raise GraphNeighborhoodError("max_depth must be at least 1.")

    records = tuple(artifact_records)
    record_index = {record.artifact_id: record for record in records}

    if target_id not in record_index:
        raise GraphNeighborhoodError(f"Target artifact not found: {target_id}")

    relations = (
        *artifact_lineage_relations(records),
        *edge_record_relations(edge_records),
        *future_edge_seed_relations(future_edge_seed_records),
    )

    paths = _shortest_relation_paths(
        target_id=target_id,
        relations=relations,
        max_depth=max_depth,
    )

    raw_candidates: list[GraphNeighborCandidate] = []

    for artifact_id, path in sorted(
        paths.items(),
        key=lambda item: (len(item[1]), item[0]),
    ):
        if artifact_id == target_id or artifact_id not in record_index:
            continue

        record = record_index[artifact_id]
        relation_sources = tuple(relation.relation_source for relation, _ in path)
        authoritative = all(relation.authoritative for relation, _ in path)
        raw_candidates.append(
            GraphNeighborCandidate(
                artifact_id=artifact_id,
                title=record.title,
                kind=record.kind,
                distance=len(path),
                relation_path=tuple(_format_path_step(relation, direction) for relation, direction in path),
                relation_sources=relation_sources,
                authoritative=authoritative,
                token_estimate=_estimate_tokens_for_record(record),
                decision="included",
                rationale=(
                    "Included by graph-neighborhood diagnostic; this has no "
                    "runtime selection effect."
                ),
            )
        )

    candidates = _apply_budget(raw_candidates, token_budget=token_budget)

    return GraphNeighborhoodReport(
        target_id=target_id,
        max_depth=max_depth,
        token_budget=token_budget,
        candidates=tuple(candidates),
    )


def format_graph_neighborhood_report(report: GraphNeighborhoodReport) -> str:
    """Format a graph-neighborhood report as human-readable Markdown."""

    lines = [
        f"# Graph Neighborhood Diagnostic for {report.target_id}",
        "",
        f"- max_depth: `{report.max_depth}`",
        f"- token_budget: `{report.token_budget}`",
        f"- selected_token_estimate: `{report.selected_token_estimate}`",
        f"- selection_effect: `none`",
        "",
        "ID | Decision | Distance | Tokens | Source | Path | Rationale",
        "--- | --- | ---: | ---: | --- | --- | ---",
    ]

    for candidate in report.candidates:
        sources = ", ".join(candidate.relation_sources)
        path = " ; ".join(candidate.relation_path)
        lines.append(
            " | ".join(
                [
                    candidate.artifact_id,
                    candidate.decision,
                    str(candidate.distance),
                    str(candidate.token_estimate),
                    sources,
                    path,
                    candidate.rationale,
                ]
            )
        )

    return "\n".join(lines)


def _predicate_for_artifact_child(record: ArtifactRecord) -> str:
    return relation_label_for_child(record).replace("-", "_").replace(" ", "_")


def _mapping(value: object, field_name: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise GraphNeighborhoodError(f"{field_name} must be a mapping.")
    return value


def _estimate_tokens_for_record(record: ArtifactRecord) -> int:
    try:
        text = record.path.read_text(encoding="utf-8")
    except OSError:
        return 1

    return max(1, len(text.split()))


def _shortest_relation_paths(
    *,
    target_id: str,
    relations: tuple[GraphRelation, ...],
    max_depth: int,
) -> dict[str, tuple[tuple[GraphRelation, str], ...]]:
    adjacency: dict[str, list[tuple[str, GraphRelation, str]]] = {}

    for relation in relations:
        adjacency.setdefault(relation.source_id, []).append(
            (relation.target_id, relation, "forward")
        )
        adjacency.setdefault(relation.target_id, []).append(
            (relation.source_id, relation, "reverse")
        )

    for items in adjacency.values():
        items.sort(key=lambda item: (item[0], item[1].predicate, item[2]))

    paths: dict[str, tuple[tuple[GraphRelation, str], ...]] = {
        target_id: (),
    }
    queue: deque[str] = deque([target_id])

    while queue:
        current = queue.popleft()
        current_path = paths[current]

        if len(current_path) >= max_depth:
            continue

        for neighbor, relation, direction in adjacency.get(current, []):
            if neighbor in paths:
                continue

            paths[neighbor] = (*current_path, (relation, direction))
            queue.append(neighbor)

    return paths


def _format_path_step(relation: GraphRelation, direction: str) -> str:
    scope = f" scope={relation.scope}" if relation.scope else ""
    source = f" source={relation.relation_source}"
    authority = " authoritative" if relation.authoritative else " non_authoritative"

    if direction == "forward":
        return (
            f"{relation.source_id} -[{relation.predicate}{scope};"
            f"{source};{authority}]-> {relation.target_id}"
        )

    return (
        f"{relation.target_id} <-[{relation.predicate}{scope};"
        f"{source};{authority}]- {relation.source_id}"
    )


def _apply_budget(
    candidates: Iterable[GraphNeighborCandidate],
    *,
    token_budget: int | None,
) -> tuple[GraphNeighborCandidate, ...]:
    if token_budget is None:
        return tuple(candidates)

    used = 0
    updated: list[GraphNeighborCandidate] = []

    for candidate in candidates:
        would_use = used + candidate.token_estimate

        if would_use <= token_budget:
            used = would_use
            updated.append(candidate)
            continue

        updated.append(
            GraphNeighborCandidate(
                artifact_id=candidate.artifact_id,
                title=candidate.title,
                kind=candidate.kind,
                distance=candidate.distance,
                relation_path=candidate.relation_path,
                relation_sources=candidate.relation_sources,
                authoritative=candidate.authoritative,
                token_estimate=candidate.token_estimate,
                decision="excluded",
                rationale=(
                    f"Excluded by diagnostic token budget {token_budget}; "
                    f"estimated {candidate.token_estimate} tokens would exceed "
                    f"remaining budget."
                ),
            )
        )

    return tuple(updated)
