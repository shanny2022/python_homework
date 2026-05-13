"""Audit log persistence for user and ticket activity."""

import sqlite3

from .database import row_to_audit_event
from .models import AuditEvent
from .validators import normalize_text


def record_event(
    connection: sqlite3.Connection,
    action: str,
    ticket_id: int | None = None,
    user_id: int | None = None,
    field_name: str | None = None,
    old_value: object | None = None,
    new_value: object | None = None,
) -> AuditEvent:
    clean_action = normalize_text(action)
    if not clean_action:
        raise ValueError("audit action is required")
    cursor = connection.execute(
        """
        INSERT INTO audit_log (ticket_id, user_id, action, field_name, old_value, new_value)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ticket_id,
            user_id,
            clean_action,
            normalize_text(field_name) if field_name else None,
            str(old_value) if old_value is not None else None,
            str(new_value) if new_value is not None else None,
        ),
    )
    connection.commit()
    event = get_event(connection, cursor.lastrowid)
    if event is None:
        raise RuntimeError("audit event was not created")
    return event


def get_event(connection: sqlite3.Connection, event_id: int) -> AuditEvent | None:
    row = connection.execute("SELECT * FROM audit_log WHERE id = ?", (event_id,)).fetchone()
    return row_to_audit_event(row)


def list_events(
    connection: sqlite3.Connection,
    ticket_id: int | None = None,
    user_id: int | None = None,
    action: str | None = None,
) -> list[AuditEvent]:
    clauses: list[str] = []
    params: list[object] = []
    if ticket_id is not None:
        clauses.append("ticket_id = ?")
        params.append(ticket_id)
    if user_id is not None:
        clauses.append("user_id = ?")
        params.append(user_id)
    if action:
        clauses.append("action = ?")
        params.append(normalize_text(action))
    sql = "SELECT * FROM audit_log"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY created_at, id"
    rows = connection.execute(sql, params).fetchall()
    return [event for row in rows if (event := row_to_audit_event(row)) is not None]
