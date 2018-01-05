from count_mongo import countMongo

def count_monster():
    monster = countMongo('monstercrawler', 'crack+sealing+machine_contents','crack+sealing+machine_keys')
    monster.count()

def count_avira():
    avira = countMongo('avira', 'avira_contents')
    avira.count()


count_avira()
# count_monster()