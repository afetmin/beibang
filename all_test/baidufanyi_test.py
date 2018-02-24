# coding:utf-8
from openpyxl import Workbook, load_workbook
import hashlib
import requests
import re
from collections import deque
import os, time,sys
def get_content(name):
    wb = load_workbook(str(name))
    ws1 = wb.active
    contents = deque()
    for i in ws1['A']:
        if i.value:
            contents.append(i.value)
    return contents

def string_to_md5(s):
    md5 = hashlib.md5(s.encode('utf-8')).hexdigest()
    return md5

def get_fanyi(q):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    salt = '123'
    appid = '20180115000115453'
    secret = 'AHYyafcYLzm3q0fkfQ7z'
    s = appid + q + salt + secret
    sign = string_to_md5(s)
    if pattern.findall(q):
        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?' \
              'q={}&from=zh&to=en&appid={}&salt={}&sign={}'.format(q, appid, salt, sign)
    else:
        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?' \
              'q={}&from=en&to=zh&appid={}&salt={}&sign={}'.format(q, appid, salt, sign)
    r = requests.get(url)
    return r
# contents = get_content('测试数据.xlsx')
# print(contents)
q = '4列白糖颗粒包装机'
r = get_fanyi(q)
print(r.text)