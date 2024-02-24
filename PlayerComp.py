import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from bisect import bisect_left

class NBA(object):
    def __init__(self, super, max, min, t1, t2, t3, t4, t5, t6):
        self.Supermax = super
        self.Max = max
        self.Min = min
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.t5 = t5
        self.t6 = t6

class Player(object):
    def __init__(self, name, firstName, salary, teamName, age, points, assists, rebounds, steals, blocks, turnovers, fouls, games, fta, ftm, fga, fgm):
        self.name = name
        self.firstName = firstName
        self.salary = salary
        self.teamName = teamName
        self.isSupermax = False
        self.ismax = False
        self.isMin = False
        self.age = age
        self.PPG = points
        self.AST = assists
        self.REB = rebounds
        self.STL = steals
        self.BLK = blocks
        self.TO = turnovers
        self.fouls = fouls
        self.G = games
        self.over = False
        self.under = False
        self.normal = False
        self.tier = ""
        self.PER = (points + assists + rebounds + steals + blocks - (fta - ftm) - (fga - fgm) - turnovers)

class Team(object):
    def __init__(self, name, players):
        self.name = name
        self.players = players

def graph(arr, z, labelVal, f):
    X_axis = np.arange(len(arr)) 
    fig = plt.figure(figsize = (z, 5))
    plt.bar(X_axis, [getattr(x, labelVal) for x in arr], 0.4, label = labelVal, color = 'g')  
    plt.xticks(X_axis, [x.firstName for x in arr], fontsize = f) 
    plt.xlabel("Players") 
    plt.ylabel(labelVal) 
    plt.legend() 
    plt.show() 

def process_team_data(team_name, allPlayers, averageCap):
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
        if row['2023-24'] > 0 and row['G'] > 3:
            parts = row['Player'].split(' ', 1)
            player = Player(row['Player'], parts[1], row['2023-24'], team_name, row['Age_x'], row['PTS'], row['AST'], row['TRB'], row['STL'], row['BLK'], row['TOV'], row['PF'], row['G'], row['FTA'], row['FT'], row['FGA'], row['FG'])
            holder = checkForMaxMin(player, averageCap)
            if holder == 1:
                player.isSupermax = True
            elif holder == 0:
                player.ismax = True
            elif holder == -1:
                player.isMin = True
            players.append(player)
            allPlayers.append(player)
    team = Team(team_name, players)
    return team

def checkForMaxMin(player, averageCap):
    if player.salary/averageCap >= 0.33: # is supermax
        return 1
    elif player.salary/averageCap >= 0.23: # is max
        return 0
    elif player.salary <= 2400000.0: # is min
        return -1
    else:
        return -2
    
#function reviews the supermax players on each team
def reviewSuperMaxes(teamFinished, labelVal):
    superMax = []
    for team in teamFinished:
        for c in team.players:
            if c.isSupermax:
                superMax.append(c)

    superMax.sort(key=lambda x: x.salary, reverse=True)

    graph(superMax, 10, labelVal, 9)

def reviewMaxes(teamFinished, labelVal):
    max = []
    for team in teamFinished:
        for c in team.players:
            if c.ismax:
                max.append(c)

    max.sort(key=lambda x: x.salary, reverse=True)
    graph(max, 30, labelVal, 6)

def reviewMins(teamFinished, labelVal):
    min = []
    for team in teamFinished:
        for c in team.players:
            if c.isMin:
                min.append(c)

    min.sort(key=lambda x: x.salary, reverse=True)
    graph(min, 10, labelVal, 6)

