import requests, time
from bs4 import BeautifulSoup
import pymongo


def get_html(url, tries=5):
    try:
        html = requests.get(url, timeout=10)
    except TimeoutError as why:
        time.sleep(10)
        if tries > 0:
            return get_html(url, tries=tries - 1)  # 重试
        else:
            print(why)
    finally:
        pass
    return html


def parse_html(html):
    try:
        soup = BeautifulSoup(html.text, 'html.parser')
        resultTitles = soup.select('.resultTitle')
        resultDes = soup.select('.resultDescription')
        searchAdresults = soup.select('.aylfResult')
        searchAdresults = list(map(lambda x: x.get_text().strip(), searchAdresults))
    except BaseException as why:
        print(why)
        print('未匹配到')
        pass
    resultTitles = list(map(lambda x: x.get_text(), resultTitles))
    resultDes = list(map(lambda x: x.get_text(), resultDes))

    return resultTitles, resultDes, searchAdresults


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

    def parse_url(self):
        base_url = 'http://search.monstercrawler.com/monster33/search/web?q={}'
        try:
            sel_key = self.find_keys.find().limit(-1).skip(0).next()  # 找到最上面的记录
            self.find_keys.delete_one(sel_key)  # 删掉查过的记录
            keyword = sel_key['keyword']
            with open('seen_keywords.txt', 'a+') as f:
                f.write(str(keyword) + '\n')  # 查过的关键字保存到txt里
            q = '+'.join(keyword.split())
            url = base_url.format(q)
            print('获得一条解析后的URL:%s' % url)
        except BaseException as why:
            print(why)
            pass
        return url


def parse_txt_to_url():
    keywords_list = []
    source = 'main_keywords.txt'
    with open(source, 'r') as f:
        content = f.read()
        for key in content.split('\n'):
            keyword = '+'.join(key.split())
            keywords_list.append(keyword)
    return keywords_list


if __name__ == '__main__':
    for q in parse_txt_to_url():
        createmongo = createMongo(q)
        print('创建了数据库表 {}_keys 和 {}_contents'.format(q, q))
        start_url = 'http://search.monstercrawler.com/monster33/search/web?q={}'.format(q)
        print('正在抓取关于关键词 {} 的内容'.format(q))
        html = get_html(start_url)
        createmongo.save_data(html)
        n = 0
        while n < 200:
            url = createmongo.parse_url()
            web = get_html(url)
            createmongo.save_data(web)
            n += 1
