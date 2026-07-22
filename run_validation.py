from src.etl.loader import load_all_core_files
from src.validation.dq_runner import DataQualityValidator


def main():

    print("=" * 60)
    print("NIFTY 100 DATA QUALITY VALIDATION")
    print("=" * 60)

    datasets = load_all_core_files()

    validator = DataQualityValidator(
        datasets
    )

    report = validator.run()

    output_file = validator.save_report()

    print()
    print("=" * 60)
    print("DATA QUALITY SUMMARY")
    print("=" * 60)

    if report.empty:

        print("No data quality failures found.")

    else:

        summary = (
            report
            .groupby(
                ["rule_id", "severity"]
            )
            .size()
            .reset_index(
                name="failures"
            )
        )

        print(
            summary.to_string(
                index=False
            )
        )

        critical_count = (
            report["severity"]
            .eq("CRITICAL")
            .sum()
        )

        warning_count = (
            report["severity"]
            .eq("WARNING")
            .sum()
        )

        print()
        print(
            f"CRITICAL failures : {critical_count}"
        )

        print(
            f"WARNING failures  : {warning_count}"
        )

    print()
    print(
        f"Validation report saved to: {output_file}"
    )


if __name__ == "__main__":
    main()