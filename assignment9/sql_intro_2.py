"""Create a product order summary with SQL and pandas."""

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "db" / "lesson.db"
OUTPUT_PATH = Path(__file__).resolve().parent / "order_summary.csv"


def main():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        sql_statement = """
            SELECT
                li.line_item_id,
                li.quantity,
                li.product_id,
                p.product_name,
                p.price
            FROM line_items AS li
            JOIN products AS p ON li.product_id = p.product_id
        """
        order_data = pd.read_sql_query(sql_statement, conn)
    except (sqlite3.Error, pd.errors.DatabaseError) as error:
        print(f"Could not read order data: {error}")
        return
    finally:
        if conn is not None:
            conn.close()

    print("First five joined rows:")
    print(order_data.head())

    order_data["total"] = order_data["quantity"] * order_data["price"]
    print("\nFirst five rows with totals:")
    print(order_data.head())

    order_summary = (
        order_data.groupby("product_id", as_index=False)
        .agg(
            line_item_id=("line_item_id", "count"),
            total=("total", "sum"),
            product_name=("product_name", "first"),
        )
        .sort_values("product_name")
    )
    print("\nFirst five product summaries:")
    print(order_summary.head())
    order_summary.to_csv(OUTPUT_PATH, index=False)
    print(f"\nOrder summary written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
