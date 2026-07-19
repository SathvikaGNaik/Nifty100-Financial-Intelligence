import pytest

from src.etl.normalizer import normalize_ticker


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("TCS", "TCS"),
        ("tcs", "TCS"),
        (" tcs ", "TCS"),
        ("INFY", "INFY"),
        ("infy", "INFY"),
        ("HDFCBANK", "HDFCBANK"),
        ("NSE:TCS", "TCS"),
        ("NSE:INFY", "INFY"),
        ("nse:tcs", "TCS"),
        ("BSE:TCS", "TCS"),
        ("TCS.NS", "TCS"),
        ("INFY.NS", "INFY"),
        ("500325.BO", "500325"),
        (None, None),
        ("", None),
    ],
)
def test_normalize_ticker(input_value, expected):

    assert normalize_ticker(input_value) == expected