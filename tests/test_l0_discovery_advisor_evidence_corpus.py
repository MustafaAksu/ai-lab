import json
import subprocess
import sys

import pytest

from ai_lab.documentation.l0_discovery_advisor_evidence_corpus import (
    CORPUS_ID,
    L0DiscoveryAdvisorEvidenceCorpusError,
    build_l0_discovery_advisor_evidence_manifest_records,
    validate_l0_discovery_advisor_evidence_corpus_record,
    write_l0_discovery_advisor_evidence_corpus,
)


def test_build_default_corpus_manifests_are_deterministic_and_diagnostic_only():
    manifests = build_l0_discovery_advisor_evidence_manifest_records(
        created_at="2026-07-07T00:00:00Z",
    )

    assert [manifest["manifest_id"] for manifest in manifests] == [
        f"corpus-expanded-{index + 1:02d}"
        for index in range(12)
    ]
    assert all(manifest["assembly_policy"] == "latest_context" for manifest in manifests)
    assert all(manifest["items"] for manifest in manifests)

    advisor = manifests[0]["diagnostics"]["l0_discovery_advisor"]
    assert advisor["selection_effect"] == "none"
    assert advisor["guardrails"]["automatic_include_l0"] is False
    assert advisor["guardrails"]["context_items_mutated"] == 0
    assert advisor["guardrails"]["provider_prompts_changed"] == 0
    assert all("diagnostics" in manifest for manifest in manifests)
    assert all(manifest["diagnostics"]["l0_discovery_advisor"]["selection_effect"] == "none" for manifest in manifests)


def test_write_evidence_corpus_records_expected_findings_and_guardrails(tmp_path):
    evidence = write_l0_discovery_advisor_evidence_corpus(
        output_root=tmp_path / "corpus",
        run_id="corpus-test",
        created_at="2026-07-07T00:00:00Z",
    )

    validate_l0_discovery_advisor_evidence_corpus_record(evidence)

    assert evidence["corpus_id"] == CORPUS_ID
    assert evidence["plan_id"] == "PLAN-20260707-0004"
    assert evidence["selection_effect"] == "none"
    assert evidence["contract"]["diagnostic_evidence_only"] is True
    assert evidence["contract"]["automatic_include_l0"] is False
    assert evidence["contract"]["mutates_context_manifest_items"] is False
    assert evidence["contract"]["changes_provider_prompts"] is False
    assert evidence["contract"]["live_retrieval"] is False
    assert evidence["contract"]["embedding_creation"] is False
    assert evidence["contract"]["index_mutation"] is False
    assert evidence["contract"]["memory_store_mutation"] is False
    assert evidence["contract"]["token_budget_telemetry"] is False
    assert evidence["contract"]["adapter_behavior"] is False

    assert evidence["findings"] == {
        "manifests_seen": 12,
        "manifests_with_advisor": 12,
        "manifests_missing_advisor": 0,
        "manifests_invalid_advisor": 0,
        "total_suggestions": 24,
        "unique_suggested_chunk_count": 24,
        "already_selected_suggestion_count": 0,
        "duplicate_suggestion_count": 0,
    }
    assert evidence["evaluation"]["aggregate"]["already_selected_suggestion_count"] == 0
    assert evidence["guardrails"]["context_items_mutated"] == 0
    assert evidence["guardrails"]["provider_prompts_changed"] == 0
    assert evidence["guardrails"]["automatic_include_l0"] is False
    assert evidence["guardrails"]["adapter_behavior"] is False


def test_write_evidence_corpus_writes_saved_manifests_and_evidence_json(tmp_path):
    output_root = tmp_path / "corpus"

    evidence = write_l0_discovery_advisor_evidence_corpus(
        output_root=output_root,
        run_id="write-test",
        created_at="2026-07-07T00:00:00Z",
    )

    evidence_path = output_root / "evidence.json"
    manifest_dir = output_root / "manifests"

    assert evidence_path.exists()
    assert manifest_dir.exists()
    assert len(list(manifest_dir.glob("*.json"))) == 12

    persisted = json.loads(evidence_path.read_text(encoding="utf-8"))
    validate_l0_discovery_advisor_evidence_corpus_record(persisted)
    assert persisted["run_id"] == "write-test"
    assert persisted["findings"] == evidence["findings"]
    assert all(path.startswith(str(manifest_dir)) for path in persisted["inputs"]["manifest_paths"])


def test_validator_rejects_automatic_include_l0_contract(tmp_path):
    evidence = write_l0_discovery_advisor_evidence_corpus(
        output_root=tmp_path / "corpus",
        run_id="bad-contract",
        created_at="2026-07-07T00:00:00Z",
    )
    evidence["contract"]["automatic_include_l0"] = True

    with pytest.raises(L0DiscoveryAdvisorEvidenceCorpusError, match="automatic_include_l0"):
        validate_l0_discovery_advisor_evidence_corpus_record(evidence)


def test_cli_writes_evidence_corpus(tmp_path):
    output_root = tmp_path / "corpus"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_l0_discovery_advisor_evidence_corpus.py",
            "--output-root",
            str(output_root),
            "--run-id",
            "cli-corpus",
            "--created-at",
            "2026-07-07T00:00:00Z",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    evidence = json.loads(completed.stdout)
    validate_l0_discovery_advisor_evidence_corpus_record(evidence)
    assert evidence["run_id"] == "cli-corpus"
    assert evidence["findings"]["manifests_seen"] == 12
    assert evidence["findings"]["manifests_invalid_advisor"] == 0
    assert (output_root / "evidence.json").exists()
    assert len(list((output_root / "manifests").glob("*.json"))) == 12
