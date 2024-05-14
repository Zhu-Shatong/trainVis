from st_pages import Page, show_pages
import streamlit as st


show_pages(
    [
        Page("./web/web1DatasetView.py", "数据集与任务一览", "🚃"),
        Page("./web/web2NationStation.py", "全国高铁站可视化", "🚝"),
        Page("./web/web3NationalTrain.py", "全国高铁线路可视化", "🚆"),
        Page("./web/web4SHTime.py", "上海高铁数据-时间可视化", "🚉"),
        Page("./web/web5SHSpace.py", "上海高铁数据-空间可视化", "🚈"),
        Page("./web/web6SHothers.py", "上海高铁数据-时距速价综合", "🚂"),
        Page("./web/webViewData.py", "查询功能", "🚵🏼‍♀️"),
    ]
)
