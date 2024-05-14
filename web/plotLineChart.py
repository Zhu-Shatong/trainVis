import pandas as pd
import plotly.graph_objects as go

from load_data import *


def plot_hourly_counts():

    # 读取CSV文件
    df = load_sh_price_info_with_distance()

    # 将时间字符串解析成datetime对象
    df['start_time'] = pd.to_datetime(df['start_time'], format="%H:%M:%S")

    # 提取小时部分
    df['hour'] = df['start_time'].dt.hour

    # 按小时进行分组并计数
    hourly_counts = df.groupby('hour').size()

    # 创建图形
    fig = go.Figure()

    # 添加折线图
    fig.add_trace(go.Scatter(x=hourly_counts.index,
                  y=hourly_counts, mode='lines+markers', name='Counts'))

    # 更新布局
    fig.update_layout(
        title='Hourly Traffic Counts',
        xaxis_title='Hour of the Day',
        yaxis_title='Count',
        xaxis=dict(tickmode='linear'),  # 确保X轴为线性标度
        template='plotly_white'  # 使用明亮的背景主题
    )

    return fig


def plot_hourly_counts2():

    # 读取CSV文件
    df = load_sh_price_info_with_distance()

    # 将时间字符串解析成datetime对象
    df['start_time'] = pd.to_datetime(df['start_time'], format="%H:%M:%S")

    # 提取小时部分
    df['hour'] = df['start_time'].dt.hour

    # 按小时进行分组并计数
    hourly_counts = df.groupby('hour').size()

    # Create polar plot
    fig = go.Figure()

    # Add scatter plot on polar coordinates
    fig.add_trace(go.Scatterpolar(
        r=hourly_counts,
        theta=[str(hour) + ":00" for hour in hourly_counts.index],
        mode='lines+markers',
        name='Counts'
    ))

    # Update layout
    fig.update_layout(
        title='Hourly Traffic Counts',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, hourly_counts.max()]
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=[str(hour) + ":00" for hour in hourly_counts.index],
                ticktext=[str(hour) for hour in hourly_counts.index]
            )
        ),
        template='plotly_white'  # Use a bright background theme
    )

    return fig


def plot_five_minute_intervals():

    # 读取CSV文件
    df = load_sh_price_info_with_distance()

    # 将时间字符串解析成datetime对象
    df['start_time'] = pd.to_datetime(df['start_time'], format="%H:%M:%S")

    # 提取小时部分
    df['hour'] = df['start_time'].dt.hour

    # 打印结果
    # print(hourly_counts)
    # plot_hourly_counts(hourly_counts).show()

    # 提取分钟部分并将其分为5分钟间隔
    df['five_minute_interval'] = df['start_time'].dt.minute

    # 按5分钟间隔分组并计数
    five_minute_counts = df.groupby('five_minute_interval').size()

    # 创建图形
    fig = go.Figure()

    # 添加折线图
    fig.add_trace(go.Scatter(
        x=five_minute_counts.index,
        y=five_minute_counts,
        mode='lines+markers',
        name='Traffic Counts'
    ))

    # 更新布局
    fig.update_layout(
        title='Traffic Counts in 5-Minute Intervals',
        xaxis_title='Five-Minute Interval',
        yaxis_title='Count',
        xaxis=dict(
            tickmode='linear'
        ),
        template='plotly_white'
    )

    return fig


if __name__ == '__main__':

    # 打印结果
    # print(five_minute_counts)
    plot_five_minute_intervals().show()
