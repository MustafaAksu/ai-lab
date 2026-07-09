import json
from pathlib import Path

import pytest

from ai_lab.documentation.self_model import (
    SelfModelError,
    audit_self_model,
    file_sha256,
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


def test_audit_reports_content_hash_matches_for_seed_capability():
    result = audit_self_model(Path("."))

    assert any(
        finding["code"] == "SELF_MODEL_CONTENT_HASH_MATCH"
        and finding["severity"] == "info"
        for finding in result["findings"]
    )


def test_audit_warns_when_content_hash_is_missing(tmp_path):
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

    verification = read_json(Path("docs/self_model/verifications/VERIFY-20260705-0001.json"))
    verification["repo_commit"] = "0" * 40
    (ver_dir / "VERIFY-20260705-0001.json").write_text(
        json.dumps(verification),
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
            "id": "CADM-X",
            "path": "docs/memory/admissions/CADM-X.json",
            "role": "warrant",
        }
    ]
    (cap_dir / "CAP-0001.json").write_text(json.dumps(capability), encoding="utf-8")

    result = audit_self_model(tmp_path)

    assert any(
        finding["code"] == "SELF_MODEL_CONTENT_HASH_MISSING"
        and finding["severity"] == "warn"
        for finding in result["findings"]
    )


def test_audit_warns_when_content_hash_mismatches(tmp_path):
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

    source = mech_dir / "mechanism.py"
    source.write_text("pass\n", encoding="utf-8")
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

    verification = read_json(Path("docs/self_model/verifications/VERIFY-20260705-0001.json"))
    verification["repo_commit"] = "0" * 40
    (ver_dir / "VERIFY-20260705-0001.json").write_text(
        json.dumps(verification),
        encoding="utf-8",
    )

    capability = read_json(Path("docs/self_model/capabilities/CAP-0001.json"))
    capability["last_verified"]["repo_commit"] = "0" * 40
    capability["last_verified"]["verification_artifact"] = (
        "docs/self_model/verifications/VERIFY-20260705-0001.json"
    )
    capability["evidence"]["commits"] = [{"commit": "0" * 40, "role": "implementation"}]
    capability["evidence"]["files"] = [
        {
            "path": "src/mechanism.py",
            "role": "mechanism",
            "content_hash": "f" * 64,
        }
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

    assert any(
        finding["code"] == "SELF_MODEL_CONTENT_HASH_MISMATCH"
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



def test_refresh_capability_hashes_script_updates_null_hash(tmp_path):
    import subprocess
    import sys

    capability = read_json(Path("docs/self_model/capabilities/CAP-0001.json"))
    capability_path = tmp_path / "CAP-0001.json"
    capability["evidence"]["files"] = [
        {"path": "source.txt", "role": "mechanism", "content_hash": None}
    ]
    source = tmp_path / "source.txt"
    source.write_text("content\n", encoding="utf-8")
    capability_path.write_text(json.dumps(capability), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/refresh_capability_hashes.py",
            str(capability_path),
            "--repo-root",
            str(tmp_path),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    refreshed = read_json(capability_path)
    assert refreshed["evidence"]["files"][0]["content_hash"] == file_sha256(source)


def test_build_self_model_index_is_aggregation_only_for_seed_records():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-05T00:00:00+00:00",
    )

    assert index["schema_version"] == "v1"
    assert index["model_type"] == "self_model"
    assert index["generation_rule"] == "aggregation_only"
    assert index["active_capabilities"] == ["CAP-0001", "CAP-0002", "CAP-0003", "CAP-0004"]
    assert index["open_gaps"] == ["GAP-0002"]
    assert index["capability_counts"]["implemented"] == 4
    assert index["gap_counts"].get("open", 0) == 1
    assert index["gap_counts"]["closed"] == 1
    assert index["gap_counts"]["open"] == 1
    assert index["audit_summary"]["ok"] is True


def test_build_self_model_index_recommendations_are_copied_from_gaps():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-05T00:00:00+00:00",
    )

    assert index["recommended_next_targets"] == [
        {
            "source_field": "recommended_first_slice",
            "source_record": "GAP-0002",
            "target": read_json(
                Path("docs/self_model/gaps/GAP-0002.json")
            )["recommended_first_slice"],
        }
    ]


def test_build_self_model_index_risks_keep_source_pointers():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-05T00:00:00+00:00",
    )

    assert {
        "risk": "Capability may be overclaimed if future docs imply automatic retrieval.",
        "source_record": "CAP-0001",
        "source_field": "risks[0]",
    } in index["known_risks"]
    assert {
        "risk": (
            "If documentation says L0 is automatically retrieved, that would "
            "overstate current behavior."
        ),
        "source_record": "GAP-0001",
        "source_field": "risk",
    } in index["known_risks"]


