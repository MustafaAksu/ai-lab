"""R16: the exact witnessed chain must exist by assessment time.

The fixtures contain real retained bytes and Git objects, but their identity
and witness premises are fictional. No C3/C10 or live qualification follows.
"""
from __future__ import annotations

import copy
import json

import pytest

from ai_lab.providers.qualification_records import validate_shape
from qualification_fixtures import (
    ASSESSED, EVENT, OBSERVED, SOURCE_AVAILABLE, WITNESS_AVAILABLE,
    build_fixture, digest, extra_source, refresh_source_ids,
)


AFTER_ASSESSMENT = "2026-11-20T02:00:00+00:00"
AFTER_CAPTURE = "2026-11-20T02:00:01+00:00"


def _change_witness(bundle, *, assessed=ASSESSED, available=WITNESS_AVAILABLE,
                    source_index=0):
    source = bundle.source_refs[source_index]
    chain = [source["capture_ref"], source["snapshot_ref"], source["payload_ref"],
             source["target_refs"][0]]
    premise = json.loads(bundle.artifacts["fixture/verification-0.json"])
    premise["evidence_refs"] = chain
    bundle.rewrite_aux("fixture/verification-0.json", premise)
    witness = json.loads(bundle.artifacts["fixture/witness-0.json"])
    witness["assessed_at"] = assessed
    witness["evidence_refs"] = chain
    bundle.rewrite_aux("fixture/witness-0.json", witness)
    proof = json.loads(bundle.artifacts["fixture/witness-availability-0.json"])
    proof["available_at"] = available
    bundle.rewrite_aux("fixture/witness-availability-0.json", proof)


def _timed_fixture(tmp_path, *, captured=OBSERVED, available=SOURCE_AVAILABLE,
                   assessed=ASSESSED, witness_available=WITNESS_AVAILABLE,
                   alternative=False, witnessed_source=0):
    def catalog_change(state):
        source = state["sources"][0]
        source["capture"]["captured_at"] = captured
        source["available_at"] = available
        refresh_source_ids(source)
        if alternative:
            extra_source(state, side=0, evidence="independently_corroborated",
                         name="early-same-mid-alternative")

    def context_change(bundle):
        _change_witness(bundle, assessed=assessed, available=witness_available,
                        source_index=witnessed_source)

    return build_fixture(tmp_path, catalog_mutator=catalog_change,
                         contract_mutator=context_change)


def _assert_catalog_only(result):
    validate_shape(result, "AssessmentResult")
    assert result["validation_status"] == "valid"
    assert result["R_identity"]["value"] == "non_equivalent"
    assert result["supplied_relation"]["value"] == "non_equivalent"
    assert result["Q_identity"]["value"] == "withheld"
    for field in ("C3", "C10", "Q_C3_C10"):
        assert result[field]["value"] == "unresolved"
    assert "WIT-0" not in {ref["record_id"] for ref in result["corroboration_witness_refs"]}


@pytest.mark.parametrize("captured", [AFTER_ASSESSMENT, OBSERVED],
                         ids=["capture-after-witness", "availability-after-witness"])
def test_r16_witness_cannot_precede_its_exact_source_availability(tmp_path, captured):
    bundle = _timed_fixture(tmp_path, captured=captured, available=AFTER_CAPTURE)
    _assert_catalog_only(bundle.evaluate())


@pytest.mark.parametrize("assessed", [ASSESSED, "2026-11-20T04:00:00+03:00"],
                         ids=["exact-instant", "same-instant-other-offset"])
def test_r16_source_available_at_assessment_is_inclusive(tmp_path, assessed):
    result = _timed_fixture(tmp_path, captured=ASSESSED, available=ASSESSED,
                            assessed=assessed).evaluate()
    assert result["validation_status"] == "valid"
    assert result["Q_identity"]["value"] == "conditions_satisfied"
    for field in ("C3", "C10", "Q_C3_C10"):
        assert result[field]["value"] == "unresolved"


def test_r16_early_same_mid_alternative_cannot_rescue_late_witnessed_chain(tmp_path):
    bundle = _timed_fixture(tmp_path, available=AFTER_CAPTURE, alternative=True)
    _assert_catalog_only(bundle.evaluate())


def test_r16_witness_can_use_its_actual_early_alternative_chain(tmp_path):
    result = _timed_fixture(tmp_path, available=AFTER_CAPTURE, alternative=True,
                            witnessed_source=2).evaluate()
    assert result["validation_status"] == "valid"
    assert result["Q_identity"]["value"] == "conditions_satisfied"
    assert len(result["corroboration_witness_refs"]) == 2


