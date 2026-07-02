from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from ai_lab.documentation.artifact_history import (
    ArtifactRecord,
    context_level_for_record,
    latest_records_by_context_level,
)
from ai_lab.documentation.context_admission import (
    ContextAdmissionError,
    ContextAdmissionVerdict,
)
from ai_lab.documentation.context_pack import (
    ContextPackError,
    ContextPackExclusion,
    ContextPackItem,
    ContextPackManifest,
)
from ai_lab.documentation.interaction_log import EpisodeL1Summary, InteractionLogError


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


def _latest_context_admission_verdicts(
    admission_dir: Path = Path("docs/memory/admissions"),
) -> dict[tuple[str, str], ContextAdmissionVerdict]:
    """Return latest admission verdict per (target_item_id, target_item_type)."""

    if not admission_dir.is_dir():
        return {}

    latest: dict[tuple[str, str], ContextAdmissionVerdict] = {}

    for path in sorted(admission_dir.glob("*.json")):
        try:
            verdict = ContextAdmissionVerdict.read_json(path)
        except (ContextAdmissionError, OSError, ValueError):
            continue

        key = (verdict.target_item_id, verdict.target_item_type)
        previous = latest.get(key)

        if previous is None or (verdict.created_at, verdict.verdict_id) > (
            previous.created_at,
            previous.verdict_id,
        ):
            latest[key] = verdict

    return latest


def context_item_with_admission_verdict(
    item: ContextPackItem,
    verdict: ContextAdmissionVerdict | None,
) -> ContextPackItem:
    """Return item annotated with admission verdict metadata, if provided."""

    if verdict is None:
        return item

    return ContextPackItem(
        item_type=item.item_type,
        item_id=item.item_id,
        reason=item.reason,
        relevance_score=item.relevance_score,
        token_estimate=item.token_estimate,
        source_path=item.source_path,
        citation=item.citation,
        admission_verdict_id=verdict.verdict_id,
        admission_decision=verdict.decision,
        freshness_state=verdict.freshness_state,
        warrant_state=verdict.warrant_state,
    )


def annotate_items_with_admission_verdicts(
    items: tuple[ContextPackItem, ...],
    admission_dir: Path = Path("docs/memory/admissions"),
) -> tuple[ContextPackItem, ...]:
    """Annotate context items with latest matching admission verdicts."""

    verdicts = _latest_context_admission_verdicts(admission_dir=admission_dir)

    return tuple(
        context_item_with_admission_verdict(
            item=item,
            verdict=verdicts.get((item.item_id, item.item_type)),
        )
        for item in items
    )


def filter_items_by_admission_requirement(
    items: tuple[ContextPackItem, ...],
) -> tuple[tuple[ContextPackItem, ...], tuple[ContextPackExclusion, ...]]:
    """Keep only items explicitly admitted by an admission verdict."""

    selected: list[ContextPackItem] = []
    exclusions: list[ContextPackExclusion] = []

    for item in items:
        if item.admission_decision in {"admit", "admit_with_warning"}:
            selected.append(item)
            continue

        if item.admission_decision is None:
            note = "No admission verdict; require_admission is enabled."
        else:
            note = (
                f"Admission decision {item.admission_decision!r}; "
                "require_admission is enabled."
            )

        exclusions.append(
            ContextPackExclusion(
                item_id=item.item_id,
                reason="policy",
                note=note,
            )
        )

    if not selected and items:
        raise ContextPackError("No context items passed the admission requirement.")

    return tuple(selected), tuple(exclusions)


def admission_summary_for_manifest(
    items: tuple[ContextPackItem, ...],
    exclusions: tuple[ContextPackExclusion, ...] = (),
) -> dict[str, int]:
    """Return manifest-level admission telemetry counts."""

    summary = {
        "admit": 0,
        "admit_with_warning": 0,
        "excluded_by_policy": 0,
    }

    for item in items:
        if item.admission_decision == "admit":
            summary["admit"] += 1
        elif item.admission_decision == "admit_with_warning":
            summary["admit_with_warning"] += 1

    for exclusion in exclusions:
        if exclusion.reason == "policy":
            summary["excluded_by_policy"] += 1

    return summary


def context_item_from_l1_summary(
    summary: EpisodeL1Summary,
    path: Path,
    relevance_score: float = 0.92,
    token_estimate: int | None = None,
) -> ContextPackItem:
    """Create a context-pack item from one EpisodeL1Summary JSON artifact."""

    if token_estimate is None:
        token_estimate = estimate_tokens_for_path(path)

    reason = _shorten(
        f"Episode L1 context seed: {summary.episode_id} "
        f"({summary.freshness_state})"
    )

    return ContextPackItem(
        item_type="episode_l1",
        item_id=summary.l1_id,
        reason=reason,
        relevance_score=relevance_score,
        token_estimate=token_estimate,
        source_path=str(path),
    )


def discover_latest_l1_summary_item(
    l1_dir: Path = Path("docs/memory/l1"),
    scope: str | None = None,
) -> ContextPackItem | None:
    """Return the newest valid EpisodeL1Summary context item, optionally by scope."""

    if not l1_dir.is_dir():
        return None

    candidates: list[tuple[str, str, Path, EpisodeL1Summary]] = []

    for path in sorted(l1_dir.glob("*.json")):
        try:
            summary = EpisodeL1Summary.read_json(path)
        except (InteractionLogError, OSError, ValueError):
            continue

        if scope is not None and summary.scope != scope:
            continue

        candidates.append((summary.created_at, summary.l1_id, path, summary))

    if not candidates:
        return None

    _created_at, _l1_id, path, summary = max(candidates)

    return context_item_from_l1_summary(summary=summary, path=path)


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
    l1_dir: Path = Path("docs/memory/l1"),
    admission_dir: Path = Path("docs/memory/admissions"),
    l1_scope: str | None = None,
    require_admission: bool = False,
    task_label: str | None = None,
    full_prompt_hash: str | None = None,
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

    latest_l1_item = discover_latest_l1_summary_item(l1_dir=l1_dir, scope=l1_scope)
    if latest_l1_item is not None:
        candidate_items = (latest_l1_item, *candidate_items)

    candidate_items = annotate_items_with_admission_verdicts(
        items=candidate_items,
        admission_dir=admission_dir,
    )

    admission_exclusions: tuple[ContextPackExclusion, ...] = ()

    if require_admission:
        candidate_items, admission_exclusions = filter_items_by_admission_requirement(
            items=candidate_items,
        )

    selected_items, budget_exclusions = select_items_with_budget(
        items=candidate_items,
        token_budget=token_budget,
    )

    exclusions = (*admission_exclusions, *budget_exclusions)

    return ContextPackManifest(
        task=task,
        assembly_policy="latest_context",
        items=selected_items,
        token_budget=token_budget,
        exclusions=exclusions,
        model_target=model_target,
        pipeline_run_id=pipeline_run_id,
        task_label=task_label,
        full_prompt_hash=full_prompt_hash,
        admission_summary=admission_summary_for_manifest(
            items=selected_items,
            exclusions=exclusions,
        ),
    )
