import pandas as pd
import plotly.express as px

from load_data import *


def generate_heatmap():
    # 确保数据加载时考虑中文字符的编码
    access_df = load_access_value_info()
    station_data = load_station_geo()

    # 合并数据帧在站名上
    merged_df = pd.merge(station_data, access_df, on='station', how='inner')

    # 过滤掉 access value 为 -1 的行
    filtered_df = merged_df[merged_df['value'] != -1]

    # 生成热力图，使用中文名字作为悬浮提示信息
    fig = px.density_mapbox(filtered_df, lat='lat', lon='lng', z='value', radius=32,
                            center=dict(lat=35, lon=104), zoom=3.7,
                            mapbox_style="open-street-map",
                            hover_data={'station': True},
                            height=900,
                            color_continuous_scale='plasma')  # 显示中文站名

    return fig


if __name__ == "__main__":
    heatmap = generate_heatmap()
    heatmap.show()
