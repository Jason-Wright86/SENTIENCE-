"""Controlled integration workspace for SENTIENCE cognitive subsystems."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..kernel import CognitiveKernel
from ..memory import EpisodicMemory
from ..reasoning import DeterministicReasoner, Reasoner, ReasoningRequest, ReasoningResult
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
    reasoning_result: ReasoningResult
    timestamp: datetime


class CognitiveWorkspace:
    """Coordinate the kernel, memory, self/world models, and reasoning layer."""

    def __init__(
        self,
        *,
        kernel: CognitiveKernel | None = None,
        memory: EpisodicMemory | None = None,
        self_model: SelfModelState | None = None,
        world_model: WorldModelState | None = None,
        reasoner: Reasoner | None = None,
    ) -> None:
        self.kernel = kernel or CognitiveKernel()
        self.memory = memory or EpisodicMemory()
        self.self_model = self_model or SelfModelState()
        self.world_model = world_model or WorldModelState()
        self.reasoner = reasoner or DeterministicReasoner()

    def cycle(
        self,
        observation: Any,
        *,
        source: str = "unknown",
        confidence: float = 1.0,
        goals: tuple[Any, ...] = (),
    ) -> CognitiveCycleResult:
        """Process one observation through the integrated cognitive workspace."""
        self.kernel.cycle()
        world_observation = self.world_model.observe(
            observation, source=source, confidence=confidence
        )
        self.memory.remember(
            observation,
            context={"source": source, "world_observation_id": str(world_observation.observation_id)},
            confidence=confidence,
        )

        relevant_memories = tuple(self.memory.recall(observation))
        self_snapshot = self.self_model.snapshot()
        world_snapshot = self.world_model.snapshot()
        request = ReasoningRequest(
            question=str(observation),
            context={
                "observation": observation,
                "source": source,
                "confidence": confidence,
                "self_model": self_snapshot,
                "world_model": world_snapshot,
            },
            evidence=relevant_memories,
            goals=tuple(goals),
        )
        reasoning_result = self.reasoner.reason(request)

        return CognitiveCycleResult(
            cycle_count=self.kernel.state.cycle_count,
            observation=observation,
            relevant_memories=relevant_memories,
            self_snapshot=self_snapshot,
            world_snapshot=world_snapshot,
            reasoning_result=reasoning_result,
            timestamp=self.kernel.state.updated_at,
        )
