import requests, re
import pandas as pd
from bs4 import BeautifulSoup as bs
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
main_link = 'https://hh.ru'
page = '/search/vacancy?clusters=true&enable_snippets=true&text=Data+science&showClusters=true'

df = pd.DataFrame({}, columns = ['name','company','salary_min','salary_max','link','site'])
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
            salary_min = 0
            salary_max = 0
        else:
            salary = salary.getText()
            if 'от' in salary:
                salary_min = re.findall('([\d\s]*)', salary)[2].replace('\xa0', '')
                salary_max = 0
            elif 'до' in salary:
                salary_max = re.findall('([\d\s]*)', salary)[2].replace('\xa0', '')
                salary_min = 0
            else:
                salary_min = re.findall('([\s\d]*)?-', salary)[0].replace('\xa0','')
                salary_max = re.findall('-([\s\d]*)', salary)[0].replace('\xa0','')
        link = vacancy.find('a', {'class':'bloko-link HH-LinkModifier'})['href'][:30]
        site = 'HeadHunter'
        df.loc[i] = name,company,salary_min,salary_max,link,site
        i += 1
    page = html.find('a', {'class':'bloko-button HH-Pager-Control'})['href']

super_job = 'https://superjob.ru'
page_sj = '/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1'
j=1

while i < 150:
    while j < 5:
        req_sj = requests.get(super_job + page_sj, headers=headers)
        html_sj = bs(req_sj.text, 'lxml')
        vacancies_sj = html_sj.find_all('div', {'class':'_3syPg _1_bQo _2FJA4'})
        for vacancy in vacancies_sj:
            name = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
            company = vacancy.find('span', {'class':'_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI'})
            if company is None:
                company = 'Не указано'
            else: company = company.findChild().getText()
            salary = vacancy.find('span', {'class':"_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz"}).getText()
            if salary == 'По договорённости':
                salary_min = 0
                salary_max = 0
            elif 'от' in salary:
                salary_min = re.findall('([\d\s]*)', salary)[2].replace('\xa0','')
                salary_max = 0
            elif 'до' in salary:
                salary_max = re.findall('([\d\s]*)', salary)[2].replace('\xa0', '')
                salary_min = 0
            else:
                salary_min = re.findall('([\d\s]*).', salary)[0].replace('\xa0','')
                salary_max = re.findall('—([\d\s]*)', salary)
                if len(salary_max) > 0:
                    salary_max = salary_max[0].replace('\xa0','')
                else: salary_max = 0
            link = super_job + vacancy.findChild().findChild()['href']
            site = 'SuperJob'
            df.loc[i] = name,company,salary_min,salary_max,link,site
            i += 1
        j += 1
        page_sj = f'/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1&page={j}'
print(df)
df.to_csv('job.csv', index=None)