def test_build_self_model_script_writes_index(tmp_path):
    import subprocess
    import sys

    output = tmp_path / "SELF_MODEL.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_self_model.py",
            "--repo-root",
            ".",
            "--output",
            str(output),
            "--generated-at",
            "2026-07-05T00:00:00+00:00",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["generated_at"] == "2026-07-05T00:00:00+00:00"
    assert data["generation_rule"] == "aggregation_only"
    assert data["active_capabilities"] == ["CAP-0001", "CAP-0002", "CAP-0003", "CAP-0004"]
    assert data["open_gaps"] == ["GAP-0002"]


def test_audit_self_model_index_seed_has_no_errors():
    from ai_lab.documentation.self_model import audit_self_model_index

    result = audit_self_model_index(Path("."))

    assert result["ok"] is True
    assert not [
        finding
        for finding in result["findings"]
        if finding["severity"] == "error"
    ]
    codes = {finding["code"] for finding in result["findings"]}
    assert codes & {
        "SELF_MODEL_INDEX_CONTENT_CURRENT",
        "SELF_MODEL_INDEX_SOURCE_RECORDS_CHANGED_CONTENT_CURRENT",
    }


def test_audit_self_model_index_detects_stale_content(tmp_path):
    from ai_lab.documentation.self_model import audit_self_model_index

    original = json.loads(Path("docs/self_model/SELF_MODEL.json").read_text())
    original["open_plans"] = ["PLAN-20260709-0001"]

    index_path = tmp_path / "SELF_MODEL.json"
    index_path.write_text(json.dumps(original), encoding="utf-8")

    result = audit_self_model_index(
        repo_root=Path("."),
        index_path=index_path,
    )

    assert result["ok"] is True
    assert any(
        finding["code"] == "SELF_MODEL_INDEX_CONTENT_STALE"
        and finding["severity"] == "warn"
        for finding in result["findings"]
    )


def test_audit_self_model_index_missing_file_is_error(tmp_path):
    from ai_lab.documentation.self_model import audit_self_model_index

    result = audit_self_model_index(
        repo_root=Path("."),
        index_path=tmp_path / "missing.json",
    )

    assert result["ok"] is False
    assert result["findings"] == [
        {
            "severity": "error",
            "code": "SELF_MODEL_INDEX_MISSING",
            "target": str(tmp_path / "missing.json"),
            "message": "SELF_MODEL.json is missing.",
        }
    ]


def test_audit_self_model_index_script_reports_json():
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_self_model_index.py",
            "--repo-root",
            ".",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    data = json.loads(result.stdout)
    assert data["schema_version"] == "v1"
    assert data["ok"] is True
    codes = {finding["code"] for finding in data["findings"]}
    assert codes & {
        "SELF_MODEL_INDEX_CONTENT_CURRENT",
        "SELF_MODEL_INDEX_SOURCE_RECORDS_CHANGED_CONTENT_CURRENT",
    }


def test_validate_plan_record_accepts_seed_plan():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_plan_record

    record = json.loads(
        Path("docs/self_model/plans/PLAN-20260705-0001.json").read_text(
            encoding="utf-8"
        )
    )

    validate_plan_record(record)


def test_validate_plan_record_rejects_invalid_plan_id():
    import pytest
    from ai_lab.documentation.self_model import SelfModelError, validate_plan_record

    record = {
        "schema_version": "v1",
        "plan_id": "PLAN-bad",
        "title": "Bad plan",
        "status": "completed",
        "created_at": "2026-07-05T00:00:00Z",
        "source_gap_id": "GAP-0001",
        "objective": "Objective.",
        "proposed_change": "Change.",
        "rationale": ["Because."],
        "constraints": ["Constraint."],
        "success_criteria": ["Success."],
        "risk": "Risk.",
        "next_action": "Next.",
    }

    with pytest.raises(SelfModelError, match="plan_id"):
        validate_plan_record(record)


