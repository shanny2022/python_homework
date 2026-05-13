"""Notification storage and delivery helpers."""

import sqlite3

from .database import row_to_notification
from .models import Notification
from .validators import normalize_choice, normalize_text


def create_notification(
    connection: sqlite3.Connection,
    message: str,
    user_id: int | None = None,
    role: str | None = None,
    ticket_id: int | None = None,
) -> Notification:
    clean_message = normalize_text(message)
    if not clean_message:
        raise ValueError("notification message is required")
    clean_role = normalize_choice(role) if role else None
    cursor = connection.execute(
        """
        INSERT INTO notifications (user_id, role, ticket_id, message)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, clean_role, ticket_id, clean_message),
    )
    connection.commit()
    notification = get_notification(connection, cursor.lastrowid)
    if notification is None:
        raise RuntimeError("notification was not created")
    return notification


def get_notification(connection: sqlite3.Connection, notification_id: int) -> Notification | None:
    row = connection.execute("SELECT * FROM notifications WHERE id = ?", (notification_id,)).fetchone()
    return row_to_notification(row)


def list_notifications(
    connection: sqlite3.Connection,
    user_id: int | None = None,
    role: str | None = None,
    unread_only: bool = False,
) -> list[Notification]:
    clauses: list[str] = []
    params: list[object] = []
    if user_id is not None:
        clauses.append("(user_id = ? OR user_id IS NULL)")
        params.append(user_id)
    if role:
        clauses.append("(role = ? OR role IS NULL)")
        params.append(normalize_choice(role))
    if unread_only:
        clauses.append("read_at IS NULL")
    sql = "SELECT * FROM notifications"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY created_at, id"
    rows = connection.execute(sql, params).fetchall()
    return [note for row in rows if (note := row_to_notification(row)) is not None]


def mark_notification_read(connection: sqlite3.Connection, notification_id: int) -> Notification:
    if get_notification(connection, notification_id) is None:
        raise LookupError(f"notification {notification_id} was not found")
    connection.execute(
        "UPDATE notifications SET read_at = CURRENT_TIMESTAMP WHERE id = ?",
        (notification_id,),
    )
    connection.commit()
    notification = get_notification(connection, notification_id)
    if notification is None:
        raise RuntimeError("notification was not updated")
    return notification
