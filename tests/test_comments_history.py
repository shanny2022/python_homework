import pytest

from app.audit_log import list_events
from app.comments import add_comment, edit_comment, list_comments
from app.database import create_connection, initialize_database
from app.history import activity_feed, ticket_history
from app.tickets import create_ticket
from app.users import create_user


@pytest.fixture
def seeded():
    database = create_connection()
    initialize_database(database)
    admin = create_user(database, "admin", "correct horse", "admin", "Admin User")
    agent = create_user(database, "maya", "correct horse", "agent", "Maya Chen")
    ticket = create_ticket(database, "Commentable ticket", "This ticket needs discussion.", "medium", "Maya Chen")
    return database, admin, agent, ticket


def test_add_comment_records_audit_event(seeded):
    connection, _, agent, ticket = seeded

    comment = add_comment(connection, ticket.id, agent, "I can reproduce this.")

    assert comment.body == "I can reproduce this."
    assert list_events(connection, ticket_id=ticket.id)[0].action == "comment.created"


def test_agent_cannot_create_internal_comment(seeded):
    connection, _, agent, ticket = seeded

    with pytest.raises(PermissionError):
        add_comment(connection, ticket.id, agent, "Admin eyes only", internal=True)


def test_admin_can_create_internal_comment_hidden_from_public_list(seeded):
    connection, admin, _, ticket = seeded

    add_comment(connection, ticket.id, admin, "Escalating to security.", internal=True)

    assert list_comments(connection, ticket.id) == []
    assert len(list_comments(connection, ticket.id, include_internal=True)) == 1


def test_edit_comment_by_author_updates_body_and_history(seeded):
    connection, _, agent, ticket = seeded
    comment = add_comment(connection, ticket.id, agent, "Initial note")

    edited = edit_comment(connection, comment.id, agent, "Updated note")

    assert edited.body == "Updated note"
    assert edited.edited_at is not None
    assert [event.action for event in ticket_history(connection, ticket.id)] == [
        "comment.created",
        "comment.edited",
    ]


def test_agent_cannot_edit_someone_elses_comment(seeded):
    connection, admin, _, ticket = seeded
    other = create_user(connection, "iris", "correct horse", "agent", "Iris Patel")
    comment = add_comment(connection, ticket.id, admin, "Owner note")

    with pytest.raises(PermissionError):
        edit_comment(connection, comment.id, other, "Takeover edit")


def test_activity_feed_returns_newest_events_first(seeded):
    connection, admin, agent, ticket = seeded
    add_comment(connection, ticket.id, agent, "First note")
    add_comment(connection, ticket.id, admin, "Second note")

    feed = activity_feed(connection, limit=1)

    assert len(feed) == 1
    assert feed[0].user_id == admin.id
