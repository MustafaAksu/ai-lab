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
        },
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
    original["open_plans"] = ["PLAN-20260709-0001", "PLAN-20260709-0002"]

    index_path = tmp_path / "SELF_MODEL.json"
    index_path.write_text(json.dumps(original), encoding="utf-8")

    result = audit_self_model_index(
        repo_root=Path("."),
        index_path=index_path,
    )

    assert result["ok"] is False
    assert any(
        finding["code"] == "SELF_MODEL_INDEX_CONTENT_STALE"
        and finding["severity"] == "error"
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

    assert "PLAN-20260706-0001" in index["admitted_plans"]
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

    assert "PLAN-20260706-0002" in index["admitted_plans"]
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

    assert "PLAN-20260706-0003" in index["admitted_plans"]
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

    assert "PLAN-20260706-0003" in index["admitted_plans"]
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

    assert "PLAN-20260706-0004" in index["admitted_plans"]
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

    assert "PLAN-20260706-0004" in index["admitted_plans"]
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

    assert any(
        warrant["warrant_id"] == "WARR-20260707-0005"
        and warrant["target_item_id"] == "PLAN-20260707-0003"
        and warrant["warrant_state"] == "supported"
        for warrant in index["warrants"]
    )


def test_build_self_model_index_records_verification_20260707_0003_for_threshold_completion():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        verification["verification_id"] == "VERIFY-20260707-0003"
        and verification["source_path"]
        == "docs/self_model/verifications/VERIFY-20260707-0003.json"
        for verification in index["verifications"]
    )


def test_build_self_model_index_records_warrant_20260707_0006_for_threshold_completion():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

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

    assert "PLAN-20260707-0004" not in index["open_plans"]


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



def test_build_self_model_index_records_warrant_20260709_0001_for_runtime_inclusion_admission():
    from pathlib import Path
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

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
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0002"


def test_build_self_model_index_records_plan_20260709_0002_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260709-0002"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260709-0002.json"
        for plan in index["plans"]
    )


