import json
import subprocess
import sys

import pytest

from ai_lab.documentation.l0_discovery_advisor import (
    build_l0_discovery_advisor_record,
)
from ai_lab.documentation.l0_discovery_advisor_evaluation import (
    EVALUATOR_ID,
    L0DiscoveryAdvisorEvaluationError,
    build_l0_discovery_advisor_evaluation_record,
    evaluate_l0_discovery_advisor_manifest_paths,
    evaluate_manifest_record,
    validate_l0_discovery_advisor_evaluation_record,
)


def advisor_record():
    return build_l0_discovery_advisor_record(
        selected_context_item_ids=["CTX-1"],
        candidate_diagnostics_records=[
            {
                "candidates": [
                    {
                        "chunk_id": "L0-ALPHA",
                        "score": 0.8,
                        "reason": "candidate diagnostic overlap",
                    },
                    {
                        "chunk_id": "CTX-1",
                        "score": 0.4,
                        "reason": "already selected context item",
                    },
                ]
            }
        ],
        run_id="advisor-eval-fixture",
        created_at="2026-07-07T00:00:00Z",
    )


def manifest_record():
    return {
        "manifest_id": "manifest-1",
        "items": [
            {
                "item_type": "abstraction",
                "item_id": "CTX-1",
                "reason": "selected context",
                "relevance_score": 0.9,
            }
        ],
        "diagnostics": {
            "l0_discovery_advisor": advisor_record(),
        },
    }


def test_evaluate_manifest_record_counts_suggestions_without_selection_effect():
    result = evaluate_manifest_record(
        manifest_record(),
        source_path="manifest.json",
    )

    assert result["source_path"] == "manifest.json"
    assert result["manifest_status"] == "ok"
    assert result["advisor_status"] == "ok"
    assert result["selection_effect"] == "none"
    assert result["selected_item_ids"] == ["CTX-1"]
    assert result["suggestion_count"] == 2
    assert result["unique_suggested_chunk_ids"] == ["CTX-1", "L0-ALPHA"]
    assert result["already_selected_suggestion_count"] == 1
    assert result["already_selected_suggestion_ids"] == ["CTX-1"]
    assert result["advisor_guardrails"]["automatic_include_l0"] is False
    assert result["advisor_guardrails"]["context_items_mutated"] == 0
    assert result["advisor_guardrails"]["provider_prompts_changed"] == 0


def test_build_evaluation_record_is_diagnostic_only():
    evaluation = evaluate_manifest_record(manifest_record())
    record = build_l0_discovery_advisor_evaluation_record(
        manifest_evaluations=[evaluation],
        manifest_paths=["manifest.json"],
        run_id="evaluation-test",
        created_at="2026-07-07T00:00:00Z",
    )

    validate_l0_discovery_advisor_evaluation_record(record)

    assert record["evaluator_id"] == EVALUATOR_ID
    assert record["selection_effect"] == "none"
    assert record["contract"]["diagnostic_evaluation_only"] is True
    assert record["contract"]["automatic_include_l0"] is False
    assert record["contract"]["mutates_context_manifest_items"] is False
    assert record["contract"]["changes_provider_prompts"] is False
    assert record["contract"]["live_retrieval"] is False
    assert record["contract"]["embedding_creation"] is False
    assert record["contract"]["index_mutation"] is False
    assert record["contract"]["memory_store_mutation"] is False
    assert record["contract"]["token_budget_telemetry"] is False
    assert record["contract"]["adapter_behavior"] is False
    assert record["aggregate"]["manifests_seen"] == 1
    assert record["aggregate"]["manifests_with_advisor"] == 1
    assert record["aggregate"]["total_suggestions"] == 2
    assert record["aggregate"]["already_selected_suggestion_count"] == 1
    assert record["guardrails"]["writes_performed"] == 0
    assert record["guardrails"]["context_items_mutated"] == 0
    assert record["guardrails"]["provider_prompts_changed"] == 0
    assert record["guardrails"]["automatic_include_l0"] is False
    assert record["guardrails"]["adapter_behavior"] is False


def test_evaluate_manifest_record_handles_missing_advisor_nonfatally():
    result = evaluate_manifest_record(
        {
            "items": [
                {
                    "item_type": "abstraction",
                    "item_id": "CTX-1",
                    "reason": "selected context",
                    "relevance_score": 0.9,
                }
            ]
        }
    )

    assert result["manifest_status"] == "ok"
    assert result["advisor_status"] == "missing_diagnostics"
    assert result["selected_item_ids"] == ["CTX-1"]
    assert result["suggestion_count"] == 0
    assert result["selection_effect"] == "none"

    record = build_l0_discovery_advisor_evaluation_record(
        manifest_evaluations=[result],
        manifest_paths=["missing.json"],
        run_id="missing-test",
        created_at="2026-07-07T00:00:00Z",
    )

    assert record["aggregate"]["manifests_with_advisor"] == 0
    assert record["aggregate"]["manifests_missing_advisor"] == 1
    assert record["aggregate"]["total_suggestions"] == 0


def test_evaluate_manifest_paths_handles_invalid_json_nonfatally(tmp_path):
    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{", encoding="utf-8")

    record = evaluate_l0_discovery_advisor_manifest_paths(
        [bad_path],
        run_id="invalid-json-test",
        created_at="2026-07-07T00:00:00Z",
    )

    validate_l0_discovery_advisor_evaluation_record(record)
    assert record["aggregate"]["manifests_seen"] == 1
    assert record["aggregate"]["manifests_missing_advisor"] == 1
    assert record["manifest_evaluations"][0]["manifest_status"] == "invalid_json"
    assert record["guardrails"]["writes_performed"] == 0


def test_validator_rejects_automatic_include_l0_contract():
    evaluation = evaluate_manifest_record(manifest_record())
    record = build_l0_discovery_advisor_evaluation_record(
        manifest_evaluations=[evaluation],
        run_id="bad-contract",
        created_at="2026-07-07T00:00:00Z",
    )
    record["contract"]["automatic_include_l0"] = True

    with pytest.raises(L0DiscoveryAdvisorEvaluationError, match="automatic_include_l0"):
        validate_l0_discovery_advisor_evaluation_record(record)


def test_cli_evaluates_saved_manifest_and_writes_output(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    output_path = tmp_path / "evaluation.json"
    manifest_path.write_text(json.dumps(manifest_record()), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_l0_discovery_advisor.py",
            "--manifest",
            str(manifest_path),
            "--run-id",
            "cli-evaluation",
            "--output",
            str(output_path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert completed.stdout == ""
    record = json.loads(output_path.read_text(encoding="utf-8"))

    validate_l0_discovery_advisor_evaluation_record(record)
    assert record["run_id"] == "cli-evaluation"
    assert record["inputs"]["manifest_paths"] == [str(manifest_path)]
    assert record["aggregate"]["total_suggestions"] == 2
    assert record["aggregate"]["already_selected_suggestion_count"] == 1


def test_cli_prints_json_when_output_omitted(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest_record()), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_l0_discovery_advisor.py",
            "--manifest",
            str(manifest_path),
            "--run-id",
            "stdout-evaluation",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    record = json.loads(completed.stdout)

    validate_l0_discovery_advisor_evaluation_record(record)
    assert record["run_id"] == "stdout-evaluation"
    assert record["guardrails"]["automatic_include_l0"] is False
