"""Deterministic local reasoner used to validate the architecture."""

from .interface import Reasoner
from .models import ReasoningRequest, ReasoningResult


class DeterministicReasoner(Reasoner):
    """A dependency-free reasoner with predictable behavior for tests."""

    def reason(self, request: ReasoningRequest) -> ReasoningResult:
        """Return a transparent conclusion without an external AI provider."""
        evidence_count = len(request.evidence)
        confidence = min(0.5 + 0.1 * evidence_count, 0.9)
        uncertainty = round(1.0 - confidence, 10)
        return ReasoningResult(
            conclusion=f"Processed question: {request.question}",
            confidence=confidence,
            uncertainty=uncertainty,
            evidence_used=tuple(request.evidence),
            alternatives=tuple(request.goals),
            metadata={"reasoner": self.__class__.__name__, "evidence_count": evidence_count},
        )
