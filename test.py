from pathlib import Path

from src.etl.loader import load_all_core_files
from src.validation.validator import (
    validate_dataset,
    save_validation_report
)
from src.validation.config import VALIDATION_CONFIG

# ---------------------------------------
# Create validation report folder
# ---------------------------------------

report_dir = Path("reports/validation")
report_dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------
# Load all datasets
# ---------------------------------------

datasets = load_all_core_files()

# ---------------------------------------
# Validate each dataset
# ---------------------------------------

for dataset_name, df in datasets.items():

    print("\n" + "=" * 60)
    print(f"VALIDATING DATASET : {dataset_name.upper()}")
    print("=" * 60)

    config = VALIDATION_CONFIG.get(dataset_name, {})

    report = validate_dataset(
        df,
        config
    )

    print(f"Missing Columns : {len(report['missing_columns'])}")
    print(f"Duplicate Rows  : {report['duplicate_rows']}")
    print(f"Duplicate IDs   : {len(report['duplicate_ids'])}")

    print("\nMissing Values")
    print("-" * 40)
    missing_found = False
    for column, count in report["missing_values"].items():
        if count > 0:
            print(f"{column:<25}{count}")
            missing_found = True

    if not missing_found:
        print("No missing values found.")

    print("\nEmpty Strings")
    print("-" * 40)

    if report["empty_strings"]:
        for column, count in report["empty_strings"].items():
            print(f"{column:<25}{count}")
    else:
        print("No empty strings found.")

    print("\nInvalid URLs")
    print("-" * 40)

    if report["invalid_urls"]:
        for column, count in report["invalid_urls"].items():
            print(f"{column:<25}{count}")
    else:
        print("No invalid URLs found.")

    print("\nInvalid Numeric Values")
    print("-" * 40)

    if report["invalid_numeric"]:
        for column, count in report["invalid_numeric"].items():
            print(f"{column:<25}{count}")
    else:
        print("No invalid numeric values found.")

    output_file = report_dir / f"{dataset_name}_validation.csv"

    save_validation_report(
        report,
        output_file
    )

print("\n" + "=" * 60)
print("ALL DATASETS VALIDATED SUCCESSFULLY")
print("=" * 60)