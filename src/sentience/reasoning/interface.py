"""Provider-independent reasoner interface."""

from abc import ABC, abstractmethod

from .models import ReasoningRequest, ReasoningResult


class Reasoner(ABC):
    """Abstract reasoning service used by the SENTIENCE architecture."""

    @abstractmethod
    def reason(self, request: ReasoningRequest) -> ReasoningResult:
        """Produce a structured reasoning result for a request."""
        raise NotImplementedError
