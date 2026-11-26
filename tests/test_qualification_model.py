"""Admitted 3A behavior: exact synthetic premises, omissions and refusal paths.

F-family labels refer to the retained r2 matrix; these are executed test oracles,
not live identity/independence evidence or a claim that all48 families are done.
"""
from __future__ import annotations

import copy
from datetime import datetime, timedelta
import itertools
import json

import pytest

from ai_lab.providers.catalog import build_endpoint_identity
from ai_lab.providers.qualification import (
    canonicalize_reasons, evaluate_production_r2, evaluate_synthetic_r2,
)
from ai_lab.providers.qualification_records import QualificationError, validate_shape
from qualification_fixtures import (
    EVENT, LATE, OBSERVED, SOURCE_AVAILABLE,
    build_fixture, digest, encode, extra_source, invocation, ref, refresh_source_ids,
)


def codes(value):
    out = set()
    if isinstance(value, dict):
        if isinstance(value.get("code"), str): out.add(value["code"])
        for x in value.values(): out.update(codes(x))
    elif isinstance(value, list):
        for x in value: out.update(codes(x))
    return out


def blocked(out, *, relation=True):
    assert out["Q_identity"]["value"] == "withheld"
    if relation: assert out["R_identity"]["value"] == "unresolved"
    for field in ("C3", "C10", "Q_C3_C10"):
        assert out[field]["value"] == "unresolved"
    validate_shape(out, "AssessmentResult")


def typed_refusal(bundle):
    """A loader refusal and an evaluator invalid-result are distinct legal phases."""
    try:
        out = bundle.evaluate()
    except QualificationError as error:
        assert isinstance(error.code, str) and error.code
        return {error.code}
    blocked(out)
    assert out["validation_status"] == "invalid"
    assert out["validation_reasons"]
    return codes(out)


def rewrite_witness(bundle, side, mutate, *, update_row=True):
    path = f"fixture/witness-{side}.json"
    witness = json.loads(bundle.artifacts[path])
    mutate(witness)
    bundle.rewrite_aux(path, witness, update_fixture_row=update_row)


def test_f01_f43_clean_synthetic_controls(tmp_path):
    f = build_fixture(tmp_path)
    out = f.evaluate()
    assert out["validation_status"] == "valid"
    assert out["supplied_relation"]["value"] == "non_equivalent"
    assert out["R_identity"]["value"] == "non_equivalent"
    assert out["Q_identity"]["value"] == "conditions_satisfied"
    assert out["coverage"]["value"] == "pinned_inventory_exhausted"
    assert len(out["corroboration_witness_refs"]) == 2
    for name in ("C3", "C10", "Q_C3_C10"):
        assert out[name]["value"] == "unresolved"
    validate_shape(out, "AssessmentResult")


@pytest.mark.parametrize("left,right", list(itertools.product(["valid", "missing", "mismatched"], repeat=2)))
def test_f43_complete_witness_pair_matrix(tmp_path, left, right):
    out = build_fixture(tmp_path, witness_states=(left, right)).evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    expected = "conditions_satisfied" if left == right == "valid" else "withheld"
    assert out["Q_identity"]["value"] == expected
    assert out["Q_C3_C10"]["value"] == "unresolved"


@pytest.mark.parametrize("left,right", list(itertools.product(
    ["self_asserted", "unassessed", "independently_corroborated", "contradicted"], repeat=2)))
def test_f02_f24_f43_evidence_class_pair_matrix(tmp_path, left, right):
    out = build_fixture(tmp_path, evidence_classes=(left, right)).evaluate()
    expected = "conditions_satisfied" if left == right == "independently_corroborated" else "withheld"
    assert out["Q_identity"]["value"] == expected
    if "contradicted" in (left, right):
        assert out["R_identity"]["value"] == "unresolved"
        assert out["supplied_relation"]["value"] == "unresolved"
        assert "CAPTURE_CONTRADICTED" in codes(out)


def test_f01_same_mid_is_catalog_equivalence_not_permission(tmp_path):
    def change(s):
        s["sources"][1]["snapshot"]["assertions"][0]["assertion_value_or_target"] = s["models"][0]["record_id"]
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    assert out["R_identity"]["value"] == "equivalent"
    blocked(out, relation=False)


