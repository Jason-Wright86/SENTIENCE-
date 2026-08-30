"""Tests for persistent episodic memory."""

from sentience.memory import EpisodicMemoryRecord, SQLiteMemoryStore


def test_memory_survives_store_reopen(tmp_path) -> None:
    database = tmp_path / "sentience.db"
    record = EpisodicMemoryRecord(
        content={"event": "first persistent experience"},
        context={"source": "test"},
        importance=0.8,
        confidence=0.9,
    )

    with SQLiteMemoryStore(database) as store:
        store.remember(record)

    with SQLiteMemoryStore(database) as reopened:
        restored = reopened.get(record.memory_id)

    assert restored == record


def test_recent_memories_survive_reopen(tmp_path) -> None:
    database = tmp_path / "sentience.db"
    first = EpisodicMemoryRecord(content="first")
    second = EpisodicMemoryRecord(content="second")

    with SQLiteMemoryStore(database) as store:
        store.remember(first)
        store.remember(second)

    with SQLiteMemoryStore(database) as reopened:
        recent = reopened.recent(2)

    assert {item.memory_id for item in recent} == {first.memory_id, second.memory_id}
