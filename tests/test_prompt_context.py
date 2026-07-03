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
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None: manifest,
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
        max_warning_admissions=None,
    ):
        assert task == "Prepare admitted context."
        assert records == ("record",)
        assert token_budget == 8000
        assert model_target == "gpt-5"
        assert l1_scope == "ai-lab-memory"
        assert require_admission is True
        assert task_label == "prepare-admitted-context"
        assert full_prompt_hash == "c" * 64
        assert max_warning_admissions == 1
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
        max_warning_admissions=1,
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


def test_resolve_provider_warning_admission_cap_defaults_to_one_when_required():
    from ai_lab.documentation.prompt_context import resolve_provider_warning_admission_cap

    assert resolve_provider_warning_admission_cap(
        require_admission=True,
        max_warning_admissions=None,
    ) == 1


def test_resolve_provider_warning_admission_cap_preserves_explicit_values():
    from ai_lab.documentation.prompt_context import resolve_provider_warning_admission_cap

    assert resolve_provider_warning_admission_cap(
        require_admission=True,
        max_warning_admissions=0,
    ) == 0
    assert resolve_provider_warning_admission_cap(
        require_admission=True,
        max_warning_admissions=2,
    ) == 2


def test_resolve_provider_warning_admission_cap_no_default_without_required_admission():
    from ai_lab.documentation.prompt_context import resolve_provider_warning_admission_cap

    assert resolve_provider_warning_admission_cap(
        require_admission=False,
        max_warning_admissions=None,
    ) is None


def test_provider_latest_context_policy_records_provider_default():
    from ai_lab.documentation.prompt_context import provider_latest_context_policy

    assert provider_latest_context_policy(
        require_admission=True,
        max_warning_admissions=None,
    ) == {
        "context_policy": "latest_context",
        "require_admission": True,
        "max_warning_admissions": 1,
        "max_warning_admissions_source": "provider_default",
    }


def test_provider_latest_context_policy_records_explicit_zero():
    from ai_lab.documentation.prompt_context import provider_latest_context_policy

    assert provider_latest_context_policy(
        require_admission=True,
        max_warning_admissions=0,
    ) == {
        "context_policy": "latest_context",
        "require_admission": True,
        "max_warning_admissions": 0,
        "max_warning_admissions_source": "explicit",
    }


def test_format_provider_latest_context_policy_returns_stable_json():
    import json

    from ai_lab.documentation.prompt_context import format_provider_latest_context_policy

    data = json.loads(
        format_provider_latest_context_policy(
            require_admission=False,
            max_warning_admissions=None,
        )
    )

    assert data == {
        "context_policy": "latest_context",
        "require_admission": False,
        "max_warning_admissions": None,
        "max_warning_admissions_source": "unset",
    }


def test_provider_latest_context_metadata_formats_comparison_values():
    from ai_lab.documentation.prompt_context import provider_latest_context_metadata

    assert provider_latest_context_metadata(
        require_admission=True,
        max_warning_admissions=None,
    ) == {
        "context_policy": "latest_context",
        "context_require_admission": "true",
        "context_max_warning_admissions": "1",
        "context_max_warning_admissions_source": "provider_default",
    }



def test_format_provider_context_budget_preview_percentages_only():
    from ai_lab.documentation.prompt_context import (
        format_provider_context_budget_preview,
    )

    output = format_provider_context_budget_preview()

    assert "Context budget preview:" in output
    assert "- System: 15%" in output
    assert "- Answer: 10%" in output
    assert "- Context: 75%" in output
    assert "  - Explicit: 40%" in output
    assert "  - Dependencies: 45%" in output
    assert "  - L1: 10%" in output
    assert "  - L0: 5%" in output
    assert "->" not in output


def test_format_provider_context_budget_preview_with_context_window():
    from ai_lab.documentation.prompt_context import (
        format_provider_context_budget_preview,
    )

    output = format_provider_context_budget_preview(context_window=8000)

    assert "Context budget preview (context window: 8000):" in output
    assert "- System: 15% -> 1200" in output
    assert "- Answer: 10% -> 800" in output
    assert "- Context: 75% -> 6000" in output
    assert "  - Explicit: 40% -> 2400" in output
    assert "  - Dependencies: 45% -> 2700" in output
    assert "  - L1: 10% -> 600" in output
    assert "  - L0: 5% -> 300" in output


