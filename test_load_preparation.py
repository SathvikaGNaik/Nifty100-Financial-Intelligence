from src.etl.load_preparation import (
    prepare_datasets_for_database,
)


prepared, rejected, audit = (
    prepare_datasets_for_database()
)


print(
    "=" * 70
)

print(
    "DATABASE LOAD PREPARATION"
)

print(
    "=" * 70
)


print(
    "\nLOAD AUDIT\n"
)

print(
    audit.to_string(
        index=False
    )
)


print(
    "\n" + "=" * 70
)

print(
    "REJECTED FOREIGN KEY RECORDS"
)

print(
    "=" * 70
)


total_rejected = 0


for table_name, df in rejected.items():

    if df.empty:
        continue

    total_rejected += len(df)

    print(
        f"\n{table_name}: "
        f"{len(df)}"
    )

    if "company_id" in df.columns:

        print(
            df["company_id"]
            .value_counts()
            .to_string()
        )


print(
    "\n" + "=" * 70
)

print(
    f"TOTAL REJECTED ROWS: "
    f"{total_rejected}"
)

print(
    "=" * 70
)


# --------------------------------------------------
# Final FK readiness check
# --------------------------------------------------

master_ids = set(
    prepared["companies"]["id"]
    .dropna()
    .astype(str)
)


remaining_fk_failures = 0


for table_name, df in prepared.items():

    if "company_id" not in df.columns:
        continue

    invalid = df[
        ~df["company_id"].isin(
            master_ids
        )
    ]

    if not invalid.empty:

        remaining_fk_failures += len(
            invalid
        )

        print(
            f"\nERROR: "
            f"{table_name} still contains "
            f"{len(invalid)} FK violations."
        )


print(
    "\nDatabase-ready FK failures:",
    remaining_fk_failures
)