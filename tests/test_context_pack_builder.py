from pathlib import Path

from ai_lab.documentation.context_pack import ContextPackError, ContextPackExclusion, ContextPackItem

from ai_lab.documentation.artifact_history import ArtifactRecord
from ai_lab.documentation.context_pack_builder import (
    build_latest_context_manifest,
    context_item_from_record,
    item_type_for_record,
)


def make_record(
    artifact_id,
    kind,
    title,
    path,
    created_at,
    abstraction_level=None,
):
    return ArtifactRecord(
        artifact_id=artifact_id,
        kind=kind,
        title=title,
        path=Path(path),
        created_at=created_at,
        source_comparison=None,
        source_synthesis=None,
        source_artifacts=(),
        abstraction_level=abstraction_level,
    )


def test_item_type_for_record_maps_history_kinds():
    assert item_type_for_record(
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            "docs/abstractions/ABS-0003.md",
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        )
    ) == "abstraction"

    assert item_type_for_record(
        make_record(
            "SYNCOMP-0003",
            "SYNCOMP",
            "Memory Synthesis",
            "docs/comparisons/syntheses/SYNCOMP-0003.md",
            "2026-06-30T00:00:00+00:00",
        )
    ) == "synthesis"

    assert item_type_for_record(
        make_record(
            "COMP-0007",
            "COMP",
            "Memory Comparison",
            "docs/comparisons/COMP-0007.md",
            "2026-06-30T00:00:00+00:00",
        )
    ) == "comparison"


def test_context_item_from_record_preserves_identity_and_path():
    record = make_record(
        "ABS-0003",
        "ABS",
        "AI-Lab Reconciled Memory Implementation Loop",
        "docs/abstractions/ABS-0003.md",
        "2026-06-30T00:00:00+00:00",
        abstraction_level=1,
    )

    item = context_item_from_record(
        record=record,
        relevance_score=0.9,
        token_estimate=1200,
    )

    assert item.item_type == "abstraction"
    assert item.item_id == "ABS-0003"
    assert item.relevance_score == 0.9
    assert item.token_estimate == 1200
    assert item.source_path == "docs/abstractions/ABS-0003.md"
    assert "ABS-L1 context seed" in item.reason


