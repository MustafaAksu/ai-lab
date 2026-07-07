from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from ai_lab.documentation.l0_discovery_advisor import (
    validate_l0_discovery_advisor_record,
)


EVALUATION_SCHEMA_VERSION = "v1"
EVALUATOR_ID = "l0_discovery_advisor_evaluation.v1"
SELECTION_EFFECT = "none"


class L0DiscoveryAdvisorEvaluationError(ValueError):
    """Raised when an L0 discovery advisor evaluation record is malformed."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise L0DiscoveryAdvisorEvaluationError(f"{field_name} must be an object")
    return value


def _as_sequence(value: Any, field_name: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise L0DiscoveryAdvisorEvaluationError(f"{field_name} must be a sequence")
    return value


def _nonempty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise L0DiscoveryAdvisorEvaluationError(f"{field_name} must be a non-empty string")
    return value


def _nonnegative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise L0DiscoveryAdvisorEvaluationError(
            f"{field_name} must be a non-negative integer"
        )
    return value


def _manifest_mapping(record: Mapping[str, Any]) -> tuple[Mapping[str, Any], str]:
    manifest = record.get("manifest")
    if isinstance(manifest, Mapping):
        return manifest, "wrapped_manifest"

    return record, "context_pack_manifest"


def _selected_item_ids(manifest: Mapping[str, Any]) -> tuple[str, ...]:
    items = manifest.get("items")
    if not isinstance(items, list):
        return ()

    item_ids: list[str] = []
    for item in items:
        if not isinstance(item, Mapping):
            continue

        item_id = item.get("item_id")
        if isinstance(item_id, str) and item_id:
            item_ids.append(item_id)

    return tuple(item_ids)


def _empty_manifest_evaluation(
    *,
    source_path: str | None,
    manifest_status: str,
    advisor_status: str,
    manifest_format: str = "unknown",
    selected_item_ids: tuple[str, ...] = (),
    error: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_path": source_path,
        "manifest_status": manifest_status,
        "manifest_format": manifest_format,
        "advisor_status": advisor_status,
        "selected_item_count": len(selected_item_ids),
        "selected_item_ids": list(selected_item_ids),
        "suggestion_count": 0,
        "suggested_chunk_ids": [],
        "unique_suggested_chunk_ids": [],
        "duplicate_suggestion_count": 0,
        "already_selected_suggestion_count": 0,
        "already_selected_suggestion_ids": [],
        "selection_effect": SELECTION_EFFECT,
    }
    if error:
        result["error"] = error
    return result


def evaluate_manifest_record(
    manifest_record: Mapping[str, Any],
    *,
    source_path: str | None = None,
) -> dict[str, Any]:
    """Evaluate advisor diagnostics in one manifest without changing selection."""

    manifest, manifest_format = _manifest_mapping(manifest_record)
    selected_item_ids = _selected_item_ids(manifest)
    selected_set = set(selected_item_ids)

    diagnostics = manifest.get("diagnostics")
    if not isinstance(diagnostics, Mapping):
        return _empty_manifest_evaluation(
            source_path=source_path,
            manifest_status="ok",
            manifest_format=manifest_format,
            advisor_status="missing_diagnostics",
            selected_item_ids=selected_item_ids,
        )

    advisor = diagnostics.get("l0_discovery_advisor")
    if not isinstance(advisor, Mapping):
        return _empty_manifest_evaluation(
            source_path=source_path,
            manifest_status="ok",
            manifest_format=manifest_format,
            advisor_status="missing_l0_discovery_advisor",
            selected_item_ids=selected_item_ids,
        )

    try:
        validate_l0_discovery_advisor_record(advisor)
    except Exception as exc:
        return _empty_manifest_evaluation(
            source_path=source_path,
            manifest_status="ok",
            manifest_format=manifest_format,
            advisor_status="invalid_l0_discovery_advisor",
            selected_item_ids=selected_item_ids,
            error=str(exc),
        )

    suggestions = advisor.get("suggestions")
    if not isinstance(suggestions, list):
        suggestions = []

    suggested_chunk_ids: list[str] = []
    for suggestion in suggestions:
        if not isinstance(suggestion, Mapping):
            continue

        chunk_id = suggestion.get("chunk_id")
        if isinstance(chunk_id, str) and chunk_id:
            suggested_chunk_ids.append(chunk_id)

    unique_suggested_chunk_ids = tuple(sorted(set(suggested_chunk_ids)))
    duplicate_suggestion_count = len(suggested_chunk_ids) - len(unique_suggested_chunk_ids)
    already_selected = tuple(
        chunk_id for chunk_id in unique_suggested_chunk_ids if chunk_id in selected_set
    )

    guardrails = advisor.get("guardrails")
    if not isinstance(guardrails, Mapping):
        guardrails = {}

    return {
        "source_path": source_path,
        "manifest_status": "ok",
        "manifest_format": manifest_format,
        "advisor_status": "ok",
        "selected_item_count": len(selected_item_ids),
        "selected_item_ids": list(selected_item_ids),
        "suggestion_count": len(suggested_chunk_ids),
        "suggested_chunk_ids": suggested_chunk_ids,
        "unique_suggested_chunk_ids": list(unique_suggested_chunk_ids),
        "duplicate_suggestion_count": duplicate_suggestion_count,
        "already_selected_suggestion_count": len(already_selected),
        "already_selected_suggestion_ids": list(already_selected),
        "selection_effect": SELECTION_EFFECT,
        "advisor_guardrails": {
            "automatic_include_l0": guardrails.get("automatic_include_l0"),
            "context_items_mutated": guardrails.get("context_items_mutated"),
            "provider_prompts_changed": guardrails.get("provider_prompts_changed"),
            "writes_performed": guardrails.get("writes_performed"),
            "index_mutations": guardrails.get("index_mutations"),
            "embedding_creations": guardrails.get("embedding_creations"),
            "token_budget_enforced": guardrails.get("token_budget_enforced"),
            "token_budget_telemetry_emitted": guardrails.get(
                "token_budget_telemetry_emitted"
            ),
            "reranker": guardrails.get("reranker"),
        },
    }


def evaluate_manifest_path(path: Path) -> dict[str, Any]:
    """Read and evaluate one saved manifest non-fatally."""

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return _empty_manifest_evaluation(
            source_path=str(path),
            manifest_status="invalid_json",
            advisor_status="unavailable",
            error=str(exc),
        )

    if not isinstance(raw, Mapping):
        return _empty_manifest_evaluation(
            source_path=str(path),
            manifest_status="not_object",
            advisor_status="unavailable",
        )

    return evaluate_manifest_record(raw, source_path=str(path))


def build_l0_discovery_advisor_evaluation_record(
    *,
    manifest_evaluations: Sequence[Mapping[str, Any]],
    manifest_paths: Sequence[str] = (),
    run_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build a diagnostic-only aggregate evaluation record."""

    evaluations = [dict(item) for item in manifest_evaluations]
    unique_suggested: set[str] = set()

    manifests_with_advisor = 0
    missing_advisor = 0
    invalid_advisor = 0
    total_suggestions = 0
    duplicate_suggestions = 0
    already_selected = 0
    manifests_without_suggestions = 0

    for item in evaluations:
        advisor_status = item.get("advisor_status")
        if advisor_status == "ok":
            manifests_with_advisor += 1
        elif advisor_status == "invalid_l0_discovery_advisor":
            invalid_advisor += 1
        else:
            missing_advisor += 1

        suggestion_count = item.get("suggestion_count", 0)
        if isinstance(suggestion_count, int) and suggestion_count >= 0:
            total_suggestions += suggestion_count
            if advisor_status == "ok" and suggestion_count == 0:
                manifests_without_suggestions += 1

        duplicate_count = item.get("duplicate_suggestion_count", 0)
        if isinstance(duplicate_count, int) and duplicate_count >= 0:
            duplicate_suggestions += duplicate_count

        already_selected_count = item.get("already_selected_suggestion_count", 0)
        if isinstance(already_selected_count, int) and already_selected_count >= 0:
            already_selected += already_selected_count

        for chunk_id in item.get("unique_suggested_chunk_ids", []):
            if isinstance(chunk_id, str) and chunk_id:
                unique_suggested.add(chunk_id)

    record = {
        "schema_version": EVALUATION_SCHEMA_VERSION,
        "evaluator_id": EVALUATOR_ID,
        "evaluation_type": "manifest_connected_l0_discovery_advisor",
        "run_id": run_id or EVALUATOR_ID,
        "created_at": created_at or _now_iso(),
        "selection_effect": SELECTION_EFFECT,
        "contract": {
            "diagnostic_evaluation_only": True,
            "automatic_include_l0": False,
            "mutates_context_manifest_items": False,
            "changes_provider_prompts": False,
            "changes_latest_context_prompt_path": False,
            "live_retrieval": False,
            "external_embedding_api_calls": False,
            "embedding_creation": False,
            "index_mutation": False,
            "memory_store_mutation": False,
            "token_budget_enforcement": False,
            "token_budget_telemetry": False,
            "reranker": "none",
            "adapter_behavior": False,
        },
        "inputs": {
            "manifest_paths": list(manifest_paths),
            "manifest_count": len(evaluations),
        },
        "aggregate": {
            "manifests_seen": len(evaluations),
            "manifests_with_advisor": manifests_with_advisor,
            "manifests_missing_advisor": missing_advisor,
            "manifests_invalid_advisor": invalid_advisor,
            "manifests_without_suggestions": manifests_without_suggestions,
            "total_suggestions": total_suggestions,
            "unique_suggested_chunk_count": len(unique_suggested),
            "unique_suggested_chunk_ids": sorted(unique_suggested),
            "duplicate_suggestion_count": duplicate_suggestions,
            "already_selected_suggestion_count": already_selected,
            "selection_effect": SELECTION_EFFECT,
        },
        "manifest_evaluations": evaluations,
        "guardrails": {
            "side_effects_blocked": True,
            "writes_performed": 0,
            "index_mutations": 0,
            "embedding_creations": 0,
            "context_items_mutated": 0,
            "provider_prompts_changed": 0,
            "latest_context_prompt_path_changed": 0,
            "automatic_include_l0": False,
            "memory_store_mutations": 0,
            "token_budget_enforced": False,
            "token_budget_telemetry_emitted": False,
            "reranker": "none",
            "adapter_behavior": False,
        },
    }

    validate_l0_discovery_advisor_evaluation_record(record)
    return record


