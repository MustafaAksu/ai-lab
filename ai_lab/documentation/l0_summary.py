from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re

from ai_lab.documentation.chunk_reference import ChunkReference


class L0SummaryError(ValueError):
    """Raised when an L0 chunk summary is malformed or invalid."""


REQUIRED_L0_RECORD_FIELDS = {
    "chunk_reference",
    "citation",
    "l0_summary",
    "keyphrases",
    "entities",
    "claims",
    "risks",
    "created_at",
    "last_refreshed_at",
}

REQUIRED_CHUNK_REFERENCE_FIELDS = {
    "chunk_id",
    "artifact_cid",
    "version",
    "span",
    "artifact_type",
    "embedding_ids",
    "redaction_level",
}

REQUIRED_CHUNK_SPAN_FIELDS = {
    "unit",
    "start",
    "end",
}


def validate_l0_summary_record(record: dict[str, object]) -> None:
    """Validate the JSON shape emitted by L0ChunkSummary.to_dict."""

    _require_mapping(record, "$")

    for field_name in sorted(REQUIRED_L0_RECORD_FIELDS):
        if field_name not in record:
            raise L0SummaryError(f"Missing required L0 field: {field_name}")

    _validate_chunk_reference_record(record["chunk_reference"])
    _require_non_empty_string(record["citation"], "$.citation")
    _require_non_empty_string(record["l0_summary"], "$.l0_summary")

    keyphrases = _require_list(record["keyphrases"], "$.keyphrases")
    if not (3 <= len(keyphrases) <= 10):
        raise L0SummaryError("$.keyphrases must contain between 3 and 10 items.")

    for index, keyphrase in enumerate(keyphrases):
        _require_non_empty_string(keyphrase, f"$.keyphrases[{index}]")

    _validate_entity_records(record["entities"])
    _validate_claim_records(record["claims"])
    _validate_risk_records(record["risks"])

    _require_non_empty_string(record["created_at"], "$.created_at")
    _require_non_empty_string(record["last_refreshed_at"], "$.last_refreshed_at")

    if "generator" in record:
        _validate_generator_record(record["generator"])

    if "provenance" in record:
        _validate_provenance_record(record["provenance"])


def _validate_chunk_reference_record(value: object) -> None:
    reference = _require_mapping(value, "$.chunk_reference")

    for field_name in sorted(REQUIRED_CHUNK_REFERENCE_FIELDS):
        if field_name not in reference:
            raise L0SummaryError(
                f"Missing required chunk_reference field: {field_name}"
            )

    _require_non_empty_string(reference["chunk_id"], "$.chunk_reference.chunk_id")
    _require_non_empty_string(
        reference["artifact_cid"],
        "$.chunk_reference.artifact_cid",
    )
    _require_non_empty_string(reference["version"], "$.chunk_reference.version")
    _require_non_empty_string(
        reference["artifact_type"],
        "$.chunk_reference.artifact_type",
    )
    _require_non_empty_string(
        reference["redaction_level"],
        "$.chunk_reference.redaction_level",
    )

    span = _require_mapping(reference["span"], "$.chunk_reference.span")
    for field_name in sorted(REQUIRED_CHUNK_SPAN_FIELDS):
        if field_name not in span:
            raise L0SummaryError(
                f"Missing required chunk_reference.span field: {field_name}"
            )

    _require_non_empty_string(span["unit"], "$.chunk_reference.span.unit")
    _require_int(span["start"], "$.chunk_reference.span.start")
    _require_int(span["end"], "$.chunk_reference.span.end")

    if "tokenizer" in span:
        _require_non_empty_string(
            span["tokenizer"],
            "$.chunk_reference.span.tokenizer",
        )

    embedding_ids = _require_list(
        reference["embedding_ids"],
        "$.chunk_reference.embedding_ids",
    )
    for index, embedding_id in enumerate(embedding_ids):
        _require_non_empty_string(
            embedding_id,
            f"$.chunk_reference.embedding_ids[{index}]",
        )

    if "path" in reference:
        _require_non_empty_string(reference["path"], "$.chunk_reference.path")

    if "language" in reference:
        _require_non_empty_string(reference["language"], "$.chunk_reference.language")


def _validate_entity_records(value: object) -> None:
    entities = _require_list(value, "$.entities")
    for index, entity in enumerate(entities):
        record = _require_mapping(entity, f"$.entities[{index}]")
        _require_non_empty_string(record.get("type"), f"$.entities[{index}].type")
        _require_non_empty_string(record.get("name"), f"$.entities[{index}].name")


def _validate_claim_records(value: object) -> None:
    claims = _require_list(value, "$.claims")
    for index, claim in enumerate(claims):
        record = _require_mapping(claim, f"$.claims[{index}]")
        _require_non_empty_string(record.get("text"), f"$.claims[{index}].text")
        _require_non_empty_string(
            record.get("polarity"),
            f"$.claims[{index}].polarity",
        )


