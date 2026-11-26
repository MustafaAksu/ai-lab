"""Step 3A record integrity and source-anchor tests; no live binding claims."""

from __future__ import annotations

import copy
from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import subprocess

import pytest

from ai_lab.providers import qualification_records as qr


def _git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.DEVNULL).decode().strip()


def _inputs(tmp_path, *, files=None):
    repo = tmp_path / "repository"
    repo.mkdir()
    _git(repo, "init", "-q")
    for path, data in {"README.md": b"fictional source inventory\n", **(files or {})}.items():
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    _git(repo, "add", ".")
    _git(repo, "-c", "user.name=Qualification Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")
    commit = _git(repo, "rev-parse", "HEAD")
    git = qr.load_git_catalog(repo, commit)
    inventory = {
        "schema_version": qr.SCHEMA_VERSION, "record_kind": "source_inventory", "domain": "synthetic",
        "inventory_id": "INVENTORY-FIXTURE", "selector_id": "REPO-CATALOG-ALL-1",
        "repository": "MustafaAksu/ai-lab", "repository_commit": commit, "root_tree_sha1": git.tree_sha1,
        "catalog_roots": list(qr.CATALOG_ROOTS), "entries": git.catalog_entries,
        "model_sources": [], "known_source_declarations": [], "omission_declarations": [],
    }
    fixture = {
        "schema_version": qr.SCHEMA_VERSION, "record_kind": "synthetic_fixture_bindings", "domain": "synthetic",
        "fixture_id": "FIXTURE-EMPTY", "fixture_artifact_refs": [],
        "tool_profile": {"profile_id": "SYN-TOOL-1", "namespace": "fixture:tools", "issuer_rows": [], "release_rows": [], "alias_rows": [], "execution_rows": []},
        "human_profile": {"profile_id": "SYN-HUMAN-1", "namespace": "fixture:human-persons", "principal_rows": [], "alias_rows": [], "actor_rows": []},
        "model_witness_profile": {"profile_id": "SYN-MODEL-WITNESS-1", "witness_rows": [], "availability_rows": []},
        "c3_conflict_fixture": {"rule_id": "SYN-C3-CONFLICT-1", "context_rows": []},
    }
    fixture_bytes = qr.canonical_bytes(fixture)
    inventory_bytes = qr.canonical_bytes(inventory)
    context = {
        "schema_version": qr.SCHEMA_VERSION, "record_kind": "evidence_context", "domain": "synthetic",
        "context_id": "CONTEXT-FIXTURE", "inventory_ref": qr.record_ref(inventory["inventory_id"], inventory_bytes),
        "context_policy": {
            "selector_id": "REPO-CATALOG-ALL-1", "mode": "event_time", "knowledge_cutoff": "2026-11-26T00:00:00Z",
            "freshness_window_days": 30,
            "production_profiles": {key: [] for key in ("endpoint_binding", "model_witness", "tool_binding", "human_binding", "ancestry", "availability")},
            "synthetic_profiles": {"model_witness": ["SYN-MODEL-WITNESS-1"], "tool_binding": ["SYN-TOOL-1"], "human_binding": ["SYN-HUMAN-1"], "ancestry": []},
        },
        "subject_refs": [], "selected_source_ids": [], "provided_artifact_refs": [],
        "known_source_declaration_refs": [], "omission_declaration_refs": [], "corroboration_witness_refs": [],
        "synthetic_fixture_ref": qr.record_ref(fixture["fixture_id"], fixture_bytes),
        "c3_context": None, "c10_context": None,
    }
    return repo, inventory, context, {"fixture.json": fixture_bytes}


def _anchor(repo, inventory, context, artifacts):
    inventory_bytes = qr.canonical_bytes(inventory)
    context = copy.deepcopy(context)
    context["inventory_ref"] = qr.record_ref(inventory["inventory_id"], inventory_bytes)
    context_bytes = qr.canonical_bytes(context)
    store = {**artifacts, "inventory.json": inventory_bytes, "context.json": context_bytes}
    return qr.load_synthetic_anchor(repo, context_ref=qr.record_ref(context["context_id"], context_bytes), artifacts=store)


@pytest.mark.parametrize("data", [b'{"x":1,"x":2}', b'{"n":NaN}', b'{"n":Infinity}', b'{"n":1e9999}', b'"\xff"'])
def test_strict_json_rejects_duplicate_nonfinite_and_invalid_utf8(data):
    with pytest.raises(qr.QualificationError) as caught:
        qr.strict_loads(data)
    assert caught.value.code == "INVALID_SCHEMA"


