import streamlit as st
import streamlit.components.v1 as components

from plotLineChart import *

if __name__ == '__main__':

    # 设置页面配置
    st.set_page_config(layout="wide", page_title="上海高铁数据-时间可视化",
                       page_icon=":date:")

    st.title('上海高铁数据-时间可视化')

    st.title('24小时观测')

    col1, col2 = st.columns([1, 1])
    # 左侧是相关性热力图
    col1.subheader("折线图")
    htmappt = plot_hourly_counts()
    col1.plotly_chart(htmappt, use_container_width=True, theme=None)

    # 右侧是散点图
    col2.subheader("极坐标折线图")
    htmappt2 = plot_hourly_counts2()
    col2.plotly_chart(htmappt2, use_container_width=True, theme=None)

    st.title("小时内规律观测")
    fig = plot_five_minute_intervals()
    st.plotly_chart(fig, use_container_width=True, theme=None)

