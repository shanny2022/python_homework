from app.validators import validate_ticket_input


def test_short_title_is_rejected():
    errors = validate_ticket_input(
        title="Bug",
        description="This description is long enough.",
        severity="low",
        assignee="Maya Chen",
    )

    assert "title must be at least 5 characters" in errors


def test_invalid_severity_is_rejected():
    errors = validate_ticket_input(
        title="Export bug",
        description="CSV exports fail for resolved tickets.",
        severity="urgent",
        assignee="Iris Patel",
    )

    assert "severity must be low, medium, high, or critical" in errors


def test_missing_assignee_is_rejected():
    errors = validate_ticket_input(
        title="Report bug",
        description="Status report counts do not match the queue.",
        severity="medium",
        assignee="",
    )

    assert "assignee is required" in errors