def test_canonical_bytes_is_total_and_does_not_coerce_non_json():
    assert qr.canonical_bytes({"b": 2, "a": [1, True]}) == qr.canonical_bytes({"a": [1, True], "b": 2})
    for value in [{1: "key"}, {"x": (1, 2)}, {"x": float("nan")}, {"x": object()}]:
        with pytest.raises(qr.QualificationError):
            qr.canonical_bytes(value)


@pytest.mark.parametrize("stamp", [
    "2026-02-30T00:00:00Z", "2026-11-26T00:00:00", "2026-11-26T00:00:60Z",
    "2026-11-26T00:00:00+24:00", "2026-11-20T00:00:00+00:60",
    "2026-11-20T00:00:00+01:99", "2026-11-20T00:00:00-00:60",
])
def test_shape_validation_checks_actual_calendar_and_offsets(stamp):
    with pytest.raises(qr.QualificationError):
        qr.validate_shape(stamp, "Timestamp")
    with pytest.raises(qr.QualificationError) as caught:
        qr.parse_timestamp(stamp)
    assert caught.value.code == "INVALID_TIMESTAMP"


@pytest.mark.parametrize("offset,seconds", [("+23:59", 86340), ("-23:59", -86340), ("+00:59", 3540), ("+01:00", 3600)])
def test_valid_explicit_offset_boundaries_are_preserved(offset, seconds):
    stamp = "2026-11-20T00:00:00" + offset
    qr.validate_shape(stamp, "Timestamp")
    assert qr.parse_timestamp(stamp).utcoffset().total_seconds() == seconds


def test_shape_validator_rejects_wrong_types_and_unknown_fields():
    with pytest.raises(qr.QualificationError):
        qr.validate_shape({"record_id": "x", "sha256": "sha256:" + "a" * 64, "established": True}, "RecordRef")
    with pytest.raises(qr.QualificationError):
        qr.validate_shape(True, "GitSha1")


def test_shape_error_detail_does_not_depend_on_dictionary_order():
    inputs = [{"x": {"a": 1, "b": 2}}, {"x": {"b": 2, "a": 1}}]
    details = []
    for value in inputs:
        with pytest.raises(qr.QualificationError) as caught:
            qr.validate_shape(value, "RecordRef")
        details.append(caught.value.detail)
    assert details[0] == details[1]


def test_artifact_reference_never_invents_bytes_or_identity():
    data = b'{"record_id":"actual"}'
    ref = qr.artifact_ref("retained.json", data, "actual", qr.git_blob_sha1(data))
    assert ref["sha256"] == qr.sha256(data)
    with pytest.raises(qr.QualificationError) as caught:
        qr.artifact_ref("retained.json", data, "invented")
    assert caught.value.code == "SCHEMA_ID_MISMATCH"
    with pytest.raises(qr.QualificationError):
        qr.artifact_ref("missing.json", None)


def test_anchor_uses_pinned_git_bytes_and_freezes_all_inputs(tmp_path):
    payload_path = "docs/catalog/payloads/payload.bin"
    repo, inventory, context, artifacts = _inputs(tmp_path, files={payload_path: b"original bytes"})
    anchor = _anchor(repo, inventory, context, artifacts)
    ref = anchor.catalog_entries[0]
    assert anchor.read(ref) == b"original bytes"
    (repo / payload_path).write_bytes(b"changed working tree")
    artifacts["fixture.json"] = b"changed input mapping"
    copy_context = anchor.context
    copy_context["context_policy"]["knowledge_cutoff"] = "2099-01-01T00:00:00Z"
    assert anchor.read(ref) == b"original bytes"
    assert anchor.context["context_policy"]["knowledge_cutoff"] == context["context_policy"]["knowledge_cutoff"]
    with pytest.raises(TypeError):
        anchor.artifacts[payload_path] = b"override"
    with pytest.raises(FrozenInstanceError):
        anchor.domain = "production"


def test_query_cannot_construct_an_anchor():
    with pytest.raises(qr.QualificationError) as caught:
        qr.EvidenceAnchor(_key=None, git=None, artifacts={}, context_ref={})
    assert caught.value.code == "CONTEXT_ANCHOR_MISMATCH"


def test_anchor_rejects_source_inventory_pruning(tmp_path):
    repo, inventory, context, artifacts = _inputs(tmp_path, files={"docs/catalog/payloads/x": b"retained"})
    inventory["entries"] = []
    with pytest.raises(qr.QualificationError) as caught:
        _anchor(repo, inventory, context, artifacts)
    assert caught.value.code == "INVENTORY_OMISSION"
    assert "docs/catalog/payloads/x" in caught.value.detail


def test_anchor_rejects_wrong_tree_without_inventing_pin(tmp_path):
    repo, inventory, context, artifacts = _inputs(tmp_path)
    inventory["root_tree_sha1"] = "0" * 40
    with pytest.raises(qr.QualificationError) as caught:
        _anchor(repo, inventory, context, artifacts)
    assert caught.value.code == "INVENTORY_PIN_MISMATCH"


