# Streamlit 株価表示アプリ
import os
import streamlit as st

from components.sidebar import sidebar_component
from views import (
    qrcode_page,
    us_stock_page,
    japan_stock_page,
    login_page,
    custom_stock_list_page,
    contact_me_page,
)

st.set_page_config(
    page_title="Stock-imaima",
    page_icon=":gorilla:",
    initial_sidebar_state="auto",
)

# Python のモジュール検索パスの追加
style_path = os.path.join(os.path.dirname(__file__), "style.css")
st.markdown("<style>" + open(style_path).read() + "</style>", unsafe_allow_html=True)

# セッション状態の初期化
if "login_auth" not in st.session_state:
    st.session_state["login_auth"] = False

# SiderBar
tabs = sidebar_component()

# Main-page
if tabs == "main":
    us_stock_page()

if tabs == "JapanStock":
    japan_stock_page()

if tabs == "Login":
    login_page()

if tabs == "Settings":
    custom_stock_list_page()

if tabs == "QR":
    qrcode_page()

if tabs == "Contact":
    contact_me_page()
