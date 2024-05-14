import json

import matplotlib.pyplot as plt
import streamlit as st
from mplsoccer import Sblocal

from web.other.file_Classify import all_opponent, get_match_info
from web.other.plotTeamInit import arrowsPlotMain, passFlow, shotScatter, rankChange

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

if __name__ == '__main__':
    st.title('球队数据探索性可视化')
    tab1, tab3, tab4,  tab5 = st.tabs(
        [ "📈 传球向量图", "🎅 传球热力向量图",  '🐣 射门多图联合可视化',
         "🐾 球队排名可视化"])
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
    df, related, freeze, tactics = parser.event('../数据资料/data/events/' + match_id + '.json')
    allMinutes = int(df['minute'].values[-1])

    with tab1:
        tab1.subheader("传球向量图")
        values = st.slider('选择时间区间', 0, allMinutes, (0, allMinutes), key=1)
        agree = st.checkbox('查看对手数据', key=2)
        if agree:
            fig = arrowsPlotMain(df, team2, team1, values[0], values[1], score2, score1)
        else:
            fig = arrowsPlotMain(df, team1, team2, values[0], values[1], score1, score2)
        st.pyplot(fig)

    with tab3:
        tab3.subheader("传球热力向量图")
        values = st.slider('选择时间区间', 0, allMinutes, (0, allMinutes), key=3)
        agree = st.checkbox('查看对手数据', key=4)
        if agree:
            fig = passFlow(df, team2, team1, values[0], values[1], score2, score1)
        else:
            fig = passFlow(df, team1, team2, values[0], values[1], score1, score2)
        st.pyplot(fig)

    with tab4:
        tab4.subheader("射门可视化")
        values = st.slider('选择时间区间', 0, allMinutes, (0, allMinutes), key=7)
        agree = st.checkbox('查看对手数据', key=8)
        if agree:
            fig = shotScatter(df, team2, team1, values[0], values[1], score2, score1)
        else:
            fig = shotScatter(df, team1, team2, values[0], values[1], score1, score2)
        st.pyplot(fig)

    with tab5:
        tab5.subheader("英超19/20赛季排名可视化")
        fileName = 'epl.json'
        with open(fileName, 'r', encoding='utf-8') as f:
            season_dict = json.load(f)
        teamList = st.multiselect('选择球队：', list(season_dict.keys()), [])
        fig = rankChange(season_dict, teamList)
        st.pyplot(fig)


