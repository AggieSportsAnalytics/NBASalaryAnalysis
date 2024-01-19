import pandas as pd
import matplotlib.pyplot as plt

# Load and process the Salary dataset
Money = pd.read_csv("LakersTest.csv")
Money = Money[["Player", "Age", "Salary"]]
Money = Money.dropna()


for val in Money.index:
    Money["Salary"][val] = int(Money["Salary"][val].replace("$", ""))

Money.to_csv('team_salaries.csv')

#print(type(Money["Salary"][0]))

# Initialize variables for each age group
u23, a23_28, a29_33, o33 = 0, 0, 0, 0


# Loop through the data and aggregate salaries based on age groups
for val in Money.index:
    if Money["Age"][val] < 23:
        u23 += Money["Salary"][val]
    elif 23 <= Money["Age"][val] <= 28:
        a23_28 += Money["Salary"][val]
    elif 29 <= Money["Age"][val] <= 33:
        a29_33 += Money["Salary"][val]
    else: # Age is over 33
        o33 += Money["Salary"][val]

# Creating a DataFrame for the new age groups and their salaries
age_group_salaries = pd.DataFrame({
    'Age Group': ["Under 23", "23-28", "29-33", "Over 33"],
    'Salary': [u23, a23_28, a29_33, o33]
})

# Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(age_group_salaries['Salary'], labels=age_group_salaries['Age Group'], autopct='%1.1f%%')
plt.title('Salary Distribution by Age Group')
plt.show()

# Load and display the Roster dataset
Roster = pd.read_csv("LakersRoster.csv")
print(Roster)

