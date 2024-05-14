import pandas as pd
import plotly.graph_objects as go
from load_data import *

# 桑基图绘制函数


def sankey_plot():

    station_geo_df = load_station_geo()
    access_value_df = load_access_value_info()

    # 合并两个数据集
    combined_df = pd.merge(station_geo_df, access_value_df,
                           left_on='station', right_on='station', how='inner')

    # 对每个地理区划和通达等级进行汇总
    summarized_df = combined_df.groupby(
        ['Geographical Zone', 'rank']).sum().reset_index()

    # 获取地理区划和通达等级的唯一值作为节点
    geographical_zones = summarized_df['Geographical Zone'].unique().tolist()
    ranks = summarized_df['rank'].unique().tolist()

    # 创建节点列表
    nodes = geographical_zones + ranks

    # 创建节点索引字典
    node_indices = {node: idx for idx, node in enumerate(nodes)}

    # 创建链接列表
    links = []

    # 添加地理区划到通达等级的链接
    for idx, row in summarized_df.iterrows():
        source = node_indices[row['Geographical Zone']]
        target = node_indices[row['rank']]
        value = row['value']
        links.append({'source': source, 'target': target, 'value': value})

    # 创建桑基图
    fig = go.Figure(go.Sankey(
        node=dict(
            line=dict(color='black', width=0.5),
            label=nodes
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
        ),
    ))

    return fig


if __name__ == '__main__':

    # 读取数据集
    station_geo_df = pd.read_csv("data/station_geo.csv")
    access_value_df = pd.read_csv("data/access_value_info.csv")

    # 调用函数绘制桑基图
    fig = sankey_plot(station_geo_df, access_value_df)
    fig.show()