@pytest.mark.parametrize("releases", [("unknown", "release-1"), ("release-0", "unknown"), ("unknown", "unknown")])
def test_f35_unknown_release_blocks_identity_not_catalog_relation(tmp_path, releases):
    out = build_fixture(tmp_path, release_identities=releases).evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    assert "TARGET_RELEASE_UNKNOWN" in codes(out)
    blocked(out, relation=False)


def test_f14_wrong_endpoint_cannot_resolve_same_requested_name(tmp_path):
    def change(s):
        s["sources"][0]["snapshot"]["service_endpoint_id"] = s["endpoints"][1]["record_id"]
        refresh_source_ids(s["sources"][0])
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert out["supplied_relation"]["value"] == "unresolved"
    assert "WRONG_ENDPOINT" in codes(out)


def test_f14_same_requested_name_binds_distinct_endpoint_targets(tmp_path):
    def change(s):
        s["invocations"][1] = invocation(1, name=s["invocations"][0]["requested_model_name"])
        s["sources"][1]["snapshot"]["assertions"][0]["assertion_subject"] = s["invocations"][0]["requested_model_name"]
    f = build_fixture(tmp_path, catalog_mutator=change)
    out = f.evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    assert out["Q_identity"]["value"] == "conditions_satisfied"
    assert out["R_identity"]["left_identity"]["identity_ref"] == f.state["models"][0]["record_id"]
    assert out["R_identity"]["right_identity"]["identity_ref"] == f.state["models"][1]["record_id"]


def test_f15_unknown_endpoint_has_no_nonempty_string_fallback(tmp_path):
    def change(s): s["invocations"][0] = invocation(0, endpoint="unbound.endpoint")
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert out["supplied_relation"]["value"] == "unresolved"
    assert "ENDPOINT_MAPPING_UNRESOLVED" in codes(out)


def test_f16_colliding_endpoint_spelling_is_unresolved(tmp_path):
    def change(s):
        s["extra_records"].append(build_endpoint_identity(operating_organization="fixture:collision",
            endpoint_identifier=s["endpoints"][0]["endpoint_identifier"]))
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert "ENDPOINT_MAPPING_UNRESOLVED" in codes(out)


def test_f32_failed_capture_cannot_supply_positive_or_name_absence(tmp_path):
    def change(s): s["sources"][0]["capture"]["capture_success"] = False
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert out["supplied_relation"]["value"] == "unresolved"
    assert "CAPTURE_UNSUCCESSFUL" in codes(out)


def test_f32_proven_irrelevant_failed_capture_is_not_global_veto(tmp_path):
    def change(s):
        s["endpoints"].append(build_endpoint_identity(operating_organization="fixture:irrelevant",
            endpoint_identifier="neither-invocation-endpoint"))
        e = extra_source(s, side=0, endpoint=2, name="irrelevant-failed")
        e["capture"]["capture_success"] = False
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    assert out["Q_identity"]["value"] == "conditions_satisfied"
    assert "WRONG_ENDPOINT" in codes(out)


@pytest.mark.parametrize("chronology_valid", [False, True])
def test_f38_availability_chronology_checked_before_endpoint_exclusion(tmp_path, chronology_valid):
    def change(s):
        s["endpoints"].append(build_endpoint_identity(operating_organization="fixture:irrelevant",
            endpoint_identifier="neither-invocation-endpoint"))
        source = extra_source(s, side=0, endpoint=2, name="irrelevant-chronology")
        if not chronology_valid:
            source["available_at"] = (datetime.fromisoformat(OBSERVED) - timedelta(microseconds=1)).isoformat()
    f = build_fixture(tmp_path, catalog_mutator=change)
    if chronology_valid:
        out = f.evaluate()
        assert out["validation_status"] == "valid"
        assert out["Q_identity"]["value"] == "conditions_satisfied"
    else:
        assert "INVALID_TIMESTAMP" in typed_refusal(f)


