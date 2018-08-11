# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):

    collect = 'ershoufang'
    code = scrapy.Field()
    title = scrapy.Field()
    loupan = scrapy.Field()
    houseInfo = scrapy.Field()
    flood = scrapy.Field()
    tag = scrapy.Field()
    img = scrapy.Field()
    total = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()


# class MasterItem(scrapy.Item):
#     url = scrapy.Field()




