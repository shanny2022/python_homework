"""Ticket workflow rules for SLA, reopen, escalation, and queues."""

from datetime import UTC, datetime, timedelta
import sqlite3

from .audit_log import record_event
from .database import row_to_ticket
from .history import compare_tickets
from .models import Ticket, User
from .notifications import create_notification
from .permissions import require_permission, require_ticket_permission
from .tickets import assign_ticket, get_ticket_by_id, update_ticket_status


SLA_HOURS = {
    "critical": 4,
    "high": 12,
    "medium": 48,
    "low": 96,
}


def sla_deadline(ticket: Ticket) -> datetime:
    return _parse_timestamp(ticket.created_at) + timedelta(hours=SLA_HOURS[ticket.severity])


def tickets_past_sla(connection: sqlite3.Connection, now: datetime | None = None) -> list[Ticket]:
    current = now or _utcnow()
    rows = connection.execute(
        """
        SELECT * FROM tickets
        WHERE status IN ('open', 'in_progress')
        ORDER BY created_at, id
        """
    ).fetchall()
    tickets = [ticket for row in rows if (ticket := row_to_ticket(row)) is not None]
    return [ticket for ticket in tickets if sla_deadline(ticket) < current]


def escalate_overdue_tickets(
    connection: sqlite3.Connection,
    actor: User,
    now: datetime | None = None,
) -> list[Ticket]:
    require_permission(actor, "ticket:assign")
    escalated: list[Ticket] = []
    for ticket in tickets_past_sla(connection, now=now):
        old_assignee = ticket.assignee
        new_severity = "critical" if ticket.severity == "high" else ticket.severity
        connection.execute(
            """
            UPDATE tickets
            SET assignee = 'Escalation Queue',
                severity = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (new_severity, ticket.id),
        )
        record_event(
            connection,
            "ticket.escalated",
            ticket_id=ticket.id,
            user_id=actor.id,
            field_name="assignee",
            old_value=old_assignee,
            new_value="Escalation Queue",
        )
        create_notification(
            connection,
            f"Ticket {ticket.id} breached SLA and was escalated",
            role="admin",
            ticket_id=ticket.id,
        )
        updated = get_ticket_by_id(connection, ticket.id)
        if updated is not None:
            escalated.append(updated)
    connection.commit()
    return escalated


def can_reopen(ticket: Ticket, actor: User, now: datetime | None = None, max_closed_days: int = 30) -> bool:
    if ticket.status not in {"resolved", "closed"}:
        return False
    if actor.role == "admin":
        return True
    if ticket.assignee.lower() != actor.display_name.lower():
        return False
    if ticket.resolved_at is None:
        return True
    current = now or _utcnow()
    return current - _parse_timestamp(ticket.resolved_at) <= timedelta(days=max_closed_days)


def reopen_ticket(
    connection: sqlite3.Connection,
    ticket_id: int,
    actor: User,
    reason: str,
    now: datetime | None = None,
) -> Ticket:
    ticket = require_ticket_permission(connection, actor, "ticket:reopen", ticket_id)
    if not can_reopen(ticket, actor, now=now):
        raise PermissionError("ticket cannot be reopened by this user")
    updated = update_ticket_status(connection, ticket_id, "open", reason=reason)
    for field_name, values in compare_tickets(ticket, updated).items():
        record_event(
            connection,
            "ticket.reopened",
            ticket_id=ticket_id,
            user_id=actor.id,
            field_name=field_name,
            old_value=values[0],
            new_value=values[1],
        )
    return updated


def assign_next_ticket(
    connection: sqlite3.Connection,
    actor: User,
    queue: str = "unassigned",
) -> Ticket | None:
    require_permission(actor, "ticket:assign")
    agent = _least_loaded_agent(connection)
    if agent is None:
        raise LookupError("no active agents are available")
    row = connection.execute(
        """
        SELECT * FROM tickets
        WHERE status = 'open' AND LOWER(assignee) = LOWER(?)
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                ELSE 4
            END,
            created_at,
            id
        LIMIT 1
        """,
        (queue,),
    ).fetchone()
    ticket = row_to_ticket(row)
    if ticket is None:
        return None
    updated = assign_ticket(connection, ticket.id, agent["display_name"])
    record_event(
        connection,
        "ticket.assigned_from_queue",
        ticket_id=ticket.id,
        user_id=actor.id,
        field_name="assignee",
        old_value=ticket.assignee,
        new_value=updated.assignee,
    )
    return updated


def transition_ticket(
    connection: sqlite3.Connection,
    ticket_id: int,
    actor: User,
    status: str,
    reason: str | None = None,
) -> Ticket:
    ticket = require_ticket_permission(connection, actor, "ticket:update", ticket_id)
    updated = update_ticket_status(connection, ticket_id, status, reason=reason)
    for field_name, values in compare_tickets(ticket, updated).items():
        record_event(
            connection,
            "ticket.changed",
            ticket_id=ticket_id,
            user_id=actor.id,
            field_name=field_name,
            old_value=values[0],
            new_value=values[1],
        )
    return updated


def _least_loaded_agent(connection: sqlite3.Connection) -> sqlite3.Row | None:
    return connection.execute(
        """
        SELECT users.id, users.display_name, COUNT(tickets.id) AS open_count
        FROM users
        LEFT JOIN tickets
            ON LOWER(tickets.assignee) = LOWER(users.display_name)
            AND tickets.status IN ('open', 'in_progress')
        WHERE users.role = 'agent' AND users.active = 1
        GROUP BY users.id
        ORDER BY open_count, users.display_name
        LIMIT 1
        """
    ).fetchone()


def _parse_timestamp(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)