def test_f38_non_json_linked_availability_invalid_before_endpoint_exclusion(tmp_path):
    def change(s):
        s["endpoints"].append(build_endpoint_identity(operating_organization="fixture:irrelevant",
            endpoint_identifier="neither-invocation-endpoint"))
        extra_source(s, side=0, endpoint=2, name="irrelevant-invalid-availability")
    f = build_fixture(tmp_path, catalog_mutator=change)
    availability = f.source_refs[2]["availability_evidence_refs"][0]
    # ArtifactRef permits a null record ID. Keep this raw-artifact path from
    # being rejected earlier by the separate named-record identity guard.
    availability["record_id"] = None
    f.rewrite_aux(availability["path"], b"this retained linked availability is not JSON")
    # Every reference hashes the new actual bytes. This is semantic parsing,
    # rather than a missing-artifact or digest-mismatch rejection.
    assert availability["sha256"] == digest(f.artifacts[availability["path"]])
    assert "INVALID_SCHEMA" in typed_refusal(f)


def test_f32_string_false_is_not_boolean_capture_success(tmp_path):
    def change(s): s["sources"][0]["capture"]["capture_success"] = "false"
    assert "INVALID_SCHEMA" in typed_refusal(build_fixture(tmp_path, catalog_mutator=change))


def test_f31_provider_self_report_cannot_claim_corroboration(tmp_path):
    def change(s):
        s["sources"][0]["capture"]["source_type"] = "provider_self_report"
        refresh_source_ids(s["sources"][0])
    assert "INVALID_SCHEMA" in typed_refusal(build_fixture(tmp_path, catalog_mutator=change))


@pytest.mark.parametrize("target", [True, False, 0, 1, 7, 1.5, "", "arbitrary-name", None, ["MID-0000000000000000"]])
def test_f33_invalid_target_domain_is_typed_before_sets(tmp_path, target):
    def change(s): s["sources"][0]["snapshot"]["assertions"][0]["assertion_value_or_target"] = target
    found = typed_refusal(build_fixture(tmp_path, catalog_mutator=change))
    assert found & {"ASSERTION_TARGET_INVALID", "INVALID_SCHEMA"}


@pytest.mark.parametrize("missing", ["payload", "snapshot", "mid"])
def test_f34_missing_chain_never_invents_refs(tmp_path, missing):
    def change(s):
        if missing == "mid": s["missing_model_ids"].add(s["models"][0]["record_id"])
        else: s["sources"][0][missing + "_present"] = False
    f = build_fixture(tmp_path, catalog_mutator=change)
    if missing == "payload": assert f.source_refs[0]["payload_ref"] is None
    if missing == "mid": assert f.source_refs[0]["target_refs"] == []
    if missing == "snapshot": assert len(f.source_refs) == 1
    found = typed_refusal(f)
    assert found & {"TARGET_MISSING", "INVENTORY_OMISSION", "INVALID_SCHEMA", "CAPTURE_SNAPSHOT_MISMATCH", "KNOWN_SOURCE_UNAVAILABLE"}


def test_f34_existing_endpoint_is_not_a_model_target(tmp_path):
    def change(s): s["sources"][0]["snapshot"]["assertions"][0]["assertion_value_or_target"] = s["endpoints"][0]["record_id"]
    assert "TARGET_WRONG_KIND" in typed_refusal(build_fixture(tmp_path, catalog_mutator=change))


def test_f34_payload_hash_mismatch_is_not_corroboration(tmp_path):
    def change(s): s["sources"][0]["payload"] = b'{"different_payload":true}'
    assert "ARTIFACT_DIGEST_MISMATCH" in typed_refusal(build_fixture(tmp_path, catalog_mutator=change))


def test_f28_capture_snapshot_reference_mismatch_is_typed(tmp_path):
    def change(f): f.inventory["model_sources"][0]["snapshot_ref"] = f.source_refs[1]["snapshot_ref"]
    assert "CAPTURE_SNAPSHOT_MISMATCH" in typed_refusal(build_fixture(tmp_path, contract_mutator=change))


def test_f36_null_scope_control_and_unsupported_scope(tmp_path):
    def change(s): s["sources"][0]["snapshot"]["assertions"][0]["scope"] = "unsupported-region"
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert out["supplied_relation"]["value"] == "unresolved"
    assert "ASSERTION_SCOPE_UNSUPPORTED" in codes(out)


