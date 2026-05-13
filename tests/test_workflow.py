from datetime import UTC, datetime, timedelta

import pytest

from app.database import create_connection, initialize_database
from app.notifications import list_notifications
from app.tickets import create_ticket, update_ticket_status
from app.users import create_user
from app.workflow import assign_next_ticket, escalate_overdue_tickets, reopen_ticket, sla_deadline, tickets_past_sla


@pytest.fixture
def connection():
    database = create_connection()
    initialize_database(database)
    create_user(database, "admin", "correct horse", "admin", "Admin User")
    create_user(database, "maya", "correct horse", "agent", "Maya Chen")
    create_user(database, "iris", "correct horse", "agent", "Iris Patel")
    return database


def test_sla_deadline_uses_severity_window(connection):
    ticket = create_ticket(connection, "Critical outage here", "A production checkout flow is down.", "critical", "Maya Chen")

    deadline = sla_deadline(ticket)

    assert deadline - datetime.strptime(ticket.created_at, "%Y-%m-%d %H:%M:%S") == timedelta(hours=4)


def test_tickets_past_sla_ignores_closed_tickets(connection):
    ticket = create_ticket(connection, "Old open ticket", "This issue has been open for too long.", "high", "Maya Chen")
    closed = create_ticket(connection, "Old closed ticket", "This issue has already been closed.", "high", "Maya Chen")
    old_created_at = (_utcnow() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    connection.execute("UPDATE tickets SET created_at = ? WHERE id IN (?, ?)", (old_created_at, ticket.id, closed.id))
    update_ticket_status(connection, closed.id, "closed")

    assert [item.id for item in tickets_past_sla(connection)] == [ticket.id]


def test_escalate_overdue_tickets_moves_to_escalation_queue_and_notifies_admin(connection):
    admin = create_user(connection, "owner", "correct horse", "admin", "Owner User")
    ticket = create_ticket(connection, "Old high ticket", "This ticket should breach the SLA clock.", "high", "Maya Chen")
    old_created_at = (_utcnow() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
    connection.execute("UPDATE tickets SET created_at = ? WHERE id = ?", (old_created_at, ticket.id))

    escalated = escalate_overdue_tickets(connection, admin)

    assert escalated[0].assignee == "Escalation Queue"
    assert escalated[0].severity == "critical"
    assert list_notifications(connection, role="admin")[0].ticket_id == ticket.id


def test_agent_cannot_escalate_overdue_tickets(connection):
    agent = create_user(connection, "noor", "correct horse", "agent", "Noor Ali")

    with pytest.raises(PermissionError):
        escalate_overdue_tickets(connection, agent)


def test_assign_next_ticket_selects_highest_priority_and_least_loaded_agent(connection):
    admin = create_user(connection, "owner", "correct horse", "admin", "Owner User")
    create_ticket(connection, "Low queue ticket", "Low severity queued ticket waits here.", "low", "unassigned")
    high = create_ticket(connection, "High queue ticket", "High severity queued ticket waits here.", "high", "unassigned")

    assigned = assign_next_ticket(connection, admin)

    assert assigned is not None
    assert assigned.id == high.id
    assert assigned.assignee == "Iris Patel"


def test_reopen_ticket_requires_assigned_agent_or_admin(connection):
    agent = create_user(connection, "noor", "correct horse", "agent", "Noor Ali")
    ticket = create_ticket(connection, "Closed owned ticket", "This ticket has a closing state.", "medium", "Maya Chen")
    update_ticket_status(connection, ticket.id, "closed")

    with pytest.raises(PermissionError):
        reopen_ticket(connection, ticket.id, agent, "Customer responded")


def test_reopen_ticket_records_reason_for_assigned_agent(connection):
    agent = create_user(connection, "maya2", "correct horse", "agent", "Maya Chen")
    ticket = create_ticket(connection, "Closed assigned ticket", "This ticket belongs to the acting agent.", "medium", "Maya Chen")
    update_ticket_status(connection, ticket.id, "closed")

    reopened = reopen_ticket(connection, ticket.id, agent, "Customer says it is still broken")

    assert reopened.status == "open"
    assert reopened.reopen_reason == "Customer says it is still broken"


def _utcnow():
    return datetime.now(UTC).replace(tzinfo=None)
