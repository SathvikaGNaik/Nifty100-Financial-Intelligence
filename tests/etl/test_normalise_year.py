import pytest

from src.etl.normalizer import normalize_year


@pytest.mark.parametrize(
    "input_value, expected",
    [
        # Standard integer years
        (2024, 2024),
        (2023, 2023),

        # Standard string years
        ("2024", 2024),
        ("2023", 2023),
        (" 2024 ", 2024),

        # FY formats
        ("FY2024", 2024),
        ("FY2023", 2023),
        ("FY 2024", 2024),
        ("FY 2023", 2023),
        ("fy2024", 2024),
        ("fy 2023", 2023),
        ("FY-2024", 2024),

        # Financial year ranges
        ("2023-24", 2024),
        ("2022-23", 2023),
        ("2023/24", 2024),
        ("2022/23", 2023),

        # Actual formats found in project datasets
        ("Mar 2024", 2024),
        ("Dec 2012", 2012),
        ("Sep 2024", 2024),
        ("Jun 2013", 2013),

        # Short year formats found in cashflow
        ("Mar-24", 2024),
        ("Mar-13", 2013),

        # Special source-data formats
        ("Mar 2016 9m", 2016),
        ("Mar 2023 15", 2023),

        # TTM is not a specific financial year
        ("TTM", None),

        # Missing / invalid values
        (None, None),
        ("", None),
        ("   ", None),
        ("invalid", None),
    ],
)
def test_normalize_year(input_value, expected):
    assert normalize_year(input_value) == expected