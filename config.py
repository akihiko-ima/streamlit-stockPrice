import os
import streamlit as st
from dataclasses import dataclass
from typing import Dict, Callable
from dotenv import load_dotenv


# import your streamlit page
from views import (
    us_stock_page,
    japan_stock_page,
    login_page,
    custom_stock_list_page,
    data_viewer_page,
    qrcode_page,
    contact_me_page,
)


@dataclass
class RouterMapping:
    routing_name: str
    icon: str
    streamlit_page: Callable[[], None]


# router mapping
"""
・If you have any pages you would like to route, please add them here.
・The icons in the sidebar use "Google Fonts."
 [https://fonts.google.com/icons](https://fonts.google.com/icons)
"""
routers: Dict[str, RouterMapping] = {
    "router_1": RouterMapping(
        routing_name="main", icon="home", streamlit_page=us_stock_page
    ),
    "router_2": RouterMapping(
        routing_name="JapanStock",
        icon="radio_button_checked",
        streamlit_page=japan_stock_page,
    ),
    "router_3": RouterMapping(
        routing_name="Login", icon="login", streamlit_page=login_page
    ),
    "router_4": RouterMapping(
        routing_name="Settings", icon="settings", streamlit_page=custom_stock_list_page
    ),
    "router_5": RouterMapping(
        routing_name="Data-Viewer",
        icon="query_stats",
        streamlit_page=data_viewer_page,
    ),
    "router_6": RouterMapping(
        routing_name="QR", icon="qr_code", streamlit_page=qrcode_page
    ),
    "router_7": RouterMapping(
        routing_name="Contact", icon="send", streamlit_page=contact_me_page
    ),
}


def initialize_setting():
    """
    環境設定を初期化する関数。

    .envファイルを読み込み、必要なディレクトリを作成し、
    Streamlitのsession_stateにパスを設定します。

    Raises:
        OSError: ディレクトリの作成に失敗した場合に発生します。
    """
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    # for authentication
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = False

    # for data
    if "is_initialized" not in st.session_state:
        st.session_state.is_initialized = False

    if not st.session_state.is_initialized:
        DATA_PATH = os.getenv("DATA_PATH")

        if DATA_PATH and not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            print(f"Directory created.")
        else:
            print(f"Directory already exists or DIR_PATH is not set in .env file.")

        # session_stateの設定
        if "db_path" not in st.session_state:
            st.session_state.db_path = os.getenv("DB_PATH")
        if "data_path" not in st.session_state:
            st.session_state.data_path = DATA_PATH

        st.session_state.is_initialized = True
