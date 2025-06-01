from openai import OpenAI
from aapl_analysis import StockDataFetcher
from openai_config import OPENAI_API_KEY, OPENAI_MODEL

class Agent:
    def run(self, ticker):
        raise NotImplementedError
    def get_name(self):
        return self.__class__.__name__

class ValuationAgent(Agent):
    def fetch_valuation_data(self, ticker="AAPL"):
        fetcher = StockDataFetcher(ticker)
        info = fetcher.get_company_info()
        fields = [
            'currentPrice', 'marketCap', 'trailingPE', 'forwardPE', 'priceToBook', 'priceToSalesTrailing12Months',
            'enterpriseToEbitda', 'pegRatio', 'trailingEps', 'forwardEps', 'returnOnEquity', 'returnOnAssets',
            'profitMargins', 'grossMargins', 'operatingMargins', 'revenueGrowth', 'earningsGrowth',
            'earningsQuarterlyGrowth', 'revenueQuarterlyGrowth', 'dividendYield', 'payoutRatio', 'debtToEquity',
            'currentRatio', 'quickRatio', 'totalCash', 'totalDebt', 'freeCashflow', 'operatingCashflow',
            'capitalExpenditures', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'volume', 'averageVolume', 'sharesOutstanding'
        ]
        data = {k: info.get(k, None) for k in fields}
        data['ticker'] = ticker
        data['shortName'] = info.get('shortName', '')
        data['sector'] = info.get('sector', '')
        data['industry'] = info.get('industry', '')
        return data

    def format_prompt(self, data):
        prompt = (
            f"You are a market analyst specializing in stock valuation.\n"
            f"Here is the data for {data['shortName']} ({data['ticker']}):\n"
            f"Sector: {data['sector']}, Industry: {data['industry']}\n"
            f"Current Price: {data['currentPrice']}, Market Cap: {data['marketCap']}\n"
            f"P/E: {data['trailingPE']}, Fwd P/E: {data['forwardPE']}, P/B: {data['priceToBook']}, "
            f"P/S: {data['priceToSalesTrailing12Months']}, EV/EBITDA: {data['enterpriseToEbitda']}, PEG: {data['pegRatio']}\n"
            f"EPS: {data['trailingEps']}, Fwd EPS: {data['forwardEps']}\n"
            f"ROE: {data['returnOnEquity']}, ROA: {data['returnOnAssets']}\n"
            f"Net Margin: {data['profitMargins']}, Gross Margin: {data['grossMargins']}, Operating Margin: {data['operatingMargins']}\n"
            f"Revenue Growth: {data['revenueGrowth']}, Earnings Growth: {data['earningsGrowth']}, "
            f"Earnings Qtr Growth: {data['earningsQuarterlyGrowth']}, Revenue Qtr Growth: {data['revenueQuarterlyGrowth']}\n"
            f"Dividend Yield: {data['dividendYield']}, Payout Ratio: {data['payoutRatio']}\n"
            f"Debt/Equity: {data['debtToEquity']}, Current Ratio: {data['currentRatio']}, Quick Ratio: {data['quickRatio']}\n"
            f"Total Cash: {data['totalCash']}, Total Debt: {data['totalDebt']}\n"
            f"Free Cash Flow: {data['freeCashflow']}, Operating Cash Flow: {data['operatingCashflow']}, CapEx: {data['capitalExpenditures']}\n"
            f"52W High: {data['fiftyTwoWeekHigh']}, 52W Low: {data['fiftyTwoWeekLow']}\n"
            f"Volume: {data['volume']}, Avg Volume: {data['averageVolume']}, Shares Out: {data['sharesOutstanding']}\n\n"
            "Based on the above data, is the stock undervalued or overvalued relative to its earnings, assets, and growth? "
            "Limit your response to 200 words and include a clear answer among ['undervalued', 'overvalued', 'fair']."
        )
        return prompt

    def run(self, ticker):
        data = self.fetch_valuation_data(ticker)
        prompt = self.format_prompt(data)
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.responses.create(
            model=OPENAI_MODEL,
            reasoning={"effort": "low"},
            input=[{"role": "user", "content": prompt}]
        )
        return response.output_text.strip() if response.output_text else "No response from valuation agent."
