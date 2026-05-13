"""User management for CaseFlow accounts."""

import sqlite3

from .auth import hash_password
from .database import row_to_user
from .models import VALID_ROLES, User
from .validators import normalize_choice, normalize_text


def create_user(
    connection: sqlite3.Connection,
    username: str,
    password: str,
    role: str = "agent",
    display_name: str | None = None,
) -> User:
    clean_username = normalize_text(username).lower()
    clean_role = normalize_choice(role)
    clean_display_name = normalize_text(display_name or username)
    _validate_user_input(clean_username, password, clean_role, clean_display_name)

    password_hash, salt = hash_password(password)
    try:
        cursor = connection.execute(
            """
            INSERT INTO users (username, display_name, role, password_hash, password_salt)
            VALUES (?, ?, ?, ?, ?)
            """,
            (clean_username, clean_display_name, clean_role, password_hash, salt),
        )
    except sqlite3.IntegrityError as exc:
        raise ValueError("username already exists") from exc
    connection.commit()

    user = get_user_by_id(connection, cursor.lastrowid)
    if user is None:
        raise RuntimeError("user was not created")
    return user


def get_user_by_id(connection: sqlite3.Connection, user_id: int) -> User | None:
    row = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return row_to_user(row)


def get_user_by_username(connection: sqlite3.Connection, username: str) -> User | None:
    row = connection.execute(
        "SELECT * FROM users WHERE username = ?", (normalize_text(username).lower(),)
    ).fetchone()
    return row_to_user(row)


def list_users(
    connection: sqlite3.Connection,
    role: str | None = None,
    active_only: bool = True,
) -> list[User]:
    clauses: list[str] = []
    params: list[str | int] = []
    if role:
        clauses.append("role = ?")
        params.append(normalize_choice(role))
    if active_only:
        clauses.append("active = 1")

    sql = "SELECT * FROM users"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY username"
    rows = connection.execute(sql, params).fetchall()
    return [user for row in rows if (user := row_to_user(row)) is not None]


def deactivate_user(connection: sqlite3.Connection, user_id: int) -> User:
    if get_user_by_id(connection, user_id) is None:
        raise LookupError(f"user {user_id} was not found")
    connection.execute("UPDATE users SET active = 0 WHERE id = ?", (user_id,))
    connection.execute("UPDATE sessions SET active = 0 WHERE user_id = ?", (user_id,))
    connection.commit()
    user = get_user_by_id(connection, user_id)
    if user is None:
        raise RuntimeError("user was not deactivated")
    return user


def change_user_role(connection: sqlite3.Connection, user_id: int, role: str) -> User:
    clean_role = normalize_choice(role)
    if clean_role not in VALID_ROLES:
        raise ValueError("role must be admin or agent")
    if get_user_by_id(connection, user_id) is None:
        raise LookupError(f"user {user_id} was not found")
    connection.execute("UPDATE users SET role = ? WHERE id = ?", (clean_role, user_id))
    connection.commit()
    user = get_user_by_id(connection, user_id)
    if user is None:
        raise RuntimeError("user role was not updated")
    return user


def _validate_user_input(username: str, password: str, role: str, display_name: str) -> None:
    errors: list[str] = []
    if len(username) < 3:
        errors.append("username must be at least 3 characters")
    if " " in username:
        errors.append("username cannot contain spaces")
    if len(password) < 8:
        errors.append("password must be at least 8 characters")
    if role not in VALID_ROLES:
        errors.append("role must be admin or agent")
    if not display_name:
        errors.append("display name is required")
    if errors:
        raise ValueError("; ".join(errors))
