import sqlite3
import pandas as pd


DB_PATH = "../db/lesson.db"


def main():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            sql_statement = """
            SELECT
                line_items.line_item_id,
                line_items.quantity,
                products.product_id,
                products.product_name,
                products.price
            FROM line_items
            JOIN products
            ON line_items.product_id = products.product_id
            """

            df = pd.read_sql_query(sql_statement, conn)

            print("First 5 rows from the SQL query:")
            print(df.head())

            df["total"] = df["quantity"] * df["price"]

            print("\nFirst 5 rows with total column:")
            print(df.head())

            summary_df = df.groupby("product_id").agg({
                "line_item_id": "count",
                "total": "sum",
                "product_name": "first"
            })

            summary_df = summary_df.rename(columns={
                "line_item_id": "times_ordered",
                "total": "total_price_paid"
            })

            summary_df = summary_df.sort_values("product_name")

            print("\nFirst 5 rows of product order summary:")
            print(summary_df.head())

            summary_df.to_csv("order_summary.csv")

            print("\norder_summary.csv has been created successfully.")

    except sqlite3.Error as error:
        print(f"Database error: {error}")
    except pd.errors.DatabaseError as error:
        print(f"Pandas database error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