def test_build_latest_context_manifest_selects_latest_per_context_level():
    records = (
        make_record(
            "ABS-0002",
            "ABS",
            "Old Memory Loop",
            "docs/abstractions/ABS-0002.md",
            "2026-06-29T00:00:00+00:00",
            abstraction_level=1,
        ),
        make_record(
            "ABS-0003",
            "ABS",
            "New Memory Loop",
            "docs/abstractions/ABS-0003.md",
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
        make_record(
            "SYNCOMP-0003",
            "SYNCOMP",
            "Memory Synthesis",
            "docs/comparisons/syntheses/SYNCOMP-0003.md",
            "2026-06-30T00:00:00+00:00",
        ),
        make_record(
            "COMP-0007",
            "COMP",
            "Memory Comparison",
            "docs/comparisons/COMP-0007.md",
            "2026-06-30T00:00:00+00:00",
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare implementation context.",
        records=records,
        token_budget=8000,
        model_target="gpt-5",
        pipeline_run_id="run_001",
        l1_dir=Path("does-not-exist-test-l1"),
    )

    assert manifest.assembly_policy == "latest_context"
    assert manifest.token_budget == 8000
    assert manifest.model_target == "gpt-5"
    assert tuple(item.item_id for item in manifest.items) == (
        "ABS-0003",
        "SYNCOMP-0003",
        "COMP-0007",
    )


def test_estimate_tokens_for_text_uses_chars_over_four():
    from ai_lab.documentation.context_pack_builder import estimate_tokens_for_text

    assert estimate_tokens_for_text("") == 0
    assert estimate_tokens_for_text("abcd") == 1
    assert estimate_tokens_for_text("abcde") == 2


def test_context_item_from_record_estimates_tokens_from_file(tmp_path):
    artifact_path = tmp_path / "artifact.md"
    artifact_path.write_text("x" * 40, encoding="utf-8")

    record = make_record(
        "COMP-0008",
        "COMP",
        "Token Estimated Comparison",
        artifact_path,
        "2026-06-30T00:00:00+00:00",
    )

    item = context_item_from_record(
        record=record,
        relevance_score=0.9,
    )

    assert item.token_estimate == 10


def test_select_items_with_budget_excludes_items_that_do_not_fit():
    from ai_lab.documentation.context_pack import ContextPackItem
    from ai_lab.documentation.context_pack_builder import select_items_with_budget

    first = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Small seed.",
        relevance_score=0.9,
        token_estimate=100,
    )
    second = ContextPackItem(
        item_type="synthesis",
        item_id="SYNCOMP-0003",
        reason="Large synthesis.",
        relevance_score=0.9,
        token_estimate=1000,
    )

    selected, exclusions = select_items_with_budget(
        items=(first, second),
        token_budget=500,
    )

    assert selected == (first,)
    assert len(exclusions) == 1
    assert exclusions[0].item_id == "SYNCOMP-0003"
    assert exclusions[0].reason == "too_large"


def test_build_latest_context_manifest_records_budget_exclusions(tmp_path):
    small_path = tmp_path / "small.md"
    large_path = tmp_path / "large.md"

    small_path.write_text("x" * 400, encoding="utf-8")
    large_path.write_text("x" * 4000, encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Small Seed",
            small_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
        make_record(
            "SYNCOMP-0003",
            "SYNCOMP",
            "Large Synthesis",
            large_path,
            "2026-06-30T00:00:00+00:00",
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare budgeted context.",
        records=records,
        token_budget=500,
        l1_dir=tmp_path / "empty-l1",
    )

    assert tuple(item.item_id for item in manifest.items) == ("ABS-0003",)
    assert manifest.total_token_estimate == 100
    assert len(manifest.exclusions) == 1
    assert manifest.exclusions[0].item_id == "SYNCOMP-0003"
    assert manifest.exclusions[0].reason == "too_large"


def test_context_item_from_l1_summary_preserves_identity_and_path(tmp_path):
    from ai_lab.documentation.context_pack_builder import context_item_from_l1_summary
    from ai_lab.documentation.interaction_log import EpisodeL1Summary

    path = tmp_path / "L1-0001.json"
    summary = EpisodeL1Summary(
        l1_id="L1-0001",
        episode_id="EP-0001",
        created_at="2026-07-02T13:00:00+00:00",
        summary_version="v1",
        summary_text="Latest episode summary for memory freshness.",
        source_event_ids=["EVT-0001"],
        citations=[],
        freshness_state="fresh",
    )
    summary.write_json(path)

    item = context_item_from_l1_summary(
        summary=summary,
        path=path,
        token_estimate=123,
    )

    assert item.item_type == "episode_l1"
    assert item.item_id == "L1-0001"
    assert item.source_path == str(path)
    assert item.token_estimate == 123
    assert "Episode L1 context seed" in item.reason


def test_discover_latest_l1_summary_item_uses_newest_valid_summary(tmp_path):
    from ai_lab.documentation.context_pack_builder import discover_latest_l1_summary_item
    from ai_lab.documentation.interaction_log import EpisodeL1Summary

    l1_dir = tmp_path / "l1"
    l1_dir.mkdir()

    old_summary = EpisodeL1Summary(
        l1_id="L1-OLD",
        episode_id="EP-OLD",
        created_at="2026-07-02T12:00:00+00:00",
        summary_version="v1",
        summary_text="Old summary.",
        source_event_ids=["EVT-OLD"],
        citations=[],
    )
    old_summary.write_json(l1_dir / "old.json")

    new_summary = EpisodeL1Summary(
        l1_id="L1-NEW",
        episode_id="EP-NEW",
        created_at="2026-07-02T13:00:00+00:00",
        summary_version="v1",
        summary_text="New summary.",
        source_event_ids=["EVT-NEW"],
        citations=[],
        freshness_state="fresh",
    )
    new_summary.write_json(l1_dir / "new.json")

    (l1_dir / "invalid.json").write_text("[]", encoding="utf-8")

    item = discover_latest_l1_summary_item(l1_dir=l1_dir)

    assert item is not None
    assert item.item_id == "L1-NEW"
    assert item.item_type == "episode_l1"


def test_build_latest_context_manifest_includes_latest_l1_first(tmp_path):
    from ai_lab.documentation.interaction_log import EpisodeL1Summary

    l1_dir = tmp_path / "l1"
    l1_dir.mkdir()

    summary = EpisodeL1Summary(
        l1_id="L1-0001",
        episode_id="EP-0001",
        created_at="2026-07-02T13:00:00+00:00",
        summary_version="v1",
        summary_text="L1 should seed latest context before artifact records.",
        source_event_ids=["EVT-0001"],
        citations=[],
        freshness_state="fresh",
    )
    summary.write_json(l1_dir / "L1-0001.json")

    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("x" * 400, encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare context with L1.",
        records=records,
        token_budget=8000,
        l1_dir=l1_dir,
    )

    assert tuple(item.item_id for item in manifest.items) == ("L1-0001", "ABS-0003")
    assert manifest.items[0].item_type == "episode_l1"


def test_build_latest_context_manifest_budget_can_exclude_l1(tmp_path):
    from ai_lab.documentation.interaction_log import EpisodeL1Summary

    l1_dir = tmp_path / "l1"
    l1_dir.mkdir()

    summary = EpisodeL1Summary(
        l1_id="L1-LARGE",
        episode_id="EP-LARGE",
        created_at="2026-07-02T13:00:00+00:00",
        summary_version="v1",
        summary_text="x" * 4000,
        source_event_ids=["EVT-0001"],
        citations=[],
    )
    summary.write_json(l1_dir / "L1-LARGE.json")

    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("x" * 400, encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare budgeted context with L1.",
        records=records,
        token_budget=500,
        l1_dir=l1_dir,
    )

    assert tuple(item.item_id for item in manifest.items) == ("ABS-0003",)
    assert manifest.exclusions[0].item_id == "L1-LARGE"
    assert manifest.exclusions[0].reason == "too_large"


def test_annotate_items_with_admission_verdicts_adds_matching_verdict(tmp_path):
    from ai_lab.documentation.context_admission import ContextAdmissionVerdict
    from ai_lab.documentation.context_pack import ContextPackItem
    from ai_lab.documentation.context_pack_builder import annotate_items_with_admission_verdicts

    admission_dir = tmp_path / "admissions"
    admission_dir.mkdir()

    verdict = ContextAdmissionVerdict.build(
        target_item_id="L1-0001",
        target_item_type="episode_l1",
        decision="admit",
        freshness_state="fresh",
        warrant_state="supported",
        author="mustafa",
        substrate="human",
        created_at="2026-07-02T14:00:00+00:00",
        reason="L1 was manually inspected.",
    )
    verdict.write_json(admission_dir / "verdict.json")

    item = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-0001",
        reason="Latest L1.",
        relevance_score=0.92,
    )

    annotated = annotate_items_with_admission_verdicts(
        items=(item,),
        admission_dir=admission_dir,
    )

    assert annotated[0].admission_verdict_id == verdict.verdict_id
    assert annotated[0].admission_decision == "admit"
    assert annotated[0].freshness_state == "fresh"
    assert annotated[0].warrant_state == "supported"


def test_build_latest_context_manifest_records_l1_admission_verdict(tmp_path):
    from ai_lab.documentation.context_admission import ContextAdmissionVerdict
    from ai_lab.documentation.interaction_log import EpisodeL1Summary

    l1_dir = tmp_path / "l1"
    admission_dir = tmp_path / "admissions"
    l1_dir.mkdir()
    admission_dir.mkdir()

    summary = EpisodeL1Summary(
        l1_id="L1-0001",
        episode_id="EP-0001",
        created_at="2026-07-02T14:00:00+00:00",
        summary_version="v1",
        summary_text="L1 summary with admission verdict.",
        source_event_ids=["EVT-0001"],
        citations=[],
        freshness_state="fresh",
    )
    summary.write_json(l1_dir / "L1-0001.json")

    verdict = ContextAdmissionVerdict.build(
        target_item_id="L1-0001",
        target_item_type="episode_l1",
        decision="admit",
        freshness_state="fresh",
        warrant_state="supported",
        author="mustafa",
        substrate="human",
        created_at="2026-07-02T14:01:00+00:00",
        reason="Manual admission test.",
    )
    verdict.write_json(admission_dir / "CADM-L1-0001.json")

    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("x" * 400, encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare context with admitted L1.",
        records=records,
        token_budget=8000,
        l1_dir=l1_dir,
        admission_dir=admission_dir,
    )

    assert manifest.items[0].item_id == "L1-0001"
    assert manifest.items[0].admission_verdict_id == verdict.verdict_id
    assert manifest.to_dict()["items"][0]["admission_decision"] == "admit"


def test_filter_items_by_admission_requirement_keeps_admitted_items():
    from ai_lab.documentation.context_pack import ContextPackItem
    from ai_lab.documentation.context_pack_builder import (
        filter_items_by_admission_requirement,
    )

    admitted = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-ADMITTED",
        reason="Admitted.",
        relevance_score=0.92,
        admission_verdict_id="CADM-1",
        admission_decision="admit",
        freshness_state="fresh",
        warrant_state="supported",
    )
    unreviewed = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Unreviewed.",
        relevance_score=0.9,
    )

    selected, exclusions = filter_items_by_admission_requirement(
        items=(admitted, unreviewed),
    )

    assert selected == (admitted,)
    assert len(exclusions) == 1
    assert exclusions[0].item_id == "ABS-0003"
    assert exclusions[0].reason == "policy"
    assert exclusions[0].note == "No admission verdict; require_admission is enabled."


