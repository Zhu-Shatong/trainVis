import matplotlib.pyplot as plt
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号


def rankPlot():
    name = ["中国","卡塔尔","塔吉克斯坦","黎巴嫩"]
    score=[1299,1407,1195,1192]
    price=[1134,1588,712.5,741]
    df=pd.DataFrame({'队名':name,'积分':score,'身价':price})
    fig=px.bar(df,x="队名",y=["积分","身价"], barmode='group')
    return fig

def winRatePlot():
    # 假设 df 是你的 DataFrame
    name = ["中国","卡塔尔","塔吉克斯坦","黎巴嫩"]
    win=[0.385,0.445,0.3085,0.3392]
    draw=[0.236,0.206,0.288,0.27]
    loss = [0.376,0.348,0.394,0.404]
    df=pd.DataFrame({'队名':name,'胜率':win,'平率':draw,"负率":loss})
    fig = make_subplots(rows=2, cols=2,
                        specs=[[{'type':'domain'}, {'type':'domain'}],[{'type':'domain'}, {'type':'domain'}]])
    colors =  ['red', 'blue', 'green']
    for i in range(len(df)):
        team_name = df.loc[i, '队名']
        win_rate = df.loc[i, '胜率']
        draw_rate = df.loc[i, '平率']
        lose_rate = df.loc[i, '负率']
        labels = ['胜利', '平局', '失败']
        values = [win_rate, draw_rate, lose_rate]
        pie_chart = go.Figure(go.Pie(labels=labels, values=values, title=team_name,hole=0.4,marker_colors=colors))
        fig.add_trace(pie_chart.data[0], row=(i//2)+1, col=(i % 2)+1)

    fig.update_layout(title_text="球队胜平负率对比")
    return fig

def statsPlot():
    name = ["中国","卡塔尔","塔吉克斯坦","黎巴嫩"]
    shot=[6.91,8.2,7.53,7.707]
    hold=[0.3366,0.3559,0.3085,0.3392]
    yellow = [1.43,1.56,1.86,1.69]
    df=pd.DataFrame({'队名':name,'射门':shot,'控球率':hold,"黄牌":yellow})
    
    fig=px.scatter(df,x='射门',y='控球率',color='队名',size=[(y-1.3) for y in yellow],hover_name=yellow, color_discrete_sequence=['red',"yellow","grey","green"]) 
    return fig