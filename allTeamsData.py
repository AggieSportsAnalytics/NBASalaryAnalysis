from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

def process_team_data(team_name):
    
    
    
    
    salary_file = f"{team_name}Salary.csv"
    roster_file = f"{team_name}Roster.csv"
    NBAstandings_file = "NBAStandings.csv"

    Salary = pd.read_csv(salary_file)
    Roster = pd.read_csv(roster_file)
    Standings = pd.read_csv(NBAstandings_file)

    if 'Player' in Salary.columns and 'Player' in Roster.columns:
        merged_data = pd.merge(Roster, Salary, on='Player', how='inner')
    merged_data.to_csv(f"{team_name}MergedData.csv", index=False)

    merged_data['Salary'] = merged_data['Salary'].replace('[\$,]', '', regex=True).astype(int)

    Salary = merged_data[['Player', 'Pos', 'Salary']].dropna()
    total_salary = Salary['Salary'].sum()

    g = Salary.loc[Salary['Pos'].isin(['PG', 'SG']), 'Salary'].sum()
    f = Salary.loc[Salary['Pos'].isin(['SF', 'PF']), 'Salary'].sum()
    c = Salary.loc[Salary['Pos'] == 'C', 'Salary'].sum()

    PosVal = {"Guard": g, "Forward": f, "Center": c}

    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.2f}%\n(${v:,})'.format(p=pct, v=val)

        return my_format


    Standings['Team'] = Standings['Team'].str.split().str[-1]
    standing_index = Standings[Standings['Team'].str.lower() == team_name.lower()].index
    if len(standing_index) == 0:
        print(f"Team record not found for {team_name}.")
        return

    team_record = Standings.iloc[standing_index[0]]

    team_record_str = f"{team_record['Team']}'s record: {team_record['Overall']}"
    
    
    # wins = int(team_record['Overall'][:2])
    # print(wins)
 #   print(team_record_str)

    # plt.figure(figsize=(10, 10))
    plt.figure(figsize = (10,10))
    plt.pie(PosVal.values(), labels=PosVal.keys(), autopct=autopct_format(PosVal.values()))
    plt.title(f'The Salary Distribution by Position for the {team_name} is \nTotal Salary: ${total_salary:,}\n{team_record_str}')

    # plt.subplot(1, 2, 2)
    # plt.bar(PosVal.keys(), PosVal.values(), color=['blue', 'orange', 'green'])
    # plt.title(f'Salary Distribution by Position for {team_name}\nTotal Salary: ${total_salary:,}')
    # plt.ylabel('Total Salary')

    plt.show()

    for pos, value in PosVal.items():
        percentage = (value / total_salary) * 100
        print(f"{pos}: {percentage:.2f}% - ${value:,.2f}")


    # Roster = pd.read_csv(roster_file)
    # print(Roster)


team_name = input("Please enter the team name: ")
process_team_data(team_name)
