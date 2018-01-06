import time
import sys
import os
from collections import deque
import requests, time, sys, os
from bs4 import BeautifulSoup
import pymongo
from collections import deque
from lxml import etree

word = '''
        asphalt crack machine equipment cracks driveway seal 
        sealer sealcoat sealcoating machines paving trucks 
        truck paver pavers
        '''

print(word.split())