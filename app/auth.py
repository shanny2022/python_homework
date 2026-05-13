"""Authentication and session helpers."""

from datetime import UTC, datetime, timedelta
import hashlib
import hmac
import secrets
import sqlite3

from .database import row_to_session
from .models import Session, User


SESSION_HOURS = 8


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000)
    return digest.hex(), salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    candidate, _ = hash_password(password, salt)
    return hmac.compare_digest(candidate, password_hash)


def login(connection: sqlite3.Connection, username: str, password: str) -> Session:
    from .users import get_user_by_username

    user = get_user_by_username(connection, username)
    if user is None or not user.active:
        raise PermissionError("invalid username or password")
    if not verify_password(password, user.password_hash, user.password_salt):
        raise PermissionError("invalid username or password")

    token = secrets.token_urlsafe(32)
    expires_at = (_utcnow() + timedelta(hours=SESSION_HOURS)).isoformat(timespec="seconds")
    connection.execute(
        """
        INSERT INTO sessions (token, user_id, expires_at)
        VALUES (?, ?, ?)
        """,
        (token, user.id, expires_at),
    )
    connection.commit()
    session = get_session(connection, token)
    if session is None:
        raise RuntimeError("session was not created")
    return session


def get_session(connection: sqlite3.Connection, token: str) -> Session | None:
    row = connection.execute("SELECT * FROM sessions WHERE token = ?", (token,)).fetchone()
    return row_to_session(row)


def get_current_user(connection: sqlite3.Connection, token: str) -> User | None:
    from .users import get_user_by_id

    session = get_session(connection, token)
    if session is None or not session.active:
        return None
    if _is_expired(session.expires_at):
        connection.execute("UPDATE sessions SET active = 0 WHERE token = ?", (token,))
        connection.commit()
        return None
    user = get_user_by_id(connection, session.user_id)
    if user is None or not user.active:
        return None
    return user


def require_login(connection: sqlite3.Connection, token: str) -> User:
    user = get_current_user(connection, token)
    if user is None:
        raise PermissionError("a valid session is required")
    return user


def logout(connection: sqlite3.Connection, token: str) -> None:
    connection.execute("UPDATE sessions SET active = 0 WHERE token = ?", (token,))
    connection.commit()


def _is_expired(expires_at: str) -> bool:
    try:
        return datetime.fromisoformat(expires_at) <= _utcnow()
    except ValueError:
        return True


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)
