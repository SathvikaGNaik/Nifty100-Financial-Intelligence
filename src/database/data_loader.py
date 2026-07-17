import sqlite3
import pandas as pd

from src.database.db_manager import DatabaseManager
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataLoader:

    def __init__(self):
        self.db = DatabaseManager()
        self.conn = self.db.connect()

    def load_table(self, dataframe, table_name):
        """
        Load a DataFrame into SQLite using a transaction.
        Existing records are removed before loading.
        """

        try:

            cursor = self.conn.cursor()

            cursor.execute(f"DELETE FROM {table_name}")

            dataframe.to_sql(
                table_name,
                self.conn,
                if_exists="append",
                index=False
            )

            self.conn.commit()

            logger.info(
                f"{table_name}: {len(dataframe)} rows loaded."
            )

            return {
                "table": table_name,
                "status": "SUCCESS",
                "rows_loaded": len(dataframe),
                "error": ""
            }

        except Exception as e:

            self.conn.rollback()

            logger.error(
                f"{table_name}: {e}"
            )

            return {
                "table": table_name,
                "status": "FAILED",
                "rows_loaded": 0,
                "error": str(e)
            }

    def close(self):
        self.conn.close()