import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# 加载车站地理位置信息


@st.cache_data
def load_access_value_info():
    return pd.read_csv("data/access_value_info.csv", encoding='utf-8')


@st.cache_data
def load_station_geo():
    return pd.read_csv("data/station_geo.csv", encoding='utf-8')


@st.cache_data
def load_sh_price_info_with_distance():
    df = pd.read_csv("data/sh_price_info_with_distance.csv", encoding='utf-8')
    df['start_time'] = pd.to_datetime(
        df['start_time'], format='%H:%M:%S').dt.strftime('%H:%M')
    df['start_time'] = pd.to_datetime(df['start_time'], format='%H:%M').dt.time
    return df


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
    train_data['start_time'] = pd.to_datetime(
        train_data['start_time'], format='%H:%M:%S')

    return train_data

# 数据预处理，计算每个地点的记录数


def preprocess_data(data):
    # 统计每个站点的到达次数
    count_data = data.groupby(
        ['arrival_station', 'lon', 'lat']).size().reset_index(name='count')
    return count_data


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
    filtered = df[(df["start_time"].dt.hour >= hr) &
                  (df["start_time"].dt.hour < (hr + 1))]
    hist = np.histogram(
        filtered["start_time"].dt.minute, bins=60, range=(0, 60))[0]
    return pd.DataFrame({"minute": range(60), "pickups": hist})
