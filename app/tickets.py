"""Ticket creation and update workflows."""

import sqlite3

from .database import row_to_ticket
from .models import Ticket
from .validators import normalize_choice, normalize_text, validate_status_change, validate_ticket_input


def create_ticket(
    connection: sqlite3.Connection,
    title: str,
    description: str,
    severity: str,
    assignee: str,
    status: str = "open",
) -> Ticket:
    errors = validate_ticket_input(title, description, severity, status, assignee)
    if errors:
        raise ValueError("; ".join(errors))

    cursor = connection.execute(
        """
        INSERT INTO tickets (title, description, severity, status, assignee)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            normalize_text(title),
            normalize_text(description),
            normalize_choice(severity),
            normalize_choice(status),
            normalize_text(assignee),
        ),
    )
    connection.commit()

    ticket = get_ticket_by_id(connection, cursor.lastrowid)
    if ticket is None:
        raise RuntimeError("ticket was not created")
    return ticket


def get_ticket_by_id(connection: sqlite3.Connection, ticket_id: int) -> Ticket | None:
    row = connection.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return row_to_ticket(row)


def update_ticket_status(
    connection: sqlite3.Connection,
    ticket_id: int,
    status: str,
    reason: str | None = None,
) -> Ticket:
    ticket = get_ticket_by_id(connection, ticket_id)
    if ticket is None:
        raise LookupError(f"ticket {ticket_id} was not found")

    errors = validate_status_change(ticket, status, reason)
    if errors:
        raise ValueError("; ".join(errors))

    clean_status = normalize_choice(status)
    resolved_at_sql = "CURRENT_TIMESTAMP" if clean_status in {"resolved", "closed"} else "NULL"

    connection.execute(
        f"""
        UPDATE tickets
        SET status = ?,
            updated_at = CURRENT_TIMESTAMP,
            resolved_at = {resolved_at_sql},
            reopen_reason = ?
        WHERE id = ?
        """,
        (clean_status, normalize_text(reason) if reason else ticket.reopen_reason, ticket_id),
    )
    connection.commit()

    updated_ticket = get_ticket_by_id(connection, ticket_id)
    if updated_ticket is None:
        raise RuntimeError("ticket was not updated")
    return updated_ticket


def assign_ticket(connection: sqlite3.Connection, ticket_id: int, assignee: str) -> Ticket:
    clean_assignee = normalize_text(assignee)
    if not clean_assignee:
        raise ValueError("assignee is required")
    if get_ticket_by_id(connection, ticket_id) is None:
        raise LookupError(f"ticket {ticket_id} was not found")

    connection.execute(
        """
        UPDATE tickets
        SET assignee = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (clean_assignee, ticket_id),
    )
    connection.commit()

    updated_ticket = get_ticket_by_id(connection, ticket_id)
    if updated_ticket is None:
        raise RuntimeError("ticket assignee was not updated")
    return updated_ticket
