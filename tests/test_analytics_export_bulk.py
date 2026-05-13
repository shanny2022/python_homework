import csv

import pytest

from app.analytics import agent_performance, average_resolution_hours, backlog_by_agent, severity_breakdown, ticket_trends
from app.bulk_update import apply_csv_updates, batch_assign, batch_update_status, cleanup_duplicate_tickets, find_duplicate_tickets
from app.dashboard import agent_dashboard, dashboard_summary
from app.database import create_connection, initialize_database
from app.exporters import export_tickets_csv
from app.search import search_tickets
from app.tickets import create_ticket, update_ticket_status
from app.users import create_user


@pytest.fixture
def seeded(tmp_path):
    database = create_connection()
    initialize_database(database)
    admin = create_user(database, "admin", "correct horse", "admin", "Admin User")
    agent = create_user(database, "maya", "correct horse", "agent", "Maya Chen")
    first = create_ticket(database, "Login form error", "Valid users cannot sign in today.", "high", "Maya Chen")
    second = create_ticket(database, "Export column issue", "CSV exports are missing a column.", "medium", "Iris Patel")
    third = create_ticket(database, "Export column issue", "CSV exports are missing a column.", "medium", "Iris Patel")
    update_ticket_status(database, first.id, "closed")
    return database, admin, agent, first, second, third, tmp_path


def test_ticket_trends_and_severity_breakdown_include_seeded_data(seeded):
    connection, *_ = seeded

    trends = ticket_trends(connection)

    assert sum(trends.values()) == 3
    assert severity_breakdown(connection) == {"high": 1, "medium": 2}


def test_average_resolution_hours_returns_float_for_resolved_tickets(seeded):
    connection, *_ = seeded

    assert isinstance(average_resolution_hours(connection), float)
    assert average_resolution_hours(connection) >= 0


def test_agent_performance_counts_active_and_resolved_work(seeded):
    connection, *_ = seeded

    performance = {row["assignee"]: row for row in agent_performance(connection)}

    assert performance["Maya Chen"]["resolved_tickets"] == 1
    assert performance["Iris Patel"]["active_tickets"] == 2


def test_dashboard_summary_combines_operational_metrics(seeded):
    connection, *_ = seeded

    summary = dashboard_summary(connection)

    assert summary["open_tickets"] == 2
    assert summary["resolved_tickets"] == 1
    assert summary["backlog_by_agent"] == {"Iris Patel": 2}


def test_agent_dashboard_filters_to_one_assignee(seeded):
    connection, *_ = seeded

    dashboard = agent_dashboard(connection, "Iris Patel")

    assert dashboard["status_counts"] == {"open": 2}


def test_export_tickets_csv_writes_header_and_rows(seeded):
    connection, *_, tmp_path = seeded
    path = tmp_path / "tickets.csv"

    csv_text = export_tickets_csv(connection, path=path)
    rows = list(csv.DictReader(csv_text.splitlines()))

    assert path.exists()
    assert rows[0]["title"] == "Login form error"
    assert len(rows) == 3


def test_batch_update_status_records_failures_without_stopping(seeded):
    connection, admin, _, _, second, _, _ = seeded

    result = batch_update_status(connection, [second.id, 999], "closed", admin)

    assert result["updated"] == [second.id]
    assert result["failed"] == {999: "ticket not found"}


def test_agent_cannot_batch_update_status(seeded):
    connection, _, agent, _, second, _, _ = seeded

    with pytest.raises(PermissionError):
        batch_update_status(connection, [second.id], "closed", agent)


def test_batch_assign_updates_multiple_tickets(seeded):
    connection, admin, _, _, second, third, _ = seeded

    result = batch_assign(connection, [second.id, third.id], "Noor Ali", admin)

    assert result == {"updated": [second.id, third.id], "failed": {}}
    assert backlog_by_agent(connection)["Noor Ali"] == 2


def test_find_duplicate_tickets_groups_matching_title_and_description(seeded):
    connection, *_, second, third, _ = seeded

    assert find_duplicate_tickets(connection) == [[second.id, third.id]]


def test_cleanup_duplicate_tickets_removes_later_duplicates(seeded):
    connection, admin, *_, third, _ = seeded

    result = cleanup_duplicate_tickets(connection, admin)

    assert result["removed"] == [third.id]
    assert len(search_tickets(connection)) == 2


def test_apply_csv_updates_reports_invalid_rows(seeded):
    connection, admin, _, _, second, _, tmp_path = seeded
    path = tmp_path / "updates.csv"
    path.write_text(f"id,status,assignee\n{second.id},in_progress,Noor Ali\nbad,closed,Noor Ali\n999,closed,Noor Ali\n")

    result = apply_csv_updates(connection, path, admin)

    assert result["applied"] == [second.id]
    assert result["failed"] == {"row 3": "id must be an integer", 999: "ticket not found"}
