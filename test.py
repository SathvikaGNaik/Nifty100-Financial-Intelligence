from src.etl.loader import load_all_core_files

datasets = load_all_core_files()

print("\nDatasets Loaded:\n")

for name, df in datasets.items():
    print(f"{name}: {df.shape}")