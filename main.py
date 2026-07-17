from src.etl.loader import load_all_core_files
from src.validation.validator import validate_dataset
from src.validation.config import VALIDATION_CONFIG
from src.database.data_loader import DataLoader

def main():
    datasets = load_all_core_files()
    loader = DataLoader()

    for name, df in datasets.items():
        print(f"\nProcessing {name}...")

        config = VALIDATION_CONFIG.get(name, {})
        report = validate_dataset(df, config)

        if report["missing_columns"]:
            print(f"Skipping {name}: missing required columns.")
            continue

        loader.load_table(df, name)

    loader.close()
    print("\nETL Pipeline Completed Successfully.")

if __name__ == "__main__":
    main()