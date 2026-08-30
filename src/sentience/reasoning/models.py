"""Data contracts for SENTIENCE reasoning."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ReasoningRequest:
    """Structured input presented to a reasoner."""

    question: str
    context: dict[str, Any] = field(default_factory=dict)
    evidence: tuple[Any, ...] = ()
    goals: tuple[Any, ...] = ()

    def __post_init__(self) -> None:
        if not self.question.strip():
            raise ValueError("question must not be empty")


@dataclass(frozen=True)
class ReasoningResult:
    """Structured output produced by a reasoner."""

    conclusion: Any
    confidence: float
    uncertainty: float
    evidence_used: tuple[Any, ...] = ()
    alternatives: tuple[Any, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not 0.0 <= self.uncertainty <= 1.0:
            raise ValueError("uncertainty must be between 0.0 and 1.0")
