import streamlit as st
from st_on_hover_tabs import on_hover_tabs

from config import routers


def sidebar_component() -> str:
    """
    Creates a custom sidebar component in a Streamlit application using `st_on_hover_tabs`.

    The sidebar includes multiple tabs with specific icons and styles for navigation.
    The tabs are defined by their names and associated icons, and custom styles are
    applied to the navigation and tab elements.

    Returns:
        str: The name of the currently selected tab.
    """
    with st.sidebar:
        tabs = on_hover_tabs(
            tabName=[router.routing_name for router in routers.values()],
            iconName=[router.icon for router in routers.values()],
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
