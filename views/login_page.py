import streamlit as st

from services.auth import Login_authentication


def login_page() -> None:
    """Renders a login form in a Streamlit application."""
    st.header("Login", divider="blue")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button(
            "Login", type="primary", icon=":material/login:"
        )

        if submitted:
            auth_result = Login_authentication(
                target_name=username, valid_pasword=password
            )
            st.write(auth_result)

            if isinstance(auth_result, bool) and auth_result:
                st.success("Login Success")
                st.balloons()
                st.session_state["login_auth"] = True
            elif isinstance(auth_result, str):
                st.error(auth_result)
                st.session_state["login_auth"] = False
