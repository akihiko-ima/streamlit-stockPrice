import pandas as pd
import yfinance as yf
import streamlit as st
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_cookies_controller import CookieController
from prophet import Prophet
from prophet.plot import plot_plotly
from typing import List


def us_stock_page() -> None:
    """Renders a USA stock prices in a Streamlit application."""
    controller = CookieController()
    st.header("StockPrice-Viewer", divider="blue")
    tab1, tab2 = st.tabs(["📈 view", "🗃 predict_Function"])

    toast_flag = False
    if "toast_flag" not in st.session_state:
        st.toast(":violet-background[このページはCookiesを使用しています]", icon="🚨")
        time.sleep(1.5)
        st.session_state["toast_flag"] = True

    @st.cache_data
    def get_stock_data(ticker_list: List[str], period: str = "1y") -> pd.DataFrame:
        """
        Fetches historical stock data for a list of tickers and returns a formatted DataFrame.

        Args:
            ticker_list (List[str]): A list of stock ticker symbols to fetch data for.
            period (str, optional): The period for which historical data is fetched.
                                    Defaults to "1y". Examples include "1d", "5d", "1mo",
                                    "6mo", "1y", "5y", "max".

        Returns:
            pd.DataFrame:A DataFrame containing the historical closing prices of the
                      specified tickers, with tickers as row indices and dates as columns.
        """
        df = pd.DataFrame()
        for ticker in ticker_list:
            try:
                tkr = yf.Ticker(ticker)
                hist = tkr.history(period=period)
                if hist.empty:
                    st.warning(f"No data for {ticker}, skipping...")
                    continue
                hist.index = hist.index.strftime("%d %B %Y")
                hist = hist[["Close"]]
                hist.columns = [ticker]
                hist = hist.T
                hist.index.name = "Name"
                df = pd.concat([df, hist])
            except Exception as e:
                st.error(f"Error retrieving data for {ticker}: {e}")
                pass
        return df

    with tab1:
        cookies = controller.getAll()
        period_options = [
            "1d",
            "5d",
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y",
            "10y",
            "ytd",
            "max",
        ]

        if (
            cookies is None
            or "stock_price_period" not in cookies
            or cookies["stock_price_period"] is None
        ):
            period = st.selectbox(
                ":calendar: Period", period_options, index=period_options.index("1y")
            )
        else:
            period = cookies["stock_price_period"]
            period = st.selectbox(
                ":calendar: Period", period_options, index=period_options.index(period)
            )

        ymin, ymax = st.slider(":chart_with_upwards_trend: Scale ", 0, 3000, (0, 500))

        st.write("#### Company Selection")
        if "ticker_list" in cookies and cookies["ticker_list"] is not None:
            ticker_list = cookies["ticker_list"]
        else:
            ticker_list = ["VT", "VTI", "VEA", "VWO", "KO", "TSM"]

        df = get_stock_data(ticker_list, period)

        companies = st.multiselect(
            "Company Selection",
            list(df.index),
            ticker_list[:3],
        )
        if not companies:
            st.error("一社は選択してください。")
        else:
            data = df.loc[companies]
            st.write("#### StockPrice(USD)", data)
            df = df.T.reset_index()
            fig1 = make_subplots(rows=1, cols=1)

        for company in companies:
            fig1.add_trace(
                go.Scatter(x=df["Date"], y=df[company], name=f"{company}"), row=1, col=1
            )
            fig1.update_yaxes(
                title_text="StockPrice [$]",
                title_font={"size": 20},
                title_standoff=0,
                range=[ymin, ymax],
                row=1,
                col=1,
            )

            fig1.update_layout(height=700, width=950)
            fig1.update_layout(
                hovermode="x",  # hervermode: x 複数参照、 closest　一番近い点
                legend=dict(
                    xanchor="left",
                    yanchor="top",
                    x=0.1,
                    y=1.1,
                    orientation="h",
                    bgcolor="white",
                    bordercolor="grey",
                    borderwidth=1,
                ),
            )
        st.plotly_chart(fig1, use_container_width=True)

        # set-cookie
        controller.set("stock_price_period", period)

    with tab2:
        if st.session_state["authentication_status"] == True:
            st.info("secret page")
            predict_df = get_stock_data(ticker_list, period)

            st.write("#### choice target")
            predict_taeget_companies = st.selectbox(
                "Company Selection for predict",
                list(predict_df.index),
            )
            predict_cols = ["Date", predict_taeget_companies]
            predict_df = df[predict_cols]
            # prophet用にcolum名を変更
            predict_df = predict_df.reset_index().rename(
                columns={"Date": "ds", predict_taeget_companies: "y"}
            )
            st.table(predict_df.head())

            st.write("#### Prophetによる予測結果")
            # Prophetによる予測
            model = Prophet()
            model.fit(predict_df)

            # 学習データに基づいて未来を予測
            future = model.make_future_dataframe(periods=60)
            forecast = model.predict(future)
            fig = plot_plotly(model, forecast)
            st.plotly_chart(fig)

        else:
            st.info(
                "This feature requires log in. Please log in on the 'Login' page first."
            )
