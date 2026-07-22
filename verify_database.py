import sqlite3


DB_PATH = "database/nifty100.db"


connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()


print("=" * 60)
print("DATABASE SCHEMA VERIFICATION")
print("=" * 60)


# ------------------------------------------------------------
# List all tables
# ------------------------------------------------------------

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
    """
)

tables = [row[0] for row in cursor.fetchall()]


print("\nTables:")

for table in tables:
    print(f"  - {table}")


print(f"\nTotal tables: {len(tables)}")


# ------------------------------------------------------------
# Check foreign key setting
# ------------------------------------------------------------

connection.execute("PRAGMA foreign_keys = ON")

foreign_keys = connection.execute(
    "PRAGMA foreign_keys"
).fetchone()[0]


print(f"\nForeign keys enabled: {foreign_keys}")


# ------------------------------------------------------------
# Check foreign key integrity
# ------------------------------------------------------------

fk_errors = connection.execute(
    "PRAGMA foreign_key_check"
).fetchall()


print(f"Foreign key violations: {len(fk_errors)}")


if fk_errors:

    print("\nForeign key errors:")

    for error in fk_errors:
        print(error)

else:

    print("No foreign key violations found.")


connection.close()


print("\n" + "=" * 60)
print("DATABASE VERIFICATION COMPLETE")
print("=" * 60)