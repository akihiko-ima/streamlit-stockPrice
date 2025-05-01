import time
import streamlit as st
import yfinance as yf
from streamlit_extras.metric_cards import style_metric_cards
from dataclasses import dataclass
from yfinance.exceptions import YFRateLimitError


@dataclass
class StockVolatility:
    weekly_change_value: float | None
    weekly_change_percent: float | None
    monthly_change_value: float | None
    monthly_change_percent: float | None
    yearly_change_value: float | None
    yearly_change_percent: float | None


class StockAnalyzer:
    """株価データを取得し、変化量と変化率を計算し、Streamlitで表示するクラス"""

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.data = self._get_stock_volatility_with_cache(ticker)

    @st.cache_data(show_spinner="📈 株価データを取得中...")
    def _get_stock_volatility_with_cache(self, ticker: str) -> StockVolatility:
        """キャッシュ付き株価データ取得＆変化率計算"""
        retries = 3
        delay = 1

        for i in range(retries):
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1y")
                break
            except YFRateLimitError:
                if i < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    st.error(
                        "❌ Yahoo Finance のレートリミットに達しました。後ほど再試行してください。"
                    )
                    return StockVolatility(None, None, None, None, None, None)

        if hist.empty:
            return StockVolatility(None, None, None, None, None, None)

        latest_price = hist["Close"].iloc[-1]
        week_ago_price = hist["Close"].iloc[-6] if len(hist) > 6 else None
        month_ago_price = hist["Close"].iloc[-21] if len(hist) > 21 else None
        year_ago_price = hist["Close"].iloc[0] if len(hist) > 1 else None

        def calc_change(new, old):
            return round(new - old, 2) if old else None

        def calc_change_percent(new, old):
            return round(((new - old) / old) * 100, 2) if old else None

        return StockVolatility(
            weekly_change_value=calc_change(latest_price, week_ago_price),
            weekly_change_percent=calc_change_percent(latest_price, week_ago_price),
            monthly_change_value=calc_change(latest_price, month_ago_price),
            monthly_change_percent=calc_change_percent(latest_price, month_ago_price),
            yearly_change_value=calc_change(latest_price, year_ago_price),
            yearly_change_percent=calc_change_percent(latest_price, year_ago_price),
        )

    def display(self, title: str):
        """Streamlit で株価カードを表示"""
        st.write(f"##### {title}: {self.ticker}")

        if self.data.weekly_change_value is None:
            st.error("❌ 無効なティッカー or データ取得に失敗")
        else:
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "1週間の変化",
                f"{self.data.weekly_change_value} USD",
                delta=f"{self.data.weekly_change_percent}%",
            )
            col2.metric(
                "1か月の変化",
                f"{self.data.monthly_change_value} USD",
                delta=f"{self.data.monthly_change_percent}%",
            )
            col3.metric(
                "1年間の変化",
                f"{self.data.yearly_change_value} USD",
                delta=f"{self.data.yearly_change_percent}%",
            )

            style_metric_cards(border_left_color="#6761A8", background_color="#F0F0F0")
