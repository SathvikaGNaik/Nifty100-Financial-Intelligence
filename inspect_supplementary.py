from pathlib import Path
import pandas as pd


SUPPORTING_DIR = Path("data/raw/supporting datasets")


print("=" * 80)
print("SUPPORTING DATASETS INSPECTION")
print("=" * 80)


files = [
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
]


for filename in files:

    file_path = SUPPORTING_DIR / filename

    print("\n" + "=" * 80)
    print(f"FILE: {filename}")
    print("=" * 80)

    if not file_path.exists():
        print("FILE NOT FOUND")
        continue

    try:
        df = pd.read_excel(file_path)

        print(f"\nShape: {df.shape}")

        print("\nColumns:")
        for column in df.columns:
            print(f"  - {column}")

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head().to_string(index=False))

        print("\nMissing Values:")

        missing = df.isnull().sum()
        missing = missing[missing > 0]

        if missing.empty:
            print("No missing values.")
        else:
            print(missing)

    except Exception as error:

        print("\nERROR while reading file:")
        print(error)


print("\n" + "=" * 80)
print("INSPECTION COMPLETE")
print("=" * 80)