from dataclasses import dataclass
from typing import Dict, Callable

# import your streamlit page
from views import (
    us_stock_page,
    japan_stock_page,
    login_page,
    custom_stock_list_page,
    qrcode_page,
    contact_me_page,
)


@dataclass
class RouterMapping:
    routing_name: str
    icon: str
    streamlit_page: Callable[[], None]


# router mapping
"""
・If you have any pages you would like to route, please add them here.
・The icons in the sidebar use "Google Fonts."
 [https://fonts.google.com/icons](https://fonts.google.com/icons)
"""
routers: Dict[str, RouterMapping] = {
    "router_1": RouterMapping(
        routing_name="main", icon="home", streamlit_page=us_stock_page
    ),
    "router_2": RouterMapping(
        routing_name="JapanStock",
        icon="radio_button_checked",
        streamlit_page=japan_stock_page,
    ),
    "router_3": RouterMapping(
        routing_name="Login", icon="login", streamlit_page=login_page
    ),
    "router_4": RouterMapping(
        routing_name="Settings", icon="settings", streamlit_page=custom_stock_list_page
    ),
    "router_5": RouterMapping(
        routing_name="QR", icon="qr_code", streamlit_page=qrcode_page
    ),
    "router_6": RouterMapping(
        routing_name="Contact", icon="send", streamlit_page=contact_me_page
    ),
}
