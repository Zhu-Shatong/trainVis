import pandas as pd

# 读取CSV文件
data = pd.read_csv('AccessInfo.csv', encoding='utf-8')

# 过滤掉评分为-1的数据
filtered_data = data[data['value'] != -1]

# 按评分从高到低排序
sorted_data = filtered_data.sort_values(by='value', ascending=False)

# 计算每个等级的数量
total_count = len(sorted_data)
group_count = total_count // 5

# 分成五个等级
rankings = {}
for i in range(5):
    start_index = i * group_count
    end_index = (i + 1) * group_count
    if i == 4:  # 处理最后一组，可能会多一些
        end_index = total_count
    group = sorted_data.iloc[start_index:end_index]
    rankings[f'等级{i+1}'] = group['station'].tolist()

# 添加评分为-1的数据到最后一个等级
rankings[f'等级5'] += data[data['value'] == -1]['station'].tolist()

# 创建一个新的DataFrame来保存结果
output_data = pd.DataFrame(columns=['等级', 'station'])
for rank, stations in rankings.items():
    for station in stations:
        output_data = pd.concat([output_data, pd.DataFrame(
            {'等级': [rank], 'station': [station]})], ignore_index=True)


# 保存结果到新的CSV文件
output_data.to_csv('AccessInfo_ranking.csv', index=False)
