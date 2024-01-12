from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster

# Find players by full name.
#print(players.find_players_by_full_name('james'))

# Find players by first name.
holder = players.find_players_by_first_name('lebron')
holder.append(players.find_players_by_last_name('durant'))

#print(holder[0]['id'])

#career = playercareerstats.PlayerCareerStats(holder[0]['id']) 

team = teams.find_teams_by_city('New Orleans')
roster = commonteamroster.CommonTeamRoster(team[0]['id'])
df = roster.get_data_frames()[0]

df.to_csv('PelsAPI.csv', index=False)
# Find players by last name.