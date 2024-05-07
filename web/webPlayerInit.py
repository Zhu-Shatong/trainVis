import json

import matplotlib.pyplot as plt
import streamlit as st
from mplsoccer import Sblocal

from file_Classify import all_opponent, get_match_info
from plotPlayerInit import passNetwork,tasson

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

if __name__ == '__main__':
    st.title('球员数据探索性可视化')
    tab1, tab2= st.tabs(["📈 球员间传球连接", "🤣 泰森多边形"])
    with open('competition_year.json', mode='r', encoding='utf-8') as json_file:
        competitionYear = json.load(json_file)
    with open('year_team.json', mode='r', encoding='utf-8') as json_file:
        yearTeam = json.load(json_file)
    competitionSelect = st.sidebar.selectbox('选择联赛', competitionYear.keys())
    yearSelect = st.sidebar.selectbox('选择赛季', competitionYear[competitionSelect])
    team1 = st.sidebar.selectbox('选择球队', yearTeam[competitionSelect][yearSelect])
    oppoList = all_opponent(competitionSelect, yearSelect, team1)
    team2 = st.sidebar.selectbox('选择对手', oppoList)
    match_info = get_match_info(team1, team2, competitionSelect, yearSelect)
    match_id = str(match_info[0])
    score1 = match_info[5] if match_info[3]['home_team_name'] == team1 else match_info[6]
    score2 = match_info[6] if match_info[3]['home_team_name'] == team1 else match_info[5]
    parser = Sblocal()
    df, related, freeze, tactics = parser.event('../数据资料/data/events/' + match_id + '.json')  # 解析文件
    allMinutes = int(df['minute'].values[-1])

    with tab1:
        tab1.subheader("球员平均位置和传球联系")
        agree = st.checkbox('查看对手数据', key=2)
        if agree:
            fig = passNetwork(team1, team2, match_id, score1, score2)
        else:
            fig = passNetwork(team2, team1, match_id, score2, score1)
        st.pyplot(fig)

    with tab2:
        tab2.subheader("泰森多边形")
        fig=tasson( match_id,team1, team2, score1, score2)
        st.pyplot(fig)
        
