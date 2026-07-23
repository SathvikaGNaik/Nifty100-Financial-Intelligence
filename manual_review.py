import sqlite3
import pandas as pd

DATABASE = "database/nifty100.db"

conn = sqlite3.connect(DATABASE)

companies = [
    "ABB",
    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
]

print("=" * 70)
print("SPRINT 1 - DAY 6 MANUAL REVIEW")
print("=" * 70)

for company in companies:

    print(f"\n{company}")
    print("-" * 50)

    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "financial_ratios",
        "market_cap",
        "stock_prices",
        "sectors",
        "peer_groups",
    ]

    for table in tables:

        try:

            if table == "companies":
                query = """
                    SELECT COUNT(*)
                    FROM companies
                    WHERE id = ?
                """
            else:
                query = f"""
                    SELECT COUNT(*)
                    FROM {table}
                    WHERE company_id = ?
                """

            count = conn.execute(
                query,
                (company,)
            ).fetchone()[0]

            print(f"{table:<20} {count}")

        except Exception:
            print(f"{table:<20} N/A")

conn.close()