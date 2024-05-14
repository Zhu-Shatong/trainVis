import pandas as pd
import plotly.express as px


def sca_dur_dis(df):
    # 绘制散点图
    fig = px.scatter(df, x="distance_km", y="duration_minutes",
                     hover_data=["arrival_station",
                                 "size", "Geographical Zone"],
                     size="size", color="Geographical Zone")

    # 设置图表布局
    fig.update_layout(
        title="Train Duration vs. Distance",
        xaxis_title="Distance (km)",
        yaxis_title="Duration (minutes)",
        hovermode="closest",
        height=900,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="linear"
        )
    )
    return fig


def sca_price_dis(df):
    # 绘制散点图
    fig = px.scatter(df, x="distance_km", y="second_class_seat",
                     hover_data=["arrival_station",
                                 "size", "Geographical Zone"],
                     size="size", color="Geographical Zone")

    # 设置图表布局
    fig.update_layout(
        title="Price vs. Distance",
        xaxis_title="Distance (km)",
        yaxis_title="Price (yuan)",
        hovermode="closest",
        height=900,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="linear"
        )
    )
    return fig


def sca_speed_dis(df):
    # 绘制散点图
    fig = px.scatter(df, x="distance_km", y="speed",
                     hover_data=["arrival_station",
                                 "size", "Geographical Zone"],
                     size="size", color="Geographical Zone")

    # 设置图表布局
    fig.update_layout(
        title="Speed vs. Distance",
        xaxis_title="Distance (km)",
        yaxis_title="Speed (km/h)",
        hovermode="closest",
        height=900,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="linear"
        )
    )
    return fig


if __name__ == '__main__':

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

    sca_speed_dis(df).show()
