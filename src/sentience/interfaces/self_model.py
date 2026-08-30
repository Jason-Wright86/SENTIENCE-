"""Self-model boundary for SENTIENCE."""

from abc import ABC, abstractmethod
from typing import Any


class SelfModel(ABC):
    """Abstract representation of the system's model of itself."""

    @abstractmethod
    def snapshot(self) -> dict[str, Any]:
        """Return an observable self-model snapshot."""
        raise NotImplementedError
