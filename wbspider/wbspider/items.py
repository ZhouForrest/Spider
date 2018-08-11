# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WbspiderItem(scrapy.Item):
    collection = 'stars'
    _id = scrapy.Field()
    screen_name = scrapy.Field()
    profile_image_url = scrapy.Field()
    profile_url = scrapy.Field()
    followers_count = scrapy.Field()
    follow_count = scrapy.Field()
    cover_image_phone = scrapy.Field()


class Relation_fans(scrapy.Item):
    fans = scrapy.Field()


class Relation_followers(scrapy.Item):

    followers = scrapy.Field()

