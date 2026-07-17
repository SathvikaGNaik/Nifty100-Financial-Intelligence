import pandas as pd

from src.validation.rules import (
    check_missing_columns,
    check_duplicate_rows,
    check_missing_values,
    check_duplicate_ids,
    check_empty_strings,
    check_invalid_urls,
    check_numeric_columns,
)


def validate_dataset(df, config):
    """
    Validate a dataset using the supplied configuration.

    Parameters:
        df (DataFrame): Dataset to validate
        config (dict): Validation configuration

    Returns:
        dict: Validation report
    """

    report = {}

    required_columns = config.get("required_columns", [])
    url_columns = config.get("url_columns", [])
    numeric_columns = config.get("numeric_columns", [])

    report["missing_columns"] = check_missing_columns(
        df,
        required_columns
    )

    report["duplicate_rows"] = len(
        check_duplicate_rows(df)
    )

    report["duplicate_ids"] = check_duplicate_ids(df)

    report["missing_values"] = (
        check_missing_values(df).to_dict()
    )

    report["empty_strings"] = (
        check_empty_strings(df)
    )

    report["invalid_urls"] = (
        check_invalid_urls(df, url_columns)
    )

    report["invalid_numeric"] = (
        check_numeric_columns(df, numeric_columns)
    )

    return report


def save_validation_report(report, output_file):
    """
    Save validation report as CSV.
    """

    rows = []

    # Missing Columns
    for column in report["missing_columns"]:
        rows.append({
            "Check": "Missing Column",
            "Column": column,
            "Value": ""
        })

    # Duplicate Rows
    rows.append({
        "Check": "Duplicate Rows",
        "Column": "",
        "Value": report["duplicate_rows"]
    })

    # Duplicate IDs
    rows.append({
        "Check": "Duplicate IDs",
        "Column": "",
        "Value": len(report["duplicate_ids"])
    })

    # Missing Values
    for column, count in report["missing_values"].items():
        rows.append({
            "Check": "Missing Values",
            "Column": column,
            "Value": count
        })

    # Empty Strings
    for column, count in report["empty_strings"].items():
        rows.append({
            "Check": "Empty Strings",
            "Column": column,
            "Value": count
        })

    # Invalid URLs
    for column, count in report["invalid_urls"].items():
        rows.append({
            "Check": "Invalid URLs",
            "Column": column,
            "Value": count
        })

    # Invalid Numeric Values
    for column, count in report["invalid_numeric"].items():
        rows.append({
            "Check": "Invalid Numeric",
            "Column": column,
            "Value": count
        })

    report_df = pd.DataFrame(rows)

    report_df.to_csv(output_file, index=False)

    print(f"Validation report saved to {output_file}")