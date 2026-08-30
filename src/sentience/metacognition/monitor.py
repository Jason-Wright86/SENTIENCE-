"""Initial metacognitive monitoring for SENTIENCE."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class CognitiveAssessment:
    """A structured assessment of one cognitive event."""

    event: Any
    confidence: float
    uncertainty: float
    evidence: tuple[Any, ...] = ()
    alternatives: tuple[Any, ...] = ()
    notes: tuple[str, ...] = ()
    timestamp: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not 0.0 <= self.uncertainty <= 1.0:
            raise ValueError("uncertainty must be between 0.0 and 1.0")


class MetacognitiveMonitor:
    """Record and inspect structured assessments of cognitive events."""

    def __init__(self) -> None:
        self._assessments: list[CognitiveAssessment] = []

    def assess(
        self,
        event: Any,
        *,
        confidence: float,
        uncertainty: float,
        evidence: tuple[Any, ...] = (),
        alternatives: tuple[Any, ...] = (),
        notes: tuple[str, ...] = (),
    ) -> CognitiveAssessment:
        """Create and record an assessment of a cognitive event."""
        assessment = CognitiveAssessment(
            event=event,
            confidence=confidence,
            uncertainty=uncertainty,
            evidence=tuple(evidence),
            alternatives=tuple(alternatives),
            notes=tuple(notes),
        )
        self._assessments.append(assessment)
        return assessment

    def assessments(self) -> list[CognitiveAssessment]:
        """Return assessments in chronological insertion order."""
        return list(self._assessments)

    def recent(self, limit: int = 10) -> list[CognitiveAssessment]:
        """Return the newest assessments first."""
        if limit < 0:
            raise ValueError("limit must not be negative")
        return list(reversed(self._assessments[-limit:])) if limit else []

    def uncertain(self, threshold: float = 0.5) -> list[CognitiveAssessment]:
        """Return assessments whose uncertainty meets or exceeds a threshold."""
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0.0 and 1.0")
        return [a for a in self._assessments if a.uncertainty >= threshold]

    def __len__(self) -> int:
        return len(self._assessments)
