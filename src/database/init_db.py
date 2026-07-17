from pathlib import Path

from src.database.db_manager import DatabaseManager


def initialize_database():

    db = DatabaseManager()

    conn = db.connect()

    schema = Path("database/schema.sql").read_text(
        encoding="utf-8"
    )

    conn.executescript(schema)

    conn.commit()

    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()