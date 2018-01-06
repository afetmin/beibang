#coding:utf-8
"""
查询数据库中数据量
"""
from count_mongo import countMongo
from pymongo import MongoClient
def count_monster():
    monster = countMongo('monstercralwer', 'crack_sealing_machine_contents','crack_sealing_machine_keys')
    monster.count()

def count_avira():
    avira = countMongo('avira', 'avira_contents')
    avira.count()

def count_bing():
    bing = countMongo('bing','bing_contents')
    bing.count()
# count_avira()
# count_monster()
count_bing()
