from pathlib import Path
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_excel(file_path, header=1, required_columns=None):
    """
    Load an Excel file, clean it, and optionally validate columns.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    df = pd.read_excel(file_path, header=header)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Clean string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("\n", " ", regex=False)
            .str.replace("\r", " ", regex=False)
            .str.strip()
        )

    # Validate required columns
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    return df

from src.etl.config import CORE_FILES


def load_all_core_files():
    """
    Load all core datasets defined in config.py.
    Returns a dictionary of DataFrames.
    """

    datasets = {}

    for name, path in CORE_FILES.items():
        try:
            logger.info(f"Loading {name}")
            datasets[name] = load_excel(path)
        except FileNotFoundError:
            logger.warning(f"Skipped {name} (file not found)")

    return datasets