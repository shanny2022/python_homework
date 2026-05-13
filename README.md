# CaseFlow QA Tracker

CaseFlow QA Tracker is a Python-based internal issue tracking tool for small support and QA teams. It allows teams to create tickets, validate issue details, search records, import CSV data, and generate basic status reports.

## Features

- Create and update support tickets
- Get tickets by ID
- Assign tickets to team members
- Validate ticket title, description, severity, and status
- Search tickets by keyword, status, severity, or assignee
- Import ticket records from CSV files
- Skip invalid CSV rows during import
- Generate summary reports for open and resolved issues
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
│   ├── tickets.py
│   ├── search.py
│   ├── reports.py
│   └── importers.py
├── tests/
│   ├── test_tickets.py
│   ├── test_validation.py
│   ├── test_search.py
│   ├── test_reports.py
│   └── test_importers.py
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
