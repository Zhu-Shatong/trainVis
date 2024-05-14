import pandas as pd

import plotly.express as px

from load_data import *

# 旭日图绘制函数


def sunburst_plot():

    # 加载站点地理信息数据
    station_geo_df = load_access_value_info()
    # 加载通达度数据
    access_value_df = load_station_geo()

    # 将通达度数据按照站点名称和通达度值进行合并
    merged_df = pd.merge(station_geo_df, access_value_df,
                         left_on='station', right_on='station', how='left')

    filtered_df = merged_df.dropna(
        subset=['Geographical Zone', 'Province', 'City'])
    filtered_df = filtered_df[filtered_df['Geographical Zone'] != '未知']
    filtered_df = filtered_df[filtered_df['Province'] != '未知']
    filtered_df = filtered_df[filtered_df['City'] != '未知']
    filtered_df = filtered_df.dropna(subset=['value'])
    filtered_df = filtered_df[filtered_df['value'] != -1]

    # filtered_df.to_csv("1.csv")

    fig = px.sunburst(filtered_df, path=['Geographical Zone', 'Province', 'City', 'station'], values='value',
                      color='value',
                      height=900,
                      color_continuous_scale=px.colors.diverging.RdYlGn, color_continuous_midpoint=7,
                      title='火车站通达度旭日图')
# 可以加station , 'station'
    # fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig


if __name__ == '__main__':

    # 使用函数绘制旭日图
    sunburst_plot().show()
