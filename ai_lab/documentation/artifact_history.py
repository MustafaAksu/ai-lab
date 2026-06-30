from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from ai_lab.documentation.reask import ReaskPromptError, extract_section


@dataclass(frozen=True)
class ArtifactRecord:
    artifact_id: str
    kind: str
    title: str
    path: Path
    created_at: str | None = None
    source_comparison: str | None = None
    source_synthesis: str | None = None


def artifact_kind_from_path(path: Path) -> str:
    if path.name.startswith("SYNCOMP-"):
        return "SYNCOMP"

    if path.name.startswith("COMP-"):
        return "COMP"

    return "UNKNOWN"


def artifact_id_from_path(path: Path) -> str:
    match = re.match(r"(SYNCOMP-\d{4}|COMP-\d{4})", path.name)

    if match:
        return match.group(1)

    return path.stem


def title_from_path(path: Path) -> str:
    """Derive a readable title from an artifact filename."""
    stem = path.stem
    stem = re.sub(r"^(SYNCOMP|COMP)-\d{4}-?", "", stem)
    return stem.replace("-", " ").title() or path.stem


def parse_metadata(markdown: str) -> dict[str, str]:
    try:
        metadata_section = extract_section(markdown, "Metadata")
    except ReaskPromptError:
        return {}

    metadata: dict[str, str] = {}

    for line in metadata_section.splitlines():
        match = re.match(r"\s*-\s+([a-zA-Z0-9_]+):\s+`([^`]*)`", line)
        if match:
            metadata[match.group(1)] = match.group(2)

    return metadata


def artifact_record_from_file(path: Path) -> ArtifactRecord:
    markdown = path.read_text(encoding="utf-8")
    metadata = parse_metadata(markdown)
    kind = artifact_kind_from_path(path)

    artifact_id = (
        metadata.get("comparison_id")
        or metadata.get("synthesis_id")
        or artifact_id_from_path(path)
    )

    title = metadata.get("title") or title_from_path(path)

    return ArtifactRecord(
        artifact_id=artifact_id,
        kind=kind,
        title=title,
        path=path,
        created_at=metadata.get("created_at"),
        source_comparison=metadata.get("source_comparison"),
        source_synthesis=metadata.get("source_synthesis"),
    )


def discover_artifacts(comparison_dir: Path = Path("docs/comparisons")) -> list[ArtifactRecord]:
    records: list[ArtifactRecord] = []

    for path in sorted(comparison_dir.glob("COMP-*.md")):
        records.append(artifact_record_from_file(path))

    synthesis_dir = comparison_dir / "syntheses"
    for path in sorted(synthesis_dir.glob("SYNCOMP-*.md")):
        records.append(artifact_record_from_file(path))

    return sorted(records, key=lambda record: (record.created_at or "", record.artifact_id))


def format_artifact_history(records: list[ArtifactRecord]) -> str:
    if not records:
        return "No comparison artifacts found."

    lines = [
        "ID | Kind | Title | Source",
        "--- | --- | --- | ---",
    ]

    for record in records:
        source = record.source_synthesis or record.source_comparison or ""
        lines.append(
            f"{record.artifact_id} | {record.kind} | {record.title} | {source}"
        )

    return "\n".join(lines)
