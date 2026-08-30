"""Tests for the provider-independent reasoning layer."""

import pytest

from sentience.reasoning import DeterministicReasoner, ReasoningRequest, Reasoner


def test_request_requires_a_question() -> None:
    with pytest.raises(ValueError):
        ReasoningRequest("   ")


def test_reasoner_implements_provider_independent_interface() -> None:
    reasoner = DeterministicReasoner()
    assert isinstance(reasoner, Reasoner)


def test_deterministic_reasoner_returns_structured_result() -> None:
    request = ReasoningRequest(
        "What should be investigated next?",
        context={"topic": "test"},
        evidence=("evidence-1", "evidence-2"),
        goals=("goal-1",),
    )
    result = DeterministicReasoner().reason(request)

    assert "What should be investigated next?" in result.conclusion
    assert result.evidence_used == ("evidence-1", "evidence-2")
    assert result.alternatives == ("goal-1",)
    assert result.metadata["reasoner"] == "DeterministicReasoner"
    assert result.metadata["evidence_count"] == 2
    assert result.confidence == 0.7
    assert result.uncertainty == 0.3


def test_reasoning_result_rejects_invalid_scores() -> None:
    from sentience.reasoning import ReasoningResult

    with pytest.raises(ValueError):
        ReasoningResult("bad", confidence=1.1, uncertainty=0.0)

    with pytest.raises(ValueError):
        ReasoningResult("bad", confidence=0.0, uncertainty=-0.1)
