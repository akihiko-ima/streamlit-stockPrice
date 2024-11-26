from config import routers

router_mappings = {}
for _, router in routers.items():
    router_mappings[router.routing_name] = router.streamlit_page
