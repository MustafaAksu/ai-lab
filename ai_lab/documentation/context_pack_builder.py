from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from ai_lab.documentation.artifact_history import (
    ArtifactRecord,
    context_level_for_record,
    latest_records_by_context_level,
)
from ai_lab.documentation.context_pack import (
    ContextPackError,
    ContextPackExclusion,
    ContextPackItem,
    ContextPackManifest,
)


def _shorten(value: str, max_length: int = 240) -> str:
    """Return a compact non-empty string within max_length."""
    value = " ".join(value.split())

    if len(value) <= max_length:
        return value

    return value[: max_length - 3].rstrip() + "..."


def estimate_tokens_for_text(text: str) -> int:
    """Estimate token count using a simple chars/4 approximation."""
    if not text:
        return 0

    return max(1, (len(text) + 3) // 4)


def estimate_tokens_for_path(path: Path) -> int:
    """Estimate token count for a text artifact path.

    Missing or unreadable files return 0 so manifest construction remains robust.
    """
    try:
        if not path.is_file():
            return 0

        return estimate_tokens_for_text(path.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        return 0


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
    token_estimate: int | None = None,
) -> ContextPackItem:
    """Create a context-pack item from one artifact-history record."""
    level = context_level_for_record(record) or record.kind
    reason = _shorten(f"{level} context seed: {record.title}")

    if token_estimate is None:
        token_estimate = estimate_tokens_for_path(record.path)

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


def select_items_with_budget(
    items: tuple[ContextPackItem, ...],
    token_budget: int | None,
) -> tuple[tuple[ContextPackItem, ...], tuple[ContextPackExclusion, ...]]:
    """Select context items within token budget and record exclusions."""
    if token_budget is None:
        return items, ()

    selected: list[ContextPackItem] = []
    exclusions: list[ContextPackExclusion] = []
    used_tokens = 0

    for item in items:
        would_use = used_tokens + item.token_estimate

        if would_use <= token_budget:
            selected.append(item)
            used_tokens = would_use
            continue

        exclusions.append(
            ContextPackExclusion(
                item_id=item.item_id,
                reason="too_large",
                note=(
                    f"Estimated {item.token_estimate} tokens would exceed "
                    f"budget {token_budget}."
                ),
            )
        )

    if not selected and items:
        raise ContextPackError("No context items fit within token_budget.")

    return tuple(selected), tuple(exclusions)


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

    candidate_items = tuple(
        context_item_from_record(
            record=record,
            relevance_score=0.9,
        )
        for record in ordered_records
    )

    selected_items, exclusions = select_items_with_budget(
        items=candidate_items,
        token_budget=token_budget,
    )

    return ContextPackManifest(
        task=task,
        assembly_policy="latest_context",
        items=selected_items,
        token_budget=token_budget,
        exclusions=exclusions,
        model_target=model_target,
        pipeline_run_id=pipeline_run_id,
    )
