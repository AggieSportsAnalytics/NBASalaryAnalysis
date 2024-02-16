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
    # Construct file names from the team name
    salary_file = f"{team_name}Salary.csv"
    roster_file = f"{team_name}Roster.csv"
    try:
        Salary = pd.read_csv(salary_file)
        Roster = pd.read_csv(roster_file)
    except FileNotFoundError:
        print(f"Salary file for {team_name} not found.")
        return
# Read the second CSV file
# WarriorsTest = pd.read_csv('WarriorsTest.csv')
# Merge the two DataFrames based on a common column
    merged_data = pd.merge(Roster, Salary, on='Player', how='inner')
# Save the merged DataFrame to a new CSV file
    merged_data.to_csv('merged_data.csv', index=False)


    Salary = Salary[["Player","Pos","Salary"]]
    Salary = Salary.dropna()

    for val in Salary.index:
        Salary["Salary"][val] = int(Salary["Salary"][val].replace("$", "").replace(",", ""))

    Salary.to_csv('team_salaries.csv')



    Salary = pd.read_csv("merged_data.csv")

    Salary = Salary[["Player","Pos","Salary"]]

    Salary = Salary.dropna()
    for val in Salary.index:
        Salary["Salary"][val] = int(Salary["Salary"][val].replace("$", ""))
    Salary.to_csv(salary_file)

    print(Salary)

    g,f,c = 0,0,0

    for val in Salary.index:
        if Salary["Pos"][val] == "PG" or Salary["Pos"][val] == "SG":
            g += Salary["Salary"][val]
        if Salary["Pos"][val] == "SF" or Salary["Pos"][val] == "PF":
            f += Salary["Salary"][val]
        if Salary["Pos"][val] == "C":
            c += Salary["Salary"][val]



    # print(g)
    # print(f)
    # print(c)


    PosVal = pd.DataFrame({
        'Pos': ["Guard", "Forward", 'Center'],
        'Salary': [g, f, c]
        })

    sums = PosVal.groupby(PosVal["Pos"])["Salary"].sum()
    plt.pie(sums, labels=sums.index,autopct='%1.1f%%')
    plt.show()

    try:
        Roster = pd.read_csv(roster_file)
        print(Roster)
    except FileNotFoundError:
        print(f"Roster file for {team_name} not found.")

team_name = input("Please enter the team name: ")
process_team_data(team_name)