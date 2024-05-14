import pandas as pd
import plotly.graph_objects as go
from load_data import *


def create_nested_donut_chart():

    # 读取CSV文件
    df = load_sh_price_info_with_distance()
    df_geo = load_station_geo()

    merged_df = pd.merge(df, df_geo, left_on='end_station',
                         right_on='station', how='inner')

    df = merged_df

    # 提取出发站和到达站的数据
    stations_departure = df['departure_station']
    stations_arrival = df['Geographical Zone']

    # 统计每个站点的出现次数
    station_counts_departure = stations_departure.value_counts()
    station_counts_arrival = stations_arrival.value_counts()

    # 创建环形图的数据
    fig = go.Figure()

    # 添加外部环形图（表示出发站）
    fig.add_trace(go.Pie(
        labels=station_counts_departure.index,
        values=station_counts_departure.values,
        name='departure_station',
        hole=0.7,
        domain={'x': [0, 1]},
        hoverinfo='label+percent+name'
    ))

    # 添加内部环形图（表示到达站），位置稍微调整使其完全嵌套在外部环形图内
    fig.add_trace(go.Pie(
        labels=station_counts_arrival.index,
        values=station_counts_arrival.values,
        name='Geographical Zone',
        hole=0.45,
        domain={'x': [0.4, 0.6]},
        hoverinfo='label+percent+name'
    ))

    # 更新布局
    fig.update_layout(
        title_text="出发站和到达站环形图",
        height=900,
    )

    return fig


if __name__ == '__main__':

    # 创建并显示图形
    fig = create_nested_donut_chart()
    fig.show()
