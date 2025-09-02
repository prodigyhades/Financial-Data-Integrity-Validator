# api_client/client.py

import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv

# Load environment variables from a.env file if it exists
load_dotenv()

class AlphaVantageClient:
    """
    A client to interact with the Alpha Vantage API for fetching stock data.
    """

    def __init__(self):
        """
        Initializes the client, retrieving the API key from environment variables.
        
        Raises:
            ValueError: If the ALPHAVANTAGE_API_KEY environment variable is not set.
        """
        self.api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("ALPHAVANTAGE_API_KEY environment variable not set.")
        
        # Initialize the TimeSeries client from the alpha-vantage library
        # We specify pandas DataFrame as the desired output format for easy analysis.
        self._ts = TimeSeries(key=self.api_key, output_format='pandas')

    def get_daily(self, symbol: str) -> pd.DataFrame:
        """
        Fetches the daily time series data (unadjusted) for a given stock symbol.

        This endpoint provides raw historical data without adjustments for splits
        or dividends, and is available on the free API tier.

        Args:
            symbol (str): The stock symbol to fetch data for (e.g., 'IBM', 'AAPL').

        Returns:
            pd.DataFrame: A pandas DataFrame containing the daily time series data,
                          indexed by date. The columns include open, high, low, close,
                          and volume.
        
        Raises:
            ValueError: If the API call fails or returns no data for the symbol.
        """
        try:
            # We now call get_daily, which is a free endpoint.
            data, meta_data = self._ts.get_daily(symbol=symbol, outputsize='compact')
            
            # The column names are different for this endpoint.
            data.rename(columns={
                '1. open': 'open',
                '2. high': 'high',
                '3. low': 'low',
                '4. close': 'close',
                '5. volume': 'volume'
            }, inplace=True)

            # Convert column types to appropriate numeric formats for validation
            for col in ['open', 'high', 'low', 'close']:
                data[col] = pd.to_numeric(data[col])
            data['volume'] = pd.to_numeric(data['volume'], downcast='integer')
            
            return data
        
        except Exception as e:
            print(f"Error fetching data for symbol '{symbol}': {e}")
            raise ValueError(f"Could not retrieve data for symbol '{symbol}'. Check if the symbol is valid.")