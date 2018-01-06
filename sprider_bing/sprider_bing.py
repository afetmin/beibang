import requests, time, sys, os
from bs4 import BeautifulSoup
import pymongo
from collections import deque

# from get_proxies import get_arandom_ip
conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn['bing']
bing = db['bing_contents']


def get_html(url, tries=5):
    # proxies = get_arandom_ip()
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1',
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
    base_url = 'https://global.bing.com{}'
    try:
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.select('.b_algo h2')
        descriptions = soup.select('.b_caption p')
        next_page = soup.select('li.b_pag a')[1:3]
        page_urls = list(map(lambda x: x.get('href'), next_page))
        page_urls = [base_url.format(page_url) for page_url in page_urls]
        titles = list(map(lambda x: x.get_text(), titles))
        descriptions = list(map(lambda x: x.get_text(), descriptions))
    except Exception as why:
        print(why)
        print('未匹配到')
        return
    return titles, descriptions, page_urls


def save_content(html):
    titles, descriptions, page_urls = parse_html(html)
    for t, d in zip(titles, descriptions):
        data = {
            'title': t,
            'description': d
        }
        bing.insert(data)
    for url in page_urls:
        html_content = get_html(url)
        titles, descriptions, page_urls = parse_html(html_content)
        for t, d in zip(titles, descriptions):
            data = {
                'title': t,
                'description': d
            }
            bing.insert(data)
    print('已写入数据库！')


def parse_txt_to_url():
    keywords_deque = deque()
    with open('keywords.txt', 'r') as f:
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
    keywords = parse_txt_to_url()
    base_url = 'https://global.bing.com/search?q={}&ensearch=1'
    try:
        while keywords:
            q = keywords.popleft()
            url = base_url.format(q)
            html = get_html(url)
            print('正在获取链接{}的内容'.format(url))
            save_content(html)
    except Exception as why:
        print(why)
        with open('keywords.txt', 'w') as f:
            while keywords:
                f.write(keywords.popleft() + '\n')
        print('正在等待2分钟后重启...')
        time.sleep(120)
        restart_program()
    else:
        print('爬取完毕！爬虫程序正常退出...')
    print('共耗时{}'.format(time.time() - start))
