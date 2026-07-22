from src.etl.loader import load_all_core_files


datasets = load_all_core_files()

companies = datasets["companies"]

master_ids = set(
    companies["id"]
    .dropna()
    .astype(str)
)


print("=" * 70)
print("FOREIGN KEY INVESTIGATION")
print("=" * 70)

print(
    f"\nCompanies in master table: "
    f"{len(master_ids)}"
)


for table_name, df in datasets.items():

    if "company_id" not in df.columns:
        continue

    invalid = df[
        ~df["company_id"].isin(master_ids)
    ].copy()

    if invalid.empty:
        continue

    print("\n" + "=" * 70)
    print(table_name.upper())
    print("=" * 70)

    print(
        f"Total unmatched rows: "
        f"{len(invalid)}"
    )

    print(
        f"Unique unmatched IDs: "
        f"{invalid['company_id'].nunique()}"
    )

    print("\nRows per unmatched ticker:")

    print(
        invalid["company_id"]
        .value_counts()
        .to_string()
    )


print("\n" + "=" * 70)
print("MASTER COMPANY IDs")
print("=" * 70)

print(
    sorted(master_ids)
)