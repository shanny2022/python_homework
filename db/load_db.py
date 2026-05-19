import pandas as pd
import sqlalchemy as sa
import sqlite3
import os

db_path = "./db/lesson.db"
os.makedirs("db", exist_ok=True)

if os.path.exists(db_path):
    answer = input("The database exists. Do you want to recreate it (y/n)? ")
    if answer.lower() != "y":
        exit(0)
    os.remove(db_path)

# Create tables and database
with sqlite3.connect(db_path, isolation_level="IMMEDIATE") as conn:
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        contact TEXT,
        street TEXT,
        city TEXT,
        postal_code TEXT,
        country TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        price REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        employee_id INTEGER,
        date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS line_items (
        line_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    )
    """)

engine = sa.create_engine("sqlite:///db/lesson.db")

tables = ["customers", "employees", "products", "orders", "line_items"]

def clean_dataframe(df):
    df = df.copy()

    # Remove duplicates
    df = df.drop_duplicates()

    # Strip whitespace from text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    return df

for table in tables:
    csv_file = "./csv/" + table + ".csv"
    data = pd.read_csv(csv_file, sep=",")

    print(f"\n--- {table.upper()} BEFORE CLEANING ---")
    print("Shape:", data.shape)
    print(data.head())
    print("Missing values:\n", data.isna().sum())

    cleaned_data = clean_dataframe(data)

    print(f"\n--- {table.upper()} AFTER CLEANING ---")
    print("Shape:", cleaned_data.shape)
    print(cleaned_data.head())
    print("Missing values:\n", cleaned_data.isna().sum())

    cleaned_data.to_sql(table.lower(), engine, if_exists="append", index=False)

print("\nDatabase created and cleaned data loaded into SQLite.")
