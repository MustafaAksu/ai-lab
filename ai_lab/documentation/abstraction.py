from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re


DEFAULT_ABSTRACTION_DIR = Path("docs/abstractions")


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def slugify(text: str) -> str:
    """Convert a title into a filesystem-safe slug."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "abstraction"


def next_abstraction_id(directory: Path) -> str:
    """Return the next ABS-XXXX identifier for an abstraction directory."""
    max_number = 0

    if directory.exists():
        for path in directory.glob("ABS-*.md"):
            match = re.match(r"ABS-(\d{4})", path.name)
            if match:
                max_number = max(max_number, int(match.group(1)))

    return f"ABS-{max_number + 1:04d}"


def auto_abstraction_path(title: str, directory: Path = DEFAULT_ABSTRACTION_DIR) -> Path:
    """Build the next abstraction artifact path from a title."""
    abstraction_id = next_abstraction_id(directory)
    slug = slugify(title)
    return directory / f"{abstraction_id}-{slug}.md"


def abstraction_id_from_path(path: Path) -> str:
    """Extract ABS-XXXX from an abstraction artifact path."""
    match = re.match(r"(ABS-\d{4})", path.name)

    if match:
        return match.group(1)

    return path.stem


def compact_artifact_markdown(markdown: str) -> str:
    """Remove embedded lower-source sections from derived artifacts."""
    section_markers = [
        "\n## Source Comparison\n",
        "\n## Source Comparisons\n",
        "\n## Source Artifacts\n",
    ]

    compact = markdown

    for marker in section_markers:
        if marker in compact:
            compact = compact.split(marker, 1)[0].rstrip() + "\n"

    return compact


def build_abstraction_prompt(
    title: str,
    abstraction_level: int,
    source_artifacts: list[tuple[Path, str]],
) -> str:
    """Build the prompt used to create a generic abstraction artifact."""
    source_blocks: list[str] = []

    for path, markdown in source_artifacts:
        compact_markdown = compact_artifact_markdown(markdown)
        source_blocks.append(
            f"""SOURCE ARTIFACT: {path.as_posix()}
---
{compact_markdown}
---"""
        )

    sources = "\n\n".join(source_blocks)

    return f"""You are creating a generic AI-Lab abstraction artifact.

Use ONLY the source artifacts below. Do not introduce outside facts unless clearly labeled as inference.

Title: {title}
Abstraction level: {abstraction_level}

Create a compact abstraction over the source artifacts.

Use these sections:

1. Stable claims
2. Important distinctions
3. Unsupported strengthenings or risks
4. Useful compression
5. Retrieval hints

Rules:
- Preserve uncertainty.
- Preserve disagreement.
- Do not turn provider claims into project truth.
- Do not load unnecessary detail into the abstraction.
- The abstraction should help future retrieval decide what lower artifacts are worth opening.
- Use numeric abstraction level only; do not invent named cognitive layers.

SOURCE ARTIFACTS:
{sources}
"""


def build_abstraction_artifact(
    abstraction_id: str,
    title: str,
    abstraction_level: int,
    source_paths: list[Path],
    abstraction_response: str,
    abstracter_provider: str,
    abstracter_model: str,
    created_at: str,
    command: str,
) -> str:
    """Build a Markdown abstraction artifact."""
    source_list = ", ".join(path.as_posix() for path in source_paths)

    source_lines = "\n".join(
        f"- `{path.as_posix()}`"
        for path in source_paths
    )

    return f"""# {abstraction_id}: Abstraction — {title}

## Metadata

- abstraction_id: `{abstraction_id}`
- title: `{title}`
- abstraction_level: `{abstraction_level}`
- source_artifacts: `{source_list}`
- created_at: `{created_at}`
- command: `{command}`
- abstracter_provider: `{abstracter_provider}`
- abstracter_model: `{abstracter_model}`

## Source Artifacts

{source_lines}

## Abstraction

~~~text
{abstraction_response}
~~~
"""
