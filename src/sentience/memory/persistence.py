"""SQLite persistence for SENTIENCE episodic memories."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from .models import EpisodicMemoryRecord


class SQLiteMemoryStore:
    """Persist episodic memories in a local SQLite database."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS episodic_memories (
                memory_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                content TEXT NOT NULL,
                context TEXT NOT NULL,
                importance REAL NOT NULL,
                confidence REAL NOT NULL
            )
            """
        )
        self._connection.commit()

    def remember(self, record: EpisodicMemoryRecord) -> None:
        """Persist one memory record."""
        self._connection.execute(
            """
            INSERT INTO episodic_memories
            (memory_id, timestamp, content, context, importance, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(record.memory_id),
                record.timestamp.isoformat(),
                json.dumps(record.content),
                json.dumps(record.context),
                record.importance,
                record.confidence,
            ),
        )
        self._connection.commit()

    def get(self, memory_id: UUID) -> EpisodicMemoryRecord | None:
        """Retrieve one persisted memory by identifier."""
        row = self._connection.execute(
            "SELECT * FROM episodic_memories WHERE memory_id = ?",
            (str(memory_id),),
        ).fetchone()
        return self._row_to_record(row) if row else None

    def recent(self, limit: int = 10) -> list[EpisodicMemoryRecord]:
        """Return persisted memories newest first."""
        if limit < 0:
            raise ValueError("limit must not be negative")
        rows = self._connection.execute(
            "SELECT * FROM episodic_memories ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def close(self) -> None:
        """Close the database connection."""
        self._connection.close()

    def __enter__(self) -> "SQLiteMemoryStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> EpisodicMemoryRecord:
        return EpisodicMemoryRecord(
            memory_id=UUID(row["memory_id"]),
            timestamp=datetime.fromisoformat(row["timestamp"]),
            content=json.loads(row["content"]),
            context=json.loads(row["context"]),
            importance=row["importance"],
            confidence=row["confidence"],
        )