def test_build_self_model_index_includes_plan_records():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-05T00:00:00+00:00",
    )

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index.get("plan_counts", {}).get("proposed", 0) == 1
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert {
        plan["plan_id"]
        for plan in index["plans"]
    } == {"PLAN-20260705-0001", "PLAN-20260706-0001", "PLAN-20260706-0002", "PLAN-20260706-0003", "PLAN-20260706-0004", "PLAN-20260707-0001", "PLAN-20260707-0002", "PLAN-20260707-0003", "PLAN-20260707-0004", "PLAN-20260709-0001", "PLAN-20260709-0002"}

    assert any(
        plan["plan_id"] == "PLAN-20260705-0001"
        and plan["title"] == "Read-only L0 candidate diagnostics"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0001"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260705-0001.json"
        for plan in index["plans"]
    )

    assert any(
        plan["plan_id"] == "PLAN-20260706-0001"
        and plan["title"] == "Context-manifest-connected L0 candidate diagnostics"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0001"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260706-0001.json"
        for plan in index["plans"]
    )
    assert {
        "risk": (
            "The diagnostic could be misread as automatic retrieval unless "
            "output labels remain explicit about read-only candidate reporting."
        ),
        "source_record": "PLAN-20260705-0001",
        "source_field": "risk",
    } in index["known_risks"]


def test_write_plan_record_script_writes_valid_record(tmp_path):
    import json
    import subprocess
    import sys

    output = tmp_path / "PLAN-20260705-9999.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/write_plan_record.py",
            "--plan-id",
            "PLAN-20260705-9999",
            "--title",
            "Test plan",
            "--status",
            "proposed",
            "--created-at",
            "2026-07-05T00:00:00Z",
            "--source-gap-id",
            "GAP-0001",
            "--objective",
            "Test objective.",
            "--proposed-change",
            "Test proposed change.",
            "--rationale",
            "Test rationale.",
            "--constraint",
            "Test constraint.",
            "--success-criterion",
            "Test success criterion.",
            "--risk",
            "Test risk.",
            "--next-action",
            "Test next action.",
            "--output",
            str(output),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["plan_id"] == "PLAN-20260705-9999"
    assert data["source_gap_id"] == "GAP-0001"


def test_validate_warrant_record_accepts_seed_warrant():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_warrant_record

    record = json.loads(
        Path("docs/self_model/warrants/WARR-20260705-0001.json").read_text(
            encoding="utf-8"
        )
    )

    validate_warrant_record(record)


def test_validate_warrant_record_rejects_invalid_target_type():
    import pytest
    from ai_lab.documentation.self_model import SelfModelError, validate_warrant_record

    record = {
        "schema_version": "v1",
        "warrant_id": "WARR-20260705-9999",
        "target_item_id": "PLAN-20260705-0001",
        "target_item_type": "context_admission",
        "decision": "admit",
        "warrant_state": "supported",
        "created_at": "2026-07-05T00:00:00Z",
        "author": "chatgpt",
        "substrate": "process",
        "reason": "Reason.",
        "scope": "Scope.",
        "evidence_ids": ["PLAN-20260705-0001"],
    }

    with pytest.raises(SelfModelError, match="target_item_type"):
        validate_warrant_record(record)


