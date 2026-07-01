from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re

from ai_lab.documentation.chunk_reference import VALID_ARTIFACT_TYPES


class ArtifactSummaryError(ValueError):
    """Raised when an artifact summary is malformed or invalid."""


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _validate_cid(value: str, field_name: str = "artifact_cid") -> None:
    if not re.fullmatch(r"[0-9a-fA-F]{12,}", value):
        raise ArtifactSummaryError(f"{field_name} must be hex and at least 12 characters.")


def _validate_identifier(value: str, field_name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9._:/@+-]+", value):
        raise ArtifactSummaryError(f"{field_name} contains unsupported characters.")


def _validate_short_text(value: str, field_name: str, max_length: int = 500) -> None:
    if not value.strip():
        raise ArtifactSummaryError(f"{field_name} must not be empty.")

    if len(value) > max_length:
        raise ArtifactSummaryError(f"{field_name} must be <= {max_length} characters.")


@dataclass(frozen=True)
class ArtifactDependency:
    """A dependency from one artifact summary to another artifact version."""

    artifact_cid: str
    version: str
    path: str
    reason: str | None = None

    def __post_init__(self) -> None:
        _validate_cid(self.artifact_cid, "dependency.artifact_cid")
        _validate_identifier(self.version, "dependency.version")
        _validate_identifier(self.path, "dependency.path")

        if self.reason:
            _validate_short_text(self.reason, "dependency.reason", max_length=160)

    def to_dict(self) -> dict[str, str]:
        """Serialize the dependency into a JSON-compatible dictionary."""
        data = {
            "artifact_cid": self.artifact_cid,
            "version": self.version,
            "path": self.path,
        }

        if self.reason:
            data["reason"] = self.reason

        return data


@dataclass(frozen=True)
class ArtifactSummary:
    """
    Lightweight artifact-level discovery record.

    This does not replace chunk-level L0 summaries or artifact-level L1 narrative
    summaries. It helps discovery, dependency traversal, and rule-based seeding.
    """

    artifact_cid: str
    version: str
    path: str
    artifact_type: str
    language: str
    size_bytes: int
    complexity_score: float
    tags: tuple[str, ...] = field(default_factory=tuple)
    dependencies: tuple[ArtifactDependency, ...] = field(default_factory=tuple)
    synopsis: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    last_refreshed_at: str = field(default_factory=utc_now_iso)
    generator_model: str | None = None
    generator_version: str | None = None
    pipeline_run_id: str | None = None

    def __post_init__(self) -> None:
        _validate_cid(self.artifact_cid)
        _validate_identifier(self.version, "version")
        _validate_identifier(self.path, "path")
        _validate_identifier(self.language, "language")

        if self.artifact_type not in VALID_ARTIFACT_TYPES:
            raise ArtifactSummaryError(f"Unsupported artifact type: {self.artifact_type}")

        if self.size_bytes < 0:
            raise ArtifactSummaryError("size_bytes must be >= 0.")

        if self.complexity_score < 0:
            raise ArtifactSummaryError("complexity_score must be >= 0.")

        if len(self.tags) > 20:
            raise ArtifactSummaryError("tags must contain at most 20 items.")

        for tag in self.tags:
            _validate_short_text(tag, "tag", max_length=80)

        if self.synopsis:
            _validate_short_text(self.synopsis, "synopsis", max_length=500)

        if self.generator_model:
            _validate_identifier(self.generator_model, "generator_model")

        if self.generator_version:
            _validate_identifier(self.generator_version, "generator_version")

        if self.pipeline_run_id:
            _validate_identifier(self.pipeline_run_id, "pipeline_run_id")

    @property
    def artifact_ref(self) -> str:
        """Return the canonical artifact reference."""
        return f"{self.artifact_cid}@{self.version}"

    def to_dict(self) -> dict[str, object]:
        """Serialize the artifact summary into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "artifact_cid": self.artifact_cid,
            "version": self.version,
            "artifact_ref": self.artifact_ref,
            "path": self.path,
            "artifact_type": self.artifact_type,
            "language": self.language,
            "size_bytes": self.size_bytes,
            "complexity_score": self.complexity_score,
            "tags": list(self.tags),
            "dependencies": [
                dependency.to_dict()
                for dependency in self.dependencies
            ],
            "created_at": self.created_at,
            "last_refreshed_at": self.last_refreshed_at,
        }

        if self.synopsis:
            data["synopsis"] = self.synopsis

        if self.generator_model:
            data["generator"] = {
                "model": self.generator_model,
                "version": self.generator_version,
            }

        if self.pipeline_run_id:
            data["provenance"] = {
                "pipeline_run_id": self.pipeline_run_id,
            }

        return data