def test_filter_items_by_admission_requirement_keeps_admit_with_warning():
    from ai_lab.documentation.context_pack import ContextPackItem
    from ai_lab.documentation.context_pack_builder import (
        filter_items_by_admission_requirement,
    )

    warned = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-WARNED",
        reason="Admitted with warning.",
        relevance_score=0.92,
        admission_verdict_id="CADM-2",
        admission_decision="admit_with_warning",
        freshness_state="fresh",
        warrant_state="unreviewed",
    )

    selected, exclusions = filter_items_by_admission_requirement(items=(warned,))

    assert selected == (warned,)
    assert exclusions == ()


def test_filter_items_by_admission_requirement_rejects_excluded_items():
    import pytest

    from ai_lab.documentation.context_pack import ContextPackError, ContextPackItem
    from ai_lab.documentation.context_pack_builder import (
        filter_items_by_admission_requirement,
    )

    excluded = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-EXCLUDED",
        reason="Excluded.",
        relevance_score=0.92,
        admission_verdict_id="CADM-3",
        admission_decision="exclude",
        freshness_state="fresh",
        warrant_state="supported",
    )

    with pytest.raises(
        ContextPackError,
        match="No context items passed the admission requirement.",
    ):
        filter_items_by_admission_requirement(items=(excluded,))