def test_validate_warr_20260709_0005_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260709-0005.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260709-0005"
    assert record["target_item_id"] == "PLAN-20260709-0002"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_plan_20260709_0002_completion_warrant():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "PLAN-20260709-0002" in index["admitted_plans"]
    assert any(
        plan["plan_id"] == "PLAN-20260709-0002"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260709-0002.json"
        for plan in index["plans"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260709-0005"
        and warrant["target_item_id"] == "PLAN-20260709-0002"
        and warrant["target_item_type"] == "plan"
        for warrant in index["warrants"]
    )


def test_validate_cap_0005_record():
    from ai_lab.documentation.self_model import validate_capability_record

    record = read_json(Path("docs/self_model/capabilities/CAP-0005.json"))
    validate_capability_record(record)

    assert record["capability_id"] == "CAP-0005"
    assert record["status"] == "implemented"
    assert record["category"] == "diagnostic"
    assert record["last_verified"]["verification_artifact"] == "docs/self_model/verifications/VERIFY-20260709-0002.json"


def test_validate_verify_20260709_0002_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260709-0002.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260709-0002"
    assert record["target_item_id"] == "CAP-0005"
    assert record["target_item_type"] == "capability"
    assert record["status"] == "passed"


def test_validate_warr_20260709_0006_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260709-0006.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260709-0006"
    assert record["target_item_id"] == "CAP-0005"
    assert record["target_item_type"] == "capability"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_cap_0005_implemented():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "CAP-0005" in index["active_capabilities"]
    assert any(
        capability["capability_id"] == "CAP-0005"
        and capability["status"] == "implemented"
        and capability["source_path"] == "docs/self_model/capabilities/CAP-0005.json"
        for capability in index["capabilities"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260709-0002"
        and verification["source_path"] == "docs/self_model/verifications/VERIFY-20260709-0002.json"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260709-0006"
        and warrant["target_item_id"] == "CAP-0005"
        and warrant["target_item_type"] == "capability"
        for warrant in index["warrants"]
    )


def test_validate_verify_20260709_0003_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260709-0003.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260709-0003"
    assert record["target_item_id"] == "PLAN-20260709-0002"
    assert record["target_item_type"] == "plan"
    assert record["status"] == "passed"


def test_validate_warr_20260709_0007_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260709-0007.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260709-0007"
    assert record["target_item_id"] == "PLAN-20260709-0002"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_plan_20260709_0002_as_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "PLAN-20260709-0002" in index["admitted_plans"]
    assert any(
        plan["plan_id"] == "PLAN-20260709-0002"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260709-0002.json"
        for plan in index["plans"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260709-0003"
        and verification["source_path"] == "docs/self_model/verifications/VERIFY-20260709-0003.json"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260709-0007"
        and warrant["target_item_id"] == "PLAN-20260709-0002"
        and warrant["target_item_type"] == "plan"
        for warrant in index["warrants"]
    )


def test_gap_0002_recommends_distance_aware_evaluation():
    from ai_lab.documentation.self_model import (
        validate_gap_record,
    )

    record = read_json(
        Path("docs/self_model/gaps/GAP-0002.json")
    )
    validate_gap_record(record)

    assert record["status"] == "open"
    assert "CAP-0009" in record["related_capabilities"]
    assert "CAP-0011" in record["related_capabilities"]
    assert (
        "distance-aware graph-neighborhood representation"
        in record["recommended_first_slice"]
    )
    assert (
        "isolated-target diagnostics"
        in record["recommended_first_slice"]
    )
    assert (
        "provider prompts"
        in record["recommended_first_slice"]
    )
    assert (
        "2,223 tokens"
        in record["evidence"]["reason"]
    )
    assert (
        "13,208 tokens"
        in record["evidence"]["reason"]
    )

    capability = read_json(
        Path(
            "docs/self_model/capabilities/"
            "CAP-0011.json"
        )
    )
    assert any(
        "PLAN-20260716-0001 is completed"
        in action
        for action
        in capability["recommended_next_actions"]
    )


def test_validate_plan_20260709_0003_record():
    from ai_lab.documentation.self_model import validate_plan_record

    record = read_json(Path("docs/self_model/plans/PLAN-20260709-0003.json"))
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260709-0003"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0002"
    assert record["admission_warrant_id"] == "WARR-20260709-0008"
    assert record["completion_verification_id"] == "VERIFY-20260709-0005"
    assert record["completion_warrant_id"] == "WARR-20260709-0010"
    assert "Evidence/reporting only." in record["constraints"]


def test_build_self_model_index_records_plan_20260709_0003_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260709-0003"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260709-0003.json"
        for plan in index["plans"]
    )


def test_validate_warr_20260709_0008_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260709-0008.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260709-0008"
    assert record["target_item_id"] == "PLAN-20260709-0003"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_plan_20260709_0003_completion_warrant():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "PLAN-20260709-0003" in index["admitted_plans"]
    assert any(
        plan["plan_id"] == "PLAN-20260709-0003"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260709-0003.json"
        for plan in index["plans"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260709-0008"
        and warrant["target_item_id"] == "PLAN-20260709-0003"
        and warrant["target_item_type"] == "plan"
        for warrant in index["warrants"]
    )


def test_validate_cap_0006_record():
    from ai_lab.documentation.self_model import validate_capability_record

    record = read_json(Path("docs/self_model/capabilities/CAP-0006.json"))
    validate_capability_record(record)

    assert record["capability_id"] == "CAP-0006"
    assert record["status"] == "implemented"
    assert record["category"] == "diagnostic"
    assert record["last_verified"]["verification_artifact"] == "docs/self_model/verifications/VERIFY-20260709-0004.json"


def test_validate_verify_20260709_0004_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260709-0004.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260709-0004"
    assert record["target_item_id"] == "CAP-0006"
    assert record["target_item_type"] == "capability"
    assert record["status"] == "passed"


def test_validate_warr_20260709_0009_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260709-0009.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260709-0009"
    assert record["target_item_id"] == "CAP-0006"
    assert record["target_item_type"] == "capability"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_cap_0006_implemented():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "CAP-0006" in index["active_capabilities"]
    assert any(
        capability["capability_id"] == "CAP-0006"
        and capability["status"] == "implemented"
        and capability["source_path"] == "docs/self_model/capabilities/CAP-0006.json"
        for capability in index["capabilities"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260709-0004"
        and verification["source_path"] == "docs/self_model/verifications/VERIFY-20260709-0004.json"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260709-0009"
        and warrant["target_item_id"] == "CAP-0006"
        and warrant["target_item_type"] == "capability"
        for warrant in index["warrants"]
    )


def test_validate_verify_20260709_0005_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260709-0005.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260709-0005"
    assert record["target_item_id"] == "PLAN-20260709-0003"
    assert record["target_item_type"] == "plan"
    assert record["status"] == "passed"


def test_validate_warr_20260709_0010_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260709-0010.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260709-0010"
    assert record["target_item_id"] == "PLAN-20260709-0003"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_plan_20260709_0003_completed_final():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "PLAN-20260709-0003" in index["admitted_plans"]
    assert any(
        plan["plan_id"] == "PLAN-20260709-0003"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260709-0003.json"
        for plan in index["plans"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260709-0005"
        and verification["source_path"] == "docs/self_model/verifications/VERIFY-20260709-0005.json"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260709-0010"
        and warrant["target_item_id"] == "PLAN-20260709-0003"
        and warrant["target_item_type"] == "plan"
        for warrant in index["warrants"]
    )


def test_validate_plan_20260710_0001_record():
    from ai_lab.documentation.self_model import validate_plan_record

    record = read_json(Path("docs/self_model/plans/PLAN-20260710-0001.json"))
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260710-0001"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0002"
    assert record["admission_warrant_id"] == "WARR-20260710-0001"
    assert record["completion_verification_id"] == "VERIFY-20260710-0002"
    assert record["completion_warrant_id"] == "WARR-20260710-0003"
    assert "Evidence and decision reporting only." in record["constraints"]
    assert "No context-pack integration." in record["constraints"]


def test_build_self_model_index_records_plan_20260710_0001_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260710-0001"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260710-0001.json"
        for plan in index["plans"]
    )


def test_validate_warr_20260710_0001_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0001.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0001"
    assert record["target_item_id"] == "PLAN-20260710-0001"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_plan_20260710_0001_completion_warrant():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "PLAN-20260710-0001" in index["admitted_plans"]
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0001"
        and warrant["target_item_id"] == "PLAN-20260710-0001"
        and warrant["target_item_type"] == "plan"
        for warrant in index["warrants"]
    )


def test_validate_cap_0007_record():
    from ai_lab.documentation.self_model import validate_capability_record

    record = read_json(Path("docs/self_model/capabilities/CAP-0007.json"))
    validate_capability_record(record)

    assert record["capability_id"] == "CAP-0007"
    assert record["status"] == "implemented"
    assert record["category"] == "diagnostic"
    assert record["last_verified"]["verification_artifact"] == "docs/self_model/verifications/VERIFY-20260710-0001.json"


def test_validate_verify_20260710_0001_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260710-0001.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260710-0001"
    assert record["target_item_id"] == "CAP-0007"
    assert record["target_item_type"] == "capability"
    assert record["status"] == "passed"


def test_validate_warr_20260710_0002_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0002.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0002"
    assert record["target_item_id"] == "CAP-0007"
    assert record["target_item_type"] == "capability"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_cap_0007_implemented():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "CAP-0007" in index["active_capabilities"]
    assert any(
        capability["capability_id"] == "CAP-0007"
        and capability["status"] == "implemented"
        and capability["source_path"] == "docs/self_model/capabilities/CAP-0007.json"
        for capability in index["capabilities"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260710-0001"
        and verification["source_path"] == "docs/self_model/verifications/VERIFY-20260710-0001.json"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0002"
        and warrant["target_item_id"] == "CAP-0007"
        and warrant["target_item_type"] == "capability"
        for warrant in index["warrants"]
    )


def test_validate_verify_20260710_0002_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260710-0002.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260710-0002"
    assert record["target_item_id"] == "PLAN-20260710-0001"
    assert record["target_item_type"] == "plan"
    assert record["status"] == "passed"


def test_validate_warr_20260710_0003_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0003.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0003"
    assert record["target_item_id"] == "PLAN-20260710-0001"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"


def test_build_self_model_index_records_plan_20260710_0001_completed_final():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "PLAN-20260710-0001" in index["admitted_plans"]
    assert any(
        plan["plan_id"] == "PLAN-20260710-0001"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260710-0001.json"
        for plan in index["plans"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260710-0002"
        and verification["source_path"] == "docs/self_model/verifications/VERIFY-20260710-0002.json"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0003"
        and warrant["target_item_id"] == "PLAN-20260710-0001"
        and warrant["target_item_type"] == "plan"
        for warrant in index["warrants"]
    )


def test_validate_plan_20260710_0002_record():
    from ai_lab.documentation.self_model import validate_plan_record

    record = read_json(Path("docs/self_model/plans/PLAN-20260710-0002.json"))
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260710-0002"
    assert record["status"] == "completed"
    assert record["admission_warrant_id"] == "WARR-20260710-0004"
    assert record["completion_verification_id"] == "VERIFY-20260710-0004"
    assert record["completion_warrant_id"] == "WARR-20260710-0006"
    assert record["source_gap_id"] == "GAP-0002"
    assert "CAP-0007" in record["depends_on_capability_ids"]
    assert "No context-pack integration." in record["constraints"]


def test_build_self_model_index_records_plan_20260710_0002_proposed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260710-0002"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        and plan["source_path"] == "docs/self_model/plans/PLAN-20260710-0002.json"
        for plan in index["plans"]
    )


def test_validate_warr_20260710_0004_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0004.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0004"
    assert record["target_item_id"] == "PLAN-20260710-0002"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"


def test_build_self_model_index_records_warr_20260710_0004_admission():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260710-0002"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0004"
        and warrant["target_item_id"] == "PLAN-20260710-0002"
        for warrant in index["warrants"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0004"
        and warrant["target_item_id"] == "PLAN-20260710-0002"
        and warrant["target_item_type"] == "plan"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        and warrant["source_path"] == "docs/self_model/warrants/WARR-20260710-0004.json"
        for warrant in index["warrants"]
    )


def test_decision_20260710_0001_graph_neighborhood_repository_readiness():
    decision = read_json(Path("docs/self_model/decisions/DECISION-20260710-0001.json"))

    assert decision["schema_version"] == "v1"
    assert decision["decision_id"] == "DECISION-20260710-0001"
    assert decision["status"] == "recorded"
    assert decision["source_gap_id"] == "GAP-0002"
    assert decision["source_plan_id"] == "PLAN-20260710-0002"
    assert decision["source_capability_ids"] == ["CAP-0006", "CAP-0007"]
    assert decision["decision"] == "propose_separate_context_pack_integration_plan"
    assert decision["selection_effect"] == "none"

    blocked = set(decision["blocked_effects"])
    assert "No context-pack integration." in blocked
    assert "No runtime context selection changes." in blocked
    assert "No provider prompt changes." in blocked
    assert "No persisted graph writes." in blocked
    assert "No graph database." in blocked
    assert "No retrieval, embedding, or reranking changes." in blocked
    assert "No production index mutation." in blocked
    assert "No memory-store mutation." in blocked
    assert "No runtime-manifest mutation." in blocked
    assert "No automatic context inclusion." in blocked

    assert any(
        "separate governed context-pack integration plan"
        in item
        for item in decision["required_next_governance"]
    )


def test_validate_cap_0008_record():
    from ai_lab.documentation.self_model import validate_capability_record

    record = read_json(Path("docs/self_model/capabilities/CAP-0008.json"))
    validate_capability_record(record)

    assert record["capability_id"] == "CAP-0008"
    assert record["status"] == "implemented"


def test_validate_verify_20260710_0003_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260710-0003.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260710-0003"


def test_validate_warr_20260710_0005_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0005.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0005"
    assert record["target_item_id"] == "CAP-0008"
    assert record["target_item_type"] == "capability"
    assert record["warrant_state"] == "supported"


def test_build_self_model_index_records_cap_0008():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "CAP-0008" in index["active_capabilities"]
    assert any(
        capability["capability_id"] == "CAP-0008"
        and capability["status"] == "implemented"
        for capability in index["capabilities"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260710-0003"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0005"
        and warrant["target_item_id"] == "CAP-0008"
        for warrant in index["warrants"]
    )


def test_validate_verify_20260710_0004_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260710-0004.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260710-0004"


def test_validate_warr_20260710_0006_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0006.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0006"
    assert record["target_item_id"] == "PLAN-20260710-0002"
    assert record["target_item_type"] == "plan"
    assert record["warrant_state"] == "supported"


def test_build_self_model_index_records_plan_20260710_0002_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260710-0002"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )

    plan_record = read_json(Path("docs/self_model/plans/PLAN-20260710-0002.json"))
    assert plan_record["completion_verification_id"] == "VERIFY-20260710-0004"
    assert plan_record["completion_warrant_id"] == "WARR-20260710-0006"
    assert any(
        verification["verification_id"] == "VERIFY-20260710-0004"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0006"
        and warrant["target_item_id"] == "PLAN-20260710-0002"
        for warrant in index["warrants"]
    )


def test_validate_plan_20260710_0003_record():
    from ai_lab.documentation.self_model import validate_plan_record

    record = read_json(Path("docs/self_model/plans/PLAN-20260710-0003.json"))
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260710-0003"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0002"
    assert record["completion_verification_id"] == "VERIFY-20260710-0006"
    assert record["completion_warrant_id"] == "WARR-20260710-0009"
    assert record["source_capability_id"] == "CAP-0008"
    assert "docs/self_model/decisions/DECISION-20260710-0001.json" in record["evidence_ids"]
    assert "docs/self_model/capabilities/CAP-0008.json" in record["evidence_ids"]
    assert "Do not change runtime context selection." in record["constraints"]
    assert "Do not change provider prompts." in record["constraints"]
    assert "Do not enable automatic context inclusion." in record["constraints"]
    assert record["admission_warrant_id"] == "WARR-20260710-0007"


def test_build_self_model_index_records_plan_20260710_0003_proposed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260710-0003"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )


def test_validate_warr_20260710_0007_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0007.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0007"
    assert record["target_item_id"] == "PLAN-20260710-0003"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"


def test_build_self_model_index_records_warr_20260710_0007_admission():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260710-0003"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0007"
        and warrant["target_item_id"] == "PLAN-20260710-0003"
        for warrant in index["warrants"]
    )


def test_validate_cap_0009_record():
    from ai_lab.documentation.self_model import (
        validate_capability_record,
    )

    record = read_json(
        Path(
            "docs/self_model/capabilities/"
            "CAP-0009.json"
        )
    )
    validate_capability_record(record)

    assert record["capability_id"] == "CAP-0009"
    assert record["status"] == "implemented"
    assert record["category"] == "memory_context"
    assert record["repo_commit"].startswith("dbcf88d")
    assert (
        "ai_lab.documentation.context_pack_builder."
        "graph_neighborhood_context_items"
        in record["interfaces"]
    )
    assert (
        "ai_lab.documentation.context_pack_builder."
        "build_latest_context_manifest"
        in record["interfaces"]
    )

    admissions = {
        item["id"]
        for item in record["evidence"]["admissions"]
    }
    assert admissions == {
        "PLAN-20260710-0003",
        "WARR-20260710-0007",
    }

    assert (
        record["evidence"]["commits"][0]["commit"]
        == (
            "dbcf88d94a8b35ed8177c1a9aadc49b8849d7c4a"
        )
    )

    files = {
        item["path"]
        for item in record["evidence"]["files"]
    }
    assert files == {
        (
            "ai_lab/documentation/"
            "context_pack_builder.py"
        ),
        "tests/test_context_pack_builder.py",
    }

    assert any(
        "may affect ContextPackManifest.items"
        in limit
        for limit in record["limits"]
    )
    assert any(
        "whole-artifact token estimates"
        in limit
        for limit in record["limits"]
    )


def test_validate_verify_20260710_0005_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260710-0005.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260710-0005"


def test_validate_warr_20260710_0008_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0008.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0008"
    assert record["target_item_id"] == "CAP-0009"
    assert record["target_item_type"] == "capability"
    assert record["warrant_state"] == "supported"


def test_build_self_model_index_records_cap_0009():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert "CAP-0009" in index["active_capabilities"]
    assert any(
        capability["capability_id"] == "CAP-0009"
        and capability["status"] == "implemented"
        for capability in index["capabilities"]
    )
    assert any(
        verification["verification_id"] == "VERIFY-20260710-0005"
        for verification in index["verifications"]
    )
    assert any(
        warrant["warrant_id"] == "WARR-20260710-0008"
        and warrant["target_item_id"] == "CAP-0009"
        for warrant in index["warrants"]
    )


def test_validate_verify_20260710_0006_record():
    from ai_lab.documentation.self_model import validate_verification_record

    record = read_json(Path("docs/self_model/verifications/VERIFY-20260710-0006.json"))
    validate_verification_record(record)

    assert record["verification_id"] == "VERIFY-20260710-0006"


def test_validate_warr_20260710_0009_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(Path("docs/self_model/warrants/WARR-20260710-0009.json"))
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0009"
    assert record["target_item_id"] == "PLAN-20260710-0003"
    assert record["target_item_type"] == "plan"
    assert record["warrant_state"] == "supported"


def test_build_self_model_index_records_plan_20260710_0003_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(repo_root=Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260710-0003"
        and plan["status"] == "completed"
        for plan in index["plans"]
    )

    plan_record = read_json(Path("docs/self_model/plans/PLAN-20260710-0003.json"))
    assert plan_record["completion_verification_id"] == "VERIFY-20260710-0006"
    assert plan_record["completion_warrant_id"] == "WARR-20260710-0009"


def test_validate_gap_0003_record():
    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        validate_gap_record,
    )

    record = read_json(
        Path("docs/self_model/gaps/GAP-0003.json")
    )
    validate_gap_record(record)

    assert record["gap_id"] == "GAP-0003"
    assert record["status"] == "closed"
    assert (
        record["category"]
        == "self_model_infrastructure"
    )
    assert record["closed_at"]
    assert (
        record["closure_warrant_id"]
        == "WARR-20260716-0001"
    )
    assert "CAP-0010" in record["closure_summary"]
    assert (
        record["related_capabilities"]
        == ["CAP-0009"]
    )

    registry = SelfModelRegistry(Path("."))
    references = {
        (
            reference.field_name,
            reference.target_id,
        )
        for reference in registry.references("gap")
        if (
            reference.source_record_id
            == "GAP-0003"
        )
    }

    assert references == {
        (
            "related_capabilities",
            "CAP-0009",
        ),
        (
            "closure_warrant_id",
            "WARR-20260716-0001",
        ),
    }


def test_validate_warr_20260710_0010_record():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(
        Path("docs/self_model/warrants/WARR-20260710-0010.json")
    )
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0010"
    assert record["target_item_id"] == "GAP-0003"
    assert record["target_item_type"] == "gap"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"


def test_build_self_model_index_records_gap_0003_closed():
    from ai_lab.documentation.self_model import (
        build_self_model_index,
    )

    index = build_self_model_index(
        repo_root=Path(".")
    )

    assert any(
        gap["gap_id"] == "GAP-0003"
        and gap["status"] == "closed"
        for gap in index["gaps"]
    )
    assert "GAP-0003" not in index["open_gaps"]

    assert any(
        warrant["warrant_id"]
        == "WARR-20260716-0001"
        and warrant["target_item_id"]
        == "GAP-0003"
        and warrant["target_item_type"]
        == "gap"
        for warrant in index["warrants"]
    )

    assert not any(
        recommendation["source_record"]
        == "GAP-0003"
        for recommendation
        in index["recommended_next_targets"]
    )


def test_validate_plan_20260710_0004_completion():
    from ai_lab.documentation.self_model import validate_plan_record

    record = read_json(
        Path("docs/self_model/plans/PLAN-20260710-0004.json")
    )
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260710-0004"
    assert record["source_gap_id"] == "GAP-0003"
    assert record["status"] == "completed"
    assert (
        record["completion_verification_id"]
        == "VERIFY-20260714-0002"
    )
    assert (
        record["completion_warrant_id"]
        == "WARR-20260714-0002"
    )
    assert record["completed_at"]
    assert "CAP-0010" in record["completion_summary"]


def test_build_self_model_index_records_plan_0004_as_completed():
    from ai_lab.documentation.self_model import build_self_model_index

    index = build_self_model_index(Path("."))

    assert any(
        plan["plan_id"] == "PLAN-20260710-0004"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0003"
        for plan in index["plans"]
    )


def test_validate_warr_20260710_0011_admission():
    from ai_lab.documentation.self_model import validate_warrant_record

    record = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260710-0011.json"
        )
    )
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260710-0011"
    assert record["target_item_id"] == "PLAN-20260710-0004"
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"


def test_self_model_registry_specs_cover_existing_record_families():
    from ai_lab.documentation.self_model import (
        SELF_MODEL_RECORD_SPECS,
    )

    assert {
        spec.record_type
        for spec in SELF_MODEL_RECORD_SPECS
    } == {
        "capability",
        "decision",
        "gap",
        "plan",
        "verification",
        "warrant",
    }

    assert len({
        spec.record_type
        for spec in SELF_MODEL_RECORD_SPECS
    }) == len(SELF_MODEL_RECORD_SPECS)


def test_validate_existing_decision_record():
    from ai_lab.documentation.self_model import (
        validate_decision_record,
    )

    record = read_json(
        Path(
            "docs/self_model/decisions/"
            "DECISION-20260710-0001.json"
        )
    )

    validate_decision_record(record)

    assert record["decision_id"] == "DECISION-20260710-0001"
    assert record["status"] == "recorded"


def test_self_model_registry_discovers_fixture_records(tmp_path):
    import json

    from ai_lab.documentation.self_model import (
        SELF_MODEL_RECORD_SPECS,
        SelfModelRegistry,
        read_json,
    )

    samples = {
        "capability": Path(
            "docs/self_model/capabilities/CAP-0001.json"
        ),
        "decision": Path(
            "docs/self_model/decisions/"
            "DECISION-20260710-0001.json"
        ),
        "gap": Path(
            "docs/self_model/gaps/GAP-0001.json"
        ),
        "plan": Path(
            "docs/self_model/plans/PLAN-20260705-0001.json"
        ),
        "verification": Path(
            "docs/self_model/verifications/"
            "VERIFY-20260705-0001.json"
        ),
        "warrant": Path(
            "docs/self_model/warrants/"
            "WARR-20260705-0001.json"
        ),
    }

    for spec in SELF_MODEL_RECORD_SPECS:
        source = samples[spec.record_type]
        target = (
            tmp_path
            / "docs"
            / "self_model"
            / spec.directory_name
            / source.name
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(
                read_json(source),
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

    registry = SelfModelRegistry(tmp_path)

    assert registry.count() == 6
    assert registry.count("capability") == 1
    assert registry.count("decision") == 1
    assert registry.count("gap") == 1
    assert registry.count("plan") == 1
    assert registry.count("verification") == 1
    assert registry.count("warrant") == 1

    capability = registry.require("CAP-0001")
    assert capability.record_type == "capability"
    assert capability.source_path == Path(
        "docs/self_model/capabilities/CAP-0001.json"
    )

    decision = registry.require(
        "DECISION-20260710-0001"
    )
    assert decision.status == "recorded"

    assert registry.get("CAP-9999") is None
    assert registry.count_by_status("verification") == {}


def test_self_model_registry_record_data_is_recursively_read_only(
    tmp_path,
):
    import json

    import pytest

    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        read_json,
    )

    source = Path(
        "docs/self_model/decisions/"
        "DECISION-20260710-0001.json"
    )
    target = (
        tmp_path
        / "docs"
        / "self_model"
        / "decisions"
        / source.name
    )
    target.parent.mkdir(parents=True)
    target.write_text(
        json.dumps(
            read_json(source),
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    registry = SelfModelRegistry(tmp_path)
    entry = registry.require("DECISION-20260710-0001")

    with pytest.raises(TypeError):
        entry.record["title"] = "mutated"

    with pytest.raises(AttributeError):
        entry.record["rationale"].append("mutated")

    mutable = entry.mutable_record()
    mutable["title"] = "changed copy"
    mutable["rationale"].append("changed copy")

    assert (
        entry.record["title"]
        == "Graph neighborhood repository readiness decision"
    )
    assert "changed copy" not in entry.record["rationale"]


def test_self_model_registry_rejects_filename_id_mismatch(
    tmp_path,
):
    import json

    import pytest

    from ai_lab.documentation.self_model import (
        SelfModelError,
        SelfModelRegistry,
        read_json,
    )

    record = read_json(
        Path(
            "docs/self_model/decisions/"
            "DECISION-20260710-0001.json"
        )
    )

    target = (
        tmp_path
        / "docs"
        / "self_model"
        / "decisions"
        / "DECISION-20260710-9999.json"
    )
    target.parent.mkdir(parents=True)
    target.write_text(
        json.dumps(record, indent=2, sort_keys=True)
        + "\n"
    )

    with pytest.raises(
        SelfModelError,
        match="filename must be DECISION-20260710-0001.json",
    ):
        SelfModelRegistry(tmp_path)


def test_self_model_registry_allows_missing_type_directories(
    tmp_path,
):
    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
    )

    registry = SelfModelRegistry(tmp_path)

    assert registry.count() == 0
    assert registry.entries() == ()


def test_build_self_model_index_consumes_registry(monkeypatch):
    import ai_lab.documentation.self_model as self_model

    calls = []
    registry_class = self_model.SelfModelRegistry

    class RecordingRegistry(registry_class):
        def entries(self, record_type=None):
            calls.append(record_type)
            return super().entries(record_type)

    monkeypatch.setattr(
        self_model,
        "SelfModelRegistry",
        RecordingRegistry,
    )

    index = self_model.build_self_model_index(
        Path("."),
        generated_at="2026-07-11T00:00:00+00:00",
    )

    assert calls == [
        "capability",
        "gap",
        "verification",
        "plan",
        "warrant",
    ]
    assert "decisions" not in index
    assert index["generation_rule"] == "aggregation_only"


def test_self_model_registry_lifecycle_metadata(tmp_path):
    import json

    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        read_json,
    )

    completed_source = Path(
        "docs/self_model/plans/"
        "PLAN-20260710-0003.json"
    )
    admitted_source = Path(
        "docs/self_model/plans/"
        "PLAN-20260710-0004.json"
    )

    completed_record = read_json(completed_source)
    admitted_record = read_json(admitted_source)

    admitted_record["status"] = "admitted"

    for field_name in (
        "completed_at",
        "completion_summary",
        "completion_verification_id",
        "completion_warrant_id",
    ):
        admitted_record.pop(field_name, None)

    fixture_records = (
        (
            completed_source,
            completed_record,
        ),
        (
            admitted_source,
            admitted_record,
        ),
    )

    for source, record in fixture_records:
        target = (
            tmp_path
            / "docs"
            / "self_model"
            / "plans"
            / source.name
        )
        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        target.write_text(
            json.dumps(
                record,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    registry = SelfModelRegistry(tmp_path)

    assert registry.is_open("PLAN-20260710-0004")
    assert not registry.is_open("PLAN-20260710-0003")
    assert [
        entry.record_id
        for entry in registry.open_entries("plan")
    ] == ["PLAN-20260710-0004"]


def test_self_model_registry_resolves_explicit_references(
    tmp_path,
):
    import json

    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        read_json,
    )

    sources = [
        Path(
            "docs/self_model/capabilities/CAP-0005.json"
        ),
        Path(
            "docs/self_model/capabilities/CAP-0009.json"
        ),
        Path(
            "docs/self_model/gaps/GAP-0003.json"
        ),
        Path(
            "docs/self_model/verifications/"
            "VERIFY-20260709-0002.json"
        ),
        Path(
            "docs/self_model/warrants/"
            "WARR-20260709-0006.json"
        ),
    ]

    directory_by_prefix = {
        "CAP": "capabilities",
        "GAP": "gaps",
        "VERIFY": "verifications",
        "WARR": "warrants",
    }

    for source in sources:
        prefix = source.name.split("-", 1)[0]
        target = (
            tmp_path
            / "docs"
            / "self_model"
            / directory_by_prefix[prefix]
            / source.name
        )
        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        record = read_json(source)

        if source.name == "GAP-0003.json":
            record["status"] = "open"

            for field_name in (
                "closed_at",
                "closure_summary",
                "closure_warrant_id",
            ):
                record.pop(field_name, None)

        target.write_text(
            json.dumps(
                record,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    registry = SelfModelRegistry(tmp_path)

    assert registry.unresolved_references() == ()

    gap_reference = registry.references("gap")[0]
    assert (
        gap_reference.field_name
        == "related_capabilities"
    )
    assert (
        registry.resolve_reference(
            gap_reference
        ).record_id
        == "CAP-0009"
    )

    verification_reference = registry.references(
        "verification"
    )[0]
    assert (
        verification_reference.expected_target_type
        == "capability"
    )
    assert (
        registry.resolve_reference(
            verification_reference
        ).record_id
        == "CAP-0005"
    )

    warrant_reference = registry.references(
        "warrant"
    )[0]
    assert (
        warrant_reference.expected_target_type
        == "capability"
    )
    assert (
        registry.resolve_reference(
            warrant_reference
        ).record_id
        == "CAP-0005"
    )


def test_self_model_registry_reports_missing_reference(
    tmp_path,
):
    import json

    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        read_json,
    )

    source = Path(
        "docs/self_model/gaps/GAP-0003.json"
    )
    target = (
        tmp_path
        / "docs"
        / "self_model"
        / "gaps"
        / source.name
    )
    target.parent.mkdir(parents=True)

    record = read_json(source)
    record["status"] = "open"

    for field_name in (
        "closed_at",
        "closure_summary",
        "closure_warrant_id",
    ):
        record.pop(field_name, None)

    target.write_text(
        json.dumps(
            record,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    registry = SelfModelRegistry(tmp_path)
    issues = registry.unresolved_references()

    assert len(issues) == 1
    assert issues[0].code == "missing_target"
    assert (
        issues[0].reference.source_record_id
        == "GAP-0003"
    )
    assert (
        issues[0].reference.target_id
        == "CAP-0009"
    )
    assert (
        issues[0].reference.expected_target_type
        == "capability"
    )
    assert issues[0].actual_target_type is None


def test_self_model_registry_reports_wrong_reference_type(
    tmp_path,
):
    import json

    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        read_json,
    )

    capability_source = Path(
        "docs/self_model/capabilities/CAP-0005.json"
    )
    capability_target = (
        tmp_path
        / "docs"
        / "self_model"
        / "capabilities"
        / capability_source.name
    )
    capability_target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    capability_target.write_text(
        json.dumps(
            read_json(capability_source),
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    warrant = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260709-0006.json"
        )
    )
    warrant["target_item_type"] = "gap"

    warrant_target = (
        tmp_path
        / "docs"
        / "self_model"
        / "warrants"
        / "WARR-20260709-0006.json"
    )
    warrant_target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    warrant_target.write_text(
        json.dumps(
            warrant,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    registry = SelfModelRegistry(tmp_path)
    issues = registry.unresolved_references()

    assert len(issues) == 1
    assert issues[0].code == "wrong_target_type"
    assert issues[0].reference.target_id == "CAP-0005"
    assert issues[0].reference.expected_target_type == "gap"
    assert issues[0].actual_target_type == "capability"
    assert (
        registry.resolve_reference(issues[0].reference)
        is None
    )


def _write_registry_relation_fixture_record(
    tmp_path,
    source,
):
    import json

    from ai_lab.documentation.self_model import read_json

    directory_by_prefix = {
        "CAP": "capabilities",
        "GAP": "gaps",
        "VERIFY": "verifications",
        "WARR": "warrants",
    }

    prefix = source.name.split("-", 1)[0]
    target = (
        tmp_path
        / "docs"
        / "self_model"
        / directory_by_prefix[prefix]
        / source.name
    )
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    record = read_json(source)

    # Relation fixtures using GAP-0003 test only the
    # related_capabilities edge. Keep them independent
    # from the live record's closure-warrant relation.
    if source.name == "GAP-0003.json":
        record["status"] = "open"

        for field_name in (
            "closed_at",
            "closure_summary",
            "closure_warrant_id",
        ):
            record.pop(field_name, None)

    target.write_text(
        json.dumps(
            record,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def test_self_model_registry_emits_graph_relations(
    tmp_path,
):
    from ai_lab.documentation.self_model import (
        RegistryRelation,
        SelfModelRegistry,
    )

    sources = [
        Path(
            "docs/self_model/capabilities/CAP-0005.json"
        ),
        Path(
            "docs/self_model/capabilities/CAP-0009.json"
        ),
        Path(
            "docs/self_model/gaps/GAP-0003.json"
        ),
        Path(
            "docs/self_model/verifications/"
            "VERIFY-20260709-0002.json"
        ),
        Path(
            "docs/self_model/warrants/"
            "WARR-20260709-0006.json"
        ),
    ]

    for source in sources:
        _write_registry_relation_fixture_record(
            tmp_path,
            source,
        )

    registry = SelfModelRegistry(tmp_path)
    relations = registry.relations()

    assert len(relations) == 3
    assert all(
        isinstance(relation, RegistryRelation)
        for relation in relations
    )

    relation_by_source = {
        relation.source_id: relation
        for relation in relations
    }

    gap_relation = relation_by_source["GAP-0003"]

    assert gap_relation.predicate == (
        "self_model.related_capabilities"
    )
    assert gap_relation.target_id == "CAP-0009"
    assert (
        gap_relation.relation_source
        == "self_model_registry"
    )
    assert gap_relation.authoritative is True
    assert gap_relation.scope == "self_model"
    assert gap_relation.evidence == (
        "docs/self_model/gaps/GAP-0003.json"
        "#related_capabilities"
    )

    verification_relation = relation_by_source[
        "VERIFY-20260709-0002"
    ]
    assert verification_relation.predicate == (
        "self_model.target_item_id"
    )
    assert verification_relation.target_id == "CAP-0005"

    warrant_relation = relation_by_source[
        "WARR-20260709-0006"
    ]
    assert warrant_relation.predicate == (
        "self_model.target_item_id"
    )
    assert warrant_relation.target_id == "CAP-0005"


def test_self_model_registry_excludes_missing_relations(
    tmp_path,
):
    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
    )

    _write_registry_relation_fixture_record(
        tmp_path,
        Path(
            "docs/self_model/gaps/GAP-0003.json"
        ),
    )

    registry = SelfModelRegistry(tmp_path)

    assert len(registry.unresolved_references()) == 1
    assert registry.relations() == ()


def test_self_model_registry_excludes_wrong_type_relations(
    tmp_path,
):
    import json

    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        read_json,
    )

    _write_registry_relation_fixture_record(
        tmp_path,
        Path(
            "docs/self_model/capabilities/CAP-0005.json"
        ),
    )

    warrant = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260709-0006.json"
        )
    )
    warrant["target_item_type"] = "gap"

    target = (
        tmp_path
        / "docs"
        / "self_model"
        / "warrants"
        / "WARR-20260709-0006.json"
    )
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    target.write_text(
        json.dumps(
            warrant,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    registry = SelfModelRegistry(tmp_path)
    issues = registry.unresolved_references()

    assert len(issues) == 1
    assert issues[0].code == "wrong_target_type"
    assert registry.relations() == ()


def test_audit_self_model_registry_accepts_valid_fixture(
    tmp_path,
):
    from ai_lab.documentation.self_model import (
        audit_self_model_registry,
    )

    sources = [
        Path(
            "docs/self_model/capabilities/CAP-0005.json"
        ),
        Path(
            "docs/self_model/capabilities/CAP-0009.json"
        ),
        Path(
            "docs/self_model/gaps/GAP-0003.json"
        ),
        Path(
            "docs/self_model/verifications/"
            "VERIFY-20260709-0002.json"
        ),
        Path(
            "docs/self_model/warrants/"
            "WARR-20260709-0006.json"
        ),
    ]

    for source_path in sources:
        _write_registry_relation_fixture_record(
            tmp_path,
            source_path,
        )

    result = audit_self_model_registry(tmp_path)

    assert result == {
        "schema_version": "v1",
        "ok": True,
        "findings": [],
    }


def test_audit_self_model_registry_reports_missing_target(
    tmp_path,
):
    from ai_lab.documentation.self_model import (
        audit_self_model_registry,
    )

    _write_registry_relation_fixture_record(
        tmp_path,
        Path(
            "docs/self_model/gaps/GAP-0003.json"
        ),
    )

    result = audit_self_model_registry(tmp_path)

    assert result["ok"] is False
    assert len(result["findings"]) == 1

    finding = result["findings"][0]

    assert finding["severity"] == "error"
    assert finding["code"] == (
        "SELF_MODEL_REFERENCE_TARGET_MISSING"
    )
    assert finding["target"] == (
        "docs/self_model/gaps/GAP-0003.json"
        "#related_capabilities"
    )
    assert "CAP-0009" in finding["message"]
    assert "capability" in finding["message"]


def test_audit_self_model_registry_reports_wrong_target_type(
    tmp_path,
):
    import json

    from ai_lab.documentation.self_model import (
        audit_self_model_registry,
        read_json,
    )

    _write_registry_relation_fixture_record(
        tmp_path,
        Path(
            "docs/self_model/capabilities/CAP-0005.json"
        ),
    )

    warrant = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260709-0006.json"
        )
    )
    warrant["target_item_type"] = "gap"

    target = (
        tmp_path
        / "docs"
        / "self_model"
        / "warrants"
        / "WARR-20260709-0006.json"
    )
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    target.write_text(
        json.dumps(
            warrant,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    result = audit_self_model_registry(tmp_path)

    assert result["ok"] is False
    assert len(result["findings"]) == 1

    finding = result["findings"][0]

    assert finding["severity"] == "error"
    assert finding["code"] == (
        "SELF_MODEL_REFERENCE_TARGET_TYPE_MISMATCH"
    )
    assert finding["target"] == (
        "docs/self_model/warrants/"
        "WARR-20260709-0006.json"
        "#target_item_id"
    )
    assert "CAP-0005" in finding["message"]
    assert "gap" in finding["message"]
    assert "capability" in finding["message"]


def test_audit_self_model_includes_registry_reference_errors(
    monkeypatch,
):
    import ai_lab.documentation.self_model as self_model

    injected = {
        "severity": "error",
        "code": "SELF_MODEL_REFERENCE_TARGET_MISSING",
        "target": "fixture.json#source_gap_id",
        "message": "Injected missing reference.",
    }

    monkeypatch.setattr(
        self_model,
        "audit_self_model_registry",
        lambda repo_root: {
            "schema_version": "v1",
            "ok": False,
            "findings": [injected],
        },
    )

    result = self_model.audit_self_model(Path("."))

    assert result["ok"] is False
    assert injected in result["findings"]


def test_audit_self_model_registry_current_repository_has_no_errors():
    from ai_lab.documentation.self_model import (
        audit_self_model_registry,
    )

    result = audit_self_model_registry(Path("."))

    assert result == {
        "schema_version": "v1",
        "ok": True,
        "findings": [],
    }


def _direct_self_model_family_records(
    repo_root,
    directory_name,
    filename_glob,
    id_field,
):
    import json

    directory = (
        repo_root
        / "docs"
        / "self_model"
        / directory_name
    )

    records = []

    for path in sorted(directory.glob(filename_glob)):
        record = json.loads(
            path.read_text(encoding="utf-8")
        )
        records.append(
            (
                record[id_field],
                path.relative_to(repo_root),
                record,
            )
        )

    return tuple(
        sorted(
            records,
            key=lambda item: item[0],
        )
    )


def _direct_status_counts(
    records,
    status_field,
):
    from collections import Counter

    return dict(
        sorted(
            Counter(
                record[status_field]
                for _, _, record in records
            ).items()
        )
    )


def test_production_self_model_index_matches_canonical_records():
    """
    Derive the expected inventory independently from canonical JSON.

    The oracle deliberately does not use SelfModelRegistry so that
    registry discovery and index projection are not verified through
    the same implementation path.
    """

    from ai_lab.documentation.self_model import (
        build_self_model_index,
    )

    repo_root = Path(".").resolve()

    capabilities = _direct_self_model_family_records(
        repo_root,
        "capabilities",
        "CAP-*.json",
        "capability_id",
    )
    gaps = _direct_self_model_family_records(
        repo_root,
        "gaps",
        "GAP-*.json",
        "gap_id",
    )
    verifications = _direct_self_model_family_records(
        repo_root,
        "verifications",
        "VERIFY-*.json",
        "verification_id",
    )
    plans = _direct_self_model_family_records(
        repo_root,
        "plans",
        "PLAN-*.json",
        "plan_id",
    )
    warrants = _direct_self_model_family_records(
        repo_root,
        "warrants",
        "WARR-*.json",
        "warrant_id",
    )

    index = build_self_model_index(repo_root)

    assert [
        item["capability_id"]
        for item in index["capabilities"]
    ] == [
        record_id
        for record_id, _, _ in capabilities
    ]

    assert [
        item["gap_id"]
        for item in index["gaps"]
    ] == [
        record_id
        for record_id, _, _ in gaps
    ]

    assert [
        item["verification_id"]
        for item in index["verifications"]
    ] == [
        record_id
        for record_id, _, _ in verifications
    ]

    assert [
        item["plan_id"]
        for item in index["plans"]
    ] == [
        record_id
        for record_id, _, _ in plans
    ]

    assert [
        item["warrant_id"]
        for item in index["warrants"]
    ] == [
        record_id
        for record_id, _, _ in warrants
    ]

    assert index["capability_counts"] == (
        _direct_status_counts(
            capabilities,
            "status",
        )
    )
    assert index["gap_counts"] == (
        _direct_status_counts(
            gaps,
            "status",
        )
    )
    assert index["plan_counts"] == (
        _direct_status_counts(
            plans,
            "status",
        )
    )
    assert index["warrant_counts"] == (
        _direct_status_counts(
            warrants,
            "warrant_state",
        )
    )

    expected_active_capabilities = sorted(
        record_id
        for record_id, _, record in capabilities
        if record["status"] in {
            "experimental",
            "implemented",
            "partial",
        }
    )
    expected_open_gaps = sorted(
        record_id
        for record_id, _, record in gaps
        if record["status"] == "open"
    )
    expected_open_plans = sorted(
        record_id
        for record_id, _, record in plans
        if record["status"] in {
            "admitted",
            "proposed",
        }
    )

    assert (
        index["active_capabilities"]
        == expected_active_capabilities
    )
    assert index["open_gaps"] == expected_open_gaps
    assert index["open_plans"] == expected_open_plans


def test_self_model_registry_covers_all_canonical_json_records():
    """
    Detect omissions without encoding a fixed production quantity.
    """

    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
    )

    repo_root = Path(".").resolve()

    family_layout = (
        ("capabilities", "CAP-*.json"),
        ("decisions", "DECISION-*.json"),
        ("gaps", "GAP-*.json"),
        ("plans", "PLAN-*.json"),
        ("verifications", "VERIFY-*.json"),
        ("warrants", "WARR-*.json"),
    )

    filesystem_paths = {
        path.relative_to(repo_root)
        for directory_name, filename_glob in family_layout
        for path in (
            repo_root
            / "docs"
            / "self_model"
            / directory_name
        ).glob(filename_glob)
    }

    registry_paths = {
        entry.source_path
        for entry in SelfModelRegistry(
            repo_root
        ).entries()
    }

    assert registry_paths == filesystem_paths


def test_self_model_registry_documentation_covers_safe_workflow():
    documentation = Path(
        "docs/self_model/REGISTRY.md"
    ).read_text(encoding="utf-8")

    required_phrases = (
        "canonical JSON",
        "SelfModelRegistry",
        "create_self_model_record.py",
        "non-transactional",
        "exclusive",
        "rebase",
        "merge",
        "SELF_MODEL.json",
        "audit_self_model_index.py",
    )

    missing = [
        phrase
        for phrase in required_phrases
        if phrase not in documentation
    ]

    assert not missing, (
        "Registry documentation is missing: "
        + ", ".join(missing)
    )


def test_self_model_tests_do_not_hardcode_production_inventory():
    """
    Prevent literal global counts and complete inventories returning.

    Dynamic expectations derived from fixture or canonical records are
    permitted. Specific record membership and record-content assertions
    are also permitted.
    """

    import ast

    source_path = Path(__file__)
    tree = ast.parse(
        source_path.read_text(encoding="utf-8")
    )

    inventory_keys = {
        "active_capabilities",
        "open_gaps",
        "open_plans",
        "admitted_plans",
        "capability_counts",
        "gap_counts",
        "plan_counts",
        "warrant_counts",
        "capabilities",
        "gaps",
        "verifications",
        "plans",
        "warrants",
    }

    def contains_inventory_key(node):
        return any(
            isinstance(child, ast.Constant)
            and isinstance(child.value, str)
            and child.value in inventory_keys
            for child in ast.walk(node)
        )

    def is_literal_quantity_or_inventory(node):
        if isinstance(
            node,
            (
                ast.List,
                ast.Tuple,
                ast.Set,
                ast.Dict,
            ),
        ):
            return True

        return (
            isinstance(node, ast.Constant)
            and isinstance(
                node.value,
                (int, float),
            )
            and not isinstance(
                node.value,
                bool,
            )
        )

    violations = []

    for function in tree.body:
        if not isinstance(
            function,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            continue

        for node in ast.walk(function):
            if not isinstance(node, ast.Assert):
                continue

            comparison = node.test

            if not isinstance(
                comparison,
                ast.Compare,
            ):
                continue

            if not all(
                isinstance(
                    operator,
                    (ast.Eq, ast.NotEq),
                )
                for operator in comparison.ops
            ):
                continue

            operands = [
                comparison.left,
                *comparison.comparators,
            ]

            if not any(
                contains_inventory_key(operand)
                for operand in operands
            ):
                continue

            if not any(
                is_literal_quantity_or_inventory(
                    operand
                )
                for operand in operands
            ):
                continue

            violations.append(
                (
                    function.name,
                    node.lineno,
                    ast.unparse(comparison),
                )
            )

    assert not violations, (
        "Literal production inventory assertions found: "
        + repr(violations)
    )

def test_validate_plan_20260716_0001_completed():
    from ai_lab.documentation.self_model import (
        validate_plan_record,
    )

    record = read_json(
        Path(
            "docs/self_model/plans/"
            "PLAN-20260716-0001.json"
        )
    )
    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260716-0001"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0002"
    assert record["source_capability_id"] == "CAP-0009"
    assert (
        record["admission_warrant_id"]
        == "WARR-20260716-0002"
    )
    assert (
        record["completion_verification_id"]
        == "VERIFY-20260716-0003"
    )
    assert (
        record["completion_warrant_id"]
        == "WARR-20260716-0004"
    )
    assert record["completed_at"]
    assert "CAP-0011" in record["completion_summary"]
    assert "GAP-0002 remains open" in record[
        "completion_summary"
    ]


def test_build_self_model_index_records_plan_20260716_0001_completed():
    from ai_lab.documentation.self_model import (
        build_self_model_index,
    )

    index = build_self_model_index(
        repo_root=Path(".")
    )

    assert any(
        plan["plan_id"] == "PLAN-20260716-0001"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        for plan in index["plans"]
    )

    assert (
        "PLAN-20260716-0001"
        not in index["open_plans"]
    )

    # admitted_plans records historical admission,
    # including plans that later completed.
    assert (
        "PLAN-20260716-0001"
        in index["admitted_plans"]
    )

    assert any(
        gap["gap_id"] == "GAP-0002"
        and gap["status"] == "open"
        for gap in index["gaps"]
    )


def test_validate_warr_20260716_0002_admission():
    from ai_lab.documentation.self_model import (
        validate_warrant_record,
    )

    record = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260716-0002.json"
        )
    )
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260716-0002"
    assert (
        record["target_item_id"]
        == "PLAN-20260716-0001"
    )
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"
    assert (
        "scripts/build_context_pack.py"
        in record["scope"]
    )
    assert any(
        "GAP-0002 must remain open"
        in condition
        for condition in record["conditions"]
    )


def test_validate_cap_0011_graph_neighborhood_context_cli():
    from ai_lab.documentation.self_model import (
        validate_capability_record,
    )

    record = read_json(
        Path(
            "docs/self_model/capabilities/"
            "CAP-0011.json"
        )
    )
    validate_capability_record(record)

    assert record["capability_id"] == "CAP-0011"
    assert record["status"] == "implemented"
    assert record["category"] == "memory_context"
    assert record["repo_commit"].startswith("c59e237")
    assert (
        "scripts.build_context_pack.main"
        in record["interfaces"]
    )
    assert (
        record["last_verified"]["verification_artifact"]
        == (
            "docs/self_model/verifications/"
            "VERIFY-20260716-0002.json"
        )
    )
    assert any(
        "disabled by default" in limit
        for limit in record["limits"]
    )
    assert any(
        "GAP-0002" in limit
        for limit in record["limits"]
    )


def test_validate_verify_20260716_0002_cap_0011():
    from ai_lab.documentation.self_model import (
        validate_verification_record,
    )

    record = read_json(
        Path(
            "docs/self_model/verifications/"
            "VERIFY-20260716-0002.json"
        )
    )
    validate_verification_record(record)

    assert (
        record["verification_id"]
        == "VERIFY-20260716-0002"
    )
    assert record["target_item_id"] == "CAP-0011"
    assert record["target_item_type"] == "capability"
    assert record["status"] == "passed"
    assert record["repo_commit"].startswith("c59e237")
    assert any(
        "55 tests" in command["summary"]
        for command in record["commands"]
    )
    assert any(
        "529 tests" in command["summary"]
        for command in record["commands"]
    )


def test_validate_warr_20260716_0003_cap_0011():
    from ai_lab.documentation.self_model import (
        validate_warrant_record,
    )

    record = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260716-0003.json"
        )
    )
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260716-0003"
    assert record["target_item_id"] == "CAP-0011"
    assert record["target_item_type"] == "capability"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"
    assert "does not complete" in record["scope"]
    assert "close GAP-0002" in record["scope"]


def test_registry_records_cap_0011_with_completed_plan():
    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
    )

    registry = SelfModelRegistry(Path(".").resolve())

    capability = registry.require("CAP-0011")
    implementation_verification = registry.require(
        "VERIFY-20260716-0002"
    )
    capability_warrant = registry.require(
        "WARR-20260716-0003"
    )
    completion_verification = registry.require(
        "VERIFY-20260716-0003"
    )
    completion_warrant = registry.require(
        "WARR-20260716-0004"
    )
    plan = registry.require("PLAN-20260716-0001")
    gap = registry.require("GAP-0002")

    assert capability.status == "implemented"
    assert (
        implementation_verification.record["status"]
        == "passed"
    )
    assert capability_warrant.status == "supported"

    assert plan.status == "completed"
    assert not registry.is_open(plan.record_id)
    assert (
        plan.record["completion_verification_id"]
        == "VERIFY-20260716-0003"
    )
    assert (
        plan.record["completion_warrant_id"]
        == "WARR-20260716-0004"
    )

    assert (
        completion_verification.record["status"]
        == "passed"
    )
    assert completion_warrant.status == "supported"

    assert gap.status == "open"
    assert registry.is_open(gap.record_id)
    assert registry.unresolved_references() == ()


def test_validate_verify_20260716_0003_plan_completion():
    from ai_lab.documentation.self_model import (
        validate_verification_record,
    )

    record = read_json(
        Path(
            "docs/self_model/verifications/"
            "VERIFY-20260716-0003.json"
        )
    )
    validate_verification_record(record)

    assert (
        record["verification_id"]
        == "VERIFY-20260716-0003"
    )
    assert (
        record["target_item_id"]
        == "PLAN-20260716-0001"
    )
    assert record["target_item_type"] == "plan"
    assert record["status"] == "passed"
    assert record["repo_commit"].startswith("ee2d620")
    assert "GAP-0002 remains open" in record["summary"]


def test_validate_warr_20260716_0004_plan_completion():
    from ai_lab.documentation.self_model import (
        validate_warrant_record,
    )

    record = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260716-0004.json"
        )
    )
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260716-0004"
    assert (
        record["target_item_id"]
        == "PLAN-20260716-0001"
    )
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"
    assert "does not close GAP-0002" in record["scope"]


