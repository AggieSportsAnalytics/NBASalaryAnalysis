import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


class Player(object):
    def __init__(self, name, firstName, salary, age, points, assists, rebounds, steals, blocks, turnovers, fouls):

        self.name = name
        self.firstName = firstName
        self.salary = salary
        self.teamName = ""
        self.isSupermax = False
        self.ismax = False
        self.isMin = False
        self.age = age
        self.points = points
        self.assists = assists
        self.rebounds = rebounds
        self.steals = steals
        self.blocks = blocks
        self.turnovers = turnovers
        self.fouls = fouls


def process_team_data(team_name, averageCap):
    stats_file = f"Data/{team_name}PlayerStats.csv"
    salary_file = f"Data/{team_name}Salary.csv"
    standings_file = "NBAStandings.csv"

    stats_data = pd.read_csv(stats_file)
    salary_data = pd.read_csv(salary_file)
    standings_data = pd.read_csv(standings_file)

    # Merge datasets based on player names
    merged_data = pd.merge(salary_data, stats_data, on='Player', how='inner')

    # Save merged dataset to a new CSV file
    merged_data.to_csv(f"Data/{team_name}MergedData.csv", index=False)

    # Remove the dollar sign from the data to clean it up
    merged_data['2023-24'] = merged_data['2023-24'].replace('[\$,]', '', regex=True).astype(float)
    total_team_salary = merged_data['2023-24'].sum()

    #create a player object for each player in the csv
    players = []
    for index, row in merged_data.iterrows():
        parts = row['Player'].split(' ', 1)
        player = Player(row['Player'], parts[1], row['2023-24'], row['Age_x'], row['PTS'], row['AST'], row['TRB'], row['STL'], row['BLK'], row['TOV'], row['PF'])
        holder = checkForMaxMin(player, averageCap)
        if holder == 1:
            player.isSupermax = True
        elif holder == 0:
            player.ismax = True
        elif holder == -1:
            player.isMin = True
        player.teamName = team_name
        players.append(player)
    #print the total team salary
    
    return players

def checkForMaxMin(player, averageCap):
    if player.salary/averageCap >= 0.33: # is supermax
        return 1
    elif player.salary/averageCap >= 0.24: # is max
        return 0
    elif player.salary <= 1100001: # is min
        return -1
    else:
        return -2


teamsFinal = ['Blazers', 'Bucks', 'Bulls', 'Cavaliers', 'Celtics', 'Clippers', 'Grizzlies', 'Hawks', 'Heat', 'Hornets', 'Jazz', 'Kings', 'Knicks', 'Lakers', 'Magic', 'Mavericks', 'Nets', 'Nuggets', 'Pacers', 'Pelicans', 'Pistons', 'Raptors', 'Rockets', 'Spurs', 'Suns', 'Thunder', 'Wolves', 'Warriors', 'Wizards', 'Sixers']
players = []
#range values
averageCap = 135000000
for team in teamsFinal:
    holderForPlayers = process_team_data(team, averageCap)
    players.append(holderForPlayers)

supermax = []

for team in players:
    for player in team:
        if player.isSupermax:
            supermax.append(player)

supermax.sort(key=lambda x: x.salary, reverse=True)

for player in supermax:
    print(player.name)
    print(player.salary)

# make a two column bar chart of supermax players showing their salary and their points

# add one bar for each players salary
# add one bar for each players points

X_axis = np.arange(len(supermax)) 
fig = plt.figure(figsize = (20, 5))
  
plt.bar(X_axis, [x.points for x in supermax], 0.4, label = 'PPG', color = 'g') 



plt.xticks(X_axis, [x.firstName for x in supermax]) 
plt.xlabel("Players") 
plt.ylabel("PPG") 
plt.legend() 
plt.show() 
    

#for team in teams:
 #   process_team_data(team)
