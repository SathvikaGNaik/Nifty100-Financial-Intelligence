import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self):

        self.database_path = (
            Path("database") / "nifty100.db"
        )

        self.connection = None

    def connect(self):
        """
        Create a SQLite connection and enable
        foreign key constraint enforcement.
        """

        self.connection = sqlite3.connect(
            self.database_path
        )

        # SQLite requires foreign keys to be enabled
        # separately for every database connection.
        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return self.connection

    def close(self):
        """
        Close the database connection.
        """

        if self.connection:
            self.connection.close()
            self.connection = None