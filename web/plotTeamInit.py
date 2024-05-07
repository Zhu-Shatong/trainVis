import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch, VerticalPitch, Bumpy

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

# 绘制传球矢量图
def arrowsPlotMain(df, team1, team2, start, end, score1, score2):
    mask_team1 = (df.type_name == 'Pass') & (df.team_name == team1) & (df.minute >= start) & (df.minute <= end)
    df_pass = df.loc[mask_team1, ['x', 'y', 'end_x', 'end_y', 'outcome_name']]
    mask_complete = df_pass.outcome_name.isnull()

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, axs = pitch.grid(endnote_height=0.03, endnote_space=0, figheight=12,
                          title_height=0.06, title_space=0, grid_height=0.86,
                          axis=False)
    fig.set_facecolor('#22312b')


    pitch.arrows(df_pass[mask_complete].x, df_pass[mask_complete].y,
                 df_pass[mask_complete].end_x, df_pass[mask_complete].end_y, width=2, headwidth=10,
                 headlength=10, color='#ad993c', ax=axs['pitch'], label='成功传球')


    pitch.arrows(df_pass[~mask_complete].x, df_pass[~mask_complete].y,
                 df_pass[~mask_complete].end_x, df_pass[~mask_complete].end_y, width=2,
                 headwidth=6, headlength=5, headaxislength=12,
                 color='#ba4f45', ax=axs['pitch'], label='失败传球')


    legend = axs['pitch'].legend(facecolor='#22312b', handlelength=5, loc='best')
    for text in legend.get_texts():
        text.set_fontsize(15)
        plt.setp(text, color='w')

    axs['title'].text(0.5, 0.5, f'{team1} vs {team2}\n' + str(score1) + ':' + str(score2) + '\n传球向量图',
                      color='#dee6ea',
                      va='center', ha='center', fontsize=25)

    return fig

# 绘制传球热力图
def passFlow(df, team1, team2, start, end, score1, score2):
    mask_team1 = (df.type_name == 'Pass') & (df.team_name == team1) & (df.minute >= start) & (df.minute <= end)

    df_pass = df.loc[mask_team1, ['x', 'y', 'end_x', 'end_y', 'outcome_name']]
    mask_complete = df_pass.outcome_name.isnull()

    pitch = Pitch(pitch_type='statsbomb', line_zorder=2, line_color='#c7d5cc', pitch_color='#22312b')
    bins = (6, 4)

    pitch = Pitch(pitch_type='statsbomb', pad_bottom=1, pad_top=1,
                  pad_left=1, pad_right=1,
                  line_zorder=2, line_color='#c7d5cc', pitch_color='#22312b')
    fig, axs = pitch.grid(figheight=8, endnote_height=0.03, endnote_space=0,
                          title_height=0.1, title_space=0, grid_height=0.82,
                          axis=False)
    fig.set_facecolor('#22312b')

    bs_heatmap = pitch.bin_statistic(df_pass.x, df_pass.y, statistic='count', bins=bins)
    hm = pitch.heatmap(bs_heatmap, ax=axs['pitch'], cmap='Reds')
    fm = pitch.flow(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y,
                    color='black', arrow_type='same',
                    arrow_length=5, bins=bins, ax=axs['pitch'])

    axs['title'].text(0.5, 0.5, f'{team1} vs {team2}\n' + str(score1) + ':' + str(score2) + '\n传球热力图',
                      fontsize=20, va='center', ha='center',color='white')
    return fig

# 绘制射门散点图
def shotScatter(df, team1, team2, start, end, score1, score2):

    df_shots_team1 = df[
        (df.type_name == 'Shot') & (df.team_name == team1) & (df.minute >= start) & (df.minute <= end)].copy()


    df_goals_team1 = df_shots_team1[df_shots_team1.outcome_name == 'Goal'].copy()
    df_non_goal_shots_team1 = df_shots_team1[df_shots_team1.outcome_name != 'Goal'].copy()

    pitch = VerticalPitch(pad_bottom=0.5,  # pitch extends slightly below halfway line
                          half=True,  # half of a pitch
                          goal_type='box',
                          goal_alpha=0.8)  # control the goal transparency

    fig, ax = pitch.draw(figsize=(12, 10))


    sc1 = pitch.scatter(df_non_goal_shots_team1.x, df_non_goal_shots_team1.y,
                        # size varies between 100 and 1900 (points squared)
                        s=(df_non_goal_shots_team1.shot_statsbomb_xg * 1900) + 100,
                        edgecolors='#b94b75',  # give the markers a charcoal border
                        c='None',
                        hatch='///',
                        marker='o',
                        ax=ax)

    sc2 = pitch.scatter(df_goals_team1.x, df_goals_team1.y,
                        # size varies between 100 and 1900 (points squared)
                        s=(df_goals_team1.shot_statsbomb_xg * 1900) + 100,
                        edgecolors='#b94b75',
                        linewidth=0.6,
                        c='white',
                        marker='football',
                        ax=ax)

    txt = ax.text(x=40, y=80, s=f'{team1} vs {team2}\n' + str(score1) + ':' + str(score2) + '\n射门可视化',
                  size=25,
                  color=pitch.line_color,
                  va='center', ha='center')

    return fig

# 绘制排名变化图
def rankChange(season_dict, teamList):

    match_day = ["Week " + str(num) for num in range(1, 39)]
    color_List = ["crimson", "skyblue", "gold", 'green', 'black', 'white']
    color_Chinese = ['红色', '蓝色', '金色', '绿色', '黑色', '白色']
    highlight_dict = {}
    SUBTITLE = ""
    for i in range(len(teamList)):
        highlight_dict[teamList[i]] = color_List[i % 6]
        SUBTITLE += teamList[i] + "——" + color_Chinese[i % 6] + ' '

    bumpy = Bumpy(
        background_color="#F6F6F6", scatter_color="#808080",
        label_color="#000000", line_color="#C0C0C0",
        rotate_xticks=90,  # rotate x-ticks by 90 degrees
        ticklabel_size=17, label_size=30,  # ticklable and label font-size
        scatter_points='D',  # other markers
        scatter_primary='o',  # marker to be used for teams
        scatter_size=150,  # size of the marker
        show_right=True,  # show position on the rightside
        plot_labels=True,  # plot the labels
        alignment_yvalue=0.1,  # y label alignment
        alignment_xvalue=0.065  # x label alignment
    )


    fig, ax = bumpy.plot(
        x_list=match_day,  # match-day or match-week
        y_list=np.linspace(1, 20, 20).astype(int),  # position value from 1 to 20
        values=season_dict,  # values having positions for each team
        secondary_alpha=0.2,  # alpha value for non-shaded lines/markers
        highlight_dict=highlight_dict,  # team to be highlighted with their colors
        figsize=(20, 16),  # size of the figure
        x_label='轮次', y_label='排名',  # label name
        ylim=(-0.1, 23),  # y-axis limit
        lw=2.5,  # linewidth of the connecting lines
    )


    TITLE = "英超19/20赛季排名变化图"

    fig.text(0.09, 0.95, TITLE + '\n' + SUBTITLE, size=29, color="#222222")


    plt.tight_layout(pad=0.5)
    return fig


