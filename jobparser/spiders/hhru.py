# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=Data+science&showClusters=true']

    def vacancy_parse(self, response):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        salary_min = response.css('div.vacancy-header ~ div div.vacancy-title > span > span > meta::attr(content)').extract_first()
        salary_max = response.css('div.vacancy-title meta[itemprop="maxValue"]::attr(content)').extract_first()
        link = response.url
        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, link=link)

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