def reviewPlayer(name, teamFinished, allPlayers, labelVal):
    temp = 0
    for i in range(len(allPlayers)):
        if allPlayers[i].name == name:
            temp = i
            break
    if allPlayers[temp].isSupermax:
            reviewSuperMaxes(teamFinished, labelVal)
            counter, expected = overUnderPlayer(allPlayers[temp], allPlayers, labelVal)

            if counter == 1:
                print(allPlayers[temp].name, "is overachieving.")
                print(allPlayers[temp].name, "is making $", round(allPlayers[temp].salary), "and is averaging ", allPlayers[temp].PER, "PER compared to the average of ", round(expected), "PER for his tier.")
            elif counter == -1:
                print(allPlayers[temp].name, "is underachieving.")
                print(allPlayers[temp].name, "is making $", round(allPlayers[temp].salary), "and is averaging ", allPlayers[temp].PER, "PER compared to the average of ", round(expected), "PER for his tier.")
            else:
                print(allPlayers[temp].name, "is performing as expected.")
                print(allPlayers[temp].name, "is making $", round(allPlayers[temp].salary), "and is averaging ", allPlayers[temp].PER, "PER compared to the average of ", round(expected), "PER for his tier.")

    else:
        holder = []
        #find the index of the player in the allPlayers array
        
        #find the players that are within 5% of the player's salary
        for i in range(temp-5, temp+5):
            if i >= 0 and i < len(allPlayers):
                holder.append(allPlayers[i])
        graph(holder, 10, labelVal, 9)
        counter, expected = overUnderPlayer(allPlayers[temp], allPlayers, labelVal)
        if counter == 1:
            print(allPlayers[temp].name, "is overachieving.")
            print(allPlayers[temp].name, "is making $", round(allPlayers[temp].salary), "and is averaging ", allPlayers[temp].PER, "PER compared to the average of ", round(expected), "PER for his tier.")
        elif counter == -1:
            print(allPlayers[temp].name, "is underachieving.")
            print(allPlayers[temp].name, "is making $", round(allPlayers[temp].salary), "and is averaging ", allPlayers[temp].PER, "PER compared to the average of ", round(expected), "PER for his tier.")
        else:
            print(allPlayers[temp].name, "is performing as expected.")
            print(allPlayers[temp].name, "is making $", round(allPlayers[temp].salary), "and is averaging ", allPlayers[temp].PER, "PER compared to the average of ", round(expected), "PER for his tier.")

    #check if player is over or under achieving
    print(allPlayers[temp].name, allPlayers[temp].teamName)

def segregatingContracts(teamFinished, allPlayers, labelVal):
    superAvg, maxAvg, minAvg = 0, 0, 0
    p1, p2, p3, p4, p5, p6 = 0, 0, 0, 0, 0, 0
    superCount, maxCount, minCount = 0, 0, 0
    c1, c2, c3, c4, c5, c6 = 0, 0, 0, 0, 0, 0
    for player in allPlayers:
        if player.isSupermax:
            superAvg += player.PER
            superCount += 1
        elif player.ismax:
            maxAvg += player.PER
            maxCount += 1
        elif player.isMin:
            minAvg += player.PER
            minCount += 1
        elif 31830356 > player.salary >= 25000000:
            p1 += player.PER
            c1 += 1
        elif 25000000 > player.salary >= 20000000:
            p2 += player.PER
            c2 += 1
        elif 20000000 > player.salary >= 15000000:
            p3 += player.PER
            c3 += 1
        elif 15000000 > player.salary >= 10000000:
            p4 += player.PER
            c4 += 1
        elif 10000000 > player.salary >= 5000000:
            p5 += player.PER
            c5 += 1
        elif 5000000 > player.salary:
            p6 += player.PER
            c6 += 1
    
    sdSuper, sdMax, sdMin, sd1, sd2, sd3, sd4, sd5, sd6 = standardDeviation(superAvg/superCount, maxAvg/maxCount, minAvg/minCount, p1/c1, p2/c2, p3/c3, p4/c4, p5/c5, p6/c6, superCount, maxCount, minCount, c1, c2, c3, c4, c5, c6, allPlayers, labelVal)
    nba = NBA(superAvg/superCount, maxAvg/maxCount, minAvg/minCount, p1/c1, p2/c2, p3/c3, p4/c4, p5/c5, p6/c6)
    return superAvg/superCount, maxAvg/maxCount, minAvg/minCount, p1/c1, p2/c2, p3/c3, p4/c4, p5/c5, p6/c6, sdSuper, sdMax, sdMin, sd1, sd2, sd3, sd4, sd5, sd6, nba
    #print("Supermax average: ", superAvg/superCount)
    #print("Max average: ", maxAvg/maxCount)
    #print("Min average: ", minAvg/minCount)
    #print("1st tier average: ", p1/c1)
    #print("2nd tier average: ", p2/c2)
    #print("3rd tier average: ", p3/c3)
    #print("4th tier average: ", p4/c4)
    #print("5th tier average: ", p5/c5)
    #print("6th tier average: ", p6/c6)

def standardDeviation(superAvg, maxAvg, minAvg, t1, t2, t3, t4, t5, t6, superCount, maxCount, minCount, c1, c2, c3, c4, c5, c6, allPlayers, labelVal):
    sdSuper, sdMax, sdMin, sd1, sd2, sd3, sd4, sd5, sd6 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    counterSuper, counterMax, counterMin, counter1, counter2, counter3, counter4, counter5, counter6 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    for player in allPlayers:
        if player.isSupermax:
            counterSuper = counterSuper + (player.PER - superAvg)**2
        elif player.ismax:
            counterMax = counterMax + (player.PER - maxAvg)**2
        elif player.isMin:
            counterMin = counterMin + (player.PER - minAvg)**2
        elif 31830356 > player.salary >= 25000000:
            counter1 = counter1 + (player.PER - t1)**2
        elif 25000000 > player.salary >= 20000000:
            counter2 = counter2 + (player.PER - t2)**2
        elif 20000000 > player.salary >= 15000000:
            counter3 = counter3 + (player.PER - t3)**2
        elif 15000000 > player.salary >= 10000000:
            counter4 = counter4 + (player.PER - t4)**2
        elif 10000000 > player.salary >= 5000000:
            counter5 = counter5 + (player.PER - t5)**2
        elif 5000000 > player.salary:
            counter6 = counter6 + (player.PER - t6)**2
    sdSuper = math.sqrt(counterSuper/superCount)
    sdMax = math.sqrt(counterMax/maxCount)
    sdMin = math.sqrt(counterMin/minCount)
    sd1 = math.sqrt(counter1/c1)
    sd2 = math.sqrt(counter2/c2)
    sd3 = math.sqrt(counter3/c3)
    sd4 = math.sqrt(counter4/c4)
    sd5 = math.sqrt(counter5/c5)
    sd6 = math.sqrt(counter6/c6)

    return sdSuper, sdMax, sdMin, sd1, sd2, sd3, sd4, sd5, sd6

