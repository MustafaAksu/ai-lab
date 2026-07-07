from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


THRESHOLD_SCHEMA_VERSION = "v1"
THRESHOLD_REVIEW_ID = "l0_discovery_advisor_acceptance_thresholds.v1"
PLAN_ID = "PLAN-20260707-0003"
SELECTION_EFFECT = "none"

DEFAULT_EVIDENCE_PATH = Path(
    "docs/reviews/l0_discovery_advisor_evidence_corpus/evidence.json"
)
DEFAULT_OUTPUT_PATH = Path("docs/reviews/l0_discovery_advisor_thresholds/thresholds.json")


class L0DiscoveryAdvisorThresholdReviewError(ValueError):
    """Raised when an L0 discovery advisor threshold review is malformed."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise L0DiscoveryAdvisorThresholdReviewError(f"{field_name} must be an object")
    return value


def _as_sequence(value: Any, field_name: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise L0DiscoveryAdvisorThresholdReviewError(f"{field_name} must be a sequence")
    return value


def _nonempty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise L0DiscoveryAdvisorThresholdReviewError(
            f"{field_name} must be a non-empty string"
        )
    return value


def _nonnegative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise L0DiscoveryAdvisorThresholdReviewError(
            f"{field_name} must be a non-negative integer"
        )
    return value


def _bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise L0DiscoveryAdvisorThresholdReviewError(f"{field_name} must be a boolean")
    return value


def _ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 6)


def _threshold(
    *,
    threshold_id: str,
    description: str,
    observed: int | float | bool | str,
    operator: str,
    required: int | float | bool | str,
    passes: bool,
    blocking: bool = True,
) -> dict[str, Any]:
    return {
        "threshold_id": threshold_id,
        "description": description,
        "observed": observed,
        "operator": operator,
        "required": required,
        "passes": passes,
        "blocking": blocking,
    }


def build_l0_discovery_advisor_threshold_review(
    *,
    evidence: Mapping[str, Any],
    evidence_source_path: Path | str = DEFAULT_EVIDENCE_PATH,
    run_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build a review-only acceptance-threshold record from saved evidence.

    This function intentionally does not mutate context manifests, provider prompts,
    indexes, memory stores, retrieval systems, token-budget systems, rerankers, or
    adapters. It only reads an evidence record supplied by the caller and returns a
    decision artifact.
    """

    created_at = created_at or _now_iso()
    run_id = run_id or THRESHOLD_REVIEW_ID

    evidence = _as_mapping(evidence, "evidence")
    findings = dict(_as_mapping(evidence.get("findings"), "evidence.findings"))
    guardrails = dict(_as_mapping(evidence.get("guardrails"), "evidence.guardrails"))

    manifests_seen = _nonnegative_int(findings.get("manifests_seen"), "manifests_seen")
    manifests_with_advisor = _nonnegative_int(
        findings.get("manifests_with_advisor"), "manifests_with_advisor"
    )
    manifests_missing_advisor = _nonnegative_int(
        findings.get("manifests_missing_advisor"), "manifests_missing_advisor"
    )
    manifests_invalid_advisor = _nonnegative_int(
        findings.get("manifests_invalid_advisor"), "manifests_invalid_advisor"
    )
    total_suggestions = _nonnegative_int(
        findings.get("total_suggestions"), "total_suggestions"
    )
    unique_suggested_chunk_count = _nonnegative_int(
        findings.get("unique_suggested_chunk_count"), "unique_suggested_chunk_count"
    )
    already_selected_suggestion_count = _nonnegative_int(
        findings.get("already_selected_suggestion_count"),
        "already_selected_suggestion_count",
    )
    duplicate_suggestion_count = _nonnegative_int(
        findings.get("duplicate_suggestion_count"), "duplicate_suggestion_count"
    )

    observed_metrics = {
        "manifest_count": manifests_seen,
        "valid_advisor_manifest_count": manifests_with_advisor,
        "missing_advisor_manifest_rate": _ratio(
            manifests_missing_advisor, manifests_seen
        ),
        "invalid_advisor_manifest_rate": _ratio(
            manifests_invalid_advisor, manifests_seen
        ),
        "already_selected_suggestion_rate": _ratio(
            already_selected_suggestion_count, total_suggestions
        ),
        "duplicate_suggestion_rate": _ratio(
            duplicate_suggestion_count, total_suggestions
        ),
        "unique_suggested_chunk_count": unique_suggested_chunk_count,
        "total_suggestions": total_suggestions,
    }

    runtime_guardrails_pass = (
        guardrails.get("automatic_include_l0") is False
        and guardrails.get("context_items_mutated") == 0
        and guardrails.get("provider_prompts_changed") == 0
        and guardrails.get("latest_context_prompt_path_changed") == 0
        and guardrails.get("live_retrieval") is False
        and guardrails.get("external_embedding_api_calls") is False
        and guardrails.get("embedding_creations") == 0
        and guardrails.get("index_mutations") == 0
        and guardrails.get("memory_store_mutations") == 0
        and guardrails.get("token_budget_enforced") is False
        and guardrails.get("token_budget_telemetry_emitted") is False
        and guardrails.get("reranker") == "none"
        and guardrails.get("adapter_behavior") is False
    )

    thresholds = [
        _threshold(
            threshold_id="minimum_manifest_count",
            description=(
                "Automatic include_l0 requires a broader deterministic evidence corpus."
            ),
            observed=manifests_seen,
            operator=">=",
            required=12,
            passes=manifests_seen >= 12,
        ),
        _threshold(
            threshold_id="minimum_valid_advisor_manifest_count",
            description="Automatic include_l0 requires enough valid advisor-bearing manifests.",
            observed=manifests_with_advisor,
            operator=">=",
            required=8,
            passes=manifests_with_advisor >= 8,
        ),
        _threshold(
            threshold_id="maximum_missing_advisor_manifest_rate",
            description="Missing advisor diagnostics must be rare before automatic inclusion.",
            observed=observed_metrics["missing_advisor_manifest_rate"],
            operator="<=",
            required=0.05,
            passes=observed_metrics["missing_advisor_manifest_rate"] <= 0.05,
        ),
        _threshold(
            threshold_id="maximum_invalid_advisor_manifest_rate",
            description="Invalid advisor diagnostics must be zero before automatic inclusion.",
            observed=observed_metrics["invalid_advisor_manifest_rate"],
            operator="<=",
            required=0.0,
            passes=observed_metrics["invalid_advisor_manifest_rate"] <= 0.0,
        ),
        _threshold(
            threshold_id="maximum_already_selected_suggestion_rate",
            description="Redundant already-selected suggestions must stay low.",
            observed=observed_metrics["already_selected_suggestion_rate"],
            operator="<=",
            required=0.10,
            passes=observed_metrics["already_selected_suggestion_rate"] <= 0.10,
        ),
        _threshold(
            threshold_id="maximum_duplicate_suggestion_rate",
            description="Duplicate advisor suggestions must remain absent.",
            observed=observed_metrics["duplicate_suggestion_rate"],
            operator="<=",
            required=0.0,
            passes=observed_metrics["duplicate_suggestion_rate"] <= 0.0,
        ),
        _threshold(
            threshold_id="minimum_unique_suggested_chunk_count",
            description="Automatic inclusion needs more unique candidate coverage.",
            observed=unique_suggested_chunk_count,
            operator=">=",
            required=12,
            passes=unique_suggested_chunk_count >= 12,
        ),
        _threshold(
            threshold_id="runtime_side_effect_guardrail",
            description="Evidence must remain diagnostic-only with no runtime side effects.",
            observed=runtime_guardrails_pass,
            operator="is",
            required=True,
            passes=runtime_guardrails_pass,
        ),
    ]

    blocking_criteria = [
        item["threshold_id"]
        for item in thresholds
        if item["blocking"] and not item["passes"]
    ]
    approved = not blocking_criteria

    review_guardrails = {
        "automatic_include_l0": False,
        "context_items_mutated": 0,
        "provider_prompts_changed": 0,
        "latest_context_prompt_path_changed": 0,
        "live_retrieval": False,
        "external_embedding_api_calls": False,
        "embedding_creations": 0,
        "index_mutations": 0,
        "memory_store_mutations": 0,
        "token_budget_enforced": False,
        "token_budget_telemetry_emitted": False,
        "reranker": "none",
        "adapter_behavior": False,
        "side_effects_blocked": True,
    }

    return {
        "schema_version": THRESHOLD_SCHEMA_VERSION,
        "threshold_review_id": THRESHOLD_REVIEW_ID,
        "plan_id": PLAN_ID,
        "created_at": created_at,
        "run_id": run_id,
        "review_type": "automatic_l0_discovery_acceptance_thresholds",
        "selection_effect": SELECTION_EFFECT,
        "evidence_source_path": str(evidence_source_path),
        "evidence_corpus_id": _nonempty_string(
            evidence.get("corpus_id"), "evidence.corpus_id"
        ),
        "contract": {
            "review_only": True,
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
            "evidence_plan_id": _nonempty_string(
                evidence.get("plan_id"), "evidence.plan_id"
            ),
            "evidence_findings": findings,
            "evidence_guardrails": guardrails,
        },
        "observed_metrics": observed_metrics,
        "thresholds": thresholds,
        "decision": {
            "approved_for_automatic_include_l0": approved,
            "decision": "approved" if approved else "not_ready",
            "reason": (
                "All blocking thresholds pass."
                if approved
                else "Current evidence corpus is too small and mixed for automatic include_l0."
            ),
            "blocking_criteria": blocking_criteria,
            "next_required_evidence": [
                "Expand deterministic corpus to at least 12 manifests.",
                "Include at least 8 valid advisor-bearing manifests.",
                "Drive missing advisor diagnostic rate to <= 5%.",
                "Drive invalid advisor diagnostic rate to 0%.",
                "Keep already-selected suggestion rate <= 10%.",
                "Keep duplicate suggestion rate at 0%.",
                "Demonstrate at least 12 unique suggested L0 chunks.",
            ],
        },
        "guardrails": review_guardrails,
    }


