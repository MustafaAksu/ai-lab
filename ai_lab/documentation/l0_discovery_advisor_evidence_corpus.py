from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from ai_lab.documentation.l0_discovery_advisor import (
    build_l0_discovery_advisor_record,
)
from ai_lab.documentation.l0_discovery_advisor_evaluation import (
    evaluate_l0_discovery_advisor_manifest_paths,
    validate_l0_discovery_advisor_evaluation_record,
)


CORPUS_SCHEMA_VERSION = "v1"
CORPUS_ID = "l0_discovery_advisor_evidence_corpus.v1"
PLAN_ID = "PLAN-20260707-0004"
SELECTION_EFFECT = "none"

DEFAULT_OUTPUT_ROOT = Path("docs/reviews/l0_discovery_advisor_evidence_corpus")


class L0DiscoveryAdvisorEvidenceCorpusError(ValueError):
    """Raised when an L0 discovery advisor evidence corpus record is malformed."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise L0DiscoveryAdvisorEvidenceCorpusError(f"{field_name} must be an object")
    return value


def _as_sequence(value: Any, field_name: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise L0DiscoveryAdvisorEvidenceCorpusError(f"{field_name} must be a sequence")
    return value


def _nonempty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise L0DiscoveryAdvisorEvidenceCorpusError(
            f"{field_name} must be a non-empty string"
        )
    return value


def _nonnegative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise L0DiscoveryAdvisorEvidenceCorpusError(
            f"{field_name} must be a non-negative integer"
        )
    return value


def _manifest(
    *,
    manifest_id: str,
    task: str,
    items: Sequence[Mapping[str, Any]],
    diagnostics: Mapping[str, Any] | None,
) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "schema_version": "v1",
        "manifest_id": manifest_id,
        "task": task,
        "assembly_policy": "latest_context",
        "items": [dict(item) for item in items],
    }
    if diagnostics is not None:
        manifest["diagnostics"] = dict(diagnostics)
    return manifest


def _item(item_id: str, reason: str) -> dict[str, Any]:
    return {
        "item_type": "abstraction",
        "item_id": item_id,
        "reason": reason,
        "relevance_score": 0.9,
        "token_estimate": 100,
        "source_path": f"docs/abstractions/{item_id}.md",
    }


def _advisor_from_candidates(
    *,
    selected_context_item_ids: Sequence[str],
    candidates: Sequence[Mapping[str, Any]],
    run_id: str,
    created_at: str,
) -> dict[str, Any]:
    return build_l0_discovery_advisor_record(
        selected_context_item_ids=selected_context_item_ids,
        candidate_diagnostics_records=[{"candidates": [dict(item) for item in candidates]}],
        candidate_diagnostics_paths=[f"deterministic-fixture:{run_id}"],
        run_id=run_id,
        created_at=created_at,
    )


def build_l0_discovery_advisor_evidence_manifest_records(
    *,
    created_at: str = "2026-07-07T00:00:00Z",
) -> tuple[dict[str, Any], ...]:
    """Build deterministic saved-manifest fixtures for evidence gathering."""

    manifests: list[dict[str, Any]] = []

    for index in range(12):
        manifest_id = f"corpus-expanded-{index + 1:02d}"
        selected_item_id = f"CTX-EXPANDED-{index + 1:02d}"
        first_chunk = f"L0-EXPANDED-{(index * 2) + 1:02d}"
        second_chunk = f"L0-EXPANDED-{(index * 2) + 2:02d}"

        advisor = _advisor_from_candidates(
            selected_context_item_ids=[selected_item_id],
            candidates=[
                {
                    "chunk_id": first_chunk,
                    "score": 0.86,
                    "reason": "primary deterministic neighboring evidence",
                },
                {
                    "chunk_id": second_chunk,
                    "score": 0.62,
                    "reason": "secondary deterministic neighboring evidence",
                },
            ],
            run_id=manifest_id,
            created_at=created_at,
        )

        manifests.append(
            _manifest(
                manifest_id=manifest_id,
                task="Evaluate clean deterministic L0 discovery suggestions.",
                items=(
                    _item(
                        selected_item_id,
                        "Selected context for expanded useful-suggestion evidence.",
                    ),
                ),
                diagnostics={"l0_discovery_advisor": advisor},
            )
        )

    return tuple(manifests)


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_l0_discovery_advisor_evidence_corpus(
    *,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
    run_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Write deterministic manifest fixtures and aggregate evaluation evidence."""

    created_at = created_at or _now_iso()
    run_id = run_id or CORPUS_ID

    manifests = build_l0_discovery_advisor_evidence_manifest_records(
        created_at=created_at,
    )
    manifest_dir = output_root / "manifests"
    manifest_paths: list[Path] = []

    for manifest in manifests:
        manifest_id = _nonempty_string(manifest.get("manifest_id"), "manifest_id")
        path = manifest_dir / f"{manifest_id}.json"
        _write_json(path, manifest)
        manifest_paths.append(path)

    evaluation = evaluate_l0_discovery_advisor_manifest_paths(
        manifest_paths,
        run_id=run_id,
        created_at=created_at,
    )
    validate_l0_discovery_advisor_evaluation_record(evaluation)

    aggregate = evaluation["aggregate"]
    evidence = {
        "schema_version": CORPUS_SCHEMA_VERSION,
        "corpus_id": CORPUS_ID,
        "plan_id": PLAN_ID,
        "created_at": created_at,
        "run_id": run_id,
        "selection_effect": SELECTION_EFFECT,
        "contract": {
            "diagnostic_evidence_only": True,
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
            "manifest_paths": [str(path) for path in manifest_paths],
            "deterministic_fixture_count": len(manifest_paths),
            "evaluator": "scripts/evaluate_l0_discovery_advisor.py",
        },
        "findings": {
            "manifests_seen": aggregate["manifests_seen"],
            "manifests_with_advisor": aggregate["manifests_with_advisor"],
            "manifests_missing_advisor": aggregate["manifests_missing_advisor"],
            "manifests_invalid_advisor": aggregate["manifests_invalid_advisor"],
            "total_suggestions": aggregate["total_suggestions"],
            "unique_suggested_chunk_count": aggregate["unique_suggested_chunk_count"],
            "already_selected_suggestion_count": aggregate[
                "already_selected_suggestion_count"
            ],
            "duplicate_suggestion_count": aggregate["duplicate_suggestion_count"],
        },
        "evaluation": evaluation,
        "guardrails": {
            "side_effects_blocked": True,
            "context_items_mutated": 0,
            "provider_prompts_changed": 0,
            "latest_context_prompt_path_changed": 0,
            "automatic_include_l0": False,
            "live_retrieval": False,
            "external_embedding_api_calls": False,
            "embedding_creations": 0,
            "index_mutations": 0,
            "memory_store_mutations": 0,
            "token_budget_enforced": False,
            "token_budget_telemetry_emitted": False,
            "reranker": "none",
            "adapter_behavior": False,
        },
        "outputs": {
            "output_root": str(output_root),
            "evidence_path": str(output_root / "evidence.json"),
            "manifest_dir": str(manifest_dir),
        },
    }

    validate_l0_discovery_advisor_evidence_corpus_record(evidence)
    _write_json(output_root / "evidence.json", evidence)
    return evidence


