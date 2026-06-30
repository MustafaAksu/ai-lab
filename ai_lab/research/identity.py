from dataclasses import dataclass, asdict
from enum import StrEnum
from typing import Any


class IdentityKind(StrEnum):
    """Kinds of persistent identities in AI-Lab."""

    HUMAN = "human"
    AI_PEER = "ai_peer"
    TOOL = "tool"
    ORGANIZATION = "organization"
    DATASET = "dataset"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Identity:
    """
    Persistent identity in the research ontology.

    An Identity may participate in many research sessions.
    It is not the same as a provider, API client, or temporary role.
    """

    identity_id: str
    name: str
    kind: IdentityKind
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize identity to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Identity":
        """Deserialize identity from a dictionary."""
        return cls(
            identity_id=data["identity_id"],
            name=data["name"],
            kind=IdentityKind(data["kind"]),
            description=data.get("description", ""),
        )
