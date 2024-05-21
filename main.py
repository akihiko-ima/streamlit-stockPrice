# Streamlit 株価表示アプリ

import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

st.title("StockPrice-Viewer")


# キャッシュを貯めるコマンド。次回以降の検索速度が工場
@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f"{days}d")
        hist.index = hist.index.strftime("%d %B %Y")
        hist = hist[["Close"]]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = "Name"
        df = pd.concat([df, hist])
    return df


# tryを使用することで、エラー発生時のコメント表示が可能
try:
    # st.write("#### ■表示日数選択")
    days = st.sidebar.slider(":calendar: Days", 1, 2000, 500)
    # st.write(f"#### 過去 **{days}日間**の株価")

    st.write("#### Company Selection")
    ymin, ymax = st.sidebar.slider(
        ":chart_with_upwards_trend: Scale ", 0, 3000, (0, 500)
    )

    tickers = {
        "KO": "KO",
        "Carnival": "CCL",
        "Crowdstrike": "CRWD",
        "Microsoft": "MSFT",
        "ETF VTI": "VTI",
        "ETF VT": "VT",
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        "Company Selection",
        list(df.index),
        ["KO", "Microsoft", "ETF VTI", "ETF VT"],  # ko, MSFT, VTI, VTを初期表示
    )
    if not companies:
        st.error("一社は選択する")
    else:
        data = df.loc[companies]
        st.write("#### StockPrice(USD)", data.sort_index())
        # yfinanceから読み取ったデータフレームのインデックスがずれているのでreset実施
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["Date"]).rename(
            columns={"value": "Stock Prices(USD)"}
        )
        df = df.T.reset_index()
        fig1 = make_subplots(rows=1, cols=1)

    # for company in tickers.keys():
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
            title=dict(
                text="<b>StockPrice_Chart",
                font=dict(size=20, color="grey"),
                x=0.45,
                xanchor="center",
            ),
            hovermode="x",  # hervermode: x 複数参照、 closest　一番近い点
            legend=dict(
                xanchor="right",
                yanchor="bottom",
                x=1.25,
                y=0.35,
                orientation="v",
                bgcolor="white",
                bordercolor="grey",
                borderwidth=1,
            ),
        )
    st.plotly_chart(fig1, use_container_width=True)


except:
    st.error("エラーが起きました。")