def test_validate_verify_20260716_0004_graph_governance_reconciliation():
    from ai_lab.documentation.self_model import (
        validate_verification_record,
    )

    record = read_json(
        Path(
            "docs/self_model/verifications/"
            "VERIFY-20260716-0004.json"
        )
    )
    validate_verification_record(record)

    assert (
        record["verification_id"]
        == "VERIFY-20260716-0004"
    )
    assert record["target_item_id"] == "GAP-0002"
    assert record["target_item_type"] == "gap"
    assert record["status"] == "passed"
    assert "CAP-0009" in record["summary"]
    assert "No runtime code was changed" in record["summary"]


def test_validate_warr_20260716_0005_graph_governance_reconciliation():
    from ai_lab.documentation.self_model import (
        validate_warrant_record,
    )

    record = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260716-0005.json"
        )
    )
    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260716-0005"
    assert record["target_item_id"] == "GAP-0002"
    assert record["target_item_type"] == "gap"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"
    assert "Does not alter historical" in record["scope"]
    assert "close GAP-0002" in record["scope"]


def test_validate_plan_20260716_0002_completed():
    from ai_lab.documentation.self_model import (
        validate_plan_record,
    )

    record = read_json(
        Path(
            "docs/self_model/plans/"
            "PLAN-20260716-0002.json"
        )
    )

    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260716-0002"
    assert record["status"] == "completed"
    assert record["source_gap_id"] == "GAP-0002"
    assert (
        record["admission_warrant_id"]
        == "WARR-20260716-0006"
    )
    assert (
        record["completion_verification_id"]
        == "VERIFY-20260716-0005"
    )
    assert (
        record["completion_warrant_id"]
        == "WARR-20260716-0007"
    )
    assert record["completed_at"]
    assert (
        "CAP-0012"
        in record["completion_summary"]
    )
    assert (
        "GAP-0002 remains open"
        in record["completion_summary"]
    )
    assert (
        "compact representation contract"
        in record["next_action"]
    )


