import streamlit as st
import time
import toml
import json


def custom_stock_list_page() -> None:
    """Renders a Create a list of stock prices in a Streamlit application."""

    def generate_download_file(
        file_type: str, tick_list_dict: dict
    ) -> tuple[str, bytes, str]:
        """
        指定されたファイルタイプのダウンロード用データを生成する。

        Args:
            file_type (str): 生成するファイルの種類 ("toml" または "json")。

        Returns:
            tuple[str, bytes, str]:
                - `filename` (str): Unixタイムスタンプ付きのファイル名（例: "1708175623_ticker_list.toml"）。
                - `data` (bytes): ダウンロードするファイルのバイナリデータ。
                - `mime` (str): ファイルのMIMEタイプ（"application/toml" または "application/json"）。
        """

        timestamp = int(time.time())
        filename = f"{timestamp}_ticker_list.{file_type}"

        if file_type == "toml":
            toml_str = toml.dumps(tick_list_dict)
            toml_bytes = toml_str.encode("utf-8")
            return filename, toml_bytes, "application/toml"
        elif file_type == "json":
            json_str = json.dumps(tick_list_dict, indent=4)
            json_bytes = json_str.encode("utf-8")
            return filename, json_bytes, "application/json"
        else:
            raise ValueError(f"Invalid file_type: {file_type}")

    # --------------------------------------------------
    # main-component
    # --------------------------------------------------
    st.header(":material/settings: Setting-Stock-List", divider="blue")

    if "ticker_list" not in st.session_state:
        st.session_state["ticker_list"] = []

    col1, col2 = st.columns([3, 1.5])
    with col1:
        ticker = st.text_input("証券コードを入力", placeholder="e.g. 7203, 6501")

    with col2:
        with st.container():
            st.write("")
            st.write("")
            if st.button(
                "Add List",
                key="Add_tick_to_List",
                type="primary",
                icon=":material/add:",
            ):
                if not ticker:
                    st.error("Enter in your favorite Tick")
                elif ticker in st.session_state["ticker_list"]:
                    st.error("すでに同じコードがあるようです。")
                else:
                    st.session_state["ticker_list"].append(ticker)

    st.divider()

    if not st.session_state["ticker_list"]:
        st.write("Ticker_list is empty.")

    if st.session_state["ticker_list"]:
        with st.container(border=True):
            st.info("入力された証券コード", icon="💰")
            for item in st.session_state["ticker_list"]:
                ticker_col1, ticker_col2 = st.columns([1, 1.5])
                with ticker_col1:
                    st.write(f"- {item}")

                with ticker_col2:
                    if st.button(f"Delete! {item}", key=item, icon=":material/delete:"):
                        st.session_state["ticker_list"].remove(item)
                        st.rerun()

        tick_list_dict = {"ticker_list": st.session_state["ticker_list"]}

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            filename_toml, data_toml, mime_toml = generate_download_file(
                "toml", tick_list_dict
            )
            st.download_button(
                label="Download Tick List as TOML",
                data=data_toml,
                file_name=filename_toml,
                mime=mime_toml,
                key="download_toml",
                type="secondary",
                icon=":material/download:",
            )

        with col2:
            filename_json, data_json, mime_json = generate_download_file(
                "json", tick_list_dict
            )
            st.download_button(
                label="Download Tick List as JSON",
                data=data_json,
                file_name=filename_json,
                mime=mime_json,
                key="download_json",
                type="secondary",
                icon=":material/download:",
            )

        if st.button(
            "Reset List",
            key="reset_ticker_list",
            type="secondary",
            icon=":material/delete:",
        ):
            st.session_state["ticker_list"] = []
            st.rerun()
