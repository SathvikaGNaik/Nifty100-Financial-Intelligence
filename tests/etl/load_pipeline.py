from pathlib import Path

import pandas as pd

from src.etl.loader import (
    load_all_core_files,
    load_excel,
    filter_to_company_master,
)

from src.etl.config import SUPPORTING_FILES
from src.database.data_loader import DataLoader


OUTPUT_DIR = Path("output")

AUDIT_FILE = OUTPUT_DIR / "load_audit.csv"

REJECTION_DIR = OUTPUT_DIR / "rejections"


def prepare_datasets_for_database():
    """
    Prepare validated datasets and load them into SQLite.

    Steps
    -----
    1. Load all core datasets
    2. Load all supporting datasets
    3. Remove FK-invalid rows from core datasets
    4. Save rejected rows
    5. Generate load_audit.csv
    6. Load everything into SQLite

    Returns
    -------
    prepared_datasets
    rejected_datasets
    audit_df
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    REJECTION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # Load Core Files
    # --------------------------------------------------

    datasets = load_all_core_files()
    
    from src.etl.config import SUPPORTING_FILES
    from src.etl.loader import load_excel

    for dataset_name, file_path in SUPPORTING_FILES.items():

        datasets[dataset_name] = load_excel(
            file_path,
            header=0
         )
    # --------------------------------------------------
    # Load Supporting Files
    # --------------------------------------------------

    for dataset_name, file_path in SUPPORTING_FILES.items():

        datasets[dataset_name] = load_excel(
            file_path,
            header=0
        )

    # --------------------------------------------------
    # Company Master
    # --------------------------------------------------

    if "companies" not in datasets:

        raise RuntimeError(
            "companies dataset must exist."
        )

    companies = datasets["companies"]

    master_ids = set(

        companies["id"]
        .dropna()
        .astype(str)
        .str.strip()

    )

    prepared_datasets = {}

    rejected_datasets = {}

    audit_rows = []

    # --------------------------------------------------
    # Prepare Core Tables
    # --------------------------------------------------

    for table_name, df in datasets.items():

        source_rows = len(df)

        # Supporting datasets are loaded directly
        if table_name in SUPPORTING_FILES:

            prepared = df.copy()

            rejected = pd.DataFrame(
                columns=df.columns
            )

        elif table_name == "companies":

            prepared = df.copy()

            rejected = pd.DataFrame(
                columns=df.columns
            )

        else:

            prepared, rejected = filter_to_company_master(

                df,

                master_ids

            )

        prepared_datasets[table_name] = prepared

        rejected_datasets[table_name] = rejected

        loaded_rows = len(prepared)

        rejected_rows = len(rejected)

        if rejected_rows > 0:

            rejection_file = (

                REJECTION_DIR /

                f"{table_name}_rejected.csv"

            )

            rejected.to_csv(

                rejection_file,

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

    # --------------------------------------------------
    # Load SQLite
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("LOADING SQLITE DATABASE")
    print("=" * 60)

    loader = DataLoader()

    load_order = [

        "companies",

        "profitandloss",

        "balancesheet",

        "cashflow",

        "analysis",

        "documents",

        "prosandcons",

        "sectors",

        "peer_groups",

        "financial_ratios",

        "market_cap",

        "stock_prices",

    ]

    for table_name in load_order:

        if table_name not in prepared_datasets:
            continue

        print(f"\nLoading {table_name}...")

        loader.load_table(

            prepared_datasets[table_name],

            table_name

        )

    loader.close()

    print("\n" + "=" * 60)
    print("LOAD COMPLETED")
    print("=" * 60)

    print(audit_df)

    return (

        prepared_datasets,

        rejected_datasets,

        audit_df,

    )


if __name__ == "__main__":

    prepare_datasets_for_database()