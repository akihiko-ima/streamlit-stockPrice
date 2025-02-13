import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def login_page() -> None:
    """Renders a login form in a Streamlit application."""

    with open("./.secrets.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)
    # -----------------------------------------------------
    # Pre-hashing all plain text passwords once
    # -----------------------------------------------------
    # stauth.Hasher.hash_passwords(config["credentials"])
    # with open("./credentials.yml", "w") as file:
    # yaml.dump(config, file, default_flow_style=False)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        auto_hash=bool,
    )

    try:
        auth = authenticator.login("main")
    except Exception as e:
        st.error(e)

    # All the authentication info is stored in the session_state
    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "main")
        st.toast("ログインに成功しました")
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
        st.stop()
    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")
        st.stop()

    st.title(":rocket: Protected Application")
    st.write(f'Welcome: *{st.session_state["username"]}*')
