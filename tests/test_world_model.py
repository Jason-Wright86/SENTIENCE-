"""Tests for the initial SENTIENCE world model."""

import pytest

from sentience.world_model import WorldModelState


def test_world_model_starts_empty() -> None:
    model = WorldModelState()
    snapshot = model.snapshot()

    assert snapshot["observations"] == []
    assert snapshot["beliefs"] == {}
    assert snapshot["version"] == 0


def test_observation_preserves_source_and_confidence() -> None:
    model = WorldModelState()

    observation = model.observe(
        "The room is dark.",
        source="user",
        confidence=0.92,
        context={"channel": "conversation"},
    )

    assert observation.source == "user"
    assert observation.confidence == 0.92
    assert observation.context["channel"] == "conversation"
    assert model.version == 1


def test_belief_is_separate_from_observation() -> None:
    model = WorldModelState()
    model.observe("It is raining.", source="user", confidence=0.8)
    model.set_belief("weather.raining", True)

    assert len(model.observations) == 1
    assert model.beliefs["weather.raining"] is True
    assert model.version == 2


def test_observations_can_be_filtered_by_source() -> None:
    model = WorldModelState()
    first = model.observe("A", source="sensor")
    model.observe("B", source="user")
    second = model.observe("C", source="sensor")

    assert model.observations_from("sensor") == [first, second]


def test_invalid_observation_confidence_is_rejected() -> None:
    model = WorldModelState()

    with pytest.raises(ValueError):
        model.observe("bad", source="user", confidence=1.1)


def test_empty_sources_and_belief_keys_are_rejected() -> None:
    model = WorldModelState()

    with pytest.raises(ValueError):
        model.observe("bad", source="   ")

    with pytest.raises(ValueError):
        model.set_belief("   ", True)
