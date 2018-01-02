import requests, time
from bs4 import BeautifulSoup
import pymongo


def get_html(url):
    try:
        html = requests.get(url, timeout=10)
    except TimeoutError as why:
        print(why)
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


conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn['sprider']
find_keys = db['find_keys']
asphalt = db['asphaltler']


def save_data(html):
    titles, des, keywords = parse_html(html)
    for keyword in keywords:
        key_data = {
            'keyword': keyword
        }
        find_keys.insert(key_data)
    for t, d in zip(titles, des):
        main_data = {
            'title': t,
            'description': d
        }
        asphalt.insert(main_data)
    print('已写入数据库')


def parse_url():
    base_url = 'http://search.monstercrawler.com/monster33/search/web?q={}'
    try:
        sel_key = find_keys.find().limit(-1).skip(0).next()  # 找到最上面的记录
        find_keys.delete_one(sel_key)  # 删掉查过的记录
        keyword = sel_key['keyword']
        with open('seen_keywords.txt', 'a+') as f:
            f.write(str(keyword)+'\n')  # 查过的关键字保存到txt里
        q = '+'.join(keyword.split())
        url = base_url.format(q)
        print('获得一条解析后的URL:%s'%url)
    except BaseException as why:
        print(why)
        pass
    return url


if __name__ == '__main__':
    start_url = 'http://search.monstercrawler.com/monster33/search/web?q=asphalt+chip+sealer'
    html = get_html(start_url)
    save_data(html)
    n = 0
    while n < 200:
        url = parse_url()
        web = get_html(url)
        save_data(web)
        n += 1
