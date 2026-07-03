from pathlib import Path
import pytest

from scripts.compare_providers import (
    auto_comparison_path,
    build_markdown_artifact,
    next_comparison_id,
    slugify,
)


def test_build_markdown_artifact_records_metadata_models_and_responses():
    artifact = build_markdown_artifact(
        prompt="Explain provenance.",
        responses={
            "OpenAI": {
                "model": "gpt-5",
                "response": "OpenAI answer.",
            },
            "Claude": {
                "model": "claude-sonnet-4-5",
                "response": "Claude answer.",
            },
        },
        created_at="2026-06-30T00:00:00Z",
        command="scripts/compare_providers.py Explain provenance.",
        comparison_id="COMP-0003",
        title="Provenance",
    )

    assert "# COMP-0003: Provider Comparison — Provenance" in artifact
    assert "- comparison_id: `COMP-0003`" in artifact
    assert "- title: `Provenance`" in artifact
    assert "- created_at: `2026-06-30T00:00:00Z`" in artifact
    assert "- providers: `OpenAI, Claude`" in artifact
    assert "- OpenAI: `gpt-5`" in artifact
    assert "- Claude: `claude-sonnet-4-5`" in artifact
    assert "## Prompt" in artifact
    assert "Explain provenance." in artifact
    assert "## OpenAI Response" in artifact
    assert "OpenAI answer." in artifact
    assert "## Claude Response" in artifact
    assert "Claude answer." in artifact


def test_build_markdown_artifact_uses_longer_fence_when_response_contains_backticks():
    artifact = build_markdown_artifact(
        prompt="Return code.",
        responses={
            "OpenAI": {
                "model": "gpt-5",
                "response": "```python\nprint('hello')\n```",
            },
        },
        created_at="2026-06-30T00:00:00Z",
        command="scripts/compare_providers.py Return code.",
    )

    assert "````" in artifact


def test_slugify_creates_filesystem_safe_slug():
    assert slugify("Model Metadata & Provenance!") == "model-metadata-provenance"


def test_next_comparison_id_uses_existing_files(tmp_path: Path):
    (tmp_path / "COMP-0001-first.md").write_text("", encoding="utf-8")
    (tmp_path / "COMP-0007-seventh.md").write_text("", encoding="utf-8")
    (tmp_path / "NOT-A-COMP.md").write_text("", encoding="utf-8")

    assert next_comparison_id(tmp_path) == "COMP-0008"


def test_auto_comparison_path_uses_next_id_and_slug(tmp_path: Path):
    (tmp_path / "COMP-0002-existing.md").write_text("", encoding="utf-8")

    path = auto_comparison_path("Edge Immutability", tmp_path)

    assert path == tmp_path / "COMP-0003-edge-immutability.md"

def test_build_markdown_artifact_records_extra_metadata():
    artifact = build_markdown_artifact(
        prompt="Prompt",
        responses={
            "OpenAI": {
                "model": "gpt-5",
                "response": "Answer",
            }
        },
        created_at="2026-06-30T00:00:00Z",
        command="command",
        comparison_id="COMP-0004",
        title="Re-Ask",
        extra_metadata={
            "source_synthesis": "docs/comparisons/syntheses/SYNCOMP-0001-example.md",
        },
    )

    assert "- source_synthesis: `docs/comparisons/syntheses/SYNCOMP-0001-example.md`" in artifact



def test_main_latest_context_print_prompt_uses_generated_context(monkeypatch, capsys):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from scripts import compare_providers

    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction.",
        relevance_score=0.9,
        token_estimate=100,
    )
    manifest = ContextPackManifest(
        task="Compare next step.",
        assembly_policy="latest_context",
        items=(item,),
        token_budget=8000,
        model_target="gpt-5",
    )

    def fake_build_latest_context_pack_manifest(task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None):
        assert task == "Compare next step."
        assert token_budget == 8000
        assert model_target == "gpt-5"
        return manifest

    monkeypatch.setattr(
        compare_providers,
        "build_latest_context_pack_manifest",
        fake_build_latest_context_pack_manifest,
    )
    monkeypatch.setattr(
        compare_providers,
        "render_context_pack_markdown",
        lambda manifest: "# Generated Context Pack",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            "Compare",
            "next",
            "step.",
            "--latest-context",
            "--token-budget",
            "8000",
            "--model-target",
            "gpt-5",
            "--print-prompt",
        ],
    )

    assert compare_providers.main() == 0

    output = capsys.readouterr().out

    assert "BEGIN CONTEXT PACK" in output
    assert "# Generated Context Pack" in output
    assert "END CONTEXT PACK" in output
    assert output.rstrip().endswith("Compare next step.")


