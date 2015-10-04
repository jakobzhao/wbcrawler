# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from wbcrawler3.settings import KEYWORDS



class KeywordSpider(scrapy.spiders.Spider):
    name = 'keyword'
    allowed_domains = ['weibo.com']
    start_url = ['http://s.weibo.com/'+ KEYWORDS[0], 'http://s.weibo.com/'+ KEYWORDS[1]]

    def parse(self, response):
            filename = response.url.split("/")[-2]
            with open(filename, 'wb') as f:
                f.write(response.body)