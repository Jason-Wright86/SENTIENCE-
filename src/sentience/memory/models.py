"""Data models used by SENTIENCE memory systems."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class EpisodicMemoryRecord:
    """An immutable record describing one stored experience."""

    content: Any
    timestamp: datetime = field(default_factory=utc_now)
    memory_id: UUID = field(default_factory=uuid4)
    context: dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.importance <= 1.0:
            raise ValueError("importance must be between 0.0 and 1.0")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
