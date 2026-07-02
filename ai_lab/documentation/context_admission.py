"""Context-admission verdict schema.

This module adds a small, durable verdict layer for deciding whether a memory
or artifact item is admissible into a context pack.

It is intentionally not a graph database and does not modify context selection
yet. It is the first warrant/admission primitive that later context assembly can
use before adding full WarrantEdge/MemoryEdge persistence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any

from ai_lab.documentation.citations import CitationError, parse_citation
from ai_lab.documentation.context_pack import VALID_CONTEXT_ITEM_TYPES


class ContextAdmissionError(ValueError):
    """Raised when a context-admission verdict is invalid."""


VALID_ADMISSION_DECISIONS = {
    "admit",
    "admit_with_warning",
    "exclude",
}

VALID_FRESHNESS_STATES = {
    "fresh",
    "stale",
    "unknown",
}

VALID_WARRANT_STATES = {
    "supported",
    "disputed",
    "unreviewed",
    "superseded",
    "rejected",
}

VALID_SUBSTRATES = {
    "human",
    "model",
    "deterministic",
    "process",
}

_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@|+-]{0,255}$")


def _validate_id(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ContextAdmissionError(f"{field_name} must be a non-empty string.")
    if not _ID_RE.match(value):
        raise ContextAdmissionError(
            f"{field_name} must start with an alphanumeric character and "
            "contain only letters, numbers, '_', '.', ':', '@', '|', '+', or '-'."
        )


def _validate_short_text(
    value: str,
    field_name: str,
    *,
    max_length: int,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, str):
        raise ContextAdmissionError(f"{field_name} must be a string.")
    if not allow_empty and not value.strip():
        raise ContextAdmissionError(f"{field_name} must not be empty.")
    if len(value) > max_length:
        raise ContextAdmissionError(f"{field_name} must be <= {max_length} characters.")


def _validate_iso_datetime(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ContextAdmissionError(f"{field_name} must be a non-empty ISO datetime string.")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContextAdmissionError(f"{field_name} must be an ISO datetime string.") from exc


def _validate_optional_iso_datetime(value: str | None, field_name: str) -> None:
    if value is not None:
        _validate_iso_datetime(value, field_name)


def _as_tuple(values: tuple[str, ...] | list[str], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise ContextAdmissionError(f"{field_name} must be a tuple or list of strings.")

    normalized = tuple(values)

    for value in normalized:
        _validate_short_text(value, field_name, max_length=512)

    if len(set(normalized)) != len(normalized):
        raise ContextAdmissionError(f"{field_name} must not contain duplicates.")

    return normalized


def _coerce_tuple_fields(payload: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    normalized = dict(payload)
    for field_name in fields:
        if field_name in normalized and isinstance(normalized[field_name], list):
            normalized[field_name] = tuple(normalized[field_name])
    return normalized


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _read_json(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text())
    if not isinstance(payload, dict):
        raise ContextAdmissionError("JSON payload must be an object.")
    return payload


def compute_context_admission_verdict_id(
    *,
    target_item_id: str,
    target_item_type: str,
    decision: str,
    freshness_state: str,
    warrant_state: str,
    created_at: str,
    author: str,
    substrate: str,
) -> str:
    """Compute a deterministic verdict ID from the load-bearing fields."""

    payload = "|".join(
        (
            target_item_id,
            target_item_type,
            decision,
            freshness_state,
            warrant_state,
            created_at,
            author,
            substrate,
        )
    )
    return f"CADM-{sha256(payload.encode('utf-8')).hexdigest()[:12]}"


@dataclass(frozen=True)
class ContextAdmissionVerdict:
    """A warrant-bearing decision about context-pack admission."""

    verdict_id: str
    target_item_id: str
    target_item_type: str
    decision: str
    freshness_state: str
    warrant_state: str
    author: str
    substrate: str
    created_at: str
    reason: str
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_paths: tuple[str, ...] = field(default_factory=tuple)
    citations: tuple[str, ...] = field(default_factory=tuple)
    expires_at: str | None = None
    note: str | None = None

    def __post_init__(self) -> None:
        _validate_id(self.verdict_id, "verdict_id")
        _validate_id(self.target_item_id, "target_item_id")

        if self.target_item_type not in VALID_CONTEXT_ITEM_TYPES:
            raise ContextAdmissionError(
                f"target_item_type must be one of {sorted(VALID_CONTEXT_ITEM_TYPES)}."
            )

        if self.decision not in VALID_ADMISSION_DECISIONS:
            raise ContextAdmissionError(
                f"decision must be one of {sorted(VALID_ADMISSION_DECISIONS)}."
            )

        if self.freshness_state not in VALID_FRESHNESS_STATES:
            raise ContextAdmissionError(
                f"freshness_state must be one of {sorted(VALID_FRESHNESS_STATES)}."
            )

        if self.warrant_state not in VALID_WARRANT_STATES:
            raise ContextAdmissionError(
                f"warrant_state must be one of {sorted(VALID_WARRANT_STATES)}."
            )

        _validate_short_text(self.author, "author", max_length=128)

        if self.substrate not in VALID_SUBSTRATES:
            raise ContextAdmissionError(
                f"substrate must be one of {sorted(VALID_SUBSTRATES)}."
            )

        _validate_iso_datetime(self.created_at, "created_at")
        _validate_short_text(self.reason, "reason", max_length=1000)

        object.__setattr__(self, "evidence_ids", _as_tuple(self.evidence_ids, "evidence_ids"))
        object.__setattr__(
            self,
            "evidence_paths",
            _as_tuple(self.evidence_paths, "evidence_paths"),
        )
        object.__setattr__(self, "citations", _as_tuple(self.citations, "citations"))

        for citation in self.citations:
            try:
                parse_citation(citation)
            except CitationError as exc:
                raise ContextAdmissionError(f"Invalid citation: {citation}") from exc

        _validate_optional_iso_datetime(self.expires_at, "expires_at")

        if self.note is not None:
            _validate_short_text(self.note, "note", max_length=1000, allow_empty=True)

        if self.decision == "admit" and self.warrant_state in {"disputed", "rejected"}:
            raise ContextAdmissionError(
                "decision=admit is not allowed for disputed or rejected warrant_state."
            )

        if self.decision != "exclude" and self.freshness_state == "stale":
            raise ContextAdmissionError(
                "stale items must use decision=exclude unless a later policy adds override."
            )

    @classmethod
    def build(
        cls,
        *,
        target_item_id: str,
        target_item_type: str,
        decision: str,
        freshness_state: str,
        warrant_state: str,
        author: str,
        substrate: str,
        created_at: str,
        reason: str,
        **kwargs: Any,
    ) -> "ContextAdmissionVerdict":
        """Build a verdict and derive a deterministic verdict_id."""

        verdict_id = compute_context_admission_verdict_id(
            target_item_id=target_item_id,
            target_item_type=target_item_type,
            decision=decision,
            freshness_state=freshness_state,
            warrant_state=warrant_state,
            created_at=created_at,
            author=author,
            substrate=substrate,
        )

        return cls(
            verdict_id=verdict_id,
            target_item_id=target_item_id,
            target_item_type=target_item_type,
            decision=decision,
            freshness_state=freshness_state,
            warrant_state=warrant_state,
            author=author,
            substrate=substrate,
            created_at=created_at,
            reason=reason,
            **kwargs,
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ContextAdmissionVerdict":
        """Load a verdict from a JSON-style dictionary."""

        if not isinstance(payload, dict):
            raise ContextAdmissionError("ContextAdmissionVerdict payload must be a dictionary.")

        return cls(
            **_coerce_tuple_fields(
                payload,
                (
                    "evidence_ids",
                    "evidence_paths",
                    "citations",
                ),
            )
        )

    def write_json(self, path: str | Path) -> None:
        """Write this verdict as stable, human-readable JSON."""

        _write_json(path, self.to_dict())

    @classmethod
    def read_json(cls, path: str | Path) -> "ContextAdmissionVerdict":
        """Read a verdict from JSON."""

        return cls.from_dict(_read_json(path))
