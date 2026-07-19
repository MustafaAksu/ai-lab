"""Shared three-valued verification outcome vocabulary.

This module defines the outcome enum, per-finding evidence classification,
and deterministic rollup shared by the self-model audits and the compact
artifact sidecar contract (PLAN-20260717-0001). It must not import from
the self-model module or any sidecar implementation; both import from it.
It contains no auditor-specific classification tables.

Introduced by PLAN-20260719-0001 under GAP-0004 via WARR-20260719-0001.
"""

from __future__ import annotations

from typing import Iterable, Mapping


VERIFIED_CURRENT = "verified_current"
STALE = "stale"
UNVERIFIABLE = "unverifiable"

VERIFICATION_OUTCOMES = frozenset({VERIFIED_CURRENT, STALE, UNVERIFIABLE})

CLASS_DRIFT = "drift"
CLASS_EVIDENCE_UNAVAILABLE = "evidence_unavailable"
CLASS_OTHER = "other"

FINDING_CLASSES = frozenset(
    {CLASS_DRIFT, CLASS_EVIDENCE_UNAVAILABLE, CLASS_OTHER}
)

EVIDENCE_STATUS_NO_GIT_DIR = "no_git_dir"
EVIDENCE_STATUS_UNREACHABLE_REPO_HEAD = "unreachable_repo_head"
EVIDENCE_STATUS_OTHER = "other"

EVIDENCE_STATUSES = frozenset(
    {
        EVIDENCE_STATUS_NO_GIT_DIR,
        EVIDENCE_STATUS_UNREACHABLE_REPO_HEAD,
        EVIDENCE_STATUS_OTHER,
    }
)


class VerificationOutcomeError(ValueError):
    """Raised when verification outcome inputs are invalid."""


def validate_outcome(value: object) -> str:
    if value not in VERIFICATION_OUTCOMES:
        raise VerificationOutcomeError(
            "verification outcome must be one of: "
            + ", ".join(sorted(VERIFICATION_OUTCOMES))
        )
    return str(value)


def validate_finding_class(value: object) -> str:
    if value not in FINDING_CLASSES:
        raise VerificationOutcomeError(
            "finding class must be one of: "
            + ", ".join(sorted(FINDING_CLASSES))
        )
    return str(value)


def rollup_outcome(finding_classes: Iterable[object]) -> str:
    """Deterministic rollup: stale beats unverifiable beats verified_current.

    Confirmed drift anywhere yields stale even when other evidence is
    unavailable; missing evidence without confirmed drift yields
    unverifiable; otherwise verified_current. CLASS_OTHER never changes
    the outcome by itself.
    """

    saw_evidence_unavailable = False
    for value in finding_classes:
        cls = validate_finding_class(value)
        if cls == CLASS_DRIFT:
            return STALE
        if cls == CLASS_EVIDENCE_UNAVAILABLE:
            saw_evidence_unavailable = True
    if saw_evidence_unavailable:
        return UNVERIFIABLE
    return VERIFIED_CURRENT


def rollup_from_findings(
    findings: Iterable[Mapping[str, object]],
    *,
    class_field: str = "class",
) -> str:
    """Roll up an iterable of finding mappings by their class field.

    Findings without the class field are treated as CLASS_OTHER, so
    legacy findings never change the outcome on their own.
    """

    return rollup_outcome(
        finding.get(class_field, CLASS_OTHER) for finding in findings
    )


def ok_from_outcome(outcome: object) -> bool:
    """Fail-closed boolean: true only for verified_current, never null."""

    return validate_outcome(outcome) == VERIFIED_CURRENT
