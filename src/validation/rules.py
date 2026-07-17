import pandas as pd


def check_missing_columns(df, required_columns):
    """Return a list of missing required columns."""
    return [col for col in required_columns if col not in df.columns]


def check_duplicate_rows(df):
    """Return duplicate rows."""
    return df[df.duplicated()]


def check_missing_values(df):
    """Return missing value count per column."""
    return df.isnull().sum()

def check_duplicate_ids(df, id_column="id"):
    """
    Return duplicate IDs in the specified column.
    """

    if id_column not in df.columns:
        return []

    duplicate_ids = df[df[id_column].duplicated()][id_column].tolist()

    return duplicate_ids

def check_empty_strings(df):
    """
    Count empty strings in object columns.
    """

    empty_counts = {}

    for col in df.select_dtypes(include="object").columns:
        count = df[col].astype(str).str.strip().eq("").sum()

        if count > 0:
            empty_counts[col] = int(count)

    return empty_counts

def check_invalid_urls(df, url_columns):
    """
    Check whether URL columns start with http:// or https://.
    """

    invalid_urls = {}

    for column in url_columns:

        if column not in df.columns:
            continue

        invalid = df[
            df[column].notna() &
            ~df[column].astype(str).str.startswith(("http://", "https://"))
        ]

        if not invalid.empty:
            invalid_urls[column] = len(invalid)

    return invalid_urls


def check_numeric_columns(df, numeric_columns):
    """
    Check if specified columns contain numeric values.
    Returns a dictionary with the count of invalid values.
    """

    invalid_counts = {}

    for column in numeric_columns:

        if column not in df.columns:
            continue

        invalid = pd.to_numeric(df[column], errors="coerce").isna() & df[column].notna()

        count = invalid.sum()

        if count > 0:
            invalid_counts[column] = int(count)

    return invalid_counts