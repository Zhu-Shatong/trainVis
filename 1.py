from math import radians, sin, cos, sqrt, atan2
import pandas as pd
import numpy as np


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Earth radius in kilometers. Use 3956 for miles
    return distance


# 读取数据
sh_price_info = pd.read_csv("data/sh_price_info.csv")
stations_geo = pd.read_csv("data/final_merged_stations_geo_continuous_save.csv")

# 合并车站经纬度信息到出发站
sh_price_info = pd.merge(sh_price_info, stations_geo,
                         left_on='departure_station_code', right_on='Code', how='left')
sh_price_info.rename(
    columns={'lng': 'dep_lng', 'lat': 'dep_lat'}, inplace=True)
sh_price_info.drop(['Station', 'Code', 'In station_base', 'In output', 'Shared by both',
                   'shared_by_all_three', 'in_sh_price_info'], axis=1, inplace=True)

# 合并车站经纬度信息到到达站
sh_price_info = pd.merge(sh_price_info, stations_geo,
                         left_on='arrival_station_code', right_on='Code', how='left')
sh_price_info.rename(
    columns={'lng': 'arr_lng', 'lat': 'arr_lat'}, inplace=True)
sh_price_info.drop(['Station', 'Code', 'In station_base', 'In output', 'Shared by both',
                   'shared_by_all_three', 'in_sh_price_info'], axis=1, inplace=True)

# 计算欧氏距离
sh_price_info['distance_km'] = sh_price_info.apply(lambda row: haversine(
    row['dep_lat'], row['dep_lng'], row['arr_lat'], row['arr_lng']), axis=1)

# 保存结果
sh_price_info.to_csv("sh_price_info_with_distance.csv", index=False)
