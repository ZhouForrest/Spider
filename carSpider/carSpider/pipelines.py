# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

from carSpider.items import DealerItem, CarItem, CarConfItem


class CarspiderPipeline(object):
    def __init__(self):
        conn = MongoClient(host='127.0.0.1', port=27017)
        self.db = conn['autohome']
        self.collection = self.db['dealer']

    def process_item(self, item, spider):
        if isinstance(item, DealerItem):
            self.collection.update({'_id': item['_id']}, {'$set': item}, True)
        if isinstance(item, CarItem):
            self.collection.update({'_id': item['id']}, {'$addToSet': {'car_type': {'$each': item['car_type']}}})
            self.db['car'].update({'_id': item['id']}, {'$set': item['car_type'][0]}, True)
        if isinstance(item, CarConfItem):
            self.db['car'].update({'_id': item['id']}, {'$set': {'car_conf': item['car_conf'][0]}})
        return item
