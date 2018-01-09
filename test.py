import time
import sys
import os
from collections import deque
import requests, time, sys, os
from bs4 import BeautifulSoup
import pymongo
from collections import deque
from lxml import etree
def get_html(url, tries=5):
    try:
        request = requests.get(url, timeout=60)
        # raise_for_status(), 如果不是 200 会抛出 HTTPError 错误
        request.raise_for_status()
        html = request.text
    except requests.HTTPError as e:
        html = None
        print(e)
        if tries > 0:
            # 如果不是 200 就重试，每次递减重试次数
            time.sleep(60)
            print('正在重试，还剩{}次'.format(tries))
            return get_html(url, tries - 1)
            # 如果 url 不存在会抛出 ConnectionError 错误，这个情况不做重试
    except requests.exceptions.ConnectionError as e:
        return
    return html
url = 'http://www.webcrawler.com/serp?q=asphalt+chip+seal&page=1'
html = get_html(url)
soup = BeautifulSoup(html,'html.parser')
sidebar = soup.select('div.sidebar .result a.title')
sidebar = list(map(lambda x:x.get_text(),sidebar))
print(sidebar)