"""Executor equivalence resolution, written as falsifying cases first.

Per DECISION-20260812-0002. The cases that matter are the ones where a naive
implementation would be wrong: differing identifiers that must NOT yield
non_equivalent, differing names that resolve to one identity and must yield
equivalent, and a non_equivalent relation that must NOT permit adjudication
unless both sides rest on independently corroborated evidence
(DECISION-20260814-0001).
"""

from __future__ import annotations

import copy
import glob
import json
import pathlib

import pytest

from ai_lab.providers.executor_equivalence import (
    EQUIVALENT,
    NON_EQUIVALENT,
    UNRESOLVED,
    EquivalenceResult,
    equivalence,
)

REPO = pathlib.Path(__file__).resolve().parents[1]
CORROBORATED = "independently_corroborated"


def _catalog():
    caps, snaps = {}, []
    for f in glob.glob(str(REPO / "docs/catalog/**/*.json"), recursive=True):
        d = json.loads(pathlib.Path(f).read_text())
        if d.get("record_kind") == "catalog_capture":
            caps[d["snapshot_id"]] = d
    for f in glob.glob(str(REPO / "docs/catalog/snap/SNAP-*.json")):
        s = json.loads(pathlib.Path(f).read_text())
        if s["record_id"] in caps:
            snaps.append((s, caps[s["record_id"]]))
    return snaps


def _invocations():
    by = {}
    for f in glob.glob(str(REPO / "docs/invocations/INV-*.json")):
        r = json.loads(pathlib.Path(f).read_text())
        by.setdefault(r["executor"]["reference"], r)
    return by


def _mut(rec, *, kind=None, ref=None):
    c = copy.deepcopy(rec)
    if kind:
        c["executor"]["kind"] = kind
    if ref:
        c["executor"]["reference"] = ref
        c["requested_model_name"] = ref
    return c


def test_the_two_reviewer_slots_are_distinct_but_do_not_permit():
    """The live question, under DECISION-20260814-0001.

    The relation is non_equivalent: the catalog asserts distinct identities and
    the resolution is clean. The permission is withheld: both captures carry
    content_evidence_status self_asserted, and C3 permits adjudication only
    where non-equivalence is affirmatively established.
    """

    by, snaps = _invocations(), _catalog()
    r = equivalence(left=by["claude-sonnet-5"], right=by["gpt-5.6-terra"], snapshots=snaps)
    assert r.status == NON_EQUIVALENT
    assert r.basis == "model_identity_resolution_inequality_asserted_by_catalog"
    assert r.left_identity != r.right_identity
    assert r.left_evidence_class == "self_asserted"
    assert r.right_evidence_class == "self_asserted"
    assert r.blocks_adjudication is True
    assert "self_asserted" in r.permits_reason


def test_same_executor_is_equivalent_and_blocks():
    by, snaps = _invocations(), _catalog()
    r = equivalence(left=by["claude-sonnet-5"], right=by["claude-sonnet-5"], snapshots=snaps)
    assert r.status == EQUIVALENT
    assert r.blocks_adjudication is True


def test_two_names_resolving_to_one_identity_are_equivalent():
    """The case that justifies resolution over string comparison.

    A string comparison would call these separate. No such alias pair exists in
    the captured catalog, so the snapshot is synthesised; the behaviour is
    established, the situation is not observed.
    """

    by = _invocations()
    caps, snap = {}, None
    for f in glob.glob(str(REPO / "docs/catalog/**/*.json"), recursive=True):
        d = json.loads(pathlib.Path(f).read_text())
        if d.get("record_kind") == "catalog_capture":
            caps[d["snapshot_id"]] = d
    for f in glob.glob(str(REPO / "docs/catalog/snap/SNAP-*.json")):
        s = json.loads(pathlib.Path(f).read_text())
        if s["record_id"] in caps and any(
            a.get("assertion_subject") == "gpt-5.6-terra" for a in s.get("assertions", [])
        ):
            snap = s
            break
    assert snap is not None
    mid = next(a["assertion_value_or_target"] for a in snap["assertions"]
               if a.get("assertion_subject") == "gpt-5.6-terra"
               and a.get("assertion_predicate") == "resolves_to")
    alias = copy.deepcopy(snap)
    proto = copy.deepcopy(next(a for a in alias["assertions"]
                               if a.get("assertion_subject") == "gpt-5.6-terra"))
    proto["assertion_subject"] = "gpt-5.6-terra-alias"
    proto["assertion_value_or_target"] = mid
    alias["assertions"].append(proto)

    r = equivalence(
        left=_mut(by["gpt-5.6-terra"], ref="gpt-5.6-terra"),
        right=_mut(by["gpt-5.6-terra"], ref="gpt-5.6-terra-alias"),
        snapshots=[(alias, caps[snap["record_id"]])],
    )
    assert r.status == EQUIVALENT
    assert r.left_identity == r.right_identity == mid
    assert r.blocks_adjudication is True


