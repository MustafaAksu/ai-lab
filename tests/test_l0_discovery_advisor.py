import json
import subprocess
import sys
from pathlib import Path

import pytest

from ai_lab.documentation.l0_discovery_advisor import (
    ADVISOR_ID,
    CANONICAL_SECTION_PATH,
    L0DiscoveryAdvisorError,
    build_l0_discovery_advisor_record,
    l0_discovery_advisor_manifest_document,
    validate_l0_discovery_advisor_record,
)


def simulator_record():
    return {
        "schema_version": "v1",
        "simulator_id": "l0_hybrid_retrieval_simulator.v1",
        "selection_effect": "none",
        "candidates": [
            {
                "cid": "L0-ALPHA",
                "retrieval_score": 0.91,
                "match_reason": "high hybrid score",
                "selection_effect": "none",
            },
            {
                "cid": "L0-BETA",
                "retrieval_score": 0.52,
                "match_reason": "moderate hybrid score",
                "selection_effect": "none",
            },
        ],
        "guardrails": {
            "side_effects_blocked": True,
            "writes_performed": 0,
            "index_mutations": 0,
            "embedding_creations": 0,
        },
    }


def candidate_diagnostics_record():
    return {
        "candidates": [
            {
                "chunk_id": "L0-BETA",
                "score": 0.61,
                "reason": "candidate diagnostic overlap",
            },
            {
                "chunk_id": "L0-GAMMA",
                "score": 0.42,
                "reason": "candidate diagnostic fallback",
            },
        ]
    }


def test_build_advisor_record_is_advisory_only_and_ranked():
    record = build_l0_discovery_advisor_record(
        selected_context_item_ids=["CTX-1", "CTX-1"],
        retrieval_simulator_records=[simulator_record()],
        candidate_diagnostics_records=[candidate_diagnostics_record()],
        retrieval_simulator_paths=["simulator.json"],
        candidate_diagnostics_paths=["diagnostics.json"],
        run_id="advisor-test",
        created_at="2026-07-06T00:00:00Z",
    )

    validate_l0_discovery_advisor_record(record)

    assert record["advisor_id"] == ADVISOR_ID
    assert record["canonical_path"] == CANONICAL_SECTION_PATH
    assert record["selection_effect"] == "none"
    assert record["contract"]["advisory_only"] is True
    assert record["contract"]["automatic_include_l0"] is False
    assert record["contract"]["changes_provider_prompts"] is False
    assert record["guardrails"]["writes_performed"] == 0
    assert record["guardrails"]["context_items_mutated"] == 0
    assert record["guardrails"]["provider_prompts_changed"] == 0
    assert record["guardrails"]["automatic_include_l0"] is False

    assert [item["chunk_id"] for item in record["suggestions"]] == [
        "L0-ALPHA",
        "L0-BETA",
        "L0-GAMMA",
    ]
    assert [item["rank"] for item in record["suggestions"]] == [1, 2, 3]
    assert all(item["selection_effect"] == "none" for item in record["suggestions"])
    assert all(
        item["suggested_include_l0_arg"] == item["chunk_id"]
        for item in record["suggestions"]
    )

    beta = next(item for item in record["suggestions"] if item["chunk_id"] == "L0-BETA")
    assert beta["suggestion_score"] == 0.61
    assert {ref["source"] for ref in beta["source_diagnostic_refs"]} == {
        "l0_retrieval_simulator",
        "l0_candidate_diagnostics",
    }


def test_manifest_document_uses_only_diagnostics_path():
    record = build_l0_discovery_advisor_record(
        retrieval_simulator_records=[simulator_record()],
        max_suggestions=1,
        run_id="advisor-test",
        created_at="2026-07-06T00:00:00Z",
    )

    document = l0_discovery_advisor_manifest_document(record)

    assert document == {
        "manifest": {
            "diagnostics": {
                "l0_discovery_advisor": record,
            }
        }
    }
    assert "items" not in document["manifest"]
    assert "context_pack" not in document


def test_max_suggestions_zero_is_valid_and_advisory():
    record = build_l0_discovery_advisor_record(
        retrieval_simulator_records=[simulator_record()],
        max_suggestions=0,
        run_id="advisor-test",
        created_at="2026-07-06T00:00:00Z",
    )

    validate_l0_discovery_advisor_record(record)

    assert record["suggestions"] == []
    assert record["inputs"]["source_counts"]["candidate_entries_seen"] == 2
    assert record["guardrails"]["automatic_include_l0"] is False


def test_validator_rejects_selection_effect_mutation():
    record = build_l0_discovery_advisor_record(
        retrieval_simulator_records=[simulator_record()],
        run_id="advisor-test",
        created_at="2026-07-06T00:00:00Z",
    )
    record["suggestions"][0]["selection_effect"] = "include"

    with pytest.raises(L0DiscoveryAdvisorError, match="selection_effect"):
        validate_l0_discovery_advisor_record(record)


def test_validator_rejects_write_guardrail_violation():
    record = build_l0_discovery_advisor_record(
        retrieval_simulator_records=[simulator_record()],
        run_id="advisor-test",
        created_at="2026-07-06T00:00:00Z",
    )
    record["guardrails"]["writes_performed"] = 1

    with pytest.raises(L0DiscoveryAdvisorError, match="writes_performed"):
        validate_l0_discovery_advisor_record(record)


def test_cli_writes_manifest_diagnostics_document(tmp_path):
    simulator_path = tmp_path / "simulator.json"
    output_path = tmp_path / "advisor.json"
    simulator_path.write_text(json.dumps(simulator_record()), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/advise_l0_discovery.py",
            "--retrieval-simulator",
            str(simulator_path),
            "--selected-context-item",
            "CTX-1",
            "--max-suggestions",
            "1",
            "--run-id",
            "cli-test",
            "--output",
            str(output_path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert completed.stdout == ""
    document = json.loads(output_path.read_text(encoding="utf-8"))
    record = document["manifest"]["diagnostics"]["l0_discovery_advisor"]

    validate_l0_discovery_advisor_record(record)
    assert record["run_id"] == "cli-test"
    assert record["inputs"]["selected_context_item_ids"] == ["CTX-1"]
    assert [item["chunk_id"] for item in record["suggestions"]] == ["L0-ALPHA"]


def test_cli_prints_json_when_output_omitted(tmp_path):
    simulator_path = tmp_path / "simulator.json"
    simulator_path.write_text(json.dumps(simulator_record()), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/advise_l0_discovery.py",
            "--retrieval-simulator",
            str(simulator_path),
            "--run-id",
            "stdout-test",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    document = json.loads(completed.stdout)
    record = document["manifest"]["diagnostics"]["l0_discovery_advisor"]

    validate_l0_discovery_advisor_record(record)
    assert record["run_id"] == "stdout-test"
