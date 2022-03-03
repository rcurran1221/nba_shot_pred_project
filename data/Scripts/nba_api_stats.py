# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import pandas as pd 
from statsnba import Game, Api

from nba_api.stats.endpoints import playbyplay
from nba_api.stats.endpoints import commonplayerinfo

#0021900016


df = playbyplay.PlayByPlay("0021900016").get_data_frames()[0]


from nba_api.stats.static import teams

nba_teams = teams.get_teams()

os.chdir("/Users/adam/Documents/GT Masters/CSE 6242/project")
df = pd.read_csv("shot_logs.csv")
player_ids = set(df['player_id'].astype(str))



j = 0
for i in player_ids: 
    print(j)
    if j == 0: 
        player_info = commonplayerinfo.CommonPlayerInfo(i).get_data_frames()[0][['HEIGHT', 'WEIGHT']]
        player_info['player_id'] = i
    else: 
        player_info1 = commonplayerinfo.CommonPlayerInfo(i).get_data_frames()[0][['HEIGHT', 'WEIGHT']]
        player_info1['player_id'] = i
        player_info = pd.concat([player_info, player_info1], axis = 0)
 
    j += 1

##### HEIGHT ######

#### WEIGHT ####### 





# Select the dictionary for the Pacers, which contains their team ID
pacers = [team for team in nba_teams if team['abbreviation'] == 'IND'][0]
pacers_id = pacers['id']
print(f'pacers_id: {pacers_id}')


from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType

gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=pacers_id,
                            season_nullable=Season.default,
                            season_type_nullable=SeasonType.regular)  

games_dict = gamefinder.get_normalized_dict()
games = games_dict['LeagueGameFinderResults']
game = games[0]
game_id = game['GAME_ID']
game_matchup = game['MATCHUP']


df = df.sort_values('EVENTNUM')