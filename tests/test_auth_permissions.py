from datetime import UTC, datetime, timedelta

import pytest

from app.auth import get_current_user, login, logout
from app.database import create_connection, initialize_database
from app.permissions import has_permission, require_ticket_permission
from app.tickets import create_ticket
from app.users import change_user_role, create_user, deactivate_user, get_user_by_username, list_users


@pytest.fixture
def connection():
    database = create_connection()
    initialize_database(database)
    return database


def test_create_user_hashes_password_and_normalizes_role(connection):
    user = create_user(connection, "Maya", "correct horse", "Admin", "Maya Chen")

    assert user.username == "maya"
    assert user.role == "admin"
    assert user.password_hash != "correct horse"
    assert len(user.password_salt) > 10


def test_duplicate_username_is_rejected(connection):
    create_user(connection, "maya", "correct horse", "agent", "Maya Chen")

    with pytest.raises(ValueError, match="username already exists"):
        create_user(connection, "MAYA", "another good password", "agent", "Maya Chen")


def test_short_password_is_rejected(connection):
    with pytest.raises(ValueError, match="password must be"):
        create_user(connection, "noor", "short", "agent", "Noor Ali")


def test_login_creates_session_and_logout_invalidates_it(connection):
    user = create_user(connection, "iris", "correct horse", "agent", "Iris Patel")

    session = login(connection, "iris", "correct horse")

    assert get_current_user(connection, session.token) == user
    logout(connection, session.token)
    assert get_current_user(connection, session.token) is None


def test_login_rejects_bad_password(connection):
    create_user(connection, "iris", "correct horse", "agent", "Iris Patel")

    with pytest.raises(PermissionError, match="invalid username or password"):
        login(connection, "iris", "wrong password")


def test_expired_session_returns_no_user(connection):
    create_user(connection, "iris", "correct horse", "agent", "Iris Patel")
    session = login(connection, "iris", "correct horse")
    expired_at = (_utcnow() - timedelta(minutes=1)).isoformat(timespec="seconds")
    connection.execute("UPDATE sessions SET expires_at = ? WHERE token = ?", (expired_at, session.token))

    assert get_current_user(connection, session.token) is None


def test_deactivated_user_cannot_keep_session(connection):
    user = create_user(connection, "iris", "correct horse", "agent", "Iris Patel")
    session = login(connection, "iris", "correct horse")

    deactivated = deactivate_user(connection, user.id)

    assert not deactivated.active
    assert get_current_user(connection, session.token) is None


def test_agent_can_update_only_assigned_ticket(connection):
    user = create_user(connection, "iris", "correct horse", "agent", "Iris Patel")
    assigned = create_ticket(connection, "Assigned bug exists", "This issue belongs to Iris.", "low", "Iris Patel")
    other = create_ticket(connection, "Other bug exists", "This issue belongs elsewhere.", "low", "Noor Ali")

    assert has_permission(user, "ticket:update", assigned)
    with pytest.raises(PermissionError):
        require_ticket_permission(connection, user, "ticket:update", other.id)


def test_admin_can_manage_users_and_change_roles(connection):
    user = create_user(connection, "noor", "correct horse", "agent", "Noor Ali")

    promoted = change_user_role(connection, user.id, "admin")

    assert promoted.role == "admin"
    assert has_permission(promoted, "user:manage")
    assert [listed.username for listed in list_users(connection, role="admin")] == ["noor"]


def test_get_user_by_username_is_case_insensitive(connection):
    user = create_user(connection, "Noor", "correct horse", "agent", "Noor Ali")

    assert get_user_by_username(connection, "NOOR") == user


def _utcnow():
    return datetime.now(UTC).replace(tzinfo=None)
