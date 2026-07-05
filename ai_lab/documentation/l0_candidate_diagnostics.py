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
