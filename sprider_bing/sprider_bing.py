import requests, time, sys, os
from bs4 import BeautifulSoup
import pymongo
from collections import deque


# from get_proxies import get_arandom_ip


def get_html(url, tries=5):
    # proxies = get_arandom_ip()
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


def parse_html(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.select('.b_algo h2')
        descriptions = soup.select('.b_caption p')
        next_page = soup.select('.sb_pagF a')
        # sidebars = soup.find_all('div.b_rrsr>ul>li>a')
        # sidebars = list(map(lambda x: x.get_text().strip(), sidebars))
        titles = list(map(lambda x: x.get_text(), titles))
        descriptions = list(map(lambda x: x.get_text(), descriptions))
    except Exception as why:
        print(why)
        print('未匹配到')
        return
    print(next_page)
    print(titles)
    print(descriptions)

url = 'https://www.bing.com/search?q=asphalt+chip+sealer&ensearch=1'
html = get_html(url)
parse_html(html)