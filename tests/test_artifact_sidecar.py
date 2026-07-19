import json
from pathlib import Path

import pytest

from ai_lab.documentation.artifact_sidecar import (
    PROFILE_CONCISE,
    PROFILE_RICH,
    SEMANTIC_FIELDS,
    SidecarError,
    assess_profile_compliance,
    assess_staleness,
    canonical_sidecar_json,
    sidecar_id_for,
    sidecar_relative_path,
    validate_sidecar_record,
)


def _source_fixture(tmp_path):
    source = tmp_path / "docs" / "comparisons" / "COMP-9999-fixture.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Fixture artifact\n\nSynthetic bounded fixture content.\n")
    import hashlib

    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    return "docs/comparisons/COMP-9999-fixture.md", digest


def _valid_rich(tmp_path):
    source_path, digest = _source_fixture(tmp_path)
    return {
        "schema_version": "v1",
        "sidecar_id": "COMP-9999::rich_immediate",
        "profile": PROFILE_RICH,
        "source_artifact_id": "COMP-9999",
        "source_path": source_path,
        "source_content_hash": digest,
        "source_repo_commit": "f" * 40,
        "generator": {
            "provider": "deterministic",
            "identity": "fixture-writer",
            "version": "v1",
        },
        "generated_at": "2026-07-19T00:00:00+00:00",
        "omitted_fields": [],
        "purpose": "Bounded fixture for contract validation.",
        "status": "synthetic",
        "key_claims": ["The contract validates this record."],
        "decisions": ["Use synthetic fixtures only."],
        "results": ["Validation passes."],
        "constraints": ["No production sidecars in this slice."],
        "risks": ["None; synthetic."],
        "dependencies": ["verification_outcome vocabulary"],
        "evidence_refs": ["docs/comparisons/COMP-9999-fixture.md"],
        "uncertainty": "None for a synthetic fixture.",
        "unresolved": [],
        "next_actions": [],
        "lineage": "Derived from COMP-9999 fixture content.",
    }


def test_valid_rich_sidecar_passes(tmp_path):
    validate_sidecar_record(_valid_rich(tmp_path))


def test_identity_and_path_are_deterministic():
    assert sidecar_id_for("COMP-9999", PROFILE_CONCISE) == "COMP-9999::concise_second_level"
    assert (
        sidecar_relative_path("COMP-9999", PROFILE_RICH)
        == "docs/sidecars/COMP-9999.rich_immediate.json"
    )


def test_canonical_serialization_is_stable(tmp_path):
    record = _valid_rich(tmp_path)
    a = canonical_sidecar_json(record)
    b = canonical_sidecar_json(json.loads(a))
    assert a == b
    assert a.endswith("\n")


def test_concise_omission_must_be_listed(tmp_path):
    record = _valid_rich(tmp_path)
    record["profile"] = PROFILE_CONCISE
    record["sidecar_id"] = "COMP-9999::concise_second_level"
    del record["decisions"]
    with pytest.raises(SidecarError):
        validate_sidecar_record(record)
    record["omitted_fields"] = ["decisions"]
    validate_sidecar_record(record)


def test_rich_profile_forbids_omission(tmp_path):
    record = _valid_rich(tmp_path)
    del record["decisions"]
    record["omitted_fields"] = ["decisions"]
    with pytest.raises(SidecarError):
        validate_sidecar_record(record)


def test_present_and_omitted_is_rejected(tmp_path):
    record = _valid_rich(tmp_path)
    record["profile"] = PROFILE_CONCISE
    record["sidecar_id"] = "COMP-9999::concise_second_level"
    record["omitted_fields"] = ["decisions"]
    with pytest.raises(SidecarError):
        validate_sidecar_record(record)


def test_generator_must_be_structured(tmp_path):
    record = _valid_rich(tmp_path)
    record["generator"] = "gpt-5"
    with pytest.raises(SidecarError):
        validate_sidecar_record(record)


def test_over_budget_is_finding_not_schema_failure(tmp_path):
    record = _valid_rich(tmp_path)
    record["key_claims"] = ["claim " + "x" * 5 for _ in range(400)]
    validate_sidecar_record(record)
    findings = assess_profile_compliance(record)
    assert any(f["code"] == "SIDECAR_OVER_TOKEN_HYPOTHESIS" for f in findings)


def test_staleness_verified_current(tmp_path):
    record = _valid_rich(tmp_path)
    result = assess_staleness(record, repo_root=tmp_path)
    assert result["verification_outcome"] == "verified_current"
    assert result["ok"] is True


def test_staleness_hash_mismatch_is_stale(tmp_path):
    record = _valid_rich(tmp_path)
    (tmp_path / record["source_path"]).write_text("changed content\n")
    result = assess_staleness(record, repo_root=tmp_path)
    assert result["verification_outcome"] == "stale"
    assert result["ok"] is False
    assert any(f["class"] == "drift" for f in result["findings"])


def test_staleness_missing_source_is_unverifiable(tmp_path):
    record = _valid_rich(tmp_path)
    (tmp_path / record["source_path"]).unlink()
    result = assess_staleness(record, repo_root=tmp_path)
    assert result["verification_outcome"] == "unverifiable"
    assert result["ok"] is False
    assert not any(f["severity"] == "error" for f in result["findings"])


def test_semantic_fields_cover_warrant_list():
    assert set(SEMANTIC_FIELDS) == {
        "purpose",
        "status",
        "key_claims",
        "decisions",
        "results",
        "constraints",
        "risks",
        "dependencies",
        "evidence_refs",
        "uncertainty",
        "unresolved",
        "next_actions",
        "lineage",
    }
