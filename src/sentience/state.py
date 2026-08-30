"""Core state types for the SENTIENCE cognitive kernel."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    """Return the current time as an aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class CognitiveState:
    """Minimal observable state shared by the initial cognitive kernel."""

    cycle_count: int = 0
    status: str = "initialized"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    values: dict[str, Any] = field(default_factory=dict)

    def advance_cycle(self) -> None:
        """Advance the kernel by one deterministic cognitive cycle."""
        self.cycle_count += 1
        self.status = "running"
        self.updated_at = utc_now()
