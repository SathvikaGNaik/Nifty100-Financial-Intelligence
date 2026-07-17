import re
from datetime import datetime


def normalize_ticker(ticker: str) -> str:
    """
    Normalize NSE ticker symbols.
    Example: " tcs " -> "TCS"
    """
    if ticker is None:
        return ""

    ticker = str(ticker).strip()
    ticker = ticker.replace("\n", "")
    ticker = ticker.upper()
    ticker = re.sub(r"\s+", "", ticker)

    return ticker


def normalize_year(year):
    """
    Convert values like:
        Mar-24 -> 2024-03
        Dec-23 -> 2023-12
    """

    if year is None:
        return None

    year = str(year).strip()

    try:
        date = datetime.strptime(year, "%b-%y")
        return date.strftime("%Y-%m")
    except ValueError:
        return year