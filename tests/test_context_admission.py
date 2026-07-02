import pytest

from ai_lab.documentation.context_admission import (
    ContextAdmissionError,
    ContextAdmissionVerdict,
    compute_context_admission_verdict_id,
)


def test_context_admission_verdict_builds_with_deterministic_id():
    verdict = ContextAdmissionVerdict.build(
        target_item_id="L1-20260702-memory-refresh",
        target_item_type="episode_l1",
        decision="admit",
        freshness_state="fresh",
        warrant_state="supported",
        author="mustafa",
        substrate="human",
        created_at="2026-07-02T13:30:00+00:00",
        reason="Manual L1 refresh was inspected and committed.",
        evidence_ids=["ef71fce"],
        evidence_paths=["docs/memory/l1/L1-20260702-memory-refresh.json"],
        citations=["3ac9f2b1d0af@a1c2d3e|b:1024-2047"],
    )

    assert verdict.verdict_id == compute_context_admission_verdict_id(
        target_item_id="L1-20260702-memory-refresh",
        target_item_type="episode_l1",
        decision="admit",
        freshness_state="fresh",
        warrant_state="supported",
        author="mustafa",
        substrate="human",
        created_at="2026-07-02T13:30:00+00:00",
    )
    assert verdict.verdict_id.startswith("CADM-")
    assert verdict.evidence_ids == ("ef71fce",)
    assert verdict.evidence_paths == ("docs/memory/l1/L1-20260702-memory-refresh.json",)


def test_context_admission_verdict_json_round_trip(tmp_path):
    verdict = ContextAdmissionVerdict.build(
        target_item_id="ABS-0003",
        target_item_type="abstraction",
        decision="admit_with_warning",
        freshness_state="unknown",
        warrant_state="unreviewed",
        author="ai-lab",
        substrate="process",
        created_at="2026-07-02T13:31:00+00:00",
        reason="Legacy abstraction is still useful but should be refreshed.",
        evidence_ids=["COMP-0009", "SYNCOMP-0005"],
        note="Included only as older context.",
    )

    target = tmp_path / "verdict.json"
    verdict.write_json(target)
    loaded = ContextAdmissionVerdict.read_json(target)

    assert loaded == verdict
    assert loaded.evidence_ids == ("COMP-0009", "SYNCOMP-0005")


def test_context_admission_verdict_rejects_unknown_item_type():
    with pytest.raises(ContextAdmissionError, match="target_item_type"):
        ContextAdmissionVerdict.build(
            target_item_id="X-0001",
            target_item_type="unknown",
            decision="admit",
            freshness_state="fresh",
            warrant_state="supported",
            author="mustafa",
            substrate="human",
            created_at="2026-07-02T13:32:00+00:00",
            reason="Invalid item type.",
        )


def test_context_admission_verdict_rejects_disputed_direct_admit():
    with pytest.raises(ContextAdmissionError, match="decision=admit"):
        ContextAdmissionVerdict.build(
            target_item_id="COMP-0009",
            target_item_type="comparison",
            decision="admit",
            freshness_state="fresh",
            warrant_state="disputed",
            author="mustafa",
            substrate="human",
            created_at="2026-07-02T13:33:00+00:00",
            reason="Disputed item cannot be admitted without warning.",
        )


def test_context_admission_verdict_allows_disputed_with_warning():
    verdict = ContextAdmissionVerdict.build(
        target_item_id="COMP-0009",
        target_item_type="comparison",
        decision="admit_with_warning",
        freshness_state="fresh",
        warrant_state="disputed",
        author="mustafa",
        substrate="human",
        created_at="2026-07-02T13:34:00+00:00",
        reason="Disputed item may be visible with explicit warning.",
    )

    assert verdict.decision == "admit_with_warning"


def test_context_admission_verdict_rejects_stale_non_exclusion():
    with pytest.raises(ContextAdmissionError, match="stale items"):
        ContextAdmissionVerdict.build(
            target_item_id="ABS-0003",
            target_item_type="abstraction",
            decision="admit_with_warning",
            freshness_state="stale",
            warrant_state="supported",
            author="ai-lab",
            substrate="process",
            created_at="2026-07-02T13:35:00+00:00",
            reason="Stale item should not enter under current policy.",
        )


def test_context_admission_verdict_rejects_bad_citation():
    with pytest.raises(ContextAdmissionError, match="Invalid citation"):
        ContextAdmissionVerdict.build(
            target_item_id="L1-20260702-memory-refresh",
            target_item_type="episode_l1",
            decision="admit",
            freshness_state="fresh",
            warrant_state="supported",
            author="mustafa",
            substrate="human",
            created_at="2026-07-02T13:36:00+00:00",
            reason="Bad citation should fail.",
            citations=["not-a-citation"],
        )


def test_context_admission_read_json_rejects_non_object_payload(tmp_path):
    target = tmp_path / "bad.json"
    target.write_text("[]", encoding="utf-8")

    with pytest.raises(ContextAdmissionError, match="JSON payload must be an object"):
        ContextAdmissionVerdict.read_json(target)
