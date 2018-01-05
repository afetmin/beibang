import time
import sys
import os
from collections import deque
import requests, time, sys, os
from bs4 import BeautifulSoup
import pymongo
from collections import deque
from lxml import etree

url = 'https://www.bing.com/search?q=asphalt+chip+sealer&ensearch=1'
r = requests.get(url)
tree = etree.HTML(r.content)
sidebar = tree.xpath("//*[@id='b_results']/li[position()=10]/div/div/div[count(./.)>0]")
print(sidebar)
for n in sidebar:
	print(n.text)