import streamlit as st
import yfinance as yf
import pandas as pd
import jaconv
import plotly.graph_objects as go
from datetime import datetime, timedelta
from prophet import Prophet


def japan_stock_page() -> None:
    """Renders a Japan stock prices in a Streamlit application."""
    st.header("Japan stock", divider="blue")

    if "stock_data" not in st.session_state:
        st.session_state["stock_data"] = None
    if "forecast_data" not in st.session_state:
        st.session_state["forecast_data"] = None

    ticker = st.text_input("ティッカーコードを入力してください（例：7203）")

    options = ["1y", "2y", "5y", "10y"]
    period = st.pills(
        "データを取得したい期間を選択してください。", options, selection_mode="single"
    )

    if st.button(
        "株価情報を取得", key="get_stock_data", type="primary", icon=":material/search:"
    ):
        if not ticker:
            st.error("ティッカーコードを入力してください。")
            return

        if not period:
            st.error("データ取得期間を選択してください。")
            return

        # 入力されたティッカーコードを標準化
        ticker = jaconv.z2h(ticker, digit=True, ascii=True).upper() + ".T"

        # 株価データを取得
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)

        if not data.empty:
            st.session_state["stock_data"] = data
            st.session_state["ticker"] = ticker
            st.session_state["period"] = period
            st.success(f"データを取得しました: {ticker} の過去{period}ear分")
        else:
            st.error(
                "データが見つかりませんでした。ティッカーコードを確認してください。"
            )
            st.session_state["stock_data"] = None

    # 株価データが存在する場合の処理
    if st.session_state["stock_data"] is not None:
        data = st.session_state["stock_data"]
        ticker = st.session_state["ticker"]
        period = st.session_state["period"]

        st.write(f"({ticker}) の過去{period}ear分の株価情報")
        st.dataframe(data)

        # グラフを作成
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Close",
                line={"color": "#FFA07A", "width": 2},
            )
        )
        fig.update_layout(
            title=f"{ticker} の過去{period}ear分の株価",
            xaxis_title="Date",
            yaxis_title="Close Price",
            autosize=False,
            width=800,  # 横幅を調整
            height=600,  # 縦幅を調整
        )
        st.plotly_chart(fig)

        with st.expander("将来の株価を予測しますか？", icon=":material/thumb_up:"):
            st.write(
                """
                時系列の予測は"prophet"を用いて行います。
                株価予測は保証されたものではなく、投資は自己責任で行ってください。
            """
            )
            if st.button(
                "株価を予測",
                key="predict_by_prophet",
                type="primary",
                icon=":material/trending_up:",
            ):
                # Prophet の入力データの準備
                forecast_data = data.reset_index()[["Date", "Close"]]
                forecast_data.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)

                # タイムゾーン情報を削除
                forecast_data["ds"] = forecast_data["ds"].dt.tz_localize(None)

                # モデルの作成と予測
                model = Prophet()
                model.fit(forecast_data)

                # 未来のデータフレームを作成（60日分の予測を行う）
                future = model.make_future_dataframe(periods=60)
                forecast = model.predict(future)

                # 予測結果をセッションステートに保存
                st.session_state["forecast_data"] = forecast

    # 予測データの表示
    if st.session_state["forecast_data"] is not None:
        forecast = st.session_state["forecast_data"]
        fig_forecast = go.Figure()
        fig_forecast.add_trace(
            go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat"],
                mode="lines",
                name="Predicted Close",
                line={"color": "#008080", "width": 2},
            )
        )
        fig_forecast.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Historical Close",
                line={"color": "#FFA07A", "width": 2},
            )
        )
        fig_forecast.update_layout(
            title={
                "text": f"{st.session_state['ticker']} の株価予測",
                "font": {"color": "black", "size": 24},
            },
            xaxis={
                "title": {
                    "text": "Date",
                    "font": {"color": "black", "size": 18},
                },
                "tickfont": {"color": "black", "size": 14},
            },
            yaxis={
                "title": {
                    "text": "Price",
                    "font": {"color": "black", "size": 18},
                },
                "tickfont": {"color": "black", "size": 14},
            },
            legend={
                "font": {
                    "size": 16,
                    "color": "black",
                }
            },
            autosize=False,
            width=1200,
            height=900,
        )

        st.plotly_chart(fig_forecast)
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]])