def test_build_self_model_index_records_plan_20260716_0002_completed():
    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        build_self_model_index,
    )

    index = build_self_model_index(
        repo_root=Path(".")
    )

    assert any(
        plan["plan_id"] == "PLAN-20260716-0002"
        and plan["status"] == "completed"
        and plan["source_gap_id"] == "GAP-0002"
        for plan in index["plans"]
    )

    assert (
        "PLAN-20260716-0002"
        not in index["open_plans"]
    )
    assert (
        "PLAN-20260716-0002"
        in index["admitted_plans"]
    )

    registry = SelfModelRegistry(Path(".").resolve())

    plan = registry.require("PLAN-20260716-0002")
    gap = registry.require("GAP-0002")

    assert plan.status == "completed"
    assert not registry.is_open(plan.record_id)
    assert gap.status == "open"
    assert registry.is_open(gap.record_id)
    assert registry.unresolved_references() == ()


def test_validate_warr_20260716_0006_admission():
    from ai_lab.documentation.self_model import (
        validate_warrant_record,
    )

    record = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260716-0006.json"
        )
    )

    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260716-0006"
    assert (
        record["target_item_id"]
        == "PLAN-20260716-0002"
    )
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"
    assert record["substrate"] == "provider_comparison"

    assert (
        "evidence-only"
        in record["scope"]
    )
    assert (
        "docs/comparisons/"
        "COMP-0027-gap-0002-next-governed-slice-review.md"
        in record["evidence_ids"]
    )
    assert any(
        "selection_effect none" in condition
        for condition in record["conditions"]
    )
    assert any(
        "No new persisted compact-summary"
        in condition
        for condition in record["conditions"]
    )
    assert any(
        "GAP-0002 must remain open"
        in condition
        for condition in record["conditions"]
    )


