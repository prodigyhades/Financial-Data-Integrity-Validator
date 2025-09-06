# tests/test_data_quality.py

import pytest
from tests.test_schema_validation import stock_data

# --- Parametrized Tests ---

POSITIVE_PRICE_COLUMNS = ['open', 'high', 'low', 'close']
@pytest.mark.parametrize("column_name", POSITIVE_PRICE_COLUMNS)
def test_prices_are_positive(stock_data, column_name):
    """
    - Validates that price-related columns contain only positive values.
    - This test runs once for each column in POSITIVE_PRICE_COLUMNS.
    """
    assert (stock_data[column_name] > 0).all(), \
        f"Found non-positive values in column '{column_name}'."

@pytest.mark.parametrize("other_column", ['open', 'close'])
def test_high_is_daily_maximum(stock_data, other_column):
    """
    - Ensures the 'high' price is the maximum for the day compared to open and close.
    - This test runs twice, comparing 'high' with 'open' and then 'high' with 'close'.
    """
    assert (stock_data['high'] >= stock_data[other_column]).all(), \
        f"Found instances where '{other_column}' price is greater than the 'high' price."

@pytest.mark.parametrize("other_column", ['open', 'close'])
def test_low_is_daily_minimum(stock_data, other_column):
    """
    - Ensures the 'low' price is the minimum for the day compared to open and close.
    - This test runs twice, comparing 'low' with 'open' and then 'low' with 'close'.
    """
    assert (stock_data['low'] <= stock_data[other_column]).all(), \
        f"Found instances where '{other_column}' price is less than the 'low' price."

# --- Standard, Non-Parametrized Tests ---

def test_volume_is_non_negative(stock_data):
    """
    - Validates that the trading volume is always non-negative (zero or positive).
    """
    assert (stock_data['volume'] >= 0).all(), "Found negative values in the 'volume' column."

def test_high_is_greater_than_or_equal_to_low(stock_data): 
    """
    - A critical data integrity check: 'high' must be >= 'low'.
    - Explicitly tests the fundamental high >= low rule to provide a clear 
    test name and a more specific error message for faster debugging.
    """
    assert (stock_data['high'] >= stock_data['low']).all(), \
        "Found instances where the 'low' price is greater than the 'high' price."
    

'''
========================== Without using pytest.mark.parameterize ===========================


def test_prices_are_positive(stock_data):
    """
    Validates that all price-related columns (open, high, low, close) contain
    only positive values.
    """
    price_columns = ['open', 'high', 'low', 'close']
    for col in price_columns:
        assert (stock_data[col] > 0).all(), f"Found non-positive values in column '{col}'."

def test_volume_is_non_negative(stock_data):
    """
    Validates that the trading volume is always non-negative (zero or positive).
    Negative volume is not possible.
    """
    assert (stock_data['volume'] >= 0).all(), "Found negative values in the 'volume' column."

def test_high_is_greater_than_or_equal_to_low(stock_data):
    """
    A critical data integrity check for OHLC (Open, High, Low, Close) data.
    The 'high' price for any given day must be greater than or equal to the 'low' price.
    """
    assert (stock_data['high'] >= stock_data['low']).all(), \
        "Found instances where the 'low' price is greater than the 'high' price."

def test_high_is_greater_than_or_equal_to_open_and_close(stock_data):
    """
    Ensures the 'high' price is the maximum for the day, meaning it must be
    greater than or equal to both the 'open' and 'close' prices.
    """
    assert (stock_data['high'] >= stock_data['open']).all(), \
        "Found instances where the 'open' price is greater than the 'high' price."
    assert (stock_data['high'] >= stock_data['close']).all(), \
        "Found instances where the 'close' price is greater than the 'high' price."
        
def test_low_is_less_than_or_equal_to_open_and_close(stock_data):

    """
    Ensures the 'low' price is the minimum for the day, meaning it must be
    less than or equal to both the 'open' and 'close' prices.
    """
    assert (stock_data['low'] <= stock_data['open']).all(), \
        "Found instances where the 'open' price is less than the 'low' price."
    assert (stock_data['low'] <= stock_data['close']).all(), \
        "Found instances where the 'close' price is less than the 'low' price."

'''