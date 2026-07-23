import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT
    company_id,
    COUNT(DISTINCT year) AS years
FROM profitandloss
GROUP BY company_id
HAVING COUNT(DISTINCT year) < 5
ORDER BY years
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()