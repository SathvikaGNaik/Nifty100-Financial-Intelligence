import sqlite3

conn = sqlite3.connect("database/nifty100.db")

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
    "peer_groups",
    "sectors",
    "stock_prices",
]

print("="*60)
print("NIFTY100 DATABASE DEMO")
print("="*60)

for table in tables:

    rows = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table:<20}{rows}")

print("\nForeign Keys")

print(
    conn.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()
)

conn.close()