"""Initial evidence-aware world model for SENTIENCE."""

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Observation:
    """A report about the environment, explicitly preserving its source and confidence."""

    content: Any
    source: str
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=utc_now)
    observation_id: UUID = field(default_factory=uuid4)
    context: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not self.source.strip():
            raise ValueError("source must not be empty")


@dataclass
class WorldModelState:
    """Evidence-aware, observable representation of the modeled environment."""

    observations: list[Observation] = field(default_factory=list)
    beliefs: dict[str, Any] = field(default_factory=dict)
    version: int = 0
    updated_at: datetime = field(default_factory=utc_now)

    def observe(
        self,
        content: Any,
        *,
        source: str,
        confidence: float = 1.0,
        context: dict[str, Any] | None = None,
    ) -> Observation:
        """Record an observation without treating it as unquestioned fact."""
        observation = Observation(
            content=content,
            source=source,
            confidence=confidence,
            context={} if context is None else dict(context),
        )
        self.observations.append(observation)
        self.version += 1
        self.updated_at = utc_now()
        return observation

    def set_belief(self, key: str, value: Any) -> None:
        """Set a modeled belief separately from the observations supporting it."""
        if not key.strip():
            raise ValueError("belief key must not be empty")
        self.beliefs[key] = value
        self.version += 1
        self.updated_at = utc_now()

    def observations_from(self, source: str) -> list[Observation]:
        """Return observations attributed to one source."""
        return [item for item in self.observations if item.source == source]

    def snapshot(self) -> dict[str, Any]:
        """Return a detached snapshot for inspection or logging."""
        return {
            "observations": deepcopy(self.observations),
            "beliefs": deepcopy(self.beliefs),
            "version": self.version,
            "updated_at": self.updated_at,
        }
