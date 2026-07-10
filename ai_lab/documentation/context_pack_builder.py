from __future__ import annotations

from collections.abc import Iterable
import json
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
from ai_lab.documentation.graph_neighborhood import graph_neighborhood_advisor
from ai_lab.documentation.interaction_log import EpisodeL1Summary, InteractionLogError
from ai_lab.documentation.l0_summary import L0SummaryError, validate_l0_summary_record


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



def admission_policy_for_manifest(
    require_admission: bool,
    max_warning_admissions: int | None,
) -> dict[str, object]:
    """Return manifest-level admission policy settings."""

    policy: dict[str, object] = {
        "require_admission": require_admission,
    }

    if max_warning_admissions is not None:
        policy["max_warning_admissions"] = max_warning_admissions

    return policy


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


def cap_admit_with_warning_items(
    items: tuple[ContextPackItem, ...],
    max_warning_admissions: int | None,
) -> tuple[tuple[ContextPackItem, ...], tuple[ContextPackExclusion, ...]]:
    """Cap admit_with_warning items without changing admit items."""

    if max_warning_admissions is None:
        return items, ()

    if max_warning_admissions < 0:
        raise ContextPackError("max_warning_admissions must be >= 0.")

    selected: list[ContextPackItem] = []
    exclusions: list[ContextPackExclusion] = []
    warning_count = 0

    for item in items:
        if item.admission_decision != "admit_with_warning":
            selected.append(item)
            continue

        if warning_count < max_warning_admissions:
            selected.append(item)
            warning_count += 1
            continue

        exclusions.append(
            ContextPackExclusion(
                item_id=item.item_id,
                reason="policy",
                note=f"admit_with_warning cap {max_warning_admissions} exceeded.",
            )
        )

    if not selected and items:
        raise ContextPackError("No context items passed the warning admission cap.")

    return tuple(selected), tuple(exclusions)


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



def estimate_tokens_for_l0_summary_record(record: dict[str, object]) -> int:
    """Estimate prompt cost for compact rendered L0 summary content."""

    chunk_reference = record.get("chunk_reference", {})
    if not isinstance(chunk_reference, dict):
        chunk_reference = {}

    keyphrases = record.get("keyphrases", ())
    if not isinstance(keyphrases, list):
        keyphrases = []

    text = "\n".join(
        (
            f"Chunk ID: {chunk_reference.get('chunk_id', '')}",
            f"Citation: {record.get('citation', '')}",
            f"Summary: {record.get('l0_summary', '')}",
            f"Keyphrases: {', '.join(str(item) for item in keyphrases)}",
        )
    )
    return estimate_tokens_for_text(text)


def context_item_from_l0_summary_record(
    record: dict[str, object],
    path: Path,
    relevance_score: float = 0.96,
    token_estimate: int | None = None,
) -> ContextPackItem:
    """Create a context-pack item from one validated L0 summary JSON artifact."""

    chunk_reference = record["chunk_reference"]
    if not isinstance(chunk_reference, dict):
        raise ContextPackError("L0 chunk_reference must be an object.")

    chunk_id = str(chunk_reference["chunk_id"])

    if token_estimate is None:
        token_estimate = estimate_tokens_for_l0_summary_record(record)

    return ContextPackItem(
        item_type="l0_summary",
        item_id=chunk_id,
        reason=_shorten(f"Explicit L0 summary context seed: {chunk_id}"),
        relevance_score=relevance_score,
        token_estimate=token_estimate,
        source_path=str(path),
        citation=str(record["citation"]),
    )


