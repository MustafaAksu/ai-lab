from scripts.compare_providers import build_markdown_artifact


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
    )

    assert "# Provider Comparison" in artifact
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
