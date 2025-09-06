# tests/test_connectivity.py

import pytest
import requests
from api_client.client import AlphaVantageClient

def test_api_endpoint_is_live():
    '''
    Tests if the base Alpha Vantage URL is reachable and returns a success status code.
    This is a basic smoke test to check for network or service availability issues.
    '''
    response = requests.get("https://www.alphavantage.co/")
    assert response.status_code == 200, "Alpha Vantage homepage is not accessible."

def test_client_instantiation_successful():
    '''
    Checks the happy path!
    Tests if the AlphaVantageClient can be instantiated correctly.
    This implicitly checks if the API key is being loaded from the environment.
    '''
    try:
        client = AlphaVantageClient() #if this is unsuccessful client.py raises a ValueError
        assert client is not None
    except ValueError as e: #we are catching the value error here
        pytest.fail(f"Client instantiation failed: {e}")

def test_client_instantiation_with_mocker(mocker):
    """
    Tests that the client correctly uses the API key returned by os.getenv,
    using a mock to avoid relying on a real environment variable.
    """
    # 1. Intercept the call to "os.getenv" and create a mock object
    mock_getenv = mocker.patch("os.getenv")

    # 2. Tell the mock what value to return when it's called
    mock_getenv.return_value = "MOCK_API_KEY_123"

    # 3. Instantiate the client. When __init__ calls os.getenv, it will get our mock value.
    client = AlphaVantageClient()

    # 4. Assert that the mock was called correctly
    mock_getenv.assert_called_once_with("ALPHAVANTAGE_API_KEY")

    # 5. Assert that the client's api_key attribute was set to our mock value
    assert client.api_key == "MOCK_API_KEY_123"

def test_client_instantiation_fails_without_api_key(monkeypatch):
    '''
    Tests that the client raises a ValueError if the API key is not set.
    Monkey patch used to temporarily modify code or the environment for the duration of a single test.
    
    monkeypatch.delenv("ALPHAVANTAGE_API_KEY", raising=False): This line uses monkeypatch to delete 
    the ALPHAVANTAGE_API_KEY environment variable. The raising=False argument prevents the test from 
    failing if the variable doesn't exist in the first place.
    '''
    monkeypatch.delenv("ALPHAVANTAGE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="ALPHAVANTAGE_API_KEY environment variable not set."): 
        AlphaVantageClient()

# The equivalent test for monkeypatch written using mocker!
# def test_client_instantiation_fails_with_mocked_none(mocker):
#     # Action: Intercepts os.getenv and tells it to return None
#     mock_getenv = mocker.patch("os.getenv")
#     mock_getenv.return_value = None
    
#     with pytest.raises(ValueError):
#         AlphaVantageClient()