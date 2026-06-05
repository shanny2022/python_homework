import sqlite3


DB_PATH = "../db/magazines.db"


def create_tables(cursor):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers (subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES magazines (magazine_id)
        )
        """)

        print("Tables created successfully.")

    except sqlite3.Error as error:
        print(f"Error creating tables: {error}")


def add_publisher(cursor, name):
    try:
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        print(f"Publisher added: {name}")
    except sqlite3.IntegrityError:
        print(f"Publisher already exists: {name}")
    except sqlite3.Error as error:
        print(f"Error adding publisher {name}: {error}")


def get_publisher_id(cursor, name):
    try:
        cursor.execute("SELECT publisher_id FROM publishers WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        print(f"Publisher not found: {name}")
        return None
    except sqlite3.Error as error:
        print(f"Error finding publisher {name}: {error}")
        return None


def add_magazine(cursor, name, publisher_name):
    try:
        publisher_id = get_publisher_id(cursor, publisher_name)
        if publisher_id is None:
            return

        cursor.execute(
            "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
            (name, publisher_id)
        )
        print(f"Magazine added: {name}")

    except sqlite3.IntegrityError:
        print(f"Magazine already exists: {name}")
    except sqlite3.Error as error:
        print(f"Error adding magazine {name}: {error}")


def add_subscriber(cursor, name, address):
    try:
        cursor.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?",
            (name, address)
        )
        result = cursor.fetchone()

        if result:
            print(f"Subscriber already exists: {name}, {address}")
            return

        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)",
            (name, address)
        )
        print(f"Subscriber added: {name}")

    except sqlite3.Error as error:
        print(f"Error adding subscriber {name}: {error}")


def get_subscriber_id(cursor, name, address):
    try:
        cursor.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?",
            (name, address)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        print(f"Subscriber not found: {name}, {address}")
        return None
    except sqlite3.Error as error:
        print(f"Error finding subscriber {name}: {error}")
        return None


def get_magazine_id(cursor, name):
    try:
        cursor.execute("SELECT magazine_id FROM magazines WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        print(f"Magazine not found: {name}")
        return None
    except sqlite3.Error as error:
        print(f"Error finding magazine {name}: {error}")
        return None


def add_subscription(cursor, subscriber_name, subscriber_address, magazine_name, expiration_date):
    try:
        subscriber_id = get_subscriber_id(cursor, subscriber_name, subscriber_address)
        magazine_id = get_magazine_id(cursor, magazine_name)

        if subscriber_id is None or magazine_id is None:
            return

        cursor.execute(
            """
            SELECT subscription_id
            FROM subscriptions
            WHERE subscriber_id = ? AND magazine_id = ?
            """,
            (subscriber_id, magazine_id)
        )
        result = cursor.fetchone()

        if result:
            print(f"Subscription already exists for {subscriber_name} to {magazine_name}.")
            return

        cursor.execute(
            """
            INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
            """,
            (subscriber_id, magazine_id, expiration_date)
        )
        print(f"Subscription added: {subscriber_name} to {magazine_name}")

    except sqlite3.Error as error:
        print(f"Error adding subscription: {error}")


def print_rows(title, rows):
    print(f"\n{title}")
    print("-" * len(title))
    for row in rows:
        print(row)


def run_queries(cursor):
    try:
        cursor.execute("SELECT * FROM subscribers")
        print_rows("All subscribers", cursor.fetchall())
    except sqlite3.Error as error:
        print(f"Error retrieving subscribers: {error}")

    try:
        cursor.execute("SELECT * FROM magazines ORDER BY name")
        print_rows("Magazines sorted by name", cursor.fetchall())
    except sqlite3.Error as error:
        print(f"Error retrieving magazines: {error}")

    try:
        publisher_name = "Meredith Publishing"
        cursor.execute("""
            SELECT magazines.name, publishers.name
            FROM magazines
            JOIN publishers
            ON magazines.publisher_id = publishers.publisher_id
            WHERE publishers.name = ?
            ORDER BY magazines.name
        """, (publisher_name,))
        print_rows(f"Magazines published by {publisher_name}", cursor.fetchall())
    except sqlite3.Error as error:
        print(f"Error retrieving magazines by publisher: {error}")


def main():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = 1")
            cursor = conn.cursor()

            create_tables(cursor)

            add_publisher(cursor, "Meredith Publishing")
            add_publisher(cursor, "Conde Nast")
            add_publisher(cursor, "Hearst Magazines")

            add_magazine(cursor, "Better Homes and Gardens", "Meredith Publishing")
            add_magazine(cursor, "Vogue", "Conde Nast")
            add_magazine(cursor, "Cosmopolitan", "Hearst Magazines")

            add_subscriber(cursor, "John Smith", "101 Main Street")
            add_subscriber(cursor, "Maria Johnson", "202 Oak Avenue")
            add_subscriber(cursor, "Alicia Brown", "303 Pine Road")

            add_subscription(cursor, "John Smith", "101 Main Street", "Better Homes and Gardens", "2026-12-31")
            add_subscription(cursor, "John Smith", "101 Main Street", "Vogue", "2026-10-15")
            add_subscription(cursor, "Maria Johnson", "202 Oak Avenue", "Cosmopolitan", "2027-01-20")
            add_subscription(cursor, "Alicia Brown", "303 Pine Road", "Vogue", "2026-09-30")

            conn.commit()
            print("\nData committed successfully.")

            run_queries(cursor)

    except sqlite3.Error as error:
        print(f"Database connection error: {error}")


if __name__ == "__main__":
    main()
