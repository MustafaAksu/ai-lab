"""Tests for ABS-0004 v5 Slice B catalog identity resolution.

Catalog record and historical v1 codec coverage is retained. The admitted
Step 3A successor replaces old positive single-source resolver expectations
with nonpersistable refusal cases; model applicability now belongs to the
complete r2 evaluator tests, not this retired entry point.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_lab.documentation.verification_outcome import (
    STALE,
    UNVERIFIABLE,
    VERIFIED_CURRENT,
)
from ai_lab.providers.catalog import (
    CHANNEL_STATUSES,
    CONTENT_EVIDENCE_STATUSES,
    DEFAULT_FRESHNESS_WINDOW_DAYS,
    EVIDENCE_CONTRADICTED,
    EVIDENCE_INDEPENDENTLY_CORROBORATED,
    EVIDENCE_SELF_ASSERTED,
    EVIDENCE_UNASSESSED,
    SOURCE_OPERATOR_ENTERED,
    SOURCE_PROVIDER_SELF_REPORT,
    SOURCE_THIRD_PARTY,
    VOCABULARY_DISJOINT,
    CatalogRecordError,
    build_assertion,
    build_capture,
    build_endpoint_identity,
    build_model_identity,
    build_snapshot,
    canonical_catalog_json,
    catalog_id_for,
    catalog_relative_path,
    validate_catalog_record,
)
from ai_lab.providers.catalog_resolution import (
    NON_RESOLUTION_REASONS,
    LEGACY_CONTEXT_REQUIRED,
    REASON_AMBIGUOUS_ASSERTIONS,
    REASON_CONTRADICTED_EVIDENCE,
    REASON_EXPIRED_FRESHNESS_WINDOW,
    REASON_NO_APPLICABLE_ASSERTION,
    REASON_SNAPSHOT_AFTER_INVOCATION,
    SLICE_B_PREDICATES,
    ResolutionError,
    build_resolution_record,
    canonical_resolution_json,
    resolution_relations,
    resolution_relative_path,
    resolve_identity,
    validate_resolution_record,
    write_resolution_record,
)

INVOCATION = {
    "invocation_id": "INV-1111111111111111",
    "requested_model_name": "model-alpha",
    "service_endpoint": "provider.endpoint",
    "occurred_at": "2026-07-20T12:00:00+00:00",
}


def make_identity():
    return build_model_identity(
        originator_id="provider-org", canonical_name="model-alpha", release_identity="r1"
    )


def make_endpoint():
    return build_endpoint_identity(
        operating_organization="provider-org", endpoint_identifier="provider.endpoint"
    )


def make_assertion(target, subject="model-alpha", valid_from="2026-07-01T00:00:00+00:00", valid_until=None):
    return build_assertion(
        assertion_subject=subject,
        assertion_predicate="resolves_to",
        assertion_value_or_target=target,
        valid_from=valid_from,
        valid_until=valid_until,
        source="provider models endpoint",
    )


def make_snapshot(assertions, observed_at="2026-07-19T00:00:00+00:00"):
    return build_snapshot(
        service_endpoint_id=make_endpoint()["record_id"],
        observed_at=observed_at,
        assertions=assertions,
        source_set="GET /models",
    )


def make_capture(snapshot, content=EVIDENCE_SELF_ASSERTED, channel=VERIFIED_CURRENT, source=SOURCE_PROVIDER_SELF_REPORT):
    return build_capture(
        snapshot_id=snapshot["record_id"],
        capture_method="https_get",
        source_type=source,
        captured_at=snapshot["observed_at"],
        capture_success=True,
        capturing_executor="tool:catalog_fetch",
        payload='{"data": []}',
        channel_authentication_status=channel,
        content_evidence_status=content,
    )


def historical_outcome(*, invocation, snapshot, capture, reason=None):
    """Explicit v1 serialization fixture, not execution of a current resolver.

    Tests supply the intended historical outcome. This helper performs no
    applicability/binding assessment and conveys no current qualification.
    """
    if reason is not None:
        return {"resolved": False, "reason": reason}
    return {
        "resolved": True,
        "resolved_identity": snapshot["assertions"][0]["assertion_value_or_target"],
        "snapshot_id": snapshot["record_id"],
        "capture_id": capture["record_id"],
        "content_evidence_status": capture["content_evidence_status"],
        "channel_authentication_status": capture["channel_authentication_status"],
    }


# --- record family ------------------------------------------------------


def test_identity_and_endpoint_records_validate():
    identity = make_identity()
    endpoint = make_endpoint()

    validate_catalog_record(identity)
    validate_catalog_record(endpoint)
    assert identity["record_id"].startswith("MID-")
    assert endpoint["record_id"].startswith("EID-")


def test_snapshot_and_capture_records_validate():
    snapshot = make_snapshot([make_assertion(make_identity()["record_id"])])
    capture = make_capture(snapshot)

    validate_catalog_record(snapshot)
    validate_catalog_record(capture)
    assert capture["snapshot_id"] == snapshot["record_id"]


def test_paths_are_deterministic_and_kind_scoped():
    snapshot = make_snapshot([make_assertion("MID-2222222222222222")])

    assert catalog_relative_path(snapshot["record_id"]) == (
        f"docs/catalog/snap/{snapshot['record_id']}.json"
    )


def test_malformed_catalog_id_has_no_path():
    with pytest.raises(CatalogRecordError, match="malformed catalog id"):
        catalog_relative_path("SNAP-nope")


# --- condition 5: determinism ------------------------------------------


def test_identity_generation_is_deterministic():
    assert make_identity()["record_id"] == make_identity()["record_id"]
    assert make_endpoint()["record_id"] == make_endpoint()["record_id"]

    first = make_snapshot([make_assertion("MID-3333333333333333")])
    second = make_snapshot([make_assertion("MID-3333333333333333")])
    assert first["record_id"] == second["record_id"]


def test_distinct_content_produces_distinct_identities():
    a = build_model_identity(originator_id="org", canonical_name="alpha", release_identity="r1")
    b = build_model_identity(originator_id="org", canonical_name="alpha", release_identity="r2")

    assert a["record_id"] != b["record_id"]


def test_canonical_serialization_is_byte_stable():
    snapshot = make_snapshot([make_assertion("MID-4444444444444444")])
    capture = make_capture(snapshot)

    assert canonical_catalog_json(capture) == canonical_catalog_json(dict(capture))
    reordered = dict(reversed(list(capture.items())))
    assert canonical_catalog_json(capture) == canonical_catalog_json(reordered)


def test_repeated_legacy_refusal_is_identical_and_not_a_v1_annotation():
    snapshot = make_snapshot([make_assertion("MID-5555555555555555")])
    capture = make_capture(snapshot)
    first = resolve_identity(invocation=INVOCATION, snapshot=snapshot, capture=capture)
    second = resolve_identity(invocation=INVOCATION, snapshot=snapshot, capture=capture)
    assert first == second
    assert first["resolved"] is False
    assert first["reason"] == LEGACY_CONTEXT_REQUIRED
    for moment in ("2026-07-23T00:00:00+00:00", "2026-07-24T00:00:00+00:00"):
        with pytest.raises(ResolutionError, match="r2 assessment/refusal"):
            build_resolution_record(invocation=INVOCATION, outcome=first, resolved_at=moment)


# --- condition 2: serialization adjacency ------------------------------


def test_content_evidence_status_serializes_immediately_before_channel():
    snapshot = make_snapshot([make_assertion("MID-6666666666666666")])
    capture = make_capture(snapshot)

    lines = canonical_catalog_json(capture).splitlines()
    content_line = next(i for i, l in enumerate(lines) if "content_evidence_status" in l)
    channel_line = next(i for i, l in enumerate(lines) if "channel_authentication_status" in l)

    assert channel_line == content_line + 1


def test_resolution_annotation_also_orders_status_fields():
    snapshot = make_snapshot([make_assertion("MID-7777777777777777")])
    capture = make_capture(snapshot)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture)
    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )

    lines = canonical_resolution_json(record).splitlines()
    content_line = next(i for i, l in enumerate(lines) if "content_evidence_status" in l)
    channel_line = next(i for i, l in enumerate(lines) if "channel_authentication_status" in l)
    assert channel_line == content_line + 1


# --- condition 3: status-field independence ----------------------------


def test_status_vocabularies_are_disjoint():
    assert VOCABULARY_DISJOINT
    assert not (CHANNEL_STATUSES & CONTENT_EVIDENCE_STATUSES)


def test_channel_status_may_not_take_a_content_evidence_value():
    snapshot = make_snapshot([make_assertion("MID-8888888888888888")])

    with pytest.raises(CatalogRecordError, match="channel_authentication_status"):
        make_capture(snapshot, channel=EVIDENCE_SELF_ASSERTED)


def test_content_status_may_not_take_a_verification_outcome_value():
    snapshot = make_snapshot([make_assertion("MID-9999999999999999")])

    for outcome in (VERIFIED_CURRENT, STALE, UNVERIFIABLE):
        with pytest.raises(CatalogRecordError, match="content_evidence_status"):
            make_capture(snapshot, content=outcome)


def test_neither_status_field_has_a_default():
    import inspect

    signature = inspect.signature(build_capture)
    for field in ("channel_authentication_status", "content_evidence_status"):
        assert signature.parameters[field].default is inspect.Parameter.empty


def test_the_two_status_fields_vary_independently():
    snapshot = make_snapshot([make_assertion("MID-1010101010101010")])

    weak_channel = make_capture(snapshot, channel=UNVERIFIABLE, content=EVIDENCE_SELF_ASSERTED)
    strong_channel = make_capture(snapshot, channel=VERIFIED_CURRENT, content=EVIDENCE_SELF_ASSERTED)

    assert weak_channel["content_evidence_status"] == strong_channel["content_evidence_status"]
    assert weak_channel["channel_authentication_status"] != strong_channel["channel_authentication_status"]


# --- the v5 adopted constraint -----------------------------------------


def test_self_report_may_not_claim_independent_corroboration():
    snapshot = make_snapshot([make_assertion("MID-1212121212121212")])

    with pytest.raises(CatalogRecordError, match="may not imply independent confirmation"):
        make_capture(snapshot, content=EVIDENCE_INDEPENDENTLY_CORROBORATED)


def test_self_report_accepts_self_asserted():
    snapshot = make_snapshot([make_assertion("MID-1313131313131313")])
    capture = make_capture(snapshot, content=EVIDENCE_SELF_ASSERTED)

    assert capture["content_evidence_status"] == EVIDENCE_SELF_ASSERTED


def test_strong_channel_does_not_license_strong_content():
    snapshot = make_snapshot([make_assertion("MID-1414141414141414")])

    with pytest.raises(CatalogRecordError):
        make_capture(snapshot, channel=VERIFIED_CURRENT, content=EVIDENCE_INDEPENDENTLY_CORROBORATED)


def test_third_party_source_may_claim_corroboration():
    snapshot = make_snapshot([make_assertion("MID-1515151515151515")])
    capture = make_capture(
        snapshot, content=EVIDENCE_INDEPENDENTLY_CORROBORATED, source=SOURCE_THIRD_PARTY
    )

    assert capture["content_evidence_status"] == EVIDENCE_INDEPENDENTLY_CORROBORATED


# --- atomicity and rejection classes -----------------------------------


def test_assertion_with_a_compound_value_is_rejected():
    with pytest.raises(CatalogRecordError, match="exactly one atomic claim"):
        build_assertion(
            assertion_subject="model-alpha",
            assertion_predicate="resolves_to",
            assertion_value_or_target=["MID-1", "MID-2"],
            valid_from="2026-07-01T00:00:00+00:00",
            source="s",
        )


def test_assertion_with_an_extra_claim_field_is_rejected():
    assertion = make_assertion("MID-1616161616161616")
    assertion["second_claim"] = "context_limit=400000"

    snapshot_input = dict(
        service_endpoint_id=make_endpoint()["record_id"],
        observed_at="2026-07-19T00:00:00+00:00",
        assertions=[assertion],
        source_set="s",
    )
    with pytest.raises(CatalogRecordError, match="unknown fields"):
        build_snapshot(**snapshot_input)


def test_unknown_assertion_predicate_is_rejected():
    with pytest.raises(CatalogRecordError, match="assertion_predicate"):
        build_assertion(
            assertion_subject="model-alpha",
            assertion_predicate="probably_is",
            assertion_value_or_target="MID-1",
            valid_from="2026-07-01T00:00:00+00:00",
            source="s",
        )


def test_naive_timestamp_is_rejected():
    with pytest.raises(CatalogRecordError, match="explicit UTC offset"):
        build_assertion(
            assertion_subject="model-alpha",
            assertion_predicate="resolves_to",
            assertion_value_or_target="MID-1",
            valid_from="2026-07-01T00:00:00",
            source="s",
        )


def test_empty_snapshot_is_rejected():
    with pytest.raises(CatalogRecordError, match="non-empty list"):
        build_snapshot(
            service_endpoint_id="EID-1", observed_at="2026-07-19T00:00:00+00:00",
            assertions=[], source_set="s",
        )


def test_unknown_source_type_is_rejected():
    snapshot = make_snapshot([make_assertion("MID-1717171717171717")])

    with pytest.raises(CatalogRecordError, match="source_type"):
        make_capture(snapshot, source="rumour")


def test_tampered_record_id_is_rejected():
    snapshot = make_snapshot([make_assertion("MID-1818181818181818")])
    snapshot["record_id"] = "SNAP-0000000000000000"

    with pytest.raises(CatalogRecordError, match="does not match"):
        validate_catalog_record(snapshot)


def test_malformed_content_digest_is_rejected():
    snapshot = make_snapshot([make_assertion("MID-1919191919191919")])
    capture = make_capture(snapshot)
    capture["content_digest"] = "notadigest"
    capture["record_id"] = catalog_id_for(capture)

    with pytest.raises(CatalogRecordError, match="content_digest"):
        validate_catalog_record(capture)


# --- admitted legacy refusal; applicability belongs to r2 ----------------


@pytest.mark.parametrize("case", [
    "matching", "absent_name", "future", "ambiguous", "stale", "contradicted",
    "failed_capture", "wrong_endpoint", "dangling_target", "scalar_target",
    "invalid_interval", "missing_link",
])
def test_legacy_sources_cannot_supply_the_missing_governed_context(case):
    target = make_identity()["record_id"]
    assertions = [make_assertion(target)]
    observed = "2026-07-19T00:00:00+00:00"
    if case == "absent_name": assertions = [make_assertion(target, subject="other-model")]
    if case == "future": observed = "2026-07-21T00:00:00+00:00"
    if case == "stale": observed = "2026-05-01T00:00:00+00:00"
    if case == "ambiguous": assertions.append(make_assertion("MID-2323232323232323"))
    if case == "dangling_target": assertions = [make_assertion("MID-9999999999999999")]
    if case == "scalar_target": assertions = [make_assertion(7)]
    if case == "invalid_interval": assertions = [make_assertion(target, valid_from="2026-07-10T00:00:00+00:00", valid_until="2026-07-01T00:00:00+00:00")]
    snapshot = make_snapshot(assertions, observed_at=observed)
    if case == "wrong_endpoint": snapshot["service_endpoint_id"] = "EID-0000000000000000"
    capture = make_capture(snapshot, content=EVIDENCE_CONTRADICTED if case == "contradicted" else EVIDENCE_SELF_ASSERTED)
    if case == "failed_capture": capture["capture_success"] = False
    if case == "missing_link": capture["snapshot_id"] = "SNAP-0000000000000000"
    outcome = resolve_identity(invocation=INVOCATION, snapshot=snapshot, capture=capture)
    assert outcome["record_kind"] == "legacy_resolution_refusal"
    assert outcome["resolved"] is False
    assert outcome["resolved_identity"] is None
    assert outcome["reason"] == LEGACY_CONTEXT_REQUIRED
    assert outcome["assessment_ref"] is None


def test_historical_v1_reason_vocabulary_stays_frozen():
    assert set(NON_RESOLUTION_REASONS) == {
        REASON_NO_APPLICABLE_ASSERTION, REASON_SNAPSHOT_AFTER_INVOCATION,
        REASON_AMBIGUOUS_ASSERTIONS, REASON_EXPIRED_FRESHNESS_WINDOW,
        REASON_CONTRADICTED_EVIDENCE,
    }
    assert LEGACY_CONTEXT_REQUIRED not in NON_RESOLUTION_REASONS


@pytest.mark.parametrize("window", [-1, 0, 30, 180, True])
def test_legacy_freshness_argument_cannot_create_or_widen_context(window):
    snapshot = make_snapshot([make_assertion(make_identity()["record_id"])])
    outcome = resolve_identity(invocation=INVOCATION, snapshot=snapshot,
                               capture=make_capture(snapshot), freshness_window_days=window)
    assert DEFAULT_FRESHNESS_WINDOW_DAYS == 30
    assert outcome["resolved"] is False
    assert outcome["reason"] == LEGACY_CONTEXT_REQUIRED


# --- annotations: append-only and evidence inheritance -----------------


def test_resolution_annotation_validates_and_is_addressable():
    snapshot = make_snapshot([make_assertion("MID-3232323232323232")])
    capture = make_capture(snapshot)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture)

    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )

    validate_resolution_record(record)
    assert resolution_relative_path(record["record_id"]).startswith("docs/catalog/resolutions/")


def test_condition_6_annotation_inherits_the_capture_evidence_class():
    snapshot = make_snapshot([make_assertion("MID-3333333333333334")])
    capture = make_capture(snapshot, content=EVIDENCE_SELF_ASSERTED, channel=UNVERIFIABLE)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture)

    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )

    assert record["content_evidence_status"] == capture["content_evidence_status"]
    assert record["channel_authentication_status"] == capture["channel_authentication_status"]


def test_unassessed_evidence_class_is_inherited_too():
    snapshot = make_snapshot([make_assertion("MID-3434343434343434")])
    capture = make_capture(snapshot, content=EVIDENCE_UNASSESSED, source=SOURCE_OPERATOR_ENTERED)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture)
    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )

    assert record["content_evidence_status"] == EVIDENCE_UNASSESSED


def test_unresolved_annotation_may_not_carry_an_identity():
    snapshot = make_snapshot([make_assertion("MID-3535353535353535", subject="other")])
    capture = make_capture(snapshot)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture, reason=REASON_NO_APPLICABLE_ASSERTION)
    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )

    assert record["resolved"] is False
    assert record["resolved_identity"] is None
    assert record["non_resolution_reason"] == REASON_NO_APPLICABLE_ASSERTION

    record["resolved_identity"] = "MID-sneaky"
    with pytest.raises(ResolutionError, match="must be null on an unresolved"):
        validate_resolution_record(record)


def test_unresolved_annotation_requires_an_enumerated_reason():
    snapshot = make_snapshot([make_assertion("MID-3636363636363636", subject="other")])
    capture = make_capture(snapshot)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture, reason=REASON_NO_APPLICABLE_ASSERTION)
    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )
    record["non_resolution_reason"] = "just because"

    with pytest.raises(ResolutionError, match="never a silent default"):
        validate_resolution_record(record)


def test_writing_an_annotation_does_not_touch_the_invocation(tmp_path):
    invocation_dir = tmp_path / "docs" / "invocations"
    invocation_dir.mkdir(parents=True)
    invocation_path = invocation_dir / f"{INVOCATION['invocation_id']}.json"
    invocation_path.write_text(json.dumps(INVOCATION, indent=2) + "\n", encoding="utf-8")
    before = invocation_path.read_bytes()

    snapshot = make_snapshot([make_assertion("MID-3737373737373737")])
    capture = make_capture(snapshot)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture)
    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )
    written = write_resolution_record(record, tmp_path)

    assert written.exists()
    assert invocation_path.read_bytes() == before


# --- condition 7: relation shape and registered predicates -------------


def test_relations_use_graph_relation_shape_and_slice_b_predicates_only():
    from ai_lab.documentation.graph_neighborhood import GraphRelation

    snapshot = make_snapshot([make_assertion("MID-3838383838383838")])
    capture = make_capture(snapshot)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture)
    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )

    relations = resolution_relations(record)

    assert relations
    assert all(isinstance(relation, GraphRelation) for relation in relations)
    assert all(relation.predicate in SLICE_B_PREDICATES for relation in relations)
    assert all(relation.authoritative is False for relation in relations)


def test_unresolved_annotation_emits_no_resolution_relation():
    snapshot = make_snapshot([make_assertion("MID-3939393939393939", subject="other")])
    capture = make_capture(snapshot)
    outcome = historical_outcome(invocation=INVOCATION, snapshot=snapshot, capture=capture, reason=REASON_NO_APPLICABLE_ASSERTION)
    record = build_resolution_record(
        invocation=INVOCATION, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00"
    )

    assert resolution_relations(record) == ()


def test_slice_b_predicate_list_matches_the_registered_four():
    assert SLICE_B_PREDICATES == ("resolved_to", "asserted_by", "concerns", "captured")


def test_predicate_registry_documents_the_slice_b_predicates():
    registry = Path("docs/self_model/PREDICATE_REGISTRY.md").read_text(encoding="utf-8")

    for predicate in SLICE_B_PREDICATES:
        assert f"### {predicate}" in registry


# --- condition 8: Slice A invariance -----------------------------------


def test_stored_slice_a_records_are_untouched_by_slice_b_code():
    from ai_lab.providers.invocation_record import (
        canonical_invocation_json,
        validate_invocation_record,
    )

    stored = sorted(Path("docs/invocations").glob("INV-*.json"))
    assert stored, "expected captured invocation records in the repository"

    for path in stored:
        raw = path.read_bytes()
        record = json.loads(raw)
        validate_invocation_record(record)

        snapshot = make_snapshot(
            [
                make_assertion(
                    "MID-4040404040404040",
                    subject=record["requested_model_name"],
                    valid_from="2026-01-01T00:00:00+00:00",
                )
            ],
            observed_at="2026-07-01T00:00:00+00:00",
        )
        capture = make_capture(snapshot)
        resolve_identity(
            invocation=record, snapshot=snapshot, capture=capture, freshness_window_days=365
        )

        assert path.read_bytes() == raw
        assert canonical_invocation_json(record) == raw.decode("utf-8")


def test_real_captured_invocation_needs_an_explicit_r2_context(tmp_path):
    stored = sorted(Path("docs/invocations").glob("INV-*.json"))
    record = json.loads(stored[0].read_text(encoding="utf-8"))
    before = stored[0].read_bytes()
    identity = build_model_identity(originator_id="unknown", canonical_name=record["requested_model_name"])
    snapshot = make_snapshot([make_assertion(identity["record_id"], subject=record["requested_model_name"], valid_from="2026-01-01T00:00:00+00:00")])
    outcome = resolve_identity(invocation=record, snapshot=snapshot, capture=make_capture(snapshot), freshness_window_days=365)
    assert outcome["resolved"] is False
    assert outcome["reason"] == LEGACY_CONTEXT_REQUIRED
    with pytest.raises(ResolutionError, match="r2 assessment/refusal"):
        build_resolution_record(invocation=record, outcome=outcome, resolved_at="2026-07-23T00:00:00+00:00")
    assert not (tmp_path / "docs/catalog/resolutions").exists()
    assert stored[0].read_bytes() == before


# --- purity ------------------------------------------------------------


def test_resolution_consults_no_clock():
    snapshot = make_snapshot([make_assertion("MID-4141414141414141")])
    capture = make_capture(snapshot)

    outcomes = [
        resolve_identity(invocation=INVOCATION, snapshot=snapshot, capture=capture)
        for _ in range(50)
    ]

    assert all(outcome == outcomes[0] for outcome in outcomes)


def test_resolution_does_not_mutate_its_inputs():
    snapshot = make_snapshot([make_assertion("MID-4242424242424242")])
    capture = make_capture(snapshot)
    invocation_before = json.dumps(INVOCATION, sort_keys=True)
    snapshot_before = json.dumps(snapshot, sort_keys=True)
    capture_before = json.dumps(capture, sort_keys=True)

    resolve_identity(invocation=INVOCATION, snapshot=snapshot, capture=capture)

    assert json.dumps(INVOCATION, sort_keys=True) == invocation_before
    assert json.dumps(snapshot, sort_keys=True) == snapshot_before
    assert json.dumps(capture, sort_keys=True) == capture_before


def test_mismatched_legacy_capture_cannot_construct_a_context():
    snapshot = make_snapshot([make_assertion(make_identity()["record_id"])])
    other = make_snapshot([make_assertion("MID-4444444444444445")], observed_at="2026-07-18T00:00:00+00:00")
    outcome = resolve_identity(invocation=INVOCATION, snapshot=snapshot, capture=make_capture(other))
    assert outcome["reason"] == LEGACY_CONTEXT_REQUIRED
    assert outcome["resolved"] is False


# --- documentation -----------------------------------------------------


def test_catalog_documentation_states_the_mitigation_honestly():
    doc = Path("docs/self_model/CATALOG_RECORDS.md").read_text(encoding="utf-8")

    assert "mitigation" in doc
    assert "not a control" in doc
    assert "self_asserted" in doc
    assert "thirty days" in doc or "30 days" in doc


# --- capture path: opt-in live, fixture replay by default --------------


def test_live_capture_is_disabled_by_default(monkeypatch):
    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV, live_capture_enabled

    monkeypatch.delenv(LIVE_CAPTURE_ENV, raising=False)
    assert live_capture_enabled() is False


def test_live_capture_refuses_while_disabled(monkeypatch):
    from ai_lab.providers.catalog_capture import (
        LIVE_CAPTURE_ENV,
        CatalogCaptureError,
        capture_live,
    )

    monkeypatch.delenv(LIVE_CAPTURE_ENV, raising=False)

    def fetcher():  # pragma: no cover - must never run
        raise AssertionError("network access attempted while disabled")

    with pytest.raises(CatalogCaptureError, match="disabled"):
        capture_live(
            fetcher=fetcher,
            operating_organization="org",
            endpoint_identifier="org.endpoint",
        )


def test_live_capture_runs_only_when_explicitly_enabled(monkeypatch):
    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV, capture_live

    monkeypatch.setenv(LIVE_CAPTURE_ENV, "1")
    payload = {"data": [{"id": "model-alpha", "owned_by": "org", "context_window": 1000}]}

    endpoint, snapshot, capture, identities = capture_live(
        fetcher=lambda: payload,
        operating_organization="org",
        endpoint_identifier="provider.endpoint",
    )

    validate_catalog_record(endpoint)
    validate_catalog_record(snapshot)
    validate_catalog_record(capture)
    assert capture["capture_method"] == "live_fetch"
    assert identities[0]["canonical_name"] == "model-alpha"


def test_captured_catalogs_are_always_self_asserted(monkeypatch):
    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV, capture_live

    monkeypatch.setenv(LIVE_CAPTURE_ENV, "1")
    payload = {"data": [{"id": "model-alpha", "owned_by": "org"}]}

    _, _, capture, _ = capture_live(
        fetcher=lambda: payload,
        operating_organization="org",
        endpoint_identifier="provider.endpoint",
    )

    assert capture["source_type"] == SOURCE_PROVIDER_SELF_REPORT
    assert capture["content_evidence_status"] == EVIDENCE_SELF_ASSERTED
    # Nothing has authenticated the channel in this slice, so claiming
    # anything stronger would be the overclaim P6 forbids.
    assert capture["channel_authentication_status"] == UNVERIFIABLE


def test_fixture_replay_needs_no_network_and_no_opt_in(monkeypatch):
    from ai_lab.providers.catalog_capture import LIVE_CAPTURE_ENV, capture_from_fixture

    monkeypatch.delenv(LIVE_CAPTURE_ENV, raising=False)

    endpoint, snapshot, capture, identities = capture_from_fixture(
        "anthropic-models-20260722"
    )

    validate_catalog_record(endpoint)
    validate_catalog_record(snapshot)
    validate_catalog_record(capture)
    assert capture["capture_method"].startswith("fixture_replay:")
    assert any(i["canonical_name"] == "claude-sonnet-4-5" for i in identities)


def test_fixture_observed_at_is_the_recording_date_not_now():
    from ai_lab.providers.catalog_capture import capture_from_fixture, load_fixture

    fixture = load_fixture("openai-models-20260722")
    _, snapshot, capture, _ = capture_from_fixture("openai-models-20260722")

    assert snapshot["observed_at"] == fixture["recorded_at"]
    assert capture["captured_at"] == fixture["recorded_at"]


def test_fixtures_declare_themselves_synthetic_not_observed():
    """A fixture may be invented; it may not claim to be an observation."""

    from ai_lab.providers.catalog_capture import FIXTURE_DIR

    fixtures = sorted(Path(FIXTURE_DIR).glob("*.json"))
    assert fixtures, "expected catalog fixtures"

    for path in fixtures:
        fixture = json.loads(path.read_text(encoding="utf-8"))
        assert fixture["recorded_at"]
        provenance = fixture["provenance"]
        assert "SYNTHETIC" in provenance
        assert "not an observation" in provenance
        # The word that made the earlier version false.
        assert "as observed by the operator" not in provenance


def test_fixture_without_provenance_is_rejected(tmp_path, monkeypatch):
    from ai_lab.providers import catalog_capture

    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "nameless.json").write_text(
        json.dumps(
            {
                "recorded_at": "2026-07-22T00:00:00+00:00",
                "operating_organization": "org",
                "endpoint_identifier": "org.endpoint",
                "payload": {"data": [{"id": "model-alpha"}]},
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(catalog_capture, "FIXTURE_DIR", str(fixture_dir.relative_to(tmp_path)))

    with pytest.raises(catalog_capture.CatalogCaptureError, match="provenance"):
        catalog_capture.load_fixture("nameless", tmp_path)


def test_fixture_replay_and_live_capture_share_one_parsing_path():
    import inspect

    from ai_lab.providers.catalog_capture import (
        capture_from_fixture,
        capture_live,
        snapshot_from_payload,
    )

    for function in (capture_from_fixture, capture_live):
        assert "snapshot_from_payload" in inspect.getsource(function)


def test_stale_fixture_does_not_construct_a_context():
    from ai_lab.providers.catalog_capture import capture_from_fixture

    _, snapshot, capture, identities = capture_from_fixture("anthropic-models-20260722")
    invocation = {
        "invocation_id": "INV-5151515151515151",
        "requested_model_name": "claude-sonnet-4-5",
        "service_endpoint": "anthropic.messages",
        "occurred_at": "2027-01-01T00:00:00+00:00",
    }

    outcome = resolve_identity(invocation=invocation, snapshot=snapshot, capture=capture)

    assert outcome["resolved"] is False
    assert outcome["reason"] == LEGACY_CONTEXT_REQUIRED
    assert outcome["assessment_ref"] is None


def test_fixture_in_window_does_not_construct_a_context():
    from ai_lab.providers.catalog_capture import capture_from_fixture

    _, snapshot, capture, identities = capture_from_fixture("anthropic-models-20260722")
    invocation = {
        "invocation_id": "INV-5252525252525252",
        "requested_model_name": "claude-sonnet-4-5",
        "service_endpoint": "anthropic.messages",
        "occurred_at": "2026-07-25T00:00:00+00:00",
    }

    outcome = resolve_identity(invocation=invocation, snapshot=snapshot, capture=capture)

    assert outcome["resolved"] is False
    assert outcome["reason"] == LEGACY_CONTEXT_REQUIRED
    assert outcome["assessment_ref"] is None


def test_catalog_records_write_to_deterministic_paths(tmp_path):
    from ai_lab.providers.catalog_capture import capture_from_fixture, write_catalog_records

    endpoint, snapshot, capture, identities = capture_from_fixture(
        "openai-models-20260722"
    )

    written = write_catalog_records([endpoint, snapshot, capture, *identities], tmp_path)

    assert len(written) == 3 + len(identities)
    for path in written:
        assert path.exists()
        validate_catalog_record(json.loads(path.read_text(encoding="utf-8")))


def test_payload_without_entries_is_rejected(monkeypatch):
    from ai_lab.providers.catalog_capture import (
        LIVE_CAPTURE_ENV,
        CatalogCaptureError,
        capture_live,
    )

    monkeypatch.setenv(LIVE_CAPTURE_ENV, "1")

    with pytest.raises(CatalogCaptureError, match="no model entries"):
        capture_live(
            fetcher=lambda: {"data": []},
            operating_organization="org",
            endpoint_identifier="provider.endpoint",
        )