def checkTier(player):
    if player.isSupermax:
        player.tier = "Supermax"
        return "Supermax"
    elif player.ismax:
        player.tier = "Max"
        return "Max"
    elif player.isMin:
        player.tier = "Min"
        return "Min"
    elif 31830356 > player.salary >= 25000000:
        player.tier = "t1"
        return "1st Tier"
    elif 25000000 > player.salary >= 20000000:
        player.tier = "t2"
        return "2nd Tier"
    elif 20000000 > player.salary >= 15000000:
        player.tier = "t3"
        return "3rd Tier"
    elif 15000000 > player.salary >= 10000000:
        player.tier = "t4"
        return "4th Tier"
    elif 10000000 > player.salary >= 5000000:
        player.tier = "t5"
        return "5th Tier"
    elif 5000000 > player.salary:
        player.tier = "t6"
        return "6th Tier"

def reviewTeam(teamName, teamFinished, labelVal):
    for team in teamFinished:
        if team.name == teamName:
            over, under, nba = overVsUnder(team, allPlayers, labelVal)
            graph(team.players, 10, labelVal, 9)
            for player in team.players:
                if player.over:
                    print(player.name, "is overachieving.")
                    print(player.name, "is making $",round(player.salary), "and is averaging ", player.PER, "PER compared to the average of ", round(getattr(nba, player.tier)), "PER for his tier.")
                elif player.under:
                    print(player.name, "is underachieving.")
                    print(player.name, "is making $",round(player.salary), "and is averaging ", player.PER, "PER compared to the average of ", round(getattr(nba, player.tier)), "PER for his tier.")

    print("The ", teamName, "have ", over, "overachieving player(s), ", under, "underachieving player(s).")

def overUnderPlayer (player, allPlayers, labelVal):
    superAvg, maxAvg, minAvg, t1, t2, t3, t4, t5, t6, sdSuper, sdMax, sdMin, sd1, sd2, sd3, sd4, sd5, sd6, nba = segregatingContracts(teamFinished, allPlayers, labelVal)
    tier = checkTier(player)
    if tier == "Supermax":
        if player.PER > superAvg + sdSuper:
            player.over = True
            return 1, round(getattr(nba, player.tier))
        if player.PER < superAvg - sdSuper:
            player.under = True
            return -1, round(getattr(nba, player.tier))
        else:
            return 0, round(getattr(nba, player.tier))
    elif tier == "Max":
        if player.PER > maxAvg + sdMax:
            player.over = True, round(getattr(nba, player.tier))
            return 1
        elif player.PER < maxAvg - sdMax:
            player.under = True, round(getattr(nba, player.tier))
            return -1
        else:
            return 0, round(getattr(nba, player.tier))
    elif tier == "Min":
        if player.PER > minAvg + sdMin:
            player.over = True
            return 1, round(getattr(nba, player.tier))
        else:
            return 0, round(getattr(nba, player.tier))
    elif tier == "1st Tier":
        if player.PER > t1 + sd1:
            player.over = True
            return 1, round(getattr(nba, player.tier))
        elif player.PER < t1 - sd1:
            player.under = True
            return -1, round(getattr(nba, player.tier))
        else:
            return 0, round(getattr(nba, player.tier))
    elif tier == "2nd Tier":
        if player.PER > t2 + sd2:
            player.over = True
            return 1, round(getattr(nba, player.tier))
        elif player.PER < t2 - sd2:
            player.under = True
            return -1, round(getattr(nba, player.tier))
        else:
            return 0
    elif tier == "3rd Tier":
        if player.PER > t3 + sd3:
            player.over = True
            return 1, round(getattr(nba, player.tier))
        elif player.PER < t3 - sd3:
            player.under = True
            return -1, round(getattr(nba, player.tier))
        else:
            return 0, round(getattr(nba, player.tier))
    elif tier == "4th Tier":
        if player.PER > t4 + sd4:
            player.over = True
            return 1, round(getattr(nba, player.tier))
        elif player.PER < t4 - sd4:
            player.under = True
            return -1, round(getattr(nba, player.tier))
        else:
            return 0, round(getattr(nba, player.tier))
    elif tier == "5th Tier":
        if player.PER > t5 + sd5:
            player.over = True
            return 1, round(getattr(nba, player.tier))
        elif player.PER < t5 - sd5:
            player.under = True
            return -1, round(getattr(nba, player.tier))
        else:
            return 0, round(getattr(nba, player.tier))
    elif tier == "6th Tier":
        if player.PER > t6 + sd6:
            player.over = True
            return 1, round(getattr(nba, player.tier))
        elif player.PER < t6 - sd6:
            player.under = True
            return -1, round(getattr(nba, player.tier))
        else:
            return 0, round(getattr(nba, player.tier))

