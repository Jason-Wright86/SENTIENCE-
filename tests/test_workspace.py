"""Integration tests for the SENTIENCE cognitive workspace."""

from sentience.cognition import CognitiveWorkspace
from sentience.reasoning import Reasoner, ReasoningRequest, ReasoningResult


class CapturingReasoner(Reasoner):
    """Test double that exposes the request sent by the workspace."""

    def __init__(self) -> None:
        self.requests: list[ReasoningRequest] = []

    def reason(self, request: ReasoningRequest) -> ReasoningResult:
        self.requests.append(request)
        return ReasoningResult(
            conclusion="captured",
            confidence=0.8,
            uncertainty=0.2,
            evidence_used=request.evidence,
            alternatives=request.goals,
        )


def test_workspace_integrates_core_subsystems() -> None:
    workspace = CognitiveWorkspace()

    result = workspace.cycle("an initial observation", source="test", confidence=0.9)

    assert result.cycle_count == 1
    assert result.observation == "an initial observation"
    assert len(result.relevant_memories) == 1
    assert result.world_snapshot["observations"]
    assert result.self_snapshot["version"] == 0
    assert result.reasoning_result.conclusion.startswith("Processed question:")


def test_workspace_preserves_state_across_cycles() -> None:
    workspace = CognitiveWorkspace()

    first = workspace.cycle("first", source="test")
    second = workspace.cycle("second", source="test")

    assert first.cycle_count == 1
    assert second.cycle_count == 2
    assert len(workspace.memory) == 2
    assert len(workspace.world_model.observations) == 2


def test_workspace_sends_observation_and_models_to_reasoner() -> None:
    reasoner = CapturingReasoner()
    workspace = CognitiveWorkspace(reasoner=reasoner)

    workspace.cycle("observe the river", source="sensor", confidence=0.7, goals=("stay safe",))

    request = reasoner.requests[0]
    assert request.question == "observe the river"
    assert request.context["observation"] == "observe the river"
    assert request.context["self_model"]["version"] == 0
    assert request.context["world_model"]["observations"]
    assert request.goals == ("stay safe",)


def test_workspace_makes_retrieved_memory_available_to_reasoner() -> None:
    reasoner = CapturingReasoner()
    workspace = CognitiveWorkspace(reasoner=reasoner)

    workspace.cycle("remember this", source="test")
    workspace.cycle("remember this", source="test")

    assert len(reasoner.requests[-1].evidence) == 2


def test_workspace_returns_reasoning_result() -> None:
    reasoner = CapturingReasoner()
    workspace = CognitiveWorkspace(reasoner=reasoner)

    result = workspace.cycle("a question")

    assert result.reasoning_result.conclusion == "captured"
    assert result.reasoning_result.confidence == 0.8
    assert result.reasoning_result.uncertainty == 0.2
