# tests/test_schema_validation.py

import pytest
import pandas as pd
from api_client.client import AlphaVantageClient

@pytest.fixture(scope="module")
def stock_data():
    """
    Pytest fixture to fetch data for a common stock (IBM) once per test module.
    This avoids hitting the API repeatedly for each test function, making tests
    faster and respecting API rate limits. 'scope="module"' means this fixture
    runs only once for all tests in this file.
    """
    client = AlphaVantageClient()
    try:
        # Calls the updated get_daily method
        data = client.get_daily('IBM')
        return data
    except ValueError as e:
        pytest.fail(f"API call failed during test setup: {e}")

def test_response_is_a_pandas_dataframe(stock_data):
    """
    Validates that the client method returns a pandas DataFrame object.
    """
    assert isinstance(stock_data, pd.DataFrame), "The returned data is not a pandas DataFrame."

def test_dataframe_is_not_empty(stock_data):
    """
    Ensures that the returned DataFrame contains data.
    """
    assert not stock_data.empty, "The DataFrame should not be empty."

def test_dataframe_has_expected_columns(stock_data):
    """
    Validates that the DataFrame contains all the expected columns after renaming.
    This is the test that was failing and is now corrected.
    """
    expected_columns = [
        'open', 'high', 'low', 'close', 'volume'
    ]
    assert all(col in stock_data.columns for col in expected_columns), \
        f"DataFrame is missing one or more expected columns. Found: {stock_data.columns.tolist()}"

def test_dataframe_index_is_datetime(stock_data):
    """
    Verifies that the DataFrame index is of type DatetimeIndex, which is
    essential for time-series analysis.
    """
    assert isinstance(stock_data.index, pd.DatetimeIndex), "DataFrame index is not a DatetimeIndex."

def test_column_data_types_are_correct(stock_data):
    """
    Checks the data types (dtypes) of key columns to ensure they are numeric,
    which is necessary for any subsequent calculations.
    """
    assert pd.api.types.is_numeric_dtype(stock_data['open']), "Column 'open' is not numeric."
    assert pd.api.types.is_numeric_dtype(stock_data['high']), "Column 'high' is not numeric."
    assert pd.api.types.is_numeric_dtype(stock_data['low']), "Column 'low' is not numeric."
    assert pd.api.types.is_numeric_dtype(stock_data['close']), "Column 'close' is not numeric."
    assert pd.api.types.is_numeric_dtype(stock_data['volume']), "Column 'volume' is not numeric."