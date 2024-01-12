from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import teamgamelogs

team = teams.find_teams_by_city('New Orleans')

pelicans_game_logs = teamgamelogs.TeamGameLogs(team[0]['id'])

# pelicans_game_logs.get_request()

# min_values = pelicans_game_logs.team_game_logs["MIN"]

print(pelicans_game_logs)