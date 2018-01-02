import pymongo
import time

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn['sprider']
find_keys = db['find_keys']
asphalt = db['asphaltler']

while 1:
    keys = find_keys.count()
    asph = asphalt.count()
    print('共找到%s条关键字' % keys)
    print('共找到%s条内容' % asph)
    time.sleep(5)
