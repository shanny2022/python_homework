"""Ticket comment workflows."""

import sqlite3

from .audit_log import record_event
from .database import row_to_comment
from .models import Comment, User
from .permissions import require_permission
from .tickets import get_ticket_by_id
from .validators import normalize_text


def add_comment(
    connection: sqlite3.Connection,
    ticket_id: int,
    user: User,
    body: str,
    internal: bool = False,
) -> Comment:
    if get_ticket_by_id(connection, ticket_id) is None:
        raise LookupError(f"ticket {ticket_id} was not found")
    require_permission(user, "comment:create")
    if internal:
        require_permission(user, "comment:internal")
    clean_body = normalize_text(body)
    if len(clean_body) < 2:
        raise ValueError("comment body must be at least 2 characters")

    cursor = connection.execute(
        """
        INSERT INTO comments (ticket_id, user_id, body, internal)
        VALUES (?, ?, ?, ?)
        """,
        (ticket_id, user.id, clean_body, int(internal)),
    )
    record_event(connection, "comment.created", ticket_id=ticket_id, user_id=user.id)
    connection.commit()

    comment = get_comment(connection, cursor.lastrowid)
    if comment is None:
        raise RuntimeError("comment was not created")
    return comment


def get_comment(connection: sqlite3.Connection, comment_id: int) -> Comment | None:
    row = connection.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
    return row_to_comment(row)


def list_comments(
    connection: sqlite3.Connection,
    ticket_id: int,
    include_internal: bool = False,
) -> list[Comment]:
    if include_internal:
        rows = connection.execute(
            "SELECT * FROM comments WHERE ticket_id = ? ORDER BY created_at, id",
            (ticket_id,),
        ).fetchall()
    else:
        rows = connection.execute(
            """
            SELECT * FROM comments
            WHERE ticket_id = ? AND internal = 0
            ORDER BY created_at, id
            """,
            (ticket_id,),
        ).fetchall()
    return [comment for row in rows if (comment := row_to_comment(row)) is not None]


def edit_comment(
    connection: sqlite3.Connection,
    comment_id: int,
    user: User,
    body: str,
) -> Comment:
    comment = get_comment(connection, comment_id)
    if comment is None:
        raise LookupError(f"comment {comment_id} was not found")
    if comment.user_id != user.id:
        require_permission(user, "comment:edit_any")
    clean_body = normalize_text(body)
    if len(clean_body) < 2:
        raise ValueError("comment body must be at least 2 characters")

    connection.execute(
        """
        UPDATE comments
        SET body = ?, edited_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (clean_body, comment_id),
    )
    record_event(
        connection,
        "comment.edited",
        ticket_id=comment.ticket_id,
        user_id=user.id,
        field_name="body",
        old_value=comment.body,
        new_value=clean_body,
    )
    connection.commit()
    updated = get_comment(connection, comment_id)
    if updated is None:
        raise RuntimeError("comment was not updated")
    return updated