def overVsUnder (team, allPlayers, labelVal):
    superAvg, maxAvg, minAvg, t1, t2, t3, t4, t5, t6, sdSuper, sdMax, sdMin, sd1, sd2, sd3, sd4, sd5, sd6, nba = segregatingContracts(teamFinished, allPlayers, labelVal)
    over, under, normal = 0, 0, 0
    tier = ""
    for player in team.players:
        tier = checkTier(player)
        if tier == "Supermax":
            if player.PER > superAvg + sdSuper:
                over += 1
                player.over = True
            if player.PER < superAvg - sdSuper:
                under += 1
                player.under = True
            else:
                normal += 1
        elif tier == "Max":
            if player.PER > maxAvg + sdMax:
                over += 1
                player.over = True
            elif player.PER < maxAvg - sdMax:
                under += 1
                player.under = True
            else:
                normal += 1
        elif tier == "Min":
            if player.PER > minAvg + sdMin:
                over += 1
                player.over = True
            else:
                normal += 1
        elif tier == "1st Tier":
            if player.PER > t1 + sd1:
                over += 1
                player.over = True
            elif player.PER < t1 - sd1:
                under += 1
                player.under = True
            else:
                normal += 1
        elif tier == "2nd Tier":
            if player.PER > t2 + sd2:
                over += 1
                player.over = True
            elif player.PER < t2 - sd2:
                under += 1
                player.under = True
            else:
                normal += 1
        elif tier == "3rd Tier":
            if player.PER > t3 + sd3:
                over += 1
                player.over = True
            elif player.PER < t3 - sd3:
                under += 1
                player.under = True
            else:
                normal += 1
        elif tier == "4th Tier":
            if player.PER > t4 + sd4:
                over += 1
                player.over = True
            elif player.PER < t4 - sd4:
                under += 1
                player.under = True
            else:
                normal += 1
        elif tier == "5th Tier":
            if player.PER > t5 + sd5:
                over += 1
                player.over = True
            elif player.PER < t5 - sd5:
                under += 1
                player.under = True
            else:
                normal += 1
        elif tier == "6th Tier":
            if player.PER > t6 + sd6:
                over += 1
                player.over = True
            elif player.PER < t6 - sd6:
                under += 1
                player.under = True
            else:
                normal += 1

    team.over = over
    team.under = under
    team.normal = normal
    return over, under, nba



teamsFinal = ['Blazers', 'Bucks', 'Bulls', 'Cavaliers', 'Celtics', 'Clippers', 'Grizzlies', 'Hawks', 'Heat', 'Hornets', 'Jazz', 'Kings', 'Knicks', 'Lakers', 'Magic', 'Mavericks', 'Nets', 'Nuggets', 'Pacers', 'Pelicans', 'Pistons', 'Raptors', 'Rockets', 'Spurs', 'Suns', 'Thunder', 'Wolves', 'Warriors', 'Wizards', 'Sixers']
teams = ['Celtics', 'Bucks']
# teamsfinished is an array of teams that have been processed and hold the team objects that hold players
teamFinished = []
allPlayers = []
labelVal = ""

for team in teamsFinal:
    teamFinished.append(process_team_data(team, allPlayers, 135000000))

allPlayers.sort(key=lambda x: x.salary, reverse=True)



val = input("What do you want to see?: ") 
labelVal = input("What stat do you want to use?: ")
segregatingContracts(teamFinished, allPlayers, labelVal)
if val == "super":
    reviewSuperMaxes(teamFinished, labelVal)
elif val == "max":
    reviewMaxes(teamFinished, labelVal)
elif val in teamsFinal:
    reviewTeam(val, teamFinished, labelVal) # needs to be completed
else:
    for player in allPlayers:
        if player.name == val:
            reviewPlayer(val, teamFinished, allPlayers, labelVal)
            break
    else:
        print("Player not found.")