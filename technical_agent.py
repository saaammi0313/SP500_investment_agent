from openai import OpenAI
import pandas as pd
from aapl_analysis import StockDataFetcher
from openai_config import OPENAI_API_KEY, OPENAI_MODEL

class Agent:
    def run(self, ticker):
        raise NotImplementedError
    def get_name(self):
        return self.__class__.__name__

class TechnicalAgent(Agent):
    def calculate_sma(self, df, window):
        return df['Close'].rolling(window=window).mean()
    def calculate_ema(self, df, window):
        return df['Close'].ewm(span=window, adjust=False).mean()
    def calculate_rsi(self, df, window=14):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    def calculate_macd(self, df):
        ema12 = self.calculate_ema(df, 12)
        ema26 = self.calculate_ema(df, 26)
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal
    def calculate_bollinger_bands(self, df, window=20):
        sma = self.calculate_sma(df, window)
        std = df['Close'].rolling(window=window).std()
        upper = sma + (2 * std)
        lower = sma - (2 * std)
        return upper, lower
    def calculate_stochastic(self, df, k_window=14, d_window=3):
        low_min = df['Low'].rolling(window=k_window).min()
        high_max = df['High'].rolling(window=k_window).max()
        k = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        d = k.rolling(window=d_window).mean()
        return k, d
    def format_technical_prompt(self, indicators, ticker, period):
        prompt = (
            f"You are a technical market analyst. Here are the latest technical indicators for {ticker} (period: {period}):\n"
            f"Short-term SMA (20): {indicators['sma20'].iloc[-1]:.2f}\n"
            f"Long-term SMA (50): {indicators['sma50'].iloc[-1]:.2f}\n"
            f"RSI (14): {indicators['rsi14'].iloc[-1]:.2f}\n"
            f"MACD: {indicators['macd'].iloc[-1]:.2f}, MACD Signal: {indicators['macd_signal'].iloc[-1]:.2f}\n"
            f"Bollinger Upper: {indicators['bb_upper'].iloc[-1]:.2f}, Bollinger Lower: {indicators['bb_lower'].iloc[-1]:.2f}\n"
            f"Stochastic %K: {indicators['stoch_k'].iloc[-1]:.2f}, %D: {indicators['stoch_d'].iloc[-1]:.2f}\n"
            f"Current Close: {indicators['close'].iloc[-1]:.2f}\n\n"
            "Based on these technical indicators, is it optimal to buy the stock now? "
            "After reasoning, you must also include a clear answer among ['strong sell', 'sell', 'neutral', 'buy', 'strong buy']."
        )
        return prompt
    def run(self, ticker):
        fetcher = StockDataFetcher(ticker)
        period = "6mo"
        df = fetcher.get_historical_data(period=period)
        indicators = {
            'sma20': self.calculate_sma(df, 20),
            'sma50': self.calculate_sma(df, 50),
            'rsi14': self.calculate_rsi(df, 14),
            'macd': self.calculate_macd(df)[0],
            'macd_signal': self.calculate_macd(df)[1],
            'bb_upper': self.calculate_bollinger_bands(df)[0],
            'bb_lower': self.calculate_bollinger_bands(df)[1],
            'stoch_k': self.calculate_stochastic(df)[0],
            'stoch_d': self.calculate_stochastic(df)[1],
            'close': df['Close']
        }
        prompt = self.format_technical_prompt(indicators, ticker, period)
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.responses.create(
            model=OPENAI_MODEL,
            reasoning={"effort": "low"},
            input=[{"role": "user", "content": prompt}]
        )
        return response.output_text.strip() if response.output_text else "No response from technical agent."