def test_main_context_comparison_saves_raw_prompt_and_sibling_context_manifest(
    tmp_path,
    monkeypatch,
):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from scripts import compare_providers

    class FakeProvider:
        def __init__(self, name):
            self.name = name
            self.model = f"{name.lower()}-model"
            self.prompts = []

        def ask(self, prompt):
            self.prompts.append(prompt)
            assert "BEGIN CONTEXT PACK" in prompt
            assert "# Generated Context Pack" in prompt
            return f"{self.name} answer"

    fake_openai = FakeProvider("OpenAI")
    fake_claude = FakeProvider("Claude")

    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction.",
        relevance_score=0.9,
        token_estimate=100,
    )
    manifest = ContextPackManifest(
        task="Compare next step.",
        assembly_policy="latest_context",
        items=(item,),
    )

    monkeypatch.setattr(
        compare_providers,
        "OpenAIProvider",
        lambda: fake_openai,
    )
    monkeypatch.setattr(
        compare_providers,
        "ClaudeProvider",
        lambda: fake_claude,
    )
    monkeypatch.setattr(
        compare_providers,
        "build_latest_context_pack_manifest",
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None: manifest,
    )
    monkeypatch.setattr(
        compare_providers,
        "render_context_pack_markdown",
        lambda manifest: "# Generated Context Pack",
    )

    save_path = tmp_path / "COMP-0001-context-test.md"
    manifest_path = tmp_path / "COMP-0001-context-test.context.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            "Compare",
            "next",
            "step.",
            "--latest-context",
            "--require-admission",
            "--save",
            str(save_path),
            "--title",
            "Context Test",
        ],
    )

    assert compare_providers.main() == 0

    artifact = save_path.read_text(encoding="utf-8")
    manifest_json = manifest_path.read_text(encoding="utf-8")

    assert "## Prompt" in artifact
    assert "Compare next step." in artifact
    assert "BEGIN CONTEXT PACK" not in artifact
    assert "# Generated Context Pack" not in artifact
    assert "- context_policy: `latest_context`" in artifact
    assert "- context_require_admission: `true`" in artifact
    assert "- context_max_warning_admissions: `1`" in artifact
    assert "- context_max_warning_admissions_source: `provider_default`" in artifact
    assert f"- context_manifest: `{manifest_path}`" in artifact

    assert "\"manifest_id\"" in manifest_json
    assert "\"item_id\": \"ABS-0003\"" in manifest_json
    assert "\"task_label\": \"compare-next-step\"" in manifest_json
    assert "\"full_prompt_hash\": \"" in manifest_json


def test_main_latest_context_uses_short_task_label_but_keeps_full_comparison_prompt(
    monkeypatch,
    capsys,
):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from scripts import compare_providers

    long_prompt = "x" * 600

    item = ContextPackItem(
        item_type="abstraction",
        item_id="ABS-0003",
        reason="Latest abstraction.",
        relevance_score=0.9,
        token_estimate=100,
    )
    manifest = ContextPackManifest(
        task=("x" * 497) + "...",
        assembly_policy="latest_context",
        items=(item,),
    )

    def fake_build_latest_context_pack_manifest(
        task,
        token_budget=None,
        model_target=None,
        scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None, max_warning_admissions=None
    ):
        assert len(task) == 500
        assert task.endswith("...")
        assert require_admission is False
        assert task_label == "x" * 80
        assert full_prompt_hash is None
        return manifest

    monkeypatch.setattr(
        compare_providers,
        "build_latest_context_pack_manifest",
        fake_build_latest_context_pack_manifest,
    )
    monkeypatch.setattr(
        compare_providers,
        "render_context_pack_markdown",
        lambda manifest: "# Generated Context Pack",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            long_prompt,
            "--latest-context",
            "--print-prompt",
        ],
    )

    assert compare_providers.main() == 0

    output = capsys.readouterr().out
    assert long_prompt in output
    assert "# Generated Context Pack" in output


def test_main_latest_context_passes_require_admission(monkeypatch, capsys):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from scripts import compare_providers

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
        task="Compare admitted step.",
        assembly_policy="latest_context",
        items=(item,),
    )

    def fake_build_latest_context_pack_manifest(
        task,
        token_budget=None,
        model_target=None,
        scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None, max_warning_admissions=None
    ):
        assert task == "Compare admitted step."
        assert token_budget == 8000
        assert model_target == "gpt-5"
        assert scope == "ai-lab-memory"
        assert require_admission is True
        assert max_warning_admissions == 1
        assert task_label == "compare-admitted-step"
        assert full_prompt_hash is None
        return manifest

    monkeypatch.setattr(
        compare_providers,
        "build_latest_context_pack_manifest",
        fake_build_latest_context_pack_manifest,
    )
    monkeypatch.setattr(
        compare_providers,
        "render_context_pack_markdown",
        lambda manifest: "# Admitted Context Pack",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            "Compare",
            "admitted",
            "step.",
            "--latest-context",
            "--scope",
            "ai-lab-memory",
            "--require-admission",
            "--token-budget",
            "8000",
            "--model-target",
            "gpt-5",
            "--print-prompt",
        ],
    )

    assert compare_providers.main() == 0

    output = capsys.readouterr().out
    assert "# Admitted Context Pack" in output
    assert "Compare admitted step." in output