def test_f37_reversed_interval_is_invalid_not_no_assertion(tmp_path):
    def change(s): s["sources"][0]["snapshot"]["assertions"][0]["valid_until"] = "2026-11-19T00:00:00+00:00"
    assert "INVALID_INTERVAL" in typed_refusal(build_fixture(tmp_path, catalog_mutator=change))


def test_f37_zero_length_assertion_interval_is_inclusive(tmp_path):
    def change(s):
        a = s["sources"][0]["snapshot"]["assertions"][0]
        a["valid_from"] = a["valid_until"] = EVENT
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    assert out["Q_identity"]["value"] == "conditions_satisfied"


@pytest.mark.parametrize("extra_microsecond,expected", [(False, "non_equivalent"), (True, "unresolved")])
def test_f20_freshness_inclusive_boundary(tmp_path, extra_microsecond, expected):
    observed = datetime.fromisoformat(EVENT) - timedelta(days=30, microseconds=int(extra_microsecond))
    def change(s):
        s["sources"][0]["snapshot"]["observed_at"] = observed.isoformat()
        refresh_source_ids(s["sources"][0])
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    assert out["R_identity"]["value"] == expected
    if extra_microsecond: assert "FRESHNESS_EXPIRED" in codes(out)


def test_f38_capture_before_observation_is_invalid(tmp_path):
    def change(s):
        s["sources"][0]["capture"]["captured_at"] = "2026-11-19T00:00:00+00:00"
        refresh_source_ids(s["sources"][0])
    assert "INVALID_TIMESTAMP" in typed_refusal(build_fixture(tmp_path, catalog_mutator=change))


@pytest.mark.parametrize("exclusion", ["expired_observation", "future_observation", "expired_assertion"])
def test_f19_time_proven_irrelevant_contradiction_is_excluded(tmp_path, exclusion):
    def change(s):
        source = extra_source(s, side=0, target=1, evidence="contradicted", name="time-irrelevant")
        if exclusion == "expired_observation":
            source["snapshot"]["observed_at"] = "2026-09-01T00:00:00+00:00"
        elif exclusion == "future_observation":
            source["snapshot"]["observed_at"] = LATE
            source["capture"]["captured_at"] = LATE
            source["available_at"] = LATE
        else:
            source["snapshot"]["assertions"][0]["valid_until"] = SOURCE_AVAILABLE
        refresh_source_ids(source)
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    assert out["validation_status"] == "valid"
    assert out["R_identity"]["value"] == "non_equivalent"
    assert out["Q_identity"]["value"] == "conditions_satisfied"


def test_f38_absent_source_availability_preserves_only_diagnostic(tmp_path):
    def change(s): s["sources"][0]["availability"] = False
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert out["supplied_relation"]["value"] == "non_equivalent"
    assert "EVENT_AVAILABILITY_UNPROVEN" in codes(out)


def test_f38_source_after_bound_is_exclusion_not_timestamp_error(tmp_path):
    def change(s): s["sources"][0]["available_at"] = LATE
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert out["validation_status"] == "valid"
    assert "EVIDENCE_AFTER_CUTOFF" in codes(out)
    assert "INVALID_TIMESTAMP" not in codes(out)


def test_a1_f38_late_witness_not_cleared_by_early_assessed_at(tmp_path):
    f = build_fixture(tmp_path)
    path = "fixture/witness-availability-0.json"
    av = json.loads(f.artifacts[path]); av["available_at"] = LATE
    f.rewrite_aux(path, av)
    out = f.evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    blocked(out, relation=False)
    assert "EVIDENCE_AFTER_CUTOFF" in codes(out)


def test_a1_f38_missing_witness_availability_is_not_assessed_at(tmp_path):
    def change(f):
        f.fixture["model_witness_profile"]["availability_rows"] = [r for r in f.fixture["model_witness_profile"]["availability_rows"] if r["availability_id"] != "AV-witness-0"]
    out = build_fixture(tmp_path, contract_mutator=change).evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    blocked(out, relation=False)
    assert "EVENT_AVAILABILITY_UNPROVEN" in codes(out)


def test_a1_f43_borrowed_corroboration_label_cannot_qualify_other_chain(tmp_path):
    def change(s): extra_source(s, side=0, evidence="independently_corroborated", name="corroborated-alternative")
    out = build_fixture(tmp_path, catalog_mutator=change,
        evidence_classes=("self_asserted", "independently_corroborated")).evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    blocked(out, relation=False)


