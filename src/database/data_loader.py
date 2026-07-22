import pandas as pd

from src.database.db_manager import DatabaseManager
from src.utils.logger import get_logger


logger = get_logger(__name__)


class DataLoader:

    def __init__(self):

        self.db = DatabaseManager()
        self.conn = self.db.connect()

    # -------------------------------------------------
    # Clear database before loading
    # -------------------------------------------------

    def clear_database(self):
        print(">>> CLEAR DATABASE CALLED")

        cursor = self.conn.cursor()

        cursor.execute("PRAGMA foreign_keys = OFF")

        tables = [

            "stock_prices",
            "market_cap",
            "financial_ratios",
            "peer_groups",
            "sectors",
            "prosandcons",
            "documents",
            "analysis",
            "cashflow",
            "balancesheet",
            "profitandloss",
            "companies"

        ]

        for table in tables:

            cursor.execute(f"DELETE FROM {table}")

        self.conn.commit()

        cursor.execute("PRAGMA foreign_keys = ON")

        logger.info("Database cleared successfully.")

    # -------------------------------------------------
    # Load one table
    # -------------------------------------------------

    def load_table(self, dataframe, table_name):

        try:

            dataframe = dataframe.copy()

            if "year_raw" in dataframe.columns:
                dataframe.drop(
                    columns=["year_raw"],
                    inplace=True
                )

            dataframe.to_sql(

                table_name,

                self.conn,

                if_exists="append",

                index=False

            )

            self.conn.commit()

            rows_loaded = len(dataframe)

            logger.info(

                f"{table_name}: {rows_loaded} rows loaded."

            )

            return {

                "table": table_name,

                "status": "SUCCESS",

                "rows_loaded": rows_loaded,

                "error": ""

            }

        except Exception as e:

            self.conn.rollback()

            print("\n" + "=" * 60)
            print(f"FAILED TABLE : {table_name}")
            print("=" * 60)

            print(e)

            print("\nColumns")
            print(list(dataframe.columns))

            print("\nDtypes")
            print(dataframe.dtypes)

            if len(dataframe):

                print("\nFirst row")
                print(dataframe.iloc[0])

            logger.exception(e)

            return {

                "table": table_name,

                "status": "FAILED",

                "rows_loaded": 0,

                "error": str(e)

            }

    # -------------------------------------------------
    # FK check
    # -------------------------------------------------

    def foreign_key_check(self):

        return self.conn.execute(

            "PRAGMA foreign_key_check"

        ).fetchall()

    # -------------------------------------------------
    # Close DB
    # -------------------------------------------------

    def close(self):

        self.db.close()