def test_r16_another_chain_availability_cannot_supply_assessment_time(tmp_path):
    bundle = _timed_fixture(tmp_path, available=AFTER_CAPTURE, alternative=True)
    # Both sources have the same MID. Retain the late exact proof and also
    # supply the early other-chain proof; only the exact one can cover the chain.
    bundle.source_refs[0]["availability_evidence_refs"].extend(
        copy.deepcopy(bundle.source_refs[2]["availability_evidence_refs"]))
    bundle.seal()
    _assert_catalog_only(bundle.evaluate())


def test_r16_timely_chain_and_availability_are_retained_as_evidence(tmp_path):
    bundle = _timed_fixture(tmp_path, available=AFTER_CAPTURE, alternative=True,
                            witnessed_source=2)
    result = bundle.evaluate()
    assert result["Q_identity"]["value"] == "conditions_satisfied"
    timing = [r for r in result["Q_identity"]["reasons"]
              if r["side"] == "left" and r["detail"].startswith("accepted fictional witness chain timing: ")]
    assert len(timing) == 1
    identifiers = {r["record_id"] for r in timing[0]["subject_refs"]}
    assert {bundle.source_refs[2]["source_id"], "AV-source-2", "AV-witness-0", "WIT-0"} <= identifiers
    assert bundle.source_refs[0]["source_id"] not in identifiers
    details = json.loads(timing[0]["detail"].split(": ", 1)[1])
    assert details["source_available_at"] == SOURCE_AVAILABLE
    assert details["assessed_at"] == ASSESSED
    assert details["witness_available_at"] == WITNESS_AVAILABLE
    assert details["payload_sha256"] == bundle.source_refs[2]["payload_ref"]["sha256"]
    assert details["verification_sha256"] == bundle.refs["fixture/verification-0.json"]["sha256"]


def test_r16_nullable_proof_artifact_ids_still_retain_exact_availability_records(tmp_path):
    bundle = _timed_fixture(tmp_path)
    paths = ("fixture/source-availability-0.json", "fixture/witness-availability-0.json")
    for path in paths:
        # ID omission is legal on ArtifactRef; it does not erase the checked
        # AvailabilityEvidence record's required availability_id in its bytes.
        bundle.refs[path]["record_id"] = None
        for references in (bundle.context["provided_artifact_refs"],
                           bundle.fixture["fixture_artifact_refs"],
                           bundle.source_refs[0]["availability_evidence_refs"]):
            for reference in references:
                if reference["path"] == path:
                    reference["record_id"] = None
    bundle.seal()
    result = bundle.evaluate()
    assert result["Q_identity"]["value"] == "conditions_satisfied"
    timing = [r for r in result["Q_identity"]["reasons"]
              if r["side"] == "left" and r["detail"].startswith("accepted fictional witness chain timing: ")]
    assert len(timing) == 1
    for path in paths:
        data = bundle.artifacts[path]
        expected = {"record_id": json.loads(data)["availability_id"], "sha256": digest(data)}
        assert expected in timing[0]["subject_refs"]


def test_r16_permuted_chain_and_timing_evidence_has_same_findings(tmp_path):
    bundle = _timed_fixture(tmp_path, available=AFTER_CAPTURE, alternative=True,
                            witnessed_source=2)
    baseline = bundle.evaluate()
    for field in ("entries", "model_sources"):
        bundle.inventory[field].reverse()
    for field in ("selected_source_ids", "provided_artifact_refs", "corroboration_witness_refs"):
        bundle.context[field].reverse()
    bundle.fixture["model_witness_profile"]["availability_rows"].reverse()
    bundle.fixture["model_witness_profile"]["witness_rows"].reverse()
    bundle.seal()
    changed = bundle.evaluate()
    for key in ("R_identity", "Q_identity", "supplied_relation", "source_findings",
                "C3", "C10", "Q_C3_C10", "corroboration_witness_refs"):
        assert changed[key] == baseline[key]


def test_r16_retrospective_bound_does_not_repair_early_assessment(tmp_path):
    bundle = _timed_fixture(tmp_path, captured=AFTER_ASSESSMENT, available=AFTER_CAPTURE)
    bundle.context["context_policy"].update(mode="retrospective", knowledge_cutoff=EVENT)
    bundle.seal()
    _assert_catalog_only(bundle.evaluate())
