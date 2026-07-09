from pathlib import Path
import pytest

from scripts.ask_provider import build_prompt, read_context_pack


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


def test_main_print_prompt_does_not_call_provider(tmp_path, monkeypatch, capsys):
    from scripts.ask_provider import main

    context_path = tmp_path / "context.md"
    context_path.write_text("# Context Pack\n\nImportant context.", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "the",
            "next",
            "step.",
            "--context-pack",
            str(context_path),
            "--print-prompt",
        ],
    )

    assert main() == 0

    output = capsys.readouterr().out

    assert "BEGIN CONTEXT PACK" in output
    assert "# Context Pack" in output
    assert "END CONTEXT PACK" in output
    assert "User task:" in output
    assert output.rstrip().endswith("Do the next step.")


def test_main_latest_context_print_prompt_uses_generated_context(monkeypatch, capsys):
    from scripts import ask_provider

    def fake_build_latest_context_pack_text(task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None):
        assert task == "Do the next step."
        assert token_budget == 8000
        assert model_target == "gpt-5"
        return "# Generated Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "the",
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

    assert ask_provider.main() == 0

    output = capsys.readouterr().out

    assert "BEGIN CONTEXT PACK" in output
    assert "# Generated Context Pack" in output
    assert "END CONTEXT PACK" in output
    assert output.rstrip().endswith("Do the next step.")


def test_main_latest_context_uses_short_task_label_but_keeps_full_prompt(monkeypatch, capsys):
    from scripts import ask_provider

    long_prompt = "x" * 600

    def fake_build_latest_context_pack_text(task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None):
        assert len(task) == 500
        assert task.endswith("...")
        return "# Generated Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            long_prompt,
            "--latest-context",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    assert long_prompt in output
    assert "# Generated Context Pack" in output


def test_main_latest_context_passes_require_admission(monkeypatch, capsys):
    from scripts import ask_provider

    def fake_build_latest_context_pack_text(
        task,
        token_budget=None,
        model_target=None,
        scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None, max_warning_admissions=None
    ):
        assert task == "Do the admitted step."
        assert token_budget == 8000
        assert model_target == "gpt-5"
        assert scope == "ai-lab-memory"
        assert require_admission is True
        assert max_warning_admissions == 1
        return "# Admitted Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "the",
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

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    assert "# Admitted Context Pack" in output
    assert "Do the admitted step." in output