def _validate_risk_records(value: object) -> None:
    risks = _require_list(value, "$.risks")
    for index, risk in enumerate(risks):
        record = _require_mapping(risk, f"$.risks[{index}]")
        _require_non_empty_string(record.get("text"), f"$.risks[{index}].text")
        _require_non_empty_string(
            record.get("severity"),
            f"$.risks[{index}].severity",
        )


def _validate_generator_record(value: object) -> None:
    generator = _require_mapping(value, "$.generator")
    _require_non_empty_string(generator.get("model"), "$.generator.model")

    if "version" in generator and generator["version"] is not None:
        _require_non_empty_string(generator["version"], "$.generator.version")


def _validate_provenance_record(value: object) -> None:
    provenance = _require_mapping(value, "$.provenance")
    _require_non_empty_string(
        provenance.get("pipeline_run_id"),
        "$.provenance.pipeline_run_id",
    )


def _require_mapping(value: object, path: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise L0SummaryError(f"{path} must be an object.")

    return value


def _require_list(value: object, path: str) -> list[object]:
    if not isinstance(value, list):
        raise L0SummaryError(f"{path} must be a list.")

    return value


def _require_non_empty_string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise L0SummaryError(f"{path} must be a non-empty string.")

    return value


def _require_int(value: object, path: str) -> int:
    if not isinstance(value, int):
        raise L0SummaryError(f"{path} must be an int.")

    return value


VALID_CLAIM_POLARITIES = {
    "pro",
    "con",
    "neutral",
}

VALID_RISK_SEVERITIES = {
    "low",
    "med",
    "high",
}


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _validate_short_text(value: str, field_name: str, max_length: int = 300) -> None:
    if not value.strip():
        raise L0SummaryError(f"{field_name} must not be empty.")

    if len(value) > max_length:
        raise L0SummaryError(f"{field_name} must be <= {max_length} characters.")


def _validate_identifier(value: str, field_name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9._:/@+-]+", value):
        raise L0SummaryError(f"{field_name} contains unsupported characters.")


@dataclass(frozen=True)
class Entity:
    """A named entity observed in a chunk."""

    type: str
    name: str

    def __post_init__(self) -> None:
        _validate_identifier(self.type, "entity.type")
        _validate_short_text(self.name, "entity.name", max_length=120)


@dataclass(frozen=True)
class Claim:
    """A short claim extracted from a chunk."""

    text: str
    polarity: str = "neutral"

    def __post_init__(self) -> None:
        _validate_short_text(self.text, "claim.text", max_length=300)

        if self.polarity not in VALID_CLAIM_POLARITIES:
            raise L0SummaryError(f"Unsupported claim polarity: {self.polarity}")


@dataclass(frozen=True)
class Risk:
    """A short risk extracted from a chunk."""

    text: str
    severity: str = "med"

    def __post_init__(self) -> None:
        _validate_short_text(self.text, "risk.text", max_length=300)

        if self.severity not in VALID_RISK_SEVERITIES:
            raise L0SummaryError(f"Unsupported risk severity: {self.severity}")


@dataclass(frozen=True)
class L0ChunkSummary:
    """
    Minimal retrieval summary for one span-bounded chunk.

    L0 is chunk-level and should remain compact.
    """

    chunk_reference: ChunkReference
    l0_summary: str
    keyphrases: tuple[str, ...]
    entities: tuple[Entity, ...] = field(default_factory=tuple)
    claims: tuple[Claim, ...] = field(default_factory=tuple)
    risks: tuple[Risk, ...] = field(default_factory=tuple)
    created_at: str = field(default_factory=utc_now_iso)
    last_refreshed_at: str = field(default_factory=utc_now_iso)
    generator_model: str | None = None
    generator_version: str | None = None
    pipeline_run_id: str | None = None

    def __post_init__(self) -> None:
        _validate_short_text(self.l0_summary, "l0_summary", max_length=300)

        if not (3 <= len(self.keyphrases) <= 10):
            raise L0SummaryError("keyphrases must contain between 3 and 10 items.")

        for keyphrase in self.keyphrases:
            _validate_short_text(keyphrase, "keyphrase", max_length=80)

        if self.generator_model:
            _validate_identifier(self.generator_model, "generator_model")

        if self.generator_version:
            _validate_identifier(self.generator_version, "generator_version")

        if self.pipeline_run_id:
            _validate_identifier(self.pipeline_run_id, "pipeline_run_id")

    @property
    def citation(self) -> str:
        """Return the citation for the summarized chunk."""
        return str(self.chunk_reference.citation)

    def to_dict(self) -> dict[str, object]:
        """Serialize the L0 summary into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "chunk_reference": self.chunk_reference.to_dict(),
            "citation": self.citation,
            "l0_summary": self.l0_summary,
            "keyphrases": list(self.keyphrases),
            "entities": [
                {
                    "type": entity.type,
                    "name": entity.name,
                }
                for entity in self.entities
            ],
            "claims": [
                {
                    "text": claim.text,
                    "polarity": claim.polarity,
                }
                for claim in self.claims
            ],
            "risks": [
                {
                    "text": risk.text,
                    "severity": risk.severity,
                }
                for risk in self.risks
            ],
            "created_at": self.created_at,
            "last_refreshed_at": self.last_refreshed_at,
        }

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
