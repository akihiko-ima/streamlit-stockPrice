import streamlit as st
import pandas as pd
from utils.auth import Login_authentication

# ユーザー名とパスワードの入力フォーム
st.title("ログイン画面")

with st.form("login_form"):
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    submitted = st.form_submit_button("Submit")
    if submitted:
        auth_result = Login_authentication(target_name=username, valid_pasword=password)
        if isinstance(auth_result, bool) and auth_result:
            st.success("ログイン成功")
            st.balloons()
        elif isinstance(auth_result, str):
            st.error(auth_result)
