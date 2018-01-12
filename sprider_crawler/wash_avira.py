#coding:utf-8
from pymongo import MongoClient
import re
conn = MongoClient('127.0.0.1', 27017)
db = conn['webcrawler']
avira = db['paver_contents']
cursor = avira.find()
result = db['paver_results']
for content in cursor:
    if content.get('abstract',None):
        re_title = re.sub(r'(<strong>|</strong>)|[\u4e00-\u9fa5]|(&#)(\w)+|(&amp)|(&quot;);','',content['title'])
        re_abstract = re.sub(r'(<strong>|</strong>)|[\u4e00-\u9fa5]|(&#)(\w)+|(&amp)|(&quot;);','',content['abstract'])
    else:
        re_title = re.sub(r'(<strong>|</strong>)|[\u4e00-\u9fa5]|(&#)(\w)+|(&amp)|(&quot;);', '', content['title'])
        re_abstract = re.sub(r'(<strong>|</strong>)|[\u4e00-\u9fa5]|(&#)(\w)+|(&amp)|(&quot;);','',content['description'])
    data = {
        'title':re_title,
        'description':re_abstract
    }
    result.insert(data)
print('Done!')
