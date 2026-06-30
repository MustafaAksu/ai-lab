from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import re

from ai_lab.documentation.citations import Citation, CitationError, CitationSpan


class ChunkReferenceError(ValueError):
    """Raised when a chunk reference is malformed or invalid."""


VALID_ARTIFACT_TYPES = {
    "code",
    "doc",
    "config",
    "schema",
    "binary",
    "other",
}

VALID_REDACTION_LEVELS = {
    "none",
    "partial",
    "full",
}


def compute_chunk_id(
    artifact_cid: str,
    version: str,
    span: CitationSpan,
) -> str:
    """Compute a deterministic chunk ID from artifact cid, version, and span."""
    citation = Citation(
        cid=artifact_cid,
        version=version,
        span=span,
    )
    return sha256(str(citation).encode("utf-8")).hexdigest()


def _validate_optional_identifier(value: str, field_name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9._:/@+-]+", value):
        raise ChunkReferenceError(f"{field_name} contains unsupported characters.")


@dataclass(frozen=True)
class ChunkReference:
    """
    Reference to a span-bounded chunk inside one artifact version.

    The chunk_id is deterministic:
      sha256(artifact_cid@version|span)
    """

    chunk_id: str
    artifact_cid: str
    version: str
    span: CitationSpan
    path: str | None = None
    artifact_type: str = "other"
    language: str | None = None
    embedding_ids: tuple[str, ...] = field(default_factory=tuple)
    redaction_level: str = "none"

    def __post_init__(self) -> None:
        try:
            expected_chunk_id = compute_chunk_id(
                artifact_cid=self.artifact_cid,
                version=self.version,
                span=self.span,
            )
        except CitationError as error:
            raise ChunkReferenceError(str(error)) from error

        if self.chunk_id != expected_chunk_id:
            raise ChunkReferenceError("Chunk ID does not match artifact/version/span.")

        if self.artifact_type not in VALID_ARTIFACT_TYPES:
            raise ChunkReferenceError(f"Unsupported artifact type: {self.artifact_type}")

        if self.redaction_level not in VALID_REDACTION_LEVELS:
            raise ChunkReferenceError(f"Unsupported redaction level: {self.redaction_level}")

        if self.path:
            _validate_optional_identifier(self.path, "path")

        if self.language:
            _validate_optional_identifier(self.language, "language")

        for embedding_id in self.embedding_ids:
            _validate_optional_identifier(embedding_id, "embedding_id")

    @property
    def citation(self) -> Citation:
        """Return the citation represented by this chunk reference."""
        return Citation(
            cid=self.artifact_cid,
            version=self.version,
            span=self.span,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize the chunk reference into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "chunk_id": self.chunk_id,
            "artifact_cid": self.artifact_cid,
            "version": self.version,
            "span": {
                "unit": self.span.unit,
                "start": self.span.start,
                "end": self.span.end,
            },
            "artifact_type": self.artifact_type,
            "embedding_ids": list(self.embedding_ids),
            "redaction_level": self.redaction_level,
        }

        if self.span.tokenizer:
            data["span"]["tokenizer"] = self.span.tokenizer

        if self.path:
            data["path"] = self.path

        if self.language:
            data["language"] = self.language

        return data


def create_chunk_reference(
    artifact_cid: str,
    version: str,
    span: CitationSpan,
    path: str | None = None,
    artifact_type: str = "other",
    language: str | None = None,
    embedding_ids: tuple[str, ...] = (),
    redaction_level: str = "none",
) -> ChunkReference:
    """Create a chunk reference with a deterministic chunk ID."""
    chunk_id = compute_chunk_id(
        artifact_cid=artifact_cid,
        version=version,
        span=span,
    )

    return ChunkReference(
        chunk_id=chunk_id,
        artifact_cid=artifact_cid,
        version=version,
        span=span,
        path=path,
        artifact_type=artifact_type,
        language=language,
        embedding_ids=embedding_ids,
        redaction_level=redaction_level,
    )
