import pytest

from app.database import create_connection, initialize_database
from app.search import filter_by_severity, filter_by_status, search_tickets
from app.tickets import create_ticket


@pytest.fixture
def connection():
    database = create_connection()
    initialize_database(database)
    create_ticket(
        database,
        "Login form rejects valid users",
        "Customers cannot sign in with valid credentials.",
        "high",
        "Maya Chen",
    )
    create_ticket(
        database,
        "CSV export drops notes",
        "Downloaded exports are missing the final notes column.",
        "medium",
        "Iris Patel",
        status="in_progress",
    )
    return database


def test_search_finds_matching_title_and_description(connection):
    assert [ticket.title for ticket in search_tickets(connection, "login")] == [
        "Login form rejects valid users"
    ]
    assert [ticket.title for ticket in search_tickets(connection, "notes column")] == [
        "CSV export drops notes"
    ]


def test_filter_by_severity(connection):
    tickets = filter_by_severity(connection, "medium")

    assert len(tickets) == 1
    assert tickets[0].assignee == "Iris Patel"


def test_filter_by_status(connection):
    tickets = filter_by_status(connection, "in progress")

    assert len(tickets) == 1
    assert tickets[0].severity == "medium"
