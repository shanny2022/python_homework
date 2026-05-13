# CaseFlow QA Tracker

CaseFlow QA Tracker is a Python-based internal issue tracking tool for small support and QA teams. It allows teams to manage tickets, users, workflow rules, comments, audit history, CSV operations, and operational reporting.

## Features

- Create and update support tickets
- Get tickets by ID
- Assign tickets to team members
- Create users with admin and agent roles
- Log in, create sessions, and enforce role-based permissions
- Apply ticket workflow rules for SLA deadlines, escalation, reopening, and assignment queues
- Add ticket comments, internal notes, change history, and activity feeds
- Validate ticket title, description, severity, and status
- Search tickets by keyword, status, severity, or assignee
- Import ticket records from CSV files
- Export tickets and audit logs to CSV
- Apply batch status/assignment updates
- Detect and clean up duplicate tickets
- Skip invalid CSV rows during import
- Generate dashboard, analytics, severity, resolution-time, and agent-performance reports
- Run tests with pytest

## Tech Stack

- Python
- SQLite
- Pytest
- Pandas

## Project Structure

```text
caseflow-qa-tracker/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── validators.py
│   ├── users.py
│   ├── auth.py
│   ├── permissions.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── notifications.py
│   ├── comments.py
│   ├── audit_log.py
│   ├── history.py
│   ├── search.py
│   ├── reports.py
│   ├── analytics.py
│   ├── dashboard.py
│   ├── importers.py
│   ├── exporters.py
│   └── bulk_update.py
├── tests/
│   ├── test_tickets.py
│   ├── test_validation.py
│   ├── test_search.py
│   ├── test_reports.py
│   ├── test_importers.py
│   ├── test_auth_permissions.py
│   ├── test_workflow.py
│   ├── test_comments_history.py
│   └── test_analytics_export_bulk.py
├── data/
│   └── sample_tickets.csv
├── README.md
├── requirements.txt
├── pyproject.toml
├── Dockerfile
└── .gitignore
```

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -vs
```

## Run with Docker

```bash
docker build -t caseflow-qa-tracker .
docker run --rm caseflow-qa-tracker
```

## Possible Silver Tasks

- Fix search so it matches title and description, not just title
- Add validation so severity only allows low, medium, high, and critical
- Fix CSV import so invalid rows are skipped instead of crashing
- Add report logic to count open, closed, and in-progress tickets correctly
- Fix ticket status update so resolved tickets cannot be reopened without a reason
- Repair role-based access so agents cannot bulk-update queues
- Prevent stale sessions from authenticating deactivated users
- Fix broken SLA escalation logic for high-priority tickets
- Add pagination to ticket search and dashboard tables
- Repair duplicate ticket detection for punctuation and Unicode differences
- Fix CSV update handling for malformed IDs and mixed encodings
- Optimize slow dashboard queries for large ticket queues
- Fix audit log ordering when many events share the same timestamp
