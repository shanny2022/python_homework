"""Assignment 11 Task 2: Cumulative revenue line chart.

This script connects to ../db/lesson.db, reads order totals with SQL,
adds a cumulative revenue column, and plots cumulative revenue by order_id.

Run from the assignment11 folder:
    python cumulative.py
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
OUTPUT_CSV = Path(__file__).resolve().parent / "cumulative_revenue.csv"
OUTPUT_PNG = Path(__file__).resolve().parent / "cumulative_revenue.png"


def load_order_totals(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Load order_id and total order price from the lesson database."""
    if not db_path.exists():
        raise FileNotFoundError(
            f"Could not find database at {db_path}. "
            "Make sure lesson.db is located in ../db/."
        )

    query = """
        SELECT
            o.order_id,
            SUM(li.quantity * p.price) AS total_price
        FROM orders AS o
        JOIN line_items AS li
            ON o.order_id = li.order_id
        JOIN products AS p
            ON li.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
    """

    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)


def add_cumulative_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Add a cumulative revenue column using Pandas cumsum()."""
    result = df.copy()
    result["cumulative_revenue"] = result["total_price"].cumsum()
    return result


def plot_cumulative_revenue(df: pd.DataFrame) -> None:
    """Plot cumulative revenue against order_id as a line chart."""
    ax = df.plot.line(
        x="order_id",
        y="cumulative_revenue",
        figsize=(10, 6),
        marker="o",
        color="darkgreen",
        legend=False,
    )
    ax.set_title("Cumulative Revenue by Order ID")
    ax.set_xlabel("Order ID")
    ax.set_ylabel("Cumulative Revenue ($)")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG)
    plt.close()


def main() -> None:
    order_totals = load_order_totals()
    cumulative_df = add_cumulative_revenue(order_totals)

    print("Order totals with cumulative revenue:")
    print(cumulative_df.head(10))

    cumulative_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved cumulative revenue CSV to {OUTPUT_CSV}")

    plot_cumulative_revenue(cumulative_df)
    print(f"Saved chart image to {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
