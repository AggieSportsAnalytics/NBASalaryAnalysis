import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("PelsSalaryMP.csv")

starters = dataset.head(5)

dataset['Role'] = dataset['Player'].apply(lambda x: 'Starter' if x in starters['Player'].tolist() else 'Bench')

# print(dataset[['Player', 'MP', '2023-24 Salary', 'Role']])

# Convert 2023-24 Salary to numeric
# dataset['2023-24 Salary'] = dataset['2023-24 Salary'].replace('[\$,]', '', regex=True).astype(float)

# Calculate total salary for starters and bench
total_salary = dataset.groupby('Role')['2023-24 Salary'].sum()

plt.figure(figsize=(10, 10))
plt.pie(total_salary, labels=total_salary.index, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
plt.title('Percentage of Total Salary Among Starters and Bench Players of New Orleans Pelicans (2023-24 Season)')
plt.show()
