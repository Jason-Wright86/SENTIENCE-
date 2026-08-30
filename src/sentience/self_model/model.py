"""Initial self-model implementation for SENTIENCE."""

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class SelfModelState:
    """Structured, observable representation of the system's current self-model."""

    identity: dict[str, Any] = field(default_factory=dict)
    capabilities: dict[str, Any] = field(default_factory=dict)
    limitations: dict[str, Any] = field(default_factory=dict)
    goals: dict[str, Any] = field(default_factory=dict)
    beliefs: dict[str, Any] = field(default_factory=dict)
    uncertainties: dict[str, Any] = field(default_factory=dict)
    state: dict[str, Any] = field(default_factory=dict)
    version: int = 0
    updated_at: datetime = field(default_factory=utc_now)

    def update(self, section: str, values: dict[str, Any]) -> None:
        """Merge values into one approved self-model section and increment its version."""
        sections = {
            "identity": self.identity,
            "capabilities": self.capabilities,
            "limitations": self.limitations,
            "goals": self.goals,
            "beliefs": self.beliefs,
            "uncertainties": self.uncertainties,
            "state": self.state,
        }
        if section not in sections:
            raise ValueError(f"unknown self-model section: {section}")
        sections[section].update(values)
        self.version += 1
        self.updated_at = utc_now()

    def snapshot(self) -> dict[str, Any]:
        """Return a detached snapshot suitable for observation or logging."""
        return {
            "identity": deepcopy(self.identity),
            "capabilities": deepcopy(self.capabilities),
            "limitations": deepcopy(self.limitations),
            "goals": deepcopy(self.goals),
            "beliefs": deepcopy(self.beliefs),
            "uncertainties": deepcopy(self.uncertainties),
            "state": deepcopy(self.state),
            "version": self.version,
            "updated_at": self.updated_at,
        }
