import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import time
import streamlit.components.v1 as components
import plotly.graph_objects as go
from plotScatter import *


def correlation_heatmap(df):
    # 计算相关性矩阵
    df = df[['duration_minutes', "distance_km", 'speed', 'second_class_seat']]
    corr_matrix = df.corr()

    # 使用Plotly Express创建相关性热力图
    fig = px.imshow(corr_matrix,
                    text_auto=True,
                    height=500,
                    color_continuous_scale='RdBu_r',
                    labels=dict(color="Correlation"),
                    zmin=-1, zmax=1)

    fig.update_layout(title='Correlation Heatmap',
                      xaxis_nticks=36)

    return fig


def violin_plot(df, columns, logif='None'):
    """
    使用Plotly为DataFrame的特定列绘制提琴图。

    参数:
    df (pd.DataFrame): 数据集。
    columns (list): 需要绘制提琴图的列名列表。
    logif (str): 'None' 或 'log'，用于指定y轴是否为对数尺度。

    返回:
    fig: Plotly图形对象。
    """
    fig = go.Figure()

    # 定义颜色列表
    colors = px.colors.qualitative.Plotly

    # 添加每个列的数据到提琴图中
    for i, column in enumerate(columns):
        y_data = df[column]
        if logif == 'log':
            y_data = y_data[y_data > 0]  # 仅保留正值以绘制对数轴

        fig.add_trace(go.Violin(y=y_data,
                                name=column,
                                box_visible=True,
                                points='all',
                                meanline_visible=True,
                                line_color=colors[i % len(colors)],
                                fillcolor=colors[i % len(colors)],
                                opacity=0.6))

    # 如果需要对数尺度，更新y轴类型
    if logif == 'log':
        fig.update_yaxes(type='log')

    # 更新布局
    fig.update_layout(
        title='Violin Plot',
        yaxis=dict(
            title='Values',
            zeroline=False,
            rangemode='tozero'
        ),
        xaxis_title='Columns'
    )

    return fig


if __name__ == '__main__':

    # 设置页面配置
    st.set_page_config(layout="wide", page_title="上海高铁数据-时距速价综合",
                       page_icon=":mag:")
    st.title('🚂上海高铁数据-时距速价综合')

    # 读取CSV文件
    df = pd.read_csv("data/sh_price_info_with_distance.csv")
    df_rank = pd.read_csv("data/access_value_info.csv")
    df_geo = pd.read_csv("data/station_geo.csv")

    merged_df = pd.merge(df, df_rank,
                         left_on='arrival_station', right_on='station', how='inner')
    merged_df = pd.merge(merged_df, df_geo, left_on='arrival_station',
                         right_on='station', how='inner')

    df = merged_df

    # 提取 size 列中的数字部分
    # df['size'] = (6 - df['rank'].str.extract('(\d+)').astype(int))
    df['size'] = df['value']
    # 将值为 -1 的元素替换为 1
    df.replace(-1, 1, inplace=True)

    # 将时间字符串解析成datetime对象
    df['start_time'] = pd.to_datetime(df['start_time'], format="%H:%M:%S")
    df['end_time'] = pd.to_datetime(df['end_time'], format="%H:%M:%S")

    # 将持续时间转换为分钟
    df['duration_minutes'] = df['duration'].str.split(
        ':').apply(lambda x: int(x[0]) * 60 + int(x[1]))

    df['speed'] = df["distance_km"] / df['duration_minutes'] * 60

    st.subheader("相关性热力图")

    st.plotly_chart(correlation_heatmap(df),
                    use_container_width=True, theme=None)

    # 界面布局中间区域的地图显示

    st.subheader("提琴图")

    log_box = st.radio(
        "点击下方按钮对y轴取对数",
        ('None', 'log'))
    row1, row2, row3 = st.columns((1, 1, 1))
    with row1:
        fig = violin_plot(df, ["duration_minutes"], log_box)
        st.plotly_chart(fig, use_container_width=True, theme=None)
    with row2:
        fig = violin_plot(df, ["distance_km"], log_box)
        st.plotly_chart(fig, use_container_width=True, theme=None)
    with row3:
        fig = violin_plot(df, ["speed"], log_box)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    fig = violin_plot(
        df, ["business_seat", "first_class_seat", "second_class_seat", "soft_sleeper", "hard_sleeper",  "hard_seat"], log_box)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    st.subheader("散点气泡图")

    st.plotly_chart(sca_dur_dis(df), use_container_width=True, theme=None)
    st.plotly_chart(sca_price_dis(df), use_container_width=True, theme=None)
    st.plotly_chart(sca_speed_dis(df), use_container_width=True, theme=None)
