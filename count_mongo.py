#coding:utf-8
"""
一个数据库查询类
"""
import pymongo
import time


class countMongo(object):
    def __init__(self, db_name,content_table_name,key_table_name=None):
        conn = pymongo.MongoClient('127.0.0.1', 27017)
        db = conn[db_name]
        if key_table_name:
            self.key = db[key_table_name]
        else:
            self.key = None
        self.content = db[content_table_name]

    def count(self):
        while 1:
            if self.key:
                keys = self.key.count()
                print('共找到%s条关键字' % keys)
            asph = self.content.count()
            print('共找到%s条内容' % asph)
            time.sleep(5)

