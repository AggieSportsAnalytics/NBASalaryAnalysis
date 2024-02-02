import pandas as pd
import matplotlib.pyplot as plt


def process_team_data(team_name):

    # Load datasets
    stats_file = f"{team_name}Salary.csv"
    salary_file = f"{team_name}BasketballReference.csv"

    stats_data = pd.read_csv(stats_file)
    salary_data = pd.read_csv(salary_file)


    # Merge datasets based on player names
    merged_data = pd.merge(stats_data, salary_data, on='Player', how='inner')

    # Save merged dataset to a new CSV file
    merged_data.to_csv(f"{team_name}MergedData.csv", index=False)

    #Remove the dollar sign
    merged_data['2023-24'] = merged_data['2023-24'].replace('[\$,]', '', regex=True).astype(float)
    starters = merged_data.head(5)

    merged_data['Role'] = merged_data['Player'].apply(lambda x: 'Starter' if x in starters['Player'].tolist() else 'Bench')

    total_salary = merged_data.groupby('Role')['2023-24'].sum()

    # Plot the pie chart
    plt.figure(figsize=(10, 10))
    plt.pie(total_salary, labels=total_salary.index, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
    plt.title(f'{team_name} Percentage of Total Salary Among Starters and Bench Players (2023-24 Season)')
    plt.show()

process_team_data("Suns")