from __future__ import annotations

from collections.abc import Iterable

from ai_lab.documentation.artifact_history import (
    ArtifactRecord,
    context_level_for_record,
    latest_records_by_context_level,
)
from ai_lab.documentation.context_pack import (
    ContextPackItem,
    ContextPackManifest,
)


def _shorten(value: str, max_length: int = 240) -> str:
    """Return a compact non-empty string within max_length."""
    value = " ".join(value.split())

    if len(value) <= max_length:
        return value

    return value[: max_length - 3].rstrip() + "..."


def item_type_for_record(record: ArtifactRecord) -> str:
    """Map artifact-history record kinds to context-pack item types."""
    if record.kind == "ABS":
        return "abstraction"

    if record.kind == "SYNCOMP":
        return "synthesis"

    if record.kind == "COMP":
        return "comparison"

    return "artifact_summary"


def context_item_from_record(
    record: ArtifactRecord,
    relevance_score: float = 0.8,
    token_estimate: int = 0,
) -> ContextPackItem:
    """Create a context-pack item from one artifact-history record."""
    level = context_level_for_record(record) or record.kind
    reason = _shorten(f"{level} context seed: {record.title}")

    return ContextPackItem(
        item_type=item_type_for_record(record),
        item_id=record.artifact_id,
        reason=reason,
        relevance_score=relevance_score,
        token_estimate=token_estimate,
        source_path=str(record.path),
    )


def _context_level_sort_key(level: str) -> tuple[int, str]:
    if level.startswith("ABS-L"):
        try:
            return (int(level.removeprefix("ABS-L")), level)
        except ValueError:
            return (90, level)

    if level == "SYNCOMP":
        return (100, level)

    if level == "COMP":
        return (110, level)

    return (999, level)


def build_latest_context_manifest(
    task: str,
    records: Iterable[ArtifactRecord],
    token_budget: int | None = None,
    model_target: str | None = None,
    pipeline_run_id: str | None = None,
) -> ContextPackManifest:
    """
    Build a manifest from the latest useful context records.

    Selection is delegated to artifact_history.latest_records_by_context_level.
    This keeps context-pack construction aligned with the existing latest-context
    seed view.
    """
    latest_by_level = latest_records_by_context_level(records)

    ordered_records = tuple(
        latest_by_level[level]
        for level in sorted(latest_by_level, key=_context_level_sort_key)
    )

    items = tuple(
        context_item_from_record(
            record=record,
            relevance_score=0.9,
            token_estimate=0,
        )
        for record in ordered_records
    )

    return ContextPackManifest(
        task=task,
        assembly_policy="latest_context",
        items=items,
        token_budget=token_budget,
        model_target=model_target,
        pipeline_run_id=pipeline_run_id,
    )
