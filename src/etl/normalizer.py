import re
import pandas as pd


def normalize_year(value):
    """
    Normalize different year formats into a 4-digit integer.

    Examples:
        2024 -> 2024
        "2024" -> 2024
        "FY2024" -> 2024
        "FY 2024" -> 2024
        "2023-24" -> 2024
        "2023/24" -> 2024
        None -> None
    """

    if value is None or pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    # Simple four-digit year
    match = re.fullmatch(r"\d{4}", value)

    if match:
        return int(value)

    # FY2024 / FY 2024 / FY-2024
    match = re.fullmatch(
        r"FY[\s-]*(\d{4})",
        value,
        flags=re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    # 2023-24 / 2023/24
    match = re.fullmatch(
        r"(\d{4})[-/](\d{2})",
        value
    )

    if match:
        start_year = int(match.group(1))
        end_short = int(match.group(2))

        century = (start_year // 100) * 100
        end_year = century + end_short

        if end_year < start_year:
            end_year += 100

        return end_year

    return None


def normalize_ticker(value):
    """
    Normalize company ticker symbols.

    Examples:
        " tcs " -> "TCS"
        "NSE:TCS" -> "TCS"
        "TCS.NS" -> "TCS"
        "500325.BO" -> "500325"
    """

    if value is None or pd.isna(value):
        return None

    ticker = str(value).strip().upper()

    if not ticker:
        return None

    # Remove exchange prefixes
    ticker = re.sub(
        r"^(NSE|BSE)\s*:\s*",
        "",
        ticker
    )

    # Remove Yahoo Finance suffixes
    ticker = re.sub(
        r"\.(NS|BO)$",
        "",
        ticker
    )

    # Remove unwanted surrounding whitespace again
    ticker = ticker.strip()

    if not ticker:
        return None

    return ticker