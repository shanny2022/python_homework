"""Dashboard composition helpers."""

import sqlite3

from .analytics import (
    agent_performance,
    average_resolution_hours,
    backlog_by_agent,
    severity_breakdown,
    ticket_trends,
)
from .reports import count_by_status, open_ticket_count, resolved_ticket_count
from .workflow import tickets_past_sla


def dashboard_summary(connection: sqlite3.Connection) -> dict[str, object]:
    return {
        "status_counts": count_by_status(connection),
        "severity_counts": severity_breakdown(connection),
        "open_tickets": open_ticket_count(connection),
        "resolved_tickets": resolved_ticket_count(connection),
        "average_resolution_hours": average_resolution_hours(connection),
        "tickets_by_day": ticket_trends(connection, bucket="day"),
        "backlog_by_agent": backlog_by_agent(connection),
        "agent_performance": agent_performance(connection),
        "sla_breaches": len(tickets_past_sla(connection)),
    }


def agent_dashboard(connection: sqlite3.Connection, assignee: str) -> dict[str, object]:
    rows = connection.execute(
        """
        SELECT status, COUNT(*) AS total
        FROM tickets
        WHERE LOWER(assignee) = LOWER(?)
        GROUP BY status
        ORDER BY status
        """,
        (assignee,),
    ).fetchall()
    overdue_ids = [
        ticket.id
        for ticket in tickets_past_sla(connection)
        if ticket.assignee.lower() == assignee.lower()
    ]
    return {
        "assignee": assignee,
        "status_counts": {row["status"]: row["total"] for row in rows},
        "overdue_ticket_ids": overdue_ids,
    }
