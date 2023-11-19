import pandas as pd
import seaborn as sns
from matplotlib.pyplot import pie, axis, show

dataset = pd.read_csv("PelicansTest.csv")

print("Dataset :")
print(dataset.head())

X = dataset
for i in range(1, 6):
    temp = "Salary." + str(i) 
    X = X.drop(temp, axis = 1)

y = dataset['Player']
X = X.drop("Unnamed: 8", axis = 1)


print("Dataset :")
print(X.head())


sums = X.groupby(X["Player"])["Salary"].sum()
axis('equal')
pie(sums, labels=sums.index)
show()