def test_main_latest_context_preserves_explicit_zero_warning_cap(monkeypatch, capsys):
    from scripts import ask_provider

    def fake_build_latest_context_pack_text(
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
        return "# Strict Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "strict",
            "step.",
            "--latest-context",
            "--require-admission",
            "--max-warning-admissions",
            "0",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    assert "# Strict Context Pack" in output


def test_main_help_documents_provider_warning_cap_default(monkeypatch, capsys):
    from scripts import ask_provider

    monkeypatch.setattr("sys.argv", ["ask_provider.py", "--help"])

    with pytest.raises(SystemExit) as exc_info:
        ask_provider.main()

    assert exc_info.value.code == 0

    output = " ".join(capsys.readouterr().out.split())
    output = output.replace("--require- admission", "--require-admission")
    assert "Defaults to 1 when --require-admission is enabled" in output
    assert "Explicit values, including 0, are preserved" in output


def test_main_print_context_policy_shows_resolved_provider_default(monkeypatch, capsys):
    from scripts import ask_provider

    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "the",
            "next",
            "step.",
            "--latest-context",
            "--require-admission",
            "--print-context-policy",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    assert '"context_policy": "latest_context"' in output
    assert '"require_admission": true' in output
    assert '"max_warning_admissions": 1' in output
    assert '"max_warning_admissions_source": "provider_default"' in output


def test_main_print_context_policy_requires_latest_context(monkeypatch):
    from scripts import ask_provider

    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "the",
            "next",
            "step.",
            "--print-context-policy",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        ask_provider.main()

    assert exc_info.value.code == 2


def test_main_print_prompt_can_include_context_summary(monkeypatch, capsys):
    from scripts import ask_provider

    def fake_build_latest_context_pack_text(
        task,
        token_budget=None,
        model_target=None,
        scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None,
        max_warning_admissions=None,
    ):
        return "# Generated Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--require-admission",
            "--print-context-summary",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    assert "Resolved latest-context policy:" in output
    assert '"max_warning_admissions": 1' in output
    assert '"max_warning_admissions_source": "provider_default"' in output
    assert "Final prompt:" in output
    assert "BEGIN CONTEXT PACK" in output
    assert output.rstrip().endswith("Do summary step.")


def test_main_print_context_summary_requires_print_prompt(monkeypatch):
    from scripts import ask_provider

    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--print-context-summary",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        ask_provider.main()

    assert exc_info.value.code == 2



def test_main_print_prompt_context_summary_can_include_budget_window(monkeypatch, capsys):
    from scripts import ask_provider

    def fake_build_latest_context_pack_text(
        task,
        token_budget=None,
        model_target=None,
        scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None,
        max_warning_admissions=None,
    ):
        return "# Generated Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--print-context-summary",
            "--context-window",
            "8000",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    assert "Context budget preview (context window: 8000):" in output
    assert "- System: 15% -> 1200" in output
    assert "- Answer: 10% -> 800" in output
    assert "- Context: 75% -> 6000" in output
    assert "  - Explicit: 40% -> 2400" in output
    assert "  - Dependencies: 45% -> 2700" in output
    assert "  - L1: 10% -> 600" in output
    assert "  - L0: 5% -> 300" in output
    assert "Final prompt:" in output



def test_main_print_prompt_context_summary_can_emit_json(monkeypatch, capsys):
    import json

    from scripts import ask_provider

    def fake_build_latest_context_pack_text(
        task,
        token_budget=None,
        model_target=None,
        scope=None,
        require_admission=False,
        task_label=None,
        full_prompt_hash=None,
        max_warning_admissions=None,
    ):
        return "# Generated Context Pack"

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--require-admission",
            "--print-context-summary",
            "--summary-format",
            "json",
            "--context-window",
            "8000",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    output = capsys.readouterr().out
    summary_text, final_prompt = output.split("\n\nFinal prompt:\n", 1)
    data = json.loads(summary_text)

    assert data["schema_version"] == "v1"
    assert data["latest_context_policy"]["max_warning_admissions"] == 1
    assert data["latest_context_policy"][
        "max_warning_admissions_source"
    ] == "provider_default"
    assert data["context_budget_preview"]["system"]["tokens"] == 1200
    assert data["context_budget_preview"]["context"]["children"]["l0"][
        "tokens"
    ] == 300
    assert "BEGIN CONTEXT PACK" in final_prompt
    assert final_prompt.rstrip().endswith("Do summary step.")


def test_main_summary_format_json_requires_context_summary(monkeypatch):
    import pytest

    from scripts import ask_provider

    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--summary-format",
            "json",
            "--print-prompt",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        ask_provider.main()

    assert exc_info.value.code == 2


def test_main_print_prompt_context_summary_json_can_include_l0(
    tmp_path,
    monkeypatch,
    capsys,
):
    import json

    from scripts import ask_provider

    chunk_id = "chunk-a"
    (tmp_path / f"{chunk_id}.json").write_text(
        json.dumps(
                {
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
                    "l0_summary": "short summary",
                    "keyphrases": ["citation", "span", "validation"],
                    "entities": [],
                    "claims": [],
                    "risks": [],
                    "created_at": "2026-06-30T00:00:00+00:00",
                    "last_refreshed_at": "2026-06-30T00:00:00+00:00",
                }
            ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None, **kwargs: "# Generated Context Pack",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--print-context-summary",
            "--summary-format",
            "json",
            "--context-window",
            "100",
            "--include-l0",
            chunk_id,
            "--l0-store",
            str(tmp_path),
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    summary_text, final_prompt = capsys.readouterr().out.split("\n\nFinal prompt:\n", 1)
    data = json.loads(summary_text)

    assert data["l0_candidates"][0]["cid"] == chunk_id
    assert data["l0_included"][0]["cid"] == chunk_id
    assert data["l0_dropped"] == []
    assert "BEGIN CONTEXT PACK" in final_prompt



def test_main_include_l0_with_context_summary_requires_json(monkeypatch):
    import pytest
    import scripts.ask_provider as script

    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "hello",
            "--latest-context",
            "--print-prompt",
            "--print-context-summary",
            "--include-l0",
            "chunk-a",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        script.main()

    assert exc_info.value.code == 2


def test_main_print_prompt_context_summary_json_can_validate_l0_invariants(
    tmp_path,
    monkeypatch,
    capsys,
):
    import json

    from scripts import ask_provider

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

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None, **kwargs: "# Generated Context Pack",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--print-context-summary",
            "--summary-format",
            "json",
            "--validate-l0-invariants",
            "--include-l0",
            chunk_id,
            "--l0-store",
            str(tmp_path),
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    summary_text, final_prompt = capsys.readouterr().out.split("\n\nFinal prompt:\n", 1)
    data = json.loads(summary_text)

    assert data["validation"]["l0_invariants"] == {"version": "v1", "ok": True, "errors": []}
    assert "BEGIN CONTEXT PACK" in final_prompt


def test_main_print_prompt_context_summary_json_validation_can_fail_without_nonzero(
    monkeypatch,
    capsys,
):
    import json

    from scripts import ask_provider

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None, **kwargs: "# Generated Context Pack",
    )
    monkeypatch.setattr(
        ask_provider,
        "provider_context_summary_payload",
        lambda require_admission, max_warning_admissions, context_window=None, include_l0=(), l0_store=None: {
            "schema_version": "v1",
            "l0_candidates": {},
            "l0_included": [],
            "l0_dropped": [],
        },
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--print-context-summary",
            "--summary-format",
            "json",
            "--validate-l0-invariants",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    summary_text, _final_prompt = capsys.readouterr().out.split("\n\nFinal prompt:\n", 1)
    data = json.loads(summary_text)

    assert data["validation"]["l0_invariants"]["ok"] is False
    assert data["validation"]["l0_invariants"]["errors"][0] == {
        "code": "L0I_L0_CANDIDATES_NOT_LIST",
        "message": "l0_candidates must be a list",
        "path": "$.l0_candidates",
    }



def test_main_print_prompt_context_summary_json_validation_collects_all_errors(
    monkeypatch,
    capsys,
):
    import json

    from scripts import ask_provider

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None, **kwargs: "# Generated Context Pack",
    )
    monkeypatch.setattr(
        ask_provider,
        "provider_context_summary_payload",
        lambda require_admission, max_warning_admissions, context_window=None, include_l0=(), l0_store=None: {
            "schema_version": "v1",
            "l0_candidates": [
                {"cid": "A", "inclusion_reason": "explicit", "token_cost": 1},
                {"cid": "A", "inclusion_reason": "explicit", "token_cost": -1},
            ],
            "l0_included": [
                {"cid": "B", "inclusion_reason": "explicit", "token_cost": 1}
            ],
            "l0_dropped": [],
        },
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--print-context-summary",
            "--summary-format",
            "json",
            "--validate-l0-invariants",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 0

    summary_text, _final_prompt = capsys.readouterr().out.split("\n\nFinal prompt:\n", 1)
    data = json.loads(summary_text)

    assert [error["code"] for error in data["validation"]["l0_invariants"]["errors"]] == [
        "L0I_DUPLICATE_CID",
        "L0I_INVALID_TOKEN_COST",
        "L0I_INCLUDED_NOT_CANDIDATE",
    ]


def test_main_print_prompt_context_summary_json_validation_can_fail_nonzero(
    monkeypatch,
    capsys,
):
    import json

    from scripts import ask_provider

    monkeypatch.setattr(
        ask_provider,
        "build_latest_context_pack_text",
        lambda task, token_budget=None, model_target=None, scope=None, require_admission=False, task_label=None, full_prompt_hash=None, max_warning_admissions=None, **kwargs: "# Generated Context Pack",
    )
    monkeypatch.setattr(
        ask_provider,
        "provider_context_summary_payload",
        lambda require_admission, max_warning_admissions, context_window=None, include_l0=(), l0_store=None: {
            "schema_version": "v1",
            "l0_candidates": {},
            "l0_included": [],
            "l0_dropped": [],
        },
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--print-context-summary",
            "--summary-format",
            "json",
            "--validate-l0-invariants",
            "--fail-on-invalid-l0",
            "--print-prompt",
        ],
    )

    assert ask_provider.main() == 1

    data = json.loads(capsys.readouterr().out)

    assert data["validation"]["l0_invariants"]["ok"] is False


def test_main_validate_l0_invariants_requires_json_summary(monkeypatch):
    import pytest

    from scripts import ask_provider

    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "Do",
            "summary",
            "step.",
            "--latest-context",
            "--print-context-summary",
            "--validate-l0-invariants",
            "--print-prompt",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        ask_provider.main()

    assert exc_info.value.code == 2


def test_main_latest_context_print_prompt_can_include_l0(monkeypatch, tmp_path, capsys):
    import scripts.ask_provider as script

    captured = []

    def fake_build_latest_context_pack_text(**kwargs):
        captured.append(kwargs)
        return "CTX"

    monkeypatch.setattr(
        script,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "hello",
            "--latest-context",
            "--print-prompt",
            "--include-l0",
            "chunk-a",
            "--l0-store",
            str(tmp_path),
        ],
    )

    assert script.main() == 0
    rendered = capsys.readouterr().out

    assert "BEGIN CONTEXT PACK" in rendered
    assert captured
    assert all(call["include_l0"] == ("chunk-a",) for call in captured)
    assert all(call["l0_store"] == tmp_path for call in captured)


def test_main_latest_context_print_prompt_can_auto_include_l0_discovery(monkeypatch, tmp_path, capsys):
    import scripts.ask_provider as script

    captured = []

    def fake_build_latest_context_pack_text(**kwargs):
        captured.append(kwargs)
        return "CTX"

    monkeypatch.setattr(
        script,
        "build_latest_context_pack_text",
        fake_build_latest_context_pack_text,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ask_provider.py",
            "openai",
            "hello",
            "--latest-context",
            "--print-prompt",
            "--auto-include-l0-discovery",
            "--auto-include-l0-discovery-max-items",
            "2",
            "--l0-store",
            str(tmp_path),
        ],
    )

    assert script.main() == 0
    rendered = capsys.readouterr().out

    assert "BEGIN CONTEXT PACK" in rendered
    assert captured
    assert all(call["auto_include_l0_discovery"] is True for call in captured)
    assert all(call["auto_include_l0_discovery_max_items"] == 2 for call in captured)
    assert all(call["l0_store"] == tmp_path for call in captured)