def test_build_latest_context_manifest_records_prompt_telemetry(tmp_path):
    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("Memory abstraction.", encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare context.",
        records=records,
        task_label="prepare-context",
        full_prompt_hash="b" * 64,
        l1_dir=tmp_path / "empty-l1",
        admission_dir=tmp_path / "empty-admissions",
    )

    assert manifest.task_label == "prepare-context"
    assert manifest.full_prompt_hash == "b" * 64
    assert manifest.to_dict()["task_label"] == "prepare-context"
    assert manifest.to_dict()["full_prompt_hash"] == "b" * 64


def test_admission_summary_for_manifest_counts_selected_and_policy_exclusions():
    admitted = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-ADMIT",
        reason="Admitted L1.",
        relevance_score=0.92,
        admission_decision="admit",
    )
    warning = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-WARN",
        reason="Warning abstraction.",
        relevance_score=0.9,
        admission_decision="admit_with_warning",
    )
    policy_exclusion = ContextPackExclusion(
        item_id="COMP-UNREVIEWED",
        reason="policy",
        note="No admission verdict.",
    )
    size_exclusion = ContextPackExclusion(
        item_id="SYNCOMP-LARGE",
        reason="too_large",
        note="Too large.",
    )

    from ai_lab.documentation.context_pack_builder import admission_summary_for_manifest

    assert admission_summary_for_manifest(
        items=(admitted, warning),
        exclusions=(policy_exclusion, size_exclusion),
    ) == {
        "admit": 1,
        "admit_with_warning": 1,
        "excluded_by_policy": 1,
    }


