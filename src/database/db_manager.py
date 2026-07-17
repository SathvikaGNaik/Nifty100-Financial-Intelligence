import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self):

        self.database_path = (
            Path("database") / "nifty100.db"
        )

        self.connection = None

    def connect(self):

        self.connection = sqlite3.connect(
            self.database_path
        )

        return self.connection

    def close(self):

        if self.connection:
            self.connection.close()