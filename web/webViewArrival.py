import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st




# 加载车站地理位置信息
@st.cache_data
def load_station_geo():
    return pd.read_csv("data/final_merged_stations_geo_continuous_save.csv", index_col="Station")

# 加载列车出发信息，并结合车站地理位置
@st.cache_data
def load_train_data():
    train_data = pd.read_csv("data/sh_price_info.csv")
    station_geo = load_station_geo()
    
    # 映射车站经纬度到列车数据中
    train_data['lat'] = train_data['arrival_station'].map(station_geo['lat'])
    train_data['lon'] = train_data['arrival_station'].map(station_geo['lng'])
    
    # 选择需要的列并确保数据完整性
    train_data = train_data[['start_time', 'arrival_station', 'lat', 'lon']]
    train_data.dropna(inplace=True)  # 删除任何因缺少经纬度信息而无法使用的行
    
    # 先将 "start_time" 列转换为 datetime 类型
    train_data['start_time'] = pd.to_datetime(train_data['start_time'], format='%H:%M:%S')
    
    return train_data

# 数据预处理，计算每个地点的记录数
def preprocess_data(data):
    # 统计每个站点的到达次数
    count_data = data.groupby(['arrival_station', 'lon', 'lat']).size().reset_index(name='count')
    return count_data




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
        get_fill_color="[count * 2.55 , 0 , (255 - count * 2.55), 150]",  # 颜色渐变，count越大，越红
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
@st.cache_data
def filterdata(df, hour_selected):
    return df[df["start_time"].dt.hour == hour_selected]

# 计算给定数据集的中心点
@st.cache_data
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# 根据小时生成直方图数据
@st.cache_data
def histdata(df, hr):
    filtered = df[(df["start_time"].dt.hour >= hr) & (df["start_time"].dt.hour < (hr + 1))]
    hist = np.histogram(filtered["start_time"].dt.minute, bins=60, range=(0, 60))[0]
    return pd.DataFrame({"minute": range(60), "pickups": hist})




if __name__ == '__main__':

    # 设置页面配置
    st.set_page_config(layout="wide", page_title="列车出发时间与位置", page_icon=":train:")





    # 主程序开始
    data = load_train_data()

    # 界面布局顶部区域
    row1_1, row1_2 = st.columns((2, 3))

    # 检查URL中是否有查询参数
    if not st.session_state.get("url_synced", False):
        try:
            pickup_hour = int(st.query_params["pickup_hour"][0])
            st.session_state["pickup_hour"] = pickup_hour
            st.session_state["url_synced"] = True
        except KeyError:
            pass

    # 如果滑块改变，更新查询参数
    def update_query_params():
        hour_selected = st.session_state["pickup_hour"]
        st.query_params["pickup_hour"] = hour_selected

    with row1_1:
        st.title("纽约市Uber拼车数据")
        hour_selected = st.slider("选择接客时间", 0, 23, key="pickup_hour", on_change=update_query_params)

    with row1_2:
        st.write("""
        ## 
        观察纽约市及其主要区域机场的Uber接客变化。
        通过左侧滑块选择不同的时间段，探索不同的交通趋势。
        """)

    # 界面布局中间区域的地图显示
    row2_1, row2_2, row2_3, row2_4 = st.columns((2, 1, 1, 1))

    # 设置机场的位置和缩放级别
    la_guardia = [40.7900, -73.8700]
    jfk = [40.6650, -73.7821]
    newark = [40.7090, -74.1805]
    zoom_level = 12
    midpoint = mpoint(data["lat"], data["lon"])

    with row2_1:
        st.write(f"""**纽约市全景从{hour_selected}:00到{(hour_selected + 1) % 24}:00**""")
        map(preprocess_data(data), midpoint[0], midpoint[1], 11)

    with row2_2:
        st.write("**拉瓜迪亚机场**")
        map(preprocess_data(filterdata(data, hour_selected)), la_guardia[0], la_guardia[1], zoom_level)

    with row2_3:
        st.write("**肯尼迪机场**")
        map(preprocess_data(filterdata(data, hour_selected)), jfk[0], jfk[1], zoom_level)

    with row2_4:
        st.write("**纽瓦克机场**")
        map(preprocess_data(filterdata(data, hour_selected)), newark[0], newark[1], zoom_level)

    # 计算直方图数据并展示
    chart_data = histdata(data, hour_selected)
    st.write(f"""**每分钟的接客数据从{hour_selected}:00到{(hour_selected + 1) % 24}:00**""")
    st.altair_chart(
        alt.Chart(chart_data).mark_area(interpolate="step-after").encode(
            x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
            y=alt.Y("pickups:Q"),
            tooltip=["minute", "pickups"],
        ).configure_mark(opacity=0.2, color="red"),
        use_container_width=True,
    )
