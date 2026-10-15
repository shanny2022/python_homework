"""Assignment 10 Task 5: rebuild cleaned quote data and import each CSV to SQLite."""
from contextlib import closing
from pathlib import Path
import os
import sqlite3
import tempfile

import pandas as pd
from clean_data import clean_quotes

HERE = Path(__file__).resolve().parent
DATABASE = HERE / "db/capstone_data.db"


def build_database():
    # Task 5: show before/after cleaning and regenerate derived features.
    clean_quotes()
    frames = {}
    for path in sorted((HERE / "data").rglob("*.csv")):
        table = path.stem
        if not table.isidentifier() or table.lower().startswith("sqlite_"):
            raise ValueError(f"Invalid table name: {table}")
        if table.lower() in {name.lower() for name in frames}:
            raise ValueError(f"Duplicate table name: {table}")
        frame = pd.read_csv(path)
        if frame.empty:
            raise ValueError(f"No records in {path}")
        frames[table] = frame
    if not {"quotes_raw", "quotes_clean"}.issubset(frames):
        raise ValueError("Both raw and clean quote CSVs are required.")

    # Task 5: import each CSV into a separate table and verify before replacement.
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=DATABASE.parent, suffix=".db")
    os.close(fd)
    try:
        with closing(sqlite3.connect(temporary)) as conn:
            for table, frame in frames.items():
                frame.to_sql(table, conn, index=False, if_exists="fail")
                count = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                if count != len(frame):
                    raise RuntimeError(f"Row count mismatch: {table}")
                print(f"{table}: {count} rows imported")
            if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise RuntimeError("Database integrity check failed")
        os.replace(temporary, DATABASE)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)
    print(f"Saved {DATABASE}")
    return DATABASE


if __name__ == "__main__":
    build_database()
