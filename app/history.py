"""Ticket history and activity-feed helpers."""

import sqlite3

from .audit_log import list_events, record_event
from .models import AuditEvent, Ticket, User
from .tickets import get_ticket_by_id


def record_ticket_change(
    connection: sqlite3.Connection,
    ticket_id: int,
    user: User,
    field_name: str,
    old_value: object | None,
    new_value: object | None,
) -> AuditEvent:
    if get_ticket_by_id(connection, ticket_id) is None:
        raise LookupError(f"ticket {ticket_id} was not found")
    return record_event(
        connection,
        "ticket.changed",
        ticket_id=ticket_id,
        user_id=user.id,
        field_name=field_name,
        old_value=old_value,
        new_value=new_value,
    )


def compare_tickets(before: Ticket, after: Ticket) -> dict[str, tuple[object | None, object | None]]:
    changes: dict[str, tuple[object | None, object | None]] = {}
    for field_name in ("title", "description", "severity", "status", "assignee", "reopen_reason"):
        old_value = getattr(before, field_name)
        new_value = getattr(after, field_name)
        if old_value != new_value:
            changes[field_name] = (old_value, new_value)
    return changes


def ticket_history(connection: sqlite3.Connection, ticket_id: int) -> list[AuditEvent]:
    return list_events(connection, ticket_id=ticket_id)


def activity_feed(connection: sqlite3.Connection, limit: int = 25) -> list[AuditEvent]:
    if limit < 1:
        raise ValueError("limit must be positive")
    rows = connection.execute(
        """
        SELECT * FROM audit_log
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    from .database import row_to_audit_event

    return [event for row in rows if (event := row_to_audit_event(row)) is not None]
