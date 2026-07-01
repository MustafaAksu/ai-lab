from ai_lab.documentation.context_pack import (
    ContextPackExclusion,
    ContextPackItem,
    ContextPackManifest,
)
from ai_lab.documentation.context_pack_renderer import render_context_pack_markdown


def test_render_context_pack_markdown_includes_selected_source(tmp_path):
    source = tmp_path / "ABS-0003.md"
    source.write_text("# ABS-0003\n\nStable memory implementation summary.", encoding="utf-8")

    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction for memory implementation.",
        relevance_score=0.9,
        token_estimate=100,
        source_path=str(source),
    )

    manifest = ContextPackManifest(
        task="Prepare implementation context.",
        assembly_policy="latest_context",
        items=(item,),
        token_budget=8000,
        model_target="gpt-5",
    )

    markdown = render_context_pack_markdown(manifest)

    assert f"# Context Pack {manifest.manifest_id}" in markdown
    assert "Task: Prepare implementation context." in markdown
    assert "### ABS-0003 (abstraction)" in markdown
    assert "BEGIN SOURCE CONTENT" in markdown
    assert "Stable memory implementation summary." in markdown
    assert "END SOURCE CONTENT" in markdown


def test_render_context_pack_markdown_includes_exclusions(tmp_path):
    source = tmp_path / "ABS-0003.md"
    source.write_text("# ABS-0003", encoding="utf-8")

    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction.",
        relevance_score=0.9,
        token_estimate=100,
        source_path=str(source),
    )

    exclusion = ContextPackExclusion(
        item_id="SYNCOMP-0003",
        reason="too_large",
        note="Estimated 8819 tokens would exceed budget 8000.",
    )

    manifest = ContextPackManifest(
        task="Prepare implementation context.",
        assembly_policy="latest_context",
        items=(item,),
        exclusions=(exclusion,),
    )

    markdown = render_context_pack_markdown(manifest)

    assert "## Excluded Context" in markdown
    assert (
        "- SYNCOMP-0003: too_large — Estimated 8819 tokens would exceed budget 8000."
        in markdown
    )


def test_render_context_pack_markdown_handles_missing_source():
    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction.",
        relevance_score=0.9,
        token_estimate=100,
        source_path="missing/path.md",
    )

    manifest = ContextPackManifest(
        task="Prepare implementation context.",
        assembly_policy="latest_context",
        items=(item,),
    )

    markdown = render_context_pack_markdown(manifest)

    assert "[source file not found: missing/path.md]" in markdown