def test_build_latest_context_manifest_records_admission_summary(tmp_path):
    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("Memory abstraction.", encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    verdict_dir = tmp_path / "admissions"
    verdict_dir.mkdir()
    (verdict_dir / "CADM-ABS-0003.json").write_text(
        """{
  "verdict_id": "CADM-ABS-0003",
  "target_item_id": "ABS-0003",
  "target_item_type": "abstraction",
  "decision": "admit_with_warning",
  "freshness_state": "unknown",
  "warrant_state": "supported",
  "reason": "Legacy abstraction admitted with warning.",
  "author": "mustafa",
  "substrate": "human",
  "created_at": "2026-07-02T00:00:00+00:00"
}
""",
        encoding="utf-8",
    )

    manifest = build_latest_context_manifest(
        task="Prepare context.",
        records=records,
        l1_dir=tmp_path / "empty-l1",
        admission_dir=verdict_dir,
        require_admission=True,
    )

    assert manifest.admission_summary == {
        "admit": 0,
        "admit_with_warning": 1,
        "excluded_by_policy": 0,
    }
    assert manifest.to_dict()["admission_summary"] == manifest.admission_summary


def test_cap_admit_with_warning_items_keeps_first_warnings_and_excludes_extra():
    from ai_lab.documentation.context_pack_builder import cap_admit_with_warning_items

    admitted = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-ADMIT",
        reason="Admitted L1.",
        relevance_score=0.92,
        admission_decision="admit",
    )
    first_warning = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-WARN-1",
        reason="Warning abstraction 1.",
        relevance_score=0.9,
        admission_decision="admit_with_warning",
    )
    second_warning = ContextPackItem(
        item_type="synthesis",
        item_id="SYNCOMP-WARN-2",
        reason="Warning synthesis 2.",
        relevance_score=0.8,
        admission_decision="admit_with_warning",
    )

    selected, exclusions = cap_admit_with_warning_items(
        items=(admitted, first_warning, second_warning),
        max_warning_admissions=1,
    )

    assert tuple(item.item_id for item in selected) == ("L1-ADMIT", "ABS-WARN-1")
    assert len(exclusions) == 1
    assert exclusions[0].item_id == "SYNCOMP-WARN-2"
    assert exclusions[0].reason == "policy"
    assert exclusions[0].note == "admit_with_warning cap 1 exceeded."


def test_cap_admit_with_warning_items_none_preserves_items():
    from ai_lab.documentation.context_pack_builder import cap_admit_with_warning_items

    warning = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-WARN",
        reason="Warning abstraction.",
        relevance_score=0.9,
        admission_decision="admit_with_warning",
    )

    selected, exclusions = cap_admit_with_warning_items(
        items=(warning,),
        max_warning_admissions=None,
    )

    assert selected == (warning,)
    assert exclusions == ()


