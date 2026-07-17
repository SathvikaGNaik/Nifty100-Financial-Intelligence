from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data folders
RAW_DATA = PROJECT_ROOT / "data" / "raw"
SUPPORTING_DATA = PROJECT_ROOT / "data" / "supporting"

# Core datasets
CORE_FILES = {
    "companies": RAW_DATA / "companies.xlsx",
    "profitandloss": RAW_DATA / "profitandloss.xlsx",
    "balancesheet": RAW_DATA / "balancesheet.xlsx",
    "cashflow": RAW_DATA / "cashflow.xlsx",
    "analysis": RAW_DATA / "analysis.xlsx",
    "documents": RAW_DATA / "documents.xlsx",
    "prosandcons": RAW_DATA / "prosandcons.xlsx",
}

# Supplementary datasets
SUPPLEMENTARY_FILES = {
    "sectors": SUPPORTING_DATA / "sectors.xlsx",
    "stock_prices": SUPPORTING_DATA / "stock_prices.xlsx",
    "market_cap": SUPPORTING_DATA / "market_cap.xlsx",
    "financial_ratios": SUPPORTING_DATA / "financial_ratios.xlsx",
    "peer_groups": SUPPORTING_DATA / "peer_groups.xlsx",
}