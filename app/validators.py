"""Validation rules for CaseFlow tickets."""

from .models import VALID_SEVERITIES, VALID_STATUSES, Ticket


def normalize_text(value: str) -> str:
    return str(value).strip()


def normalize_choice(value: str) -> str:
    return normalize_text(value).lower().replace(" ", "_")


def validate_ticket_input(
    title: str,
    description: str,
    severity: str,
    status: str = "open",
    assignee: str = "unassigned",
) -> list[str]:
    errors: list[str] = []
    clean_title = normalize_text(title)
    clean_description = normalize_text(description)
    clean_severity = normalize_choice(severity)
    clean_status = normalize_choice(status)
    clean_assignee = normalize_text(assignee)

    if len(clean_title) < 5:
        errors.append("title must be at least 5 characters")
    if len(clean_description) < 10:
        errors.append("description must be at least 10 characters")
    if clean_severity not in VALID_SEVERITIES:
        errors.append("severity must be low, medium, high, or critical")
    if clean_status not in VALID_STATUSES:
        errors.append("status must be open, in_progress, resolved, or closed")
    if not clean_assignee:
        errors.append("assignee is required")

    return errors


def validate_status_change(ticket: Ticket, new_status: str, reason: str | None = None) -> list[str]:
    clean_status = normalize_choice(new_status)
    errors: list[str] = []

    if clean_status not in VALID_STATUSES:
        errors.append("status must be open, in_progress, resolved, or closed")
    if ticket.status in {"resolved", "closed"} and clean_status in {"open", "in_progress"}:
        if not reason or not reason.strip():
            errors.append("reopening a resolved or closed ticket requires a reason")

    return errors
