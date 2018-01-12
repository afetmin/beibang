#coding:utf-8
"""
清洗数据库里含有特殊字符的内容，替换掉错误的特殊字符
"""
from pymongo import MongoClient
import re
import random
ok_words = '''asphalt machine equipment cracks driveway sealer sealcoat sealant machines paving bitumen paver pavers road'''
conn = MongoClient('127.0.0.1', 27017)
db = conn['avira']
avira = db['avira_results']
cursor = avira.find()
result = db['asphalt_results']
replace_title = ['asphalt paving','ashalt chip sealer','asphalt distributor']
pattern = re.compile(r'[\u4e00-\u9fa5]')
for content in cursor:
    if len(pattern.findall(content['title'])) ==0 and len(pattern.findall(content['description'])) ==0:
        if any(key in content['title'].split() for key in ok_words.split()):
            re_title = re.sub(r'[@!#$%^*|]|(<strong>)|(</strong>)|(&amp;)|(&#\d+;)','',content['title'])
            re_des = re.sub(r'[@!#$%^*|]|(<strong>)|(</strong>)|(&amp;)|(&#\d+;)','',content['description'])
            data = {
                'title':re_title,
                'description':re_des
            }
            result.insert(data)
print('Done!')
