"""Bulk update and data cleanup workflows."""

from pathlib import Path
import csv
import sqlite3

from .audit_log import record_event
from .models import User
from .permissions import require_permission
from .tickets import assign_ticket, get_ticket_by_id, update_ticket_status
from .validators import normalize_text


def batch_update_status(
    connection: sqlite3.Connection,
    ticket_ids: list[int],
    status: str,
    actor: User,
    reason: str | None = None,
) -> dict[str, object]:
    require_permission(actor, "ticket:bulk_update")
    updated: list[int] = []
    failed: dict[int, str] = {}
    for ticket_id in ticket_ids:
        before = get_ticket_by_id(connection, ticket_id)
        if before is None:
            failed[ticket_id] = "ticket not found"
            continue
        try:
            after = update_ticket_status(connection, ticket_id, status, reason=reason)
            record_event(
                connection,
                "ticket.bulk_status",
                ticket_id=ticket_id,
                user_id=actor.id,
                field_name="status",
                old_value=before.status,
                new_value=after.status,
            )
            updated.append(ticket_id)
        except (LookupError, ValueError) as exc:
            failed[ticket_id] = str(exc)
    return {"updated": updated, "failed": failed}


def batch_assign(
    connection: sqlite3.Connection,
    ticket_ids: list[int],
    assignee: str,
    actor: User,
) -> dict[str, object]:
    require_permission(actor, "ticket:assign")
    updated: list[int] = []
    failed: dict[int, str] = {}
    for ticket_id in ticket_ids:
        before = get_ticket_by_id(connection, ticket_id)
        if before is None:
            failed[ticket_id] = "ticket not found"
            continue
        try:
            after = assign_ticket(connection, ticket_id, assignee)
            record_event(
                connection,
                "ticket.bulk_assign",
                ticket_id=ticket_id,
                user_id=actor.id,
                field_name="assignee",
                old_value=before.assignee,
                new_value=after.assignee,
            )
            updated.append(ticket_id)
        except (LookupError, ValueError) as exc:
            failed[ticket_id] = str(exc)
    return {"updated": updated, "failed": failed}


def find_duplicate_tickets(connection: sqlite3.Connection) -> list[list[int]]:
    rows = connection.execute(
        """
        SELECT LOWER(TRIM(title)) AS title_key,
               LOWER(TRIM(description)) AS description_key,
               GROUP_CONCAT(id) AS ids,
               COUNT(*) AS total
        FROM tickets
        GROUP BY title_key, description_key
        HAVING total > 1
        ORDER BY MIN(id)
        """
    ).fetchall()
    groups: list[list[int]] = []
    for row in rows:
        groups.append([int(value) for value in row["ids"].split(",")])
    return groups


def cleanup_duplicate_tickets(connection: sqlite3.Connection, actor: User) -> dict[str, object]:
    require_permission(actor, "ticket:bulk_update")
    duplicate_groups = find_duplicate_tickets(connection)
    removed: list[int] = []
    for group in duplicate_groups:
        for ticket_id in group[1:]:
            connection.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
            record_event(
                connection,
                "ticket.duplicate_removed",
                ticket_id=ticket_id,
                user_id=actor.id,
                field_name="id",
                old_value=ticket_id,
                new_value=None,
            )
            removed.append(ticket_id)
    connection.commit()
    return {"groups": duplicate_groups, "removed": removed}


def apply_csv_updates(connection: sqlite3.Connection, path: str | Path, actor: User) -> dict[str, object]:
    require_permission(actor, "ticket:bulk_update")
    applied: list[int] = []
    failed: dict[int | str, str] = {}
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=2):
            raw_id = normalize_text(row.get("id", ""))
            if not raw_id.isdigit():
                failed[f"row {index}"] = "id must be an integer"
                continue
            ticket_id = int(raw_id)
            ticket = get_ticket_by_id(connection, ticket_id)
            if ticket is None:
                failed[ticket_id] = "ticket not found"
                continue
            try:
                if row.get("status"):
                    update_ticket_status(connection, ticket_id, row["status"], reason=row.get("reason") or None)
                if row.get("assignee"):
                    assign_ticket(connection, ticket_id, row["assignee"])
                record_event(connection, "ticket.csv_updated", ticket_id=ticket_id, user_id=actor.id)
                applied.append(ticket_id)
            except (LookupError, ValueError) as exc:
                failed[ticket_id] = str(exc)
    return {"applied": applied, "failed": failed}
