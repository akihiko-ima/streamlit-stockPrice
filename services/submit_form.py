import streamlit as st
import requests
import os
import time
from typing import Dict, Any
from dotenv import load_dotenv


def submit_form(
    name: str, email: str, body: str, from_site: str = "streamlit"
) -> Dict[str, Any]:
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
