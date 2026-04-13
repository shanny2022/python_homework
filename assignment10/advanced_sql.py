import sqlite3

DB_PATH = "../db/lesson.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()

    # Task 1: Complex JOINs with Aggregation
    print("Task 1 Results:")
    task1_sql = """
    SELECT o.order_id,
           SUM(p.price * li.quantity) AS total_price
    FROM orders AS o
    JOIN line_items AS li
      ON o.order_id = li.order_id
    JOIN products AS p
      ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """
    cur.execute(task1_sql)
    for row in cur.fetchall():
        print(row)

    # Task 2: Understanding Subqueries
    print("\nTask 2 Results:")
    task2_sql = """
    SELECT c.customer_name,
           AVG(order_totals.total_price) AS average_total_price
    FROM customers AS c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b,
               o.order_id,
               SUM(p.price * li.quantity) AS total_price
        FROM orders AS o
        JOIN line_items AS li
          ON o.order_id = li.order_id
        JOIN products AS p
          ON li.product_id = p.product_id
        GROUP BY o.order_id
    ) AS order_totals
      ON c.customer_id = order_totals.customer_id_b
    GROUP BY c.customer_id, c.customer_name
    ORDER BY c.customer_name;
    """
    cur.execute(task2_sql)
    for row in cur.fetchall():
        print(row)

    # Task 3: An Insert Transaction Based on Data
    print("\nTask 3 Results:")
    try:
        conn.execute("BEGIN")

        cur.execute("""
            SELECT customer_id
            FROM customers
            WHERE customer_name = ?;
        """, ("Perez and Sons",))
        customer_row = cur.fetchone()
        if customer_row is None:
            raise ValueError("Customer 'Perez and Sons' not found.")
        customer_id = customer_row[0]

        cur.execute("""
            SELECT employee_id
            FROM employees
            WHERE first_name = ? AND last_name = ?;
        """, ("Miranda", "Harris"))
        employee_row = cur.fetchone()
        if employee_row is None:
            raise ValueError("Employee 'Miranda Harris' not found.")
        employee_id = employee_row[0]

        cur.execute("""
            SELECT product_id
            FROM products
            ORDER BY price ASC, product_id ASC
            LIMIT 5;
        """)
        product_ids = [row[0] for row in cur.fetchall()]
        if len(product_ids) < 5:
            raise ValueError("Fewer than 5 products found.")

        cur.execute("""
            INSERT INTO orders (customer_id, employee_id, date)
            VALUES (?, ?, date('now'))
            RETURNING order_id;
        """, (customer_id, employee_id))
        order_id = cur.fetchone()[0]

        for product_id in product_ids:
            cur.execute("""
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, ?);
            """, (order_id, product_id, 10))

        conn.commit()

        cur.execute("""
            SELECT li.line_item_id,
                   li.quantity,
                   p.product_name
            FROM line_items AS li
            JOIN products AS p
              ON li.product_id = p.product_id
            WHERE li.order_id = ?
            ORDER BY li.line_item_id;
        """, (order_id,))
        for row in cur.fetchall():
            print(row)

    except Exception as e:
        conn.rollback()
        print("Task 3 failed:", e)

    # Task 4: Aggregation with HAVING
    print("\nTask 4 Results:")
    task4_sql = """
    SELECT e.employee_id,
           e.first_name,
           e.last_name,
           COUNT(o.order_id) AS order_count
    FROM employees AS e
    JOIN orders AS o
      ON e.employee_id = o.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
    HAVING COUNT(o.order_id) > 5
    ORDER BY order_count DESC, e.last_name, e.first_name;
    """
    cur.execute(task4_sql)
    for row in cur.fetchall():
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
