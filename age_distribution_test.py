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

    # Convert Salary to integer
    Money['Salary'] = Money['Salary'].replace("[\$,]", "", regex=True).astype(int)

    # Calculate total salary
    total_salary = Money['Salary'].sum()

    Money.to_csv('team_salaries.csv', index=False)

    # Initialize variables for each age group
    age_groups = {'Under 23': 0, '23-28': 0, '29-33': 0, 'Over 33': 0}

    # Loop through the data and aggregate salaries based on age groups
    for index, row in Money.iterrows():
        age, salary = row['Age'], row['Salary']

        if age < 23:
            age_groups['Under 23'] += salary
        elif 23 <= age <= 28:
            age_groups['23-28'] += salary
        elif 29 <= age <= 33:
            age_groups['29-33'] += salary
        else:  # Age is over 33
            age_groups['Over 33'] += salary

    # Custom autopct function to show percentage and money value
    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}%\n(${v:,})'.format(p=pct,v=val)
        return my_format

    # Plotting the pie chart for age groups with percentage and money value
    plt.figure(figsize=(8, 8))
    plt.pie(age_groups.values(), labels=age_groups.keys(), autopct=autopct_format(age_groups.values()))
    plt.title(f'Salary Distribution by Age Group for {team_name}\nTotal Salary: ${total_salary:,}')
    plt.show()

    # Load and display the Roster dataset
    try:
        Roster = pd.read_csv(roster_file)
        print(Roster)
    except FileNotFoundError:
        print(f"Roster file for {team_name} not found.")

# Example usage
team_name = input("Please enter the team name: ")
process_team_data(team_name)


# Asking the user for the team name
team_name = input("Please enter the team name: ")
process_team_data(team_name)
