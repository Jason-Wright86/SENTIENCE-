"""Memory boundary for SENTIENCE.

The initial phase defines the contract without providing persistence.
"""

from abc import ABC, abstractmethod
from typing import Any


class MemoryStore(ABC):
    """Abstract boundary for future memory implementations."""

    @abstractmethod
    def remember(self, experience: Any) -> None:
        """Store an experience."""
        raise NotImplementedError

    @abstractmethod
    def recall(self, query: Any) -> list[Any]:
        """Retrieve relevant experiences."""
        raise NotImplementedError
