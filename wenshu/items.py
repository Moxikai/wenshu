# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Item,Field
class WenshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = Field()
    date = Field()
    document_code = Field()
    court = Field()
    content = Field()
    url = Field()
    source_crawl = Field()
    type = Field()
    areaName = Field()
    first_court = Field()