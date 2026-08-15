"""Executor equivalence resolution for ABS-0004 C3, C7 and C10.

WHY THIS EXISTS

C3 forbids an invocation from adjudicating a claim whose evidence ancestry
contains an equivalent executor identity, and refuses when the relation is
unresolved. C7 needs the same relation to distinguish separation from
coincidence of names. C10 needs it for verifier lineage. Three of the six
manual-mode constraints share this dependency, which is why it is built before
any of them.

WHAT IT ESTABLISHES, AND WHAT IT DOES NOT

ABS-0004 v9.1 states: "Distinct identifiers, endpoints, or invocation records do
not by themselves establish distinct executor identities. When executor-kind
specific equivalence cannot be resolved, independence remains unresolved."

So a string comparison of executor references cannot produce NON_EQUIVALENT, and
this module never does that. It resolves each executor reference to a
ModelIdentity record through catalog_resolution.resolve_identity, and compares
the resolved identities. That is the equivalence test C3 names for models:
"ModelIdentity resolution equality".

A NON_EQUIVALENT result means the supplied catalog evidence resolves the two
references to distinct ModelIdentity records. It does not mean the two executors
cannot share weights, training data, or failure modes. `left_evidence_class` and
`right_evidence_class` state the evidentiary class supporting each side's
resolution, so a reader can tell what class of evidence produced the relation.

Every capture retained today is a provider self-report, and per the admitted
Section 4.4 text transport integrity does not establish the truth of an asserted
model mapping. The catalog validator enforces this: a provider_self_report
capture may not carry independently_corroborated. That is why no live pair
permits adjudication.

P5 governs the unresolved case: unknown facts block qualification and never
increase independence. Every path that cannot resolve returns UNRESOLVED with an
enumerated reason, never a default of NON_EQUIVALENT.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from ai_lab.providers.catalog import EVIDENCE_INDEPENDENTLY_CORROBORATED
from ai_lab.providers.catalog_resolution import ResolutionError, resolve_identity

EQUIVALENT = "equivalent"
NON_EQUIVALENT = "non_equivalent"
UNRESOLVED = "unresolved"

# executor kinds ABS-0004 names, with the equivalence test each requires
KIND_MODEL = "model"
KIND_TOOL = "tool"
KIND_HUMAN = "human"


@dataclass(frozen=True)
class EquivalenceResult:
    """The relation between two executors, with the basis on which it was reached.

    `status` is never inferred from identifiers differing. `basis` names what was
    actually established, so a reader can tell a resolved catalog assertion from
    a string comparison.
    """

    status: str
    basis: str
    left_identity: str | None = None
    right_identity: str | None = None
    reason: str | None = None
    unresolved_side: str | None = None

    left_evidence_class: str | None = None
    right_evidence_class: str | None = None
    permits_reason: str | None = None

    @property
    def blocks_adjudication(self) -> bool:
        """True when C3 forbids adjudication.

        EQUIVALENT and UNRESOLVED block, as the corrected C3 requires: an
        unresolved relation is not treated as distinct.

        NON_EQUIVALENT blocks TOO unless the resolution rested on content
        evidence stronger than provider self-report. C3 permits adjudication
        only where non-equivalence is affirmatively established, and admitted
        v9.1 states that provider catalog self-report does not independently
        establish an asserted model mapping. Both current captures carry
        content_evidence_status self_asserted, and the catalog module records
        that a provider-sourced capture may never carry anything stronger,
        however well its channel authenticated.

        So the relation and the permission are separated (DECISION-20260814-0001):
        the resolution honestly reports non-equivalence as the catalog asserts
        it, and the permission waits for evidence the catalog cannot supply
        about itself. Today every real pair blocks.
        """

        if self.status != NON_EQUIVALENT:
            return True
        return not (self.left_evidence_class == EVIDENCE_INDEPENDENTLY_CORROBORATED
                    and self.right_evidence_class == EVIDENCE_INDEPENDENTLY_CORROBORATED)


# KNOWN BOUNDARY: _resolve_one returns the FIRST snapshot that resolves, so with
# two captures covering one executor the result depends on iteration order. This
# is demonstrated by test_multiple_captures_for_one_executor_are_order_dependent.
#
# It is harmless today: no third_party_record capture exists, every retained
# capture is self_asserted, and no live pair can therefore differ. It becomes
# unsafe the moment a corroborating source arrives, which is exactly the state
# the permitting path requires. Same evidence, different list order, opposite
# governance outcome.
#
# NOT FIXED HERE. Choosing an aggregation rule now would repeat the mistake this
# module already made once with the ordinal ranking: inventing semantics the
# ontology does not govern. DECISION-20260814-0001 records the requirement that
# order-independent multi-capture semantics be defined and falsified before any
# third_party_record is relied upon to clear C3.


def _resolve_one(
    invocation: Mapping[str, Any],
    snapshots: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> tuple[str | None, str, str | None]:
    """Resolve one invocation's executor to a ModelIdentity record id.

    Returns (identity, reason, evidence_class). evidence_class is the
    content_evidence_status of the capture the resolution rested on, so a
    caller can tell what class of evidence produced the identity rather than
    only that one was produced.
    """

    if not snapshots:
        return None, "no_catalog_snapshot_available", None
    last = "no_snapshot_covered_the_invocation"
    for snapshot, capture in snapshots:
        try:
            out = resolve_identity(
                invocation=invocation, snapshot=snapshot, capture=capture
            )
        except ResolutionError as exc:
            last = f"resolution_error: {exc}"
            continue
        if out.get("resolved"):
            return (out.get("resolved_identity"), "resolved",
                    capture.get("content_evidence_status"))
        last = str(out.get("reason", "unresolved"))
    return None, last, None


def equivalence(
    *,
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    snapshots: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> EquivalenceResult:
    """Resolve the equivalence relation between two invocations' executors.

    Pure. Never raises for a non-resolution; every failure to resolve returns
    UNRESOLVED with a reason.
    """

    lk = left.get("executor", {}).get("kind")
    rk = right.get("executor", {}).get("kind")

    if lk != rk:
        # Different executor kinds have different equivalence tests, and ABS-0004
        # defines no cross-kind test. Differing kinds is NOT evidence of
        # non-equivalence; it is a case the ontology does not cover.
        return EquivalenceResult(
            status=UNRESOLVED,
            basis="no_cross_kind_equivalence_test_defined",
            reason=f"left kind {lk!r}, right kind {rk!r}",
        )

    if lk != KIND_MODEL:
        # tool identity-and-version equality and principal equality are defined
        # by ABS-0004 but not implemented here. Returning UNRESOLVED is the
        # honest result; returning NON_EQUIVALENT on differing references would
        # be exactly the inference the ontology forbids.
        return EquivalenceResult(
            status=UNRESOLVED,
            basis=f"equivalence_test_for_kind_{lk}_not_implemented",
            reason="only model equivalence by ModelIdentity resolution is implemented",
        )

    l_id, l_reason, l_ev = _resolve_one(left, snapshots)
    r_id, r_reason, r_ev = _resolve_one(right, snapshots)

    if l_id is None or r_id is None:
        side = ("both" if l_id is None and r_id is None
                else "left" if l_id is None else "right")
        return EquivalenceResult(
            status=UNRESOLVED,
            basis="model_identity_resolution_incomplete",
            left_identity=l_id,
            right_identity=r_id,
            reason=l_reason if l_id is None else r_reason,
            unresolved_side=side,
        )

    # Both sides must be independently corroborated. The two evidence classes are
    # kept separate rather than collapsed into a pair-level value.
    #
    # An earlier version ranked the four CONTENT_EVIDENCE_STATUSES on an invented
    # ordinal scale and took the weaker. DECISION-20260814-0001 establishes one
    # threshold, that independently_corroborated licenses the permission; it does
    # not establish that the classes form a total order, and nothing governs the
    # claim that unassessed is stronger than self_asserted. Requiring both sides
    # to be corroborated gives the adjudicated behaviour without that assumption,
    # and is directly falsifiable: corroborated/self_asserted must block in either
    # arrangement.
    if l_id == r_id:
        return EquivalenceResult(
            status=EQUIVALENT,
            basis="model_identity_resolution_equality",
            left_identity=l_id,
            right_identity=r_id,
            left_evidence_class=l_ev,
            right_evidence_class=r_ev,
        )

    permits = (l_ev == EVIDENCE_INDEPENDENTLY_CORROBORATED
               and r_ev == EVIDENCE_INDEPENDENTLY_CORROBORATED)
    return EquivalenceResult(
        status=NON_EQUIVALENT,
        basis="model_identity_resolution_inequality_asserted_by_catalog",
        left_identity=l_id,
        right_identity=r_id,
        left_evidence_class=l_ev,
        right_evidence_class=r_ev,
        permits_reason=(
            "both sides independently corroborated"
            if permits else
            f"content evidence is {l_ev!r} and {r_ev!r}; C3 requires "
            "non-equivalence to be affirmatively established, and provider "
            "self-report does not establish an asserted model mapping"
        ),
    )