def test_a1_f43_witness_on_exact_alternative_chain_positive_control(tmp_path):
    def change(s): extra_source(s, side=0, evidence="independently_corroborated", name="corroborated-alternative")
    f = build_fixture(tmp_path, catalog_mutator=change,
        evidence_classes=("self_asserted", "independently_corroborated"))
    source = f.source_refs[2]
    chain = [source["capture_ref"], source["snapshot_ref"], source["payload_ref"], source["target_refs"][0]]
    verification = json.loads(f.artifacts["fixture/verification-0.json"])
    verification["evidence_refs"] = chain
    f.rewrite_aux("fixture/verification-0.json", verification)
    rewrite_witness(f, 0, lambda w: w.update(evidence_refs=chain))
    out = f.evaluate()
    assert out["validation_status"] == "valid"
    assert out["Q_identity"]["value"] == "conditions_satisfied"
    assert len(out["corroboration_witness_refs"]) == 2


def test_a1_f43_verification_premise_is_bound_to_exact_chain(tmp_path):
    f = build_fixture(tmp_path)
    # Both digest and pinned proof row are updated: this tests decoded semantics.
    right_premise = json.loads(f.artifacts["fixture/verification-1.json"])
    f.rewrite_aux("fixture/verification-0.json", right_premise)
    out = f.evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    blocked(out, relation=False)
    assert "WITNESS_EVIDENCE_MISMATCH" in codes(out)


def test_a1_f43_witness_payload_from_other_side_is_rejected(tmp_path):
    f = build_fixture(tmp_path)
    right_payload = f.source_refs[1]["payload_ref"]
    premise = json.loads(f.artifacts["fixture/verification-0.json"])
    premise["evidence_refs"][2] = right_payload
    f.rewrite_aux("fixture/verification-0.json", premise)
    def change(w): w["evidence_refs"][2] = right_payload
    rewrite_witness(f, 0, change)
    out = f.evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    blocked(out, relation=False)
    assert "WITNESS_EVIDENCE_MISMATCH" in codes(out)


@pytest.mark.parametrize("field", ["requested_model_name", "event_at", "endpoint_ref", "target_model_ref"])
def test_f43_exact_witness_property_binding(tmp_path, field):
    f = build_fixture(tmp_path)
    def change(w):
        if field == "requested_model_name": w["subject"][field] = "another-model"
        elif field == "event_at": w["subject"][field] = OBSERVED
        else: w["subject"][field] = f.witnesses[1]["subject"][field]
    rewrite_witness(f, 0, change)
    out = f.evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    blocked(out, relation=False)
    expected = "WITNESS_MISSING" if field == "requested_model_name" else "WITNESS_SCOPE_MISMATCH"
    assert expected in codes(out)


def test_f43_exact_row_not_merely_witness_label(tmp_path):
    f = build_fixture(tmp_path)
    rewrite_witness(f, 0, lambda w: w.update(assessed_at=SOURCE_AVAILABLE), update_row=False)
    out = f.evaluate()
    blocked(out, relation=False)
    assert out["R_identity"]["value"] == "non_equivalent"


def test_f43_unknown_property_is_not_model_identity_evidence(tmp_path):
    f = build_fixture(tmp_path)
    rewrite_witness(f, 0, lambda w: w["subject"].update(property_id="independent_executor"))
    assert "INVALID_SCHEMA" in typed_refusal(f)


@pytest.mark.parametrize("field", ["verifier_executor_ref", "verifier_version_ref", "rule_version_ref", "assessment_scope_ref"])
def test_f43_proof_row_pins_checker_rule_version_and_scope(tmp_path, field):
    f = build_fixture(tmp_path)
    rewrite_witness(f, 0, lambda w: w.update({field: f.refs["fixture/observer.json"]}), update_row=False)
    out = f.evaluate()
    blocked(out, relation=False)
    assert "WITNESS_EVIDENCE_MISMATCH" in codes(out)


