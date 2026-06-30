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
    source_artifacts: str | None = None
    abstraction_level: str | None = None


def artifact_kind_from_path(path: Path) -> str:
    if path.name.startswith("ABS-"):
        return "ABS"

    if path.name.startswith("SYNCOMP-"):
        return "SYNCOMP"

    if path.name.startswith("COMP-"):
        return "COMP"

    return "UNKNOWN"


def artifact_id_from_path(path: Path) -> str:
    match = re.match(r"(ABS-\d{4}|SYNCOMP-\d{4}|COMP-\d{4})", path.name)

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
        or metadata.get("abstraction_id")
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
        source_artifacts=metadata.get("source_artifacts"),
        abstraction_level=metadata.get("abstraction_level"),
    )


def discover_artifacts(
    comparison_dir: Path = Path("docs/comparisons"),
    abstraction_dir: Path | None = None,
) -> list[ArtifactRecord]:
    records: list[ArtifactRecord] = []

    if abstraction_dir is None:
        abstraction_dir = comparison_dir.parent / "abstractions"

    for path in sorted(comparison_dir.glob("COMP-*.md")):
        records.append(artifact_record_from_file(path))

    synthesis_dir = comparison_dir / "syntheses"
    for path in sorted(synthesis_dir.glob("SYNCOMP-*.md")):
        records.append(artifact_record_from_file(path))

    for path in sorted(abstraction_dir.glob("ABS-*.md")):
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
        source = (
            record.source_synthesis
            or record.source_comparison
            or record.source_artifacts
            or ""
        )
        lines.append(
            f"{record.artifact_id} | {record.kind} | {record.title} | {source}"
        )

    return "\n".join(lines)

class ArtifactHistoryError(ValueError):
    """Raised when artifact history cannot be resolved."""


def source_path_for_record(record: ArtifactRecord) -> str | None:
    """Return the primary source artifact path recorded by an artifact, if any."""
    return record.source_synthesis or record.source_comparison


def source_paths_for_record(record: ArtifactRecord) -> list[str]:
    """Return all source artifact paths recorded by an artifact."""
    if record.source_artifacts:
        return [
            source.strip()
            for source in record.source_artifacts.split(",")
            if source.strip()
        ]

    primary_source = source_path_for_record(record)

    if primary_source:
        return [primary_source]

    return []


def records_by_id(records: list[ArtifactRecord]) -> dict[str, ArtifactRecord]:
    """Index artifact records by artifact ID."""
    return {record.artifact_id: record for record in records}


def lineage_for_artifact(
    records: list[ArtifactRecord],
    target_id: str,
) -> list[ArtifactRecord]:
    """Return the source-to-target lineage chain for an artifact."""
    index = records_by_id(records)

    if target_id not in index:
        raise ArtifactHistoryError(f"Artifact not found: {target_id}")

    chain: list[ArtifactRecord] = []
    seen: set[str] = set()
    current_id: str | None = target_id

    while current_id:
        if current_id in seen:
            raise ArtifactHistoryError(f"Cycle detected at artifact: {current_id}")

        seen.add(current_id)

        current = index[current_id]
        chain.append(current)

        source_path = source_path_for_record(current)
        if not source_path:
            break

        source_id = artifact_id_from_path(Path(source_path))
        if source_id not in index:
            break

        current_id = source_id

    return list(reversed(chain))


def relation_label_for_child(record: ArtifactRecord) -> str:
    """Return a readable relation label from a parent artifact to this child."""
    if record.source_artifacts:
        return "abstracted into"

    if record.source_comparison:
        return "synthesized into"

    if record.source_synthesis:
        return "re-asked into"

    return "derived into"


def format_artifact_lineage(
    records: list[ArtifactRecord],
    target_id: str,
) -> str:
    """Format a source-to-target lineage chain as readable text."""
    chain = lineage_for_artifact(records, target_id)

    lines = [
        f"Lineage for {target_id}",
        "",
    ]

    for index, record in enumerate(chain):
        indent = "  " * index

        if index > 0:
            relation = relation_label_for_child(record)
            lines.append(f"{indent}↓ {relation}")

        lines.append(
            f"{indent}{record.artifact_id} [{record.kind}] {record.title}"
        )

    return "\n".join(lines)

def format_artifact_source_tree(
    records: list[ArtifactRecord],
    target_id: str,
) -> str:
    """Format recursive source dependencies for an artifact."""
    index = records_by_id(records)

    if target_id not in index:
        raise ArtifactHistoryError(f"Artifact not found: {target_id}")

    lines = [f"Source tree for {target_id}", ""]

    def walk(artifact_id: str, depth: int, seen: set[str]) -> None:
        if artifact_id in seen:
            lines.append(f"{'  ' * depth}{artifact_id} [cycle]")
            return

        record = index[artifact_id]
        lines.append(
            f"{'  ' * depth}{record.artifact_id} [{record.kind}] {record.title}"
        )

        source_paths = source_paths_for_record(record)
        if not source_paths:
            return

        relation = relation_label_for_child(record)

        for source_path in source_paths:
            source_id = artifact_id_from_path(Path(source_path))
            lines.append(f"{'  ' * (depth + 1)}↑ source for {relation}")

            if source_id in index:
                walk(source_id, depth + 2, seen | {artifact_id})
            else:
                lines.append(f"{'  ' * (depth + 2)}{source_path} [not indexed]")

    walk(target_id, 0, set())

    return "\n".join(lines)

def context_level_for_record(record: ArtifactRecord) -> str:
    """Return the context level bucket for an artifact."""
    if record.kind == "ABS" and record.abstraction_level:
        return f"ABS-L{record.abstraction_level}"

    return record.kind


def _record_sort_key(record: ArtifactRecord) -> tuple[str, str]:
    """Sort records by creation time, then artifact ID."""
    return (record.created_at or "", record.artifact_id)


def latest_records_by_context_level(
    records: list[ArtifactRecord],
) -> dict[str, ArtifactRecord]:
    """Return the latest artifact for each context level."""
    latest: dict[str, ArtifactRecord] = {}

    for record in records:
        level = context_level_for_record(record)

        if level not in latest or _record_sort_key(record) > _record_sort_key(latest[level]):
            latest[level] = record

    return latest


def _context_level_display_order(level: str) -> tuple[int, int, str]:
    """Sort higher abstraction first, then synthesis, then raw comparison."""
    if level.startswith("ABS-L"):
        try:
            number = int(level.removeprefix("ABS-L"))
        except ValueError:
            number = 0

        return (0, -number, level)

    if level == "SYNCOMP":
        return (1, 0, level)

    if level == "COMP":
        return (2, 0, level)

    return (3, 0, level)


def format_latest_context(records: list[ArtifactRecord]) -> str:
    """Format the latest artifact from each context level."""
    latest = latest_records_by_context_level(records)

    if not latest:
        return "No context artifacts found."

    lines = [
        "Level | ID | Kind | Title | Path",
        "--- | --- | --- | --- | ---",
    ]

    for level, record in sorted(latest.items(), key=lambda item: _context_level_display_order(item[0])):
        lines.append(
            f"{level} | {record.artifact_id} | {record.kind} | {record.title} | {record.path.as_posix()}"
        )

    return "\n".join(lines)

