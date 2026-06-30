from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4
import json


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ResearchSession:
    """
    Persistent boundary for a research activity.

    A ResearchSession is the unit that connects participants,
    artifacts, events, and future memory/context packs.
    """

    title: str
    session_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    participants: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    def add_participant(self, participant_id: str) -> None:
        """Attach a participant to this session."""
        if participant_id not in self.participants:
            self.participants.append(participant_id)

    def add_artifact(self, artifact_id: str) -> None:
        """Attach an artifact to this session."""
        if artifact_id not in self.artifacts:
            self.artifacts.append(artifact_id)

    def add_event(self, event_type: str, content: str) -> None:
        """Record an event in the session timeline."""
        self.events.append(
            {
                "timestamp": utc_now_iso(),
                "type": event_type,
                "content": content,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize session to a dictionary."""
        return asdict(self)

    def save(self, path: Path) -> None:
        """Save session as JSON."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> "ResearchSession":
        """Load session from JSON."""
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**data)