@pytest.mark.parametrize("offset,qualified", [(0, False), (1, True)])
def test_f43_witness_revocation_boundary(tmp_path, offset, qualified):
    f = build_fixture(tmp_path)
    revoked = (datetime.fromisoformat(EVENT) + timedelta(microseconds=offset)).isoformat()
    rewrite_witness(f, 0, lambda w: w["applicable_interval"].update(revoked_at=revoked))
    out = f.evaluate()
    assert out["Q_identity"]["value"] == ("conditions_satisfied" if qualified else "withheld")


@pytest.mark.parametrize("field,time_field", [("witness_rows", "assessed_at"), ("availability_rows", "available_at")])
def test_f43_duplicate_conflicting_fixture_row_identity_is_invalid(tmp_path, field, time_field):
    def change(f):
        rows = f.fixture["model_witness_profile"][field]
        contradictory = copy.deepcopy(rows[0]); contradictory[time_field] = LATE
        rows.append(contradictory)
    assert "CONFLICTING_ARTIFACT_BYTES" in typed_refusal(build_fixture(tmp_path, contract_mutator=change))


def test_f22_relevant_contradiction_survives_clean_source(tmp_path):
    def change(s): extra_source(s, side=0, target=1, evidence="contradicted", name="adverse")
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert out["supplied_relation"]["value"] == "unresolved"
    assert "CAPTURE_CONTRADICTED" in codes(out)


def test_f23_ambiguity_survives_clean_source(tmp_path):
    def change(s):
        e = extra_source(s, side=0, name="ambiguous")
        a = copy.deepcopy(e["snapshot"]["assertions"][0]); a["assertion_value_or_target"] = s["models"][1]["record_id"]
        e["snapshot"]["assertions"].append(a)
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert "TARGETS_AMBIGUOUS" in codes(out)


def test_f24_cross_source_disagreement_survives_corroboration(tmp_path):
    def change(s): extra_source(s, side=0, target=1, evidence="independently_corroborated", name="conflicting")
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert "TARGETS_CONFLICT" in codes(out)


def test_f21_irrelevant_contradiction_not_global_veto(tmp_path):
    def change(s):
        e = extra_source(s, side=0, evidence="contradicted", name="different-name")
        e["snapshot"]["assertions"][0]["assertion_subject"] = "neither-requested-name"
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    assert out["R_identity"]["value"] == "non_equivalent"
    assert out["Q_identity"]["value"] == "conditions_satisfied"
    assert "ASSERTION_NAME_ABSENT" in codes(out)


def test_f29_supersession_is_not_newest_source_override(tmp_path):
    def change(s): s["sources"][0]["snapshot"]["assertions"][0]["superseded_by"] = "uninterpreted-source"
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    assert "SUPERSESSION_UNRESOLVED" in codes(out)


def test_f42_inventory_source_removal_is_detected(tmp_path):
    def change(f):
        f.inventory["model_sources"] = f.inventory["model_sources"][1:]
        f.context["selected_source_ids"] = f.context["selected_source_ids"][1:]
    assert "INVENTORY_OMISSION" in typed_refusal(build_fixture(tmp_path, contract_mutator=change))


def test_f42_inventory_file_removal_is_detected(tmp_path):
    def change(f): f.inventory["entries"] = f.inventory["entries"][1:]
    assert "INVENTORY_OMISSION" in typed_refusal(build_fixture(tmp_path, contract_mutator=change))


def test_f42_selected_sources_cannot_prune_pinned_inventory(tmp_path):
    def change(f): f.context["selected_source_ids"] = f.context["selected_source_ids"][1:]
    assert "INVENTORY_OMISSION" in typed_refusal(build_fixture(tmp_path, contract_mutator=change))


def test_a1_f42_source_target_manifest_cannot_drop_decoded_target(tmp_path):
    def change(f): f.inventory["model_sources"][0]["target_refs"] = []
    assert "CONTEXT_ANCHOR_MISMATCH" in typed_refusal(build_fixture(tmp_path, contract_mutator=change))


def test_a2_f42_orphan_snapshot_cannot_be_silently_dropped(tmp_path):
    def change(s): s["sources"][0]["capture_present"] = False
    assert "KNOWN_SOURCE_UNAVAILABLE" in typed_refusal(build_fixture(tmp_path, catalog_mutator=change))


