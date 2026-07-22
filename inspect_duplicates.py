from src.etl.loader import load_all_core_files


datasets = load_all_core_files()


for table_name in [
    "profitandloss",
    "balancesheet",
    "cashflow"
]:

    df = datasets[table_name]

    print("\n" + "=" * 70)
    print(f"DUPLICATE ANALYSIS: {table_name.upper()}")
    print("=" * 70)

    duplicates = df[
        df.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ].copy()

    print(
        f"Total rows involved in collisions: "
        f"{len(duplicates)}"
    )

    if duplicates.empty:
        continue

    print(
        "\nCompanies with most collisions:"
    )

    print(
        duplicates["company_id"]
        .value_counts()
        .head(20)
        .to_string()
    )

    print(
        "\nSample collision groups:"
    )

    columns = [
        "id",
        "company_id",
        "year",
        "year_raw"
    ]

    existing_columns = [
        col
        for col in columns
        if col in duplicates.columns
    ]

    print(
        duplicates[
            existing_columns
        ]
        .sort_values(
            ["company_id", "year"]
        )
        .head(100)
        .to_string(index=False)
    )