def explicit_l0_summary_items(
    include_l0: tuple[str, ...] = (),
    l0_store: Path = Path("docs/memory/l0"),
) -> tuple[tuple[ContextPackItem, ...], tuple[ContextPackExclusion, ...]]:
    """Return valid explicit L0 context items plus non-fatal exclusions."""

    items: list[ContextPackItem] = []
    exclusions: list[ContextPackExclusion] = []

    for chunk_id in include_l0:
        path = l0_store / f"{chunk_id}.json"

        if not path.is_file():
            exclusions.append(
                ContextPackExclusion(
                    item_id=chunk_id,
                    reason="policy",
                    note="Requested explicit L0 summary was not found.",
                )
            )
            continue

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            exclusions.append(
                ContextPackExclusion(
                    item_id=chunk_id,
                    reason="policy",
                    note="Requested explicit L0 summary could not be read as JSON.",
                )
            )
            continue

        if not isinstance(data, dict):
            exclusions.append(
                ContextPackExclusion(
                    item_id=chunk_id,
                    reason="policy",
                    note="Requested explicit L0 summary was not a JSON object.",
                )
            )
            continue

        try:
            validate_l0_summary_record(data)
        except L0SummaryError:
            exclusions.append(
                ContextPackExclusion(
                    item_id=chunk_id,
                    reason="policy",
                    note="Requested explicit L0 summary failed record validation.",
                )
            )
            continue

        record_chunk_reference = data["chunk_reference"]
        if not isinstance(record_chunk_reference, dict):
            exclusions.append(
                ContextPackExclusion(
                    item_id=chunk_id,
                    reason="policy",
                    note="Requested explicit L0 summary had invalid chunk reference.",
                )
            )
            continue

        record_chunk_id = str(record_chunk_reference["chunk_id"])
        if record_chunk_id != chunk_id:
            exclusions.append(
                ContextPackExclusion(
                    item_id=chunk_id,
                    reason="policy",
                    note="Requested explicit L0 summary chunk_id did not match file name.",
                )
            )
            continue

        items.append(context_item_from_l0_summary_record(record=data, path=path))

    return tuple(items), tuple(exclusions)


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


def graph_neighborhood_context_items(
    *,
    target_id: str,
    records: Iterable[ArtifactRecord],
    edge_records: Iterable[dict[str, object]] = (),
    future_edge_seed_records: Iterable[dict[str, str]] = (),
    max_depth: int = 2,
    token_budget: int | None = None,
) -> tuple[tuple[ContextPackItem, ...], dict[str, object]]:
    """Return opt-in graph-neighborhood context items plus diagnostics.

    This helper is default-off at the manifest builder boundary. It converts the
    read-only graph-neighborhood advisor output into ordinary context-pack
    candidates without mutating provider prompts, persisted graph artifacts,
    retrieval, embeddings, indexes, memory stores, or runtime manifests.
    """

    record_tuple = tuple(records)
    record_index = {record.artifact_id: record for record in record_tuple}

    report = graph_neighborhood_advisor(
        target_id=target_id,
        artifact_records=record_tuple,
        edge_records=edge_records,
        future_edge_seed_records=future_edge_seed_records,
        max_depth=max_depth,
        token_budget=token_budget,
    )

    items: list[ContextPackItem] = []

    for candidate in report.candidates:
        if candidate.decision != "included":
            continue

        record = record_index.get(candidate.artifact_id)
        if record is None:
            continue

        distance_penalty = max(candidate.distance - 1, 0) * 0.08
        relevance_score = max(0.5, 0.88 - distance_penalty)

        items.append(
            ContextPackItem(
                item_type=item_type_for_record(record),
                item_id=record.artifact_id,
                reason=_shorten(
                    "Graph-neighborhood context candidate "
                    f"distance {candidate.distance}: {record.title}"
                ),
                relevance_score=relevance_score,
                token_estimate=candidate.token_estimate,
                source_path=str(record.path),
            )
        )

    diagnostics = {
        "enabled": True,
        "selection_effect": "opt_in_context_candidate",
        "target_id": report.target_id,
        "max_depth": report.max_depth,
        "token_budget": report.token_budget,
        "candidate_count": len(report.candidates),
        "included_count": len(items),
        "selected_artifact_ids": list(report.selected_artifact_ids),
        "excluded_artifact_ids": list(report.excluded_artifact_ids),
        "selected_token_estimate": report.selected_token_estimate,
        "guardrails": {
            "default_off": True,
            "provider_prompt_changed": False,
            "persisted_graph_writes": False,
            "retrieval_changed": False,
            "embeddings_changed": False,
            "runtime_manifest_changed": False,
        },
    }

    return tuple(items), diagnostics


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


