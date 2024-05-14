from st_pages import Page, show_pages
import streamlit as st


show_pages(
    [
        Page("./web/web1NationStation.py", "全国高铁站数据", "🎈️"),
        Page("./web/web2NationalTrain.py", "全国高铁线路数据", "🎈️"),
        Page("./web/webViewData.py", "数据", "🎈️"),
        Page("./web/webViewArrival.py", "地图", "📈"),
    ]
)
