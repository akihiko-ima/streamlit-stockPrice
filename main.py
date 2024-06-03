# Streamlit 株価表示アプリ

import pandas as pd
import yfinance as yf
import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_cookies_controller import CookieController
from prophet import Prophet
from prophet.plot import plot_plotly

st.set_page_config(
    page_title="Stock-AKI",
    page_icon=":gorilla:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# セッション状態の初期化
if "login_auth" not in st.session_state:
    st.session_state["login_auth"] = False


st.title("StockPrice-Viewer")

tab1, tab2 = st.tabs(["📈 view", "🗃 predict_Function"])

toast_flag = False
if "toast_flag" not in st.session_state:
    st.toast(":violet-background[このページはCookiesを使用しています]", icon="🚨")
    time.sleep(1.5)
    st.session_state["toast_flag"] = True

controller = CookieController()


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


with tab1:

    # cookiesの取得
    cookies = controller.getAll()

    try:
        if (
            cookies is None
            or "stock_price_days" not in cookies
            or cookies["stock_price_days"] is None
        ):
            days = st.sidebar.slider(":calendar: Days", 1, 5000, 365)
            controller.set("stock_price_days", days)
        else:
            days = cookies["stock_price_days"]
            days = st.sidebar.slider(":calendar: Days", 1, 5000, days)
            controller.set("stock_price_days", days)

        st.write("#### Company Selection")
        ymin, ymax = st.sidebar.slider(
            ":chart_with_upwards_trend: Scale ", 0, 3000, (0, 500)
        )

        tickers = {
            "KO": "KO",
            "Carnival": "CCL",
            "TSMC": "TSM",
            "MongoDB": "MDB",
            "Crowdstrike": "CRWD",
            "Microsoft": "MSFT",
            "ETF VTI": "VTI",
            "ETF VT": "VT",
        }

        df = get_data(days, tickers)

        companies = st.multiselect(
            "Company Selection",
            list(df.index),
            ["KO", "TSMC", "MongoDB", "Microsoft", "ETF VT"],
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

    except:
        st.error("エラーが起きました。")

with tab2:
    if st.session_state["login_auth"] == True:
        st.write("secret page")
        predict_df = get_data(days, tickers)

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
            "This feature requires log in. Please log in on the 'user-auth' page first."
        )