def test_provider_context_budget_preview_requires_positive_window():
    import pytest

    from ai_lab.documentation.prompt_context import provider_context_budget_preview

    with pytest.raises(ValueError, match="context_window must be positive"):
        provider_context_budget_preview(context_window=0)



def test_format_provider_context_summary_json_is_stable_and_parseable():
    import json

    from ai_lab.documentation.prompt_context import (
        format_provider_context_summary_json,
    )

    output = format_provider_context_summary_json(
        require_admission=True,
        max_warning_admissions=None,
        context_window=8000,
    )

    data = json.loads(output)

    assert data["schema_version"] == "v1"
    assert data["latest_context_policy"] == {
        "context_policy": "latest_context",
        "require_admission": True,
        "max_warning_admissions": 1,
        "max_warning_admissions_source": "provider_default",
    }
    assert data["context_budget_preview"]["system"] == {
        "percentage": 15,
        "tokens": 1200,
    }
    assert data["context_budget_preview"]["answer"] == {
        "percentage": 10,
        "tokens": 800,
    }
    assert data["context_budget_preview"]["context"]["percentage"] == 75
    assert data["context_budget_preview"]["context"]["tokens"] == 6000
    assert data["context_budget_preview"]["context"]["children"]["explicit"] == {
        "percentage": 40,
        "tokens": 2400,
    }
    assert data["context_budget_preview"]["context"]["children"][
        "dependencies"
    ] == {
        "percentage": 45,
        "tokens": 2700,
    }
    assert data["context_budget_preview"]["context"]["children"]["l1"] == {
        "percentage": 10,
        "tokens": 600,
    }
    assert data["context_budget_preview"]["context"]["children"]["l0"] == {
        "percentage": 5,
        "tokens": 300,
    }
    assert output == format_provider_context_summary_json(
        require_admission=True,
        max_warning_admissions=None,
        context_window=8000,
    )


def test_provider_context_summary_json_can_report_explicit_l0_inclusion(tmp_path):
    import json

    from ai_lab.documentation.prompt_context import format_provider_context_summary_json

    chunk_id = "chunk-a"
    (tmp_path / f"{chunk_id}.json").write_text(
        json.dumps(
            {
                "chunk_reference": {"chunk_id": chunk_id},
                "citation": "3ac9f2b1d0af@a1c2d3e|b:100-200",
                "l0_summary": "short summary",
                "keyphrases": ["citation", "span", "validation"],
            }
        ),
        encoding="utf-8",
    )

    data = json.loads(
        format_provider_context_summary_json(
            require_admission=True,
            max_warning_admissions=None,
            context_window=100,
            include_l0=(chunk_id,),
            l0_store=tmp_path,
        )
    )

    assert data["l0_candidates"] == [
        {
            "cid": chunk_id,
            "citation": "3ac9f2b1d0af@a1c2d3e|b:100-200",
            "inclusion_reason": "explicit",
            "token_cost": 5,
        }
    ]
    assert data["l0_included"] == data["l0_candidates"]
    assert data["l0_dropped"] == []


def test_provider_context_summary_json_dedupes_l0_and_reports_missing_or_over_budget(
    tmp_path,
):
    import json

    from ai_lab.documentation.prompt_context import format_provider_context_summary_json

    chunk_id = "chunk-large"
    (tmp_path / f"{chunk_id}.json").write_text(
        json.dumps(
            {
                "chunk_reference": {"chunk_id": chunk_id},
                "l0_summary": "one two three four five six seven eight nine ten",
                "keyphrases": ["large", "budget", "drop"],
            }
        ),
        encoding="utf-8",
    )

    data = json.loads(
        format_provider_context_summary_json(
            require_admission=False,
            max_warning_admissions=None,
            context_window=100,
            include_l0=(chunk_id, chunk_id, "missing-chunk"),
            l0_store=tmp_path,
        )
    )

    assert len(data["l0_candidates"]) == 1
    assert data["l0_included"] == []
    assert data["l0_dropped"] == [
        {
            "cid": "missing-chunk",
            "dropped_reason": "not_found",
            "token_cost": 0,
        },
        {
            "cid": chunk_id,
            "dropped_reason": "over_budget",
            "token_cost": 13,
        },
    ]
