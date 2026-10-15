"""Create and query the magazines database for Assignment 9."""

import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "db" / "magazines.db"


def create_tables(cursor):
    """Create the four tables used by the magazine subscription system."""
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS publishers (
                publisher_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS magazines (
                magazine_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subscribers (
                subscriber_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                UNIQUE (name, address)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscription_id INTEGER PRIMARY KEY,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                UNIQUE (subscriber_id, magazine_id),
                FOREIGN KEY (subscriber_id)
                    REFERENCES subscribers (subscriber_id),
                FOREIGN KEY (magazine_id) REFERENCES magazines (magazine_id)
            )
            """
        )
    except sqlite3.Error as error:
        print(f"Could not create the tables: {error}")
        raise


def add_publisher(cursor, name):
    try:
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        print(f"Publisher '{name}' is already in the database.")


def add_magazine(cursor, name, publisher_name):
    try:
        cursor.execute(
            "SELECT publisher_id FROM publishers WHERE name = ?",
            (publisher_name,),
        )
        publisher = cursor.fetchone()
        if publisher is None:
            print(f"Publisher '{publisher_name}' was not found.")
            return
        cursor.execute(
            "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
            (name, publisher[0]),
        )
    except sqlite3.IntegrityError:
        print(f"Magazine '{name}' is already in the database.")
    except sqlite3.Error as error:
        print(f"Could not add magazine '{name}': {error}")


def add_subscriber(cursor, name, address):
    try:
        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)",
            (name, address),
        )
    except sqlite3.IntegrityError:
        print(f"Subscriber '{name}' at '{address}' is already in the database.")


def add_subscription(cursor, subscriber_name, address, magazine_name, expiration_date):
    try:
        cursor.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?",
            (subscriber_name, address),
        )
        subscriber = cursor.fetchone()
        if subscriber is None:
            print(f"Subscriber '{subscriber_name}' at '{address}' was not found.")
            return

        cursor.execute(
            "SELECT magazine_id FROM magazines WHERE name = ?", (magazine_name,)
        )
        magazine = cursor.fetchone()
        if magazine is None:
            print(f"Magazine '{magazine_name}' was not found.")
            return

        cursor.execute(
            """
            INSERT INTO subscriptions
                (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
            """,
            (subscriber[0], magazine[0], expiration_date),
        )
    except sqlite3.IntegrityError:
        print(
            f"'{subscriber_name}' already has a subscription to "
            f"'{magazine_name}'."
        )
    except sqlite3.Error as error:
        print(f"Could not add the subscription: {error}")


def print_query(cursor, heading, statement, parameters=()):
    try:
        cursor.execute(statement, parameters)
        print(f"\n{heading}")
        for row in cursor.fetchall():
            print(row)
    except sqlite3.Error as error:
        print(f"Could not run query '{heading}': {error}")


def main():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        create_tables(cursor)

        for publisher in ("Condé Nast", "National Geographic Partners", "Time USA"):
            add_publisher(cursor, publisher)

        magazines = (
            ("The New Yorker", "Condé Nast"),
            ("National Geographic", "National Geographic Partners"),
            ("Time", "Time USA"),
        )
        for magazine in magazines:
            add_magazine(cursor, *magazine)

        subscribers = (
            ("Jordan Lee", "12 Oak Street"),
            ("Morgan Smith", "84 Pine Avenue"),
            ("Taylor Brown", "7 Maple Drive"),
        )
        for subscriber in subscribers:
            add_subscriber(cursor, *subscriber)

        subscriptions = (
            ("Jordan Lee", "12 Oak Street", "The New Yorker", "2027-06-30"),
            ("Jordan Lee", "12 Oak Street", "Time", "2027-08-31"),
            ("Morgan Smith", "84 Pine Avenue", "National Geographic", "2027-04-30"),
        )
        for subscription in subscriptions:
            add_subscription(cursor, *subscription)

        conn.commit()

        print_query(cursor, "All subscribers:", "SELECT * FROM subscribers")
        print_query(
            cursor,
            "Magazines sorted by name:",
            "SELECT * FROM magazines ORDER BY name",
        )
        print_query(
            cursor,
            "Magazines published by Condé Nast:",
            """
            SELECT m.*
            FROM magazines AS m
            JOIN publishers AS p ON m.publisher_id = p.publisher_id
            WHERE p.name = ?
            ORDER BY m.name
            """,
            ("Condé Nast",),
        )
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
