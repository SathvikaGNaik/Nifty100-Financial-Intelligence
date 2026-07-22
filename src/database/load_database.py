from src.database.data_loader import DataLoader
from src.etl.load_pipeline import prepare_datasets_for_database


def load_database():

    prepared_datasets, rejected_datasets, audit_df = (
        prepare_datasets_for_database()
    )

    loader = DataLoader()

    loader.clear_database()

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

    print("\n" + "=" * 60)
    print("LOADING DATABASE")
    print("=" * 60)

    for table in load_order:

        if table not in prepared_datasets:
            continue

        print(f"\nLoading {table}")

        loader.load_table(
            prepared_datasets[table],
            table
        )

    loader.close()

    print("\nDatabase loaded successfully.")

    return audit_df


if __name__ == "__main__":

    load_database()