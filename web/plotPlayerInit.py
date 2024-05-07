import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba
from mplsoccer import Pitch, Sblocal

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

# 绘制传球网络
def passNetwork(TEAM, OPPONENT, match_id, score1, score2):
    parser = Sblocal()

    events, related, freeze, players = parser.event('../数据资料/data/events/' + match_id + '.json')

    events.loc[events.tactics_formation.notnull(), 'tactics_id'] = events.loc[
        events.tactics_formation.notnull(), 'id']
    events[['tactics_id', 'tactics_formation']] = events.groupby('team_name')[[
        'tactics_id', 'tactics_formation']].ffill()

    formation_dict = {1: 'GK', 2: 'RB', 3: 'RCB', 4: 'CB', 5: 'LCB', 6: 'LB', 7: 'RWB',
                      8: 'LWB', 9: 'RDM', 10: 'CDM', 11: 'LDM', 12: 'RM', 13: 'RCM',
                      14: 'CM', 15: 'LCM', 16: 'LM', 17: 'RW', 18: 'RAM', 19: 'CAM',
                      20: 'LAM', 21: 'LW', 22: 'RCF', 23: 'ST', 24: 'LCF', 25: 'SS'}
    players['position_abbreviation'] = players.position_id.map(formation_dict)
    # 考虑换人
    sub = events.loc[events.type_name == 'Substitution',
    ['tactics_id', 'player_id', 'substitution_replacement_id',
     'substitution_replacement_name']]
    players_sub = players.merge(sub.rename({'tactics_id': 'id'}, axis='columns'),
                                on=['id', 'player_id'], how='inner', validate='1:1')
    players_sub = (players_sub[['id', 'substitution_replacement_id', 'position_abbreviation']]
                   .rename({'substitution_replacement_id': 'player_id'}, axis='columns'))
    players = pd.concat([players, players_sub])
    players.rename({'id': 'tactics_id'}, axis='columns', inplace=True)
    players = players[['tactics_id', 'player_id', 'position_abbreviation']]
    # 比赛中的事件
    events = events.merge(players, on=['tactics_id', 'player_id'], how='left', validate='m:1')
    events = events.merge(players.rename({'player_id': 'pass_recipient_id'},
                                         axis='columns'), on=['tactics_id', 'pass_recipient_id'],
                          how='left', validate='m:1', suffixes=['', '_receipt'])

    events.groupby('team_name').tactics_formation.unique()
    # 选出传球事件的数据
    pass_cols = ['id', 'position_abbreviation', 'position_abbreviation_receipt']
    passes_formation = events.loc[(events.team_name == TEAM) & (events.type_name == 'Pass') &
                                  (events.position_abbreviation_receipt.notnull()), pass_cols].copy()
    location_cols = ['position_abbreviation', 'x', 'y']
    location_formation = events.loc[(events.team_name == TEAM) &
                                    (events.type_name.isin(['Pass', 'Ball Receipt'])), location_cols].copy()

    # 对每个球员的传球事件进行平均
    average_locs_and_count = (location_formation.groupby('position_abbreviation')
                              .agg({'x': ['mean'], 'y': ['mean', 'count']}))
    average_locs_and_count.columns = ['x', 'y', 'count']

    passes_formation['pos_max'] = (passes_formation[['position_abbreviation',
                                                     'position_abbreviation_receipt']]
                                   .max(axis='columns'))
    passes_formation['pos_min'] = (passes_formation[['position_abbreviation',
                                                     'position_abbreviation_receipt']]
                                   .min(axis='columns'))
    passes_between = passes_formation.groupby(['pos_min', 'pos_max']).id.count().reset_index()
    passes_between.rename({'id': 'pass_count'}, axis='columns', inplace=True)

    passes_between = passes_between.merge(average_locs_and_count, left_on='pos_min', right_index=True)
    passes_between = passes_between.merge(average_locs_and_count, left_on='pos_max', right_index=True,
                                          suffixes=['', '_end'])
    # 进行绘制
    MAX_LINE_WIDTH = 18
    MAX_MARKER_SIZE = 3000
    passes_between['width'] = (passes_between.pass_count / passes_between.pass_count.max() *
                               MAX_LINE_WIDTH)
    average_locs_and_count['marker_size'] = (average_locs_and_count['count']
                                             / average_locs_and_count['count'].max() * MAX_MARKER_SIZE)

    MIN_TRANSPARENCY = 0.3
    color = np.array(to_rgba('white'))
    color = np.tile(color, (len(passes_between), 1))
    c_transparency = passes_between.pass_count / passes_between.pass_count.max()
    c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
    color[:, 3] = c_transparency

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')

    fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0,
                          axis=False,
                          title_space=0, grid_height=0.82, endnote_height=0.05)
    fig.set_facecolor("#22312b")
    pass_lines = pitch.lines(passes_between.x, passes_between.y,
                             passes_between.x_end, passes_between.y_end, lw=passes_between.width,
                             color=color, zorder=1, ax=axs['pitch'])
    pass_nodes = pitch.scatter(average_locs_and_count.x, average_locs_and_count.y,
                               s=average_locs_and_count.marker_size,
                               color='red', edgecolors='black', linewidth=1, alpha=1, ax=axs['pitch'])
    for index, row in average_locs_and_count.iterrows():
        pitch.annotate(row.name, xy=(row.x, row.y), c='white', va='center',
                       ha='center', size=16, weight='bold', ax=axs['pitch'])

    TITLE_TEXT = f'{TEAM} vs {OPPONENT}\n {score1} : {score2} '
    axs['title'].text(0.5, 0.7, TITLE_TEXT, color='#c7d5cc',
                      va='center', ha='center', fontsize=30)

    return fig