def test_f42_query_cannot_replace_pinned_context(tmp_path):
    f = build_fixture(tmp_path)
    anchor = f.anchor()
    query = copy.deepcopy(f.query)
    query["evidence_context_ref"]["sha256"] = digest(b"another-context")
    out = evaluate_synthetic_r2(query, anchor=anchor)
    blocked(out)
    assert "CONTEXT_ANCHOR_MISMATCH" in codes(out)


@pytest.mark.parametrize("field,value", [("complete", True), ("freshness_window_days", 9999), ("established", True), ("test_mode", True)])
def test_f42_query_has_no_caller_authority_fields(tmp_path, field, value):
    f = build_fixture(tmp_path)
    query = copy.deepcopy(f.query); query[field] = value
    out = evaluate_synthetic_r2(query, anchor=f.anchor())
    blocked(out)
    assert "INVALID_SCHEMA" in codes(out)


def add_omission(f, *, other_endpoint=False, known_at=OBSERVED, missing=None):
    unavailable = {"source_key": "missing-source", "locator": "fixture://unavailable", "expected_record_id": None,
        "expected_sha256": None, "endpoint_id": f.state["endpoints"][1]["record_id"] if other_endpoint else None,
        "requested_name": "unrelated-name" if other_endpoint else None}
    if missing is not None:
        unavailable.update(endpoint_id=f.state["endpoints"][0]["record_id"],
            requested_name=f.state["invocations"][0]["requested_model_name"])
        if missing == "payload":
            unavailable["expected_sha256"] = f.state["sources"][0]["capture"]["content_digest"]
        elif missing == "mid":
            unavailable["expected_record_id"] = f.state["models"][0]["record_id"]
    body = {"unavailable_ref": unavailable, "known_at": known_at, "reason": "not retained"}
    path = "fixture/omission.json"; data = encode(body); declaration = ref(path, data)
    f.artifacts[path] = data; f.refs[path] = declaration
    f.inventory["omission_declarations"].append({"declaration_ref": declaration, **body})
    f.context["omission_declaration_refs"].append(declaration)
    f.context["provided_artifact_refs"].append(declaration)
    f.fixture["fixture_artifact_refs"].append(declaration)


@pytest.mark.parametrize("missing", ["payload", "mid"])
def test_a2_f34_explicit_missing_chain_declaration_is_representable(tmp_path, missing):
    def change(s):
        if missing == "mid": s["missing_model_ids"].add(s["models"][0]["record_id"])
        else: s["sources"][0]["payload_present"] = False
    f = build_fixture(tmp_path, catalog_mutator=change,
        contract_mutator=lambda f: add_omission(f, missing=missing))
    out = f.evaluate()
    assert out["validation_status"] == "valid"
    blocked(out)
    assert out["supplied_relation"]["value"] == "unresolved"
    assert "KNOWN_SOURCE_UNAVAILABLE" in codes(out)


def test_a2_f42_unknown_digest_omission_blocks_clean_but_not_supplied_relation(tmp_path):
    f = build_fixture(tmp_path, contract_mutator=add_omission)
    out = f.evaluate()
    blocked(out)
    assert out["supplied_relation"]["value"] == "non_equivalent"
    assert out["coverage"]["value"] in {"missing_items", "undetermined"}
    assert "KNOWN_SOURCE_UNAVAILABLE" in codes(out)
    missing = f.inventory["omission_declarations"][0]["unavailable_ref"]
    assert missing["expected_sha256"] is None and missing["expected_record_id"] is None


def test_a2_f42_proven_irrelevant_omission_control(tmp_path):
    out = build_fixture(tmp_path, contract_mutator=lambda f: add_omission(f, other_endpoint=True)).evaluate()
    assert out["Q_identity"]["value"] == "conditions_satisfied"


def test_a2_f42_declaration_after_cutoff_is_not_known_at_event(tmp_path):
    out = build_fixture(tmp_path, contract_mutator=lambda f: add_omission(f, known_at=LATE)).evaluate()
    assert out["Q_identity"]["value"] == "conditions_satisfied"


def test_a2_f42_declaration_body_must_match_retained_bytes(tmp_path):
    f = build_fixture(tmp_path, contract_mutator=add_omission)
    f.inventory["omission_declarations"][0]["reason"] = "a different claimed declaration"
    f.seal()
    assert "CONTEXT_ANCHOR_MISMATCH" in typed_refusal(f)