def test_build_self_model_index_includes_warrant_records():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-05T00:00:00+00:00",
    )

    assert index["warrant_counts"]["supported"] == 22
    assert index["admitted_plans"] == ["PLAN-20260705-0001", "PLAN-20260706-0001", "PLAN-20260706-0002", "PLAN-20260706-0003", "PLAN-20260706-0004", "PLAN-20260707-0001", "PLAN-20260707-0002", "PLAN-20260707-0003", "PLAN-20260707-0004", "PLAN-20260709-0001"]
    assert {
        warrant["warrant_id"]
        for warrant in index["warrants"]
    } == {"WARR-20260705-0001", "WARR-20260705-0002", "WARR-20260706-0001", "WARR-20260706-0002", "WARR-20260706-0003", "WARR-20260706-0004", "WARR-20260706-0005", "WARR-20260706-0006", "WARR-20260706-0007", "WARR-20260706-0008", "WARR-20260707-0001", "WARR-20260707-0002", "WARR-20260707-0003", "WARR-20260707-0004", "WARR-20260707-0005", "WARR-20260707-0006", "WARR-20260707-0007", "WARR-20260707-0008", "WARR-20260709-0001", "WARR-20260709-0002", "WARR-20260709-0003", "WARR-20260709-0004"}

    assert any(
        warrant["warrant_id"] == "WARR-20260705-0001"
        and warrant["target_item_id"] == "PLAN-20260705-0001"
        and warrant["target_item_type"] == "plan"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        and warrant["source_path"] == "docs/self_model/warrants/WARR-20260705-0001.json"
        for warrant in index["warrants"]
    )

    assert any(
        warrant["warrant_id"] == "WARR-20260705-0002"
        and warrant["target_item_id"] == "PLAN-20260705-0001"
        and warrant["target_item_type"] == "plan"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        and warrant["source_path"] == "docs/self_model/warrants/WARR-20260705-0002.json"
        for warrant in index["warrants"]
    )


def test_write_warrant_record_script_writes_valid_record(tmp_path):
    import json
    import subprocess
    import sys

    output = tmp_path / "WARR-20260705-9999.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/write_warrant_record.py",
            "--warrant-id",
            "WARR-20260705-9999",
            "--target-item-id",
            "PLAN-20260705-0001",
            "--target-item-type",
            "plan",
            "--decision",
            "admit",
            "--warrant-state",
            "supported",
            "--created-at",
            "2026-07-05T00:00:00Z",
            "--author",
            "chatgpt",
            "--substrate",
            "process",
            "--reason",
            "Reason.",
            "--scope",
            "Scope.",
            "--evidence-id",
            "PLAN-20260705-0001",
            "--output",
            str(output),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["warrant_id"] == "WARR-20260705-9999"
    assert data["target_item_type"] == "plan"
    assert data["decision"] == "admit"

def test_validate_capability_record_accepts_cap_0002():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_capability_record

    record = json.loads(
        Path("docs/self_model/capabilities/CAP-0002.json").read_text(
            encoding="utf-8"
        )
    )

    validate_capability_record(record)


def test_validate_verification_record_accepts_verify_0002():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_verification_record

    record = json.loads(
        Path("docs/self_model/verifications/VERIFY-20260705-0002.json").read_text(
            encoding="utf-8"
        )
    )

    validate_verification_record(record)


def test_build_self_model_index_includes_cap_0002():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-05T00:00:00+00:00",
    )

    assert "CAP-0002" in index["active_capabilities"]
    assert any(
        capability["capability_id"] == "CAP-0002"
        and capability["status"] == "implemented"
        for capability in index["capabilities"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260705-0002"
        for verification in index["verifications"]
    )


def test_validate_warrant_record_accepts_warr_0002():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_warrant_record

    record = json.loads(
        Path("docs/self_model/warrants/WARR-20260705-0002.json").read_text(
            encoding="utf-8"
        )
    )

    validate_warrant_record(record)


def test_build_self_model_index_includes_completion_warrant():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-05T00:00:00+00:00",
    )

    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260705-0002"
        and warrant["target_item_id"] == "PLAN-20260705-0001"
        and warrant["target_item_type"] == "plan"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )


def test_validate_plan_record_accepts_completed_plan_0001():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_plan_record

    record = json.loads(
        Path("docs/self_model/plans/PLAN-20260705-0001.json").read_text(
            encoding="utf-8"
        )
    )

    assert record["status"] == "completed"
    validate_plan_record(record)


def test_build_self_model_index_excludes_completed_plan_from_open_plans():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-05T00:00:00+00:00",
    )

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index.get("plan_counts", {}).get("proposed", 0) == 1
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert any(
        plan["plan_id"] == "PLAN-20260705-0001"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )


def test_validate_plan_record_accepts_plan_20260706_0001():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_plan_record

    record = json.loads(
        Path("docs/self_model/plans/PLAN-20260706-0001.json").read_text(
            encoding="utf-8"
        )
    )

    assert record["status"] == "completed"
    validate_plan_record(record)


