import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import pivot_table

df = pd.read_csv('Job opportunities.csv')

df['Min_Salary'] = df['Salary Range'].str.split('-').str[0].str.replace('£', '').str.replace(',', '').astype(int)
df['Max_Salary'] = df['Salary Range'].str.split('-').str[1].str.replace('£', '').str.replace(',', '').astype(int)
df['Average_Salary'] = (df['Min_Salary'] + df['Max_Salary']) / 2

plt.figure(figsize=(10,6))
sns.barplot(x='Experience Level', y='Average_Salary', data=df, palette= 'viridis', hue= 'Experience Level')
plt.title('Залежність середньої зарплати від рівня досвіду')
plt.xlabel('Рівень досвіду')
plt.ylabel('Середня зарплата (£)')
plt.show()

# y - chyslo, x - ne chyslo

plt.figure(figsize=(12,6))
sns.boxplot(x='Industry', y='Average_Salary', data=df, palette='Set2')
plt.title("Розподіл зарплат за галузями")
plt.xlabel("Індустрія")
plt.ylabel("Зарплата")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


pivot_table = pd.crosstab(df['Experience Level'], df['Industry'])
plt.figure(figsize=(12,4))
sns.heatmap(pivot_table, annot=True, cmap='viridis', linewidths=0.5)
plt.title('Кореляція між Experience Level та Industry')
plt.tight_layout()
plt.xticks(rotation=45, ha='right')
plt.show()


df['Date Posted'] = pd.to_datetime(df['Date Posted'])
df['Year'] = df['Date Posted'].dt.year
plt.figure(figsize=(12,8))
sns.scatterplot(y='Average_Salary', x='Year', hue='Experience Level', data=df, palette='deep', alpha=0.7)
plt.title('Залежність зарплати від року публікації вакансії')
plt.ylabel('Зарплата')
plt.xlabel("Рік публікації")
plt.legend(title='Рівень досвіду', bbox_to_anchor=(1.0,1), loc='upper left')
plt.show()


sns.pairplot(df[['Average_Salary', 'Year', 'Experience Level']], hue= 'Experience Level', diag_kind='kde', palette='bright')
plt.suptitle('Парні графіки для Average_Salary, Year та Experience Level', y=1.05)
plt.show()