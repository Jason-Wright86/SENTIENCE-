"""Tests for the initial SENTIENCE cognitive kernel."""

from sentience.kernel import CognitiveKernel


def test_kernel_starts_initialized() -> None:
    kernel = CognitiveKernel()

    assert kernel.state.cycle_count == 0
    assert kernel.state.status == "initialized"


def test_cycle_advances_observable_state() -> None:
    kernel = CognitiveKernel()

    state = kernel.cycle()

    assert state.cycle_count == 1
    assert state.status == "running"
    assert state.updated_at >= state.created_at
