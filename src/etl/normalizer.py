import re
import pandas as pd


def normalize_year(value):
    """
    Normalize financial year/date labels to a four-digit year.

    Examples:
        2024          -> 2024
        "2024"        -> 2024
        "FY2024"      -> 2024
        "2023-24"     -> 2024
        "Mar 2024"    -> 2024
        "Dec 2012"    -> 2012
        "Sep 2024"    -> 2024
        "Mar-24"      -> 2024
        "Mar 2016 9m" -> 2016
        "Mar 2023 15" -> 2023
        "TTM"         -> None
    """

    if value is None or pd.isna(value):
        return None

    text = str(value).strip()

    if not text:
        return None

    # TTM is not a specific financial year
    if text.upper() == "TTM":
        return None

    # Four-digit year
    if re.fullmatch(r"\d{4}", text):
        return int(text)

    # FY2024 / FY 2024 / FY-2024
    match = re.fullmatch(
        r"FY[\s-]*(\d{4})",
        text,
        flags=re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    # 2023-24 / 2023/24
    match = re.fullmatch(
        r"(\d{4})[-/](\d{2})",
        text
    )

    if match:
        start_year = int(match.group(1))
        end_short = int(match.group(2))

        century = (start_year // 100) * 100
        end_year = century + end_short

        if end_year < start_year:
            end_year += 100

        return end_year

    # Extract four-digit year from:
    # Mar 2024
    # Dec 2012
    # Mar 2016 9m
    # Mar 2023 15
    match = re.search(
        r"\b(19|20)\d{2}\b",
        text
    )

    if match:
        return int(match.group(0))

    # Month + two-digit year:
    # Mar-24 / Mar-13
    match = re.fullmatch(
        r"[A-Za-z]{3}[-\s](\d{2})",
        text
    )

    if match:
        short_year = int(match.group(1))

        if short_year <= 50:
            return 2000 + short_year

        return 1900 + short_year

    return None


def normalize_ticker(value):
    """
    Normalize company ticker symbols.

    Examples:
        "TCS"       -> "TCS"
        " tcs "     -> "TCS"
        "NSE:TCS"   -> "TCS"
        "BSE:TCS"   -> "TCS"
        "TCS.NS"    -> "TCS"
        "500325.BO" -> "500325"
    """

    if value is None or pd.isna(value):
        return None

    ticker = str(value).strip().upper()

    if not ticker:
        return None

    # Remove NSE/BSE prefixes
    ticker = re.sub(
        r"^(NSE|BSE)\s*:\s*",
        "",
        ticker
    )

    # Remove Yahoo Finance exchange suffixes
    ticker = re.sub(
        r"\.(NS|BO)$",
        "",
        ticker
    )

    ticker = ticker.strip()

    if not ticker:
        return None
    
    ticker_aliases = {
    "AGTL": "ATGL",
    }

    ticker = ticker_aliases.get(
        ticker,
        ticker
    )

    return ticker