import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple, Union

class StockDataFetcher:
    def __init__(self, ticker: str = "AAPL"):
        """Initialize with a stock ticker symbol."""
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
    
    def get_company_info(self) -> Dict[str, Any]:
        """Get basic company information."""
        return self.stock.info
    
    def get_historical_data(self, period: str = "1y") -> pd.DataFrame:
        """Get historical price data.
        
        Args:
            period: Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        """
        return self.stock.history(period=period)
    
    def get_financials(self) -> Dict[str, pd.DataFrame]:
        """Get financial statements (income statement, balance sheet, cash flow)."""
        return {
            'income_statement': self.stock.financials,
            'balance_sheet': self.stock.balance_sheet,
            'cash_flow': self.stock.cashflow
        }
    
    def get_analyst_recommendations(self) -> Optional[pd.DataFrame]:
        """Get analyst recommendations."""
        try:
            return self.stock.recommendations
        except:
            return None
    
    def get_dividends_splits(self) -> Dict[str, pd.DataFrame]:
        """Get dividend and stock split history."""
        return {
            'dividends': self.stock.dividends,
            'splits': self.stock.splits
        }
    
    def get_options_data(self) -> Optional[Dict[str, pd.DataFrame]]:
        """Get options chain data for the next expiration date."""
        try:
            options = self.stock.options
            if not options:
                return None
                
            options_chain = self.stock.option_chain(options[0])
            return {
                'calls': options_chain.calls,
                'puts': options_chain.puts
            }
        except Exception as e:
            print(f"Error fetching options data: {e}")
            return None
    
    def get_holders_info(self) -> Dict[str, Optional[pd.DataFrame]]:
        """Get major and institutional holders information."""
        try:
            return {
                'major_holders': self.stock.major_holders,
                'institutional_holders': self.stock.institutional_holders
            }
        except Exception as e:
            print(f"Error fetching holders info: {e}")
            return {'major_holders': None, 'institutional_holders': None}
    
    def get_earnings_data(self) -> Dict[str, Optional[pd.DataFrame]]:
        """Get earnings dates and estimates."""
        try:
            return {
                'earnings_dates': self.stock.earnings_dates,
                'earnings_estimates': self.stock.earnings_estimates
            }
        except Exception as e:
            print(f"Error fetching earnings data: {e}")
            return {'earnings_dates': None, 'earnings_estimates': None}
    
    def get_news(self) -> list:
        """Get company news."""
        return self.stock.news
    
    def get_analyst_price_target(self) -> Optional[pd.Series]:
        """Get analyst price targets."""
        try:
            return self.stock.analyst_price_target
        except:
            return None
    
    def get_quarterly_financials(self) -> Dict[str, Optional[pd.DataFrame]]:
        """Get quarterly financial statements."""
        try:
            return {
                'quarterly_income': self.stock.quarterly_financials,
                'quarterly_balance_sheet': self.stock.quarterly_balance_sheet,
                'quarterly_cash_flow': self.stock.quarterly_cashflow
            }
        except Exception as e:
            print(f"Error fetching quarterly financials: {e}")
            return {
                'quarterly_income': None,
                'quarterly_balance_sheet': None,
                'quarterly_cash_flow': None
            }
    
    def get_sustainability_data(self) -> Optional[pd.DataFrame]:
        """Get sustainability/ESG data."""
        try:
            return self.stock.sustainability
        except:
            return None
    
    def get_calendar_events(self) -> Optional[pd.DataFrame]:
        """Get company calendar events."""
        try:
            return self.stock.calendar
        except:
            return None
    
    def get_all_data(self) -> Dict[str, Any]:
        """Get all available data in a single dictionary."""
        data = {
            'company_info': self.get_company_info(),
            'historical_data': self.get_historical_data(),
            'financials': self.get_financials(),
            'analyst_recommendations': self.get_analyst_recommendations(),
            'dividends_splits': self.get_dividends_splits(),
            'options_data': self.get_options_data(),
            'holders_info': self.get_holders_info(),
            'earnings_data': self.get_earnings_data(),
            'news': self.get_news(),
            'analyst_price_target': self.get_analyst_price_target(),
            'quarterly_financials': self.get_quarterly_financials(),
            'sustainability': self.get_sustainability_data(),
            'calendar_events': self.get_calendar_events()
        }
        return data
