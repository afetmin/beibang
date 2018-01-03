import requests
from bs4 import BeautifulSoup
import pymongo

start_url = 'https://global.bing.com/search?q=asphalt+chip+sealer&qs=ds&first=1&ensearch=1'


# proxies = {
#     'https': 'socks5://livps:Li021011@!@127.0.0.1:7070',
#     'http': 'socks5://livps:Li021011@!@127.0.0.1:7070'
# }

def get_html(url):
    try:
        html = requests.get(url, timeout=10)
    except TimeoutError as why:
        print(why)
        pass
    return html


# def parse_html(html):
#     try:
html = get_html(start_url)


soup = BeautifulSoup(html.text,'html.parser')
titles = list(map(lambda x:x.get_text(),soup.select('.b_algo h2')))
contents = list(map(lambda x:x.get_text(),soup.select('.b_caption p')))
vlists = soup.select('.b_rich')
print(titles)
print(vlists,len(vlists))