def test_auxiliary_bytes_cannot_override_a_pinned_path(tmp_path):
    repo, inventory, context, artifacts = _inputs(tmp_path, files={"docs/catalog/payloads/x": b"retained"})
    artifacts["docs/catalog/payloads/x"] = b"favorable replacement"
    with pytest.raises(qr.QualificationError) as caught:
        _anchor(repo, inventory, context, artifacts)
    assert caught.value.code == "CONFLICTING_ARTIFACT_BYTES"


def test_nonnull_git_blob_requires_path_membership_not_just_equal_hash(tmp_path):
    repo, inventory, context, artifacts = _inputs(tmp_path)
    data = b"untracked auxiliary bytes"
    artifacts["auxiliary.bin"] = data
    anchor = _anchor(repo, inventory, context, artifacts)
    assert anchor.read(qr.artifact_ref("auxiliary.bin", data)) == data
    with pytest.raises(qr.QualificationError) as caught:
        anchor.read(qr.artifact_ref("auxiliary.bin", data, git_blob_sha1=qr.git_blob_sha1(data)))
    assert caught.value.code == "INVENTORY_PIN_MISMATCH"


def test_missing_artifact_is_a_typed_failure_not_a_fabricated_record(tmp_path):
    repo, inventory, context, artifacts = _inputs(tmp_path)
    anchor = _anchor(repo, inventory, context, artifacts)
    ref = qr.artifact_ref("previously-seen.bin", b"expected original bytes")
    with pytest.raises(qr.QualificationError) as caught:
        anchor.read(ref)
    assert caught.value.code == "KNOWN_SOURCE_UNAVAILABLE"
    assert "previously-seen.bin" not in anchor.artifacts


def test_conflicting_same_id_bytes_have_order_invariant_diagnostic(tmp_path):
    repo, inventory, context, artifacts = _inputs(tmp_path)
    a = qr.canonical_bytes({"record_id": "CONFLICT", "value": "a"})
    b = qr.canonical_bytes({"record_id": "CONFLICT", "value": "b"})
    messages = []
    for pairs in [(a, b), (b, a)]:
        with pytest.raises(qr.QualificationError) as caught:
            _anchor(repo, inventory, context, {**artifacts, "first.json": pairs[0], "last.json": pairs[1]})
        messages.append((caught.value.code, caught.value.detail))
    assert messages[0] == messages[1]
    assert messages[0][0] == "CONFLICTING_ARTIFACT_BYTES"


def test_identical_duplicate_record_bytes_are_idempotent(tmp_path):
    repo, inventory, context, artifacts = _inputs(tmp_path)
    a = qr.canonical_bytes({"record_id": "DUPLICATE", "value": "same"})
    anchor = _anchor(repo, inventory, context, {**artifacts, "a.json": a, "b.json": a})
    assert anchor.record(qr.record_ref("DUPLICATE", a)) == {"record_id": "DUPLICATE", "value": "same"}


