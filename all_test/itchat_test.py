import requests,os
import pymongo
import openpyxl
import random
conn = pymongo.MongoClient('127.0.0.1',27017)
db = conn['all_contents']
sprider = db['all_contents']

need_db = conn['webcrawler']
need_coll = need_db['paver_contents']

all_contents = need_coll.find()
for each_content in all_contents:
	data = {
		'abstract':each_content['title']+each_content['description'],
		'rand':random.random()
	}
	sprider.insert(data)
print('done')