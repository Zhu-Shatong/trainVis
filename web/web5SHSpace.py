import altair as alt
import pandas as pd
import pydeck as pdk
import streamlit as st
from datetime import time

from load_data import *

from plotRose import plot_rose
from plotStack import plot_train_stack
from plotCircle import create_nested_donut_chart


def load_train_data():
    train_data = load_sh_price_info_with_distance()
    station_geo = pd.read_csv("data\station_geo.csv", index_col="station")

    # 映射车站经纬度到列车数据中
    train_data['lat'] = train_data['arrival_station'].map(station_geo['lat'])
    train_data['lon'] = train_data['arrival_station'].map(station_geo['lng'])

    # 选择需要的列并确保数据完整性
    train_data = train_data[['start_time', 'arrival_station', 'lat', 'lon']]
    train_data.dropna(inplace=True)  # 删除任何因缺少经纬度信息而无法使用的行

    return train_data

# 数据预处理，计算每个地点的记录数


# 定义一个函数来绘制地图
def map(data, lat, lon, zoom):
    tooltip = {
        "html": "<b>到达站:</b> {arrival_station}<br><b>记录数:</b> {count}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    # 使用 ColumnLayer 来允许显示每个柱子的数据统计
    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="count",
        elevation_scale=5000,  # 调整适合的高度缩放
        radius=10000,  # 柱子的基底半径
        # 颜色渐变，count越大，越红
        get_fill_color="[count * 2.55 , 0 , (255 - count * 2.55), 150]",
        pickable=True,
        auto_highlight=True,
    )

    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50
            },
            layers=[layer],
            tooltip=tooltip
        )
    )

# 根据选定的小时过滤数据


if __name__ == '__main__':

    # 设置页面配置
    st.set_page_config(layout="wide", page_title="上海高铁数据-空间可视化",
                       page_icon=":train:")

    st.title('🚈上海高铁数据-空间可视化')
    tab1, tab2 = st.tabs(["全国视角", "上海视角"])

    with tab1:

        # 主程序开始
        data = load_train_data()

        # print(data.head())

        # 界面布局顶部区域
        row1_1, row1_2 = st.columns((2, 3))

        # 如果滑块改变，更新查询参数

        with row1_1:
            st.title("上海高铁到达数据")

            time_range = st.slider("选择时间区间", value=(
                time(0, 0), time(23, 59)), format="HH:mm")
            data = data[(data['start_time'] >= time_range[0]) &
                        (data['start_time'] <= time_range[1])]

        with row1_2:
            st.write("""
            观察全国及其主要区域的数据
            通过左侧滑块选择不同的时间段，探索不同的抵达趋势。
            """)

        # 界面布局中间区域的地图显示
        row2_1, row2_2, row2_3, row2_4 = st.columns((3, 1, 1, 1))

        # 设置机场的位置和缩放级别
        la_guardia = [31.371993, 120.524439]
        jfk = [23, 113]
        newark = [39.8, 116.4]
        zoom_level = 5
        midpoint = mpoint(data["lat"], data["lon"])

        with row2_1:
            st.write(
                f"""**全国从{time_range[0]}到{time_range[1]}**""")
            map(data.groupby(
                ['arrival_station', 'lon', 'lat']).size().reset_index(name='count'), 34, 105, 3.7)

        with row2_2:
            st.write("**长三角**")
            map(data.groupby(
                ['arrival_station', 'lon', 'lat']).size().reset_index(name='count'), la_guardia[0], la_guardia[1], zoom_level)

        with row2_3:
            st.write("**珠三角**")
            map(data.groupby(
                ['arrival_station', 'lon', 'lat']).size().reset_index(name='count'), jfk[0], jfk[1], zoom_level)

        with row2_4:
            st.write("**京津冀**")
            map(data.groupby(
                ['arrival_station', 'lon', 'lat']).size().reset_index(name='count'), newark[0], newark[1], zoom_level)

    with tab2:
        st.subheader("玫瑰图")
        st.plotly_chart(plot_rose(), use_container_width=True, theme=None)
        st.subheader("环形图")
        st.plotly_chart(create_nested_donut_chart(),
                        use_container_width=True, theme=None)
        st.subheader("堆叠柱状图")
        st.plotly_chart(plot_train_stack(),
                        use_container_width=True, theme=None)