def test_cap_admit_with_warning_items_rejects_negative_cap():
    from ai_lab.documentation.context_pack_builder import cap_admit_with_warning_items

    warning = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-WARN",
        reason="Warning abstraction.",
        relevance_score=0.9,
        admission_decision="admit_with_warning",
    )

    import pytest

    with pytest.raises(ContextPackError, match="max_warning_admissions must be >= 0"):
        cap_admit_with_warning_items(
            items=(warning,),
            max_warning_admissions=-1,
        )


def test_build_latest_context_manifest_applies_warning_cap(tmp_path):
    first_path = tmp_path / "ABS-0003.md"
    first_path.write_text("Warning abstraction.", encoding="utf-8")
    second_path = tmp_path / "SYNCOMP-0003.md"
    second_path.write_text("Warning synthesis.", encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            first_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
        make_record(
            "SYNCOMP-0003",
            "SYNCOMP",
            "Memory Synthesis",
            second_path,
            "2026-07-01T00:00:00+00:00",
        ),
    )

    verdict_dir = tmp_path / "admissions"
    verdict_dir.mkdir()

    for item_id, item_type in (
        ("ABS-0003", "abstraction"),
        ("SYNCOMP-0003", "synthesis"),
    ):
        (verdict_dir / f"CADM-{item_id}.json").write_text(
            f"""{{
  "verdict_id": "CADM-{item_id}",
  "target_item_id": "{item_id}",
  "target_item_type": "{item_type}",
  "decision": "admit_with_warning",
  "freshness_state": "unknown",
  "warrant_state": "supported",
  "reason": "Legacy item admitted with warning.",
  "author": "mustafa",
  "substrate": "human",
  "created_at": "2026-07-02T00:00:00+00:00"
}}
""",
            encoding="utf-8",
        )

    manifest = build_latest_context_manifest(
        task="Prepare capped warning context.",
        records=records,
        l1_dir=tmp_path / "empty-l1",
        admission_dir=verdict_dir,
        require_admission=True,
        max_warning_admissions=1,
    )

    assert tuple(item.item_id for item in manifest.items) == ("ABS-0003",)
    assert tuple(exclusion.item_id for exclusion in manifest.exclusions) == (
        "SYNCOMP-0003",
    )
    assert manifest.admission_summary == {
        "admit": 0,
        "admit_with_warning": 1,
        "excluded_by_policy": 1,
    }


def test_admission_policy_for_manifest_records_require_and_cap():
    from ai_lab.documentation.context_pack_builder import admission_policy_for_manifest

    assert admission_policy_for_manifest(
        require_admission=True,
        max_warning_admissions=1,
    ) == {
        "require_admission": True,
        "max_warning_admissions": 1,
    }


def test_admission_policy_for_manifest_omits_unset_cap():
    from ai_lab.documentation.context_pack_builder import admission_policy_for_manifest

    assert admission_policy_for_manifest(
        require_admission=False,
        max_warning_admissions=None,
    ) == {
        "require_admission": False,
    }


def test_build_latest_context_manifest_records_admission_policy(tmp_path):
    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("Memory abstraction.", encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare policy context.",
        records=records,
        l1_dir=tmp_path / "empty-l1",
        admission_dir=tmp_path / "empty-admissions",
        require_admission=False,
        max_warning_admissions=1,
    )

    assert manifest.admission_policy == {
        "require_admission": False,
        "max_warning_admissions": 1,
    }
    assert manifest.to_dict()["admission_policy"] == manifest.admission_policy


