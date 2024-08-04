import streamlit as st
import requests
import os
import time
from typing import Dict, Any
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError


# Read env. file
load_dotenv()
CONTACT_API_ENDPOINT = os.getenv("CONTACT_API_ENDPOINT")


st.set_page_config(layout="wide")


def submit_form(
    name: str, email: str, body: str, from_site: str = "streamlit"
) -> Dict[str, Any]:
    data = {"name": name, "email": email, "body": body, "from_site": from_site}

    # HTTP POST method
    response = requests.post(CONTACT_API_ENDPOINT, data=data)

    # response message
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": "An error occurred."}


col1, col2, col3 = st.columns([0.25, 3, 0.25])

## Contact form
with col2:
    st.header("✉️ Contact Me")
    name = st.text_input(
        "**Your name***", value=st.session_state.get("name", ""), key="name"
    )
    email = st.text_input(
        "**Your email***", value=st.session_state.get("email", ""), key="email"
    )
    body = st.text_area(
        "**Your message***", value=st.session_state.get("body", ""), key="body"
    )

    st.markdown(
        '<p style="font-size: 13px;">*Required fields</p>', unsafe_allow_html=True
    )

    if st.button("Send", type="primary"):
        if not name or not email or not body:
            st.error("Please fill out all required fields.")
        else:
            try:
                valid = validate_email(email, check_deliverability=True)

                response: Dict[str, Any] = submit_form(name, email, body)

                if response["message"] == "success!":
                    st.toast("""success!""", icon="✅")
                    time.sleep(2)
                else:
                    st.error("Some error has occurred.")

            except EmailNotValidError as e:
                st.error(f"Invalid email address. {e}")
