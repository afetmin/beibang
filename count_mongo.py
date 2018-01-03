import pymongo
import time


class countMongo(object):
    def __init__(self, key_table_name, content_table_name):
        conn = pymongo.MongoClient('127.0.0.1', 27017)
        db = conn['sprider']
        self.key = db[key_table_name]
        self.content = db[content_table_name]

    def count(self):
        while 1:
            keys = self.key.count()
            asph = self.content.count()
            print('共找到%s条关键字' % keys)
            print('共找到%s条内容' % asph)
            time.sleep(5)