def test_main_latest_context_preserves_explicit_zero_warning_cap(
    monkeypatch,
    capsys,
):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from scripts import compare_providers

    item = ContextPackItem(
        item_type="episode_l1",
        item_id="L1-ADMITTED",
        reason="Admitted L1.",
        relevance_score=0.92,
    )
    manifest = ContextPackManifest(
        task="Compare strict step.",
        assembly_policy="latest_context",
        items=(item,),
    )

    def fake_build_latest_context_pack_manifest(
        task,
        token_budget=None,
        model_target=None,
        scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None,
        max_warning_admissions=None,
    ):
        assert require_admission is True
        assert max_warning_admissions == 0
        return manifest

    monkeypatch.setattr(
        compare_providers,
        "build_latest_context_pack_manifest",
        fake_build_latest_context_pack_manifest,
    )
    monkeypatch.setattr(
        compare_providers,
        "render_context_pack_markdown",
        lambda manifest: "# Strict Context Pack",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            "Compare",
            "strict",
            "step.",
            "--latest-context",
            "--require-admission",
            "--max-warning-admissions",
            "0",
            "--print-prompt",
        ],
    )

    assert compare_providers.main() == 0

    output = capsys.readouterr().out
    assert "# Strict Context Pack" in output


def test_main_help_documents_provider_warning_cap_default(monkeypatch, capsys):
    from scripts import compare_providers

    monkeypatch.setattr("sys.argv", ["compare_providers.py", "--help"])

    with pytest.raises(SystemExit) as exc_info:
        compare_providers.main()

    assert exc_info.value.code == 0

    output = " ".join(capsys.readouterr().out.split())
    output = output.replace("--require- admission", "--require-admission")
    assert "Defaults to 1 when --require-admission is enabled" in output
    assert "Explicit values, including 0, are preserved" in output


def test_main_print_context_policy_shows_explicit_zero(monkeypatch, capsys):
    from scripts import compare_providers

    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            "Compare",
            "strict",
            "step.",
            "--latest-context",
            "--require-admission",
            "--max-warning-admissions",
            "0",
            "--print-context-policy",
        ],
    )

    assert compare_providers.main() == 0

    output = capsys.readouterr().out
    assert '"context_policy": "latest_context"' in output
    assert '"require_admission": true' in output
    assert '"max_warning_admissions": 0' in output
    assert '"max_warning_admissions_source": "explicit"' in output


def test_main_print_context_policy_requires_latest_context(monkeypatch):
    from scripts import compare_providers

    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            "Compare",
            "next",
            "step.",
            "--print-context-policy",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        compare_providers.main()

    assert exc_info.value.code == 2


def test_main_context_comparison_records_explicit_zero_policy_metadata(
    tmp_path,
    monkeypatch,
):
    from ai_lab.documentation.context_pack import ContextPackItem, ContextPackManifest
    from scripts import compare_providers

    class FakeProvider:
        def __init__(self, name):
            self.name = name
            self.model = f"{name.lower()}-model"

        def ask(self, prompt):
            return f"{self.name} answer"

    manifest = ContextPackManifest(
        task="Compare strict step.",
        assembly_policy="latest_context",
        items=(
            ContextPackItem(
                item_type="episode_l1",
                item_id="L1-ADMITTED",
                reason="Admitted L1.",
                relevance_score=0.92,
            ),
        ),
    )

    monkeypatch.setattr(compare_providers, "OpenAIProvider", lambda: FakeProvider("OpenAI"))
    monkeypatch.setattr(compare_providers, "ClaudeProvider", lambda: FakeProvider("Claude"))
    monkeypatch.setattr(
        compare_providers,
        "build_latest_context_pack_manifest",
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None: manifest,
    )
    monkeypatch.setattr(
        compare_providers,
        "render_context_pack_markdown",
        lambda manifest: "# Generated Context Pack",
    )

    save_path = tmp_path / "COMP-0002-strict-context-test.md"

    monkeypatch.setattr(
        "sys.argv",
        [
            "compare_providers.py",
            "Compare",
            "strict",
            "step.",
            "--latest-context",
            "--require-admission",
            "--max-warning-admissions",
            "0",
            "--save",
            str(save_path),
        ],
    )

    assert compare_providers.main() == 0

    artifact = save_path.read_text(encoding="utf-8")

    assert "- context_policy: `latest_context`" in artifact
    assert "- context_require_admission: `true`" in artifact
    assert "- context_max_warning_admissions: `0`" in artifact
    assert "- context_max_warning_admissions_source: `explicit`" in artifact