def _dedupe_l0_chunk_ids(chunk_ids: tuple[str, ...]) -> tuple[str, ...]:
    """Return chunk IDs in first-seen deterministic order without duplicates."""
    seen: set[str] = set()
    deduped: list[str] = []

    for chunk_id in chunk_ids:
        if chunk_id in seen:
            continue
        seen.add(chunk_id)
        deduped.append(chunk_id)

    return tuple(deduped)


def automatic_l0_discovery_include_l0_args(
    *,
    selected_items: tuple[ContextPackItem, ...],
    l0_store: Path = Path("docs/memory/l0"),
    max_suggestions: int | None = None,
    run_id: str | None = None,
) -> tuple[str, ...]:
    """Return deterministic advisor-suggested include_l0 args for opt-in runtime use."""

    advisor = l0_discovery_advisor_diagnostics_for_manifest(
        selected_items=selected_items,
        l0_store=l0_store,
        max_suggestions=max_suggestions,
        run_id=run_id,
    )

    selected_item_ids = {item.item_id for item in selected_items}
    include_l0_args: list[str] = []

    for suggestion in advisor.get("suggestions", ()):
        if not isinstance(suggestion, dict):
            continue

        chunk_id = suggestion.get("suggested_include_l0_arg")
        if not isinstance(chunk_id, str) or not chunk_id:
            continue

        if chunk_id in selected_item_ids:
            continue

        include_l0_args.append(chunk_id)

    return _dedupe_l0_chunk_ids(tuple(include_l0_args))


