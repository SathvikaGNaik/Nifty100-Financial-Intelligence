from src.etl.loader import (
    load_all_core_files,
    load_all_supporting_files,
)


print("=" * 70)
print("ALL SOURCE FILES")
print("=" * 70)


core = load_all_core_files()
supporting = load_all_supporting_files()


all_datasets = {
    **core,
    **supporting,
}


print("\nCORE DATASETS")
print("-" * 70)

for name, df in core.items():

    print(
        f"{name:<25} "
        f"rows={len(df):<6} "
        f"columns={len(df.columns)}"
    )


print("\nSUPPORTING DATASETS")
print("-" * 70)

for name, df in supporting.items():

    print(
        f"{name:<25} "
        f"rows={len(df):<6} "
        f"columns={len(df.columns)}"
    )


print("\n" + "=" * 70)

print(
    f"Total datasets detected: {len(all_datasets)}"
)

print("=" * 70)