"""Analytics and reporting queries for ticket operations."""

from collections import defaultdict
from datetime import datetime
import sqlite3


def ticket_trends(connection: sqlite3.Connection, bucket: str = "day") -> dict[str, int]:
    if bucket not in {"day", "month"}:
        raise ValueError("bucket must be day or month")
    date_expr = "substr(created_at, 1, 10)" if bucket == "day" else "substr(created_at, 1, 7)"
    rows = connection.execute(
        f"""
        SELECT {date_expr} AS bucket, COUNT(*) AS total
        FROM tickets
        GROUP BY {date_expr}
        ORDER BY bucket
        """
    ).fetchall()
    return {row["bucket"]: row["total"] for row in rows}


def severity_breakdown(connection: sqlite3.Connection) -> dict[str, int]:
    rows = connection.execute(
        """
        SELECT severity, COUNT(*) AS total
        FROM tickets
        GROUP BY severity
        ORDER BY severity
        """
    ).fetchall()
    return {row["severity"]: row["total"] for row in rows}


def average_resolution_hours(connection: sqlite3.Connection) -> float:
    rows = connection.execute(
        """
        SELECT created_at, resolved_at
        FROM tickets
        WHERE resolved_at IS NOT NULL
        """
    ).fetchall()
    if not rows:
        return 0.0
    hours = []
    for row in rows:
        created_at = _parse_timestamp(row["created_at"])
        resolved_at = _parse_timestamp(row["resolved_at"])
        hours.append((resolved_at - created_at).total_seconds() / 3600)
    return round(sum(hours) / len(hours), 2)


def resolution_hours_by_severity(connection: sqlite3.Connection) -> dict[str, float]:
    rows = connection.execute(
        """
        SELECT severity, created_at, resolved_at
        FROM tickets
        WHERE resolved_at IS NOT NULL
        """
    ).fetchall()
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        created_at = _parse_timestamp(row["created_at"])
        resolved_at = _parse_timestamp(row["resolved_at"])
        grouped[row["severity"]].append((resolved_at - created_at).total_seconds() / 3600)
    return {severity: round(sum(values) / len(values), 2) for severity, values in grouped.items()}


def agent_performance(connection: sqlite3.Connection) -> list[dict[str, object]]:
    rows = connection.execute(
        """
        SELECT
            assignee,
            COUNT(*) AS total_tickets,
            SUM(CASE WHEN status IN ('resolved', 'closed') THEN 1 ELSE 0 END) AS resolved_tickets,
            SUM(CASE WHEN status IN ('open', 'in_progress') THEN 1 ELSE 0 END) AS active_tickets,
            MIN(created_at) AS first_ticket_at,
            MAX(updated_at) AS last_update_at
        FROM tickets
        GROUP BY assignee
        ORDER BY resolved_tickets DESC, total_tickets DESC, assignee
        """
    ).fetchall()
    return [
        {
            "assignee": row["assignee"],
            "total_tickets": row["total_tickets"],
            "resolved_tickets": row["resolved_tickets"] or 0,
            "active_tickets": row["active_tickets"] or 0,
            "first_ticket_at": row["first_ticket_at"],
            "last_update_at": row["last_update_at"],
        }
        for row in rows
    ]


def backlog_by_agent(connection: sqlite3.Connection) -> dict[str, int]:
    rows = connection.execute(
        """
        SELECT assignee, COUNT(*) AS total
        FROM tickets
        WHERE status IN ('open', 'in_progress')
        GROUP BY assignee
        ORDER BY assignee
        """
    ).fetchall()
    return {row["assignee"]: row["total"] for row in rows}


def _parse_timestamp(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
