from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re

from ai_lab.documentation.chunk_reference import ChunkReference


class L0SummaryError(ValueError):
    """Raised when an L0 chunk summary is malformed or invalid."""


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