def test_build_self_model_index_includes_plan_20260706_0001():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-06T00:00:00+00:00",
    )

    assert "PLAN-20260706-0001" not in index["open_plans"]
    assert any(
        plan["plan_id"] == "PLAN-20260706-0001"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0001"
        for plan in index["plans"]
    )


def test_validate_warrant_record_accepts_warr_20260706_0001():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_warrant_record

    record = json.loads(
        Path("docs/self_model/warrants/WARR-20260706-0001.json").read_text(
            encoding="utf-8"
        )
    )

    validate_warrant_record(record)


def test_build_self_model_index_admits_plan_20260706_0001():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-06T00:00:00+00:00",
    )

    assert "PLAN-20260706-0001" not in index["open_plans"]
    assert "PLAN-20260706-0001" in index["admitted_plans"]
    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260706-0001"
        and warrant["target_item_id"] == "PLAN-20260706-0001"
        and warrant["target_item_type"] == "plan"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )


def test_validate_verification_record_accepts_verify_20260706_0001():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_verification_record

    record = json.loads(
        Path("docs/self_model/verifications/VERIFY-20260706-0001.json").read_text(
            encoding="utf-8"
        )
    )

    validate_verification_record(record)


def test_validate_warrant_record_accepts_warr_20260706_0002():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_warrant_record

    record = json.loads(
        Path("docs/self_model/warrants/WARR-20260706-0002.json").read_text(
            encoding="utf-8"
        )
    )

    validate_warrant_record(record)


def test_build_self_model_index_marks_plan_20260706_0001_completed():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(
        Path("."),
        generated_at="2026-07-06T00:00:00+00:00",
    )

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert "PLAN-20260706-0001" in index["admitted_plans"]
    assert index["warrant_counts"]["supported"] == 22
    assert any(
        plan["plan_id"] == "PLAN-20260706-0001"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260706-0001"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260706-0002"
        and warrant["target_item_id"] == "PLAN-20260706-0001"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )


def test_validate_plan_20260706_0002_record():
    from ai_lab.documentation.self_model import validate_plan_record

    validate_plan_record(
        read_json(Path("docs/self_model/plans/PLAN-20260706-0002.json"))
    )


def test_build_self_model_index_includes_plan_20260706_0002():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"].get("proposed", 0) == 1
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert any(
        plan["plan_id"] == "PLAN-20260706-0002"
        and plan["status"] == "completed"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260706-0002.json"
        for plan in index["plans"]
    )


def test_validate_warrant_20260706_0003_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    validate_warrant_record(
        read_json(Path("docs/self_model/warrants/WARR-20260706-0003.json"))
    )


def test_build_self_model_index_admits_plan_20260706_0002():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "PLAN-20260706-0002" in index["admitted_plans"]
    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260706-0003"
        and warrant["target_item_id"] == "PLAN-20260706-0002"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )

def test_validate_capability_0003_record():
    from ai_lab.documentation.self_model import validate_capability_record

    validate_capability_record(
        read_json(Path("docs/self_model/capabilities/CAP-0003.json"))
    )


def test_validate_verification_record_accepts_verify_20260706_0002():
    from ai_lab.documentation.self_model import validate_verification_record

    validate_verification_record(
        read_json(Path("docs/self_model/verifications/VERIFY-20260706-0002.json"))
    )


