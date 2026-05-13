"""SQLite database setup and row mapping."""

import sqlite3
from pathlib import Path

from .models import Ticket


def create_connection(database_path: str | Path = ":memory:") -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            assignee TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            resolved_at TEXT,
            reopen_reason TEXT
        )
        """
    )
    connection.commit()


def row_to_ticket(row: sqlite3.Row | None) -> Ticket | None:
    if row is None:
        return None

    return Ticket(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        severity=row["severity"],
        status=row["status"],
        assignee=row["assignee"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        resolved_at=row["resolved_at"],
        reopen_reason=row["reopen_reason"],
    )
