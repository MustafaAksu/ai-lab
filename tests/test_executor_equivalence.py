"""Executor equivalence resolution, written as falsifying cases first.

Per DECISION-20260812-0002. The cases that matter are the ones where a naive
implementation would be wrong: differing identifiers that must NOT yield
non_equivalent, and differing names that resolve to one identity and must yield
equivalent.
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
    equivalence,
)

REPO = pathlib.Path(__file__).resolve().parents[1]


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


def test_the_two_reviewer_slots_resolve_to_distinct_identities():
    """The live question: may gpt-5.6-terra review what claude-sonnet-5 drafted?"""

    by, snaps = _invocations(), _catalog()
    r = equivalence(left=by["claude-sonnet-5"], right=by["gpt-5.6-terra"], snapshots=snaps)
    assert r.status == NON_EQUIVALENT
    assert r.basis == "model_identity_resolution_inequality_asserted_by_catalog"
    assert r.left_identity != r.right_identity
    assert r.blocks_adjudication is False


def test_same_executor_is_equivalent_and_blocks():
    by, snaps = _invocations(), _catalog()
    r = equivalence(left=by["claude-sonnet-5"], right=by["claude-sonnet-5"], snapshots=snaps)
    assert r.status == EQUIVALENT
    assert r.blocks_adjudication is True


def test_two_names_resolving_to_one_identity_are_equivalent():
    """The case that justifies resolution over string comparison.

    A string comparison would call these separate and permit adjudication. No
    such alias pair exists in the captured catalog, so the snapshot is
    synthesised; the behaviour is established, the situation is not observed.
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


def test_only_non_equivalent_permits_adjudication():
    """C3 as corrected: equivalent blocks, and unresolved also blocks."""

    from ai_lab.providers.executor_equivalence import EquivalenceResult
    assert EquivalenceResult(NON_EQUIVALENT, "x").blocks_adjudication is False
    assert EquivalenceResult(EQUIVALENT, "x").blocks_adjudication is True
    assert EquivalenceResult(UNRESOLVED, "x").blocks_adjudication is True
