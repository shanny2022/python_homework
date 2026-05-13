"""CSV export helpers."""

from io import StringIO
from pathlib import Path
import csv
import sqlite3


TICKET_EXPORT_FIELDS = [
    "id",
    "title",
    "description",
    "severity",
    "status",
    "assignee",
    "created_at",
    "updated_at",
    "resolved_at",
    "reopen_reason",
]


def export_tickets_csv(
    connection: sqlite3.Connection,
    path: str | Path | None = None,
    status: str | None = None,
) -> str:
    rows = _ticket_rows(connection, status=status)
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=TICKET_EXPORT_FIELDS)
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row[field] for field in TICKET_EXPORT_FIELDS})
    csv_text = output.getvalue()
    if path is not None:
        Path(path).write_text(csv_text, encoding="utf-8")
    return csv_text


def export_audit_log_csv(connection: sqlite3.Connection, path: str | Path | None = None) -> str:
    fields = ["id", "ticket_id", "user_id", "action", "field_name", "old_value", "new_value", "created_at"]
    rows = connection.execute("SELECT * FROM audit_log ORDER BY created_at, id").fetchall()
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row[field] for field in fields})
    csv_text = output.getvalue()
    if path is not None:
        Path(path).write_text(csv_text, encoding="utf-8")
    return csv_text


def _ticket_rows(connection: sqlite3.Connection, status: str | None = None) -> list[sqlite3.Row]:
    if status:
        return connection.execute(
            "SELECT * FROM tickets WHERE status = ? ORDER BY id",
            (status,),
        ).fetchall()
    return connection.execute("SELECT * FROM tickets ORDER BY id").fetchall()
