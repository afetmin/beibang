from count_mongo import countMongo
from pymongo import MongoClient
def count_monster():
    monster = countMongo('monstercralwer', 'crack_sealing_machine_contents','crack_sealing_machine_keys')
    monster.count()

def count_avira():
    avira = countMongo('avira', 'avira_contents')
    avira.count()


# count_avira()
# count_monster()

