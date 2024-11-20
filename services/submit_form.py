import streamlit as st
import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv


def submit_contact_form_data(
    name: str, email: str, body: str, from_site: str = "streamlit"
) -> Dict[str, Any]:
    """
    Submits a contact form by sending the provided data to an API endpoint.

    This function reads the API endpoint from an environment variable,
    constructs a data payload using the provided arguments, and sends
    the data using an HTTP POST request. It handles the response and
    returns a parsed JSON object or an error message.

    Args:
        name (str): The name of the person submitting the form.
        email (str): The email address of the person submitting the form.
        body (str): The message or content of the form submission.
        from_site (str, optional): Identifies the source of the submission.
                                   Defaults to "streamlit".

    Returns:
        Dict[str, Any]: A dictionary containing the API's response. If the
                        request is successful, the parsed JSON response is
                        returned. Otherwise, a dictionary with an error
                        message is returned.
    """
    # Read env. file
    load_dotenv()
    CONTACT_API_ENDPOINT = os.getenv("CONTACT_API_ENDPOINT")

    data = {"name": name, "email": email, "body": body, "from_site": from_site}

    # HTTP POST method
    response = requests.post(CONTACT_API_ENDPOINT, data=data)

    # response message
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": "An error occurred."}
