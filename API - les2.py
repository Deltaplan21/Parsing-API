import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
main_link = 'https://hh.ru'
page = '/search/vacancy?clusters=true&enable_snippets=true&text=Data+science&showClusters=true'

df = pd.DataFrame({}, columns = ['name','company','salary','city','link','site'])
i = 0
while i < 100:
    req = requests.get(main_link + page, headers=headers)
    html = bs(req.text, 'lxml')
    vacancies = html.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
    for vacancy in vacancies:
        name = vacancy.find('a', {'class':'bloko-link HH-LinkModifier'}).getText()
        company = vacancy.find('a', {'class':'bloko-link bloko-link_secondary HH-AnonymousIndexAnalytics-Recommended-Company'}).getText()
        salary = vacancy.find('div', {'class':"vacancy-serp-item__compensation"})
        if salary is None:
            salary = 'Не указано'
        else: salary = salary.getText()
        city = vacancy.find('span', {'data-qa':'vacancy-serp__vacancy-address'}).getText()
        link = vacancy.find('a', {'class':'bloko-link HH-LinkModifier'})['href'][:30]
        site = 'HeadHunter'
        df.loc[i] = name,company,salary,city, link,site
        i += 1
    page = html.find('a', {'class':'bloko-button HH-Pager-Control'})['href']

super_job = 'https://superjob.ru'
page_sj = '/vacancy/search/?keywords=python'

# while i < 200:
#     req_sj = requests.get(super_job + page_sj, headers=headers)
#     html_sj = bs(req_sj.text, 'lxml')
#     vacancies_sj = html_sj.find_all('div', {'class':'_2GPIV'})
#     link = super_job + html_sj.find('a', {'class': 'icMQ_ _1QIBo'})['href']
#     print(link)
#     print(vacancies_sj)
#     for vacancy in vacancies_sj:
#         name = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
#         company = vacancy.find('a', {'class':'icMQ_'}).getText()
#         salary = vacancy.find('span', {'class':"_3mfro"})
#         if salary is None:
#             salary = 'Не указано'
#         else: salary = salary.getText()
#         city = vacancy.find('span', {'class':'_3mfro _9fXTd _2JVkc _3e53o _3Ll36'}).getText()
#         link = super_job + vacancy.find('a', {'class':'icMQ_ _1QIBo'})['href']
#         site = 'SuperJob'
#         df.loc[i] = name,company,salary,city, link,site
#         i += 1
#     page_sj = html_sj.find('a', {'class': 'icMQ_ _1_Cht _3ze9n'})['href']
print(df)
df.to_csv('hh.csv')