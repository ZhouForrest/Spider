# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

from scrapy.conf import settings


class DbspiderPipeline(object):

    def __init__(self):
        conn = MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for i in range(len(item['name'])):
            data = [{
                'name': item['name'][i],
                'year': item['year'][i],
                'director': item['director'][i],
                'avatar': item['avatar'][i]
                }]
            self.collection.update({})

        return item
