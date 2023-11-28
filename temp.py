import pandas as pd
import seaborn as sns
from matplotlib.pyplot import pie, axis, show

Salary = pd.read_csv("PelicansTest.csv")

Salary = Salary[["Player", "Age", "Salary"]]

Salary = Salary.dropna()

print("Dataset :")
# print(Salary)

# sums = Salary.groupby(Salary["Player"])["Salary"].sum()
# axis('equal')
# pie(sums, labels=sums.index)
# show()

df = pd.read_csv("PelsStats.csv")

df = df[["Player", "Age", "MP"]]
# print(df)

u23, o30, between = 0, 0, 0

for val in Salary.index:
        if Salary["Age"][val] <= 23:
            u23 += Salary["Salary"][val]
        if Salary["Age"][val] >= 30:
            o30 += Salary["Salary"][val]
        else:
            between += Salary["Salary"][val]



ageVals = pd.DataFrame({
    'Age': ["under 23", "23-30", '30+'],
    'Salary': [u23, between, o30]
    })

# sums = ageVals.groupby(ageVals["Age"])["Salary"].sum()
# axis('equal')
# pie(sums, labels=sums.index)
# show()

Roster = pd.read_csv("PelsRoster.csv")
print(Roster)
    

# 0 - 23 24 - 29 30+