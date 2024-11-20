import os
import json
import gspread
import pandas as pd
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from typing import Union

load_dotenv()


def get_user_df() -> pd.DataFrame:
    """
    Retrieves data from a Google Sheets document and returns it as a pandas DataFrame.

    Raises:
        ValueError: If the environment variable `GOOGLE_APPLICATION_CREDENTIALS_JSON`
                    is not set or invalid.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the specified
                      Google Sheets document. The first row of the sheet is used
                      as the column headers, and subsequent rows form the data.
    """
    creds_json_str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if creds_json_str is None:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON not found in .env file")

    # JSON文字列を辞書に変換
    creds_json = json.loads(creds_json_str)
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
    client = gspread.authorize(creds)
    SP_SHEET_KEY = os.getenv("GOOGLE_SP_SHEET_KEY")
    sh = client.open_by_key(SP_SHEET_KEY)
    SP_SHEET = os.getenv("GOOGLE_SP_SHEET_NAME")
    worksheet = sh.worksheet(SP_SHEET)
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df


def Login_authentication(target_name: str, valid_pasword: str) -> Union[bool, str]:
    """
    Authenticates a user by verifying the username and password against data
    retrieved from a Google Sheets document.

    Args:
        target_name (str): The username to authenticate.
        valid_pasword (str): The password to validate against the username.

    Returns:
        Union[bool, str]: Returns `True` if the username and password match
                          the record in the data. Returns an error message as a string
                          if the username is not unique, does not exist, or the password
                          is incorrect.
    """
    user_df = get_user_df()

    # user確認
    if (user_df["username"] == target_name).sum() == 1:
        result_index = user_df.index[user_df["username"] == target_name].item()
    else:
        return "The target name is not unique or does not exist."

    # pass確認
    if valid_pasword == user_df.at[result_index, "pass"]:
        return True
    else:
        return "passwordが違います"
