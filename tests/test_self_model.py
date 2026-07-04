import json
from pathlib import Path

import pytest

from ai_lab.documentation.self_model import (
    SelfModelError,
    audit_self_model,
    read_json,
    validate_capability_record,
    validate_gap_record,
    validate_verification_record,
)


def test_seed_self_model_records_validate():
    validate_capability_record(
        read_json(Path("docs/self_model/capabilities/CAP-0001.json"))
    )
    validate_gap_record(read_json(Path("docs/self_model/gaps/GAP-0001.json")))
    validate_verification_record(
        read_json(Path("docs/self_model/verifications/VERIFY-20260705-0001.json"))
    )


def test_capability_requires_full_commit_hash():
    record = read_json(Path("docs/self_model/capabilities/CAP-0001.json"))
    record["evidence"]["commits"][0]["commit"] = "2ba4d78"

    with pytest.raises(SelfModelError, match="full 40-character"):
        validate_capability_record(record)


def test_verification_requires_recorded_by():
    record = read_json(Path("docs/self_model/verifications/VERIFY-20260705-0001.json"))
    record.pop("recorded_by")

    with pytest.raises(SelfModelError, match=r"\$\.recorded_by must be an object"):
        validate_verification_record(record)


def test_audit_seed_self_model_has_no_errors():
    result = audit_self_model(Path("."))

    assert result["schema_version"] == "v1"
    assert result["ok"] is True
    assert not [
        finding
        for finding in result["findings"]
        if finding["severity"] == "error"
    ]


def test_audit_warns_when_content_hash_is_missing():
    result = audit_self_model(Path("."))

    assert any(
        finding["code"] == "SELF_MODEL_CONTENT_HASH_MISSING"
        and finding["severity"] == "warn"
        for finding in result["findings"]
    )


def test_audit_errors_when_capability_evidence_path_is_missing(tmp_path):
    cap_dir = tmp_path / "docs" / "self_model" / "capabilities"
    ver_dir = tmp_path / "docs" / "self_model" / "verifications"
    mem_dir = tmp_path / "docs" / "memory" / "l1"
    adm_dir = tmp_path / "docs" / "memory" / "admissions"

    cap_dir.mkdir(parents=True)
    ver_dir.mkdir(parents=True)
    mem_dir.mkdir(parents=True)
    adm_dir.mkdir(parents=True)

    verification = read_json(Path("docs/self_model/verifications/VERIFY-20260705-0001.json"))
    verification["repo_commit"] = "0" * 40
    (ver_dir / "VERIFY-20260705-0001.json").write_text(
        json.dumps(verification),
        encoding="utf-8",
    )

    (mem_dir / "L1-X.json").write_text("{}", encoding="utf-8")
    (adm_dir / "CADM-X.json").write_text(
        json.dumps(
            {
                "verdict_id": "CADM-X",
                "target_item_id": "L1-X",
                "decision": "admit",
                "created_at": "2026-07-05T00:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    capability = read_json(Path("docs/self_model/capabilities/CAP-0001.json"))
    capability["last_verified"]["repo_commit"] = "0" * 40
    capability["last_verified"]["verification_artifact"] = (
        "docs/self_model/verifications/VERIFY-20260705-0001.json"
    )
    capability["evidence"]["commits"] = [{"commit": "0" * 40, "role": "implementation"}]
    capability["evidence"]["files"] = [
        {"path": "missing.py", "role": "mechanism", "content_hash": None}
    ]
    capability["evidence"]["memory_records"] = [
        {"id": "L1-X", "path": "docs/memory/l1/L1-X.json", "role": "summary"}
    ]
    capability["evidence"]["admissions"] = [
        {
            "id": "CADM-X",
            "path": "docs/memory/admissions/CADM-X.json",
            "role": "warrant",
        }
    ]
    (cap_dir / "CAP-0001.json").write_text(json.dumps(capability), encoding="utf-8")

    result = audit_self_model(tmp_path)

    assert result["ok"] is False
    assert any(
        finding["code"] == "SELF_MODEL_EVIDENCE_PATH_MISSING"
        for finding in result["findings"]
    )


def test_audit_warns_when_latest_warrant_is_not_admitting(tmp_path):
    cap_dir = tmp_path / "docs" / "self_model" / "capabilities"
    ver_dir = tmp_path / "docs" / "self_model" / "verifications"
    mech_dir = tmp_path / "src"
    mem_dir = tmp_path / "docs" / "memory" / "l1"
    adm_dir = tmp_path / "docs" / "memory" / "admissions"

    cap_dir.mkdir(parents=True)
    ver_dir.mkdir(parents=True)
    mech_dir.mkdir(parents=True)
    mem_dir.mkdir(parents=True)
    adm_dir.mkdir(parents=True)

    (mech_dir / "mechanism.py").write_text("pass\n", encoding="utf-8")
    (mem_dir / "L1-X.json").write_text("{}", encoding="utf-8")

    verification = read_json(Path("docs/self_model/verifications/VERIFY-20260705-0001.json"))
    verification["repo_commit"] = "0" * 40
    (ver_dir / "VERIFY-20260705-0001.json").write_text(
        json.dumps(verification),
        encoding="utf-8",
    )

    (adm_dir / "CADM-OLD.json").write_text(
        json.dumps(
            {
                "verdict_id": "CADM-OLD",
                "target_item_id": "L1-X",
                "decision": "admit",
                "created_at": "2026-07-05T00:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )
    (adm_dir / "CADM-NEW.json").write_text(
        json.dumps(
            {
                "verdict_id": "CADM-NEW",
                "target_item_id": "L1-X",
                "decision": "reject",
                "created_at": "2026-07-05T00:01:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    capability = read_json(Path("docs/self_model/capabilities/CAP-0001.json"))
    capability["last_verified"]["repo_commit"] = "0" * 40
    capability["last_verified"]["verification_artifact"] = (
        "docs/self_model/verifications/VERIFY-20260705-0001.json"
    )
    capability["evidence"]["commits"] = [{"commit": "0" * 40, "role": "implementation"}]
    capability["evidence"]["files"] = [
        {"path": "src/mechanism.py", "role": "mechanism", "content_hash": None}
    ]
    capability["evidence"]["memory_records"] = [
        {"id": "L1-X", "path": "docs/memory/l1/L1-X.json", "role": "summary"}
    ]
    capability["evidence"]["admissions"] = [
        {
            "id": "CADM-OLD",
            "path": "docs/memory/admissions/CADM-OLD.json",
            "role": "warrant",
        }
    ]
    (cap_dir / "CAP-0001.json").write_text(json.dumps(capability), encoding="utf-8")

    result = audit_self_model(tmp_path)

    assert any(
        finding["code"] == "SELF_MODEL_WARRANT_NOT_ADMITTING"
        and finding["severity"] == "warn"
        for finding in result["findings"]
    )
