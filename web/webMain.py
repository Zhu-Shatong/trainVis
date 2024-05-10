from st_pages import Page, show_pages
import streamlit as st





show_pages(
    [
        Page("./web/webViewData.py", "数据", "🎈️"),
        Page("./web/webViewArrival.py","地图","📈"),
    ]
)

