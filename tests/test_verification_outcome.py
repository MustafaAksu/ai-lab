import pytest

from ai_lab.documentation.verification_outcome import (
    CLASS_DRIFT,
    CLASS_EVIDENCE_UNAVAILABLE,
    CLASS_OTHER,
    STALE,
    UNVERIFIABLE,
    VERIFIED_CURRENT,
    VerificationOutcomeError,
    ok_from_outcome,
    rollup_from_findings,
    rollup_outcome,
)


def test_rollup_empty_is_verified_current():
    assert rollup_outcome([]) == VERIFIED_CURRENT


def test_rollup_other_only_is_verified_current():
    assert rollup_outcome([CLASS_OTHER, CLASS_OTHER]) == VERIFIED_CURRENT


def test_rollup_evidence_unavailable_is_unverifiable():
    assert rollup_outcome([CLASS_OTHER, CLASS_EVIDENCE_UNAVAILABLE]) == UNVERIFIABLE


def test_rollup_drift_is_stale():
    assert rollup_outcome([CLASS_DRIFT]) == STALE


def test_rollup_mixed_drift_beats_evidence_unavailable():
    assert (
        rollup_outcome(
            [CLASS_EVIDENCE_UNAVAILABLE, CLASS_DRIFT, CLASS_OTHER]
        )
        == STALE
    )


def test_rollup_rejects_unknown_class():
    with pytest.raises(VerificationOutcomeError):
        rollup_outcome(["bogus"])


def test_rollup_from_findings_defaults_missing_class_to_other():
    findings = [
        {"severity": "info", "code": "LEGACY_NO_CLASS"},
        {"severity": "warn", "class": CLASS_EVIDENCE_UNAVAILABLE},
    ]
    assert rollup_from_findings(findings) == UNVERIFIABLE


def test_ok_from_outcome_is_fail_closed_boolean():
    assert ok_from_outcome(VERIFIED_CURRENT) is True
    assert ok_from_outcome(STALE) is False
    assert ok_from_outcome(UNVERIFIABLE) is False
    with pytest.raises(VerificationOutcomeError):
        ok_from_outcome(None)


def test_module_exports_are_consistent():
    from ai_lab.documentation import verification_outcome as vo

    assert vo.VERIFICATION_OUTCOMES == {
        vo.VERIFIED_CURRENT,
        vo.STALE,
        vo.UNVERIFIABLE,
    }
    assert vo.FINDING_CLASSES == {
        vo.CLASS_DRIFT,
        vo.CLASS_EVIDENCE_UNAVAILABLE,
        vo.CLASS_OTHER,
    }
