import sqlite3

connection = sqlite3.connect("database/nifty100.db")
cursor = connection.cursor()

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents"
]

print("=" * 50)
print("DATABASE VERIFICATION")
print("=" * 50)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:<20} {count}")

connection.close()