from pymongo import MongoClient
conn = MongoClient('127.0.0.1', 27017)
db = conn['sprider']
content = db['asphaltler']
result = content.find({'description':{'$regex':'asphalt','$options':'i'}})
for i in result:
    print(i)