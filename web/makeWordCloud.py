import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

font = r'C:\Windows\Fonts\simhei.ttf'

# 读取 CSV 文件
df = pd.read_csv('data/access_value_info.csv')

# 创建词云
wordcloud = WordCloud(width=1485, height=810, background_color='white', font_path=font).generate_from_frequencies(
    dict(zip(df['station'], df['value'])))

# 显示词云

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
