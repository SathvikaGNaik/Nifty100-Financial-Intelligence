from pathlib import Path

import pandas as pd

from src.etl.loader import (
    load_all_core_files,
    load_excel,
    filter_to_company_master,
)

from src.etl.config import SUPPORTING_FILES


OUTPUT_DIR = Path("output")

AUDIT_FILE = OUTPUT_DIR / "load_audit.csv"

REJECTION_DIR = OUTPUT_DIR / "rejections"


def prepare_datasets_for_database():
    """
    Prepare all datasets for SQLite loading.

    Returns
    -------
    prepared_datasets
    rejected_datasets
    audit_dataframe
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    REJECTION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------
    # Load Core Files
    # -----------------------------------------

    datasets = load_all_core_files()

    # -----------------------------------------
    # Load Supporting Files
    # -----------------------------------------

    for table_name, file_path in SUPPORTING_FILES.items():

        datasets[table_name] = load_excel(
            file_path,
            header=0
        )

    # -----------------------------------------
    # Company Master
    # -----------------------------------------

    companies = datasets["companies"]

    master_ids = set(

        companies["id"]

        .dropna()

        .astype(str)

    )

    prepared_datasets = {}

    rejected_datasets = {}

    audit_rows = []

    # -----------------------------------------
    # Prepare Every Dataset
    # -----------------------------------------

    for table_name, df in datasets.items():

        source_rows = len(df)

        # Companies table
        if table_name == "companies":

            prepared = df.copy()

            rejected = pd.DataFrame(
                columns=df.columns
            )

        # Tables having company_id
        elif "company_id" in df.columns:

            prepared, rejected = (
                filter_to_company_master(
                    df,
                    master_ids
                )
            )

        # Tables without FK
        else:

            prepared = df.copy()

            rejected = pd.DataFrame(
                columns=df.columns
            )
        
        # Remove duplicate company/year records
        if (
            table_name == "financial_ratios"
            and "company_id" in prepared.columns
            and "year" in prepared.columns
        ):

            before = len(prepared)

            prepared = prepared.drop_duplicates(
                subset=["company_id", "year"],
                keep="first"
            )

            print(
                f"Removed {before-len(prepared)} duplicate rows "
                f"from financial_ratios."
            )
        prepared_datasets[table_name] = prepared

        rejected_datasets[table_name] = rejected

        loaded_rows = len(prepared)

        rejected_rows = len(rejected)

        if rejected_rows > 0:

            rejected.to_csv(

                REJECTION_DIR /

                f"{table_name}_rejected.csv",

                index=False

            )

        audit_rows.append(

            {

                "table": table_name,

                "source_rows": source_rows,

                "loaded_rows": loaded_rows,

                "rejected_rows": rejected_rows,

                "status": (

                    "READY"

                    if rejected_rows == 0

                    else "READY_WITH_REJECTIONS"

                )

            }

        )

    audit_df = pd.DataFrame(audit_rows)

    audit_df.to_csv(

        AUDIT_FILE,

        index=False

    )

    return (

        prepared_datasets,

        rejected_datasets,

        audit_df

    )