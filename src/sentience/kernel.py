"""Minimal cognitive kernel for SENTIENCE Phase 1."""

from .state import CognitiveState


class CognitiveKernel:
    """Owns the initial shared cognitive state and deterministic cycle."""

    def __init__(self) -> None:
        self.state = CognitiveState()

    def cycle(self) -> CognitiveState:
        """Advance one observable cognitive cycle and return a state snapshot."""
        self.state.advance_cycle()
        return self.state
