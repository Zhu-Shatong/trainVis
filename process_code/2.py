import csv
import requests
from time import sleep


def get_place_info(place_name, ak):
    url = "http://api.map.baidu.com/place/v2/suggestion"
    params = {
        "query": place_name+"站",
        "region": "全国",
        "city_limit": "true",
        "output": "json",
        "ak": ak
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == 0 and data["result"]:
        return data["result"][0]
    else:
        return None


def add_place_info_to_csv(input_file, output_file, api_key):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + \
            ['Province', 'Geographical Zone', 'City', 'District', 'Address']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            station_name = row['Station']
            place_info = get_place_info(station_name, api_key)

            if place_info:
                row['Province'] = place_info.get('province', '未知')
                row['Geographical Zone'] = get_geographical_zone(
                    row['Province'])
                row['City'] = place_info.get('city', '未知')
                row['District'] = place_info.get('district', '未知')
                row['Address'] = place_info.get('address', '未知')
            else:
                row['Province'] = '未知'
                row['Geographical Zone'] = '未知'
                row['City'] = '未知'
                row['District'] = '未知'
                row['Address'] = '未知'

            writer.writerow(row)
            print(row)
            # sleep(1)  # Add a short delay to avoid overloading the API


def get_geographical_zone(province):
    zones = {
        "华北": ["北京市", "天津市", "河北省", "山西省", "内蒙古自治区"],
        "东北": ["辽宁省", "吉林省", "黑龙江省"],
        "华东": ["上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省"],
        "华中": ["河南省", "湖北省", "湖南省"],
        "华南": ["广东省", "广西壮族自治区", "海南省"],
        "西南": ["重庆市", "四川省", "贵州省", "云南省", "西藏自治区"],
        "西北": ["陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区"]
    }
    for zone, provinces in zones.items():
        if province in provinces:
            return zone
    return "未知"


input_file = "data/final_merged_stations_geo_continuous_save.csv"
output_file = "final_merged_stations_with_place_info.csv"
api_key = "rRXOcoeW56ECqZuR89fWLHsXx3rWROmE"  # 请替换为你自己的百度地图API密钥

add_place_info_to_csv(input_file, output_file, api_key)
