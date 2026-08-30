"""World-model boundary for SENTIENCE."""

from abc import ABC, abstractmethod
from typing import Any


class WorldModel(ABC):
    """Abstract representation of the modeled external environment."""

    @abstractmethod
    def observe(self, observation: Any) -> None:
        """Ingest an observation into a future world-model implementation."""
        raise NotImplementedError

    @abstractmethod
    def snapshot(self) -> dict[str, Any]:
        """Return an observable world-model snapshot."""
        raise NotImplementedError
