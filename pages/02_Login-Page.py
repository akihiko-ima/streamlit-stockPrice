import streamlit as st
import pandas as pd
from utils.auth import Login_authentication

# ユーザー名とパスワードの入力フォーム
st.header("Login", divider="blue")

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

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Submit")
    if submitted:
        auth_result = Login_authentication(target_name=username, valid_pasword=password)
        if isinstance(auth_result, bool) and auth_result:
            st.success("Login Success")
            st.balloons()
            st.session_state["login_auth"] = True
        elif isinstance(auth_result, str):
            st.error(auth_result)
            st.session_state["login_auth"] = False
