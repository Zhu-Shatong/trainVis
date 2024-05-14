import pandas as pd
import plotly.express as px
from load_data import *


def plot_train_stack():

    df = load_sh_price_info_with_distance()

    # 计算每个出发站的火车数量
    departure_counts = df['departure_station'].value_counts()
    # 创建一个空的DataFrame来存储堆叠数据
    stacked_data = pd.DataFrame()

    # 对于每个出发站，计算不同到达站的火车数量并堆叠
    for departure_station, count in departure_counts.items():
        # 选择出发站为当前站的所有行
        departure_df = df[df['departure_station'] == departure_station]
        # 计算不同到达站的火车数量
        arrival_counts = departure_df['arrival_station'].value_counts()
        # 将结果添加到堆叠数据中
        stacked_data = pd.concat([stacked_data, arrival_counts], axis=1)

    # 将NaN值替换为0
    stacked_data = stacked_data.fillna(0)
    # 重命名列名为出发站
    stacked_data.columns = departure_counts.index

    # 计算每个车站的总和
    stacked_data['总和'] = stacked_data.sum(axis=1)

    # 按照总和大小对 DataFrame 进行排序
    stacked_data = stacked_data.sort_values(by='总和', ascending=False)

    # 删除添加的总和列
    stacked_data.drop(columns='总和', inplace=True)

    # print(stacked_data.head(30))

    # 绘制堆叠图
    fig = px.bar(stacked_data, x=stacked_data.index, y=stacked_data.columns, height=900,
                 title="Train Counts by Arrival Station for Each Departure Station",
                 labels={'index': 'Arrival Station', 'value': 'Train Counts'},
                 barmode='stack')
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        )
    )

    # 旋转x轴标签
    fig.update_layout(xaxis_tickangle=-45)
    return fig


if __name__ == '__main__':

    plot_train_stack().show()
