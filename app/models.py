"""Application data models."""

from dataclasses import dataclass


VALID_SEVERITIES = {"low", "medium", "high", "critical"}
VALID_STATUSES = {"open", "in_progress", "resolved", "closed"}


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
