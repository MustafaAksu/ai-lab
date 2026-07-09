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
        task_label=None,
        full_prompt_hash=None, max_warning_admissions=None
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
        task_label=None,
        full_prompt_hash=None, max_warning_admissions=None
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


def test_main_passes_explicit_l0_arguments(monkeypatch, tmp_path, capsys):
    import scripts.build_context_pack as script
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest

    captured = {}

    def fake_discover_artifacts(comparison_dir, abstraction_dir):
        return ()

    def fake_build_latest_context_manifest(**kwargs):
        captured.update(kwargs)
        item = ContextPackItem(
            item_type="l0_summary",
            item_id="chunk-a",
            reason="Explicit L0.",
            relevance_score=0.95,
            source_path=str(tmp_path / "chunk-a.json"),
            citation="3ac9f2b1d0af@a1c2d3e|b:100-200",
        )
        return ContextPackManifest(
            task=kwargs["task"],
            assembly_policy="latest_context",
            items=(item,),
        )

    monkeypatch.setattr(script, "discover_artifacts", fake_discover_artifacts)
    monkeypatch.setattr(script, "build_latest_context_manifest", fake_build_latest_context_manifest)
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_context_pack.py",
            "Prepare context.",
            "--include-l0",
            "chunk-a",
            "--l0-store",
            str(tmp_path),
        ],
    )

    assert script.main() == 0
    capsys.readouterr()

    assert captured["include_l0"] == ("chunk-a",)
    assert captured["l0_store"] == tmp_path

def test_main_passes_l0_discovery_advisor_diagnostics_arguments(monkeypatch, tmp_path, capsys):
    import scripts.build_context_pack as script

    captured = {}

    def fake_discover_artifacts(comparison_dir, abstraction_dir):
        return ()

    def fake_build_latest_context_manifest(**kwargs):
        captured.update(kwargs)
        item = ContextPackItem(
            item_type="abstraction",
            item_id="ABS-0003",
            reason="Latest abstraction.",
            relevance_score=0.9,
            token_estimate=100,
        )
        return ContextPackManifest(
            task=kwargs["task"],
            assembly_policy="latest_context",
            items=(item,),
            diagnostics={
                "l0_discovery_advisor": {
                    "selection_effect": "none",
                    "suggestions": [],
                }
            },
        )

    monkeypatch.setattr(script, "discover_artifacts", fake_discover_artifacts)
    monkeypatch.setattr(script, "build_latest_context_manifest", fake_build_latest_context_manifest)
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_context_pack.py",
            "Prepare context.",
            "--include-l0-discovery-advisor-diagnostics",
            "--l0-discovery-advisor-max-suggestions",
            "3",
            "--l0-store",
            str(tmp_path),
        ],
    )

    assert script.main() == 0
    data = json.loads(capsys.readouterr().out)

    assert captured["include_l0_discovery_advisor_diagnostics"] is True
    assert captured["l0_discovery_advisor_max_suggestions"] == 3
    assert data["diagnostics"]["l0_discovery_advisor"]["selection_effect"] == "none"


def test_main_passes_auto_include_l0_discovery_arguments(monkeypatch, tmp_path, capsys):
    import scripts.build_context_pack as script
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest

    captured = {}

    def fake_discover_artifacts(comparison_dir, abstraction_dir):
        return ()

    def fake_build_latest_context_manifest(**kwargs):
        captured.update(kwargs)
        item = ContextPackItem(
            item_type="abstraction",
            item_id="ABS-0003",
            reason="Latest abstraction.",
            relevance_score=0.9,
            token_estimate=100,
        )
        return ContextPackManifest(
            task=kwargs["task"],
            assembly_policy="latest_context",
            items=(item,),
        )

    monkeypatch.setattr(script, "discover_artifacts", fake_discover_artifacts)
    monkeypatch.setattr(script, "build_latest_context_manifest", fake_build_latest_context_manifest)
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_context_pack.py",
            "Prepare context.",
            "--auto-include-l0-discovery",
            "--auto-include-l0-discovery-max-items",
            "2",
            "--l0-store",
            str(tmp_path),
        ],
    )

    assert script.main() == 0
    capsys.readouterr()

    assert captured["auto_include_l0_discovery"] is True
    assert captured["auto_include_l0_discovery_max_items"] == 2
    assert captured["l0_store"] == tmp_path
