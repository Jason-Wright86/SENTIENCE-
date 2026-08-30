"""Tests for the initial episodic memory implementation."""

import pytest

from sentience.memory import EpisodicMemory


def test_memory_starts_empty() -> None:
    memory = EpisodicMemory()
    assert len(memory) == 0
    assert memory.recall() == []


def test_remember_creates_unique_timestamped_record() -> None:
    memory = EpisodicMemory()
    first = memory.remember("first experience")
    second = memory.remember("second experience")

    assert len(memory) == 2
    assert first.memory_id != second.memory_id
    assert first.timestamp.tzinfo is not None
    assert second.timestamp.tzinfo is not None


def test_recall_by_content_and_get_by_id() -> None:
    memory = EpisodicMemory()
    record = memory.remember("remember this", context={"source": "test"})

    assert memory.recall("remember this") == [record]
    assert memory.get(record.memory_id) == record
    assert memory.get(type(record.memory_id).int) is None


def test_recent_returns_newest_first() -> None:
    memory = EpisodicMemory()
    first = memory.remember("first")
    second = memory.remember("second")

    assert memory.recent(1) == [second]
    assert memory.recent(2) == [second, first]
    assert memory.recent(0) == []


def test_invalid_scores_are_rejected() -> None:
    memory = EpisodicMemory()

    with pytest.raises(ValueError):
        memory.remember("bad", importance=1.1)

    with pytest.raises(ValueError):
        memory.remember("bad", confidence=-0.1)


def test_negative_recent_limit_is_rejected() -> None:
    memory = EpisodicMemory()

    with pytest.raises(ValueError):
        memory.recent(-1)
