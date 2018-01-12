import requests, time, sys, os
from bs4 import BeautifulSoup
import pymongo
from openpyxl import load_workbook
from config import *
from collections import deque

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn[db_name]
collection_name = db[collection_name]


def get_html(url, tries=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Accept-Language': 'en-US'
    }
    try:
        request = requests.get(url, headers=headers, timeout=60)
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
        titles = soup.select('.PartialSearchResults-item-title')
        descriptions = soup.select('.PartialSearchResults-item-abstract')
        titles = list(map(lambda x: x.get_text(), titles))
        descriptions = list(map(lambda x: x.get_text(), descriptions))
    except Exception as why:
        print(why)
        print('未匹配到')
        return
    return titles, descriptions


def save_content(html):
    titles, descriptions = parse_html(html)
    for t, d in zip(titles, descriptions):
        data = {
            'title': t,
            'description': d
        }
        collection_name.insert(data)
    print('已写入数据库！')


def parse_txt_to_url():
    keywords = deque()
    with open('unseen_keywords.txt', 'r') as f:
        content = f.read()
        if content:
            for key in content.strip().split('\n'):
                if not '+' in key:
                    keyword = '+'.join(key.split())
                    keywords.append(keyword)
                else:
                    keywords.append(key)
        else:
            print('没有关键字了')
    return keywords


def parse_db_to_url():
    try:
        sel_key = collection_name.find().limit(-1).skip(0).next()  # 找到最上面的记录
        collection_name.delete_one(sel_key)  # 删掉查过的记录
        keyword = sel_key['keyword']
        with open('seen_keywords.txt', 'a+') as f:
            f.write(str(keyword) + '\n')  # 查过的关键字保存到txt里
        q = '+'.join(keyword.split())
    except Exception as why:
        print(why)
        return
    return q

def parse_excel_to_url():
    contents = deque()
    files = os.listdir()
    for file in files:
        if len(file.split('.'))==2:
            if file.split('.')[1] == 'xlsx':
                wb = load_workbook(str(file))
                ws1 = wb.active
                for i in ws1['A']:
                    if i.value:
                        q = '+'.join(i.value.split())
                        contents.append(q)
    return contents

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    keywords = parse_txt_to_url()
    base_url = 'https://www.smarter.com/web?q={}&page={}'
    try:
        while keywords:
            key = keywords.popleft()
            urls = [base_url.format(key, page) for page in range(1, 4)]
            for url in urls:
                html = get_html(url)
                print('正在获取链接{}的内容'.format(url))
                save_content(html)
    except Exception as why:
        print(why)
        with open('unseen_keywords.txt','w') as f:
            while keywords:
                f.write(keywords.popleft()+'\n')
        print('出错了，还好未搜索的关键词保存了')
        print('稍等片刻，2min后自动重启哦')
        time.sleep(120)
        restart_program()
    else:
        print('爬取完毕！爬虫程序正常退出...')
