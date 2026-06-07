import sqlite3
import pandas as pd


df = pd.read_csv('Job opportunities.csv')
print(df.head())
conn = sqlite3.connect('jobs_database.db')
df.to_sql('jobs', conn, if_exists='replace', index=False)

query = "SELECT * FROM jobs LIMIT 10;"
result = pd.read_sql(query, conn)
print(result)
query2 = "SELECT * FROM jobs WHERE [Required Skills] LIKE '%SQL%'"
python_vacancies = pd.read_sql(query2, conn)
print(python_vacancies.head())
print(python_vacancies[['Job Title', 'Required Skills', 'Location']].head())

query_distinct = "SELECT DISTINCT Location, Company FROM jobs"
unique_places = pd.read_sql(query_distinct, conn)
print("Унікальні локації та компанії:")
print(unique_places.head)

df['Min_Salary'] = df['Salary Range'].str.split('-').str[0].str.replace('£', '').str.replace(',', '').astype(int)
df['Max_Salary'] = df['Salary Range'].str.split('-').str[1].str.replace('£', '').str.replace(',', '').astype(int)
df['Avg_Salary'] = (df['Min_Salary'] + df['Max_Salary']) / 2
df.to_sql('jobs', conn, if_exists='replace', index=False)

query3 = """
    SELECT
        [Experience Level],
        AVG(Avg_Salary) as Average_Salary
    FROM jobs
    GROUP BY [Experience Level]
    ORDER BY Average_Salary DESC
"""
experience_salaries = pd.read_sql(query3, conn)
pd.options.display.float_format = '{:,.0f}'.format
print("Середня зарплата залежно від рівня досвіду:")
print(experience_salaries)

query4 = "SELECT [Experience Level], COUNT() FROM jobs GROUP BY [Experience Level];"
experience_count = pd.read_sql(query4, conn)
print("Кількість вакансій для рівнів досвіду:")
print(experience_count)


query5 = "SELECT [Job Title], [Salary Range], MIN(Min_Salary) FROM jobs"
min_sal = pd.read_sql(query5, conn)
print("мінімальна зарплата: ")
print(min_sal)

query5 = "SELECT [Job Title], [Salary Range], MAX(Max_Salary) FROM jobs"
max_sal = pd.read_sql(query5, conn)
print("максимальна зарплата: ")
print(max_sal)


query6 = """ SELECT Industry, COUNT() FROM jobs WHERE  [Min_Salary] > 50000 GROUP BY Industry """
indust = pd.read_sql(query6, conn)
print("Кількість вакансій у кожній індустрії, де зарплата більша 50000: ")
print(indust)

query7 = " SELECT Industry, AVG(Avg_salary) as avg_salary FROM jobs GROUP BY Industry; "
avg_sal = pd.read_sql(query7, conn)
print("середня зарплата для кожної індустрії: ")
print(avg_sal)


query8 = """ SELECT Location, [Experience Level], COUNT(*) AS vacancies
        FROM jobs GROUP BY Location, [Experience Level]; """
vacan = pd.read_sql(query8, conn)
print("Кількість вакансій за Location i Experience Level: ")
print(vacan)


query9 = """ SELECT Industry, [Job Type], COUNT(*) AS vacancies
            FROM jobs GROUP BY Industry, [Job Type]; """
vac = pd.read_sql(query9, conn)
print("кількість вакансій у кожній індустрії та для кожного типу роботи: ")
print(vac)


query10 = """ SELECT Location, [Experience Level], AVG(Avg_Salary)
        FROM jobs GROUP BY Location, [Experience Level]; """
avg = pd.read_sql(query10, conn)
print("середня зарплата для вакансій за Location та Experience Level: ")
print(avg)


query11 = " SELECT Max_Salary FROM jobs ORDER BY Max_Salary DESC "
high_line = pd.read_sql(query11, conn)
print("вакансії з навищою верхньою межею зарплат: ")
print(high_line.head())


skills_list = df['Required Skills'].str.split(',')
exploded_skills = skills_list.explode()
clean_skills = exploded_skills.str.strip()
skills_count = clean_skills.value_counts()
print("кількість вакансій: ")
print(skills_count)



query12 = """SELECT Company, COUNT(*) as Vacancies_Count FROM jobs
    WHERE [Date Posted] LIKE '%2023%'
    GROUP BY Company
    ORDER BY Vacancies_Count DESC
    LIMIT 10
"""

top_companies_2023 = pd.read_sql(query12, conn)
print("Топ-10 компаній за кількістю вакансій у 2023 році:")
print(top_companies_2023)

conn.close()