def write_l0_record(path, chunk_id="chunk-a", summary_text="Explicit L0 summary."):
    import json

    data = {
        "chunk_reference": {
            "chunk_id": chunk_id,
            "artifact_cid": "3ac9f2b1d0af",
            "version": "a1c2d3e",
            "span": {"unit": "b", "start": 100, "end": 200},
            "artifact_type": "doc",
            "embedding_ids": [],
            "redaction_level": "none",
        },
        "citation": "3ac9f2b1d0af@a1c2d3e|b:100-200",
        "l0_summary": summary_text,
        "keyphrases": ["citation", "span", "validation"],
        "entities": [],
        "claims": [],
        "risks": [],
        "created_at": "2026-07-03T00:00:00+00:00",
        "last_refreshed_at": "2026-07-03T00:00:00+00:00",
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


def test_build_latest_context_manifest_includes_explicit_l0_summary(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    write_l0_record(l0_store / "chunk-a.json")

    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("Memory abstraction.", encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare context with explicit L0.",
        records=records,
        include_l0=("chunk-a",),
        l0_store=l0_store,
        l1_dir=tmp_path / "empty-l1",
    )

    assert tuple(item.item_id for item in manifest.items) == ("chunk-a", "ABS-0003")
    assert manifest.items[0].item_type == "l0_summary"
    assert manifest.items[0].source_path == str(l0_store / "chunk-a.json")
    assert manifest.items[0].citation == "3ac9f2b1d0af@a1c2d3e|b:100-200"
    assert manifest.exclusions == ()


def test_build_latest_context_manifest_skips_missing_explicit_l0(tmp_path):
    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("Memory abstraction.", encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare context with missing explicit L0.",
        records=records,
        include_l0=("missing-chunk",),
        l0_store=tmp_path / "missing-l0",
        l1_dir=tmp_path / "empty-l1",
    )

    assert tuple(item.item_id for item in manifest.items) == ("ABS-0003",)
    assert len(manifest.exclusions) == 1
    assert manifest.exclusions[0].item_id == "missing-chunk"
    assert manifest.exclusions[0].reason == "policy"
    assert manifest.exclusions[0].note == "Requested explicit L0 summary was not found."


def test_build_latest_context_manifest_skips_malformed_explicit_l0(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    (l0_store / "chunk-a.json").write_text('{"chunk_reference": {"chunk_id": "chunk-a"}}', encoding="utf-8")

    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("Memory abstraction.", encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare context with malformed explicit L0.",
        records=records,
        include_l0=("chunk-a",),
        l0_store=l0_store,
        l1_dir=tmp_path / "empty-l1",
    )

    assert tuple(item.item_id for item in manifest.items) == ("ABS-0003",)
    assert len(manifest.exclusions) == 1
    assert manifest.exclusions[0].item_id == "chunk-a"
    assert manifest.exclusions[0].reason == "policy"
    assert manifest.exclusions[0].note == "Requested explicit L0 summary failed record validation."


def test_build_latest_context_manifest_budget_can_exclude_explicit_l0(tmp_path):
    l0_store = tmp_path / "l0"
    l0_store.mkdir()
    write_l0_record(l0_store / "chunk-a.json", summary_text="x" * 300)

    artifact_path = tmp_path / "ABS-0003.md"
    artifact_path.write_text("x" * 40, encoding="utf-8")

    records = (
        make_record(
            "ABS-0003",
            "ABS",
            "Memory Loop",
            artifact_path,
            "2026-06-30T00:00:00+00:00",
            abstraction_level=1,
        ),
    )

    manifest = build_latest_context_manifest(
        task="Prepare budgeted context with explicit L0.",
        records=records,
        token_budget=20,
        include_l0=("chunk-a",),
        l0_store=l0_store,
        l1_dir=tmp_path / "empty-l1",
    )

    assert tuple(item.item_id for item in manifest.items) == ("ABS-0003",)
    assert any(
        exclusion.item_id == "chunk-a" and exclusion.reason == "too_large"
        for exclusion in manifest.exclusions
    )
