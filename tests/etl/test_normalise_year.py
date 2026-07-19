import pytest

from src.etl.normalizer import normalize_year


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (2024, 2024),
        (2023, 2023),
        ("2024", 2024),
        ("2023", 2023),
        (" 2024 ", 2024),
        ("FY2024", 2024),
        ("FY2023", 2023),
        ("FY 2024", 2024),
        ("FY 2023", 2023),
        ("fy2024", 2024),
        ("fy 2023", 2023),
        ("FY-2024", 2024),
        ("2023-24", 2024),
        ("2022-23", 2023),
        ("2023/24", 2024),
        ("2022/23", 2023),
        (None, None),
        ("", None),
        ("   ", None),
        ("invalid", None),
    ],
)
def test_normalize_year(input_value, expected):
    assert normalize_year(input_value) == expected