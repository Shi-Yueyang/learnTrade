"""
Utility functions for quantitative trading analysis
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def download_stock_data(symbol, start_date=None, end_date=None, period="2y"):
    """
    Download stock data using yfinance
    
    Parameters:
    - symbol: Stock ticker symbol
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - period: Period to download if dates not specified
    
    Returns:
    - DataFrame with stock data
    """
    if start_date and end_date:
        data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    else:
        data = yf.download(symbol, period=period, progress=False)
    
    return data

def calculate_returns(prices, method='simple'):
    """
    Calculate returns from price series
    
    Parameters:
    - prices: Series of prices
    - method: 'simple' or 'log'
    
    Returns:
    - Series of returns
    """
    if method == 'simple':
        return prices.pct_change()
    elif method == 'log':
        return np.log(prices / prices.shift(1))
    else:
        raise ValueError("Method must be 'simple' or 'log'")

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe ratio
    
    Parameters:
    - returns: Series of returns
    - risk_free_rate: Annual risk-free rate
    
    Returns:
    - Sharpe ratio
    """
    excess_returns = returns - risk_free_rate/252
    return excess_returns.mean() / returns.std() * np.sqrt(252)

def calculate_max_drawdown(returns):
    """
    Calculate maximum drawdown
    
    Parameters:
    - returns: Series of returns
    
    Returns:
    - Maximum drawdown value
    """
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.expanding().max()
    drawdown = (cumulative - rolling_max) / rolling_max
    return drawdown.min()

def validate_data(data, required_columns=['Open', 'High', 'Low', 'Close', 'Volume']):
    """
    Validate that data has required columns and no missing values
    
    Parameters:
    - data: DataFrame to validate
    - required_columns: List of required column names
    
    Returns:
    - Boolean indicating if data is valid
    """
    # Check required columns
    for col in required_columns:
        if col not in data.columns:
            print(f"Missing required column: {col}")
            return False
    
    # Check for missing values
    missing_data = data[required_columns].isnull().sum()
    if missing_data.sum() > 0:
        print("Missing values found:")
        for col, missing in missing_data.items():
            if missing > 0:
                print(f"  {col}: {missing}")
        return False
    
    return True

def print_performance_summary(strategy_return, benchmark_return, strategy_sharpe, max_dd):
    """
    Print a formatted performance summary
    
    Parameters:
    - strategy_return: Strategy total return
    - benchmark_return: Benchmark total return  
    - strategy_sharpe: Strategy Sharpe ratio
    - max_dd: Maximum drawdown
    """
    print("=" * 50)
    print("PERFORMANCE SUMMARY")
    print("=" * 50)
    print(f"Strategy Return:    {strategy_return:.2%}")
    print(f"Benchmark Return:   {benchmark_return:.2%}")
    print(f"Excess Return:      {strategy_return - benchmark_return:.2%}")
    print(f"Sharpe Ratio:       {strategy_sharpe:.3f}")
    print(f"Maximum Drawdown:   {max_dd:.2%}")
    print("=" * 50)