@pytest.mark.parametrize("left_ev,right_ev,expect_block", [
    (CORROBORATED, CORROBORATED, False),
    (CORROBORATED, "self_asserted", True),
    ("self_asserted", CORROBORATED, True),
    ("self_asserted", "self_asserted", True),
])
def test_permission_requires_both_sides_corroborated(left_ev, right_ev, expect_block):
    """The four combinations DECISION-20260814-0001 distinguishes.

    Both asymmetric cases must block. An earlier implementation ranked the four
    CONTENT_EVIDENCE_STATUSES on an invented ordinal scale and took the weaker of
    the two; nothing governs that ordering, and this matrix falsifies any rule
    that would permit on a single corroborated side.

    A provider-sourced capture may not carry independently_corroborated: the
    catalog validator refuses it, which
    test_catalog_rejects_corroborated_provider_self_report establishes.
    Corroboration requires a third_party_record source that this repository does
    not have, so these captures are synthesised. The behaviour is established;
    the situation is not observed.
    """

    by, snaps = _invocations(), _catalog()
    left_rec, right_rec = by["claude-sonnet-5"], by["gpt-5.6-terra"]

    def dress(snapshot, capture):
        """Give each capture the evidence class of the executor it resolves.

        Keyed on which executor the snapshot actually covers, so the asymmetric
        cases are genuinely asymmetric rather than depending on list order.
        """

        subjects = {a.get("assertion_subject") for a in snapshot.get("assertions", [])}
        if left_rec["executor"]["reference"] in subjects:
            ev = left_ev
        elif right_rec["executor"]["reference"] in subjects:
            ev = right_ev
        else:
            return (snapshot, capture)
        c = dict(capture)
        c["content_evidence_status"] = ev
        if ev == CORROBORATED:
            c["source_type"] = "third_party_record"
        return (snapshot, c)

    r = equivalence(left=left_rec, right=right_rec,
                    snapshots=[dress(s, c) for s, c in snaps])
    assert r.status == NON_EQUIVALENT
    assert r.left_evidence_class == left_ev
    assert r.right_evidence_class == right_ev
    assert r.blocks_adjudication is expect_block


@pytest.mark.parametrize("kind,left,right", [
    ("tool", "tool-a", "tool-b"),
    ("human", "operator", "someone-else"),
])
def test_unimplemented_kinds_never_return_non_equivalent(kind, left, right):
    """ABS-0004 defines these tests; this module does not implement them.

    Differing references must not produce non_equivalent: v9.1 states that
    distinct identifiers do not by themselves establish distinct executor
    identities.
    """

    by, snaps = _invocations(), _catalog()
    r = equivalence(
        left=_mut(by["claude-sonnet-5"], kind=kind, ref=left),
        right=_mut(by["gpt-5.6-terra"], kind=kind, ref=right),
        snapshots=snaps,
    )
    assert r.status == UNRESOLVED
    assert kind in r.basis


def test_cross_kind_is_unresolved_not_non_equivalent():
    by, snaps = _invocations(), _catalog()
    r = equivalence(left=by["claude-sonnet-5"],
                    right=_mut(by["gpt-5.6-terra"], kind="human"), snapshots=snaps)
    assert r.status == UNRESOLVED
    assert r.basis == "no_cross_kind_equivalence_test_defined"


def test_unknown_name_is_unresolved_not_non_equivalent():
    """An executor absent from every snapshot. P5: unknown facts block."""

    by, snaps = _invocations(), _catalog()
    r = equivalence(left=by["claude-sonnet-4-5"], right=by["gpt-5.6-terra"], snapshots=snaps)
    assert r.status == UNRESOLVED
    assert r.unresolved_side == "left"
    assert r.blocks_adjudication is True


def test_no_catalog_is_unresolved():
    by = _invocations()
    r = equivalence(left=by["claude-sonnet-5"], right=by["gpt-5.6-terra"], snapshots=[])
    assert r.status == UNRESOLVED
    assert r.reason == "no_catalog_snapshot_available"


def test_malformed_input_does_not_raise():
    by, snaps = _invocations(), _catalog()
    r = equivalence(left=by["claude-sonnet-5"],
                    right={"occurred_at": "2026-01-01T00:00:00+00:00"}, snapshots=snaps)
    assert r.status == UNRESOLVED