def test_catalog_symlink_cannot_replace_retained_regular_bytes(tmp_path):
    repo, inventory, context, artifacts = _inputs(tmp_path)
    target = repo / "docs/catalog/payloads/link"
    target.parent.mkdir(parents=True)
    target.symlink_to("../../../README.md")
    _git(repo, "add", ".")
    _git(repo, "-c", "user.name=Qualification Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "nonregular catalog input")
    with pytest.raises(qr.QualificationError) as caught:
        qr.load_git_catalog(repo, _git(repo, "rev-parse", "HEAD"))
    assert caught.value.code == "INVENTORY_PIN_MISMATCH"


def test_atomic_publication_preserves_original_bytes_and_cleans_tempfiles(tmp_path):
    target = tmp_path / "nested" / "assessment.json"
    qr._publish_no_replace(target, b"complete first record")
    qr._publish_no_replace(target, b"complete first record")
    with pytest.raises(qr.QualificationError) as caught:
        qr._publish_no_replace(target, b"different record")
    assert caught.value.code == "CONFLICTING_ARTIFACT_BYTES"
    assert target.read_bytes() == b"complete first record"
    assert list(target.parent.glob(".assessment-*")) == []


def test_interrupted_publication_does_not_publish_partial_bytes(tmp_path, monkeypatch):
    target = tmp_path / "assessment.json"
    def fail_link(*_args):
        raise OSError("simulated publication failure")
    monkeypatch.setattr(qr.os, "link", fail_link)
    with pytest.raises(OSError):
        qr._publish_no_replace(target, b"complete but unpublished")
    assert not target.exists()
    assert list(tmp_path.glob(".assessment-*")) == []


def test_invalid_result_envelope_cannot_be_published_as_an_assessment(tmp_path):
    corpus = json.loads((qr.SCHEMA_PATH.parent / "SCHEMA-EXAMPLES.json").read_text())
    invalid_result = next(case["document"] for case in corpus["schema_cases"] if case["case_id"] == "valid-typed-invalid-envelope")
    qr.validate_shape(invalid_result, "AssessmentResult")
    with pytest.raises(qr.QualificationError) as caught:
        qr.write_assessment(invalid_result, anchor=None, query_bytes=b"{}", output_dir=tmp_path)
    assert caught.value.code == "INVALID_SCHEMA"
    assert list(tmp_path.iterdir()) == []


@pytest.fixture
def evaluated_model_fixture(tmp_path):
    from qualification_fixtures import build_fixture, encode
    from ai_lab.providers.qualification import evaluate_synthetic_r2

    fixture = build_fixture(tmp_path / "model-fixture")
    anchor = fixture.anchor()
    result = evaluate_synthetic_r2(fixture.query, anchor=anchor)
    assert result["validation_status"] == "valid"
    assert result["Q_identity"]["value"] == "conditions_satisfied"
    return anchor, encode(fixture.query), result


def test_assessment_store_recomputes_and_identical_replay_is_idempotent(tmp_path, evaluated_model_fixture):
    anchor, query_bytes, result = evaluated_model_fixture
    target = qr.write_assessment(result, anchor=anchor, query_bytes=query_bytes, output_dir=tmp_path / "store")
    again = qr.write_assessment(copy.deepcopy(result), anchor=anchor, query_bytes=query_bytes, output_dir=tmp_path / "store")
    assert target == again
    assert target.read_bytes() == qr.canonical_bytes(result)
    assert target.name == qr.sha256(target.read_bytes())[7:] + ".json"
    assert result["C3"]["value"] == result["C10"]["value"] == result["Q_C3_C10"]["value"] == "unresolved"


def test_shape_valid_forged_assessment_cannot_be_published(tmp_path, evaluated_model_fixture):
    anchor, query_bytes, result = evaluated_model_fixture
    forged = copy.deepcopy(result)
    forged["source_findings"][0]["applicability"] = "inapplicable"
    qr.validate_shape(forged, "AssessmentResult")
    with pytest.raises(qr.QualificationError) as caught:
        qr.write_assessment(forged, anchor=anchor, query_bytes=query_bytes, output_dir=tmp_path / "store")
    assert caught.value.code == "CONTEXT_ANCHOR_MISMATCH"
    assert not (tmp_path / "store").exists()


def test_synthetic_result_cannot_be_published_in_production_domain(tmp_path, evaluated_model_fixture):
    anchor, query_bytes, result = evaluated_model_fixture
    forged = copy.deepcopy(result)
    forged["domain"] = "production"
    forged["entry_point"] = "evaluate_production_r2"
    forged["Q_identity"]["value"] = "withheld"
    qr.validate_shape(forged, "AssessmentResult")
    with pytest.raises(qr.QualificationError) as caught:
        qr.write_assessment(forged, anchor=anchor, query_bytes=query_bytes, output_dir=tmp_path / "store")
    assert caught.value.code == "DOMAIN_MISMATCH"
    assert not (tmp_path / "store").exists()


def test_synthetic_assessment_store_cannot_enter_production_checkout(tmp_path, evaluated_model_fixture, monkeypatch):
    anchor, query_bytes, result = evaluated_model_fixture
    isolated_checkout = tmp_path / "checkout"
    monkeypatch.setattr(qr, "__file__", str(isolated_checkout / "ai_lab/providers/qualification_records.py"))
    with pytest.raises(qr.QualificationError) as caught:
        qr.write_assessment(result, anchor=anchor, query_bytes=query_bytes, output_dir=isolated_checkout / "docs/catalog")
    assert caught.value.code == "DOMAIN_MISMATCH"
    assert not isolated_checkout.exists()


@pytest.mark.parametrize("occupied", ["object", "display_id"])
def test_accepted_assessment_cannot_overwrite_conflicting_store_bytes(tmp_path, evaluated_model_fixture, occupied):
    anchor, query_bytes, result = evaluated_model_fixture
    store = tmp_path / "store"
    target = qr.write_assessment(result, anchor=anchor, query_bytes=query_bytes, output_dir=store)
    occupied_path = target if occupied == "object" else next((store / "synthetic/by-id").glob("*.json"))
    occupied_path.write_bytes(b"preexisting different bytes")
    with pytest.raises(qr.QualificationError) as caught:
        qr.write_assessment(result, anchor=anchor, query_bytes=query_bytes, output_dir=store)
    assert caught.value.code == "CONFLICTING_ARTIFACT_BYTES"
    assert occupied_path.read_bytes() == b"preexisting different bytes"
