from pathlib import Path

import pandas as pd

from src.etl.config import CORE_FILES, SUPPORTING_FILES
from src.etl.normalizer import normalize_year, normalize_ticker
from src.utils.logger import get_logger


logger = get_logger(__name__)


def load_excel(file_path, header=1, required_columns=None):
    """
    Load an Excel file, clean it,
    and optionally validate required columns.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"{file_path} not found."
        )

    df = pd.read_excel(
        file_path,
        header=header
    )

    # Clean column names
    df.columns = df.columns.str.strip()

    # Clean string columns
    for col in df.select_dtypes(
        include="object"
    ).columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(
                "\n",
                " ",
                regex=False
            )
            .str.replace(
                "\r",
                " ",
                regex=False
            )
            .str.strip()
        )

    # Validate required columns
    if required_columns:

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

    return df


def normalize_dataframe(
    df,
    dataset_name
):
    """
    Normalize ticker and year fields.

    The original year value is preserved
    in year_raw for auditing purposes.
    """

    df = df.copy()

    # Normalize company master ticker
    if (
        dataset_name == "companies"
        and "id" in df.columns
    ):
        df["id"] = df["id"].apply(
            normalize_ticker
        )

    # Normalize company foreign key
    if "company_id" in df.columns:

        df["company_id"] = (
            df["company_id"]
            .apply(normalize_ticker)
        )

    # Normalize financial year
    if "year" in df.columns:

        # Preserve original source value
        df["year_raw"] = df["year"]

        # Create normalized year
        df["year"] = (
            df["year"]
            .apply(normalize_year)
        )
    
        # Normalize stock price dates
    if dataset_name == "stock_prices" and "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")
    return df


def prepare_annual_financial_data(df, dataset_name):
    """
    Prepare annual financial datasets for tables that use
    (company_id, year) as the logical key.

    Rules:
    - Exclude TTM because it is not a financial year.
    - Prefer Mar annual records when multiple reporting periods
      exist for the same company and year.
    - Remove duplicated source periods.
    """

    annual_tables = {
        "profitandloss",
        "balancesheet",
        "cashflow"
    }

    if dataset_name not in annual_tables:
        return df

    if not all(
        col in df.columns
        for col in ["company_id", "year", "year_raw"]
    ):
        return df

    df = df.copy()

    # --------------------------------------------------------
    # Remove records without a normalized financial year.
    # This excludes TTM rows from annual tables.
    # --------------------------------------------------------

    df = df[
        df["year"].notna()
    ].copy()

    # --------------------------------------------------------
    # Remove duplicate source periods.
    #
    # Example:
    # ADANIPORTS | Mar 2013
    # ADANIPORTS | Mar 2013
    # --------------------------------------------------------

    df = df.drop_duplicates(
        subset=[
            "company_id",
            "year_raw"
        ],
        keep="first"
    )

    # --------------------------------------------------------
    # Assign reporting-period priority.
    #
    # March is preferred because most Indian companies use
    # March as their annual financial year end.
    #
    # December and June may represent valid annual periods
    # for companies with different reporting cycles.
    #
    # September is generally an interim period when a March
    # annual record exists for the same normalized year.
    # --------------------------------------------------------

    def period_priority(value):

        value = str(value).strip().lower()

        if value.startswith("mar"):
            return 1

        if value.startswith("dec"):
            return 2

        if value.startswith("jun"):
            return 3

        if value.startswith("sep"):
            return 4

        return 5

    df["_period_priority"] = (
        df["year_raw"]
        .apply(period_priority)
    )

    # --------------------------------------------------------
    # Sort so preferred annual period comes first.
    # --------------------------------------------------------

    df = df.sort_values(
        by=[
            "company_id",
            "year",
            "_period_priority"
        ]
    )

    # --------------------------------------------------------
    # Keep one annual record per company/year.
    # --------------------------------------------------------

    df = df.drop_duplicates(
        subset=[
            "company_id",
            "year"
        ],
        keep="first"
    )

    # Remove temporary helper column
    df = df.drop(
        columns=["_period_priority"]
    )

    # Reset DataFrame index
    df = df.reset_index(
        drop=True
    )

    return df


def filter_to_company_master(df, master_ids):
    """
    Keep only records whose company_id exists in the
    companies master dataset.

    This function is intended for preparing data for
    database loading after raw DQ validation.

    Source data itself is never modified.
    """

    if "company_id" not in df.columns:
        return df.copy(), pd.DataFrame()

    df = df.copy()

    valid_mask = df["company_id"].isin(master_ids)

    accepted = df[valid_mask].copy()

    rejected = df[~valid_mask].copy()

    return (
        accepted.reset_index(drop=True),
        rejected.reset_index(drop=True),
    )

def load_all_core_files():
    """
    Load and normalize all core datasets
    defined in config.py.

    Returns:
        Dictionary of normalized DataFrames.
    """

    datasets = {}

    for name, path in CORE_FILES.items():

        try:

            logger.info(
                f"Loading {name}"
            )

            # Load raw Excel data
            df = load_excel(path)

            # Normalize ticker and year
            df = normalize_dataframe(
            df,
            name
            )

            df = prepare_annual_financial_data(
            df,
            name
            )

            datasets[name] = df

        except FileNotFoundError:

            logger.warning(
                f"Skipped {name} "
                "(file not found)"
            )

    return datasets


def load_all_supporting_files():
    """
    Load all supporting datasets defined in config.py.

    Returns
    -------
    dict
        Dictionary containing dataset name -> DataFrame.
    """

    datasets = {}

    for name, path in SUPPORTING_FILES.items():

        try:

            logger.info(f"Loading {name}")

            datasets[name] = load_excel(
                path,
                header=0
            )

        except FileNotFoundError:

            logger.warning(
                f"Skipped {name} (file not found)"
            )

    return datasets