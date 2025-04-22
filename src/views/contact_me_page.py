import streamlit as st
import time
from typing import Dict, Any
from email_validator import validate_email, EmailNotValidError

from services.submit_form import submit_contact_form_data


def contact_me_page() -> None:
    """Renders a contact form in a Streamlit application."""
    col1, col2, col3 = st.columns([0.25, 3, 0.25])
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

        if st.button("Send", type="primary", icon=":material/send:"):
            if not name or not email or not body:
                st.error("Please fill out all required fields.")
            else:
                try:
                    valid = validate_email(email, check_deliverability=True)
                    response: Dict[str, Any] = submit_contact_form_data(
                        name, email, body
                    )

                    if response["message"] == "success!":
                        st.toast("""success!""", icon="✅")
                        time.sleep(2)
                    else:
                        st.error("Some error has occurred.")

                except EmailNotValidError as e:
                    st.error(f"Invalid email address. {e}")
