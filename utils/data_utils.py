import os
import requests
from datetime import datetime
import yfinance as yf
import pandas as pd


class DataManager:
    """A comprehensive data manager for financial data acquisition and processing."""
    
    def __init__(self, use_proxy=True, proxy_host="localhost", proxy_port=10809):
        self.use_proxy = use_proxy
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.session = None
        self._setup_session()
    
    def _setup_session(self):
        """Set up requests session with proxy if needed."""
        self.session = requests.Session()
        if self.use_proxy:
            proxy_url = f"http://{self.proxy_host}:{self.proxy_port}"
            self.session.proxies.update({
                'http': proxy_url,
                'https': proxy_url
            })
            # Set environment variables for yfinance
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url
            print(f"🌐 Proxy configured: {proxy_url}")
    
    def get_stock_data(self, symbol, start_date, end_date=None, period="1d"):
        """Download stock data with comprehensive error handling."""
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            
            ticker = yf.Ticker(symbol)
            if self.use_proxy:
                ticker.session = self.session
            
            data = ticker.history(start=start_date, end=end_date, interval=period)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            # Clean up data
            data = data.dropna()
            data.index = pd.to_datetime(data.index)
            
            print(f"✅ Successfully downloaded {len(data)} trading days")

            return data
            
        except Exception as e:
            print(f"❌ Error downloading data for {symbol}: {str(e)}")
            return None
    
    def get_multiple_stocks(self, symbols, start_date, end_date=None):
        """Download data for multiple stocks."""
        data_dict = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol, start_date, end_date)
            if data is not None:
                data_dict[symbol] = data
        return data_dict
    
    def calculate_return(self,data,price_column='Close'):
        current_price = data[price_column].iloc[-1]
        start_price = data[price_column].iloc[0]
        return_value = (current_price - start_price) / start_price * 100
        return return_value
    
    def calculate_return(self,symbols,start_date,end_date=None,column='Close'):
        """Calculate returns for multiple stocks."""
        returns = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol, start_date, end_date)
            if data is not None:
                returns[symbol] = self.calculate_return(data, column)
        return returns
    
    