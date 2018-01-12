import requests
import pymongo
from collections import deque
import sys, os, time


# from get_proxies import get_arandom_ip

def get_html(url, tries=5):
    # proxies = get_arandom_ip()
    try:
        request = requests.get(url, timeout=60)
        # raise_for_status(), 如果不是 200 会抛出 HTTPError 错误
        request.raise_for_status()
        html = request.json()
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


class createMongo(object):

    def __init__(self):
        conn = pymongo.MongoClient('127.0.0.1', 27017)
        db = conn['avira']
        self.contents = db['paver_contents']
        webcrawler = conn['webcrawler']
        self.asphalt_avira_seen_keys = webcrawler['paver_avira_seen_keys']

    def save_data(self, html):
        for baseuri in html['results']:
            title = baseuri.get('title', 'none')
            abstract = baseuri.get('abstract', 'none')
            db_data = {
                'title': title,
                'description': abstract
            }
            self.contents.insert(db_data)
        print('已写入数据库')

    def parse_db_to_url(self):
        try:
            sel_key = self.asphalt_avira_seen_keys.find().limit(-1).skip(0).next()  # 找到最上面的记录
            self.asphalt_avira_seen_keys.delete_one(sel_key)  # 删掉查过的记录
            keyword = sel_key['keyword']
            with open('avira_seen_keywords.txt', 'a+') as f:
                f.write(str(keyword) + '\n')  # 查过的关键字保存到txt里
            q = '+'.join(keyword.split())
        except Exception as why:
            print(why)
            return None
        return q

def parse_txt_to_url():
    keywords_deque = deque()
    source = 'seen_keywords.txt'
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
    start = time.time()
    # keywords = parse_txt_to_url()
    base_url = 'https://search.avira.com/web?q={}&p={}&l=en_US'
    avira = createMongo()
    try:
        # while keywords:
        #     q = keywords.popleft()
        while 1:
            time.sleep(2)
            q = avira.parse_db_to_url()
            if q is None:
                break
            urls = [base_url.format(q, page) for page in range(1, 4)]
            for url in urls:
                html = get_html(url)
                print('读取链接{}'.format(url))
                avira.save_data(html)
    except Exception as why:
        print(why)
        print('正在等待2分钟后重启...')
        time.sleep(120)
        restart_program()
    else:
        print('爬取完毕！爬虫程序正常退出...')
    print('共耗时{}'.format(time.time()-start))
    time.sleep(600)
    restart_program()