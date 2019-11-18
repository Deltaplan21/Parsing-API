# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avito.items import AvitoItem
from scrapy.loader import ItemLoader


class AutoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/transport']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.pagination-page js-pagination-next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        ads_links = response.xpath('//a[@class="styles-link-36uWZ"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoItem(), response=response)
        loader.add_xpath('photos', '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        yield loader.load_item()