def l0_discovery_advisor_diagnostics_for_manifest(
    *,
    selected_items: tuple[ContextPackItem, ...],
    l0_store: Path = Path("docs/memory/l0"),
    max_suggestions: int | None = None,
    run_id: str | None = None,
) -> dict[str, object]:
    """Build read-only advisor diagnostics for an already-selected manifest.

    This helper is intentionally diagnostic-only. It derives candidate input from
    existing L0 candidate diagnostics and never mutates selected context items,
    provider prompts, indexes, embeddings, memory stores, or adapters.
    """

    from ai_lab.documentation.l0_candidate_diagnostics import l0_candidate_diagnostics
    from ai_lab.documentation.l0_discovery_advisor import (
        build_l0_discovery_advisor_record,
        validate_l0_discovery_advisor_record,
    )

    selected_context_item_ids = tuple(item.item_id for item in selected_items)
    candidate_diagnostics = l0_candidate_diagnostics(
        l0_store=l0_store,
        context_item_ids=selected_context_item_ids,
    )

    record = build_l0_discovery_advisor_record(
        selected_context_item_ids=selected_context_item_ids,
        candidate_diagnostics_records=[candidate_diagnostics],
        max_suggestions=max_suggestions,
        run_id=run_id,
    )
    validate_l0_discovery_advisor_record(record)
    return record


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
    max_warning_admissions: int | None = None,
    include_l0: tuple[str, ...] = (),
    l0_store: Path = Path("docs/memory/l0"),
    include_l0_discovery_advisor_diagnostics: bool = False,
    l0_discovery_advisor_max_suggestions: int | None = None,
    auto_include_l0_discovery: bool = False,
    auto_include_l0_discovery_max_items: int | None = None,
    include_graph_neighborhood_candidates: bool = False,
    graph_neighborhood_target_id: str | None = None,
    graph_neighborhood_edge_records: Iterable[dict[str, object]] = (),
    graph_neighborhood_future_edge_seed_records: Iterable[dict[str, str]] = (),
    graph_neighborhood_max_depth: int = 2,
    graph_neighborhood_token_budget: int | None = None,
) -> ContextPackManifest:
    """
    Build a manifest from the latest useful context records.

    Selection is delegated to artifact_history.latest_records_by_context_level.
    This keeps context-pack construction aligned with the existing latest-context
    seed view.
    """
    record_tuple = tuple(records)
    latest_by_level = latest_records_by_context_level(record_tuple)

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

    explicit_l0_items, explicit_l0_exclusions = explicit_l0_summary_items(
        include_l0=include_l0,
        l0_store=l0_store,
    )

    latest_l1_item = discover_latest_l1_summary_item(l1_dir=l1_dir, scope=l1_scope)
    if latest_l1_item is not None:
        candidate_items = (latest_l1_item, *candidate_items)

    graph_neighborhood_diagnostics: dict[str, object] | None = None

    if include_graph_neighborhood_candidates:
        if graph_neighborhood_target_id is None:
            raise ContextPackError(
                "graph_neighborhood_target_id is required when "
                "include_graph_neighborhood_candidates is enabled."
            )

        graph_items, graph_neighborhood_diagnostics = graph_neighborhood_context_items(
            target_id=graph_neighborhood_target_id,
            records=record_tuple,
            edge_records=graph_neighborhood_edge_records,
            future_edge_seed_records=graph_neighborhood_future_edge_seed_records,
            max_depth=graph_neighborhood_max_depth,
            token_budget=graph_neighborhood_token_budget,
        )

        existing_item_ids = {item.item_id for item in candidate_items}
        deduped_graph_items = tuple(
            item for item in graph_items if item.item_id not in existing_item_ids
        )

        if deduped_graph_items:
            candidate_items = (*deduped_graph_items, *candidate_items)

    candidate_items = (*explicit_l0_items, *candidate_items)

    candidate_items = annotate_items_with_admission_verdicts(
        items=candidate_items,
        admission_dir=admission_dir,
    )

    admission_exclusions: tuple[ContextPackExclusion, ...] = ()

    if require_admission:
        candidate_items, admission_exclusions = filter_items_by_admission_requirement(
            items=candidate_items,
        )

    warning_cap_exclusions: tuple[ContextPackExclusion, ...] = ()

    if max_warning_admissions is not None:
        candidate_items, warning_cap_exclusions = cap_admit_with_warning_items(
            items=candidate_items,
            max_warning_admissions=max_warning_admissions,
        )

    selected_items, budget_exclusions = select_items_with_budget(
        items=candidate_items,
        token_budget=token_budget,
    )

    auto_l0_exclusions: tuple[ContextPackExclusion, ...] = ()

    if auto_include_l0_discovery:
        auto_include_l0 = automatic_l0_discovery_include_l0_args(
            selected_items=selected_items,
            l0_store=l0_store,
            max_suggestions=auto_include_l0_discovery_max_items,
            run_id="context_pack_manifest_auto_include",
        )
        auto_l0_items, auto_l0_exclusions = explicit_l0_summary_items(
            include_l0=auto_include_l0,
            l0_store=l0_store,
        )

        if auto_l0_items:
            existing_item_ids = {item.item_id for item in candidate_items}
            deduped_auto_l0_items = tuple(
                item for item in auto_l0_items if item.item_id not in existing_item_ids
            )

            if deduped_auto_l0_items:
                candidate_items = (*deduped_auto_l0_items, *candidate_items)
                candidate_items = annotate_items_with_admission_verdicts(
                    items=candidate_items,
                    admission_dir=admission_dir,
                )

                if require_admission:
                    candidate_items, admission_exclusions = (
                        filter_items_by_admission_requirement(items=candidate_items)
                    )

                if max_warning_admissions is not None:
                    candidate_items, warning_cap_exclusions = (
                        cap_admit_with_warning_items(
                            items=candidate_items,
                            max_warning_admissions=max_warning_admissions,
                        )
                    )

                selected_items, budget_exclusions = select_items_with_budget(
                    items=candidate_items,
                    token_budget=token_budget,
                )

    exclusions = (
        *explicit_l0_exclusions,
        *auto_l0_exclusions,
        *admission_exclusions,
        *warning_cap_exclusions,
        *budget_exclusions,
    )

    diagnostics: dict[str, object] = {}
    if graph_neighborhood_diagnostics is not None:
        diagnostics["graph_neighborhood"] = graph_neighborhood_diagnostics

    if include_l0_discovery_advisor_diagnostics:
        diagnostics["l0_discovery_advisor"] = l0_discovery_advisor_diagnostics_for_manifest(
            selected_items=selected_items,
            l0_store=l0_store,
            max_suggestions=l0_discovery_advisor_max_suggestions,
            run_id="context_pack_manifest",
        )

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
        admission_policy=admission_policy_for_manifest(
            require_admission=require_admission,
            max_warning_admissions=max_warning_admissions,
        ),
        diagnostics=diagnostics or None,
    )
