import json
from pathlib import Path

from ai_lab.documentation.artifact_history import discover_artifacts
from ai_lab.documentation.compact_graph_representation_evaluation import (
    TOKEN_ESTIMATOR_ID,
    estimate_text_tokens,
    evaluate_compact_graph_representations,
    format_compact_graph_representation_report,
    inventory_repository_representations,
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def metadata(identifier: str, title: str, extra: str = "") -> str:
    key = {
        "COMP": "comparison_id",
        "SYNCOMP": "synthesis_id",
        "ABS": "abstraction_id",
    }[identifier.split("-")[0]]
    return (
        "## Metadata\n\n"
        f"- {key}: `{identifier}`\n"
        f"- title: `{title}`\n"
        f"{extra}"
    )


def test_inventory_finds_existing_sections_and_repository_records(tmp_path: Path):
    comparisons = tmp_path / "docs" / "comparisons"
    abstractions = tmp_path / "docs" / "abstractions"

    write(
        comparisons / "COMP-0001-root.md",
        "# Root\n\n" + metadata("COMP-0001", "Root") + "\n\nfull comparison",
    )
    write(
        comparisons / "syntheses" / "SYNCOMP-0001-root.md",
        "# Synthesis\n\n"
        + metadata(
            "SYNCOMP-0001",
            "Root Synthesis",
            "- source_comparison: `docs/comparisons/COMP-0001-root.md`\n",
        )
        + "\n## Synthesis\n\n~~~text\ncompact synthesis\n~~~\n",
    )
    write(
        abstractions / "ABS-0001-root.md",
        "# Abstraction\n\n"
        + metadata(
            "ABS-0001",
            "Root Abstraction",
            "- source_artifacts: `docs/comparisons/syntheses/SYNCOMP-0001-root.md`\n",
        )
        + "\n## Abstraction\n\ncompact abstraction\n",
    )

    l0_dir = tmp_path / "docs" / "memory" / "l0"
    l1_dir = tmp_path / "docs" / "memory" / "l1"
    write(l0_dir / "L0-0001.json", json.dumps({"l0_summary": "summary"}))
    write(
        l1_dir / "L1-0001.json",
        json.dumps({"citations": ["COMP-0001"], "summary_text": "episode"}),
    )
    write(
        tmp_path / "docs" / "artifact-summary.json",
        json.dumps(
            {
                "artifact_cid": "abcdef123456",
                "version": "v1",
                "path": "docs/example.md",
                "artifact_type": "doc",
                "language": "markdown",
                "size_bytes": 10,
                "complexity_score": 0.1,
            }
        ),
    )

    records = discover_artifacts(comparisons, abstractions)
    inventory = inventory_repository_representations(
        artifact_records=records,
        l0_dir=l0_dir,
        l1_dir=l1_dir,
        docs_root=tmp_path / "docs",
    )

    assert inventory.token_estimator_id == TOKEN_ESTIMATOR_ID
    assert inventory.artifact_count == 3
    assert dict(inventory.artifact_kind_counts) == {
        "ABS": 1,
        "COMP": 1,
        "SYNCOMP": 1,
    }
    assert inventory.semantic_compact_artifact_count == 2
    assert dict(inventory.semantic_compact_kind_counts) == {
        "ABS": 1,
        "SYNCOMP": 1,
    }
    assert inventory.l0_record_count == 1
    assert inventory.l1_record_count == 1
    assert inventory.l1_record_count_with_citations == 1
    assert inventory.l1_record_count_with_canonical_artifact_links == 1
    assert inventory.artifact_summary_record_count == 1

    profiles = {profile.artifact_id: profile for profile in inventory.profiles}
    assert profiles["COMP-0001"].semantic_compact_available is False
    assert profiles["SYNCOMP-0001"].semantic_compact_source == (
        "markdown_section:Synthesis"
    )
    assert profiles["ABS-0001"].semantic_compact_source == (
        "markdown_section:Abstraction"
    )
    assert all(
        profile.metadata_lower_bound_semantically_sufficient is False
        for profile in profiles.values()
    )


def test_evaluation_preserves_baseline_and_exposes_contract_gap(tmp_path: Path):
    comparisons = tmp_path / "docs" / "comparisons"

    root_body = " ".join(f"root{i}" for i in range(80))
    child_body = " ".join(f"child{i}" for i in range(10))

    write(
        comparisons / "COMP-0001-root.md",
        "# Root\n\n" + metadata("COMP-0001", "Root") + "\n\n" + root_body,
    )
    write(
        comparisons / "syntheses" / "SYNCOMP-0001-root.md",
        "# Synthesis\n\n"
        + metadata(
            "SYNCOMP-0001",
            "Root Synthesis",
            "- source_comparison: `docs/comparisons/COMP-0001-root.md`\n",
        )
        + "\n## Synthesis\n\nshort synthesis\n",
    )
    write(
        comparisons / "COMP-0002-target.md",
        "# Target\n\n"
        + metadata(
            "COMP-0002",
            "Target",
            (
                "- source_synthesis: `docs/comparisons/syntheses/"
                "SYNCOMP-0001-root.md`\n"
            ),
        )
        + "\n"
        + child_body,
    )
    write(
        comparisons / "COMP-0003-post-audit.md",
        "# Later\n\n" + metadata("COMP-0003", "Later"),
    )

    records = discover_artifacts(comparisons)
    report = evaluate_compact_graph_representations(
        evaluation_id="EVAL-TEST",
        artifact_records=records,
        budgets=(40, 120),
        excluded_artifact_ids=("COMP-0003",),
        l0_dir=tmp_path / "docs" / "memory" / "l0",
        l1_dir=tmp_path / "docs" / "memory" / "l1",
        docs_root=tmp_path / "docs",
    )

    assert report.selection_effect == "none"
    assert report.excluded_artifact_ids == ("COMP-0003",)
    assert report.inventory.artifact_count == 3
    assert report.connected_target_count == 3
    assert report.isolated_target_ids == ()
    assert report.recommendation == (
        "propose_separate_compact_representation_contract"
    )

    target = next(
        item
        for item in report.target_evaluations
        if item.target_id == "COMP-0002"
    )
    low_budget = {
        result.scenario: result
        for result in target.results
        if result.token_budget == 40
    }
    assert low_budget["whole_artifact_baseline"].included_artifact_ids == (
        "SYNCOMP-0001",
    )
    assert (
        low_budget["distance_aware_existing_compact"].included_artifact_ids
        == ("SYNCOMP-0001",)
    )
    assert low_budget[
        "distance_aware_metadata_lower_bound"
    ].included_artifact_ids == (
        "SYNCOMP-0001",
        "COMP-0001",
    )


def test_existing_semantic_distance_two_can_improve_packing(tmp_path: Path):
    comparisons = tmp_path / "docs" / "comparisons"

    write(
        comparisons / "COMP-0001-root.md",
        "# Root\n\n" + metadata("COMP-0001", "Root") + "\n\nroot text",
    )
    write(
        comparisons / "syntheses" / "SYNCOMP-0001-root.md",
        "# Synthesis\n\n"
        + metadata(
            "SYNCOMP-0001",
            "Root Synthesis",
            "- source_comparison: `docs/comparisons/COMP-0001-root.md`\n",
        )
        + "\n## Synthesis\n\nbrief\n"
        + "\n## Detail\n\n"
        + " ".join(f"detail{i}" for i in range(80)),
    )
    write(
        comparisons / "COMP-0002-reask.md",
        "# Reask\n\n"
        + metadata(
            "COMP-0002",
            "Reask",
            (
                "- source_synthesis: `docs/comparisons/syntheses/"
                "SYNCOMP-0001-root.md`\n"
            ),
        )
        + "\nsmall target",
    )
    write(
        comparisons / "syntheses" / "SYNCOMP-0002-target.md",
        "# Target Synthesis\n\n"
        + metadata(
            "SYNCOMP-0002",
            "Target Synthesis",
            "- source_comparison: `docs/comparisons/COMP-0002-reask.md`\n",
        )
        + "\n## Synthesis\n\ntarget summary\n",
    )

    records = discover_artifacts(comparisons)
    report = evaluate_compact_graph_representations(
        evaluation_id="EVAL-SEMANTIC",
        artifact_records=records,
        budgets=(60,),
        l0_dir=tmp_path / "missing-l0",
        l1_dir=tmp_path / "missing-l1",
        docs_root=tmp_path / "docs",
    )

    target = next(
        item
        for item in report.target_evaluations
        if item.target_id == "SYNCOMP-0002"
    )
    results = {result.scenario: result for result in target.results}

    assert results["whole_artifact_baseline"].included_artifact_ids == (
        "COMP-0002",
    )
    assert results[
        "distance_aware_existing_compact"
    ].included_artifact_ids == (
        "COMP-0002",
        "SYNCOMP-0001",
    )


def test_report_is_deterministic_json_ready_and_marks_boundaries(tmp_path: Path):
    comparisons = tmp_path / "docs" / "comparisons"
    write(
        comparisons / "COMP-0001-only.md",
        "# Only\n\n" + metadata("COMP-0001", "Only"),
    )

    records = discover_artifacts(comparisons)
    first = evaluate_compact_graph_representations(
        evaluation_id="EVAL-DETERMINISTIC",
        artifact_records=records,
        budgets=(500,),
        docs_root=tmp_path / "docs",
    )
    second = evaluate_compact_graph_representations(
        evaluation_id="EVAL-DETERMINISTIC",
        artifact_records=records,
        budgets=(500,),
        docs_root=tmp_path / "docs",
    )

    assert first.to_dict() == second.to_dict()
    assert json.dumps(first.to_dict(), sort_keys=True)
    assert first.isolated_target_ids == ("COMP-0001",)

    markdown = format_compact_graph_representation_report(first)
    assert "selection_effect: `none`" in markdown
    assert "semantically insufficient" in markdown
    assert "does not modify ContextPackManifest.items" in markdown


def test_whitespace_estimator_matches_graph_neighborhood_semantics():
    assert estimate_text_tokens("") == 1
    assert estimate_text_tokens("one two three") == 3
