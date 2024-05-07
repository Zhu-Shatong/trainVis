import json
import os

import pandas as pd

# 对所有的比赛详细数据文件进行处理分析

def matchesToFolder():
    matcherFile = ['2', '11', '16', '37', '43', '49', '55', '72']
    for m in matcherFile:
        path = matches + '/' + m
        fileList = os.listdir(path)
        for f in fileList:
            df = pd.read_json(path + '/' + f)
            df.to_json('../数据资料/data/match/' + m + '_' + f)


def writeMatch():
    matchList = os.listdir(events)
    fileList = os.listdir(match)
    columnsList = ['match_id', 'competition', 'season',
                   'home_team', 'away_team', 'home_score', 'away_score']
    res_df = pd.DataFrame(columns=columnsList)
    for f in fileList:
        df = pd.read_json(match + '/' + f)
        # 用match_id找
        for i in range(len(df.values)):
            match_id = df['match_id'][0]
            if str(match_id) + '.json' in matchList:
                res_df.loc[len(res_df.index)] = df[columnsList].values[i]
    res_df.to_json('allMatch.json')


def writeCompetition():
    matchDf = pd.read_json('allMatch.json')
    competitionYearDict = {}
    yearTeamDict = {}
    for i in range(len(matchDf.values)):
        competitionName = matchDf['competition'][i]['competition_name']
        competitionSeason = matchDf['season'][i]['season_name']
        home_team = matchDf['home_team'][i]['home_team_name']
        away_team = matchDf['away_team'][i]['away_team_name']
        # 第一次有这个比赛
        if competitionName not in competitionYearDict:
            competitionYearDict[competitionName] = [competitionSeason]
            yearTeamDict[competitionName] = {competitionSeason: [home_team, away_team]}
        else:
            if competitionSeason not in competitionYearDict[competitionName]:
                competitionYearDict[competitionName].append(competitionSeason)
                yearTeamDict[competitionName][competitionSeason] = [home_team, away_team]
            if home_team not in yearTeamDict[competitionName][competitionSeason]:
                yearTeamDict[competitionName][competitionSeason].append(home_team)
            if away_team not in yearTeamDict[competitionName][competitionSeason]:
                yearTeamDict[competitionName][competitionSeason].append(away_team)
    competition_year_str = json.dumps(competitionYearDict)
    with open('competition_year.json', 'w', encoding='utf-8') as json_file:
        json_file.write(competition_year_str)
    year_team_str = json.dumps(yearTeamDict)
    with open('year_team.json', 'w', encoding='utf-8') as json_file:
        json_file.write(year_team_str)


def all_opponent(competition_name, season_name, team):
    matchDf = pd.read_json('allMatch.json')
    resList = []
    for i in range(len(matchDf)):
        if matchDf['competition'][i]['competition_name'] == competition_name and matchDf['season'][i][
            'season_name'] == season_name:
            if matchDf['home_team'][i]['home_team_name'] == team:
                resList.append(matchDf['away_team'][i]['away_team_name'])
            if matchDf['away_team'][i]['away_team_name'] == team:
                resList.append(matchDf['home_team'][i]['home_team_name'])
    return list(set(resList))


def get_match_info(team1, team2, competition_name, season_name):
    matchDf = pd.read_json('allMatch.json')
    for i in range(len(matchDf)):
        if matchDf['competition'][i]['competition_name'] == competition_name and matchDf['season'][i][
            'season_name'] == season_name:
            if matchDf['home_team'][i]['home_team_name'] == team1 and matchDf['away_team'][i][
                'away_team_name'] == team2:
                return matchDf.values[i]
            elif matchDf['home_team'][i]['home_team_name'] == team2 and matchDf['away_team'][i][
                'away_team_name'] == team1:
                return matchDf.values[i]


def translateCompetition():
    f = open('competition_year.json', 'r')
    competitionDict = json.load(f)
    EngCh = {'La Liga': '西甲', 'Champions League': '欧冠', 'Premier League': '英超(男)',
             "FA Women's Super League": '英超(女)'
        , 'FIFA World Cup': '世界杯(男)', "Women's World Cup": '世界杯(女)', 'NWSL': '美职联', 'UEFA Euro': '欧洲杯'}
    ChEng = {}
    for i in range(len(EngCh)):
        ChEng[EngCh.values()[i]] = EngCh.keys()[i]
    return ChEng, EngCh


def translateTeam():
    f = open('year_team.json', 'r')
    Dict = json.load(f)
    EngCh = {'Barcelona': '巴塞罗那', 'Las Palmas': '拉斯帕尔马斯', 'Eibar': '埃瓦尔', 'Real Betis': '皇家贝蒂斯',
             'Villarreal': '比利亚雷亚尔'
        , 'Real Madrid': '皇家马德里', 'Levante': '莱万特'}
    ChEng = {}
    for i in range(len(EngCh)):
        ChEng[EngCh.values()[i]] = EngCh.keys()[i]
    return ChEng, EngCh


# 先选比赛名称，然后选比赛年份，然后选比赛球队，然后选对手
events = '../数据资料/data/events'
lineups = '../数据资料/data/lineups'
matches = '../数据资料/data/matches'
match = '../数据资料/data/match'

