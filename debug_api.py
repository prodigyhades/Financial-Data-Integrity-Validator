# debug_api.py

from api_client.client import AlphaVantageClient

print("--- Starting API Connection Test ---")
print("Attempting to create AlphaVantageClient...")

try:
    # This will initialize the client and load the key from your.env file
    client = AlphaVantageClient()
    print("Client created successfully. API key has been loaded.")
    print("Attempting to fetch data for symbol 'IBM' from Alpha Vantage...")
    
    # This is the function call that is failing in the tests
    stock_data = client.get_daily_adjusted('IBM')
    
    print("\n✅ --- SUCCESS! --- ✅")
    print("Successfully retrieved data from the API.")
    print("Here is a sample of the data:")
    print(stock_data.head())

except Exception as e:
    print("\n❌ --- ERROR! --- ❌")
    print("The API call failed. Here is the exact error message from the server:")
    print(f"Error details: {e}")
    print("\n--- Next Steps ---")
    print("1. The most common cause is an invalid API key. Please go back to the Alpha Vantage website and claim a new key. Then, update the.env file with the new key.")
    print("2. If the key is correct, you may have exceeded the 25 requests/day limit. You can either wait until tomorrow or get a new key.")