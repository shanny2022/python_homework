"""Assignment 10: advanced SQL using the shared db/lesson.db database."""

from pathlib import Path
import sqlite3


DB_PATH = Path(__file__).resolve().parents[1] / "db" / "lesson.db"

# Task 1: Complex JOINs with aggregation.
ORDER_TOTALS = """
SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
FROM orders AS o
JOIN line_items AS li ON li.order_id = o.order_id
JOIN products AS p ON p.product_id = li.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5;
"""

# Task 2: Average order price per customer using a subquery.
CUSTOMER_AVERAGES = """
SELECT c.customer_name, AVG(order_totals.total_price) AS average_total_price
FROM customers AS c
LEFT JOIN (
    SELECT o.customer_id AS customer_id_b,
           SUM(p.price * li.quantity) AS total_price
    FROM orders AS o
    JOIN line_items AS li ON li.order_id = o.order_id
    JOIN products AS p ON p.product_id = li.product_id
    GROUP BY o.order_id, o.customer_id
) AS order_totals ON c.customer_id = order_totals.customer_id_b
GROUP BY c.customer_id, c.customer_name
ORDER BY c.customer_id;
"""


# Task 3: Insert an order and its five line items in one transaction.
def create_order(conn):
    # The connection context commits on success and rolls back on an error.
    with conn:
        conn.execute("BEGIN IMMEDIATE")
        customer = conn.execute(
            "SELECT customer_id FROM customers WHERE customer_name = ?",
            ("Perez and Sons",),
        ).fetchone()
        products = conn.execute(
            "SELECT product_id FROM products ORDER BY price, product_id LIMIT 5"
        ).fetchall()
        employee = conn.execute(
            "SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?",
            ("Miranda", "Harris"),
        ).fetchone()
        if customer is None or employee is None or len(products) != 5:
            raise ValueError("The required customer, employee, or five products are missing.")

        order_id = conn.execute(
            """INSERT INTO orders (customer_id, employee_id, date)
               VALUES (?, ?, date('now')) RETURNING order_id""",
            (customer[0], employee[0]),
        ).fetchone()[0]
        conn.executemany(
            "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            [(order_id, product[0], 10) for product in products],
        )
    return order_id


ORDER_ITEMS = """
SELECT li.line_item_id, li.quantity, p.product_name
FROM line_items AS li
JOIN products AS p ON p.product_id = li.product_id
WHERE li.order_id = ?
ORDER BY li.line_item_id;
"""

# Task 4: Employees associated with more than five orders.
BUSY_EMPLOYEES = """
SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
FROM employees AS e
JOIN orders AS o ON o.employee_id = e.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
HAVING COUNT(o.order_id) > 5
ORDER BY e.employee_id;
"""


def main():
    if not DB_PATH.is_file():
        raise FileNotFoundError("Run python3 load_db.py from python_homework first.")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = 1")
    try:
        print("Task 1: First five order totals (order_id, total_price)")
        for order_id, total in conn.execute(ORDER_TOTALS):
            print(order_id, f"{total:.2f}")

        print("\nTask 2: Average order price per customer")
        for name, average in conn.execute(CUSTOMER_AVERAGES):
            print(name, f"{average:.2f}" if average is not None else "No orders")

        order_id = create_order(conn)
        print(f"\nTask 3: Order {order_id} (line_item_id, quantity, product_name)")
        for row in conn.execute(ORDER_ITEMS, (order_id,)):
            print(*row, sep=" | ")

        print("\nTask 4: Employees with more than five orders")
        for row in conn.execute(BUSY_EMPLOYEES):
            print(*row, sep=" | ")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