def test_build_self_model_index_records_warr_20260716_0006_admission():
    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        build_self_model_index,
    )

    index = build_self_model_index(
        repo_root=Path(".")
    )

    assert any(
        warrant["warrant_id"]
        == "WARR-20260716-0006"
        and warrant["target_item_id"]
        == "PLAN-20260716-0002"
        and warrant["target_item_type"] == "plan"
        and warrant["decision"] == "admit"
        and warrant["warrant_state"] == "supported"
        and warrant["source_path"]
        == (
            "docs/self_model/warrants/"
            "WARR-20260716-0006.json"
        )
        for warrant in index["warrants"]
    )

    registry = SelfModelRegistry(Path(".").resolve())

    warrant = registry.require("WARR-20260716-0006")
    plan = registry.require("PLAN-20260716-0002")

    assert warrant.status == "supported"

    # The admission warrant remains historical evidence after
    # the admitted plan progresses to completion.
    assert plan.status == "completed"
    assert not registry.is_open(plan.record_id)
    assert registry.unresolved_references() == ()


def test_validate_cap_0012_compact_graph_evaluator():
    from ai_lab.documentation.self_model import (
        validate_capability_record,
    )

    record = read_json(
        Path(
            "docs/self_model/capabilities/"
            "CAP-0012.json"
        )
    )

    validate_capability_record(record)

    assert record["capability_id"] == "CAP-0012"
    assert record["status"] == "implemented"
    assert record["category"] == "memory_context"
    assert record["repo_commit"].startswith("b17482b")
    assert (
        "evaluate_compact_graph_representations"
        in " ".join(record["interfaces"])
    )
    assert (
        record["last_verified"][
            "verification_artifact"
        ]
        == (
            "docs/self_model/verifications/"
            "VERIFY-20260716-0005.json"
        )
    )
    assert any(
        "selection_effect none" in limit
        for limit in record["limits"]
    )
    assert any(
        "17 of 43" in limit
        for limit in record["limits"]
    )
    assert any(
        "GAP-0002" in action
        for action in record[
            "recommended_next_actions"
        ]
    )


