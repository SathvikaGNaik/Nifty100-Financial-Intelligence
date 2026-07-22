from src.validation.report import ValidationFailure


class DQRunner:

    def __init__(self):
        self.failures = []

    def add_failure(
        self,
        rule_id,
        severity,
        table,
        company_id="",
        year="",
        message=""
    ):

        self.failures.append(
            ValidationFailure(
                rule_id,
                severity,
                table,
                company_id,
                year,
                message
            )
        )

    def summary(self):

        critical = sum(
            1
            for f in self.failures
            if f.severity == "CRITICAL"
        )

        warning = sum(
            1
            for f in self.failures
            if f.severity == "WARNING"
        )

        return critical, warning
    

from pathlib import Path
import pandas as pd

from src.validation.rules import (
    dq01_primary_key,
    dq02_company_year,
    dq03_foreign_key,
    dq04_balance_sheet,
    dq05_opm_cross_check,
    dq06_positive_sales,
    dq07_net_cash_flow,
    dq08_tax_rate,
    dq09_dividend_cap,
    dq10_url_validation,
    dq11_eps_sign,
    dq12_bse_coverage,
    dq13_year_validity,
    dq14_year_coverage,
    dq15_company_coverage,
    dq16_required_field_coverage,
)


class DataQualityValidator:

    def __init__(self, datasets):
        self.datasets = datasets
        self.failures = []

        companies = datasets.get("companies")

        if companies is not None and "id" in companies.columns:
            self.company_ids = set(
                companies["id"]
                .dropna()
                .astype(str)
            )
        else:
            self.company_ids = set()

    def add_failures(
        self,
        rule_id,
        severity,
        table,
        failed_rows,
        message
    ):
        """
        Convert failed rows into standard validation
        failure records.
        """

        if failed_rows is None:
            return

        if isinstance(failed_rows, list):
            if not failed_rows:
                return

            failed_rows = pd.DataFrame({
                "id": failed_rows
            })

        if failed_rows.empty:
            return

        for index, row in failed_rows.iterrows():

            company_id = row.get(
                "company_id",
                row.get("id", "")
            )

            year = row.get("year", "")

            self.failures.append({
                "rule_id": rule_id,
                "severity": severity,
                "table": table,
                "row_index": index,
                "company_id": company_id,
                "year": year,
                "message": message
            })

    def run(self):

        # ====================================================
        # DQ-01: PRIMARY KEY UNIQUENESS
        # ====================================================

        for table, df in self.datasets.items():

            failed = dq01_primary_key(
                df,
                key_column="id"
            )

            self.add_failures(
                "DQ-01",
                "CRITICAL",
                table,
                failed,
                "Primary key is null or duplicated."
            )

        # ====================================================
        # DQ-02: COMPANY + YEAR UNIQUENESS
        # ====================================================

        financial_tables = [
            "profitandloss",
            "balancesheet",
            "cashflow"
        ]

        for table in financial_tables:

            if table not in self.datasets:
                continue

            df = self.datasets[table]

            failed = dq02_company_year(df)

            self.add_failures(
                "DQ-02",
                "CRITICAL",
                table,
                failed,
                "Duplicate (company_id, year) combination."
            )

        # ====================================================
        # DQ-03: FOREIGN KEY INTEGRITY
        # ====================================================

        for table, df in self.datasets.items():

            if table == "companies":
                continue

            if "company_id" not in df.columns:
                continue

            failed = dq03_foreign_key(
                df,
                self.company_ids
            )

            self.add_failures(
                "DQ-03",
                "CRITICAL",
                table,
                failed,
                "company_id does not exist in companies."
            )

        # ====================================================
        # DQ-04: BALANCE SHEET BALANCE
        # ====================================================

        if "balancesheet" in self.datasets:

            failed = dq04_balance_sheet(
                self.datasets["balancesheet"]
            )

            self.add_failures(
                "DQ-04",
                "WARNING",
                "balancesheet",
                failed,
                "Balance sheet difference exceeds 1%."
            )

        # ====================================================
        # DQ-05: OPM CROSS-CHECK
        # ====================================================

        if "profitandloss" in self.datasets:

            failed = dq05_opm_cross_check(
                self.datasets["profitandloss"]
            )

            self.add_failures(
                "DQ-05",
                "WARNING",
                "profitandloss",
                failed,
                "Reported OPM differs from calculated OPM."
            )

        # ====================================================
        # DQ-06: POSITIVE SALES
        # ====================================================

        if "profitandloss" in self.datasets:

            failed = dq06_positive_sales(
                self.datasets["profitandloss"]
            )

            self.add_failures(
                "DQ-06",
                "WARNING",
                "profitandloss",
                failed,
                "Sales is zero or negative."
            )

        # ====================================================
        # DQ-07: NET CASH FLOW
        # ====================================================

        if "cashflow" in self.datasets:

            failed = dq07_net_cash_flow(
                self.datasets["cashflow"]
            )

            self.add_failures(
                "DQ-07",
                "WARNING",
                "cashflow",
                failed,
                "Net cash flow does not match activity totals."
            )

        # ====================================================
        # DQ-08: TAX RATE
        # ====================================================

        if "profitandloss" in self.datasets:

            failed = dq08_tax_rate(
                self.datasets["profitandloss"]
            )

            self.add_failures(
                "DQ-08",
                "WARNING",
                "profitandloss",
                failed,
                "Tax percentage is outside 0-100 range."
            )

        # ====================================================
        # DQ-09: DIVIDEND CAP
        # ====================================================

        if "profitandloss" in self.datasets:

            failed = dq09_dividend_cap(
                self.datasets["profitandloss"]
            )

            self.add_failures(
                "DQ-09",
                "WARNING",
                "profitandloss",
                failed,
                "Dividend payout is outside 0-100 range."
            )

        # ====================================================
        # DQ-10: URL VALIDATION
        # ====================================================

        if "companies" in self.datasets:

            failed = dq10_url_validation(
                self.datasets["companies"],
                [
                    "company_logo",
                    "chart_link",
                    "website",
                    "nse_profile",
                    "bse_profile"
                ]
            )

            self.add_failures(
                "DQ-10",
                "WARNING",
                "companies",
                failed,
                "Invalid URL format."
            )

        # ====================================================
        # DQ-11: EPS SIGN
        # ====================================================

        if "profitandloss" in self.datasets:

            failed = dq11_eps_sign(
                self.datasets["profitandloss"]
            )

            self.add_failures(
                "DQ-11",
                "WARNING",
                "profitandloss",
                failed,
                "EPS sign is inconsistent with net profit."
            )

        # ====================================================
        # DQ-12: BSE COVERAGE
        # ====================================================

        if "companies" in self.datasets:

            failed = dq12_bse_coverage(
                self.datasets["companies"]
            )

            self.add_failures(
                "DQ-12",
                "WARNING",
                "companies",
                failed,
                "BSE profile is missing."
            )

        # ====================================================
        # DQ-13: YEAR VALIDITY
        # ====================================================

        for table in financial_tables:

            if table not in self.datasets:
                continue

            failed = dq13_year_validity(
                self.datasets[table]
            )

            self.add_failures(
                "DQ-13",
                "WARNING",
                table,
                failed,
                "Invalid financial year."
            )

        # ====================================================
        # DQ-14: YEAR COVERAGE
        # ====================================================

        for table in financial_tables:

            if table not in self.datasets:
                continue

            failed = dq14_year_coverage(
                self.datasets[table],
                minimum_years=5
            )

            self.add_failures(
                "DQ-14",
                "WARNING",
                table,
                failed,
                "Company has fewer than 5 years of data."
            )

        # ====================================================
        # DQ-15: COMPANY COVERAGE
        # ====================================================

        for table in financial_tables:

            if table not in self.datasets:
                continue

            failed = dq15_company_coverage(
                self.datasets[table],
                self.company_ids
            )

            self.add_failures(
                "DQ-15",
                "WARNING",
                table,
                failed,
                "Company has no records in this dataset."
            )

        # ====================================================
        # DQ-16: REQUIRED FIELD COVERAGE
        # ====================================================

        required_fields = {
            "companies": [
                "id",
                "company_name"
            ],

            "profitandloss": [
                "id",
                "company_id",
                "year",
                "sales",
                "net_profit"
            ],

            "balancesheet": [
                "id",
                "company_id",
                "year",
                "total_assets",
                "total_liabilities"
            ],

            "cashflow": [
                "id",
                "company_id",
                "year"
            ]
        }

        for table, columns in required_fields.items():

            if table not in self.datasets:
                continue

            failed = dq16_required_field_coverage(
                self.datasets[table],
                columns
            )

            self.add_failures(
                "DQ-16",
                "WARNING",
                table,
                failed,
                "Required field contains a null value."
            )

        return pd.DataFrame(self.failures)

    def save_report(
        self,
        output_path="output/validation_failures.csv"
    ):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        report = pd.DataFrame(self.failures)

        columns = [
            "rule_id",
            "severity",
            "table",
            "row_index",
            "company_id",
            "year",
            "message"
        ]

        if report.empty:
            report = pd.DataFrame(
                columns=columns
            )

        report.to_csv(
            output_path,
            index=False
        )

        return output_path