"""Read-only L0 discovery advisor.

This module intentionally produces advisory diagnostics only. It does not
retrieve from live indexes, create embeddings, mutate context manifests, alter
provider prompts, or automatically include L0 chunks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ADVISOR_SCHEMA_VERSION = "v1"
ADVISOR_ID = "l0_discovery_advisor.v1"
CANONICAL_SECTION_PATH = "manifest.diagnostics.l0_discovery_advisor"
SELECTION_EFFECT = "none"


class L0DiscoveryAdvisorError(ValueError):
    """Raised when an L0 discovery advisor record is invalid."""


@dataclass
class _SuggestionAccumulator:
    chunk_id: str
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    source_refs: list[dict[str, str]] = field(default_factory=list)

    def add_reason(self, reason: str) -> None:
        if reason and reason not in self.reasons:
            self.reasons.append(reason)

    def add_source_ref(self, source: str, chunk_id: str, source_path: str | None = None) -> None:
        ref = {
            "source": source,
            "source_candidate_id": chunk_id,
        }
        if source_path:
            ref["source_path"] = source_path
        if ref not in self.source_refs:
            self.source_refs.append(ref)


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _as_mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise L0DiscoveryAdvisorError(f"{label} must be an object")
    return value


def _as_sequence(value: object, label: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise L0DiscoveryAdvisorError(f"{label} must be a list")
    return value


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise L0DiscoveryAdvisorError(f"{label} must be a non-empty string")
    return value


def _optional_string(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _number(value: object, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise L0DiscoveryAdvisorError(f"{label} must be a number")
    return float(value)


def _dedupe_strings(values: Sequence[str] | None) -> list[str]:
    out: list[str] = []
    for value in values or []:
        if isinstance(value, str) and value and value not in out:
            out.append(value)
    return out


def _extract_chunk_id(candidate: Mapping[str, Any]) -> str | None:
    for key in ("chunk_id", "cid", "l0_chunk_id", "item_id"):
        value = candidate.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def _extract_score(candidate: Mapping[str, Any]) -> float:
    for key in ("retrieval_score", "suggestion_score", "score", "candidate_score"):
        value = candidate.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)

    total = 0.0
    found = False
    for key in ("bm25_score", "dense_score", "semantic_score", "literal_score"):
        value = candidate.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            total += float(value)
            found = True
    return total if found else 0.0


def _extract_reasons(candidate: Mapping[str, Any], default_reason: str) -> list[str]:
    reasons: list[str] = []

    for key in ("reason", "match_reason", "inclusion_reason", "diagnostic_reason"):
        value = candidate.get(key)
        if isinstance(value, str) and value.strip() and value not in reasons:
            reasons.append(value)

    value = candidate.get("reasons")
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            if isinstance(item, str) and item.strip() and item not in reasons:
                reasons.append(item)

    if not reasons:
        reasons.append(default_reason)
    return reasons


def _candidate_list_from_record(record: Mapping[str, Any], source: str) -> list[Mapping[str, Any]]:
    """Return candidate-like objects from known diagnostic shapes.

    The function is deliberately permissive because it is a read-only bridge
    over diagnostic artifacts, not a production retrieval adapter.
    """

    if isinstance(record.get("candidates"), list):
        return [
            candidate
            for candidate in record["candidates"]
            if isinstance(candidate, Mapping)
        ]

    if source == "l0_retrieval_simulator":
        manifest = record.get("manifest")
        if isinstance(manifest, Mapping):
            diagnostics = manifest.get("diagnostics")
            if isinstance(diagnostics, Mapping):
                simulator = diagnostics.get("l0_retrieval_simulator")
                if isinstance(simulator, Mapping):
                    return _candidate_list_from_record(simulator, source)

    if source == "l0_candidate_diagnostics":
        for key in ("l0_candidates", "diagnostics", "candidate_diagnostics"):
            value = record.get(key)
            if isinstance(value, list):
                return [
                    candidate
                    for candidate in value
                    if isinstance(candidate, Mapping)
                ]

        manifest = record.get("manifest")
        if isinstance(manifest, Mapping):
            diagnostics = manifest.get("diagnostics")
            if isinstance(diagnostics, Mapping):
                for key in ("l0_candidate_diagnostics", "l0_candidates"):
                    value = diagnostics.get(key)
                    if isinstance(value, Mapping):
                        return _candidate_list_from_record(value, source)
                    if isinstance(value, list):
                        return [
                            candidate
                            for candidate in value
                            if isinstance(candidate, Mapping)
                        ]

    return []


def _add_candidates(
    accumulators: dict[str, _SuggestionAccumulator],
    *,
    record: Mapping[str, Any],
    source: str,
    source_path: str | None,
    default_reason: str,
) -> int:
    added = 0
    for candidate in _candidate_list_from_record(record, source):
        if candidate.get("dropped_reason") == "not_found":
            continue

        chunk_id = _extract_chunk_id(candidate)
        if not chunk_id:
            continue

        score = _extract_score(candidate)
        accumulator = accumulators.setdefault(
            chunk_id,
            _SuggestionAccumulator(chunk_id=chunk_id),
        )
        accumulator.score = max(accumulator.score, score)
        accumulator.add_source_ref(source, chunk_id, source_path=source_path)
        for reason in _extract_reasons(candidate, default_reason):
            accumulator.add_reason(reason)

        if chunk_id in _dedupe_strings(candidate.get("selected_context_item_ids")):
            accumulator.add_reason("candidate also appears in selected_context_item_ids")

        added += 1
    return added


def build_l0_discovery_advisor_record(
    *,
    selected_context_item_ids: Sequence[str] | None = None,
    retrieval_simulator_records: Sequence[Mapping[str, Any]] | None = None,
    candidate_diagnostics_records: Sequence[Mapping[str, Any]] | None = None,
    retrieval_simulator_paths: Sequence[str] | None = None,
    candidate_diagnostics_paths: Sequence[str] | None = None,
    max_suggestions: int | None = None,
    run_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build a diagnostic-only L0 discovery advisor record."""

    if max_suggestions is not None and (not isinstance(max_suggestions, int) or max_suggestions < 0):
        raise L0DiscoveryAdvisorError("max_suggestions must be a non-negative integer or None")

    selected_ids = _dedupe_strings(list(selected_context_item_ids or []))
    accumulators: dict[str, _SuggestionAccumulator] = {}

    retrieval_records = list(retrieval_simulator_records or [])
    candidate_records = list(candidate_diagnostics_records or [])
    retrieval_paths = list(retrieval_simulator_paths or [])
    candidate_paths = list(candidate_diagnostics_paths or [])

    source_counts = {
        "l0_retrieval_simulator_records": len(retrieval_records),
        "l0_candidate_diagnostics_records": len(candidate_records),
        "candidate_entries_seen": 0,
    }

    for index, record in enumerate(retrieval_records):
        source_counts["candidate_entries_seen"] += _add_candidates(
            accumulators,
            record=_as_mapping(record, "retrieval_simulator_record"),
            source="l0_retrieval_simulator",
            source_path=retrieval_paths[index] if index < len(retrieval_paths) else None,
            default_reason="suggested by l0_retrieval_simulator diagnostic output",
        )

    for index, record in enumerate(candidate_records):
        source_counts["candidate_entries_seen"] += _add_candidates(
            accumulators,
            record=_as_mapping(record, "candidate_diagnostics_record"),
            source="l0_candidate_diagnostics",
            source_path=candidate_paths[index] if index < len(candidate_paths) else None,
            default_reason="suggested by l0_candidate_diagnostics output",
        )

    suggestions = sorted(
        accumulators.values(),
        key=lambda item: (-item.score, item.chunk_id),
    )
    if max_suggestions is not None:
        suggestions = suggestions[:max_suggestions]

    suggestion_records: list[dict[str, Any]] = []
    for rank, suggestion in enumerate(suggestions, start=1):
        suggestion_records.append(
            {
                "chunk_id": suggestion.chunk_id,
                "rank": rank,
                "suggestion_score": suggestion.score,
                "reasons": suggestion.reasons,
                "source_diagnostic_refs": suggestion.source_refs,
                "suggested_include_l0_arg": suggestion.chunk_id,
                "selection_effect": SELECTION_EFFECT,
            }
        )

    record = {
        "schema_version": ADVISOR_SCHEMA_VERSION,
        "advisor_id": ADVISOR_ID,
        "run_id": run_id or ADVISOR_ID,
        "created_at": created_at or _now_iso(),
        "canonical_path": CANONICAL_SECTION_PATH,
        "selection_effect": SELECTION_EFFECT,
        "contract": {
            "advisory_only": True,
            "automatic_include_l0": False,
            "mutates_context_manifest_items": False,
            "changes_provider_prompts": False,
            "live_retrieval": False,
            "external_embedding_api_calls": False,
            "embedding_creation": False,
            "index_mutation": False,
            "token_budget_enforcement": False,
            "token_budget_telemetry": False,
            "reranker": "none",
        },
        "inputs": {
            "selected_context_item_ids": selected_ids,
            "source_counts": source_counts,
            "max_suggestions": max_suggestions,
        },
        "suggestions": suggestion_records,
        "guardrails": {
            "side_effects_blocked": True,
            "writes_performed": 0,
            "index_mutations": 0,
            "embedding_creations": 0,
            "context_items_mutated": 0,
            "provider_prompts_changed": 0,
            "automatic_include_l0": False,
            "token_budget_enforced": False,
            "token_budget_telemetry_emitted": False,
            "reranker": "none",
        },
    }

    validate_l0_discovery_advisor_record(record)
    return record


