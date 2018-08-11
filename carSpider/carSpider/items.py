# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DealerItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    img = scrapy.Field()
    main_type = scrapy.Field()
    type_num = scrapy.Field()
    adress = scrapy.Field()


class CarItem(scrapy.Item):
    id = scrapy.Field()
    car_type = scrapy.Field()


class CarConfItem(scrapy.Item):
    id = scrapy.Field()
    car_conf = scrapy.Field()