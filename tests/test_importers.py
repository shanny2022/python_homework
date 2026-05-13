from pathlib import Path

from app.database import create_connection, initialize_database
from app.importers import import_tickets_from_csv
from app.search import search_tickets


def test_csv_import_skips_invalid_rows():
    connection = create_connection()
    initialize_database(connection)

    result = import_tickets_from_csv(connection, Path("data/sample_tickets.csv"))

    assert result == {"imported": 3, "skipped": 1}
    assert len(search_tickets(connection)) == 3
