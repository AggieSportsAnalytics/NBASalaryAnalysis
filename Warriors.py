from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd
import seaborn as sns
from matplotlib.pyplot import pie, axis, show
import numpy as np
import os
import csv



WarriorsRoster = pd.read_csv('WarriorsRoster.csv')
# Read the second CSV file
WarriorsTest = pd.read_csv('WarriorsTest.csv')
# Merge the two DataFrames based on a common column
WarriorsRosSalPos = pd.merge(WarriorsRoster, WarriorsTest, on='Player', how='inner')
# Save the merged DataFrame to a new CSV file
WarriorsRosSalPos.to_csv('WarriorsRosSalPos.csv', index=False)



Salary = pd.read_csv("WarriorsRosSalPos.csv")

Salary = Salary[["Player","Pos","Salary"]]

Salary = Salary.dropna()
for val in Salary.index:
    Salary["Salary"][val] = int(Salary["Salary"][val].replace("$", ""))
Salary.to_csv('WarriorsTest.csv')

print(Salary)

g,f,c = 0,0,0

for val in Salary.index:
    if Salary["Pos"][val] == "PG" or Salary["Pos"][val] == "SG":
        g += Salary["Salary"][val]
    if Salary["Pos"][val] == "SF" or Salary["Pos"][val] == "PF":
        f += Salary["Salary"][val]
    if Salary["Pos"][val] == "C":
        c += Salary["Salary"][val]



print(g)
print(f)
print(c)


PosVal = pd.DataFrame({
    'Pos': ["Guard", "Forward", 'Center'],
    'Salary': [g, f, c]
    })

sums = PosVal.groupby(PosVal["Pos"])["Salary"].sum()
pie(sums, labels=sums.index,autopct='%1.1f%%')
show()
