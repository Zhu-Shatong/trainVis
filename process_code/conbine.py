import pandas as pd

# 读取两个 CSV 文件
df_access_ranking = pd.read_csv("data/AccessInfo_ranking.csv")
df_access = pd.read_csv("data/AccessInfo.csv")

# 合并两个 DataFrame，根据 station 进行内连接
merged_df = pd.merge(df_access_ranking, df_access, on="station", how="inner")

# 输出合并后的 DataFrame 到 CSV 文件
merged_df.to_csv("merged_access_info.csv", index=False)
