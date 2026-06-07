import pandas as pd
df = pd.read_csv("job opportunities.csv")
print(df.head(5))
print(df.tail(5))
print(df.shape)
print(f"Обсяг: {df.memory_usage().sum() / 1024 ** 2:.2f}MB")
print(df.dtypes)
print(df.isna().sum())

cloud_jobs = df[df['Industry'] == 'Cloud Computing']
print(cloud_jobs.head())
cloud_jobs = df[df['Experience Level'] == 'Senior']
print(cloud_jobs.head())

target_jobs = df[(df['Job Type'] == 'Full-Time') & (df['Location'] == 'London')]
print(f"Знайдено вакансій: {len(target_jobs)}")
print(target_jobs.head())


industry_counts = df.groupby('Industry').size()
print("Кількість вакансій за галузями:")
print(industry_counts)

df['Min_Salary'] = df['Salary Range'].str.split('-').str[0].str.replace('£', '').str.replace(',', '').astype(int)
df['Max_Salary'] = df['Salary Range'].str.split('-').str[1].str.replace('£', '').str.replace(',', '').astype(int)
avg_Min_Salary = df.groupby('Industry').agg({'Min_Salary': 'mean'})
print(avg_Min_Salary)

df['Avg_Salary'] = (df['Min_Salary'] + df['Max_Salary']) / 2
best_industry = df.groupby('Industry')['Avg_Salary'].mean().idxmax()
best_salary = df.groupby('Industry')['Avg_Salary'].mean().max()
print(f"Галузь з найвищою зарплатою: {best_industry}")
print(f"Середня зарплата: {best_salary:.0f}")


def Salary_Category(sal):
    if sal < 40001:
        return 'Low'
    elif 40001 <= sal < 70000:
        return 'Medium'
    else:
        return 'High'

df['Salary Category'] = df['Max_Salary'].apply(Salary_Category)
print(df[['Salary Range', 'Salary Category']].head())

df['Date Posted'] = pd.to_datetime(df['Date Posted'])
print(df[['Date Posted']].info())

df['Year'] = df['Date Posted'].dt.year
print(df[['Date Posted', 'Year']].head())

jobs_per_year = df.groupby('Year')['Job Title'].agg('count')
most_active_years = jobs_per_year.sort_values(ascending=False)
print("Кількість вакансій за роками (від найактивнішого):")
print(most_active_years)

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print(f"Дані успішно завантажено! Рядків: {self.df.shape[0]}, Колонок: {self.df.shape[1]}")
        return self.df

    def check_memory_and_missing(self):
        usage = self.df.memory_usage().sum() / 1024**2
        print(f"\nЗагальний обсяг пам'яті: {usage:.2f} MB")
        print("Пропущені значення:")
        print(self.df.isna().sum())

loader = DataLoader('Job opportunities.csv')
my_data = loader.load_data()
loader.check_memory_and_missing()



sorted_jobs = df.sort_values(by='Max_Salary', ascending=False)
print("5 вакансій з найвищою зарплатою:")
print(sorted_jobs[['Job Title', 'Company', 'Max_Salary']].head(5))

top_job_titles = df.groupby('Job Title')['Max_Salary'].mean().sort_values(ascending=False)
print("\nТоп найбільш високооплачуваних посад:")
print(top_job_titles.head(5))