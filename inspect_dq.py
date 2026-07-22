from src.etl.loader import load_all_core_files

datasets = load_all_core_files()

companies = datasets["companies"]

print("\n" + "=" * 60)
print("COMPANY MASTER IDs")
print("=" * 60)

print(companies["id"].head(20).tolist())


for table_name in [
    "profitandloss",
    "balancesheet",
    "cashflow"
]:

    df = datasets[table_name]

    print("\n" + "=" * 60)
    print(table_name.upper())
    print("=" * 60)

    print("\nCompany IDs:")
    print(
        df["company_id"]
        .dropna()
        .unique()[:30]
    )

    print("\nYears:")
    print(
        df["year"]
        .dropna()
        .unique()[:30]
    )

    print("\nData types:")
    print(
        df[
            ["company_id", "year"]
        ].dtypes
    )

    duplicates = df[
        df.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ]

    print(
        "\nDuplicate company/year rows:",
        len(duplicates)
    )

    if not duplicates.empty:

        print(
            duplicates[
                ["id", "company_id", "year"]
            ]
            .head(20)
            .to_string(index=False)
        )


print("\n" + "=" * 60)
print("FOREIGN KEY DIFFERENCES")
print("=" * 60)

valid_ids = set(
    companies["id"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
)

for table_name in [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents"
]:

    df = datasets[table_name]

    if "company_id" not in df.columns:
        continue

    child_ids = set(
        df["company_id"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
    )

    missing = child_ids - valid_ids

    print(
        f"\n{table_name}: "
        f"{len(missing)} unmatched unique company IDs"
    )

    print(
        sorted(missing)[:30]
    )