def validate_l0_discovery_advisor_record(record: Mapping[str, Any]) -> None:
    """Validate a read-only L0 discovery advisor record."""

    record = _as_mapping(record, "record")

    if record.get("schema_version") != ADVISOR_SCHEMA_VERSION:
        raise L0DiscoveryAdvisorError("schema_version must be v1")
    if record.get("advisor_id") != ADVISOR_ID:
        raise L0DiscoveryAdvisorError(f"advisor_id must be {ADVISOR_ID}")
    if record.get("canonical_path") != CANONICAL_SECTION_PATH:
        raise L0DiscoveryAdvisorError(f"canonical_path must be {CANONICAL_SECTION_PATH}")
    if record.get("selection_effect") != SELECTION_EFFECT:
        raise L0DiscoveryAdvisorError("record selection_effect must be none")

    _nonempty_string(record.get("run_id"), "run_id")
    _nonempty_string(record.get("created_at"), "created_at")

    contract = _as_mapping(record.get("contract"), "contract")
    required_false_contract_fields = (
        "automatic_include_l0",
        "mutates_context_manifest_items",
        "changes_provider_prompts",
        "live_retrieval",
        "external_embedding_api_calls",
        "embedding_creation",
        "index_mutation",
        "token_budget_enforcement",
        "token_budget_telemetry",
    )
    if contract.get("advisory_only") is not True:
        raise L0DiscoveryAdvisorError("contract.advisory_only must be true")
    for field_name in required_false_contract_fields:
        if contract.get(field_name) is not False:
            raise L0DiscoveryAdvisorError(f"contract.{field_name} must be false")
    if contract.get("reranker") != "none":
        raise L0DiscoveryAdvisorError("contract.reranker must be none")

    inputs = _as_mapping(record.get("inputs"), "inputs")
    _as_sequence(inputs.get("selected_context_item_ids"), "inputs.selected_context_item_ids")
    source_counts = _as_mapping(inputs.get("source_counts"), "inputs.source_counts")
    for key in (
        "l0_retrieval_simulator_records",
        "l0_candidate_diagnostics_records",
        "candidate_entries_seen",
    ):
        value = source_counts.get(key)
        if not isinstance(value, int) or value < 0 or isinstance(value, bool):
            raise L0DiscoveryAdvisorError(f"inputs.source_counts.{key} must be a non-negative integer")
    max_suggestions = inputs.get("max_suggestions")
    if max_suggestions is not None and (
        not isinstance(max_suggestions, int) or max_suggestions < 0 or isinstance(max_suggestions, bool)
    ):
        raise L0DiscoveryAdvisorError("inputs.max_suggestions must be a non-negative integer or null")

    suggestions = _as_sequence(record.get("suggestions"), "suggestions")
    seen_chunk_ids: set[str] = set()
    expected_rank = 1
    for suggestion_value in suggestions:
        suggestion = _as_mapping(suggestion_value, "suggestion")
        chunk_id = _nonempty_string(suggestion.get("chunk_id"), "suggestion.chunk_id")
        if chunk_id in seen_chunk_ids:
            raise L0DiscoveryAdvisorError(f"duplicate suggestion chunk_id: {chunk_id}")
        seen_chunk_ids.add(chunk_id)

        rank = suggestion.get("rank")
        if rank != expected_rank:
            raise L0DiscoveryAdvisorError("suggestion ranks must be contiguous starting at 1")
        expected_rank += 1

        _number(suggestion.get("suggestion_score"), "suggestion.suggestion_score")
        if suggestion.get("selection_effect") != SELECTION_EFFECT:
            raise L0DiscoveryAdvisorError("suggestion selection_effect must be none")
        if suggestion.get("suggested_include_l0_arg") != chunk_id:
            raise L0DiscoveryAdvisorError("suggestion.suggested_include_l0_arg must equal chunk_id")

        reasons = _as_sequence(suggestion.get("reasons"), "suggestion.reasons")
        if not reasons:
            raise L0DiscoveryAdvisorError("suggestion.reasons must not be empty")
        for reason in reasons:
            _nonempty_string(reason, "suggestion.reason")

        refs = _as_sequence(suggestion.get("source_diagnostic_refs"), "suggestion.source_diagnostic_refs")
        if not refs:
            raise L0DiscoveryAdvisorError("suggestion.source_diagnostic_refs must not be empty")
        for ref_value in refs:
            ref = _as_mapping(ref_value, "suggestion.source_diagnostic_ref")
            source = _nonempty_string(ref.get("source"), "suggestion.source_diagnostic_ref.source")
            if source not in {"l0_retrieval_simulator", "l0_candidate_diagnostics"}:
                raise L0DiscoveryAdvisorError("suggestion.source_diagnostic_ref.source is unsupported")
            _nonempty_string(
                ref.get("source_candidate_id"),
                "suggestion.source_diagnostic_ref.source_candidate_id",
            )
            source_path = ref.get("source_path")
            if source_path is not None:
                _nonempty_string(source_path, "suggestion.source_diagnostic_ref.source_path")

    guardrails = _as_mapping(record.get("guardrails"), "guardrails")
    if guardrails.get("side_effects_blocked") is not True:
        raise L0DiscoveryAdvisorError("guardrails.side_effects_blocked must be true")
    for key in (
        "writes_performed",
        "index_mutations",
        "embedding_creations",
        "context_items_mutated",
        "provider_prompts_changed",
    ):
        if guardrails.get(key) != 0:
            raise L0DiscoveryAdvisorError(f"guardrails.{key} must be 0")
    for key in (
        "automatic_include_l0",
        "token_budget_enforced",
        "token_budget_telemetry_emitted",
    ):
        if guardrails.get(key) is not False:
            raise L0DiscoveryAdvisorError(f"guardrails.{key} must be false")
    if guardrails.get("reranker") != "none":
        raise L0DiscoveryAdvisorError("guardrails.reranker must be none")


def l0_discovery_advisor_manifest_document(record: Mapping[str, Any]) -> dict[str, Any]:
    """Wrap an advisor record at its canonical manifest diagnostics path."""

    validate_l0_discovery_advisor_record(record)
    return {
        "manifest": {
            "diagnostics": {
                "l0_discovery_advisor": dict(record),
            }
        }
    }


def load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise L0DiscoveryAdvisorError(f"{path} must contain a JSON object")
    return value
