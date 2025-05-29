import unittest
import pandas as pd
from aapl_analysis import StockDataFetcher

class TestAAPLAnalysis(unittest.TestCase):    
    @classmethod
    def setUpClass(cls):
        """Initialize the StockDataFetcher once for all tests."""
        cls.fetcher = StockDataFetcher("AAPL")
    
    def test_company_info(self):
        """Test company info retrieval."""
        info = self.fetcher.get_company_info()
        self.assertIsInstance(info, dict)
        self.assertIn('shortName', info)
        self.assertIn('sector', info)
    
    def test_historical_data(self):
        """Test historical data retrieval."""
        hist = self.fetcher.get_historical_data(period="1mo")  # Shorter period for testing
        self.assertIsInstance(hist, pd.DataFrame)
        self.assertFalse(hist.empty)
        self.assertIn('Close', hist.columns)
    
    def test_financials(self):
        """Test financial statements retrieval."""
        financials = self.fetcher.get_financials()
        self.assertIsInstance(financials, dict)
        self.assertIn('income_statement', financials)
        self.assertIn('balance_sheet', financials)
        self.assertIn('cash_flow', financials)
    
    def test_analyst_recommendations(self):
        """Test analyst recommendations retrieval."""
        recs = self.fetcher.get_analyst_recommendations()
        if recs is not None:  # Some stocks might not have recommendations
            self.assertIsInstance(recs, pd.DataFrame)
    
    def test_dividends_splits(self):
        """Test dividends and splits data retrieval."""
        data = self.fetcher.get_dividends_splits()
        self.assertIsInstance(data, dict)
        self.assertIn('dividends', data)
        self.assertIn('splits', data)
    
    def test_options_data(self):
        """Test options data retrieval."""
        options = self.fetcher.get_options_data()
        if options is not None:  # Options might not be available for all stocks
            self.assertIsInstance(options, dict)
            self.assertIn('calls', options)
            self.assertIn('puts', options)
    
    def test_holders_info(self):
        """Test holders information retrieval."""
        holders = self.fetcher.get_holders_info()
        self.assertIsInstance(holders, dict)
        self.assertIn('major_holders', holders)
        self.assertIn('institutional_holders', holders)
    
    def test_earnings_data(self):
        """Test earnings data retrieval."""
        earnings = self.fetcher.get_earnings_data()
        self.assertIsInstance(earnings, dict)
        self.assertIn('earnings_dates', earnings)
        self.assertIn('earnings_estimates', earnings)
    
    def test_news(self):
        """Test news retrieval."""
        news = self.fetcher.get_news()
        self.assertIsInstance(news, list)
    
    def test_analyst_price_target(self):
        """Test analyst price target retrieval."""
        target = self.fetcher.get_analyst_price_target()
        if target is not None:  # Might not be available for all stocks
            self.assertIsInstance(target, pd.Series)
    
    def test_quarterly_financials(self):
        """Test quarterly financials retrieval."""
        q_fin = self.fetcher.get_quarterly_financials()
        self.assertIsInstance(q_fin, dict)
        self.assertIn('quarterly_income', q_fin)
        self.assertIn('quarterly_balance_sheet', q_fin)
        self.assertIn('quarterly_cash_flow', q_fin)
    
    def test_sustainability(self):
        """Test sustainability data retrieval."""
        sustainability = self.fetcher.get_sustainability_data()
        if sustainability is not None:  # Not all stocks have sustainability data
            self.assertIsInstance(sustainability, pd.DataFrame)
    
    def test_calendar_events(self):
        """Test calendar events retrieval."""
        calendar = self.fetcher.get_calendar_events()
        if calendar is not None:  # Not all stocks have calendar data
            self.assertIsInstance(calendar, dict)
            # Check for some expected keys in the calendar data
            self.assertIn('Earnings Date', calendar)
            self.assertIn('Ex-Dividend Date', calendar)
    
    def test_get_all_data(self):
        """Test retrieval of all data at once."""
        all_data = self.fetcher.get_all_data()
        self.assertIsInstance(all_data, dict)
        self.assertIn('company_info', all_data)
        self.assertIn('historical_data', all_data)
        self.assertIn('financials', all_data)
        self.assertIn('analyst_recommendations', all_data)
        self.assertIn('dividends_splits', all_data)
        self.assertIn('options_data', all_data)
        self.assertIn('holders_info', all_data)
        self.assertIn('earnings_data', all_data)
        self.assertIn('news', all_data)
        self.assertIn('analyst_price_target', all_data)
        self.assertIn('quarterly_financials', all_data)
        self.assertIn('sustainability', all_data)
        self.assertIn('calendar_events', all_data)

if __name__ == "__main__":
    unittest.main()
