"""Step 3A compatibility successor to DECISION-20260814-0001.

The unsafe first-success/label-only permission assertions are replaced under
DECISION-20261126-0001. Historical probe artifacts retain their old observations.
Full model relation/witness behavior belongs to the governed r2 evaluator tests.
"""

from __future__ import annotations

import glob
import itertools
import json
import pathlib

import pytest

from ai_lab.providers.catalog_resolution import LEGACY_CONTEXT_REQUIRED
from ai_lab.providers.executor_equivalence import (
    EQUIVALENT, NON_EQUIVALENT, UNRESOLVED, EquivalenceResult,
    _resolve_one, equivalence,
)

REPO = pathlib.Path(__file__).resolve().parents[1]
CORROBORATED = "independently_corroborated"


def _catalog():
    captures = [json.loads(p.read_text()) for p in (REPO / "docs/catalog/cap").glob("*.json")]
    by_snapshot = {c["snapshot_id"]: c for c in captures}
    return [(s, by_snapshot[s["record_id"]])
            for p in sorted((REPO / "docs/catalog/snap").glob("*.json"))
            if (s := json.loads(p.read_text()))["record_id"] in by_snapshot]


def _invocations():
    result = {}
    for p in sorted((REPO / "docs/invocations").glob("INV-*.json")):
        record = json.loads(p.read_text())
        result.setdefault(record["executor"]["reference"], record)
    return result


def test_retained_live_catalog_does_not_supply_an_implicit_context():
    records = _invocations()
    result = equivalence(left=records["claude-sonnet-5"], right=records["gpt-5.6-terra"], snapshots=_catalog())
    assert result.status == UNRESOLVED
    assert result.reason == LEGACY_CONTEXT_REQUIRED
    assert result.left_identity is None and result.right_identity is None
    assert result.assessment_ref is None
    assert result.blocks_adjudication is True


@pytest.mark.parametrize("left,right", [
    ({"executor": {"kind": "model", "reference": "same"}}, {"executor": {"kind": "model", "reference": "same"}}),
    ({"executor": {"kind": "model", "reference": "alias-a"}}, {"executor": {"kind": "model", "reference": "alias-b"}}),
    ({"executor": {"kind": "tool", "reference": "tool-a"}}, {"executor": {"kind": "tool", "reference": "tool-b"}}),
    ({"executor": {"kind": "human", "reference": "person-a"}}, {"executor": {"kind": "human", "reference": "person-b"}}),
    ({"executor": {"kind": "tool"}}, {"executor": {"kind": "model"}}),
    ({}, {}), (None, {}),
])
def test_names_kinds_and_malformed_inputs_do_not_create_context(left, right):
    result = equivalence(left=left, right=right, snapshots=[])
    assert result.status == UNRESOLVED
    assert result.reason == LEGACY_CONTEXT_REQUIRED
    assert result.blocks_adjudication is True


@pytest.mark.parametrize("status", [EQUIVALENT, NON_EQUIVALENT, UNRESOLVED])
@pytest.mark.parametrize("left_evidence,right_evidence", list(itertools.product(
    ["self_asserted", "independently_corroborated", "unassessed", "contradicted"], repeat=2)))
def test_legacy_boolean_always_blocks_even_direct_construction(status, left_evidence, right_evidence):
    result = EquivalenceResult(status, "caller claimed basis",
                               left_evidence_class=left_evidence,
                               right_evidence_class=right_evidence,
                               permits_reason="caller claimed authorization")
    assert result.blocks_adjudication is True


def test_no_context_never_iterates_a_caller_selected_source_universe():
    class UntrustedSources:
        def __iter__(self):
            raise AssertionError("retired source loop was executed")

    assert _resolve_one({}, UntrustedSources()) == (None, LEGACY_CONTEXT_REQUIRED, None)
    result = equivalence(left={}, right={}, snapshots=UntrustedSources())
    assert result.status == UNRESOLVED and result.blocks_adjudication is True


def test_known_first_success_counterexample_is_now_order_invariant():
    records, pairs = _invocations(), _catalog()
    snapshot, capture = pairs[0]
    weak = (snapshot, {**capture, "content_evidence_status": "self_asserted"})
    strong = (snapshot, {**capture, "source_type": "third_party_record", "content_evidence_status": CORROBORATED})
    conflict = (snapshot, {**capture, "source_type": "third_party_record", "content_evidence_status": "contradicted"})
    results = [equivalence(left=records["claude-sonnet-5"], right=records["gpt-5.6-terra"], snapshots=order)
               for order in itertools.permutations((weak, strong, conflict))]
    assert all(result == results[0] for result in results)
    assert results[0].status == UNRESOLVED
    assert results[0].blocks_adjudication is True


def _a_real_capture():
    for f in glob.glob(str(REPO / "docs/catalog/**/*.json"), recursive=True):
        d = json.loads(pathlib.Path(f).read_text())
        if d.get("record_kind") == "catalog_capture":
            return d
    raise AssertionError("no catalog capture found")


def test_catalog_rejects_corroborated_provider_self_report():
    """Preserve the catalog evidence-class rule independently of the adapter."""

    from ai_lab.providers.catalog import CatalogRecordError, validate_catalog_record

    c = dict(_a_real_capture())
    assert c["source_type"] == "provider_self_report"
    c["content_evidence_status"] = CORROBORATED
    with pytest.raises(CatalogRecordError, match="may not imply independent confirmation"):
        validate_catalog_record(c)


def test_catalog_accepts_corroborated_third_party_record():
    """A valid corroboration label remains shape-valid, never a Boolean permit."""

    from ai_lab.providers.catalog import validate_catalog_record

    c = dict(_a_real_capture())
    c["source_type"] = "third_party_record"
    c["content_evidence_status"] = CORROBORATED
    validate_catalog_record(c)
