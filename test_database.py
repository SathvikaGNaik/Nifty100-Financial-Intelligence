from pathlib import Path
import pandas as pd

from src.database.data_loader import DataLoader
from src.etl.loader import load_all_core_files

datasets = load_all_core_files()
loader = DataLoader()

results = []

for table_name, df in datasets.items():

    print(f"\nLoading {table_name}")

    result = loader.load_table(df, table_name)

    results.append(result)

loader.close()

report_dir = Path("reports/etl")
report_dir.mkdir(parents=True, exist_ok=True)

audit_df = pd.DataFrame(results)

audit_file = report_dir / "etl_load_report.csv"

audit_df.to_csv(audit_file, index=False)

print("\nETL Audit Report")
print(audit_df)

print(f"\nAudit report saved to {audit_file}")