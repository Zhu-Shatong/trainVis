
import pandas as pd
import requests
import json
import re
import time

# 读取CSV文件
df = pd.read_csv('final_merged_stations_geo_continuous_save.csv')

# 定义百度地图API的访问密钥
AK = 'WYiG4WZRn6S3uZAq0Vlxol9z6gJzZCR2'

# 定义一个函数用于调用百度地图API获取经纬度
def get_location(address):
    address = address +"站"
    url = f'http://api.map.baidu.com/geocoding/v3/?address={address}&output=json&ak={AK}&callback=showLocation'
    try:
        response = requests.get(url)
        results = json.loads(re.findall(r'\((.*?)\)', response.text)[0])
        return results['result']['location']
    except Exception as e:
        print(f"Error retrieving data for {address}: {e}")
        return None

# 遍历DataFrame中每一行
for index, row in df.iterrows():
    if pd.isna(row['lat']) or pd.isna(row['lng']):
        # 重试机制
        # 初始化重试计数器
        retry_count = 0
        while retry_count < 20:
            location = get_location(row['Station'])
            if location:
                # 更新DataFrame中的经纬度
                df.at[index, 'lat'] = location['lat']
                df.at[index, 'lng'] = location['lng']
                print(f"Updated {row['Station']} with location {location}")
                # 保存到CSV文件
                df.to_csv('final_merged_stations_geo_continuous_save.csv', index=False)
                break
            else:
                print(f"Retry getting location for {row['Station']}")
                time.sleep(1)  # 暂停1秒后重试，以避免频繁请求
                retry_count += 1
        if retry_count == 20:
            print(f"Failed to update {row['Station']} after 20 attempts.")

