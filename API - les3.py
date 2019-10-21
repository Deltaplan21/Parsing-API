from pymongo import MongoClient
import pandas as pd
client = MongoClient('localhost',27017)
db = client['Jobs_db']
jobs = db.jobs_coll
jobs2 = db.jobs_coll2

pd_db = pd.read_csv('jobs.csv')

jobs.drop()
jobs2.drop()


def job_insert(coll,pandas_df):
    for j in pandas_df.values:
        for i, k in zip(pandas_df.columns,j):
            coll.insert_one({i:k})


def insert_many(coll,pandas_df):
    for j in pandas_df.values:
        lst = [{i:k for i,k in zip(pandas_df.columns,j)}]
        coll.insert_many(lst)


job_insert(jobs, pd_db)
insert_many(jobs2,pd_db)

desired_salary = int(input('Введите желаемую зарплатy: '))

objects = jobs.find({'salary_min':{'$gte':desired_salary}}) # Поиск для insert_one, но так мы не видим все данные организации в целом
for obj in objects:
    print(obj)

objects = jobs2.find({'salary_min':{'$gte':desired_salary}}) # Поэтому лучше пользоваться поиском для insert_many
for obj in objects:
    print(obj)