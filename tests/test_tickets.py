import pytest

from app.database import create_connection, initialize_database
from app.tickets import assign_ticket, create_ticket, get_ticket_by_id, update_ticket_status


@pytest.fixture
def connection():
    database = create_connection()
    initialize_database(database)
    return database


def test_create_ticket_saves_title_and_severity(connection):
    ticket = create_ticket(
        connection,
        title="Login fails for valid users",
        description="Customers cannot sign in with valid credentials.",
        severity="high",
        assignee="Maya Chen",
    )

    assert ticket.id == 1
    assert ticket.title == "Login fails for valid users"
    assert ticket.severity == "high"
    assert ticket.status == "open"


def test_get_ticket_by_id_returns_saved_ticket(connection):
    created = create_ticket(
        connection,
        "CSV export drops a column",
        "The exported CSV file is missing the notes column.",
        "medium",
        "Iris Patel",
    )

    found = get_ticket_by_id(connection, created.id)

    assert found == created


def test_assigned_user_can_be_updated(connection):
    ticket = create_ticket(
        connection,
        "Dashboard total is stale",
        "The open issue count does not refresh after updates.",
        "low",
        "Noor Ali",
    )

    updated = assign_ticket(connection, ticket.id, "Jordan Lee")

    assert updated.assignee == "Jordan Lee"


def test_status_cannot_be_changed_to_invalid_value(connection):
    ticket = create_ticket(
        connection,
        "Search misses descriptions",
        "Keyword search checks titles but ignores descriptions.",
        "critical",
        "Maya Chen",
    )

    with pytest.raises(ValueError, match="status must be"):
        update_ticket_status(connection, ticket.id, "waiting")


def test_resolved_ticket_cannot_be_reopened_without_reason(connection):
    ticket = create_ticket(
        connection,
        "Resolved issue reappears",
        "A resolved support issue appears again in open queues.",
        "high",
        "Maya Chen",
    )
    update_ticket_status(connection, ticket.id, "closed")

    with pytest.raises(ValueError, match="requires a reason"):
        update_ticket_status(connection, ticket.id, "open")

    reopened = update_ticket_status(connection, ticket.id, "open", reason="Customer confirmed recurrence")
    assert reopened.status == "open"
    assert reopened.reopen_reason == "Customer confirmed recurrence"
