import re, time

import requests, trip

@trip.coroutine
def get_proxies(number=10):
    r = yield trip.get('http://www.89ip.cn/apijk/' +
        '?&tqsl=%s&sxa=&sxb=&tta=&ports=&ktip=&cf=1' % number)
    p = re.findall('((?:\d{1,3}.){3}\d{1,3}:\d+)', r.text)
    raise trip.Return(p)

@trip.coroutine
def test_proxy(proxy):
    try:
        r = yield trip.get('http://httpbin.org/get', timeout=5,
            proxies={ 'http': proxy, 'https': proxy })
        if 'httpbin.org' not in r.text:
            raise Exception('Invalid reply')
    except Exception as e:
        pass
    else:
        raise trip.Return(proxy)

def main():
    proxies = yield get_proxies(100)
    r = yield [test_proxy(p) for p in proxies]
    print(filter(lambda x: x, r))

start_time = time.time()
trip.run(main)
print(time.time() - start_time)