def test_permission_threshold_independent_of_the_resolver():
    """blocks_adjudication in isolation, over every combination that blocks."""

    for left, right in [("self_asserted", "self_asserted"),
                        ("unassessed", "unassessed"),
                        (None, None),
                        (CORROBORATED, "self_asserted"),
                        ("self_asserted", CORROBORATED),
                        (CORROBORATED, None)]:
        assert EquivalenceResult(NON_EQUIVALENT, "x", left_evidence_class=left,
                                 right_evidence_class=right).blocks_adjudication is True
    assert EquivalenceResult(NON_EQUIVALENT, "x", left_evidence_class=CORROBORATED,
                             right_evidence_class=CORROBORATED).blocks_adjudication is False
    for status in (EQUIVALENT, UNRESOLVED):
        assert EquivalenceResult(status, "x", left_evidence_class=CORROBORATED,
                                 right_evidence_class=CORROBORATED).blocks_adjudication is True


def _a_real_capture():
    for f in glob.glob(str(REPO / "docs/catalog/**/*.json"), recursive=True):
        d = json.loads(pathlib.Path(f).read_text())
        if d.get("record_kind") == "catalog_capture":
            return d
    raise AssertionError("no catalog capture found")


def test_catalog_rejects_corroborated_provider_self_report():
    """The rule the permission threshold rests on, as retained evidence.

    DECISION-20260814-0001 requires independently_corroborated content evidence
    before a non_equivalent relation permits adjudication, and states that no
    provider-sourced capture may carry it. That claim was previously established
    only in a development episode. This test retains it.
    """

    from ai_lab.providers.catalog import CatalogRecordError, validate_catalog_record

    c = dict(_a_real_capture())
    assert c["source_type"] == "provider_self_report"
    c["content_evidence_status"] = CORROBORATED
    with pytest.raises(CatalogRecordError, match="may not imply independent confirmation"):
        validate_catalog_record(c)


def test_catalog_accepts_corroborated_third_party_record():
    """The only source that can clear the threshold.

    The synthetic captures used in the permission matrix are of this shape, so
    this establishes that those captures are ones the catalog would accept rather
    than shapes the validator would reject.
    """

    from ai_lab.providers.catalog import validate_catalog_record

    c = dict(_a_real_capture())
    c["source_type"] = "third_party_record"
    c["content_evidence_status"] = CORROBORATED
    validate_catalog_record(c)


def test_multiple_captures_for_one_executor_are_order_dependent():
    """A KNOWN BOUNDARY, pinned so it cannot change silently.

    _resolve_one returns the first snapshot that resolves. With two captures
    covering one executor and differing in evidence class, the same evidence in
    a different list order produces the opposite governance outcome. This test
    asserts that the defect is present and reachable, not that the behaviour is
    correct.

    It is harmless today: every retained capture is a provider self-report and
    the catalog validator forbids independently_corroborated on one, so no live
    pair can differ. It becomes unsafe when the first corroborating source
    arrives, which is precisely what the permitting path requires.

    DECISION-20260814-0001 records that order-independent multi-capture
    semantics must be defined and falsified before any third_party_record is
    relied upon to clear C3. When they are, this test should be replaced by one
    asserting order independence.
    """

    by, snaps = _invocations(), _catalog()
    left_ref = by["claude-sonnet-5"]["executor"]["reference"]
    covering = next((s, c) for s, c in snaps
                    if any(a.get("assertion_subject") == left_ref
                           for a in s.get("assertions", [])))
    other = next((s, c) for s, c in snaps if (s, c) != covering)

    weak = (covering[0], {**covering[1], "content_evidence_status": "self_asserted"})
    strong = (covering[0], {**covering[1], "source_type": "third_party_record",
                            "content_evidence_status": CORROBORATED})
    right_strong = (other[0], {**other[1], "source_type": "third_party_record",
                               "content_evidence_status": CORROBORATED})

    weak_first = equivalence(left=by["claude-sonnet-5"], right=by["gpt-5.6-terra"],
                             snapshots=[weak, strong, right_strong])
    strong_first = equivalence(left=by["claude-sonnet-5"], right=by["gpt-5.6-terra"],
                               snapshots=[strong, weak, right_strong])

    assert weak_first.left_evidence_class == "self_asserted"
    assert strong_first.left_evidence_class == CORROBORATED
    assert weak_first.blocks_adjudication is True
    assert strong_first.blocks_adjudication is False
    assert weak_first.blocks_adjudication != strong_first.blocks_adjudication, (
        "the boundary has been closed; replace this test with one asserting "
        "order independence and update DECISION-20260814-0001"
    )
