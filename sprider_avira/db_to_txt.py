#coding:utf-8
"""
将一个数据库里的所有表中的关键字导入到一个txt文件中，以便爬虫爬取
"""
import pymongo

class dbToTxt(object):
    def __init__(self,db_name='monstercralwer'):
        conn = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = conn[db_name]

    def key_to_txt(self):

        collection_names=self.db.collection_names()
        for name in collection_names:
            if 'keys' in name.split('_'):
                cursor = self.db[name].find()
                for content in cursor:
                    with open('seen_keywords.txt','a+') as f:
                        f.write(content['keyword']+'\n')

dbtotxt = dbToTxt()
dbtotxt.key_to_txt()




