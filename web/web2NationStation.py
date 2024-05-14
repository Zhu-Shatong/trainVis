import streamlit as st
import pandas as pd
from datetime import time
import streamlit.components.v1 as components
from PIL import Image


from plotHeatmap import generate_heatmap
from plotBarStation import plot_rank_relationship
from plotSunBrust import sunburst_plot
from plotSanky import sankey_plot

if __name__ == '__main__':

    # 设置页面配置
    st.set_page_config(layout="wide", page_title="全国高铁站可视化",
                       page_icon=":house:")

    st.title('全国高铁站可视化')

    tab1, tab2, tab3 = st.tabs(
        ["🌟 高铁站全国分布图（仿灯光图）", "📈 高铁站通达度-全国分析", "📱 高铁站通达度-地域分析"])

    with tab1:

        st.title("🌟 高铁站全国分布图（仿灯光图）")

        # 显示火车站散点图
        st.subheader("中国地图散点图 Echarts")

        components.html(open("static\stations.html").read(),
                        width=1485, height=810)

    with tab2:

        st.title("📈 高铁站通达度-全国分析")

        st.subheader("中国地图热力图")
        # 调用函数生成热力图
        heatmap = generate_heatmap()
        # 在 Streamlit 中显示图表
        st.plotly_chart(heatmap, use_container_width=True, theme=None)

        st.subheader("柱状图")
        range = st.slider("选择区间", min_value=0, max_value=300, value=(0, 25))

        fig = plot_rank_relationship(range[0], range[1])
        st.plotly_chart(fig, use_container_width=True, theme=None)

        st.subheader("词云图")
        image = Image.open('static/wordcloud.png')
        st.image(image, caption='高铁站通达度词云', use_column_width=True)

    with tab3:

        st.title("📱 高铁站通达度-地域分析")
        # 使用函数绘制旭日图
        st.subheader("旭日图")
        sunburstplot = sunburst_plot()
        st.plotly_chart(sunburstplot, use_container_width=True,
                        theme=None)

        st.subheader("桑基图")
        # 调用函数绘制桑基图
        fig = sankey_plot()
        st.plotly_chart(fig, use_container_width=True, theme=None)