def test_build_self_model_index_includes_cap_0003_and_verify_20260706_0002():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["capability_counts"]["implemented"] == 4
    assert "CAP-0003" in index["active_capabilities"]
    assert any(
        capability["capability_id"] == "CAP-0003"
        and capability["status"] == "implemented"
        and capability["source_path"] == "docs/self_model/capabilities/CAP-0003.json"
        for capability in index["capabilities"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260706-0002"
        and verification["repo_commit"] == "be78851e53916d009817fd2436817a9da9fb1ab8"
        for verification in index["verifications"]
    )

def test_validate_warrant_20260706_0004_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    validate_warrant_record(
        read_json(Path("docs/self_model/warrants/WARR-20260706-0004.json"))
    )


def test_build_self_model_index_marks_plan_20260706_0002_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert "PLAN-20260706-0002" in index["admitted_plans"]
    assert index["warrant_counts"]["supported"] == 22
    assert any(
        plan["plan_id"] == "PLAN-20260706-0002"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260706-0004"
        and warrant["target_item_id"] == "PLAN-20260706-0002"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )

def test_validate_plan_20260706_0003_record():
    from ai_lab.documentation.self_model import validate_plan_record

    validate_plan_record(
        read_json(Path("docs/self_model/plans/PLAN-20260706-0003.json"))
    )


def test_build_self_model_index_includes_plan_20260706_0003():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["plan_counts"].get("proposed", 0) == 1
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert any(
        plan["plan_id"] == "PLAN-20260706-0003"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0001"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260706-0003.json"
        for plan in index["plans"]
    )

def test_validate_warr_20260706_0005_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    validate_warrant_record(
        read_json(Path("docs/self_model/warrants/WARR-20260706-0005.json"))
    )


def test_build_self_model_index_includes_warr_20260706_0005_admission():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["plan_counts"].get("proposed", 0) == 1
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert "PLAN-20260706-0003" in index["admitted_plans"]
    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260706-0005"
        and warrant["target_item_id"] == "PLAN-20260706-0003"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        and warrant["source_path"] == "docs/self_model/warrants/WARR-20260706-0005.json"
        for warrant in index["warrants"]
    )

def test_validate_cap_0004_record():
    from ai_lab.documentation.self_model import validate_capability_record

    validate_capability_record(
        read_json(Path("docs/self_model/capabilities/CAP-0004.json"))
    )


def test_validate_verify_20260706_0003_record():
    from ai_lab.documentation.self_model import validate_verification_record

    validate_verification_record(
        read_json(Path("docs/self_model/verifications/VERIFY-20260706-0003.json"))
    )


def test_build_self_model_index_includes_cap_0004():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["capability_counts"]["implemented"] == 4
    assert index["active_capabilities"] == [
        "CAP-0001",
        "CAP-0002",
        "CAP-0003",
        "CAP-0004",
    ]
    assert any(
        capability["capability_id"] == "CAP-0004"
        and capability["status"] == "implemented"
        and capability["source_path"] == "docs/self_model/capabilities/CAP-0004.json"
        for capability in index["capabilities"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260706-0003"
        and verification["source_path"] == "docs/self_model/verifications/VERIFY-20260706-0003.json"
        for verification in index["verifications"]
    )

def test_validate_warr_20260706_0006_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    validate_warrant_record(
        read_json(Path("docs/self_model/warrants/WARR-20260706-0006.json"))
    )


def test_build_self_model_index_records_plan_20260706_0003_completion():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert "PLAN-20260706-0003" in index["admitted_plans"]
    assert index["warrant_counts"]["supported"] == 22
    assert any(
        plan["plan_id"] == "PLAN-20260706-0003"
        and plan["status"] == "completed"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260706-0003.json"
        for plan in index["plans"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260706-0006"
        and warrant["target_item_id"] == "PLAN-20260706-0003"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        and warrant["source_path"] == "docs/self_model/warrants/WARR-20260706-0006.json"
        for warrant in index["warrants"]
    )


def test_validate_plan_20260706_0004_record():
    from ai_lab.documentation.self_model import validate_plan_record

    validate_plan_record(
        read_json(Path("docs/self_model/plans/PLAN-20260706-0004.json"))
    )


def test_build_self_model_index_records_plan_20260706_0004_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index.get("plan_counts", {}).get("proposed", 0) == 1
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert "PLAN-20260706-0004" in index["admitted_plans"]
    assert index["capability_counts"]["implemented"] == 4
    assert any(
        plan["plan_id"] == "PLAN-20260706-0004"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0001"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260706-0004.json"
        and plan["title"] == "Context-manifest-connected L0 Discovery Advisor Diagnostics"
        for plan in index["plans"]
    )

def test_validate_warr_20260706_0007_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    validate_warrant_record(
        read_json(Path("docs/self_model/warrants/WARR-20260706-0007.json"))
    )


def test_build_self_model_index_includes_warr_20260706_0007_admission():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index.get("plan_counts", {}).get("proposed", 0) == 1
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert "PLAN-20260706-0004" in index["admitted_plans"]
    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260706-0007"
        and warrant["target_item_id"] == "PLAN-20260706-0004"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        and warrant["source_path"] == "docs/self_model/warrants/WARR-20260706-0007.json"
        for warrant in index["warrants"]
    )

def test_validate_plan_record_accepts_plan_20260707_0001_completed():
    from ai_lab.documentation.self_model import read_json, validate_plan_record

    record = read_json(Path("docs/self_model/plans/PLAN-20260707-0001.json"))
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260707-0001"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0001"
    assert record["title"] == "Evaluate Manifest-Connected L0 Discovery Advisor Diagnostics"


def test_build_self_model_index_records_plan_20260707_0001_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("proposed", 0) == 1
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert "PLAN-20260707-0001" in index["admitted_plans"]
    assert any(
        plan["plan_id"] == "PLAN-20260707-0001"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0001"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260707-0001.json"
        and plan["title"] == "Evaluate Manifest-Connected L0 Discovery Advisor Diagnostics"
        for plan in index["plans"]
    )

def test_build_self_model_index_records_warrant_20260707_0001_for_plan_20260707_0001():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260707-0001"
        and warrant["target_item_id"] == "PLAN-20260707-0001"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )

