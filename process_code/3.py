import json
import csv

# 读取JSON文件
with open('static/data/AccessInfo.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 写入CSV文件
with open('AccessInfo.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # 写入表头
    writer.writerow(['station', 'value'])

    # 写入数据
    for station, value in data.items():
        writer.writerow([station, value])
