from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster

#provides csv of all players of a certain team in the nba with important stats

#put team name here
team = teams.find_teams_by_city('New Orleans')
roster = commonteamroster.CommonTeamRoster(team[0]['id'])
df = roster.get_data_frames()[0]

df = df[["TeamID", "PLAYER", "POSITION", "AGE", "EXP", "PLAYER_ID"]]

df.to_csv('PelsAPI.csv', index=False)