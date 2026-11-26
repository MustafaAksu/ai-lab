"""Legacy equivalence projection protected by DECISION-20261126-0001.

R2 separates the catalog relation, identity-evidence condition and constraint
findings. This historical result type cannot encode their complete evidence.
Its Boolean is therefore always blocking, including direct construction. Only
an explicit query and externally pinned context can produce a diagnostic
relation projection; no old first-success or evidence-label fallback remains.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from ai_lab.providers.catalog_resolution import (
    LEGACY_CONTEXT_REQUIRED, LEGACY_POSITIVE_DISABLED,
    _assessment_ref, _legacy_assessment,
)

EQUIVALENT = "equivalent"
NON_EQUIVALENT = "non_equivalent"
UNRESOLVED = "unresolved"
KIND_MODEL = "model"
KIND_TOOL = "tool"
KIND_HUMAN = "human"


@dataclass(frozen=True)
class EquivalenceResult:
    """Diagnostic compatibility object; never a qualification or authority grant."""

    status: str
    basis: str
    left_identity: str | None = None
    right_identity: str | None = None
    reason: str | None = None
    unresolved_side: str | None = None
    left_evidence_class: str | None = None
    right_evidence_class: str | None = None
    permits_reason: str | None = None
    assessment_ref: Mapping[str, str] | None = None
    diagnostic_codes: tuple[str, ...] = ()

    @property
    def blocks_adjudication(self) -> bool:
        """Unconditional 3A refusal; does not itself evaluate C3 or C10."""
        return True


def _resolve_one(
    invocation: Mapping[str, Any],
    snapshots: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> tuple[None, str, None]:
    """Retired helper retained as a refusal shim, never first-success resolution."""
    return None, LEGACY_CONTEXT_REQUIRED, None


def equivalence(
    *,
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    snapshots: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
    query: Mapping[str, Any] | None = None,
    anchor: Any = None,
) -> EquivalenceResult:
    """Project a checked r2 relation diagnostically; always block adjudication.

    The supplied snapshots are not a selectable source universe. No explicit
    query/context means no resolution. Full-context paths delegate to the same
    complete pipeline after matching both exact retained invocation records.
    """
    if query is None or anchor is None:
        return EquivalenceResult(
            UNRESOLVED, "legacy_context_required", reason=LEGACY_CONTEXT_REQUIRED,
            unresolved_side="both", permits_reason="legacy permission is disabled",
        )
    result, diagnostics = _legacy_assessment(
        query=query, anchor=anchor,
        bindings=((left, ("left",)), (right, ("right",))),
    )
    status = UNRESOLVED
    if result is not None and result.get("validation_status") == "valid":
        relation = result.get("R_identity", {}).get("value")
        if relation in {EQUIVALENT, NON_EQUIVALENT, UNRESOLVED}:
            status = relation
    return EquivalenceResult(
        status, "governed_r2_relation_diagnostic" if result is not None else "legacy_context_refusal",
        reason=LEGACY_POSITIVE_DISABLED,
        permits_reason="legacy permission is disabled; structured r2 findings are separate",
        assessment_ref=_assessment_ref(result), diagnostic_codes=diagnostics,
    )
