"""Tests for the initial SENTIENCE self-model."""

import pytest

from sentience.self_model import SelfModelState


def test_self_model_starts_empty_and_version_zero() -> None:
    model = SelfModelState()
    snapshot = model.snapshot()

    assert snapshot["identity"] == {}
    assert snapshot["capabilities"] == {}
    assert snapshot["version"] == 0


def test_update_changes_the_selected_section_and_version() -> None:
    model = SelfModelState()
    model.update("identity", {"name": "SENTIENCE"})
    model.update("capabilities", {"python": True})

    assert model.identity == {"name": "SENTIENCE"}
    assert model.capabilities == {"python": True}
    assert model.version == 2


def test_snapshot_is_detached_from_internal_state() -> None:
    model = SelfModelState()
    model.update("beliefs", {"example": {"confidence": 0.5}})

    snapshot = model.snapshot()
    snapshot["beliefs"]["example"]["confidence"] = 1.0

    assert model.beliefs["example"]["confidence"] == 0.5


def test_unknown_section_is_rejected() -> None:
    model = SelfModelState()

    with pytest.raises(ValueError):
        model.update("unknown", {"value": True})
