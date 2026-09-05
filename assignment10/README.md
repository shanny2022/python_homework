# Assignment 10

From the repository root, install the database loader dependencies and create the
lesson database (only recreate an existing database if you want to erase changes):

```sh
python3 -m pip install -r requirements.txt
python3 load_db.py
cd assignment10
python3 advanced_sql.py
```

The script locates `db/lesson.db` relative to its own file, so it also works from
the repository root. Tasks 1, 2, and 4 print order totals, customer averages, and
employees with more than five orders. Customers without orders display `No orders`.
Task 3 creates and commits a new order each time the script runs, with ten units
of each of the five cheapest products. Equal prices are ordered by product ID.
All five line items and the order are rolled back if an insert fails.

Use `python3 sqlcommand.py` from the repository root to practice the SQL queries
in `advanced_sql.py`. For Task 3, look up the customer, employee, and products,
insert the order with `RETURNING order_id`, and use that returned ID in the line
items. After practicing, delete that order's line items before deleting the order.
The SQL shell commits each statement; the Python script groups the inserts into
one transaction.

Task 5 is completed in `capstone_quotes/` using the populated quotes project
supplied separately. See its README for the cleaning pipeline, SQLite database,
and tests. Run `python3 assignment10/capstone_quotes/capstone_database.py` from
the repository root. The database contains 12 raw and 12 cleaned quote records.
