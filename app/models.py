"""Application data models."""

from dataclasses import dataclass


VALID_SEVERITIES = {"low", "medium", "high", "critical"}
VALID_STATUSES = {"open", "in_progress", "resolved", "closed"}
VALID_ROLES = {"admin", "agent"}


@dataclass(frozen=True)
class Ticket:
    id: int
    title: str
    description: str
    severity: str
    status: str
    assignee: str
    created_at: str
    updated_at: str
    resolved_at: str | None = None
    reopen_reason: str | None = None

    @property
    def is_open(self) -> bool:
        return self.status != "closed"


@dataclass(frozen=True)
class User:
    id: int
    username: str
    display_name: str
    role: str
    password_hash: str
    password_salt: str
    active: bool
    created_at: str

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


@dataclass(frozen=True)
class Session:
    token: str
    user_id: int
    created_at: str
    expires_at: str
    active: bool


@dataclass(frozen=True)
class Comment:
    id: int
    ticket_id: int
    user_id: int
    body: str
    internal: bool
    created_at: str
    edited_at: str | None = None


@dataclass(frozen=True)
class AuditEvent:
    id: int
    ticket_id: int | None
    user_id: int | None
    action: str
    field_name: str | None
    old_value: str | None
    new_value: str | None
    created_at: str


@dataclass(frozen=True)
class Notification:
    id: int
    user_id: int | None
    role: str | None
    ticket_id: int | None
    message: str
    read_at: str | None
    created_at: str
