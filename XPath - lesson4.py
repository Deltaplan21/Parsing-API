import requests
from lxml import html

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
sites = 'https://lenta.ru','https://mail.ru'

request_lenta = requests.get(sites[0], headers=headers)
root_lenta = html.fromstring(request_lenta.text)
request_mailru = requests.get(sites[1], headers=headers)
root_mailru = html.fromstring(request_mailru.text)

link_lenta = root_lenta.xpath("//h2/a/@href | //div[@class='span4']//div[@class='item']/a/@href")
date_lenta = root_lenta.xpath("//h2/a/time/@title | //div[@class='span4']//div[@class='item']/a/time/@title")
headline_lenta = root_lenta.xpath("//h2/a/text() | //div[@class='span4']//div[@class='item']/a/text()")
source_lenta = 'lenta.ru'

date_mailru = []
link_mailru = root_mailru.xpath("//div[contains(@class, 'news-item_main')]/a/@href | //div[contains(@class, 'news-item__inner')]/a[last()]/@href")
headline_mailru = root_mailru.xpath("//div[contains(@class, 'news-item_main')]//h3/text() | //div[contains(@class, 'news-item_inline')]//a[last()]/text()")
source_mailru = 'mail.ru'
for i in link_mailru:
    request = requests.get(i, headers=headers)
    root = html.fromstring(request.text)
    news_dates = root.xpath("//span[contains(@class, 'breadcrumbs')]/@datetime")
    news_dates = news_dates[0]
    date_mailru.append(news_dates)
for i, j, k in zip(headline_lenta, date_lenta, link_lenta):
    print('='*70+f'\n{j}\n{i}\n{sites[0]+k}\n{source_lenta}')
for i, j, k in zip(headline_mailru, date_mailru, link_mailru):
    print('='*70+f'\n{j[:10]}\n{i}\n{k}\n{source_mailru}')
