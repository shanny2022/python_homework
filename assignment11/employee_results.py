"""Assignment 11 Task 1: Employee revenue bar chart.

This script connects to ../db/lesson.db, joins employees, orders,
line_items, and products, loads the result into Pandas, groups revenue by
employee, and creates a bar chart of revenue by employee last name.

Run from the assignment11 folder:
    python employee_results.py
"""

from pathlib import Path
import os
import sqlite3
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "assignment11-matplotlib"))

import matplotlib
import pandas as pd

matplotlib.use("Agg")

import matplotlib.pyplot as plt


DB_PATH = Path(__file__).resolve().parent.parent / "db" / "lesson.db"
OUTPUT_CSV = Path(__file__).resolve().parent / "employee_results.csv"
OUTPUT_PNG = Path(__file__).resolve().parent / "employee_revenue_by_last_name.png"


def load_employee_revenue(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Load joined employee/order revenue data from the lesson database."""
    if not db_path.exists():
        raise FileNotFoundError(
            f"Could not find database at {db_path}. "
            "Make sure this file is inside assignment11 and lesson.db is inside ../db/."
        )

    query = """
        SELECT
            e.employee_id,
            e.first_name,
            e.last_name,
            o.order_id,
            li.quantity,
            p.price,
            li.quantity * p.price AS line_revenue
        FROM employees AS e
        JOIN orders AS o
            ON e.employee_id = o.employee_id
        JOIN line_items AS li
            ON o.order_id = li.order_id
        JOIN products AS p
            ON li.product_id = p.product_id
    """

    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)


def summarize_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Group joined revenue data by employee_id and employee name."""
    revenue_by_employee = (
        df.groupby(["employee_id", "first_name", "last_name"], as_index=False)["line_revenue"]
        .sum()
        .rename(columns={"line_revenue": "total_revenue"})
        .sort_values("total_revenue", ascending=False)
    )
    return revenue_by_employee


def plot_revenue_by_last_name(summary_df: pd.DataFrame) -> None:
    """Create and display a bar chart of revenue by employee last name."""
    plot_df = summary_df.set_index("last_name")

    ax = plot_df["total_revenue"].plot.bar(
        figsize=(10, 6),
        color="steelblue",
        edgecolor="black",
    )
    ax.set_title("Total Revenue by Employee Last Name")
    ax.set_xlabel("Employee Last Name")
    ax.set_ylabel("Total Revenue ($)")
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG)
    plt.close()


def main() -> None:
    employee_order_df = load_employee_revenue()
    print("Joined employee revenue data:")
    print(employee_order_df.head())

    revenue_summary = summarize_revenue(employee_order_df)
    print("\nRevenue by employee:")
    print(revenue_summary)

    revenue_summary.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved summary CSV to {OUTPUT_CSV}")

    plot_revenue_by_last_name(revenue_summary)
    print(f"Saved chart image to {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
