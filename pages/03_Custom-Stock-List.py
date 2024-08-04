import streamlit as st
from streamlit_cookies_controller import CookieController
import toml

# ユーザー名とパスワードの入力フォーム
st.header("Setting-Stock-List", divider="blue")

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# use cookie
controller = CookieController()

if "ticker_list" not in st.session_state:
    st.session_state["ticker_list"] = []

# st.write("st.session_state object:", st.session_state)

tick = st.text_input("Enter in your favorite Tick")
if st.button("Add List", key="Add_tick_to_List"):
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
