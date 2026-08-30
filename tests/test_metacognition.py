"""Tests for the initial metacognitive monitor."""

import pytest

from sentience.metacognition import MetacognitiveMonitor


def test_monitor_starts_empty() -> None:
    monitor = MetacognitiveMonitor()
    assert len(monitor) == 0
    assert monitor.assessments() == []


def test_assessment_records_confidence_uncertainty_and_evidence() -> None:
    monitor = MetacognitiveMonitor()
    assessment = monitor.assess(
        "observation A",
        confidence=0.7,
        uncertainty=0.3,
        evidence=("source A",),
        alternatives=("alternative A",),
        notes=("needs review",),
    )

    assert len(monitor) == 1
    assert assessment.event == "observation A"
    assert assessment.confidence == 0.7
    assert assessment.uncertainty == 0.3
    assert assessment.evidence == ("source A",)
    assert assessment.alternatives == ("alternative A",)
    assert assessment.notes == ("needs review",)


def test_recent_returns_newest_first() -> None:
    monitor = MetacognitiveMonitor()
    first = monitor.assess("first", confidence=0.9, uncertainty=0.1)
    second = monitor.assess("second", confidence=0.4, uncertainty=0.6)

    assert monitor.recent(1) == [second]
    assert monitor.recent(2) == [second, first]
    assert monitor.recent(0) == []


def test_uncertain_filters_by_threshold() -> None:
    monitor = MetacognitiveMonitor()
    certain = monitor.assess("certain", confidence=0.9, uncertainty=0.1)
    uncertain = monitor.assess("uncertain", confidence=0.4, uncertainty=0.8)

    assert monitor.uncertain(0.5) == [uncertain]
    assert monitor.uncertain(0.1) == [certain, uncertain]


def test_invalid_ranges_are_rejected() -> None:
    monitor = MetacognitiveMonitor()

    with pytest.raises(ValueError):
        monitor.assess("bad", confidence=1.1, uncertainty=0.0)

    with pytest.raises(ValueError):
        monitor.assess("bad", confidence=0.0, uncertainty=-0.1)

    with pytest.raises(ValueError):
        monitor.uncertain(1.1)


def test_assessment_collections_are_immutable_tuples() -> None:
    monitor = MetacognitiveMonitor()
    assessment = monitor.assess(
        "event", confidence=0.5, uncertainty=0.5, evidence=("e",)
    )

    assert isinstance(assessment.evidence, tuple)
    assert isinstance(assessment.alternatives, tuple)
    assert isinstance(assessment.notes, tuple)
