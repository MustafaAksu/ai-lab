from __future__ import annotations

import json
from pathlib import Path

from ai_lab.documentation.context_pack_builder import (
    estimate_tokens_for_l0_summary_record,
)
from ai_lab.documentation.l0_summary import (
    L0SummaryError,
    l0_summary_record_diagnostics,
    validate_l0_summary_record,
)


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _chunk_id(record: dict[str, object]) -> str | None:
    chunk_reference = record.get("chunk_reference")
    if not isinstance(chunk_reference, dict):
        return None

    chunk_id = chunk_reference.get("chunk_id")
    if not isinstance(chunk_id, str) or not chunk_id:
        return None

    return chunk_id


def _citation(record: dict[str, object]) -> str | None:
    chunk_reference = record.get("chunk_reference")
    if not isinstance(chunk_reference, dict):
        return None

    citation = chunk_reference.get("citation")
    if isinstance(citation, str) and citation:
        return citation

    return None


def _dedupe_preserving_order(values: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    deduped: list[str] = []

    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)

    return tuple(deduped)


def context_item_ids_from_manifest_record(
    manifest_record: dict[str, object],
) -> tuple[str, ...]:
    """Extract selected context item IDs from a context-pack manifest record."""

    items = manifest_record.get("items")
    if not isinstance(items, list):
        return ()

    item_ids: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue

        item_id = item.get("item_id")
        if isinstance(item_id, str) and item_id:
            item_ids.append(item_id)

    return _dedupe_preserving_order(tuple(item_ids))


def context_item_ids_from_manifest_path(
    context_manifest_path: Path,
) -> tuple[tuple[str, ...], dict[str, object]]:
    """Read context item IDs from a saved context-pack manifest non-fatally."""

    details: dict[str, object] = {
        "context_manifest_path": str(context_manifest_path),
    }

    if not context_manifest_path.exists():
        details["context_manifest_status"] = "missing"
        details["context_manifest_item_count"] = 0
        return (), details

    if not context_manifest_path.is_file():
        details["context_manifest_status"] = "not_file"
        details["context_manifest_item_count"] = 0
        return (), details

    try:
        raw = _read_json(context_manifest_path)
    except Exception:
        details["context_manifest_status"] = "invalid_json"
        details["context_manifest_item_count"] = 0
        return (), details

    if not isinstance(raw, dict):
        details["context_manifest_status"] = "not_object"
        details["context_manifest_item_count"] = 0
        return (), details

    if "items" not in raw or not isinstance(raw.get("items"), list):
        details["context_manifest_status"] = "missing_items"
        details["context_manifest_item_count"] = 0
        return (), details

    context_item_ids = context_item_ids_from_manifest_record(raw)
    details["context_manifest_status"] = "ok"
    details["context_manifest_item_count"] = len(context_item_ids)
    return context_item_ids, details


def l0_candidate_diagnostics(
    l0_store: Path = Path("docs/memory/l0"),
    context_item_ids: tuple[str, ...] = (),
) -> dict[str, object]:
    """Report possible L0 candidate sources without changing context selection."""

    context_ids = set(context_item_ids)

    result: dict[str, object] = {
        "schema_version": "v1",
        "diagnostic_type": "l0_candidate_sources",
        "selection_effect": "none",
        "candidate_policy": "valid_l0_summary_records",
        "l0_store": str(l0_store),
        "context_item_ids": sorted(context_ids),
        "candidates": [],
        "dropped": [],
    }

    candidates: list[dict[str, object]] = []
    dropped: list[dict[str, object]] = []

    if not l0_store.exists():
        result["store_status"] = "missing"
        return result

    if not l0_store.is_dir():
        result["store_status"] = "not_directory"
        dropped.append(
            {
                "path": str(l0_store),
                "dropped_reason": "store_not_directory",
            }
        )
        return result

    result["store_status"] = "ok"

    for path in sorted(l0_store.glob("*.json")):
        try:
            raw = _read_json(path)
        except Exception:
            dropped.append(
                {
                    "path": str(path),
                    "dropped_reason": "invalid_json",
                }
            )
            continue

        if not isinstance(raw, dict):
            dropped.append(
                {
                    "path": str(path),
                    "dropped_reason": "not_object",
                }
            )
            continue

        try:
            validate_l0_summary_record(raw)
        except L0SummaryError:
            diagnostics = l0_summary_record_diagnostics(
                raw,
                source="l0_candidate_diagnostic",
                record_id=path.stem,
            )
            dropped.append(
                {
                    "path": str(path),
                    "cid": _chunk_id(raw) or path.stem,
                    "dropped_reason": "invalid_record",
                    "diagnostics": diagnostics["diagnostics"],
                }
            )
            continue

        cid = _chunk_id(raw)
        if cid is None:
            dropped.append(
                {
                    "path": str(path),
                    "cid": path.stem,
                    "dropped_reason": "missing_chunk_id",
                }
            )
            continue

        item: dict[str, object] = {
            "cid": cid,
            "path": str(path),
            "token_cost": estimate_tokens_for_l0_summary_record(raw),
            "candidate_reason": "valid_l0_summary_record",
            "selection_effect": "none",
        }

        if context_ids:
            item["context_match"] = cid in context_ids

        citation = _citation(raw)
        if citation is not None:
            item["citation"] = citation

        candidates.append(item)

    result["candidates"] = candidates
    result["dropped"] = dropped
    return result


def l0_candidate_diagnostics_from_context_manifest(
    l0_store: Path = Path("docs/memory/l0"),
    context_manifest_path: Path = Path("docs/context/latest_manifest.json"),
) -> dict[str, object]:
    """Run read-only L0 diagnostics against item IDs from a saved manifest."""

    context_item_ids, details = context_item_ids_from_manifest_path(
        context_manifest_path
    )

    result = l0_candidate_diagnostics(
        l0_store=l0_store,
        context_item_ids=context_item_ids,
    )
    result.update(details)
    return result
