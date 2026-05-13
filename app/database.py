"""SQLite database setup and row mapping."""

import sqlite3
from pathlib import Path

from .models import AuditEvent, Comment, Notification, Session, Ticket, User


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
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            display_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'agent')),
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            body TEXT NOT NULL,
            internal INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            edited_at TEXT,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER,
            user_id INTEGER,
            action TEXT NOT NULL,
            field_name TEXT,
            old_value TEXT,
            new_value TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            ticket_id INTEGER,
            message TEXT NOT NULL,
            read_at TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (ticket_id) REFERENCES tickets(id)
        )
        """
    )
    connection.execute("CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_comments_ticket ON comments(ticket_id)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_audit_ticket ON audit_log(ticket_id)")
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


def row_to_user(row: sqlite3.Row | None) -> User | None:
    if row is None:
        return None
    return User(
        id=row["id"],
        username=row["username"],
        display_name=row["display_name"],
        role=row["role"],
        password_hash=row["password_hash"],
        password_salt=row["password_salt"],
        active=bool(row["active"]),
        created_at=row["created_at"],
    )


def row_to_session(row: sqlite3.Row | None) -> Session | None:
    if row is None:
        return None
    return Session(
        token=row["token"],
        user_id=row["user_id"],
        created_at=row["created_at"],
        expires_at=row["expires_at"],
        active=bool(row["active"]),
    )


def row_to_comment(row: sqlite3.Row | None) -> Comment | None:
    if row is None:
        return None
    return Comment(
        id=row["id"],
        ticket_id=row["ticket_id"],
        user_id=row["user_id"],
        body=row["body"],
        internal=bool(row["internal"]),
        created_at=row["created_at"],
        edited_at=row["edited_at"],
    )


def row_to_audit_event(row: sqlite3.Row | None) -> AuditEvent | None:
    if row is None:
        return None
    return AuditEvent(
        id=row["id"],
        ticket_id=row["ticket_id"],
        user_id=row["user_id"],
        action=row["action"],
        field_name=row["field_name"],
        old_value=row["old_value"],
        new_value=row["new_value"],
        created_at=row["created_at"],
    )


def row_to_notification(row: sqlite3.Row | None) -> Notification | None:
    if row is None:
        return None
    return Notification(
        id=row["id"],
        user_id=row["user_id"],
        role=row["role"],
        ticket_id=row["ticket_id"],
        message=row["message"],
        read_at=row["read_at"],
        created_at=row["created_at"],
    )