def test_validate_verify_20260716_0005_completion():
    from ai_lab.documentation.self_model import (
        validate_verification_record,
    )

    record = read_json(
        Path(
            "docs/self_model/verifications/"
            "VERIFY-20260716-0005.json"
        )
    )

    validate_verification_record(record)

    assert (
        record["verification_id"]
        == "VERIFY-20260716-0005"
    )
    assert (
        record["target_item_id"]
        == "PLAN-20260716-0002"
    )
    assert record["target_item_type"] == "plan"
    assert record["status"] == "passed"
    assert record["repo_commit"].startswith("b17482b")
    assert any(
        "49 tests" in command["summary"]
        for command in record["commands"]
    )
    assert any(
        "548 tests" in command["summary"]
        for command in record["commands"]
    )
    assert (
        "GAP-0002 remains open"
        in record["summary"]
    )


def test_validate_warr_20260716_0007_completion():
    from ai_lab.documentation.self_model import (
        validate_warrant_record,
    )

    record = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260716-0007.json"
        )
    )

    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260716-0007"
    assert (
        record["target_item_id"]
        == "PLAN-20260716-0002"
    )
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"
    assert "CAP-0012" in record["reason"]
    assert (
        "does not create or persist"
        in record["scope"]
    )
    assert "close GAP-0002" in record["scope"]


