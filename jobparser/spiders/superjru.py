# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import json


class SuperjruSpider(scrapy.Spider):
    name = 'superjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/dvornik.html?geo%5Bc%5D%5B0%5D=1']

    def vacancy_parse(self, response):
        name = response.css('h1::text').extract()
        salary_min = json.loads(response.css('div._1Tjoc._3C60a.Ghoh2.UGN79._1XYex > script::text').extract_first())['baseSalary']['value']['minValue']
        salary_max = json.loads(response.css('div._1Tjoc._3C60a.Ghoh2.UGN79._1XYex > script::text').extract_first())['baseSalary']['value']['maxValue']
        link = response.url
        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, link=link)

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.css('div.f-test-vacancy-item a[class*=f-test-link][href^="/vakansii"]::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)
