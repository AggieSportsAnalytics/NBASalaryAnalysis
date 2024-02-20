import pandas as pd
import matplotlib.pyplot as plt

def process_team_data(team_name):
    stats_file = f"{team_name}PlayerStats.csv"
    salary_file = f"{team_name}Salary.csv"
    standings_file = "NBAStandings.csv"

    stats_data = pd.read_csv(stats_file)
    salary_data = pd.read_csv(salary_file)
    standings_data = pd.read_csv(standings_file)

    # Merge datasets based on player names
    merged_data = pd.merge(salary_data, stats_data, on='Player', how='inner')

    # Save merged dataset to a new CSV file
    merged_data.to_csv(f"{team_name}MergedData.csv", index=False)

    # Remove the dollar sign from the data to clean it up
    merged_data['2023-24'] = merged_data['2023-24'].replace('[\$,]', '', regex=True).astype(float)
    starters = merged_data.head(5)

    merged_data['Role'] = merged_data['Player'].apply(lambda x: 'Starters' if x in starters['Player'].tolist() else 'Bench')

    total_salary = merged_data.groupby('Role')['2023-24'].sum()

    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}%\n(${v:,})'.format(p=pct, v=val)
        return my_format

    # Calculate total team salary
    total_team_salary = merged_data['2023-24'].sum()

    # Extract only the last name of each team from standings data
    standings_data['Team'] = standings_data['Team'].str.split().str[-1]

    # Matches the team name input with the input that is on the standings
    standing_index = standings_data[standings_data['Team'].str.lower() == team_name.lower()].index
    if len(standing_index) == 0:
        print(f"Team record not found for {team_name}.")
        return

    # Extract team's record by the row index wherever the team name is
    team_record = standings_data.iloc[standing_index[0]]

    team_record_str = f"{team_record['Team']}'s record: {team_record['Overall']}"

    colors = ['#f44336', '#2986cc']

    # Plot the pie chart
    plt.figure(figsize=(10, 10))
    plt.pie(total_salary, labels=total_salary.index, autopct=autopct_format(total_salary), colors=colors)
    plt.title(f'Salary Distribution based on Starters and Bench for {team_record["Team"]}\nTotal Salary: ${total_team_salary:,.0f}\n{team_record_str}')
    plt.show()

team_name = input("Please enter the team name: ")
process_team_data(team_name)
