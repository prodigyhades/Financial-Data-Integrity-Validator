# tests/test_connectivity.py

import pytest
import requests
from api_client.client import AlphaVantageClient

def test_api_endpoint_is_live():
    """
    Tests if the base Alpha Vantage URL is reachable and returns a success status code.
    This is a basic smoke test to check for network or service availability issues.
    """
    response = requests.get("https://www.alphavantage.co/")
    assert response.status_code == 200, "Alpha Vantage homepage is not accessible."

def test_client_instantiation_successful():
    """
    Tests if the AlphaVantageClient can be instantiated correctly.
    This implicitly checks if the API key is being loaded from the environment.
    """
    try:
        client = AlphaVantageClient()
        assert client is not None
    except ValueError as e:
        pytest.fail(f"Client instantiation failed: {e}")

def test_client_instantiation_fails_without_api_key(monkeypatch):
    """
    Tests that the client raises a ValueError if the API key is not set.
    'monkeypatch' is a pytest fixture to safely modify environment variables for a test.
    """
    monkeypatch.delenv("ALPHAVANTAGE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="ALPHAVANTAGE_API_KEY environment variable not set."):
        AlphaVantageClient()