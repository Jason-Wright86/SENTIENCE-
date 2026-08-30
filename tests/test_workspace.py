"""Integration tests for the SENTIENCE cognitive workspace."""

from sentience.cognition import CognitiveWorkspace


def test_workspace_integrates_core_subsystems() -> None:
    workspace = CognitiveWorkspace()

    result = workspace.cycle("an initial observation", source="test", confidence=0.9)

    assert result.cycle_count == 1
    assert result.observation == "an initial observation"
    assert len(result.relevant_memories) == 1
    assert result.world_snapshot["observations"]
    assert result.self_snapshot["version"] == 0


def test_workspace_preserves_state_across_cycles() -> None:
    workspace = CognitiveWorkspace()

    first = workspace.cycle("first", source="test")
    second = workspace.cycle("second", source="test")

    assert first.cycle_count == 1
    assert second.cycle_count == 2
    assert len(workspace.memory) == 2
    assert len(workspace.world_model.observations) == 2
