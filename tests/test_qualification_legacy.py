"""A3 boundary tests. Mocked assessments isolate adapters, never prove identity.

The real evaluator/anchor tests independently establish the model mechanism.
Here a deliberately favorable schema-valid engine result exercises projection
and persistence guards that must remain blocking even if the new engine clears
its synthetic identity subcondition.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import types

import pytest

from ai_lab.providers.catalog import build_capture, build_model_identity, build_snapshot, build_assertion, build_endpoint_identity
from ai_lab.providers.catalog_resolution import (
    LEGACY_CONTEXT_REQUIRED, LEGACY_POSITIVE_DISABLED, ResolutionError,
    build_resolution_record, canonical_resolution_json, resolve_identity,
    resolution_relations, validate_resolution_record, write_resolution_record,
)
from ai_lab.providers.executor_equivalence import NON_EQUIVALENT, UNRESOLVED, equivalence
from ai_lab.providers.qualification_records import (
    artifact_ref, canonical_bytes, record_ref, sha256,
)

REPO = Path(__file__).resolve().parents[1]


def _case(case_id):
    corpus = json.loads((REPO / "docs/reviews/qualification_semantics/r2/SCHEMA-EXAMPLES.json").read_text())
    return copy.deepcopy(next(c["document"] for c in corpus["schema_cases"] if c["case_id"] == case_id))


@pytest.fixture
def boundary(monkeypatch):
    stored = sorted((REPO / "docs/invocations").glob("INV-*.json"))
    left, right = [json.loads(p.read_text()) for p in stored[:2]]
    query = _case("valid-Query")
    blobs = {}
    for side, inv in (("left", left), ("right", right)):
        data = canonical_bytes(inv)
        ref = artifact_ref(f"fixtures/{side}.json", data, inv["invocation_id"])
        blobs[ref["path"]] = data
        query[side] = {
            "invocation_ref": ref, "kind": inv["executor"]["kind"],
            "executor_reference": inv["executor"]["reference"],
            "occurred_at": inv["occurred_at"],
            "requested_model_name": inv["requested_model_name"],
            "service_endpoint": inv["service_endpoint"],
        }
    result = _case("valid-AssessmentResult")
    result["query_ref"] = record_ref(query["query_id"], canonical_bytes(query))
    result["evidence_context_ref"] = copy.deepcopy(query["evidence_context_ref"])
    calls = []

    class ReadDouble:
        # This is an isolated adapter test double, not a production anchor.
        domain = "synthetic"

        def read(self, ref):
            data = blobs[ref["path"]]
            assert sha256(data) == ref["sha256"]
            return data

    module = types.ModuleType("ai_lab.providers.qualification")
    def evaluate(query_arg, *, anchor):
        calls.append((copy.deepcopy(query_arg), anchor))
        return copy.deepcopy(result)
    module.evaluate_synthetic_r2 = evaluate
    module.evaluate_production_r2 = evaluate
    monkeypatch.setitem(sys.modules, module.__name__, module)
    return left, right, query, ReadDouble(), result, calls, module


def test_checked_full_context_still_never_projects_positive_legacy_resolution(boundary):
    left, _, query, anchor, result, calls, _ = boundary
    out = resolve_identity(invocation=left, snapshot={}, capture={}, query=query, anchor=anchor)
    assert len(calls) == 1
    assert out["resolved"] is False and out["resolved_identity"] is None
    assert out["reason"] == LEGACY_POSITIVE_DISABLED
    assert out["assessment_ref"] == record_ref(result["assessment_id"], canonical_bytes(result))
    with pytest.raises(ResolutionError, match="r2 assessment/refusal"):
        build_resolution_record(invocation=left, outcome=out, resolved_at=left["occurred_at"])


def test_checked_equivalence_can_project_relation_but_never_permission(boundary):
    left, right, query, anchor, result, calls, _ = boundary
    out = equivalence(left=left, right=right, snapshots=[], query=query, anchor=anchor)
    assert len(calls) == 1
    assert out.status == NON_EQUIVALENT
    assert out.assessment_ref == record_ref(result["assessment_id"], canonical_bytes(result))
    assert out.blocks_adjudication is True


@pytest.mark.parametrize("change", ["extra_field", "occurred_at", "requested_model_name", "executor"])
def test_legacy_arguments_must_equal_the_complete_retained_invocation(boundary, change):
    left, right, query, anchor, _, calls, _ = boundary
    changed = copy.deepcopy(left)
    changed[change] = "not the retained value"
    out = equivalence(left=changed, right=right, snapshots=[], query=query, anchor=anchor)
    assert not calls
    assert out.status == UNRESOLVED and out.blocks_adjudication is True
    assert out.assessment_ref is None
    assert "CONTEXT_ANCHOR_MISMATCH" in out.diagnostic_codes


def test_wrong_subject_order_cannot_borrow_another_query(boundary):
    left, right, query, anchor, _, calls, _ = boundary
    assert left != right
    out = equivalence(left=right, right=left, snapshots=[], query=query, anchor=anchor)
    assert not calls
    assert out.status == UNRESOLVED and out.blocks_adjudication is True


@pytest.mark.parametrize("failure", [RuntimeError, ImportError, ValueError])
def test_disabled_or_failing_engine_never_recovers_old_permitting_path(boundary, failure):
    left, right, query, anchor, _, _, module = boundary
    def fail(*args, **kwargs):
        raise failure("disabled evaluator")
    module.evaluate_synthetic_r2 = fail
    out = equivalence(left=left, right=right, snapshots=[], query=query, anchor=anchor)
    assert out.status == UNRESOLVED and out.blocks_adjudication is True
    assert out.assessment_ref is None
    assert out.diagnostic_codes == ("NOT_EVALUATED",)


def test_assessment_for_another_query_is_not_a_projection_source(boundary):
    left, right, query, anchor, result, _, _ = boundary
    result["query_ref"]["sha256"] = "sha256:" + "0" * 64
    out = equivalence(left=left, right=right, snapshots=[], query=query, anchor=anchor)
    assert out.status == UNRESOLVED and out.blocks_adjudication is True
    assert out.assessment_ref is None
    assert out.diagnostic_codes == ("CONTEXT_ANCHOR_MISMATCH",)


def test_malformed_assessment_cannot_be_projected(boundary):
    left, right, query, anchor, result, _, _ = boundary
    result["R_identity"] = {"value": NON_EQUIVALENT}
    out = equivalence(left=left, right=right, snapshots=[], query=query, anchor=anchor)
    assert out.status == UNRESOLVED and out.blocks_adjudication is True
    assert out.assessment_ref is None


def _historical():
    identity = build_model_identity(originator_id="fixture", canonical_name="model", release_identity="r1")
    endpoint = build_endpoint_identity(operating_organization="fixture", endpoint_identifier="fixture.endpoint")
    assertion = build_assertion(assertion_subject="model", assertion_predicate="resolves_to",
                                assertion_value_or_target=identity["record_id"],
                                valid_from="2026-07-01T00:00:00+00:00", source="fixture")
    snapshot = build_snapshot(service_endpoint_id=endpoint["record_id"], observed_at="2026-07-01T00:00:00+00:00", assertions=[assertion], source_set="fixture")
    capture = build_capture(snapshot_id=snapshot["record_id"], capture_method="fixture", source_type="provider_self_report",
                            captured_at=snapshot["observed_at"], capture_success=True, capturing_executor="fixture",
                            payload="fixture", content_evidence_status="self_asserted", channel_authentication_status="unverifiable")
    invocation = {"invocation_id": "INV-1111111111111111", "requested_model_name": "model", "service_endpoint": "fixture.endpoint"}
    outcome = {"resolved": True, "resolved_identity": identity["record_id"], "snapshot_id": snapshot["record_id"],
               "capture_id": capture["record_id"], "content_evidence_status": "self_asserted",
               "channel_authentication_status": "unverifiable"}
    return invocation, outcome


@pytest.mark.parametrize("value", ["false", "true", 1, 0, None])
def test_new_v1_builder_never_coerces_resolved_to_boolean(value):
    inv, outcome = _historical()
    outcome["resolved"] = value
    with pytest.raises(ResolutionError, match="coercion is forbidden"):
        build_resolution_record(invocation=inv, outcome=outcome, resolved_at="2026-07-02T00:00:00+00:00")


@pytest.mark.parametrize("field,value", [
    ("resolved_identity", 7), ("resolved_identity", "EID-1111111111111111"),
    ("snapshot_id", "SNAP-not-valid"), ("capture_id", "CAP-not-valid"),
    ("content_evidence_status", "established"), ("content_evidence_status", []),
    ("channel_authentication_status", "independently_corroborated"), ("channel_authentication_status", {}),
])
def test_new_v1_builder_rejects_fabricated_positive_projection_shapes(field, value):
    inv, outcome = _historical()
    outcome[field] = value
    with pytest.raises(ResolutionError):
        build_resolution_record(invocation=inv, outcome=outcome, resolved_at="2026-07-02T00:00:00+00:00")


def test_r2_refusal_and_assessment_cannot_be_written_as_historical_records(tmp_path, boundary):
    left, _, query, anchor, result, _, _ = boundary
    refusal = resolve_identity(invocation=left, snapshot={}, capture={}, query=query, anchor=anchor)
    for value in (refusal, result):
        with pytest.raises(ResolutionError):
            validate_resolution_record(value)
        with pytest.raises(ResolutionError):
            write_resolution_record(value, tmp_path)
    assert not list(tmp_path.rglob("*.json"))


def test_historical_graph_and_idempotent_storage_do_not_upgrade_standing(tmp_path):
    inv, outcome = _historical()
    record = build_resolution_record(invocation=inv, outcome=outcome, resolved_at="2026-07-02T00:00:00+00:00")
    before = canonical_resolution_json(record)
    path = write_resolution_record(record, tmp_path)
    assert path == write_resolution_record(record, tmp_path)
    assert path.read_text() == before
    assert all(edge.authoritative is False for edge in resolution_relations(record))
    assert not list(path.parent.glob(".resolution-*"))


def test_same_legacy_id_with_changed_bytes_cannot_overwrite_history(tmp_path):
    inv, outcome = _historical()
    record = build_resolution_record(invocation=inv, outcome=outcome, resolved_at="2026-07-02T00:00:00+00:00")
    path = write_resolution_record(record, tmp_path)
    before = path.read_bytes()
    changed = copy.deepcopy(record)
    changed["resolved_identity"] = "MID-0000000000000000"
    assert changed["record_id"] == record["record_id"]
    with pytest.raises(ResolutionError, match="already names different bytes"):
        write_resolution_record(changed, tmp_path)
    assert path.read_bytes() == before
    assert not list(path.parent.glob(".resolution-*"))


def test_failed_atomic_publication_leaves_no_valid_record(tmp_path, monkeypatch):
    import ai_lab.providers.catalog_resolution as legacy
    inv, outcome = _historical()
    record = build_resolution_record(invocation=inv, outcome=outcome, resolved_at="2026-07-02T00:00:00+00:00")
    def fail(*args, **kwargs):
        raise OSError("simulated failed publication")
    monkeypatch.setattr(legacy.os, "link", fail)
    with pytest.raises(OSError, match="failed publication"):
        write_resolution_record(record, tmp_path)
    assert not list(tmp_path.rglob("*.json"))
    assert not list(tmp_path.rglob(".resolution-*"))


@pytest.mark.parametrize("window", [-1, True, "30"])
def test_new_historical_annotation_rejects_invalid_freshness_types(window):
    inv, outcome = _historical()
    with pytest.raises(ResolutionError, match="nonnegative integer"):
        build_resolution_record(invocation=inv, outcome=outcome,
                                resolved_at="2026-07-02T00:00:00+00:00",
                                freshness_window_days=window)
