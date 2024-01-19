import pandas as pd
import matplotlib.pyplot as plt

def process_team_data(team_name):
    # Construct file names from the team name
    salary_file = f"{team_name}Test.csv"
    roster_file = f"{team_name}Roster.csv"

    # Load and process the Salary dataset
    try:
        Money = pd.read_csv(salary_file)
    except FileNotFoundError:
        print(f"Salary file for {team_name} not found.")
        return

    Money = Money[["Player", "Age", "Salary"]]
    Money = Money.dropna()

    for val in Money.index:
        Money["Salary"][val] = int(Money["Salary"][val].replace("$", ""))

    Money.to_csv('team_salaries.csv')

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
    plt.title(f'Salary Distribution by Age Group for {team_name}')
    plt.show()

    # Load and display the Roster dataset
    try:
        Roster = pd.read_csv(roster_file)
        print(Roster)
    except FileNotFoundError:
        print(f"Roster file for {team_name} not found.")

# Example usage
process_team_data("Warriors")
