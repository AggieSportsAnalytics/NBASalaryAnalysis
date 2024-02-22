import pandas as pd
import matplotlib.pyplot as plt

def process_team_data(team_name):
    # File paths
    salary_file = f"{team_name}Salary.csv"
    roster_file = f"{team_name}Roster.csv"
    standings_file = "NBAStandings.csv"

    # Load datasets
    try:
        Salary = pd.read_csv(salary_file)
        Roster = pd.read_csv(roster_file)
        Standings = pd.read_csv(standings_file)
    except FileNotFoundError as e:
        print(e)
        return

    # Merge Roster and Salary data
    if 'Player' in Salary.columns and 'Player' in Roster.columns:
        merged_data = pd.merge(Roster, Salary, on='Player', how='inner')
    else:
        print("Required columns not found in the data.")
        return

    # Process merged data for salary
    merged_data['Salary'] = merged_data['Salary'].replace('[\$,]', '', regex=True).astype(int)
    total_salary = merged_data['Salary'].sum()

    # Age group processing
    age_groups = {'Under 23': 0, '23-28': 0, '29-33': 0, 'Over 33': 0}
    for _, row in merged_data.iterrows():
        age = row['Age']
        salary = row['Salary']
        if age < 23:
            age_groups['Under 23'] += salary
        elif 23 <= age <= 28:
            age_groups['23-28'] += salary
        elif 29 <= age <= 33:
            age_groups['29-33'] += salary
        else:
            age_groups['Over 33'] += salary
    # Filter out age groups with no salary
    age_groups = {k: v for k, v in age_groups.items() if v > 0}

    # Position processing
    PosVal = {
        "Guard": merged_data.loc[merged_data['Pos'].isin(['PG', 'SG']), 'Salary'].sum(),
        "Forward": merged_data.loc[merged_data['Pos'].isin(['SF', 'PF']), 'Salary'].sum(),
        "Center": merged_data.loc[merged_data['Pos'] == 'C', 'Salary'].sum()
    }
    # Filter out positions with no salary
    PosVal = {k: v for k, v in PosVal.items() if v > 0}

    # Custom autopct function
    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}%\n(${v:,})'.format(p=pct,v=val)
        return my_format

    # Standings processing
    Standings['Team'] = Standings['Team'].str.split().str[-1]
    standing_index = Standings[Standings['Team'].str.lower() == team_name.lower()].index
    if len(standing_index) == 0:
        print(f"Team record not found for {team_name}.")
        return
    team_record = Standings.iloc[standing_index[0]]
    team_record_str = f"{team_record['Team']}'s record: {team_record['Overall']}"

    # Plotting
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.pie(age_groups.values(), labels=age_groups.keys(), autopct=autopct_format(age_groups.values()))
    plt.title(f'Salary Distribution by Age Group for {team_name}\nTotal Salary: ${total_salary:,}\n{team_record_str}')

    plt.subplot(1, 2, 2)
    plt.pie(PosVal.values(), labels=PosVal.keys(), autopct=autopct_format(PosVal.values()))
    plt.title(f'Salary Distribution by Position for {team_name}\nTotal Salary: ${total_salary:,}\n{team_record_str}')
    plt.show()

# Example usage
team_name = input("Please enter the team name: ")
process_team_data(team_name)

