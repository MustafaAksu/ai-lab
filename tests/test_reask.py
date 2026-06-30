import pytest

from ai_lab.documentation.reask import (
    ReaskPromptError,
    extract_section,
    extract_suggested_reask_prompt,
    strip_markdown_fence,
)


def test_extract_section_returns_named_level_two_section():
    markdown = """# Artifact

## Metadata

ignored

## Synthesis

wanted

## Source Comparison

ignored
"""

    assert extract_section(markdown, "Synthesis") == "wanted"


def test_strip_markdown_fence_removes_tilde_fence():
    text = """~~~text
hello
~~~"""

    assert strip_markdown_fence(text) == "hello"


def test_extract_suggested_reask_prompt_from_numbered_synthesis():
    artifact = """# SYNCOMP-0001: Comparison Synthesis

## Synthesis

~~~text
1. Shared agreement
- Both agree.

7. Suggested re-ask prompt
- In one sentence, explain why artifact IDs improve traceability.
~~~

## Source Comparison

ignored
"""

    prompt = extract_suggested_reask_prompt(artifact)

    assert prompt == "In one sentence, explain why artifact IDs improve traceability."


def test_extract_suggested_reask_prompt_accepts_prompt_prefix():
    artifact = """# SYNCOMP-0001: Comparison Synthesis

## Synthesis

~~~text
## Suggested Re-Ask Prompt
Prompt: Compare the strongest point from each provider.
~~~
"""

    prompt = extract_suggested_reask_prompt(artifact)

    assert prompt == "Compare the strongest point from each provider."


def test_extract_suggested_reask_prompt_raises_when_missing():
    artifact = """# SYNCOMP-0001

## Synthesis

~~~text
No re-ask here.
~~~
"""

    with pytest.raises(ReaskPromptError):
        extract_suggested_reask_prompt(artifact)