def validate_l0_discovery_advisor_evidence_corpus_record(
    record: Mapping[str, Any],
) -> None:
    """Validate diagnostic-only evidence corpus output."""

    record = _as_mapping(record, "record")

    if record.get("schema_version") != CORPUS_SCHEMA_VERSION:
        raise L0DiscoveryAdvisorEvidenceCorpusError("schema_version must be v1")
    if record.get("corpus_id") != CORPUS_ID:
        raise L0DiscoveryAdvisorEvidenceCorpusError(f"corpus_id must be {CORPUS_ID}")
    if record.get("plan_id") != PLAN_ID:
        raise L0DiscoveryAdvisorEvidenceCorpusError(f"plan_id must be {PLAN_ID}")
    if record.get("selection_effect") != SELECTION_EFFECT:
        raise L0DiscoveryAdvisorEvidenceCorpusError("selection_effect must be none")

    _nonempty_string(record.get("created_at"), "created_at")
    _nonempty_string(record.get("run_id"), "run_id")

    contract = _as_mapping(record.get("contract"), "contract")
    if contract.get("diagnostic_evidence_only") is not True:
        raise L0DiscoveryAdvisorEvidenceCorpusError(
            "contract.diagnostic_evidence_only must be true"
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
            raise L0DiscoveryAdvisorEvidenceCorpusError(f"contract.{key} must be false")
    if contract.get("reranker") != "none":
        raise L0DiscoveryAdvisorEvidenceCorpusError("contract.reranker must be none")

    inputs = _as_mapping(record.get("inputs"), "inputs")
    manifest_paths = _as_sequence(inputs.get("manifest_paths"), "inputs.manifest_paths")
    _nonnegative_int(
        inputs.get("deterministic_fixture_count"),
        "inputs.deterministic_fixture_count",
    )
    if inputs["deterministic_fixture_count"] != len(manifest_paths):
        raise L0DiscoveryAdvisorEvidenceCorpusError(
            "inputs.deterministic_fixture_count must equal manifest path count"
        )
    _nonempty_string(inputs.get("evaluator"), "inputs.evaluator")

    findings = _as_mapping(record.get("findings"), "findings")
    for key in (
        "manifests_seen",
        "manifests_with_advisor",
        "manifests_missing_advisor",
        "manifests_invalid_advisor",
        "total_suggestions",
        "unique_suggested_chunk_count",
        "already_selected_suggestion_count",
        "duplicate_suggestion_count",
    ):
        _nonnegative_int(findings.get(key), f"findings.{key}")

    evaluation = _as_mapping(record.get("evaluation"), "evaluation")
    validate_l0_discovery_advisor_evaluation_record(evaluation)

    guardrails = _as_mapping(record.get("guardrails"), "guardrails")
    if guardrails.get("side_effects_blocked") is not True:
        raise L0DiscoveryAdvisorEvidenceCorpusError(
            "guardrails.side_effects_blocked must be true"
        )
    for key in (
        "context_items_mutated",
        "provider_prompts_changed",
        "latest_context_prompt_path_changed",
        "embedding_creations",
        "index_mutations",
        "memory_store_mutations",
    ):
        if guardrails.get(key) != 0:
            raise L0DiscoveryAdvisorEvidenceCorpusError(f"guardrails.{key} must be 0")
    for key in (
        "automatic_include_l0",
        "live_retrieval",
        "external_embedding_api_calls",
        "token_budget_enforced",
        "token_budget_telemetry_emitted",
        "adapter_behavior",
    ):
        if guardrails.get(key) is not False:
            raise L0DiscoveryAdvisorEvidenceCorpusError(f"guardrails.{key} must be false")
    if guardrails.get("reranker") != "none":
        raise L0DiscoveryAdvisorEvidenceCorpusError("guardrails.reranker must be none")

    outputs = _as_mapping(record.get("outputs"), "outputs")
    _nonempty_string(outputs.get("output_root"), "outputs.output_root")
    _nonempty_string(outputs.get("evidence_path"), "outputs.evidence_path")
    _nonempty_string(outputs.get("manifest_dir"), "outputs.manifest_dir")
