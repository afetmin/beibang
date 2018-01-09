from collections import deque
import requests, time, sys, os
from bs4 import BeautifulSoup
import pymongo


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


def get_content(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        sidebar = soup.select('div.sidebar .result a.title')
        if len(sidebar) > 0:
            sidebars = list(map(lambda x: x.get_text(), sidebar))
        else:
            sidebars = sidebar
        titles = list(map(lambda x: x.get_text(), soup.select('div.results div.result a.title')))
        dess = list(map(lambda x: x.get_text(), soup.select('.result span')))[1::2]
    except Exception as why:
        print(why)
        print('未匹配到')
        return
    return sidebars, titles, dess


class connectDb(object):

    def __init__(self, col_name='asphalt'):
        conn = pymongo.MongoClient('127.0.0.1', 27017)
        db = conn['webcrawler']
        self.find_keys = db[str(col_name) + '_keys']
        self.contents = db[str(col_name) + '_contents']
        self.seen_keys = db[str(col_name) + '_bing_seen_keys']
        self.other_seen_keys = db[str(col_name) + '_avira_seen_keys']

    def save_content(self, html):
        main_words = '''
                    asphalt machine equipment cracks driveway 
                    sealer sealcoat sealant machines paving bitumen 
                    paver pavers road
                    '''
        keywords, titles, des = get_content(html)
        if len(keywords):
            for keyword in keywords:
                key_data = {
                    'keyword': keyword
                }
                if any(key in keyword.split() for key in main_words.split()):
                    self.find_keys.insert(key_data)
        print('关键词已写入')
        for t, d in zip(titles, des):
            main_data = {
                'title': t,
                'description': d
            }
            self.contents.insert(main_data)
        print('已写入数据库')

    def parse_db_to_url(self):
        base_url = 'http://www.webcrawler.com/serp?q={}&page={}'
        try:
            sel_key = self.find_keys.find().limit(-1).skip(0).next()  # 找到最上面的记录
            self.find_keys.delete_one(sel_key)  # 删掉查过的记录
            self.seen_keys.insert(sel_key)
            self.other_seen_keys.insert(sel_key)
            keyword = sel_key['keyword']
            q = '+'.join(keyword.split())
            urls = [base_url.format(q, page) for page in range(1, 4)]
            print('获得一个URL列表{}'.format(urls))
        except Exception as why:
            print(why)
            return None
        return urls


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    start = time.time()
    start_url = 'http://www.webcrawler.com/serp?q=asphalt+crack+filling+machine&page=1'
    try:
        start_html = get_html(start_url)
        conndb = connectDb()
        conndb.save_content(start_html)
        while 1:
            urls = conndb.parse_db_to_url()
            if urls is None:
                print('没有关键字了')
                break
            for url in urls:
                html = get_html(url)
                conndb.save_content(html)
    except Exception as why:
        print(why)
        print('正在等待5分钟后重启...')
        time.sleep(300)
        restart_program()
    else:
        print('爬取完毕！程序正常退出...')

    print('共耗时{}'.format(time.time()-start))
    time.sleep(600)
    restart_program()