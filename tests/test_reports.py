from app.database import create_connection, initialize_database
from app.reports import count_by_severity, count_by_status, open_ticket_count, resolved_ticket_count
from app.tickets import create_ticket, update_ticket_status


def test_report_counts_open_closed_and_in_progress_tickets_correctly():
    connection = create_connection()
    initialize_database(connection)
    create_ticket(
        connection,
        "Login form rejects valid users",
        "Customers cannot sign in with valid credentials.",
        "high",
        "Maya Chen",
    )
    create_ticket(
        connection,
        "CSV export drops notes",
        "Downloaded exports are missing the final notes column.",
        "medium",
        "Iris Patel",
        status="in_progress",
    )
    closed = create_ticket(
        connection,
        "Closed tickets show in open queue",
        "Resolved records are still visible in the open ticket queue.",
        "critical",
        "Noor Ali",
    )
    update_ticket_status(connection, closed.id, "closed")

    assert count_by_status(connection) == {"closed": 1, "in_progress": 1, "open": 1}
    assert count_by_severity(connection) == {"critical": 1, "high": 1, "medium": 1}
    assert open_ticket_count(connection) == 2
    assert resolved_ticket_count(connection) == 1
