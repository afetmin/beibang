#coding:utf-8
"""
查询数据库中数据量
"""
from count_mongo import countMongo
from pymongo import MongoClient
def count_monster():
    monster = countMongo('webcrawler', 'paver_contents','paver_keys')
    monster.count()

def count_avira():
    avira = countMongo('avira', 'paver_contents')
    avira.count()

def count_bing():
    bing = countMongo('bing','paver_contents')
    bing.count()
count_avira()
# count_monster()
# count_bing()
