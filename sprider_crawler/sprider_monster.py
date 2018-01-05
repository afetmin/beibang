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
        resultTitles = soup.select('.resultTitle')
        resultDes = soup.select('.resultDescription')
        searchAdresults = soup.select('.aylfResult')
        searchAdresults = list(map(lambda x: x.get_text().strip(), searchAdresults))
        resultTitles = list(map(lambda x: x.get_text(), resultTitles))
        resultDes = list(map(lambda x: x.get_text(), resultDes))
    except Exception as why:
        print(why)
        print('未匹配到')
        return

    return resultTitles, resultDes, searchAdresults


def parse_other_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = list(map(lambda x: x.get_text(), soup.select('.result a.title')))
    des = list(map(lambda x: x.get_text(), soup.select('.result span')))[1::2]
    return title, des


class createMongo(object):

    def __init__(self, db_name):
        conn = pymongo.MongoClient('127.0.0.1', 27017)
        db = conn['monstercrawler']
        self.find_keys = db[str(db_name) + '_keys']
        self.contents = db[str(db_name) + '_contents']

    def save_data(self, html):
        titles, des, keywords = parse_html(html)
        for keyword in keywords:
            key_data = {
                'keyword': keyword
            }
            if not 'chip' in keyword.split():  # 过滤带有chip字段的关键词
                self.find_keys.insert(key_data)
        for t, d in zip(titles, des):
            main_data = {
                'title': t,
                'description': d
            }
            self.contents.insert(main_data)
        print('已写入数据库')

    def save_other_data(self, html):
        titles, des = parse_other_html(html)
        for t, d in zip(titles, des):
            data = {
                'title': t,
                "description": d
            }
            self.contents.insert(data)
        print('其他搜索结果已写入数据库')

    def parse_db_to_url(self):
        base_url = 'http://search.monstercrawler.com/monster33/search/web?q={}'
        other_url = 'http://www.webcrawler.com/serp?q={}&page={}'
        try:
            sel_key = self.find_keys.find().limit(-1).skip(0).next()  # 找到最上面的记录
            self.find_keys.delete_one(sel_key)  # 删掉查过的记录
            keyword = sel_key['keyword']
            with open('seen_keywords.txt', 'a+') as f:
                f.write(str(keyword) + '\n')  # 查过的关键字保存到txt里
            q = '+'.join(keyword.split())
            url = base_url.format(q)
            other_urls = [other_url.format(q, page) for page in range(1, 4)]
            print('获得一个其他搜索引擎列表！')
            print('获得一条解析后的URL:%s' % url)
        except Exception as why:
            print(why)
            return
        return url, other_urls


def parse_txt_to_url():
    keywords_deque = deque()
    source = 'main_keywords.txt'
    with open(source, 'r') as f:
        content = f.read()
        if not content is None:
            for key in content.strip().split('\n'):
                if not '+' in key:
                    keyword = '+'.join(key.split())
                    keywords_deque.append(keyword)
                else:
                    keywords_deque.append(key)
        else:
            print('没有关键字了')
    return keywords_deque


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    keywords_list = parse_txt_to_url()
    try:
        while keywords_list:
            q = keywords_list.popleft()
            createmongo = createMongo(q)
            print('创建了数据库表 {}_keys 和 {}_contents'.format(q, q))
            start_url = 'http://search.monstercrawler.com/monster33/search/web?q={}'.format(q)
            print('正在抓取关于关键词 {} 的内容'.format(q))
            html = get_html(start_url)
            createmongo.save_data(html)
            n = 0
            while n < 200:
                url, other_urls = createmongo.parse_db_to_url()
                web = get_html(url)
                createmongo.save_data(web)
                for other_url in other_urls:
                    other_web = get_html(other_url)
                    createmongo.save_other_data(other_web)
                n += 1
    except Exception as why:
        print(why)
        with open('main_keywords.txt', 'w') as f:
            f.write(q + '\n')
            while keywords_list:
                f.write(keywords_list.popleft() + '\n')
        print('正在等待2分钟后重启...')
        time.sleep(120)
        restart_program()
    else:
        print('爬取完毕！程序正常退出...')

