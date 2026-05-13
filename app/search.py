"""Search and filtering support."""

import sqlite3

from .database import row_to_ticket
from .models import Ticket
from .validators import normalize_choice, normalize_text


def search_tickets(
    connection: sqlite3.Connection,
    keyword: str = "",
    status: str | None = None,
    severity: str | None = None,
    assignee: str | None = None,
) -> list[Ticket]:
    clauses: list[str] = []
    params: list[str] = []

    clean_keyword = normalize_text(keyword)
    if clean_keyword:
        clauses.append("(LOWER(title) LIKE ? OR LOWER(description) LIKE ?)")
        keyword_param = f"%{clean_keyword.lower()}%"
        params.extend([keyword_param, keyword_param])

    if status:
        clauses.append("status = ?")
        params.append(normalize_choice(status))

    if severity:
        clauses.append("severity = ?")
        params.append(normalize_choice(severity))

    if assignee:
        clauses.append("LOWER(assignee) = ?")
        params.append(normalize_text(assignee).lower())

    sql = "SELECT * FROM tickets"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY id"

    rows = connection.execute(sql, params).fetchall()
    return [ticket for row in rows if (ticket := row_to_ticket(row)) is not None]


def filter_by_severity(connection: sqlite3.Connection, severity: str) -> list[Ticket]:
    return search_tickets(connection, severity=severity)


def filter_by_status(connection: sqlite3.Connection, status: str) -> list[Ticket]:
    return search_tickets(connection, status=status)