def test_validate_plan_20260717_0001_admitted():
    from ai_lab.documentation.self_model import (
        validate_plan_record,
    )

    record = read_json(
        Path(
            "docs/self_model/plans/"
            "PLAN-20260717-0001.json"
        )
    )

    validate_plan_record(record)

    assert record["plan_id"] == "PLAN-20260717-0001"
    assert record["status"] == "admitted"
    assert record["source_gap_id"] == "GAP-0002"
    assert record["source_capability_id"] == "CAP-0012"
    assert (
        record["admission_warrant_id"]
        == "WARR-20260717-0001"
    )
    assert record["admitted_at"]
    assert (
        "contract-only implementation"
        in record["admission_summary"]
    )
    assert (
        "WARR-20260717-0001"
        in record["constraints"][0]
    )
    assert any(
        "250-500" in item
        and "80-200" in item
        for item in record["scope"]
    )
    assert any(
        "fidelity" in item.lower()
        for item in record["expected_outputs"]
    )
    assert (
        "docs/self_model/warrants/"
        "WARR-20260717-0001.json"
        in record["evidence_ids"]
    )

    assert "completed_at" not in record
    assert "completion_verification_id" not in record
    assert "completion_warrant_id" not in record


def test_build_self_model_index_records_plan_20260717_0001_admitted():
    from ai_lab.documentation.self_model import (
        SelfModelRegistry,
        build_self_model_index,
    )

    index = build_self_model_index(
        repo_root=Path(".")
    )

    assert any(
        plan["plan_id"] == "PLAN-20260717-0001"
        and plan["status"] == "admitted"
        and plan["source_gap_id"] == "GAP-0002"
        for plan in index["plans"]
    )
    assert (
        "PLAN-20260717-0001"
        in index["open_plans"]
    )
    assert (
        "PLAN-20260717-0001"
        in index["admitted_plans"]
    )

    registry = SelfModelRegistry(Path(".").resolve())
    plan = registry.require("PLAN-20260717-0001")
    warrant = registry.require("WARR-20260717-0001")
    gap = registry.require("GAP-0002")

    assert plan.status == "admitted"
    assert registry.is_open(plan.record_id)
    assert warrant.status == "supported"
    assert gap.status == "open"
    assert registry.is_open(gap.record_id)
    assert registry.unresolved_references() == ()


def test_validate_warr_20260717_0001_admission():
    from ai_lab.documentation.self_model import (
        validate_warrant_record,
    )

    record = read_json(
        Path(
            "docs/self_model/warrants/"
            "WARR-20260717-0001.json"
        )
    )

    validate_warrant_record(record)

    assert record["warrant_id"] == "WARR-20260717-0001"
    assert (
        record["target_item_id"]
        == "PLAN-20260717-0001"
    )
    assert record["target_item_type"] == "plan"
    assert record["decision"] == "admit"
    assert record["warrant_state"] == "supported"
    assert (
        "17 of 43"
        in record["reason"]
    )
    assert any(
        "bounded fixtures" in condition
        for condition in record["conditions"]
    )
    assert any(
        "GAP-0002 must remain open"
        in condition
        for condition in record["conditions"]
    )
    assert (
        "No bulk or production sidecars"
        in record["scope"]
    )
