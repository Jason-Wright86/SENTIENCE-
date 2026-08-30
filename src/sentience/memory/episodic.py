"""Initial in-memory episodic memory implementation."""

from typing import Any
from uuid import UUID

from .models import EpisodicMemoryRecord


class EpisodicMemory:
    """Store and retrieve experiences for the current process.

    This is intentionally an in-memory Phase 1 implementation. Persistent
    storage will be introduced only after the memory contract is validated.
    """

    def __init__(self) -> None:
        self._records: list[EpisodicMemoryRecord] = []

    def remember(
        self,
        content: Any,
        *,
        context: dict[str, Any] | None = None,
        importance: float = 0.5,
        confidence: float = 1.0,
    ) -> EpisodicMemoryRecord:
        """Create and store an episodic memory record."""
        record = EpisodicMemoryRecord(
            content=content,
            context={} if context is None else dict(context),
            importance=importance,
            confidence=confidence,
        )
        self._records.append(record)
        return record

    def recall(self, query: Any | None = None) -> list[EpisodicMemoryRecord]:
        """Return stored records, optionally matching simple content equality."""
        if query is None:
            return list(self._records)
        return [record for record in self._records if record.content == query]

    def recent(self, limit: int = 10) -> list[EpisodicMemoryRecord]:
        """Return up to ``limit`` most recently stored records."""
        if limit < 0:
            raise ValueError("limit must not be negative")
        if limit == 0:
            return []
        return list(reversed(self._records[-limit:]))

    def get(self, memory_id: UUID) -> EpisodicMemoryRecord | None:
        """Return one memory by identifier, or ``None`` if it is absent."""
        return next((record for record in self._records if record.memory_id == memory_id), None)

    def __len__(self) -> int:
        return len(self._records)
