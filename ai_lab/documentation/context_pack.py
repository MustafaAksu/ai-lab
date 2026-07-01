from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import re


class ContextPackError(ValueError):
    """Raised when a context pack manifest is malformed or invalid."""


VALID_CONTEXT_ITEM_TYPES = {
    "artifact_summary",
    "l0_summary",
    "chunk_reference",
    "raw_chunk",
    "raw_artifact",
    "abstraction",
    "synthesis",
    "comparison",
}

VALID_ASSEMBLY_POLICIES = {
    "manual",
    "latest_context",
    "lineage",
    "semantic",
    "hybrid",
}

VALID_EXCLUSION_REASONS = {
    "duplicate",
    "low_relevance",
    "stale",
    "too_large",
    "redacted",
    "policy",
    "superseded",
}


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _validate_identifier(value: str, field_name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9._:/@|+-]+", value):
        raise ContextPackError(f"{field_name} contains unsupported characters.")


def _validate_short_text(value: str, field_name: str, max_length: int = 500) -> None:
    if not value.strip():
        raise ContextPackError(f"{field_name} must not be empty.")

    if len(value) > max_length:
        raise ContextPackError(f"{field_name} must be <= {max_length} characters.")


def compute_manifest_id(
    task: str,
    assembly_policy: str,
    item_ids: tuple[str, ...],
) -> str:
    """Compute a deterministic manifest ID from task, policy, and selected item IDs."""
    payload = "|".join((task.strip(), assembly_policy, *item_ids))
    return sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class ContextPackItem:
    """One selected item inside a context pack."""

    item_type: str
    item_id: str
    reason: str
    relevance_score: float
    token_estimate: int = 0
    source_path: str | None = None
    citation: str | None = None

    def __post_init__(self) -> None:
        if self.item_type not in VALID_CONTEXT_ITEM_TYPES:
            raise ContextPackError(f"Unsupported context item type: {self.item_type}")

        _validate_identifier(self.item_id, "item_id")
        _validate_short_text(self.reason, "reason", max_length=240)

        if not (0 <= self.relevance_score <= 1):
            raise ContextPackError("relevance_score must be between 0 and 1.")

        if self.token_estimate < 0:
            raise ContextPackError("token_estimate must be >= 0.")

        if self.source_path:
            _validate_identifier(self.source_path, "source_path")

        if self.citation:
            _validate_identifier(self.citation, "citation")

    def to_dict(self) -> dict[str, object]:
        """Serialize the context item into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "item_type": self.item_type,
            "item_id": self.item_id,
            "reason": self.reason,
            "relevance_score": self.relevance_score,
            "token_estimate": self.token_estimate,
        }

        if self.source_path:
            data["source_path"] = self.source_path

        if self.citation:
            data["citation"] = self.citation

        return data


@dataclass(frozen=True)
class ContextPackExclusion:
    """One candidate item excluded from a context pack."""

    item_id: str
    reason: str
    note: str | None = None

    def __post_init__(self) -> None:
        _validate_identifier(self.item_id, "exclusion.item_id")

        if self.reason not in VALID_EXCLUSION_REASONS:
            raise ContextPackError(f"Unsupported exclusion reason: {self.reason}")

        if self.note:
            _validate_short_text(self.note, "exclusion.note", max_length=240)

    def to_dict(self) -> dict[str, object]:
        """Serialize the exclusion into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "item_id": self.item_id,
            "reason": self.reason,
        }

        if self.note:
            data["note"] = self.note

        return data


@dataclass(frozen=True)
class ContextPackManifest:
    """
    Manifest describing the exact context selected for one task.

    This is the bridge between memory retrieval and prompt construction.
    """

    task: str
    assembly_policy: str
    items: tuple[ContextPackItem, ...]
    manifest_id: str | None = None
    token_budget: int | None = None
    exclusions: tuple[ContextPackExclusion, ...] = field(default_factory=tuple)
    created_at: str = field(default_factory=utc_now_iso)
    model_target: str | None = None
    pipeline_run_id: str | None = None

    def __post_init__(self) -> None:
        _validate_short_text(self.task, "task", max_length=500)

        if self.assembly_policy not in VALID_ASSEMBLY_POLICIES:
            raise ContextPackError(f"Unsupported assembly policy: {self.assembly_policy}")

        if not self.items:
            raise ContextPackError("Context pack must contain at least one item.")

        if self.token_budget is not None and self.token_budget < 0:
            raise ContextPackError("token_budget must be >= 0.")

        if self.model_target:
            _validate_identifier(self.model_target, "model_target")

        if self.pipeline_run_id:
            _validate_identifier(self.pipeline_run_id, "pipeline_run_id")

        expected_manifest_id = compute_manifest_id(
            task=self.task,
            assembly_policy=self.assembly_policy,
            item_ids=tuple(item.item_id for item in self.items),
        )

        if self.manifest_id is not None and self.manifest_id != expected_manifest_id:
            raise ContextPackError("manifest_id does not match task/policy/items.")

        object.__setattr__(self, "manifest_id", expected_manifest_id)

    @property
    def total_token_estimate(self) -> int:
        """Return the total estimated token cost of selected items."""
        return sum(item.token_estimate for item in self.items)

    def to_dict(self) -> dict[str, object]:
        """Serialize the manifest into a JSON-compatible dictionary."""
        data: dict[str, object] = {
            "manifest_id": self.manifest_id,
            "task": self.task,
            "assembly_policy": self.assembly_policy,
            "items": [item.to_dict() for item in self.items],
            "exclusions": [exclusion.to_dict() for exclusion in self.exclusions],
            "total_token_estimate": self.total_token_estimate,
            "created_at": self.created_at,
        }

        if self.token_budget is not None:
            data["token_budget"] = self.token_budget

        if self.model_target:
            data["model_target"] = self.model_target

        if self.pipeline_run_id:
            data["provenance"] = {
                "pipeline_run_id": self.pipeline_run_id,
            }

        return data
