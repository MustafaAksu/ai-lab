from __future__ import annotations

import re


class ReaskPromptError(ValueError):
    """Raised when a re-ask prompt cannot be extracted from a synthesis artifact."""


def _is_fence_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("~~~") or stripped.startswith("```")


def extract_section(markdown: str, heading: str) -> str:
    """Extract a level-two Markdown section by heading, ignoring headings in fences."""
    target = f"## {heading}"
    lines = markdown.splitlines()

    in_fence = False
    collecting = False
    collected: list[str] = []

    for line in lines:
        if collecting and _is_fence_line(line):
            in_fence = not in_fence
            collected.append(line)
            continue

        if not in_fence and line.strip() == target:
            collecting = True
            continue

        if collecting and not in_fence and line.startswith("## "):
            break

        if collecting:
            collected.append(line)

    if not collecting:
        raise ReaskPromptError(f"Section not found: {heading}")

    return "\n".join(collected).strip()


def strip_markdown_fence(text: str) -> str:
    """Strip a surrounding Markdown code fence if one wraps the whole text."""
    stripped = text.strip()
    lines = stripped.splitlines()

    if len(lines) >= 2:
        opening = lines[0].strip()
        closing = lines[-1].strip()

        if opening.startswith("~~~") and closing.startswith("~~~"):
            return "\n".join(lines[1:-1]).strip()

        if opening.startswith("```") and closing.startswith("```"):
            return "\n".join(lines[1:-1]).strip()

    return stripped


def _is_reask_heading(line: str) -> bool:
    normalized = line.strip().lower()
    normalized = re.sub(r"^#+\s*", "", normalized)
    normalized = re.sub(r"^\d+\.\s*", "", normalized)
    return normalized in {
        "suggested re-ask prompt",
        "suggested reask prompt",
        "re-ask prompt",
        "reask prompt",
    }


def _is_next_numbered_heading(line: str) -> bool:
    return bool(re.match(r"^\s*\d+\.\s+\S+", line))


def _clean_prompt_line(line: str) -> str:
    cleaned = line.strip()
    cleaned = re.sub(r"^[-*]\s+", "", cleaned)
    cleaned = re.sub(r"^prompt:\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def extract_suggested_reask_prompt(synthesis_artifact: str) -> str:
    """Extract the suggested re-ask prompt from a SYNCOMP artifact."""
    synthesis_section = extract_section(synthesis_artifact, "Synthesis")
    synthesis_text = strip_markdown_fence(synthesis_section)
    lines = synthesis_text.splitlines()

    for index, line in enumerate(lines):
        if not _is_reask_heading(line):
            continue

        prompt_lines: list[str] = []

        for following in lines[index + 1 :]:
            if prompt_lines and _is_next_numbered_heading(following):
                break

            cleaned = _clean_prompt_line(following)
            if cleaned:
                prompt_lines.append(cleaned)

        prompt = " ".join(prompt_lines).strip()

        if prompt:
            return prompt

    raise ReaskPromptError("Suggested re-ask prompt not found.")
