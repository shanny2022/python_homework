"""CSV import workflow for ticket records."""

from pathlib import Path
import sqlite3

import pandas as pd

from .tickets import create_ticket
from .validators import normalize_choice


def import_tickets_from_csv(connection: sqlite3.Connection, path: str | Path) -> dict[str, int]:
    frame = pd.read_csv(path).fillna("")
    imported = 0
    skipped = 0

    for row in frame.to_dict("records"):
        try:
            ticket = create_ticket(
                connection,
                title=row.get("title", ""),
                description=row.get("description", ""),
                severity=row.get("severity", ""),
                assignee=row.get("assignee", ""),
                status=row.get("status", "open"),
            )
            if normalize_choice(row.get("status", "open")) in {"resolved", "closed"}:
                connection.execute(
                    """
                    UPDATE tickets
                    SET resolved_at = COALESCE(NULLIF(?, ''), CURRENT_TIMESTAMP)
                    WHERE id = ?
                    """,
                    (row.get("resolved_at", ""), ticket.id),
                )
                connection.commit()
            imported += 1
        except (KeyError, TypeError, ValueError):
            skipped += 1

    return {"imported": imported, "skipped": skipped}
