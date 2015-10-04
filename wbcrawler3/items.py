# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Wbcrawler3Item(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    content
    username = scrapy.Field()
    userid = scrapy.Field()

    pass


class PostItem(scrapy.Item):
    # define the fields for your item here like:
    #metadata
    keyword = scrapy.Field()

    #self
    id = scrapy.Field()
    content = scrapy.Field()

    #author
    username = scrapy.Field()
    userid = scrapy.Field()

    # time
    pass