def getPosition(match_id, team1):
    parser = Sblocal()
    # 读取和分析数据
    events, related, freeze, players = parser.event('../数据资料/data/events/' + match_id + '.json')

    events.loc[events.tactics_formation.notnull(), 'tactics_id'] = events.loc[
        events.tactics_formation.notnull(), 'id']
    events[['tactics_id', 'tactics_formation']] = events.groupby('team_name')[[
        'tactics_id', 'tactics_formation']].ffill()
    # 位置编号
    formation_dict = {1: 'GK', 2: 'RB', 3: 'RCB', 4: 'CB', 5: 'LCB', 6: 'LB', 7: 'RWB',
                      8: 'LWB', 9: 'RDM', 10: 'CDM', 11: 'LDM', 12: 'RM', 13: 'RCM',
                      14: 'CM', 15: 'LCM', 16: 'LM', 17: 'RW', 18: 'RAM', 19: 'CAM',
                      20: 'LAM', 21: 'LW', 22: 'RCF', 23: 'ST', 24: 'LCF', 25: 'SS'}
    players['position_abbreviation'] = players.position_id.map(formation_dict)
    # 考虑换人
    sub = events.loc[events.type_name == 'Substitution',
    ['tactics_id', 'player_id', 'substitution_replacement_id',
     'substitution_replacement_name']]
    players_sub = players.merge(sub.rename({'tactics_id': 'id'}, axis='columns'),
                                on=['id', 'player_id'], how='inner', validate='1:1')
    players_sub = (players_sub[['id', 'substitution_replacement_id', 'position_abbreviation']]
                   .rename({'substitution_replacement_id': 'player_id'}, axis='columns'))
    players = pd.concat([players, players_sub])
    players.rename({'id': 'tactics_id'}, axis='columns', inplace=True)
    players = players[['tactics_id', 'player_id', 'position_abbreviation']]
    # 选取传球事件
    events = events.merge(players, on=['tactics_id', 'player_id'], how='left', validate='m:1')
    events = events.merge(players.rename({'player_id': 'pass_recipient_id'},
                                         axis='columns'), on=['tactics_id', 'pass_recipient_id'],
                          how='left', validate='m:1', suffixes=['', '_receipt'])

    events.groupby('team_name').tactics_formation.unique()

    pass_cols = ['id', 'position_abbreviation', 'position_abbreviation_receipt']
    passes_formation = events.loc[(events.team_name == team1) & (events.type_name == 'Pass') &
                                  (events.position_abbreviation_receipt.notnull()), pass_cols].copy()
    location_cols = ['position_abbreviation', 'x', 'y']
    location_formation = events.loc[(events.team_name == team1) &
                                    (events.type_name.isin(['Pass', 'Ball Receipt'])), location_cols].copy()

    average_locs_and_count = (location_formation.groupby('position_abbreviation')
                              .agg({'x': ['mean'], 'y': ['mean', 'count']}))
    average_locs_and_count.columns = ['x', 'y', 'count']
    return average_locs_and_count

# 绘制泰森多边形
def tasson(match_id, team1name, team2name, score1, score2):
    team1LocsCount = getPosition(match_id, team1name)
    team2LocsCount = getPosition(match_id, team2name)
    team1Locs = team1LocsCount.iloc[:, 0:2]
    team2Locs = team2LocsCount.iloc[:, 0:2]

    visible_area = np.array([[0, 0], [120, 0], [120, 80], [0, 80], [0, 0]])
    # 获取每个球员的位置
    p = Pitch(pitch_type='statsbomb')
    fig, ax = p.draw(figsize=(12, 8))
    allx = []
    ally = []
    teamMate = []
    for i in range(len(team1Locs)):
        allx.append(team1Locs['x'][i])
        ally.append(team1Locs['y'][i])
        teamMate.append(True)
    for i in range(len(team2Locs)):
        team2Locs['x'][i] = 120 - team2Locs['x'][i]
        team2Locs['y'][i] = team2Locs['y'][i]
        allx.append(team2Locs['x'][i])
        ally.append(team2Locs['y'][i])
        teamMate.append(False)
    df = pd.DataFrame({'x': allx, 'y': ally, 'teammate': teamMate})
    df.sort_values(by='x')
    team1, team2 = p.voronoi(df['x'], df['y'], df['teammate'])
    # 绘制多边形
    t1 = p.polygon(team1, ax=ax, fc='orange', ec='white', lw=3, alpha=0.4)
    t2 = p.polygon(team2, ax=ax, fc='dodgerblue', ec='white', lw=3, alpha=0.4)

    sc1 = p.scatter(team1Locs['x'], team1Locs['y'], c='orange', s=80, ec='k', ax=ax)
    sc2 = p.scatter(team2Locs['x'], team2Locs['y'], c='dodgerblue', s=80, ec='k', ax=ax)

    visible = p.polygon([visible_area], color='None', ec='k', linestyle='--', lw=2, ax=ax)

    for p1 in t1:
        p1.set_clip_path(visible[0])
    for p2 in t2:
        p2.set_clip_path(visible[0])

    fig.text(0.09, 0.95, team1name + ' vs ' + team2name + '\n ' + str(score1) + ':' + str(score2), size=29,
             color="#222222")
    txt1 = ax.text(x=15, y=70, s=team1name, color='orange',
                   ha='center', va='center', fontsize=30)
    txt2 = ax.text(x=105, y=70, s=team2name, color='dodgerblue',
                   ha='center', va='center', fontsize=30)
    return fig


tasson('3788741', 'Italy', 'Turkey', 2, 0)

