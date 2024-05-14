import pandas as pd
import plotly.express as px

from load_data import *


def plot_rank_relationship(a=0, b=20):

    df = load_access_value_info()

    # 筛选排名在指定范围内的数据
    df_filtered = df[a:b]

    # 按值字段降序排序
    df_filtered_sorted = df_filtered.sort_values(by='value', ascending=True)

    # 绘制横向直方图
    fig = px.bar(df_filtered_sorted, y='station', x='value',
                 hover_data=['value'],  # 鼠标悬停显示数值
                 color='value',  # 柱状图颜色根据数值大小自动着色
                 labels={'station': 'Station', 'value': 'Value'},  # 设置轴标签
                 height=750,  # 图表高度
                 width=800,  # 图表宽度
                 orientation='h',  # 横向直方图
                 color_continuous_scale='plasma'
                 )

    # 显示图表
    return fig


if __name__ == '__main__':
    # 调用函数并显示图表
    fig = plot_rank_relationship("data/access_value_info.csv")
    fig.show()
