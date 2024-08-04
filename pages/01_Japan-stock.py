import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import jaconv

st.header("Japan stock", divider="blue")

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 3rem;
    }
    .stButton button {
        background-color: teal;
        color: white;
        border: none;
        padding: 15px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        box-shadow: 3px 7px 13px -10px #65789f;
        transition-duration: 0.4s;
        transition: all 0.4s;
    }
    .stButton button:hover {
        background-color: white;
        color: teal;
        border: 2px solid teal;
        box-shadow: none;
        transform: translateY(5px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

ticker = st.text_input("ティッカーコードを入力してください（例：7203）")

if st.button("株価情報を取得"):
    if ticker:
        ticker = jaconv.z2h(ticker, digit=True, ascii=True).upper() + ".T"

        end_date = datetime.today()
        start_date = end_date - timedelta(days=365)
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)

        if not data.empty:
            st.write(f"({ticker}) の過去1年分の株価情報**")
            st.dataframe(data)

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close")
            )
            fig.update_layout(
                title=f"{ticker} の過去1年分の株価",
                xaxis_title="Date",
                yaxis_title="Close Price",
                autosize=False,
                width=800,  # 横幅を調整
                height=600,  # 縦幅を調整
            )
            st.plotly_chart(fig)
        else:
            st.write(
                "データが見つかりませんでした。ティッカーコードを確認してください。"
            )
    else:
        st.write("ティッカーコードを入力してください。")
