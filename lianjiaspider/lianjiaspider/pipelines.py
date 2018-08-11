# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from pymongo import MongoClient
from scrapy.conf import settings
from lianjiaspider.items import LianjiaspiderItem


class LianjiaspiderPipeline(object):
    def __init__(self):
        conn = MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[LianjiaspiderItem.collect]

    def process_item(self, item, spider):
        if isinstance(item, LianjiaspiderItem):
            self.collection.update({'code': item['code']}, {'$set':item}, True)
        return item


class MasterPipeline(object):
    def __init__(self):
        self.r = redis.Redis(host='127.0.01', port=6379)

    def process_item(self, item, spider):
        self.r.lpush('lianjia:start_urls', item['url'])
