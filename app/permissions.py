"""Role-based permission checks."""

import sqlite3

from .models import Ticket, User
from .tickets import get_ticket_by_id


ADMIN_PERMISSIONS = {
    "ticket:create",
    "ticket:view",
    "ticket:update",
    "ticket:assign",
    "ticket:reopen",
    "ticket:bulk_update",
    "comment:create",
    "comment:internal",
    "comment:edit_any",
    "comment:delete",
    "analytics:view",
    "export:csv",
    "user:manage",
}

AGENT_PERMISSIONS = {
    "ticket:create",
    "ticket:view",
    "ticket:update_assigned",
    "ticket:reopen_assigned",
    "comment:create",
    "analytics:view_own",
}


def has_permission(user: User, permission: str, ticket: Ticket | None = None) -> bool:
    if not user.active:
        return False
    if user.role == "admin":
        return permission in ADMIN_PERMISSIONS
    if user.role != "agent":
        return False
    if permission in AGENT_PERMISSIONS:
        return True
    if permission == "ticket:update" and ticket is not None:
        return ticket.assignee.lower() == user.display_name.lower()
    if permission == "ticket:reopen" and ticket is not None:
        return ticket.assignee.lower() == user.display_name.lower()
    return False


def require_permission(user: User, permission: str, ticket: Ticket | None = None) -> None:
    if not has_permission(user, permission, ticket):
        raise PermissionError(f"{user.role} is not allowed to {permission}")


def require_ticket_permission(
    connection: sqlite3.Connection,
    user: User,
    permission: str,
    ticket_id: int,
) -> Ticket:
    ticket = get_ticket_by_id(connection, ticket_id)
    if ticket is None:
        raise LookupError(f"ticket {ticket_id} was not found")
    require_permission(user, permission, ticket)
    return ticket