def validate_l0_discovery_advisor_threshold_review_record(
    record: Mapping[str, Any],
) -> None:
    """Validate the review-only acceptance-threshold record."""

    record = _as_mapping(record, "record")
    if record.get("schema_version") != THRESHOLD_SCHEMA_VERSION:
        raise L0DiscoveryAdvisorThresholdReviewError("unsupported schema_version")
    if record.get("threshold_review_id") != THRESHOLD_REVIEW_ID:
        raise L0DiscoveryAdvisorThresholdReviewError("unexpected threshold_review_id")
    if record.get("plan_id") != PLAN_ID:
        raise L0DiscoveryAdvisorThresholdReviewError("unexpected plan_id")
    if record.get("selection_effect") != SELECTION_EFFECT:
        raise L0DiscoveryAdvisorThresholdReviewError("selection_effect must be none")

    _nonempty_string(record.get("created_at"), "created_at")
    _nonempty_string(record.get("run_id"), "run_id")
    _nonempty_string(record.get("evidence_source_path"), "evidence_source_path")
    _nonempty_string(record.get("evidence_corpus_id"), "evidence_corpus_id")

    contract = _as_mapping(record.get("contract"), "contract")
    if contract.get("review_only") is not True:
        raise L0DiscoveryAdvisorThresholdReviewError("contract.review_only must be true")
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
            raise L0DiscoveryAdvisorThresholdReviewError(f"contract.{key} must be false")
    if contract.get("reranker") != "none":
        raise L0DiscoveryAdvisorThresholdReviewError("contract.reranker must be none")

    observed_metrics = _as_mapping(record.get("observed_metrics"), "observed_metrics")
    for key in (
        "manifest_count",
        "valid_advisor_manifest_count",
        "unique_suggested_chunk_count",
        "total_suggestions",
    ):
        _nonnegative_int(observed_metrics.get(key), f"observed_metrics.{key}")

    thresholds = _as_sequence(record.get("thresholds"), "thresholds")
    if not thresholds:
        raise L0DiscoveryAdvisorThresholdReviewError("thresholds must not be empty")
    for index, threshold in enumerate(thresholds):
        threshold = _as_mapping(threshold, f"thresholds[{index}]")
        _nonempty_string(threshold.get("threshold_id"), f"thresholds[{index}].threshold_id")
        _nonempty_string(threshold.get("description"), f"thresholds[{index}].description")
        _nonempty_string(threshold.get("operator"), f"thresholds[{index}].operator")
        _bool(threshold.get("passes"), f"thresholds[{index}].passes")
        _bool(threshold.get("blocking"), f"thresholds[{index}].blocking")

    decision = _as_mapping(record.get("decision"), "decision")
    if decision.get("approved_for_automatic_include_l0") is not False:
        raise L0DiscoveryAdvisorThresholdReviewError(
            "decision.approved_for_automatic_include_l0 must be false"
        )
    if decision.get("decision") != "not_ready":
        raise L0DiscoveryAdvisorThresholdReviewError("decision must be not_ready")
    blocking_criteria = _as_sequence(
        decision.get("blocking_criteria"), "decision.blocking_criteria"
    )
    if not blocking_criteria:
        raise L0DiscoveryAdvisorThresholdReviewError(
            "decision.blocking_criteria must not be empty"
        )

    guardrails = _as_mapping(record.get("guardrails"), "guardrails")
    if guardrails.get("automatic_include_l0") is not False:
        raise L0DiscoveryAdvisorThresholdReviewError(
            "guardrails.automatic_include_l0 must be false"
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
            raise L0DiscoveryAdvisorThresholdReviewError(f"guardrails.{key} must be 0")
    for key in (
        "live_retrieval",
        "external_embedding_api_calls",
        "token_budget_enforced",
        "token_budget_telemetry_emitted",
        "adapter_behavior",
    ):
        if guardrails.get(key) is not False:
            raise L0DiscoveryAdvisorThresholdReviewError(
                f"guardrails.{key} must be false"
            )
    if guardrails.get("reranker") != "none":
        raise L0DiscoveryAdvisorThresholdReviewError("guardrails.reranker must be none")


def write_l0_discovery_advisor_threshold_review(
    *,
    evidence_path: Path = DEFAULT_EVIDENCE_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
    run_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Read saved evidence and write the review-only threshold artifact."""

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    review = build_l0_discovery_advisor_threshold_review(
        evidence=evidence,
        evidence_source_path=evidence_path,
        run_id=run_id,
        created_at=created_at,
    )
    validate_l0_discovery_advisor_threshold_review_record(review)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(review, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return review
