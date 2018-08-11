# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from pymongo import MongoClient
from scrapy.conf import settings

from wbspider.items import WbspiderItem, Relation_fans, Relation_followers


class WbspiderPipeline(object):

    def __init__(self):
        self.conn = MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
        self.db = self.conn[settings['MONGODB_DB']]
        self.collection = self.db[WbspiderItem.collection]

    def process_item(self, item, spider):
        if isinstance(item, WbspiderItem):
            self.collection.update({'_id': item.get('_id')}, {'$set': item}, True)
        if isinstance(item, Relation_fans):
            self.collection.update({'_id': item.get('_id')},
                                   {'$addToSet':
                                        {'$each': item['fans']}
                                    }, True)
        if isinstance(item, Relation_followers):
            self.collection.update({'_id': item.get('_id')},
                                   {'$addToSet':
                                        {'$each': item['followers']}
                                    }, True)
        return item


class CreateTime(object):

    def process_item(self, item, spider):
        if isinstance(item, WbspiderItem):
            dict(item)['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%m')
        return item
