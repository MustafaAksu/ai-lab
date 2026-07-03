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


def test_render_context_pack_includes_admission_metadata(tmp_path):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from ai_lab.documentation.context_pack_renderer import render_context_pack_markdown

    source = tmp_path / "l1.json"
    source.write_text('{"summary_text": "Admitted L1 summary."}', encoding="utf-8")

    item = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-0001",
        reason="Latest admitted L1.",
        relevance_score=0.92,
        token_estimate=100,
        source_path=str(source),
        admission_verdict_id="CADM-0001",
        admission_decision="admit",
        freshness_state="fresh",
        warrant_state="supported",
    )

    manifest = ContextPackManifest(
        task="Render admitted L1.",
        assembly_policy="latest_context",
        items=(item,),
    )

    rendered = render_context_pack_markdown(manifest)

    assert "Admission verdict: CADM-0001" in rendered
    assert "Admission decision: admit" in rendered
    assert "Freshness state: fresh" in rendered
    assert "Warrant state: supported" in rendered


def test_render_context_pack_includes_admission_summary(tmp_path):
    source = tmp_path / "l1.json"
    source.write_text('{"summary_text": "Admitted L1 summary."}', encoding="utf-8")

    item = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-0001",
        reason="Latest admitted L1.",
        relevance_score=0.92,
        token_estimate=100,
        source_path=str(source),
        admission_decision="admit",
    )

    manifest = ContextPackManifest(
        task="Render admission summary.",
        assembly_policy="latest_context",
        items=(item,),
        admission_summary={
            "admit": 1,
            "admit_with_warning": 0,
            "excluded_by_policy": 2,
        },
    )

    rendered = render_context_pack_markdown(manifest)

    assert "Admission summary:" in rendered
    assert "- admit: 1" in rendered
    assert "- admit_with_warning: 0" in rendered
    assert "- excluded_by_policy: 2" in rendered


def test_render_context_pack_includes_admission_policy(tmp_path):
    source = tmp_path / "l1.json"
    source.write_text('{"summary_text": "Admitted L1 summary."}', encoding="utf-8")

    item = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-0001",
        reason="Latest admitted L1.",
        relevance_score=0.92,
        token_estimate=100,
        source_path=str(source),
        admission_decision="admit",
    )

    manifest = ContextPackManifest(
        task="Render admission policy.",
        assembly_policy="latest_context",
        items=(item,),
        admission_policy={
            "require_admission": True,
            "max_warning_admissions": 1,
        },
    )

    rendered = render_context_pack_markdown(manifest)

    assert "Admission policy:" in rendered
    assert "- require_admission: True" in rendered
    assert "- max_warning_admissions: 1" in rendered
