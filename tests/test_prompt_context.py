from pathlib import Path

from ai_lab.documentation.prompt_context import build_prompt, read_context_pack


def test_build_prompt_without_context_returns_prompt():
    assert build_prompt("Do the task.") == "Do the task."


def test_build_prompt_with_context_pack_wraps_context():
    prompt = build_prompt(
        prompt="Implement the next step.",
        context_pack="# Context Pack\n\nImportant source.",
    )

    assert "BEGIN CONTEXT PACK" in prompt
    assert "# Context Pack" in prompt
    assert "END CONTEXT PACK" in prompt
    assert "User task:" in prompt
    assert prompt.endswith("Implement the next step.")


def test_read_context_pack_reads_markdown(tmp_path):
    path = tmp_path / "context.md"
    path.write_text("# Context Pack", encoding="utf-8")

    assert read_context_pack(Path(path)) == "# Context Pack"


def test_build_latest_context_pack_text_uses_manifest_helper(monkeypatch):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from ai_lab.documentation import prompt_context

    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction.",
        relevance_score=0.9,
        token_estimate=100,
    )
    manifest = ContextPackManifest(
        task="Prepare context.",
        assembly_policy="latest_context",
        items=(item,),
    )

    monkeypatch.setattr(
        prompt_context,
        "build_latest_context_pack_manifest",
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None: manifest,
    )
    monkeypatch.setattr(
        prompt_context,
        "render_context_pack_markdown",
        lambda manifest: "# Rendered Context",
    )

    assert (
        prompt_context.build_latest_context_pack_text(
            task="Prepare context.",
            token_budget=8000,
            model_target="gpt-5",
        )
        == "# Rendered Context"
    )


def test_context_task_label_normalizes_whitespace():
    from ai_lab.documentation.prompt_context import context_task_label

    assert context_task_label("  Compare   next\n\nstep.  ") == "Compare next step."


def test_context_task_label_truncates_long_prompt():
    from ai_lab.documentation.prompt_context import context_task_label

    label = context_task_label("x" * 100, max_length=20)

    assert len(label) == 20
    assert label.endswith("...")


def test_context_task_label_returns_fallback_for_empty_prompt():
    from ai_lab.documentation.prompt_context import context_task_label

    assert context_task_label("   \n\t  ") == "Untitled task"


def test_build_latest_context_pack_manifest_passes_require_admission(monkeypatch):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from ai_lab.documentation import prompt_context

    item = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-ADMITTED",
        reason="Admitted L1.",
        relevance_score=0.92,
        admission_verdict_id="CADM-1",
        admission_decision="admit",
        freshness_state="fresh",
        warrant_state="supported",
    )
    manifest = ContextPackManifest(
        task="Prepare admitted context.",
        assembly_policy="latest_context",
        items=(item,),
    )

    monkeypatch.setattr(prompt_context, "discover_artifacts", lambda **kwargs: ("record",))

    def fake_build_latest_context_manifest(
        task,
        records,
        token_budget=None,
        model_target=None,
        l1_scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None,
    ):
        assert task == "Prepare admitted context."
        assert records == ("record",)
        assert token_budget == 8000
        assert model_target == "gpt-5"
        assert l1_scope == "ai-lab-memory"
        assert require_admission is True
        assert task_label == "prepare-admitted-context"
        assert full_prompt_hash == "c" * 64
        return manifest

    monkeypatch.setattr(
        prompt_context,
        "build_latest_context_manifest",
        fake_build_latest_context_manifest,
    )

    result = prompt_context.build_latest_context_pack_manifest(
        task="Prepare admitted context.",
        token_budget=8000,
        model_target="gpt-5",
        scope="ai-lab-memory",
        require_admission=True,
        task_label="prepare-admitted-context",
        full_prompt_hash="c" * 64,
    )

    assert result is manifest


def test_context_task_slug_returns_kebab_case():
    from ai_lab.documentation.prompt_context import context_task_slug

    assert context_task_slug("  Compare NEXT step!!  ") == "compare-next-step"


def test_context_task_slug_truncates_safely():
    from ai_lab.documentation.prompt_context import context_task_slug

    slug = context_task_slug("Alpha Beta Gamma Delta", max_length=12)

    assert slug == "alpha-beta-g"
    assert len(slug) <= 12


def test_prompt_sha256_returns_lowercase_digest():
    from ai_lab.documentation.prompt_context import prompt_sha256

    digest = prompt_sha256("hello")

    assert digest == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
