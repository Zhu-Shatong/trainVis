# visualization.py

import pandas as pd
from pyecharts.charts import Geo
from pyecharts import options as opts


def merge_data(all_train_csv, final_merged_stations_csv):
    """
    合并两个数据文件
    :param all_train_csv: 车次信息的CSV文件路径
    :param final_merged_stations_csv: 车站信息的CSV文件路径
    :return: 合并后的数据框
    """
    all_train_df = pd.read_csv(all_train_csv)
    final_merged_stations_df = pd.read_csv(final_merged_stations_csv)

    merged_df = pd.merge(all_train_df, final_merged_stations_df,
                         left_on='origin_station', right_on='station', how='inner')
    merged_df = pd.merge(merged_df, final_merged_stations_df, left_on='destination_station',
                         right_on='station', suffixes=('_origin', '_destination'), how='inner')

    return merged_df


def airports_viz(merged_data):
    """
    绘制火车站散点图
    :param merged_data: 合并后的数据
    :return: pyecharts GEO图表实例
    """
    geo = Geo(
        init_opts=opts.InitOpts(
            theme='dark',
            bg_color='#000000',
            width='1980px',
            height='1080px'
        )
    )

    data_pair = []
    for idx, row in merged_data.iterrows():
        geo.add_coordinate(row["origin_station"],
                           row["lng_origin"], row["lat_origin"])
        geo.add_coordinate(row["destination_station"],
                           row["lng_destination"], row["lat_destination"])
        data_pair.append((row["origin_station"], 1))
        data_pair.append((row["destination_station"], 1))

    geo.add_schema(
        maptype="china",
        is_roam=False,  # 禁止缩放
        itemstyle_opts=opts.ItemStyleOpts(
            color="#000000", border_color="#1E90FF"
        ),
        emphasis_label_opts=opts.LabelOpts(is_show=False),
        emphasis_itemstyle_opts=opts.ItemStyleOpts(color="#323c48")
    )

    geo.add("火车站",
            data_pair,
            type_='scatter',
            is_selected=True,
            symbol_size=2,
            is_large=True,
            itemstyle_opts=opts.ItemStyleOpts(color="#FFD700")
            )

    # 关闭Label显示
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    geo.set_global_opts(
        title_opts=opts.TitleOpts(
            title="火车站分布", pos_top='3%', pos_left='center'),
        tooltip_opts=opts.TooltipOpts(is_show=False),  # 关闭提示框
        legend_opts=opts.LegendOpts(
            is_show=True, pos_left='left', pos_top='2', orient='vertical')
    )

    return geo


def flights_line_viz(merged_data):
    geo = Geo(
        init_opts=opts.InitOpts(
            theme='dark',
            bg_color='#000000',
            width='1980px',
            height='1080px'
        )
    )

    for idx, row in merged_data.iterrows():
        geo.add_coordinate(row["origin_station"],
                           row["lng_origin"], row["lat_origin"])
        geo.add_coordinate(row["destination_station"],
                           row["lng_destination"], row["lat_destination"])

    data_pair = []
    for idx, row in merged_data.iterrows():
        data_pair.append(
            (row["origin_station"], row["destination_station"])
        )

    geo.add_schema(
        maptype="china",
        is_roam=False,
        itemstyle_opts=opts.ItemStyleOpts(
            color="#000000", border_color="#1E90FF"
        ),
        emphasis_label_opts=opts.LabelOpts(is_show=False),
        emphasis_itemstyle_opts=opts.ItemStyleOpts(color="#323c48")
    )

    geo.add("火车线路图",
            data_pair,
            type_='lines',
            is_selected=True,
            symbol_size=2,
            is_large=True,
            large_threshold=1e6,
            progressive_threshold=100000,
            linestyle_opts=opts.LineStyleOpts(
                curve=0.2, opacity=0.03, color='#4682B4', width=0.3),
            effect_opts=opts.EffectOpts(symbol='pin', period=5, symbol_size=2, trail_length=0.5,
                                        color="#E1FFFF"),
            )

    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    geo.set_global_opts(
        title_opts=opts.TitleOpts(
            title="火车线路图", pos_top='3%', pos_left='center'),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        legend_opts=opts.LegendOpts(is_show=True, pos_left='left', pos_top='50%', orient='vertical',
                                    selected_mode='single')
    )

    return geo
