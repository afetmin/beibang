#coding:utf-8
"""
将txt关键词清洗一遍，保留想要的关键词
"""
word = '''
        asphalt crack machine equipment cracks driveway seal 
        sealer sealcoat sealcoating machines paving trucks 
        truck paver pavers
        '''
import time
def wash_keywords():
    with open('seen_keywords.txt', 'r') as f:
        content = f.read()
    with open('wash_keywords.txt', 'w') as fp:
        for keywords in content.strip().split('\n'):
            if any(key in keywords.split() for key in word.split()):
                fp.write(keywords + '\n')


def hasnumbers(keywords):
    return any(char.isdigit() for char in keywords.split())


def wash_numbers():
    with open('wash_keywords.txt', 'r') as f:
        content = f.read()
    with open('result_keywords.txt', 'w') as fp:
        for keywords in content.strip().split('\n'):
            if not hasnumbers(keywords):
                fp.write(keywords + '\n')
start = time.time()
wash_keywords()
wash_numbers()
print('共耗时{}'.format(time.time()-start))