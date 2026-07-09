import json
import subprocess
import sys

import pytest

from ai_lab.documentation.l0_discovery_advisor_evidence_corpus import (
    write_l0_discovery_advisor_evidence_corpus,
)
from ai_lab.documentation.l0_discovery_advisor_thresholds import (
    PLAN_ID,
    THRESHOLD_REVIEW_ID,
    L0DiscoveryAdvisorThresholdReviewError,
    build_l0_discovery_advisor_threshold_review,
    validate_l0_discovery_advisor_threshold_review_record,
    write_l0_discovery_advisor_threshold_review,
)


def _current_evidence(tmp_path):
    return write_l0_discovery_advisor_evidence_corpus(
        output_root=tmp_path / "corpus",
        run_id="threshold-source",
        created_at="2026-07-07T00:00:00Z",
    )


def test_build_threshold_review_marks_expanded_evidence_approved(tmp_path):
    evidence = _current_evidence(tmp_path)

    review = build_l0_discovery_advisor_threshold_review(
        evidence=evidence,
        evidence_source_path=tmp_path / "corpus" / "evidence.json",
        run_id="threshold-test",
        created_at="2026-07-07T00:00:00Z",
    )

    validate_l0_discovery_advisor_threshold_review_record(review)

    assert review["threshold_review_id"] == THRESHOLD_REVIEW_ID
    assert review["plan_id"] == PLAN_ID
    assert review["selection_effect"] == "none"
    assert review["contract"]["review_only"] is True
    assert review["contract"]["automatic_include_l0"] is False
    assert review["decision"]["approved_for_automatic_include_l0"] is True
    assert review["decision"]["decision"] == "approved"
    assert review["observed_metrics"]["manifest_count"] == 12
    assert review["observed_metrics"]["valid_advisor_manifest_count"] == 12
    assert review["observed_metrics"]["missing_advisor_manifest_rate"] == 0.0
    assert review["observed_metrics"]["invalid_advisor_manifest_rate"] == 0.0
    assert review["observed_metrics"]["already_selected_suggestion_rate"] == 0.0
    assert review["observed_metrics"]["duplicate_suggestion_rate"] == 0.0

    blocking = set(review["decision"]["blocking_criteria"])
    assert blocking == set()
    assert all(threshold["passes"] for threshold in review["thresholds"])
    assert review["decision"]["next_required_evidence"] == []


def test_threshold_review_preserves_review_only_guardrails(tmp_path):
    review = build_l0_discovery_advisor_threshold_review(
        evidence=_current_evidence(tmp_path),
        run_id="guardrail-test",
        created_at="2026-07-07T00:00:00Z",
    )

    assert review["guardrails"] == {
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


def test_write_threshold_review_reads_evidence_and_writes_thresholds_json(tmp_path):
    evidence_root = tmp_path / "corpus"
    write_l0_discovery_advisor_evidence_corpus(
        output_root=evidence_root,
        run_id="write-threshold-source",
        created_at="2026-07-07T00:00:00Z",
    )
    output_path = tmp_path / "thresholds" / "thresholds.json"

    review = write_l0_discovery_advisor_threshold_review(
        evidence_path=evidence_root / "evidence.json",
        output_path=output_path,
        run_id="write-threshold-test",
        created_at="2026-07-07T00:00:00Z",
    )

    assert output_path.exists()
    persisted = json.loads(output_path.read_text(encoding="utf-8"))
    validate_l0_discovery_advisor_threshold_review_record(persisted)
    assert persisted == review
    assert persisted["run_id"] == "write-threshold-test"
    assert persisted["evidence_source_path"] == str(evidence_root / "evidence.json")


def test_validator_rejects_inconsistent_approved_threshold_decision(tmp_path):
    review = build_l0_discovery_advisor_threshold_review(
        evidence=_current_evidence(tmp_path),
        run_id="bad-approval",
        created_at="2026-07-07T00:00:00Z",
    )
    review["decision"]["decision"] = "not_ready"

    with pytest.raises(
        L0DiscoveryAdvisorThresholdReviewError,
        match="approved threshold reviews must use decision approved",
    ):
        validate_l0_discovery_advisor_threshold_review_record(review)


def test_validator_rejects_runtime_side_effect_contract(tmp_path):
    review = build_l0_discovery_advisor_threshold_review(
        evidence=_current_evidence(tmp_path),
        run_id="bad-contract",
        created_at="2026-07-07T00:00:00Z",
    )
    review["contract"]["changes_provider_prompts"] = True

    with pytest.raises(
        L0DiscoveryAdvisorThresholdReviewError,
        match="changes_provider_prompts",
    ):
        validate_l0_discovery_advisor_threshold_review_record(review)


def test_cli_writes_threshold_review(tmp_path):
    evidence_root = tmp_path / "corpus"
    write_l0_discovery_advisor_evidence_corpus(
        output_root=evidence_root,
        run_id="cli-threshold-source",
        created_at="2026-07-07T00:00:00Z",
    )
    output_path = tmp_path / "thresholds" / "thresholds.json"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_l0_discovery_advisor_thresholds.py",
            "--evidence-path",
            str(evidence_root / "evidence.json"),
            "--output-path",
            str(output_path),
            "--run-id",
            "cli-threshold",
            "--created-at",
            "2026-07-07T00:00:00Z",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    review = json.loads(completed.stdout)
    validate_l0_discovery_advisor_threshold_review_record(review)
    assert output_path.exists()
    assert review["run_id"] == "cli-threshold"
    assert review["decision"]["decision"] == "approved"
    assert review["guardrails"]["automatic_include_l0"] is False