def test_build_self_model_index_records_warrant_20260707_0002_for_plan_20260707_0001_completion():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260707-0002"
        and warrant["target_item_id"] == "PLAN-20260707-0001"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )

def test_validate_plan_record_accepts_plan_20260707_0002_completed():
    import json
    from pathlib import Path

    from ai_lab.documentation.self_model import validate_plan_record

    record = json.loads(
        Path("docs/self_model/plans/PLAN-20260707-0002.json").read_text(
            encoding="utf-8"
        )
    )

    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260707-0002"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0001"


def test_build_self_model_index_records_plan_20260707_0002_completed():
    from pathlib import Path

    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("proposed", 0) == 1
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert any(
        plan["plan_id"] == "PLAN-20260707-0002"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0001"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260707-0002.json"
        for plan in index["plans"]
    )

def test_build_self_model_index_records_warrant_20260707_0003_for_plan_20260707_0002_admission():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260707-0003"
        and warrant["target_item_id"] == "PLAN-20260707-0002"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )


def test_build_self_model_index_records_plan_20260707_0002_completion_artifacts():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert any(
        plan["plan_id"] == "PLAN-20260707-0002"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260707-0004"
        and warrant["target_item_id"] == "PLAN-20260707-0002"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260707-0002"
        for verification in index["verifications"]
    )

def test_validate_plan_record_accepts_plan_20260707_0003_completed():
    import json
    from pathlib import Path

    from ai_lab.documentation.self_model import validate_plan_record

    record = json.loads(
        Path("docs/self_model/plans/PLAN-20260707-0003.json").read_text(
            encoding="utf-8"
        )
    )

    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260707-0003"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0001"
    assert record["completion_verification_id"] == "VERIFY-20260707-0003"
    assert record["completion_warrant_id"] == "WARR-20260707-0006"


def test_build_self_model_index_records_plan_20260707_0003_as_completed():
    from pathlib import Path

    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("proposed", 0) == 1
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert any(
        plan["plan_id"] == "PLAN-20260707-0003"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0001"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260707-0003.json"
        for plan in index["plans"]
    )


def test_build_self_model_index_records_warrant_20260707_0005_for_plan_20260707_0003_admission():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260707-0005"
        and warrant["target_item_id"] == "PLAN-20260707-0003"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )


def test_build_self_model_index_records_verification_20260707_0003_for_threshold_completion():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert len(index["verifications"]) == 11
    assert any(
        verification["verification_id"] == "VERIFY-20260707-0003"
        and verification["source_path"]
        == "docs/self_model/verifications/VERIFY-20260707-0003.json"
        for verification in index["verifications"]
    )


def test_build_self_model_index_records_warrant_20260707_0006_for_threshold_completion():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["warrant_counts"]["supported"] == 22
    assert any(
        warrant["warrant_id"] == "WARR-20260707-0006"
        and warrant["target_item_id"] == "PLAN-20260707-0003"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )


