import pytest

from ai_lab.documentation.context_pack import (
    ContextPackError,
    ContextPackExclusion,
    ContextPackItem,
    ContextPackManifest,
    compute_manifest_id,
)


def test_compute_manifest_id_is_deterministic():
    first = compute_manifest_id(
        task="Build prompt context.",
        assembly_policy="hybrid",
        item_ids=("ABS-0003", "SYNCOMP-0003"),
    )
    second = compute_manifest_id(
        task="Build prompt context.",
        assembly_policy="hybrid",
        item_ids=("ABS-0003", "SYNCOMP-0003"),
    )

    assert first == second
    assert len(first) == 16


def test_context_pack_item_builds_valid_item():
    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction for memory implementation.",
        relevance_score=0.95,
        token_estimate=1200,
        source_path="docs/abstractions/ABS-0003.md",
        citation="3ac9f2b1d0af@a1c2d3e|b:100-200",
    )

    assert item.item_type == "abstraction"
    assert item.item_id == "ABS-0003"
    assert item.relevance_score == 0.95


def test_context_pack_manifest_builds_valid_manifest():
    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction for memory implementation.",
        relevance_score=0.95,
        token_estimate=1200,
    )

    manifest = ContextPackManifest(
        task="Prepare context for the next implementation step.",
        assembly_policy="latest_context",
        items=(item,),
        token_budget=8000,
        model_target="gpt-5",
        pipeline_run_id="run_001",
    )

    assert manifest.manifest_id == compute_manifest_id(
        task="Prepare context for the next implementation step.",
        assembly_policy="latest_context",
        item_ids=("ABS-0003",),
    )
    assert manifest.total_token_estimate == 1200


def test_context_pack_exclusion_builds_valid_exclusion():
    exclusion = ContextPackExclusion(
        item_id="COMP-0001",
        reason="superseded",
        note="Later comparison covers the same implementation decision.",
    )

    assert exclusion.to_dict() == {
        "item_id": "COMP-0001",
        "reason": "superseded",
        "note": "Later comparison covers the same implementation decision.",
    }


def test_context_pack_item_rejects_invalid_type_or_score():
    with pytest.raises(ContextPackError):
        ContextPackItem(
            item_type="unknown",
            item_id="ABS-0003",
            reason="Invalid item type.",
            relevance_score=0.5,
        )

    with pytest.raises(ContextPackError):
        ContextPackItem(
            item_type="abstraction",
            item_id="ABS-0003",
            reason="Invalid relevance score.",
            relevance_score=1.5,
        )


def test_context_pack_manifest_rejects_empty_items():
    with pytest.raises(ContextPackError):
        ContextPackManifest(
            task="Prepare context.",
            assembly_policy="latest_context",
            items=(),
        )


def test_context_pack_manifest_rejects_wrong_manifest_id():
    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction for memory implementation.",
        relevance_score=0.95,
    )

    with pytest.raises(ContextPackError):
        ContextPackManifest(
            task="Prepare context.",
            assembly_policy="latest_context",
            items=(item,),
            manifest_id="wrong",
        )


def test_context_pack_exclusion_rejects_invalid_reason():
    with pytest.raises(ContextPackError):
        ContextPackExclusion(
            item_id="COMP-0001",
            reason="not_a_reason",
        )


def test_context_pack_manifest_to_dict_serializes_metadata():
    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction for memory implementation.",
        relevance_score=0.95,
        token_estimate=1200,
        source_path="docs/abstractions/ABS-0003.md",
    )

    exclusion = ContextPackExclusion(
        item_id="COMP-0001",
        reason="superseded",
    )

    manifest = ContextPackManifest(
        task="Prepare context for implementation.",
        assembly_policy="hybrid",
        items=(item,),
        token_budget=8000,
        exclusions=(exclusion,),
        created_at="2026-06-30T00:00:00+00:00",
        model_target="gpt-5",
        pipeline_run_id="run_001",
    )

    data = manifest.to_dict()

    assert data["manifest_id"] == manifest.manifest_id
    assert data["task"] == "Prepare context for implementation."
    assert data["assembly_policy"] == "hybrid"
    assert data["total_token_estimate"] == 1200
    assert data["token_budget"] == 8000
    assert data["model_target"] == "gpt-5"
    assert data["items"] == [
        {
            "item_type": "abstraction",
            "item_id": "ABS-0003",
            "reason": "Latest abstraction for memory implementation.",
            "relevance_score": 0.95,
            "token_estimate": 1200,
            "source_path": "docs/abstractions/ABS-0003.md",
        }
    ]
    assert data["exclusions"] == [
        {
            "item_id": "COMP-0001",
            "reason": "superseded",
        }
    ]
    assert data["provenance"] == {
        "pipeline_run_id": "run_001",
    }


def test_context_pack_item_accepts_episode_l1_type():
    item = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-0001",
        reason="Latest episode L1 summary.",
        relevance_score=0.92,
        token_estimate=200,
        source_path="docs/memory/l1/L1-0001.json",
    )

    assert item.item_type == "episode_l1"
    assert item.item_id == "L1-0001"
