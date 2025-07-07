"""
Proxy Configuration Utilities for Quantitative Trading Project

This module provides utility functions for configuring proxies,
especially useful for users in China who need to access international APIs.
"""

import os
import requests
import yfinance as yf
from typing import Optional, Dict, Any


class ProxyConfig:
    """Proxy configuration manager for the trading project."""
    
    def __init__(self, 
                 host: str = "localhost", 
                 port: str = "10809",
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 use_proxy: bool = True):
        """
        Initialize proxy configuration.
        
        Args:
            host: Proxy server hostname or IP
            port: Proxy server port
            username: Proxy username (if authentication required)
            password: Proxy password (if authentication required)
            use_proxy: Whether to use proxy or direct connection
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_proxy = use_proxy
        self.proxy_dict = None
        
        if self.use_proxy:
            self._setup_proxy()
    
    def _setup_proxy(self):
        """Set up proxy configuration."""
        # Build proxy URL
        if self.username and self.password:
            proxy_url = f"http://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            proxy_url = f"http://{self.host}:{self.port}"
        
        # Set environment variables
        os.environ['HTTP_PROXY'] = proxy_url
        os.environ['HTTPS_PROXY'] = proxy_url
        
        # Create proxy dictionary for requests
        self.proxy_dict = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        print(f"🌐 Proxy configured: {self.host}:{self.port}")
    
    def test_connection(self, timeout: int = 10) -> bool:
        """
        Test proxy connection.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            True if connection successful, False otherwise
        """
        if not self.use_proxy:
            print("🌐 Testing direct connection...")
            try:
                response = requests.get("https://httpbin.org/ip", timeout=timeout)
                if response.status_code == 200:
                    print("✅ Direct connection successful!")
                    return True
            except Exception as e:
                print(f"❌ Direct connection failed: {e}")
                return False
        
        print("🔌 Testing proxy connection...")
        try:
            response = requests.get("https://httpbin.org/ip", 
                                 proxies=self.proxy_dict, 
                                 timeout=timeout)
            if response.status_code == 200:
                ip_info = response.json().get('origin', 'Unknown')
                print(f"✅ Proxy connection successful! IP: {ip_info}")
                return True
            else:
                print(f"❌ Proxy connection failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Proxy connection failed: {e}")
            return False
    
    def download_stock_data(self, 
                          symbol: str, 
                          start_date: str, 
                          end_date: str) -> Optional[Any]:
        """
        Download stock data using configured proxy.
        
        Args:
            symbol: Stock ticker symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Pandas DataFrame with stock data or None if failed
        """
        print(f"📈 Downloading {symbol} data from {start_date} to {end_date}")
        
        # Method 1: Standard yfinance download
        try:
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            if data is not None and not data.empty:
                print("✅ Data downloaded successfully!")
                return data
        except Exception as e:
            print(f"❌ Standard download failed: {e}")
        
        # Method 2: Custom session with proxy (if using proxy)
        if self.use_proxy and self.proxy_dict:
            try:
                print("🔄 Trying with custom proxy session...")
                session = requests.Session()
                session.proxies.update(self.proxy_dict)
                
                ticker = yf.Ticker(symbol)
                ticker.session = session
                
                data = ticker.history(start=start_date, end=end_date)
                if data is not None and not data.empty:
                    print("✅ Data downloaded with proxy session!")
                    return data
            except Exception as e:
                print(f"❌ Proxy session download failed: {e}")
        
        print("❌ All download methods failed")
        return None
    
    def get_session(self) -> requests.Session:
        """
        Get a requests session configured with proxy.
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        if self.use_proxy and self.proxy_dict:
            session.proxies.update(self.proxy_dict)
        return session


# Convenience functions for common configurations

def setup_china_proxy(host: str = "localhost", port: str = "10809") -> ProxyConfig:
    """
    Set up common proxy configuration for users in China.
    
    Args:
        host: Proxy server host (default: localhost)
        port: Proxy server port (default: 10809)
        
    Returns:
        Configured ProxyConfig instance
    """
    return ProxyConfig(host=host, port=port, use_proxy=True)


def setup_direct_connection() -> ProxyConfig:
    """
    Set up direct internet connection (no proxy).
    
    Returns:
        ProxyConfig instance configured for direct connection
    """
    return ProxyConfig(use_proxy=False)


# Example usage
if __name__ == "__main__":
    # Example 1: China proxy setup
    proxy = setup_china_proxy()
    proxy.test_connection()
    
    # Example 2: Download data with proxy
    data = proxy.download_stock_data("AAPL", "2023-01-01", "2024-01-01")
    if data is not None:
        print(f"Downloaded {len(data)} rows of data")
    
    # Example 3: Direct connection
    direct = setup_direct_connection()
    direct.test_connection()
