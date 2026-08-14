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

The result is therefore the catalog's assertion, resolved through a governed
path, and not a proof. The catalog is provider self-report: per the admitted
Section 4.4 text, transport integrity does not establish the truth of an
asserted model mapping. A NON_EQUIVALENT result means the provider asserts these
are different model identities and the assertion resolved cleanly. It does not
mean the two executors cannot share weights, training data, or failure modes.
`basis` records which of those was established.

P5 governs the unresolved case: unknown facts block qualification and never
increase independence. Every path that cannot resolve returns UNRESOLVED with an
enumerated reason, never a default of NON_EQUIVALENT.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

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

    @property
    def blocks_adjudication(self) -> bool:
        """True when C3 forbids adjudication.

        Both EQUIVALENT and UNRESOLVED block. Under the corrected C3, an
        unresolved relation is not treated as distinct: the adjudicating
        invocation may not adjudicate while the relation remains unresolved.
        Only an affirmatively resolved NON_EQUIVALENT permits it.
        """

        return self.status != NON_EQUIVALENT


def _resolve_one(
    invocation: Mapping[str, Any],
    snapshots: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> tuple[str | None, str]:
    """Resolve one invocation's executor to a ModelIdentity record id.

    Returns (identity, reason). identity is None when unresolved, and reason
    always names why, so a caller never has to infer it from absence.
    """

    if not snapshots:
        return None, "no_catalog_snapshot_available"
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
            return out.get("resolved_identity"), "resolved"
        last = str(out.get("reason", "unresolved"))
    return None, last


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

    l_id, l_reason = _resolve_one(left, snapshots)
    r_id, r_reason = _resolve_one(right, snapshots)

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

    if l_id == r_id:
        return EquivalenceResult(
            status=EQUIVALENT,
            basis="model_identity_resolution_equality",
            left_identity=l_id,
            right_identity=r_id,
        )

    return EquivalenceResult(
        status=NON_EQUIVALENT,
        basis="model_identity_resolution_inequality_asserted_by_catalog",
        left_identity=l_id,
        right_identity=r_id,
    )
