import streamlit as st
import toml
from streamlit_cookies_controller import CookieController


def custom_stock_list_page() -> None:
    """Renders a Create a list of stock prices in a Streamlit application."""
    st.header("Setting-Stock-List", divider="blue")

    controller = CookieController()

    if "ticker_list" not in st.session_state:
        st.session_state["ticker_list"] = []

    tick = st.text_input("Enter in your favorite Tick", placeholder="e.g. KO, MS, MSFT")

    if st.button(
        "Add List", key="Add_tick_to_List", type="primary", icon=":material/add:"
    ):
        if not tick:
            st.error("Enter in your favorite Tick")
        else:
            st.session_state["ticker_list"].append(tick)

    # toggle for showing tick list
    show_list = st.toggle("Show Tick List")
    if show_list:
        if st.session_state["ticker_list"]:
            for item in st.session_state["ticker_list"]:
                st.write(f"- {item}")

            if st.button("Add cookie", key="Add_tickList_to_Cookie"):
                controller.set("ticker_list", st.session_state["ticker_list"])

            # making toml file
            tick_list_dict = {"ticker_list": st.session_state["ticker_list"]}
            toml_str = toml.dumps(tick_list_dict)
            toml_bytes = toml_str.encode("utf-8")

            st.download_button(
                label="Download Tick List as TOML",
                data=toml_bytes,
                file_name="ticker_list.toml",
                mime="application/toml",
            )

        else:
            st.write("Ticker_list is empty.")
