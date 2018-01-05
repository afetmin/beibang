from bs4 import BeautifulSoup
import requests, time
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
    soup = BeautifulSoup(html.text, 'html.parser')
    title = list(map(lambda x: x.get_text(), soup.select('.result a.title')))
    des = list(map(lambda x: x.get_text(), soup.select('.result span')))[1::2]
    return title, des


class createMongo(object):

    def __init__(self, db_name):
        conn = pymongo.MongoClient('127.0.0.1', 27017)
        db = conn['monstercrawler']
        self.contents = db[str(db_name) + '_contents']

    def save_data(self, html):
        titles, des = parse_html(html)
        for t, d in zip(titles, des):
            data = {
                'title': t,
                "description": d
            }
            self.contents.insert(data)
        print('已写入数据库')


def parse_txt_to_url():
    url_list = []
    keywords_list = []
    source = 'main_keywords.txt'
    with open(source, 'r') as f:
        content = f.read()
        for key in content.split('\n'):
            keyword = '+'.join(key.split())
            keywords_list.append(keyword)
    for q in keywords_list:
        urls = ['http://www.webcrawler.com/serp?q={}&page={}'.format(q, page) for page in range(1, 4)]
        url_list.extend(urls)
    return url_list, keywords_list


if __name__ == '__main__':
    url_list, keywords_list = parse_txt_to_url()

url = 'http://www.webcrawler.com/serp?q=asphalt+chip+sealer&page=3'
html = get_html(url)
parse_html(html)
