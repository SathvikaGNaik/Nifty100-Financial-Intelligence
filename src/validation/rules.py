import pandas as pd


# ============================================================
# GENERIC VALIDATION HELPERS
# ============================================================

def check_missing_columns(df, required_columns):
    """
    Return a list of required columns missing from the dataset.
    """
    return [
        col for col in required_columns
        if col not in df.columns
    ]


def check_empty_strings(df):
    """
    Count empty strings in text columns.
    """
    empty_counts = {}

    for col in df.select_dtypes(include="object").columns:

        count = (
            df[col]
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        if count > 0:
            empty_counts[col] = int(count)

    return empty_counts


def check_numeric_columns(df, numeric_columns):
    """
    Check specified columns for non-numeric values.
    """
    invalid_counts = {}

    for column in numeric_columns:

        if column not in df.columns:
            continue

        invalid = (
            pd.to_numeric(
                df[column],
                errors="coerce"
            ).isna()
            & df[column].notna()
        )

        count = invalid.sum()

        if count > 0:
            invalid_counts[column] = int(count)

    return invalid_counts


# ============================================================
# DQ-01: PRIMARY KEY UNIQUENESS
# ============================================================

def dq01_primary_key(df, key_column="id"):
    """
    DQ-01 CRITICAL

    Check that the primary key is not null
    and contains no duplicate values.
    """

    if key_column not in df.columns:
        return df

    invalid = df[
        df[key_column].isna()
        | df[key_column].duplicated(keep=False)
    ]

    return invalid


# ============================================================
# DQ-02: COMPANY + YEAR UNIQUENESS
# ============================================================

def dq02_company_year(df):
    """
    DQ-02 CRITICAL

    Check uniqueness of (company_id, year).
    """

    required = ["company_id", "year"]

    if not all(col in df.columns for col in required):
        return pd.DataFrame()

    invalid = df[
        df.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ]

    return invalid


# ============================================================
# DQ-03: FOREIGN KEY INTEGRITY
# ============================================================

def dq03_foreign_key(df, valid_company_ids):
    """
    DQ-03 CRITICAL

    Check that every company_id exists
    in the companies table.
    """

    if "company_id" not in df.columns:
        return pd.DataFrame()

    invalid = df[
        df["company_id"].isna()
        | ~df["company_id"].isin(valid_company_ids)
    ]

    return invalid

# ============================================================
# DQ-04: BALANCE SHEET BALANCE
# ============================================================

def dq04_balance_sheet(df, tolerance=0.01):
    """
    DQ-04 WARNING

    Check whether total_assets and total_liabilities
    differ by more than 1%.
    """

    required = ["total_assets", "total_liabilities"]

    if not all(col in df.columns for col in required):
        return pd.DataFrame()

    assets = pd.to_numeric(df["total_assets"], errors="coerce")
    liabilities = pd.to_numeric(df["total_liabilities"], errors="coerce")

    denominator = assets.abs().replace(0, pd.NA)

    difference_ratio = (
        (assets - liabilities).abs() / denominator
    )

    invalid = df[
        difference_ratio > tolerance
    ]

    return invalid


# ============================================================
# DQ-05: OPM CROSS-CHECK
# ============================================================

def dq05_opm_cross_check(df, tolerance=1.0):
    """
    DQ-05 WARNING

    Cross-check:
        OPM % = operating_profit / sales * 100

    A difference greater than 1 percentage point
    is treated as a validation failure.
    """

    required = [
        "sales",
        "operating_profit",
        "opm_percentage"
    ]

    if not all(col in df.columns for col in required):
        return pd.DataFrame()

    sales = pd.to_numeric(df["sales"], errors="coerce")
    operating_profit = pd.to_numeric(
        df["operating_profit"],
        errors="coerce"
    )
    reported_opm = pd.to_numeric(
        df["opm_percentage"],
        errors="coerce"
    )

    calculated_opm = (
        operating_profit / sales.replace(0, pd.NA)
    ) * 100

    difference = (
        calculated_opm - reported_opm
    ).abs()

    invalid = df[
        difference > tolerance
    ]

    return invalid


# ============================================================
# DQ-06: POSITIVE SALES
# ============================================================

def dq06_positive_sales(df):
    """
    DQ-06 WARNING

    Sales should be greater than zero.
    """

    if "sales" not in df.columns:
        return pd.DataFrame()

    sales = pd.to_numeric(
        df["sales"],
        errors="coerce"
    )

    return df[
        sales.notna()
        & (sales <= 0)
    ]


# ============================================================
# DQ-07: NET CASH FLOW CROSS-CHECK
# ============================================================

def dq07_net_cash_flow(df, tolerance=1.0):
    """
    DQ-07 WARNING

    Check:
        operating_activity
        + investing_activity
        + financing_activity
        ~= net_cash_flow
    """

    required = [
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow"
    ]

    if not all(col in df.columns for col in required):
        return pd.DataFrame()

    operating = pd.to_numeric(
        df["operating_activity"],
        errors="coerce"
    )

    investing = pd.to_numeric(
        df["investing_activity"],
        errors="coerce"
    )

    financing = pd.to_numeric(
        df["financing_activity"],
        errors="coerce"
    )

    reported = pd.to_numeric(
        df["net_cash_flow"],
        errors="coerce"
    )

    calculated = (
        operating
        + investing
        + financing
    )

    difference = (
        calculated - reported
    ).abs()

    return df[
        difference > tolerance
    ]


# ============================================================
# DQ-08: TAX RATE RANGE
# ============================================================

def dq08_tax_rate(df):
    """
    DQ-08 WARNING

    Tax percentage should normally be
    between 0 and 100.
    """

    if "tax_percentage" not in df.columns:
        return pd.DataFrame()

    tax = pd.to_numeric(
        df["tax_percentage"],
        errors="coerce"
    )

    return df[
        tax.notna()
        & (
            (tax < 0)
            | (tax > 100)
        )
    ]


# ============================================================
# DQ-09: DIVIDEND PAYOUT CAP
# ============================================================

def dq09_dividend_cap(df):
    """
    DQ-09 WARNING

    Dividend payout percentage should
    normally be between 0 and 100.
    """

    if "dividend_payout" not in df.columns:
        return pd.DataFrame()

    dividend = pd.to_numeric(
        df["dividend_payout"],
        errors="coerce"
    )

    return df[
        dividend.notna()
        & (
            (dividend < 0)
            | (dividend > 100)
        )
    ]


# ============================================================
# DQ-10: URL VALIDATION
# ============================================================

def dq10_url_validation(df, url_columns):
    """
    DQ-10 WARNING

    Non-null URLs must begin with
    http:// or https://.
    """

    failures = []

    for column in url_columns:

        if column not in df.columns:
            continue

        invalid = df[
            df[column].notna()
            & ~df[column]
                .astype(str)
                .str.strip()
                .str.startswith(
                    ("http://", "https://")
                )
        ].copy()

        if not invalid.empty:
            invalid["invalid_url_column"] = column
            failures.append(invalid)

    if not failures:
        return pd.DataFrame()

    return pd.concat(
        failures,
        ignore_index=True
    )


# ============================================================
# DQ-11: EPS SIGN CONSISTENCY
# ============================================================

def dq11_eps_sign(df):
    """
    DQ-11 WARNING

    EPS and net profit should normally
    have the same sign.

    Zero values are ignored.
    """

    required = ["eps", "net_profit"]

    if not all(col in df.columns for col in required):
        return pd.DataFrame()

    eps = pd.to_numeric(
        df["eps"],
        errors="coerce"
    )

    net_profit = pd.to_numeric(
        df["net_profit"],
        errors="coerce"
    )

    invalid = (
        eps.notna()
        & net_profit.notna()
        & (eps != 0)
        & (net_profit != 0)
        & (
            ((eps > 0) & (net_profit < 0))
            | ((eps < 0) & (net_profit > 0))
        )
    )

    return df[invalid]


# ============================================================
# DQ-12: BSE BALANCE / PROFILE COVERAGE
# ============================================================

def dq12_bse_coverage(df):
    """
    DQ-12 WARNING

    Check companies with missing BSE profile information.
    """

    if "bse_profile" not in df.columns:
        return pd.DataFrame()

    invalid = df[
        df["bse_profile"].isna()
        | df["bse_profile"]
            .astype(str)
            .str.strip()
            .eq("")
    ]

    return invalid


# ============================================================
# DQ-13: YEAR VALIDITY
# ============================================================

def dq13_year_validity(df):
    """
    DQ-13 WARNING

    Financial year must be a valid
    four-digit year after normalization.
    """

    if "year" not in df.columns:
        return pd.DataFrame()

    year = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    return df[
        year.isna()
        | (year < 1900)
        | (year > 2100)
    ]


# ============================================================
# DQ-14: COMPANY YEAR COVERAGE
# ============================================================

def dq14_year_coverage(df, minimum_years=5):
    """
    DQ-14 WARNING

    Identify companies with fewer than
    the required number of distinct years.
    """

    required = ["company_id", "year"]

    if not all(col in df.columns for col in required):
        return pd.DataFrame()

    coverage = (
        df.groupby("company_id")["year"]
        .nunique()
        .reset_index(name="year_count")
    )

    return coverage[
        coverage["year_count"] < minimum_years
    ]


# ============================================================
# DQ-15: COMPANY COVERAGE
# ============================================================

def dq15_company_coverage(df, valid_company_ids):
    """
    DQ-15 WARNING

    Identify companies from the master companies
    table that have no records in the dataset.
    """

    if "company_id" not in df.columns:
        return pd.DataFrame()

    present = set(
        df["company_id"]
        .dropna()
        .astype(str)
    )

    missing = [
        company_id
        for company_id in valid_company_ids
        if str(company_id) not in present
    ]

    return pd.DataFrame(
        {"company_id": missing}
    )


# ============================================================
# DQ-16: REQUIRED FIELD COVERAGE
# ============================================================

def dq16_required_field_coverage(
    df,
    required_columns
):
    """
    DQ-16 WARNING

    Identify rows where required fields
    contain null values.
    """

    existing_columns = [
        column
        for column in required_columns
        if column in df.columns
    ]

    if not existing_columns:
        return pd.DataFrame()

    invalid = df[
        df[existing_columns]
        .isna()
        .any(axis=1)
    ]

    return invalid