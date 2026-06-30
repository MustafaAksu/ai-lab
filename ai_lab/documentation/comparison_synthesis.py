from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re


DEFAULT_SYNTHESIS_DIR = Path("docs/comparisons/syntheses")


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def slugify(text: str) -> str:
    """Convert a title into a filesystem-safe slug."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "synthesis"


def next_synthesis_id(directory: Path) -> str:
    """Return the next SYNCOMP-XXXX identifier for a synthesis directory."""
    max_number = 0

    if directory.exists():
        for path in directory.glob("SYNCOMP-*.md"):
            match = re.match(r"SYNCOMP-(\d{4})", path.name)
            if match:
                max_number = max(max_number, int(match.group(1)))

    return f"SYNCOMP-{max_number + 1:04d}"


def auto_synthesis_path(title: str, directory: Path = DEFAULT_SYNTHESIS_DIR) -> Path:
    """Build the next synthesis artifact path from a title."""
    synthesis_id = next_synthesis_id(directory)
    slug = slugify(title)
    return directory / f"{synthesis_id}-{slug}.md"


def title_from_comparison_path(path: Path) -> str:
    """Derive a synthesis title from a comparison artifact path."""
    stem = path.stem

    if stem.startswith("COMP-"):
        parts = stem.split("-", 2)
        if len(parts) == 3:
            return parts[2].replace("-", " ").title()

    return stem.replace("-", " ").title()


def build_synthesis_prompt(comparison_markdown: str) -> str:
    """Build the prompt used to synthesize a provider comparison artifact."""
    return f"""You are synthesizing a saved AI-Lab provider comparison artifact.

Use ONLY the comparison artifact below. Do not introduce outside facts unless clearly labeled as inference.

Produce a structured synthesis with these sections:

1. Shared agreement
2. Meaningful differences
3. Stronger points from OpenAI
4. Stronger points from Claude
5. Combined answer
6. Risks or missing assumptions
7. Suggested re-ask prompt

Rules:
- Preserve disagreements.
- Do not claim consensus where there is only overlap.
- Treat the provider responses as primary artifacts.
- Treat your synthesis as a derived artifact.
- Keep the synthesis concise but useful.

COMPARISON ARTIFACT:
---
{comparison_markdown}
---
"""


def build_synthesis_artifact(
    synthesis_id: str,
    title: str,
    comparison_path: Path,
    comparison_markdown: str,
    synthesis_response: str,
    synthesizer_provider: str,
    synthesizer_model: str,
    created_at: str,
    command: str,
) -> str:
    """Build a Markdown synthesis artifact for one comparison."""
    return f"""# {synthesis_id}: Comparison Synthesis — {title}

## Metadata

- synthesis_id: `{synthesis_id}`
- title: `{title}`
- created_at: `{created_at}`
- command: `{command}`
- source_comparison: `{comparison_path.as_posix()}`
- synthesizer_provider: `{synthesizer_provider}`
- synthesizer_model: `{synthesizer_model}`

## Synthesis

~~~text
{synthesis_response}
~~~

## Source Comparison

~~~markdown
{comparison_markdown}
~~~
"""
