"""Controlled integration workspace for SENTIENCE cognitive subsystems."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..kernel import CognitiveKernel
from ..memory import EpisodicMemory
from ..self_model import SelfModelState
from ..world_model import WorldModelState


@dataclass(frozen=True)
class CognitiveCycleResult:
    """Observable result of one integrated cognitive cycle."""

    cycle_count: int
    observation: Any
    relevant_memories: tuple[Any, ...]
    self_snapshot: dict[str, Any]
    world_snapshot: dict[str, Any]
    timestamp: datetime


class CognitiveWorkspace:
    """Coordinate the initial kernel, memory, self-model, and world-model."""

    def __init__(
        self,
        *,
        kernel: CognitiveKernel | None = None,
        memory: EpisodicMemory | None = None,
        self_model: SelfModelState | None = None,
        world_model: WorldModelState | None = None,
    ) -> None:
        self.kernel = kernel or CognitiveKernel()
        self.memory = memory or EpisodicMemory()
        self.self_model = self_model or SelfModelState()
        self.world_model = world_model or WorldModelState()

    def cycle(self, observation: Any, *, source: str = "unknown", confidence: float = 1.0) -> CognitiveCycleResult:
        """Process one observation through the integrated Phase 1 workspace."""
        self.kernel.cycle()
        world_observation = self.world_model.observe(
            observation, source=source, confidence=confidence
        )
        self.memory.remember(
            observation,
            context={"source": source, "world_observation_id": str(world_observation.observation_id)},
            confidence=confidence,
        )
        return CognitiveCycleResult(
            cycle_count=self.kernel.state.cycle_count,
            observation=observation,
            relevant_memories=tuple(self.memory.recall(observation)),
            self_snapshot=self.self_model.snapshot(),
            world_snapshot=self.world_model.snapshot(),
            timestamp=self.kernel.state.updated_at,
        )
