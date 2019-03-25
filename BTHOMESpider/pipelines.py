# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .settings import Mongo_config


class BthomespiderPipeline(object):

    def __init__(self):
        self.mongo_host = Mongo_config['MONGO_HOST']
        self.mongo_dbname = Mongo_config['MONGO_DBNAME']
        self.mongo_port = Mongo_config['MONGO_PORT']
        self.mongo_docname = Mongo_config['MONGO_DOCNAME']
        self.client = pymongo.MongoClient(host=self.mongo_host,port=self.mongo_port)
        self.mondb = self.client[self.mongo_dbname]
        self.post = self.mondb[self.mongo_docname]



    def process_item(self, item, spider):
        info = dict(item)
        self.post.insert(info)
        return item


    def open_spder(self, spider):
        print("Begin to store BTHome... ")

    def close_spider(self, spider):
        self.movie_nmber = self.post.count()
        print('总共保存 {} 部电影'.format(self.movie_nmber))

