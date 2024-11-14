import streamlit as st
from st_on_hover_tabs import on_hover_tabs


def sidebar_component():
    with st.sidebar:
        tabs = on_hover_tabs(
            tabName=["main", "JapanStock", "Login", "Settings", "Contact"],
            iconName=["home", "radio_button_checked", "login", "settings", "send"],
            styles={
                "navtab": {
                    "background-color": "#111",
                    "color": "#818181",
                    "font-size": "18px",
                    "transition": ".3s",
                    "white-space": "nowrap",
                    "text-transform": "uppercase",
                },
                "tabStyle": {":hover :hover": {"color": "red", "cursor": "pointer"}},
                "tabStyle": {
                    "list-style-type": "none",
                    "margin-bottom": "30px",
                    "padding-left": "30px",
                },
                "iconStyle": {
                    "position": "fixed",
                    "left": "7.5px",
                    "text-align": "left",
                },
            },
            key="0",
            default_choice=0,
        )
    return tabs