def test_validate_plan_record_accepts_plan_20260707_0004_completed():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_plan_record

    record = json.loads(Path("docs/self_model/plans/PLAN-20260707-0004.json").read_text())
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260707-0004"
    assert record["status"] == "completed"
    assert record["admission_warrant_id"] == "WARR-20260707-0007"
    assert record["completion_verification_id"] == "VERIFY-20260707-0004"
    assert record["completion_warrant_id"] == "WARR-20260707-0008"


def test_build_self_model_index_records_plan_20260707_0004_as_completed():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"].get("proposed", 0) == 1
    assert index["plan_counts"]["completed"] == 10
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert "PLAN-20260707-0004" not in index["open_plans"]
    assert index["open_gaps"] == ["GAP-0002"]


def test_build_self_model_index_records_warrant_20260707_0007_for_plan_20260707_0004_admission():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        warrant["warrant_id"] == "WARR-20260707-0007"
        and warrant["decision"] == "admit"
        and warrant["source_path"] == "docs/self_model/warrants/WARR-20260707-0007.json"
        for warrant in index["warrants"]
    )

    raw = json.loads(Path("docs/self_model/warrants/WARR-20260707-0007.json").read_text())
    assert raw["target_id"] == "PLAN-20260707-0004"
    assert raw["decision"] == "admit"


def test_validate_plan_record_accepts_plan_20260709_0001_completed():
    import json
    from pathlib import Path
    from ai_lab.documentation.self_model import validate_plan_record

    record = json.loads(Path("docs/self_model/plans/PLAN-20260709-0001.json").read_text())
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260709-0001"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0001"
    assert record["admission_warrant_id"] == "WARR-20260709-0001"
    assert "Do not make automatic include_l0 default-on." in record["non_goals"]


def test_build_self_model_index_records_plan_20260709_0001_as_completed():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"].get("proposed", 0) == 1
    assert index["plan_counts"].get("admitted", 0) == 0
    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert index["open_gaps"] == ["GAP-0002"]


def test_build_self_model_index_records_warrant_20260709_0001_for_runtime_inclusion_admission():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["warrant_counts"]["supported"] == 22
    assert "PLAN-20260709-0001" in index["admitted_plans"]
    assert any(
        warrant["warrant_id"] == "WARR-20260709-0001"
        and warrant["target_item_id"] == "PLAN-20260709-0001"
        for warrant in index["warrants"]
    )


def test_validate_gap_0002_record():
    from ai_lab.documentation.self_model import validate_gap_record

    record = read_json(Path("docs/self_model/gaps/GAP-0002.json"))
    validate_gap_record(record)

    assert record["gap_id"] == "GAP-0002"
    assert record["status"] == "open"
    assert record["category"] == "memory_context"


def test_validate_warr_20260709_0004_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260709-0004.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260709-0004"
    assert record["target_item_id"] == "GAP-0002"
    assert record["target_item_type"] == "gap"


def test_build_self_model_index_records_gap_0002_open():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["open_gaps"] == ["GAP-0002"]
    assert index["gap_counts"]["closed"] == 1
    assert index["gap_counts"]["open"] == 1
    assert any(
        gap["gap_id"] == "GAP-0002"
        and gap["status"] == "open"
        and gap["category"] == "memory_context"
        and gap["source_path"] == "docs/self_model/gaps/GAP-0002.json"
        for gap in index["gaps"]
    )
    assert any(
        item["source_record"] == "GAP-0002"
        and item["source_field"] == "recommended_first_slice"
        for item in index["recommended_next_targets"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260709-0004"
        and warrant["target_item_id"] == "GAP-0002"
        and warrant["target_item_type"] == "gap"
        for warrant in index["warrants"]
    )


def test_validate_plan_20260709_0002_record():
    from ai_lab.documentation.self_model import validate_plan_record

    record = read_json(Path("docs/self_model/plans/PLAN-20260709-0002.json"))
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260709-0002"
    assert record["status"] == "proposed"
    assert record["source_gap_id"] == "GAP-0002"


def test_build_self_model_index_records_plan_20260709_0002_open():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert index["open_plans"] == ["PLAN-20260709-0002"]
    assert index["plan_counts"]["completed"] == 10
    assert index["plan_counts"]["proposed"] == 1
    assert any(
        plan["plan_id"] == "PLAN-20260709-0002"
        and plan["status"] == "proposed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260709-0002.json"
        for plan in index["plans"]
    )
