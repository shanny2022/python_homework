"""Summary reports for QA ticket queues."""

import sqlite3


def count_by_status(connection: sqlite3.Connection) -> dict[str, int]:
    rows = connection.execute(
        """
        SELECT status, COUNT(*) AS total
        FROM tickets
        GROUP BY status
        ORDER BY status
        """
    ).fetchall()
    return {row["status"]: row["total"] for row in rows}


def count_by_severity(connection: sqlite3.Connection) -> dict[str, int]:
    rows = connection.execute(
        """
        SELECT severity, COUNT(*) AS total
        FROM tickets
        GROUP BY severity
        ORDER BY severity
        """
    ).fetchall()
    return {row["severity"]: row["total"] for row in rows}


def open_ticket_count(connection: sqlite3.Connection) -> int:
    row = connection.execute(
        "SELECT COUNT(*) AS total FROM tickets WHERE status != 'closed'"
    ).fetchone()
    return row["total"]


def resolved_ticket_count(connection: sqlite3.Connection) -> int:
    row = connection.execute(
        "SELECT COUNT(*) AS total FROM tickets WHERE status IN ('resolved', 'closed')"
    ).fetchone()
    return row["total"]
