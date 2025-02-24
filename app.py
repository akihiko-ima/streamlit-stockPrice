# Streamlit 株価表示アプリ
import os
import streamlit as st

from config import initialize_setting
from components.sidebar import sidebar_component
from router import router_mappings

st.set_page_config(
    page_title="Stock-imaima",
    page_icon=":gorilla:",
    initial_sidebar_state="auto",
    layout="wide",
)

style_path = os.path.join(os.path.dirname(__file__), "style.css")
st.markdown("<style>" + open(style_path).read() + "</style>", unsafe_allow_html=True)

initialize_setting()

# SiderBar
router = sidebar_component()

# routing
if router in router_mappings:
    router_mappings[router]()