def test_f42_known_external_source_cannot_be_counted_as_exhausted(tmp_path):
    def change(f):
        path = "fixture/unsupported-source.json"; data = encode({"source": "known but applicability unsupported"})
        source_ref = ref(path, data); f.artifacts[path] = data; f.refs[path] = source_ref
        body = {"source_refs": [source_ref], "known_at": OBSERVED}
        path = "fixture/known-source-declaration.json"; data = encode(body)
        declaration = ref(path, data); f.artifacts[path] = data; f.refs[path] = declaration
        f.inventory["known_source_declarations"].append({"declaration_ref": declaration, **body})
        f.context["known_source_declaration_refs"].append(declaration)
        for reference in (source_ref, declaration):
            f.context["provided_artifact_refs"].append(reference)
            f.fixture["fixture_artifact_refs"].append(reference)
    out = build_fixture(tmp_path, contract_mutator=change).evaluate()
    blocked(out)
    assert out["validation_status"] == "valid"
    assert out["supplied_relation"]["value"] == "non_equivalent"
    assert "COVERAGE_UNDETERMINED" in codes(out)


def test_f10_f26_permutation_and_exact_duplicate_invariance(tmp_path):
    f = build_fixture(tmp_path)
    baseline = f.evaluate()
    for name in ["entries", "model_sources"]: f.inventory[name].reverse()
    f.inventory["model_sources"].append(copy.deepcopy(f.inventory["model_sources"][0]))
    for name in ["selected_source_ids", "provided_artifact_refs", "corroboration_witness_refs"]: f.context[name].reverse()
    f.fixture["model_witness_profile"]["availability_rows"].reverse()
    f.seal(); changed = f.evaluate()
    for key in ["R_identity", "Q_identity", "supplied_relation", "source_findings", "C3", "C10", "Q_C3_C10"]:
        assert changed[key] == baseline[key]


def test_a3_total_diagnostic_order_has_canonical_tie_break():
    base = {"code": "WITNESS_SCOPE_MISMATCH", "stage": 5, "side": "left", "subject_refs": []}
    a, b = {**base, "detail": "a"}, {**base, "detail": "b"}
    assert canonicalize_reasons([b, a, a]) == canonicalize_reasons([a, b]) == [a, b]


def test_f44_no_anchor_production_cannot_invent_context(tmp_path):
    f = build_fixture(tmp_path)
    query = copy.deepcopy(f.query); query.update(domain="production", entry_point="evaluate_production_r2")
    out = evaluate_production_r2(query)
    blocked(out)
    assert "CONTEXT_ANCHOR_MISMATCH" in codes(out)


def test_f44_synthetic_anchor_cannot_enter_production(tmp_path):
    f = build_fixture(tmp_path)
    query = copy.deepcopy(f.query); query.update(domain="production", entry_point="evaluate_production_r2")
    out = evaluate_production_r2(query, anchor=f.anchor())
    blocked(out)
    assert "DOMAIN_MISMATCH" in codes(out)


@pytest.mark.parametrize("entry", ["synthetic", "production"])
def test_f33_raw_surrogate_query_is_typed_refusal(tmp_path, entry):
    if entry == "synthetic":
        f = build_fixture(tmp_path)
        out = evaluate_synthetic_r2("\ud800", anchor=f.anchor())
    else:
        out = evaluate_production_r2("\ud800")
    blocked(out)
    assert out["validation_status"] == "invalid"
    assert "INVALID_SCHEMA" in codes(out)


@pytest.mark.parametrize("kinds", [("tool", "tool"), ("human", "human"), ("model", "tool"), ("tool", "human")])
def test_f48_unadmitted_kinds_and_cross_kind_remain_unresolved(tmp_path, kinds):
    def change(s): s["invocations"] = [invocation(i, kind=kind) for i, kind in enumerate(kinds)]
    out = build_fixture(tmp_path, catalog_mutator=change).evaluate()
    blocked(out)
    expected = "PROFILE_UNAVAILABLE" if kinds[0] == kinds[1] else "CROSS_KIND_UNDEFINED"
    assert expected in codes(out)
