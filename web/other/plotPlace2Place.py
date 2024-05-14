import matplotlib.pyplot as plt
import pandas as pd

from mplsoccer import Pitch

import plotly.express as px
import numpy as np


plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

# 绘制每个球队的进攻区域
def p2pMain():
    URL = 'https://fbref.com/en/share/LdLSY'
    df = pd.read_html(URL)[0]

    df = df[['Unnamed: 0_level_0', 'Touches']].copy()
    df.columns = df.columns.droplevel()  # drop the top-level of the multi-index
    df = df.drop(["Def Pen", "Att Pen", "Live"], axis = 1) # drop the def pen, att pen, live touches column

    touches_cols = ['Def 3rd', 'Mid 3rd', 'Att 3rd']
    df_total = pd.DataFrame(df[touches_cols].sum())
    df_total.columns = ['total']
    df_total = df_total.T
    df_total = df_total.divide(df_total.sum(axis=1), axis=0) * 100

    df[touches_cols] = df[touches_cols].divide(df[touches_cols].sum(axis=1), axis=0) * 100.
    df.sort_values(['Att 3rd', 'Def 3rd'], ascending=[True, False], inplace=True)


    pitch = Pitch(line_zorder=2, line_color='black', pad_top=20)


    bin_statistic = pitch.bin_statistic([0], [0], statistic='count', bins=(3, 1))

    GRID_HEIGHT = 0.8
    CBAR_WIDTH = 0.03
    fig, axs = pitch.grid(nrows=4, ncols=5, figheight=20,

                          grid_width=0.88, left=0.025,
                          endnote_height=0.03, endnote_space=0,
                          axis=False,
                          title_space=0.02, title_height=0.06, grid_height=GRID_HEIGHT)
    fig.set_facecolor('white')

    teams = df['Squad'].values
    vmin = df[touches_cols].min().min()
    vmax = df[touches_cols].max().max()
    for i, ax in enumerate(axs['pitch'].flat[:len(teams)]):

        ax.text(60, -10, teams[i],
                ha='center', va='center', fontsize=50,color='black')

    # 绘制进攻区域热力图
        bin_statistic['statistic'] = df.loc[df.Squad == teams[i], touches_cols].values
        heatmap = pitch.heatmap(bin_statistic, ax=ax, cmap='coolwarm', vmin=vmin, vmax=vmax)
        annotate = pitch.label_heatmap(bin_statistic, color='black', fontsize=50, ax=ax,
                                       str_format='{0:.0f}%', ha='center', va='center')


    if len(teams) == 18:
        for ax in axs['pitch'][-1, 3:]:
            ax.remove()

    # add cbar axes
    cbar_bottom = axs['pitch'][-1, 0].get_position().y0
    cbar_left = axs['pitch'][0, -1].get_position().x1 + 0.01
    ax_cbar = fig.add_axes((cbar_left, cbar_bottom, CBAR_WIDTH,
                            # take a little bit off the height because of padding
                            GRID_HEIGHT - 0.036))
    cbar = plt.colorbar(heatmap, cax=ax_cbar)
    for label in cbar.ax.get_yticklabels():
        label.set_fontsize(50)


    title = axs['title'].text(0.5, 0.5, '2022/23赛季 德甲各球队控球位置占比',
                              ha='center', va='center', fontsize=70,color='black')


    return fig

def minMax(x):
    minN=np.min(x)
    maxN=np.max(x)
    return (x-minN+5)/(maxN-minN)


def AxsScatter():
    name=['拜仁慕尼黑','多特蒙德','莱比锡红牛','柏林联合','弗莱堡','勒沃库森','法兰克福','沃尔夫斯堡','美因茨','门兴格拉德巴赫','科隆'
        ,'霍芬海姆','云达不来梅','波鸿','奥格斯堡','斯图加特','沙尔克04','柏林赫塔']
    score=[71,71,66,62,59,50,50,49,46,43,42,36,36,35,34,33,31,29]
    front=[27,24,22,23,24,20,21,21,22,21,18,20,19,21,22,21,20,21]
    mid=[43,46,48,38,44,49,46,45,48,44,44,43,46,42,37,40,41,44]
    df=pd.DataFrame({'队名':name,'积分':score,'前场控球率':front,'中场控球率':mid})

    fig=px.scatter(df,x='前场控球率',y='中场控球率',color='队名',size=minMax(score),hover_name=score)
    return fig

