import pandas as pd
import os
from dotenv import load_dotenv
import json
import gspread
from google.oauth2.service_account import Credentials
from typing import Union

load_dotenv()


def get_user_df() -> pd.DataFrame:
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