def evaluate_l0_discovery_advisor_manifest_paths(
    manifest_paths: Sequence[Path],
    *,
    run_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    evaluations = [evaluate_manifest_path(path) for path in manifest_paths]
    return build_l0_discovery_advisor_evaluation_record(
        manifest_evaluations=evaluations,
        manifest_paths=[str(path) for path in manifest_paths],
        run_id=run_id,
        created_at=created_at,
    )


def validate_l0_discovery_advisor_evaluation_record(record: Mapping[str, Any]) -> None:
    """Validate a diagnostic-only advisor evaluation record."""

    record = _as_mapping(record, "record")

    if record.get("schema_version") != EVALUATION_SCHEMA_VERSION:
        raise L0DiscoveryAdvisorEvaluationError("schema_version must be v1")
    if record.get("evaluator_id") != EVALUATOR_ID:
        raise L0DiscoveryAdvisorEvaluationError(f"evaluator_id must be {EVALUATOR_ID}")
    if record.get("evaluation_type") != "manifest_connected_l0_discovery_advisor":
        raise L0DiscoveryAdvisorEvaluationError("evaluation_type is unsupported")
    if record.get("selection_effect") != SELECTION_EFFECT:
        raise L0DiscoveryAdvisorEvaluationError("selection_effect must be none")

    _nonempty_string(record.get("run_id"), "run_id")
    _nonempty_string(record.get("created_at"), "created_at")

    contract = _as_mapping(record.get("contract"), "contract")
    if contract.get("diagnostic_evaluation_only") is not True:
        raise L0DiscoveryAdvisorEvaluationError(
            "contract.diagnostic_evaluation_only must be true"
        )
    for key in (
        "automatic_include_l0",
        "mutates_context_manifest_items",
        "changes_provider_prompts",
        "changes_latest_context_prompt_path",
        "live_retrieval",
        "external_embedding_api_calls",
        "embedding_creation",
        "index_mutation",
        "memory_store_mutation",
        "token_budget_enforcement",
        "token_budget_telemetry",
        "adapter_behavior",
    ):
        if contract.get(key) is not False:
            raise L0DiscoveryAdvisorEvaluationError(f"contract.{key} must be false")
    if contract.get("reranker") != "none":
        raise L0DiscoveryAdvisorEvaluationError("contract.reranker must be none")

    inputs = _as_mapping(record.get("inputs"), "inputs")
    manifest_paths = _as_sequence(inputs.get("manifest_paths"), "inputs.manifest_paths")
    _nonnegative_int(inputs.get("manifest_count"), "inputs.manifest_count")
    for manifest_path in manifest_paths:
        _nonempty_string(manifest_path, "inputs.manifest_path")

    aggregate = _as_mapping(record.get("aggregate"), "aggregate")
    for key in (
        "manifests_seen",
        "manifests_with_advisor",
        "manifests_missing_advisor",
        "manifests_invalid_advisor",
        "manifests_without_suggestions",
        "total_suggestions",
        "unique_suggested_chunk_count",
        "duplicate_suggestion_count",
        "already_selected_suggestion_count",
    ):
        _nonnegative_int(aggregate.get(key), f"aggregate.{key}")
    if aggregate.get("selection_effect") != SELECTION_EFFECT:
        raise L0DiscoveryAdvisorEvaluationError("aggregate.selection_effect must be none")

    unique_ids = _as_sequence(
        aggregate.get("unique_suggested_chunk_ids"),
        "aggregate.unique_suggested_chunk_ids",
    )
    for chunk_id in unique_ids:
        _nonempty_string(chunk_id, "aggregate.unique_suggested_chunk_id")

    evaluations = _as_sequence(
        record.get("manifest_evaluations"),
        "manifest_evaluations",
    )
    for evaluation_value in evaluations:
        evaluation = _as_mapping(evaluation_value, "manifest_evaluation")
        _nonnegative_int(
            evaluation.get("selected_item_count"),
            "manifest_evaluation.selected_item_count",
        )
        _nonnegative_int(
            evaluation.get("suggestion_count"),
            "manifest_evaluation.suggestion_count",
        )
        _nonnegative_int(
            evaluation.get("duplicate_suggestion_count"),
            "manifest_evaluation.duplicate_suggestion_count",
        )
        _nonnegative_int(
            evaluation.get("already_selected_suggestion_count"),
            "manifest_evaluation.already_selected_suggestion_count",
        )
        if evaluation.get("selection_effect") != SELECTION_EFFECT:
            raise L0DiscoveryAdvisorEvaluationError(
                "manifest_evaluation.selection_effect must be none"
            )

    guardrails = _as_mapping(record.get("guardrails"), "guardrails")
    if guardrails.get("side_effects_blocked") is not True:
        raise L0DiscoveryAdvisorEvaluationError(
            "guardrails.side_effects_blocked must be true"
        )
    for key in (
        "writes_performed",
        "index_mutations",
        "embedding_creations",
        "context_items_mutated",
        "provider_prompts_changed",
        "latest_context_prompt_path_changed",
        "memory_store_mutations",
    ):
        if guardrails.get(key) != 0:
            raise L0DiscoveryAdvisorEvaluationError(f"guardrails.{key} must be 0")
    for key in (
        "automatic_include_l0",
        "token_budget_enforced",
        "token_budget_telemetry_emitted",
        "adapter_behavior",
    ):
        if guardrails.get(key) is not False:
            raise L0DiscoveryAdvisorEvaluationError(f"guardrails.{key} must be false")
    if guardrails.get("reranker") != "none":
        raise L0DiscoveryAdvisorEvaluationError("guardrails.reranker must be none")
