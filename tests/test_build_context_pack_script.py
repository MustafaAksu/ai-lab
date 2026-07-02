import json

from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest


def test_build_context_pack_writes_output_and_manifest(tmp_path, monkeypatch):
    from scripts import build_context_pack

    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction.",
        relevance_score=0.9,
        token_estimate=100,
        source_path="docs/abstractions/ABS-0003.md",
    )

    manifest = ContextPackManifest(
        task="Prepare context.",
        assembly_policy="latest_context",
        items=(item,),
        token_budget=8000,
        model_target="gpt-5",
    )

    markdown_path = tmp_path / "context.md"
    manifest_path = tmp_path / "context.json"

    def fake_discover_artifacts(comparison_dir, abstraction_dir):
        return ("record",)

    def fake_build_latest_context_manifest(
        task,
        records,
        token_budget=None,
        model_target=None,
        pipeline_run_id=None,
        l1_scope=None,
        require_admission=False,
    ):
        assert task == "Prepare context."
        assert records == ("record",)
        assert token_budget == 8000
        assert model_target == "gpt-5"
        assert require_admission is False
        return manifest

    monkeypatch.setattr(
        build_context_pack,
        "discover_artifacts",
        fake_discover_artifacts,
    )
    monkeypatch.setattr(
        build_context_pack,
        "build_latest_context_manifest",
        fake_build_latest_context_manifest,
    )
    monkeypatch.setattr(
        build_context_pack,
        "render_context_pack_markdown",
        lambda manifest: "# Rendered Context Pack\n",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_context_pack.py",
            "Prepare context.",
            "--token-budget",
            "8000",
            "--model-target",
            "gpt-5",
            "--format",
            "markdown",
            "--output",
            str(markdown_path),
            "--manifest-output",
            str(manifest_path),
        ],
    )

    assert build_context_pack.main() == 0

    assert markdown_path.read_text(encoding="utf-8") == "# Rendered Context Pack\n"

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest_data["task"] == "Prepare context."
    assert manifest_data["token_budget"] == 8000
    assert manifest_data["model_target"] == "gpt-5"
    assert manifest_data["items"][0]["item_id"] == "ABS-0003"


def test_build_context_pack_passes_require_admission(tmp_path, monkeypatch):
    from scripts import build_context_pack

    item = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-ADMITTED",
        reason="Admitted L1.",
        relevance_score=0.92,
        token_estimate=100,
        admission_verdict_id="CADM-1",
        admission_decision="admit",
        freshness_state="fresh",
        warrant_state="supported",
    )

    manifest = ContextPackManifest(
        task="Prepare admitted context.",
        assembly_policy="latest_context",
        items=(item,),
        token_budget=8000,
        model_target="gpt-5",
    )

    monkeypatch.setattr(
        build_context_pack,
        "discover_artifacts",
        lambda comparison_dir, abstraction_dir: ("record",),
    )

    def fake_build_latest_context_manifest(
        task,
        records,
        token_budget=None,
        model_target=None,
        pipeline_run_id=None,
        l1_scope=None,
        require_admission=False,
    ):
        assert task == "Prepare admitted context."
        assert records == ("record",)
        assert token_budget == 8000
        assert model_target == "gpt-5"
        assert l1_scope == "ai-lab-memory"
        assert require_admission is True
        return manifest

    monkeypatch.setattr(
        build_context_pack,
        "build_latest_context_manifest",
        fake_build_latest_context_manifest,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_context_pack.py",
            "Prepare admitted context.",
            "--scope",
            "ai-lab-memory",
            "--require-admission",
            "--token-budget",
            "8000",
            "--model-target",
            "gpt-5",
        ],
    )

    assert build_context_pack.main() == 0
